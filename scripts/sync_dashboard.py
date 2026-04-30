"""Sync the UnitySVC Labs provider catalog dashboard.

Reads from three sources and writes to two surfaces:

Sources
-------
1. **GitHub** (via ``gh`` CLI) —
   - public ``unitysvc-services-*`` repos in ``unitysvc-labs``
   - tracking issues in ``unitysvc-labs/unitysvc-labs`` (one per repo)
     with ``status:`` / ``type:`` / ``reselling:`` labels
   - latest ``ci.yml`` workflow conclusion per repo
   - open PR count per repo
2. **Backend** (via ``usvc_seller services list --provider X``,
   *optional* — skipped when ``UNITYSVC_SELLER_API_KEY`` is unset) —
   active service count per provider.
3. **(future)** repo-emitted ``status.json`` artifact for ``data
   validate`` results — *not yet wired*; placeholder column rendered as
   "—" until the per-repo CI step lands.

Surfaces
--------
1. ``profile/README.md`` — replaces content between the
   ``<!-- providers-start -->`` / ``<!-- providers-end -->`` markers
   with a Markdown table.  Public repos only.
2. ``unitysvc-labs/unitysvc-labs/issues/{N}`` — sticky comment per
   tracking issue (matched by a ``<!-- provider-status-sync -->`` HTML
   marker so reruns edit instead of accumulating).  All repos
   (including private), since the issue tracker is private.

Run modes
---------
- ``python scripts/sync_dashboard.py`` — full sync (reads, renders,
  writes both surfaces).
- ``python scripts/sync_dashboard.py --dry-run`` — print the rendered
  Markdown to stdout; touch nothing.

Cross-repo authentication
-------------------------
- Reading public repos: anonymous ``gh`` works.
- Reading the private ``unitysvc-labs/unitysvc-labs`` issues: needs
  ``GH_TOKEN`` set to a PAT with repo:read scope across the org.  The
  workflow injects this from ``secrets.LABS_DASHBOARD_TOKEN``.
- Writing to ``profile/README.md`` in *this* repo: the workflow's
  default ``GITHUB_TOKEN`` is enough.
- Writing comments on cross-repo issues: needs the same PAT as for
  reading them.

Idempotence
-----------
README is replaced only between markers; reruns are byte-identical
when source data is unchanged.  Sticky comments use a marker so
reruns edit the same comment.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ORG = "unitysvc-labs"
ISSUE_REPO = f"{ORG}/unitysvc-labs"
README_PATH = Path("profile/README.md")
SECTION_START = "<!-- providers-start -->"
SECTION_END = "<!-- providers-end -->"
COMMENT_MARKER = "<!-- provider-status-sync -->"

# Repo prefix that identifies a tracked services data repo.
REPO_PREFIX = "unitysvc-services-"


@dataclass
class ProviderRow:
    """One row in the dashboard table — one services repo."""

    repo: str  # e.g. "unitysvc-services-anthropic"
    is_public: bool
    is_archived: bool
    issue_number: int | None
    issue_title: str  # human-readable provider name (e.g. "Anthropic")
    type_labels: list[str]  # e.g. ["llm", "image"] from the tracking issue
    ci_conclusion: str | None  # "success" / "failure" / "in_progress" / None
    open_pr_count: int
    # Service-level signals from ``usvc_seller services list``.  Populated
    # when ``UNITYSVC_SELLER_API_KEY`` is set; empty dicts otherwise (cells
    # render as ``—``).  Counts are by enum value.  Unknown / extra keys
    # pass through so future enum values automatically appear in the table.
    lifecycle_counts: dict[str, int]  # by ServiceStatusEnum value
    visibility_counts: dict[str, int]  # by ServiceVisibilityEnum value
    mode_counts: dict[str, int]  # by enrollment mode (TODO: see fetch_mode_counts)


def gh(*args: str) -> str:
    """Run ``gh`` and return stdout, raising on non-zero exit.

    Authentication comes from ``GH_TOKEN`` (workflow-injected PAT) or
    the user's local ``gh auth`` cache.
    """
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def list_services_repos() -> list[dict[str, Any]]:
    """All ``unitysvc-services-*`` repos in the labs org, public or private."""
    out = gh(
        "repo",
        "list",
        ORG,
        "--limit",
        "200",
        "--json",
        "name,visibility,isArchived,description",
    )
    data = json.loads(out)
    return [r for r in data if r["name"].startswith(REPO_PREFIX)]


def list_tracking_issues() -> list[dict[str, Any]]:
    """All issues in the issue-tracker repo, with body and labels."""
    out = gh(
        "issue",
        "list",
        "--repo",
        ISSUE_REPO,
        "--state",
        "all",
        "--limit",
        "200",
        "--json",
        "number,title,body,labels",
    )
    return json.loads(out)


def fetch_issue_comments(issue_number: int) -> list[str]:
    """Comment bodies for one issue.  Used to find ``Repo:`` mentions
    on pre-existing issues that don't have the link in their body.
    """
    out = gh(
        "issue",
        "view",
        str(issue_number),
        "--repo",
        ISSUE_REPO,
        "--json",
        "comments",
    )
    return [c["body"] for c in json.loads(out).get("comments", [])]


def build_repo_to_issue_map(issues: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Match ``unitysvc-services-X`` repos to their tracking issues.

    The ``unitysvc-services-X`` reference may appear in the issue body
    (new-style issues created by this PR) or in a comment (older issues
    where I added a ``Repo:`` comment retroactively).  Both shapes use
    the same backtick-fenced repo name pattern.
    """
    pattern = re.compile(rf"`({re.escape(REPO_PREFIX)}[A-Za-z0-9._-]+)`")
    mapping: dict[str, dict[str, Any]] = {}

    for issue in issues:
        repos: set[str] = set(pattern.findall(issue.get("body") or ""))
        if not repos:
            for comment_body in fetch_issue_comments(issue["number"]):
                repos |= set(pattern.findall(comment_body))
        for repo in repos:
            # Earliest issue wins on ties (chronological stability).
            mapping.setdefault(repo, issue)
    return mapping


