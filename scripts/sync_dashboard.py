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
2. **Backend** (via the ``unitysvc_sellers`` SDK, *optional* —
   skipped when ``UNITYSVC_SELLER_API_KEY`` is unset) — fetches every
   service the API key owns once, then matches them per repo by
   intersecting the SDK's ``service_id`` set with the IDs declared in
   each repo's ``listing.override.json`` files.  This handles
   multi-provider repos (e.g. ``template`` under ``unitysvc-demo``)
   and one-provider-many-repos (``unitysvc-labs`` across http / s3 /
   smtp / ntfy) without naming heuristics.
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
import asyncio
import json
import os
import re
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
    listing_type_counts: dict[str, int]  # by listing_type (regular / byok / self_hosted)


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


async def _list_services_for_provider(
    client: Any, provider_name: str
) -> list[dict[str, Any]]:
    """Pull every service for a provider via the SDK, paging cursors.

    Mirrors the seller CLI's ``services list --provider <name> --all``
    behaviour: server-side pagination via cursor, client-side filter
    on ``provider_name`` (case-insensitive substring) since the
    backend list endpoint doesn't take a provider filter.
    """
    needle = provider_name.lower()
    collected: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        page = await client.services.list(cursor=cursor, limit=200)
        for svc in page.data:
            svc_dict = svc.to_dict() if hasattr(svc, "to_dict") else dict(svc)
            if needle in (svc_dict.get("provider_name") or "").lower():
                collected.append(svc_dict)
        if not getattr(page, "has_more", False):
            break
        next_cursor = getattr(page, "next_cursor", None)
        if not next_cursor or not isinstance(next_cursor, str):
            break
        cursor = next_cursor
    return collected


_services_by_id: dict[str, dict[str, Any]] | None = None


def _populate_services_cache() -> dict[str, dict[str, Any]] | None:
    """Fetch every service once, then index by ``service_id``.

    The seller list endpoint returns *all* services the API key owns
    on each call.  Doing one call per repo would refetch the same N
    rows N times, so we fetch once and index by ID — repos look up
    their services by intersecting this map with the IDs declared
    in their ``listing.override.json`` files.
    """
    api_key = os.environ.get("UNITYSVC_SELLER_API_KEY")
    if not api_key:
        return None

    try:
        from unitysvc_sellers import AsyncClient
    except ImportError as exc:
        print(f"  ⚠ unitysvc_sellers SDK not installed ({exc}); skipping seller data")
        return None

    base_url = os.environ.get("UNITYSVC_SELLER_API_URL")

    async def _fetch_all() -> list[dict[str, Any]]:
        async with AsyncClient(api_key=api_key, base_url=base_url) as client:
            return await _list_services_for_provider(client, "")  # empty filter → all

    try:
        all_services = asyncio.run(_fetch_all())
    except Exception as exc:  # noqa: BLE001 — surface the cause and degrade gracefully
        print(f"  ⚠ Seller SDK call failed ({type(exc).__name__}: {exc}); skipping")
        return None

    by_id = {str(svc["id"]): svc for svc in all_services if svc.get("id")}
    print(f"  ✓ Seller SDK: {len(all_services)} services indexed by id")
    return by_id


# Filename suffix that marks a per-service override file.  These tiny
# JSON files live alongside each listing under
# ``data/<provider>/services/<svc>/listing.override.json`` and carry
# the live ``service_id`` written back by the seller upload step.
OVERRIDE_FILENAME = "listing.override.json"


def fetch_repo_service_ids(repo: str) -> set[str]:
    """Service-IDs declared by this repo, read from override files.

    Walks the repo's git tree once via the GitHub API, filters for
    ``listing.override.json`` paths, and reads ``service_id`` from
    each.  Returns ``set()`` on any failure so the dashboard still
    renders — the cells just go to ``—`` for that repo.
    """
    try:
        tree_raw = gh("api", f"repos/{ORG}/{repo}/git/trees/HEAD?recursive=1")
    except RuntimeError:
        return set()
    try:
        tree = json.loads(tree_raw)
    except json.JSONDecodeError:
        return set()
    if tree.get("truncated"):
        # If a repo ever grows past the GitHub tree-API cap (~100k
        # entries) the dashboard would silently miss late paths.  Flag
        # it so the operator notices before stats start drifting.
        print(f"  ⚠ {repo}: tree response truncated, may miss service_ids")

    paths = [
        node["path"]
        for node in tree.get("tree", [])
        if node.get("type") == "blob"
        and node.get("path", "").endswith(OVERRIDE_FILENAME)
    ]
    if not paths:
        return set()

    ids: set[str] = set()
    for path in paths:
        try:
            raw = gh(
                "api",
                "-H",
                "Accept: application/vnd.github.raw",
                f"repos/{ORG}/{repo}/contents/{path}",
            )
        except RuntimeError:
            continue
        try:
            sid = json.loads(raw).get("service_id")
        except json.JSONDecodeError:
            continue
        if sid:
            ids.add(str(sid))
    return ids


