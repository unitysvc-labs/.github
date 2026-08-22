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
2. **Backend** (via the ``unitysvc_sellers`` SDK, *per-environment*) —
   queried once per environment (production + staging) using two
   independent ``(API_URL, API_KEY)`` pairs.  Each environment yields
   its own table on the README and its own sub-block on the per-issue
   sticky comment.  For each repo we read the ``service_id`` set from
   the identity sidecars ``usvc_seller`` commits back after upload
   (``specs/<name>.service.json`` in the template + param layout, or
   ``<service_dir>/service.json`` in the per-folder layout) and look
   those IDs up on each backend — same IDs are expected to exist in
   staging and production (lab repos share IDs across environments)
   but cells degrade to "—" when a backend is unreachable or the API
   key for that environment is unset.  Per-env env vars:
     - production: ``UNITYSVC_SELLER_PRODUCTION_API_KEY`` (required),
       ``UNITYSVC_SELLER_PRODUCTION_API_URL`` (optional — defaults to
       ``https://seller.unitysvc.com/v1``).
     - staging: ``UNITYSVC_SELLER_STAGING_API_KEY``,
       ``UNITYSVC_SELLER_STAGING_API_URL``.
3. **(future)** repo-emitted ``status.json`` artifact for ``data
   validate`` results — *not yet wired*; placeholder column rendered as
   "—" until the per-repo CI step lands.

Surfaces
--------
1. ``profile/README.md`` — replaces content between the
   ``<!-- providers-start -->`` / ``<!-- providers-end -->`` markers
   with two Markdown tables (Production then Staging) under ``###``
   sub-headings.  Public repos only.
2. ``unitysvc-labs/unitysvc-labs/issues/{N}`` — sticky comment per
   tracking issue (matched by a ``<!-- provider-status-sync -->`` HTML
   marker so reruns edit instead of accumulating).  Each comment
   carries both env snapshots, side-by-side.  All repos
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
    # Service-level signals from the seller API.  Populated when this
    # environment's ``UNITYSVC_SELLER_<ENV>_API_KEY`` is set *and* the repo
    # yielded service ids; empty dicts otherwise (cells render as ``—``).
    # Counts are by enum value.  Unknown / extra keys
    # pass through so future enum values automatically appear in the table.
    lifecycle_counts: dict[str, int]  # by ServiceStatusEnum value
    visibility_counts: dict[str, int]  # by ServiceVisibilityEnum value
    # By channel type (managed / byok / byoe / enrollable).  A service
    # offering several channels contributes to several buckets, so these
    # counts can sum past the service count — see _breakdown_for_services.
    listing_type_counts: dict[str, int]


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


# Process-wide flag: ``None`` until the first call, then either the imported
# ``AsyncClient`` class or ``False`` if the SDK is unusable.  Caches the
# import check (env-key checks are per-call now, so the import is the only
# thing worth caching here).
_seller_client_cls: Any = None


def _seller_client_class() -> Any:
    """Resolve the seller ``AsyncClient`` class once, cache the result.

    Returns ``False`` (not ``None``) when the SDK isn't installed so repeat
    calls short-circuit without re-emitting the warning.  Per-environment
    API-key gating is the caller's responsibility — this function only
    answers "is the SDK importable?".
    """
    global _seller_client_cls
    if _seller_client_cls is not None:
        return _seller_client_cls

    try:
        from unitysvc_sellers import AsyncClient
    except ImportError as exc:
        print(f"  ⚠ unitysvc_sellers SDK not installed ({exc}); skipping seller data")
        _seller_client_cls = False
        return False

    _seller_client_cls = AsyncClient
    return AsyncClient


def _service_ids_from_sidecars(root: Path) -> set[str]:
    """Backend-assigned ``service_id`` values recorded under ``root``.

    ``usvc_seller`` writes the id the backend assigned at upload time
    into an *identity sidecar* next to the spec files, and commits it
    back.  Two shapes exist depending on the repo's layout:

    - flat ``specs/`` layout (template + param files):
      ``specs/<name>.service.json``
    - per-folder layout: ``<service_dir>/service.json``

    Repos mid-migration carry both, so we take the union.

    Listing files are deliberately *not* consulted.  They used to be
    the source (via a ``schema: listing_v1`` walk) but no longer are:
    template-driven repos render ``listing.json`` from
    ``templates/listing.json.j2`` at command time and commit nothing,
    and the listings that *are* committed carry neither a ``schema``
    field nor a ``service_id``.  The sidecar is now the only committed
    record of the backend id.

    Malformed or id-less sidecars are skipped individually so one bad
    file can't blank out a whole repo.
    """
    ids: set[str] = set()
    # ``rglob("*.service.json")`` does not match a bare ``service.json``
    # (the glob requires at least the dot), so both patterns are needed.
    for path in (*root.rglob("service.json"), *root.rglob("*.service.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            # Name the file relative to the clone root: the bare filename
            # is almost always "service.json", which identifies nothing.
            try:
                where = path.relative_to(root)
            except ValueError:  # pragma: no cover — path is always under root
                where = path
            print(f"  ⚠ unreadable sidecar {where}: {exc}")
            continue
        if not isinstance(data, dict):
            continue
        sid = data.get("service_id")
        if sid:
            ids.add(str(sid))
    return ids


def fetch_repo_service_ids(repo: str) -> set[str]:
    """Service-IDs declared by this repo, read from its identity sidecars.

    Shallow-clones the repo into a temp dir and collects every
    ``service_id`` recorded by ``usvc_seller`` — see
    :func:`_service_ids_from_sidecars` for why the sidecars (and not
    the listing files) are the source of truth.

    Returns ``set()`` on any failure so the dashboard still renders —
    the cells just go to ``—`` for that repo.
    """
    import shutil
    import tempfile

    tmp_root = Path(tempfile.mkdtemp(prefix="labs-dashboard-"))
    clone_dir = tmp_root / repo
    try:
        # ``gh repo clone`` reuses gh's auth, so private labs repos work
        # without extra credential plumbing.  ``-- --depth 1`` is passed
        # through to git: we only need the latest tree, no history.
        result = subprocess.run(
            [
                "gh", "repo", "clone", f"{ORG}/{repo}", str(clone_dir),
                "--", "--depth", "1",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"  ⚠ {repo}: clone failed: {result.stderr.strip()}")
            return set()

        ids = _service_ids_from_sidecars(clone_dir)
        if not ids:
            # Loud on purpose: an empty id set silently blanks this
            # repo's Lifecycle / Visibility / Listing-type cells, which
            # is exactly how the previous (stale) discovery rotted
            # unnoticed across months of green runs.
            print(
                f"  ⚠ {repo}: no service_id found in any "
                f"service.json / *.service.json sidecar — count cells will render as —"
            )
        return ids
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


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
        #
        # The backend renamed the scalar ``listing_type`` to the list
        # ``channel_types`` when it widened the concept: a service is
        # reachable through one or more channels, each with its own
        # type (``managed`` / ``byok`` / ``byoe`` / ``enrollable``).  A
        # service offering both a managed and a BYOK channel therefore
        # counts once in each bucket — the cell describes channels on
        # offer, not a partition of services.  The retired scalar is
        # still read so an older backend keeps rendering.
        if not svc.get("revision_of"):
            channel_types = svc.get("channel_types") or []
            if isinstance(channel_types, str):  # defensive: scalar from an older shape
                channel_types = [channel_types]
            legacy = svc.get("listing_type")
            if legacy and not channel_types:
                channel_types = [legacy]
            for ct in channel_types:
                if ct:
                    listing_type[ct] = listing_type.get(ct, 0) + 1
        st = svc.get("service_type")
        if st:
            types.add(st)

    return lifecycle, visibility, listing_type, sorted(types)


def fetch_service_breakdown(
    repo: str,
    ids: set[str],
    api_url: str | None,
    api_key: str | None,
) -> tuple[dict[str, int], dict[str, int], dict[str, int], list[str]]:
    """Per-repo service breakdown for one environment.

    ``ids`` is the precomputed override-file id set for the repo (env-
    independent — computed once in the metadata phase and reused for
    every environment).  ``api_url`` / ``api_key`` target one backend.

    The backend returns the requested services *and* any pending
    revisions of them in one call (``ids=`` auto-expands to also match
    ``revision_of=``), see backend PR unitysvc/unitysvc#915.

    Returns empty tuples when ``api_key`` is unset, ``ids`` is empty,
    or any SDK call fails — so the dashboard still renders, with cells
    going to ``—`` for the affected (repo, env) cell.
    """
    if not api_key or not ids:
        return {}, {}, {}, []

    client_cls = _seller_client_class()
    if not client_cls:
        return {}, {}, {}, []

    services = _fetch_services_by_ids(client_cls, ids, api_url, api_key)
    return _breakdown_for_services(services)


def _fetch_services_by_ids(
    client_cls: Any,
    ids: set[str],
    api_url: str | None,
    api_key: str,
) -> list[dict[str, Any]]:
    """Resolve a set of service ids through the seller list endpoint.

    The backend returns the requested services *and* any pending
    revisions of them in one call (``ids=`` auto-expands to also
    match ``revision_of=``).  Cursor-paged in case the id set + its
    revisions exceed the 200-row server cap.

    ``api_url`` empty / ``None`` passes through to the SDK so its
    default (``https://seller.unitysvc.com/v1``) applies — keeps the
    production workflow valid even when no ``…_PRODUCTION_API_URL``
    secret is set.  Returns ``[]`` on any failure so the dashboard
    still renders — the cells just go to ``—`` for that repo.
    """
    from uuid import UUID

    uuid_ids = [UUID(sid) for sid in ids]
    page_limit = min(max(len(uuid_ids) * 2, 50), 200)
    # Empty string from an undefined GitHub secret would otherwise short-
    # circuit the SDK's "fall back to default" logic — normalize to None.
    effective_url = api_url or None

    async def _fetch() -> list[dict[str, Any]]:
        collected: list[dict[str, Any]] = []
        cursor: str | None = None
        async with client_cls(api_key=api_key, base_url=effective_url) as client:
            while True:
                page = await client.services.list(
                    ids=uuid_ids, limit=page_limit, cursor=cursor
                )
                for svc in page.data:
                    svc_dict = svc.to_dict() if hasattr(svc, "to_dict") else dict(svc)
                    collected.append(svc_dict)
                if not getattr(page, "has_more", False):
                    break
                next_cursor = getattr(page, "next_cursor", None)
                if not next_cursor or not isinstance(next_cursor, str):
                    break
                cursor = next_cursor
        return collected

    try:
        return asyncio.run(_fetch())
    except Exception as exc:  # noqa: BLE001 — surface the cause and degrade gracefully
        print(f"  ⚠ Seller SDK call failed ({type(exc).__name__}: {exc}); skipping")
        return []


@dataclass
class RepoBaseMeta:
    """Env-independent per-repo data — computed once and reused for
    every environment we render.  Kept separate from ``ProviderRow``
    so the (per-env) breakdown doesn't trigger N×env-count GitHub /
    git-clone calls.
    """

    repo: str
    is_public: bool
    is_archived: bool
    issue_number: int | None
    issue_title: str
    issue_type_labels: list[str]
    ci_conclusion: str | None
    open_pr_count: int
    service_ids: set[str]


def collect_repo_metadata() -> list[RepoBaseMeta]:
    """One pass over every env-independent source.

    Includes the github metadata (repos, issues, CI, PR counts) AND the
    per-repo ``service_id`` set from the override files — that set
    lives in the repo and is identical across environments, so we read
    it once even though it'll be looked up against multiple backends.
    """
    repos = list_services_repos()
    issues = list_tracking_issues()
    repo_to_issue = build_repo_to_issue_map(issues)

    metas: list[RepoBaseMeta] = []
    for r in repos:
        repo_name = r["name"]
        issue = repo_to_issue.get(repo_name)
        labels = (issue or {}).get("labels", [])

        # Skip live-data fetches for archived repos — no services on
        # any backend, no recent CI, no open PRs we care about.
        if r["isArchived"]:
            ci_conclusion = None
            open_pr_count = 0
            service_ids: set[str] = set()
        else:
            ci_conclusion = fetch_ci_conclusion(repo_name)
            open_pr_count = fetch_open_pr_count(repo_name)
            service_ids = fetch_repo_service_ids(repo_name)

        metas.append(
            RepoBaseMeta(
                repo=repo_name,
                is_public=r["visibility"] == "PUBLIC",
                is_archived=r["isArchived"],
                issue_number=(issue or {}).get("number"),
                issue_title=(issue or {}).get("title") or repo_name[len(REPO_PREFIX) :],
                issue_type_labels=label_values(labels, "type"),
                ci_conclusion=ci_conclusion,
                open_pr_count=open_pr_count,
                service_ids=service_ids,
            )
        )

    return metas


def build_rows_for_env(
    metas: list[RepoBaseMeta],
    env_name: str,
    api_url: str | None,
    api_key: str | None,
) -> list[ProviderRow]:
    """One ``ProviderRow`` per repo, with breakdowns fetched from the
    given backend.  When ``api_key`` is empty, every row's count dicts
    come back empty (cells render as ``—``) without any network I/O.
    """
    rows: list[ProviderRow] = []
    for meta in metas:
        if meta.is_archived:
            lifecycle, visibility, listing_type, service_types = {}, {}, {}, []
        else:
            lifecycle, visibility, listing_type, service_types = fetch_service_breakdown(
                meta.repo, meta.service_ids, api_url, api_key
            )

        # Prefer SDK-derived service types (auto-populated, always
        # current) over issue labels.  Fall back to issue labels when
        # the SDK returned nothing — archived repos, missing key for
        # this env, or services that haven't been uploaded to this
        # backend yet.
        type_labels = service_types or meta.issue_type_labels

        rows.append(
            ProviderRow(
                repo=meta.repo,
                is_public=meta.is_public,
                is_archived=meta.is_archived,
                issue_number=meta.issue_number,
                issue_title=meta.issue_title,
                type_labels=type_labels,
                ci_conclusion=meta.ci_conclusion,
                open_pr_count=meta.open_pr_count,
                lifecycle_counts=lifecycle,
                visibility_counts=visibility,
                listing_type_counts=listing_type,
            )
        )

    # Stable sort by display name so README diffs are minimal.  Sort
    # here (not in metadata collection) so the result order matches
    # the rendering order each renderer expects.
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
    # Current channel-type vocabulary, in operator priority order:
    # ``managed`` (seller's key — the monetized default), ``byok``,
    # ``byoe``, ``enrollable``.  The two retired names are mapped onto
    # their replacements so a mixed-vintage backend renders one
    # consistent vocabulary instead of both.
    return _counts_cell(
        counts,
        primary_order=["managed", "byok", "byoe", "enrollable"],
        display_map={"regular": "managed", "self_hosted": "byoe"},
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
        "| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |",
        "|---|---|---|---|---|---|---|---|---|",
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
                    _status_cell(r),
                    provider_link,
                    repo_link,
                    type_cell,
                    _lifecycle_cell(r.lifecycle_counts),
                    _visibility_cell(r.visibility_counts),
                    _listing_type_cell(r.listing_type_counts),
                    _ci_cell(r.ci_conclusion),
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
                "—",
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


def render_readme_block(
    env_tables: list[tuple[str, str]],
) -> str:
    """Combine per-env tables into one block for the README markers.

    Each entry in ``env_tables`` is ``(heading, rendered_table_md)``.
    Emits ``### <heading>`` above each table; tables are separated by
    a blank line so the Markdown renders cleanly.
    """
    parts: list[str] = []
    for i, (heading, table) in enumerate(env_tables):
        if i:
            parts.append("")  # blank line between sections
        parts.append(f"### {heading}")
        parts.append("")
        parts.append(table)
    return "\n".join(parts)


def _env_subblock(label: str, row: ProviderRow | None) -> str:
    """One ``**Env**`` sub-block inside a sticky comment.

    ``row`` may be ``None`` when an entire env's data is missing
    (e.g. its API key isn't configured) — in which case we still
    emit the header so the operator can see "production was meant
    to be here" rather than silently omitting it.
    """
    if row is None:
        return f"**{label}**\n- _(no data — API key not configured)_\n"

    visibility_cell = _counts_cell(
        row.visibility_counts,
        primary_order=["public", "unlisted", "private"],
        display_map=_VISIBILITY_DISPLAY,
    )
    return (
        f"**{label}**\n"
        f"- Status: {_status_cell(row)}\n"
        f"- Lifecycle: {_lifecycle_cell(row.lifecycle_counts)}\n"
        f"- Visibility: {visibility_cell}\n"
        f"- Listing type: {_listing_type_cell(row.listing_type_counts)}\n"
    )


def render_issue_comment_dual(
    env_rows: list[tuple[str, ProviderRow | None]],
    timestamp: str,
) -> str:
    """Sticky-comment body covering every environment for one repo.

    ``env_rows`` is ``[(label, row), …]`` in render order (e.g.
    ``[("Production", prod_row), ("Staging", staging_row)]``).  The
    repo-level header section (repo link, type, CI, PRs) is rendered
    once from the first non-``None`` row — those fields are
    env-independent — and then each env contributes its own snapshot
    block below.
    """
    # Find the first available row for the env-independent header.
    header_row = next((r for _, r in env_rows if r is not None), None)
    if header_row is None:
        # Should never happen — we always pass at least one row — but
        # be defensive so a misconfigured run still produces a marker
        # comment instead of crashing.
        return (
            f"{COMMENT_MARKER}\n"
            f"**Provider status snapshot** _(auto-synced {timestamp} UTC)_\n\n"
            f"_(no environment data available)_\n"
        )

    type_cell = ", ".join(header_row.type_labels) if header_row.type_labels else "—"
    head = (
        f"{COMMENT_MARKER}\n"
        f"**Provider status snapshot** _(auto-synced {timestamp} UTC)_\n\n"
        f"- Repo: [`{header_row.repo}`](https://github.com/{ORG}/{header_row.repo})"
        f" — {'public' if header_row.is_public else 'private'}"
        f"{' · archived' if header_row.is_archived else ''}\n"
        f"- Type: {type_cell}\n"
        f"- Last CI: {_ci_cell(header_row.ci_conclusion)}\n"
        f"- Open PRs: {_pr_cell(header_row.open_pr_count, header_row.repo)}\n\n"
    )

    subblocks = "\n".join(_env_subblock(label, row) for label, row in env_rows)
    return head + subblocks


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


# Environments rendered, in display order (production first — operators
# look at the canonical catalog first, then the staging preview).  Each
# entry is ``(heading, url_env_var, key_env_var)``; the script reads
# those env vars at run time, so leaving either pair unset is a
# supported degraded mode (cells render as "—").
ENVIRONMENTS: list[tuple[str, str, str]] = [
    ("Production", "UNITYSVC_SELLER_PRODUCTION_API_URL", "UNITYSVC_SELLER_PRODUCTION_API_KEY"),
    ("Staging", "UNITYSVC_SELLER_STAGING_API_URL", "UNITYSVC_SELLER_STAGING_API_KEY"),
]


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

    # Phase 1: env-independent metadata (repos, issues, CI, PRs,
    # sidecar-recorded service ids).  One pass.
    metas = collect_repo_metadata()

    # Canary.  Every count column on the dashboard is downstream of the
    # per-repo service-id set, and an empty set renders as "—" rather
    # than as an error — which is how a stale discovery rule survived
    # months of green runs.  If *no* live repo yields a single id, the
    # discovery rule is broken (not the data), so fail the run loudly
    # instead of quietly publishing a table of dashes.
    live = [m for m in metas if not m.is_archived]
    discovery_broken = bool(live) and not any(m.service_ids for m in live)
    if discovery_broken:
        print(
            f"\n  ✗ None of the {len(live)} live repos yielded a service id. "
            "Service ids are read from the committed identity sidecars "
            "(service.json / *.service.json); if the repos moved to a new "
            "layout, _service_ids_from_sidecars needs updating.\n"
        )
    else:
        total_ids = sum(len(m.service_ids) for m in live)
        print(f"  ✓ Discovered {total_ids} service ids across {len(live)} live repos")

    # Phase 2: per-env breakdown rows.  One pass per environment;
    # missing API key for an env yields empty count dicts (no I/O).
    env_rows: list[tuple[str, list[ProviderRow]]] = []
    for heading, url_var, key_var in ENVIRONMENTS:
        api_url = os.environ.get(url_var) or None
        api_key = os.environ.get(key_var) or None
        if not api_key:
            print(f"  ⚠ {heading}: {key_var} unset; cells will render as —")
        env_rows.append(
            (heading, build_rows_for_env(metas, heading, api_url, api_key))
        )

    # Render the README block — two tables under ``###`` sub-headings,
    # one per environment.
    block = render_readme_block(
        [(heading, render_readme_table(rows)) for heading, rows in env_rows]
    )

    # Timestamp is generated once per run so README and all sticky
    # comments share the same value.
    from datetime import datetime, timezone

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    if args.dry_run:
        print("=== README block ===")
        print(block)
        print()
        # Index rows by repo for sticky-comment rendering — env_rows is
        # already per-env, so we need to pivot to per-repo.
        by_repo: dict[str, list[tuple[str, ProviderRow | None]]] = {}
        for heading, rows in env_rows:
            for r in rows:
                by_repo.setdefault(r.repo, []).append((heading, r))
        # Use the first env's row ordering as the iteration order so
        # dry-run output is stable across runs.
        order = [r.repo for r in env_rows[0][1]]
        for repo_name in order:
            entries = by_repo.get(repo_name, [])
            issue_number = next(
                (r.issue_number for _, r in entries if r and r.issue_number is not None),
                None,
            )
            if issue_number is None:
                continue
            print(f"=== Comment on issue #{issue_number} ({repo_name}) ===")
            print(render_issue_comment_dual(entries, timestamp))
            print()
        return 1 if discovery_broken else 0

    # README write
    readme = README_PATH.read_text()
    new_readme = replace_section(readme, block)
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
        return 1 if discovery_broken else 0

    # Pivot env_rows (per-env lists) to per-repo (one entry per env).
    by_repo: dict[str, list[tuple[str, ProviderRow | None]]] = {}
    for heading, rows in env_rows:
        for r in rows:
            by_repo.setdefault(r.repo, []).append((heading, r))

    # Iterate in the first env's sorted order for deterministic output.
    for r in env_rows[0][1]:
        entries = by_repo.get(r.repo, [])
        issue_number = next(
            (er.issue_number for _, er in entries if er and er.issue_number is not None),
            None,
        )
        if issue_number is None:
            print(f"  ⊘ {r.repo}: no tracking issue mapped")
            continue
        try:
            update_sticky_comment(issue_number, render_issue_comment_dual(entries, timestamp))
            print(f"  ✓ {r.repo} → #{issue_number}")
        except RuntimeError as err:
            print(f"  ✗ {r.repo} → #{issue_number}: {err}")

    return 1 if discovery_broken else 0


if __name__ == "__main__":
    sys.exit(main())