def label_value(labels: list[dict[str, Any]], prefix: str) -> str | None:
    """First label whose name starts with ``<prefix>: ``, prefix stripped."""
    needle = f"{prefix}: "
    for lbl in labels:
        name = lbl["name"]
        if name.startswith(needle):
            return name[len(needle) :]
    return None


def label_values(labels: list[dict[str, Any]], prefix: str) -> list[str]:
    """All label values matching the ``<prefix>: `` namespace."""
    needle = f"{prefix}: "
    return [lbl["name"][len(needle) :] for lbl in labels if lbl["name"].startswith(needle)]


def fetch_ci_conclusion(repo: str) -> str | None:
    """Latest workflow run conclusion on the default branch.

    Returns the ``conclusion`` field (``success`` / ``failure`` /
    ``cancelled`` / …) or ``None`` if no runs exist.  We do *not*
    filter by workflow name — the dashboard reflects whatever the
    repo's most-recent CI declared, not a specific job.
    """
    try:
        out = gh(
            "run",
            "list",
            "--repo",
            f"{ORG}/{repo}",
            "--branch",
            "main",
            "--limit",
            "1",
            "--json",
            "conclusion,status",
        )
    except RuntimeError:
        return None
    runs = json.loads(out)
    if not runs:
        return None
    run = runs[0]
    # Still running → no conclusion yet.
    return run.get("conclusion") or run.get("status")


def fetch_open_pr_count(repo: str) -> int:
    """Number of open PRs on a repo.  Bot/auto-PRs count too — they
    *are* the signal: a stale auto-update PR is a maintenance gap."""
    try:
        out = gh(
            "pr",
            "list",
            "--repo",
            f"{ORG}/{repo}",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number",
        )
    except RuntimeError:
        return 0
    return len(json.loads(out))