def _breakdown_for_services(
    services: list[dict[str, Any]],
) -> tuple[dict[str, int], dict[str, int], dict[str, int], list[str]]:
    """Compute lifecycle / visibility / listing-type / service-type
    cells for a list of services (the rendering helpers consume the
    output as-is).
    """
    lifecycle: dict[str, int] = {}
    visibility: dict[str, int] = {}
    listing_type: dict[str, int] = {}
    types: set[str] = set()
    for svc in services:
        status = svc.get("status")
        if status:
            # A service with ``revision_of`` set is a revision of another
            # service, not an independent one — bucket it separately so
            # e.g. 3 rejected revisions of an active service don't read
            # as 3 unrelated rejected services.
            key = f"{status} revision" if svc.get("revision_of") else status
            lifecycle[key] = lifecycle.get(key, 0) + 1
        vis = svc.get("visibility")
        # Revisions are staged edits to a live service, not independently
        # routable rows — exclude them from the visibility column entirely
        # so e.g. a provider with 3 published + 3 revisions reads as
        # "3 published" instead of "3 published · 3 unlisted".
        if vis and not svc.get("revision_of"):
            visibility[vis] = visibility.get(vis, 0) + 1
        # Listing type follows the same revision rule as visibility:
        # revisions piggy-back on their parent's listing, so counting
        # them separately would double-count the same listed offering.
        lt = svc.get("listing_type")
        if lt and not svc.get("revision_of"):
            listing_type[lt] = listing_type.get(lt, 0) + 1
        st = svc.get("service_type")
        if st:
            types.add(st)

    return lifecycle, visibility, listing_type, sorted(types)