def fetch_service_breakdown(
    provider_name: str,
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    """Lifecycle / visibility / mode counts via ``usvc_seller services list``.

    One paginated call per provider — ``--all`` follows cursors so the
    counts cover the whole catalog, not just the first page.  Returns
    three dicts:

    1. ``lifecycle`` keyed by :class:`ServiceStatusEnum` values
       (``active``, ``draft``, ``review``, ``deprecated``, ``pending``,
       ``rejected``, ``suspended``).
    2. ``visibility`` keyed by :class:`ServiceVisibilityEnum` values
       (``public``, ``unlisted``, ``private``).  ``public`` is rendered
       as "published" in the README to match operator vocabulary.
    3. ``mode`` keyed by enrollment mode (``managed``, ``byok``,
       ``byoe``).  **Currently always empty** — see
       ``fetch_mode_counts`` TODO below.

    All three default to ``{}`` when the seller API isn't reachable
    (no key, CLI missing, network error) so the rest of the dashboard
    stays usable.
    """
    if not os.environ.get("UNITYSVC_SELLER_API_KEY"):
        return {}, {}, {}
    if shutil.which("usvc_seller") is None:
        return {}, {}, {}

    try:
        result = subprocess.run(
            [
                "usvc_seller",
                "services",
                "list",
                "--provider",
                provider_name,
                "--all",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return {}, {}, {}
        services = json.loads(result.stdout)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}, {}, {}

    lifecycle: dict[str, int] = {}
    visibility: dict[str, int] = {}
    for svc in services:
        status = svc.get("status")
        if status:
            lifecycle[status] = lifecycle.get(status, 0) + 1
        vis = svc.get("visibility")
        if vis:
            visibility[vis] = visibility.get(vis, 0) + 1

    mode = fetch_mode_counts(provider_name, services)
    return lifecycle, visibility, mode


def fetch_mode_counts(
    provider_name: str, services: list[dict[str, Any]]
) -> dict[str, int]:
    """Counts by enrollment mode (managed / byok / byoe).

    TODO(post-merge): ``ServicePublic`` doesn't surface enrollment mode
    today.  Mode is encoded in the *offering's* ``upstream_access_config``:

    - all fields use ``${ secrets.X }`` → **managed**
    - ``api_key`` uses ``${ customer_secrets.X }``, others ``${ secrets.X }`` → **byok**
    - ``base_url`` (or ``host``) uses ``${ customer_secrets.X }`` → **byoe**

    Computing this on the dashboard requires either:

    1. **An N+1 detail fetch per service** (~50–100 calls per cron
       run, fine but wasteful) — use ``client.services.get(id)`` and
       inspect ``offering.upstream_access_config``.
    2. **A new SDK / list-endpoint field** that returns the derived
       mode alongside ``status`` / ``visibility``.  Cleaner; needs
       backend change.
    3. **Local repo inspection**: clone each ``unitysvc-services-*``
       repo, walk its data tree, parse offerings.  Heavier but no
       extra API surface.

    For now this returns ``{}`` so the column renders as ``—``.  See
    the dashboard PR discussion for which path you want.
    """
    del provider_name, services  # unused until one of the paths above lands
    return {}


def repo_to_provider_name(repo: str, issue_title: str) -> str:
    """Provider-name slug to pass to ``usvc_seller services list --provider``.

    The seller CLI does case-insensitive partial matching, so the slug
    after ``unitysvc-services-`` (e.g. ``anthropic``, ``mistral``)
    matches the seller's ``provider_name`` reliably.  ``issue_title``
    is unused here but kept in the signature so callers can override
    in the future for repos whose slug doesn't match the backend (none
    today).
    """
    del issue_title
    return repo[len(REPO_PREFIX) :]


def collect() -> list[ProviderRow]:
    """Aggregate every data source into one ``ProviderRow`` per repo."""
    repos = list_services_repos()
    issues = list_tracking_issues()
    repo_to_issue = build_repo_to_issue_map(issues)

    rows: list[ProviderRow] = []
    for r in repos:
        repo_name = r["name"]
        issue = repo_to_issue.get(repo_name)
        labels = (issue or {}).get("labels", [])

        # Skip the seller-API call entirely for archived repos — they
        # don't have live services on the gateway, and the call would
        # just waste a round-trip returning an empty list.
        if r["isArchived"]:
            lifecycle, visibility, mode = {}, {}, {}
        else:
            lifecycle, visibility, mode = fetch_service_breakdown(
                repo_to_provider_name(repo_name, "")
            )

        rows.append(
            ProviderRow(
                repo=repo_name,
                is_public=r["visibility"] == "PUBLIC",
                is_archived=r["isArchived"],
                issue_number=(issue or {}).get("number"),
                issue_title=(issue or {}).get("title") or repo_name[len(REPO_PREFIX) :],
                type_labels=label_values(labels, "type"),
                ci_conclusion=fetch_ci_conclusion(repo_name) if not r["isArchived"] else None,
                open_pr_count=fetch_open_pr_count(repo_name) if not r["isArchived"] else 0,
                lifecycle_counts=lifecycle,
                visibility_counts=visibility,
                mode_counts=mode,
            )
        )

    # Stable sort by display name so README diffs are minimal.
    rows.sort(key=lambda r: r.issue_title.lower())
    return rows


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


_CI_EMOJI = {
    "success": "✅",
    "failure": "❌",
    "cancelled": "⚪",
    "in_progress": "🟡",
    "queued": "🟡",
    "skipped": "⚪",
}

# README maps ``public`` → ``published`` to match operator vocabulary
# (the user said "published / unlisted").  ``private`` is excluded
# from rendering — the public org README never lists private services.
_VISIBILITY_DISPLAY = {
    "public": "published",
    "unlisted": "unlisted",
    # ``private`` intentionally absent — filtered out at render time.
}

# Lifecycle states the user explicitly asked to see, in operator
# priority order (most-actionable first).  Other states (pending,
# rejected, suspended) get appended after these when present.
_LIFECYCLE_PRIMARY = ["active", "draft", "review", "deprecated"]


def _ci_cell(conclusion: str | None) -> str:
    if not conclusion:
        return "—"
    return _CI_EMOJI.get(conclusion, "⚪")


def _pr_cell(count: int) -> str:
    return "—" if count == 0 else str(count)


def _counts_cell(
    counts: dict[str, int],
    *,
    primary_order: list[str] | None = None,
    display_map: dict[str, str] | None = None,
    omit_keys: set[str] | None = None,
) -> str:
    """Render a ``{name: count}`` dict as ``"3 active · 1 review"``.

    - ``primary_order`` lists keys to render first (ones the user cares
      about most); the rest are sorted alphabetically and appended.
    - ``display_map`` overrides the rendered name (e.g. ``public`` →
      ``published``).  Missing keys render as-is.
    - ``omit_keys`` drops keys entirely (used to filter out
      ``private`` from the public README's visibility column).
    - Zero counts are not rendered.  Empty dict / all-zero → ``—``.
    """
    omit = omit_keys or set()
    filtered = {k: v for k, v in counts.items() if v > 0 and k not in omit}
    if not filtered:
        return "—"

    primary = primary_order or []
    ordered_keys = [k for k in primary if k in filtered] + sorted(
        k for k in filtered if k not in primary
    )

    parts = [f"{filtered[k]} {(display_map or {}).get(k, k)}" for k in ordered_keys]
    return " · ".join(parts)


def _lifecycle_cell(counts: dict[str, int]) -> str:
    return _counts_cell(counts, primary_order=_LIFECYCLE_PRIMARY)


def _visibility_cell(counts: dict[str, int]) -> str:
    # Drop ``private`` from public README / sticky comments — irrelevant
    # to the operator who looks at the public catalog.
    return _counts_cell(
        counts,
        primary_order=["public", "unlisted"],
        display_map=_VISIBILITY_DISPLAY,
        omit_keys={"private"},
    )


def _mode_cell(counts: dict[str, int]) -> str:
    return _counts_cell(counts, primary_order=["managed", "byok", "byoe"])


def render_readme_table(rows: list[ProviderRow]) -> str:
    """Public-only summary table for the org README.

    Private + archived repos are intentionally omitted — those are
    surfaced on the per-issue sticky comments instead.
    """
    public_rows = [r for r in rows if r.is_public and not r.is_archived]

    lines = [
        "| Provider | Repo | Type | Lifecycle | Visibility | Mode | Validate | Open PRs |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in public_rows:
        repo_link = f"[`{r.repo}`](https://github.com/{ORG}/{r.repo})"
        provider_link = (
            f"[{r.issue_title}](https://github.com/{ISSUE_REPO}/issues/{r.issue_number})"
            if r.issue_number
            else r.issue_title
        )
        type_cell = ", ".join(r.type_labels) if r.type_labels else "—"
        lines.append(
            "| "
            + " | ".join(
                [
                    provider_link,
                    repo_link,
                    type_cell,
                    _lifecycle_cell(r.lifecycle_counts),
                    _visibility_cell(r.visibility_counts),
                    _mode_cell(r.mode_counts),
                    _ci_cell(r.ci_conclusion),
                    _pr_cell(r.open_pr_count),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_issue_comment(row: ProviderRow, timestamp: str) -> str:
    """Sticky-comment body for one tracking issue.

    Includes the marker as the first line so reruns can locate-and-edit
    instead of accumulating new comments.  Unlike the README, sticky
    comments include private repos (the issue tracker is private), so
    the visibility cell here doesn't filter ``private``.
    """
    type_cell = ", ".join(row.type_labels) if row.type_labels else "—"
    visibility_cell = _counts_cell(
        row.visibility_counts,
        primary_order=["public", "unlisted", "private"],
        display_map=_VISIBILITY_DISPLAY,
    )
    return (
        f"{COMMENT_MARKER}\n"
        f"**Provider status snapshot** _(auto-synced {timestamp} UTC)_\n\n"
        f"- Repo: [`{row.repo}`](https://github.com/{ORG}/{row.repo})"
        f" — {'public' if row.is_public else 'private'}"
        f"{' · archived' if row.is_archived else ''}\n"
        f"- Type: {type_cell}\n"
        f"- Lifecycle: {_lifecycle_cell(row.lifecycle_counts)}\n"
        f"- Visibility: {visibility_cell}\n"
        f"- Mode: {_mode_cell(row.mode_counts)}\n"
        f"- Last CI: {_ci_cell(row.ci_conclusion)}\n"
        f"- Open PRs: {_pr_cell(row.open_pr_count)}\n"
    )


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------


def replace_section(readme: str, table: str) -> str:
    """Replace content between the markers; raise if markers missing."""
    pattern = re.compile(
        rf"({re.escape(SECTION_START)})(.*)({re.escape(SECTION_END)})",
        re.DOTALL,
    )
    if not pattern.search(readme):
        raise SystemExit(
            f"Markers {SECTION_START!r} / {SECTION_END!r} not found in README — "
            "the workflow refuses to guess where to write."
        )
    replacement = f"\\1\n{table}\n\\3"
    return pattern.sub(replacement, readme)


def update_sticky_comment(issue_number: int, body: str) -> None:
    """Find a comment carrying the marker; edit if present, post if not.

    ``gh`` doesn't expose comment-by-marker natively, so we list+filter
    via the REST API.  Idempotent: byte-identical body → still POSTs an
    edit (no-op effect on the surface, one API call).
    """
    raw = gh(
        "api",
        f"repos/{ISSUE_REPO}/issues/{issue_number}/comments",
        "--paginate",
    )
    # ``gh api`` paginates by concatenating arrays; parse one or many.
    if raw.strip().startswith("["):
        comments = json.loads(raw)
    else:
        comments = []
        for chunk in re.findall(r"\[.*?\](?=\[|$)", raw, re.DOTALL):
            comments.extend(json.loads(chunk))

    existing = next((c for c in comments if COMMENT_MARKER in (c.get("body") or "")), None)
    if existing:
        gh(
            "api",
            "--method",
            "PATCH",
            f"repos/{ISSUE_REPO}/issues/comments/{existing['id']}",
            "-f",
            f"body={body}",
        )
    else:
        gh(
            "issue",
            "comment",
            str(issue_number),
            "--repo",
            ISSUE_REPO,
            "--body",
            body,
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print rendered Markdown to stdout; touch no files / issues.",
    )
    parser.add_argument(
        "--skip-comments",
        action="store_true",
        help="Update README only (skip cross-repo issue comments).",
    )
    args = parser.parse_args()

    rows = collect()
    table = render_readme_table(rows)

    # Timestamp is generated once per run so README and all sticky
    # comments share the same value.
    from datetime import datetime, timezone

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    if args.dry_run:
        print("=== README table ===")
        print(table)
        print()
        for row in rows:
            if row.issue_number is None:
                continue
            print(f"=== Comment on issue #{row.issue_number} ({row.repo}) ===")
            print(render_issue_comment(row, timestamp))
            print()
        return 0

    # README write
    readme = README_PATH.read_text()
    new_readme = replace_section(readme, table)
    new_readme = re.sub(
        r"_Last synced: [^_]*_",
        f"_Last synced: {timestamp} UTC_",
        new_readme,
    )
    if new_readme != readme:
        README_PATH.write_text(new_readme)
        print(f"Updated {README_PATH}")
    else:
        print(f"{README_PATH} unchanged")

    # Sticky comments (skipped when explicitly requested or when no PAT
    # is configured — the workflow exposes the PAT as GH_TOKEN).
    if args.skip_comments:
        print("Skipping sticky comments (--skip-comments)")
        return 0

    for row in rows:
        if row.issue_number is None:
            print(f"  ⊘ {row.repo}: no tracking issue mapped")
            continue
        try:
            update_sticky_comment(row.issue_number, render_issue_comment(row, timestamp))
            print(f"  ✓ {row.repo} → #{row.issue_number}")
        except RuntimeError as err:
            print(f"  ✗ {row.repo} → #{row.issue_number}: {err}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