def fetch_service_breakdown(
    repo: str,
) -> tuple[dict[str, int], dict[str, int], dict[str, int], list[str]]:
    """Per-repo service breakdown, matched via override files.

    Pulls the repo's declared ``service_id`` set from
    ``listing.override.json`` files and intersects it with the
    process-wide SDK cache.  Replaces the old ``provider_name`` slug
    heuristic, which broke for multi-provider-per-repo and
    one-provider-many-repos relationships (e.g. ``unitysvc-labs``
    spread across http / s3 / smtp / ntfy).
    """
    global _services_by_id
    if _services_by_id is None:
        _services_by_id = _populate_services_cache()
        if _services_by_id is None:
            _services_by_id = {}  # negative cache so we don't retry
    if not _services_by_id:
        return {}, {}, {}, []

    ids = fetch_repo_service_ids(repo)
    # Override files only carry the parent service's ID.  Revisions are
    # separate rows in the SDK with their own IDs and ``revision_of``
    # pointing back at the parent, so they wouldn't be picked up by a
    # plain ID intersection.  Pull them in by following ``revision_of``
    # to any matched parent — that's how the lifecycle column gets
    # "3 active · 6 rejected revisions" instead of just "3 active".
    services = [_services_by_id[i] for i in ids if i in _services_by_id]
    services += [
        svc
        for svc in _services_by_id.values()
        if str(svc.get("revision_of") or "") in ids
    ]
    return _breakdown_for_services(services)


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

        # Skip both the seller-API match and the override-file walk
        # for archived repos — they don't have live services on the
        # gateway, and the calls would just waste round-trips.
        if r["isArchived"]:
            lifecycle, visibility, listing_type, service_types = {}, {}, {}, []
        else:
            lifecycle, visibility, listing_type, service_types = fetch_service_breakdown(
                repo_name
            )

        # Prefer SDK-derived service types (auto-populated, always
        # current) over issue labels, which require manual upkeep.
        # Fall back to labels only when the SDK has nothing — archived
        # repos, or runs without ``UNITYSVC_SELLER_API_KEY``.
        type_labels = service_types or label_values(labels, "type")

        rows.append(
            ProviderRow(
                repo=repo_name,
                is_public=r["visibility"] == "PUBLIC",
                is_archived=r["isArchived"],
                issue_number=(issue or {}).get("number"),
                issue_title=(issue or {}).get("title") or repo_name[len(REPO_PREFIX) :],
                type_labels=type_labels,
                ci_conclusion=fetch_ci_conclusion(repo_name) if not r["isArchived"] else None,
                open_pr_count=fetch_open_pr_count(repo_name) if not r["isArchived"] else 0,
                lifecycle_counts=lifecycle,
                visibility_counts=visibility,
                listing_type_counts=listing_type,
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


# Lifecycle keys that count as "in-flight" (work pending) — anything
# here flips a row to the yellow status bucket regardless of how many
# active services it also has.  Revisions in any state are by
# definition in-flight (they're staged edits awaiting a transition).
_IN_FLIGHT_LIFECYCLE = {"draft", "review", "rejected", "suspended", "pending"}


def _status_cell(row: ProviderRow) -> str:
    """Roll the per-repo signals up to a single health badge.

    Priority order (first match wins): broken > in-flight > healthy >
    unknown.  Both ``rejected`` services and open PRs flip a row to
    in-flight (yellow); the operator's stance is "someone needs to
    look at this", whether the work is already underway or not.
    """
    # Archived repos are intentionally inert; a colored badge there
    # would just be noise.  Same for repos with literally no signal —
    # the dashboard ran without an API key, or the repo has nothing
    # populated yet.
    if row.is_archived:
        return "⚪"
    has_any_signal = (
        bool(row.lifecycle_counts) or row.ci_conclusion is not None
    )
    if not has_any_signal:
        return "⚪"

    # 🔴 broken: CI explicitly failed, or no active service at all on a
    # non-archived repo with data populated.
    if row.ci_conclusion == "failure":
        return "🔴"
    if row.lifecycle_counts and row.lifecycle_counts.get("active", 0) == 0:
        return "🔴"

    # 🟡 in-flight: anything pending — open PR, rejected/draft/review
    # services, or any revision in any state.
    if row.open_pr_count > 0:
        return "🟡"
    for k in row.lifecycle_counts:
        if k in _IN_FLIGHT_LIFECYCLE or k.endswith(" revision"):
            return "🟡"

    # 🟢 healthy: CI green (or absent — repos can be healthy before
    # their first CI run), ≥1 active service, no in-flight states.
    if row.ci_conclusion in (None, "success") and row.lifecycle_counts.get("active", 0) > 0:
        return "🟢"

    # Fallback — CI in some non-failure non-success state (cancelled,
    # in_progress) and no other strong signal.
    return "⚪"


def _pr_cell(count: int, repo: str) -> str:
    if count == 0:
        return "—"
    return f"[{count}](https://github.com/{ORG}/{repo}/pulls)"


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

    def _label(key: str, count: int) -> str:
        name = (display_map or {}).get(key, key)
        # Pluralize the revision suffix so "1 rejected revision" but
        # "3 rejected revisions" — the other lifecycle/visibility names
        # are adjectives that don't need plural agreement.
        if name.endswith("revision") and count != 1:
            name += "s"
        return f"{count} {name}"

    parts = [_label(k, filtered[k]) for k in ordered_keys]
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


def _listing_type_cell(counts: dict[str, int]) -> str:
    # ``self_hosted`` is the SDK enum value; operators say "byoe"
    # (bring-your-own-endpoint) — surface the operator term.
    return _counts_cell(
        counts,
        primary_order=["regular", "byok", "self_hosted"],
        display_map={"self_hosted": "byoe"},
    )


def _sum_counts(dicts: list[dict[str, int]]) -> dict[str, int]:
    """Element-wise sum of a list of count dicts."""
    total: dict[str, int] = {}
    for d in dicts:
        for k, v in d.items():
            total[k] = total.get(k, 0) + v
    return total


def render_readme_table(rows: list[ProviderRow]) -> str:
    """Public-only summary table for the org README.

    Private + archived repos are intentionally omitted — those are
    surfaced on the per-issue sticky comments instead.
    """
    public_rows = [r for r in rows if r.is_public and not r.is_archived]

    lines = [
        "| Provider | Repo | Type | Lifecycle | Visibility | Listing type | Status | Open PRs |",
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
                    _listing_type_cell(r.listing_type_counts),
                    _status_cell(r),
                    _pr_cell(r.open_pr_count, r.repo),
                ]
            )
            + " |"
        )

    # Totals row at the bottom — sums every count-based cell across
    # the rendered rows so operators get a one-glance org-wide view
    # without eyeballing the column.  Type / Validate don't aggregate
    # cleanly (set union and per-repo signal respectively); ``—``.
    total_lifecycle = _sum_counts([r.lifecycle_counts for r in public_rows])
    total_visibility = _sum_counts([r.visibility_counts for r in public_rows])
    total_listing_type = _sum_counts([r.listing_type_counts for r in public_rows])
    total_open_prs = sum(r.open_pr_count for r in public_rows)
    lines.append(
        "| "
        + " | ".join(
            [
                f"**Total** ({len(public_rows)} repos)",
                "—",
                "—",
                _lifecycle_cell(total_lifecycle),
                _visibility_cell(total_visibility),
                _listing_type_cell(total_listing_type),
                "—",
                str(total_open_prs) if total_open_prs else "—",
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
        f"- Status: {_status_cell(row)}\n"
        f"- Repo: [`{row.repo}`](https://github.com/{ORG}/{row.repo})"
        f" — {'public' if row.is_public else 'private'}"
        f"{' · archived' if row.is_archived else ''}\n"
        f"- Type: {type_cell}\n"
        f"- Lifecycle: {_lifecycle_cell(row.lifecycle_counts)}\n"
        f"- Visibility: {visibility_cell}\n"
        f"- Listing type: {_listing_type_cell(row.listing_type_counts)}\n"
        f"- Last CI: {_ci_cell(row.ci_conclusion)}\n"
        f"- Open PRs: {_pr_cell(row.open_pr_count, row.repo)}\n"
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
