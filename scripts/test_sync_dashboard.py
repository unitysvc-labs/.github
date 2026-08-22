"""Tests for the dashboard's repo-local discovery and count aggregation.

These cover the two things that silently rotted when the services repos
moved to the template + param ``specs/`` layout and the backend renamed
``listing_type`` → ``channel_types``:

1. ``_service_ids_from_sidecars`` — where a repo's ``service_id`` values
   actually live now (the backend-written identity sidecars).
2. ``_breakdown_for_services`` — turning a backend service list into the
   lifecycle / visibility / listing-type counts the table renders.

No network, no SDK: both functions are pure over local files / dicts.

Run with::

    python -m unittest discover -s scripts -p 'test_*.py'
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import sync_dashboard as sd


@contextlib.contextmanager
def captured_stdout() -> "contextlib.AbstractContextManager[io.StringIO]":
    """Swallow the module's diagnostic prints.

    Without this the warnings the tests deliberately provoke land in the
    CI log looking like findings about a real repo — which is precisely
    the confusion these warnings exist to prevent.
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        yield buf


class ServiceIdDiscoveryTests(unittest.TestCase):
    """``service_id`` comes from the sidecars ``usvc_seller`` writes back."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write(self, rel: str, payload: object) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload) if not isinstance(payload, str) else payload)

    def test_flat_specs_layout_named_sidecars(self) -> None:
        """``specs/<name>.service.json`` — the template + param layout."""
        self._write(
            "services/specs/groq/allam-2-7b.service.json",
            {"service_id": "0309aad6-c2a6-420c-b4f0-8dac8e488164", "upstream_test_status": "pass"},
        )
        self._write(
            "services/specs/groq/openai/gpt-oss-20b.service.json",
            {"service_id": "11111111-2222-3333-4444-555555555555"},
        )
        self.assertEqual(
            sd._service_ids_from_sidecars(self.root),
            {
                "0309aad6-c2a6-420c-b4f0-8dac8e488164",
                "11111111-2222-3333-4444-555555555555",
            },
        )

    def test_folder_layout_bare_sidecar(self) -> None:
        """``<service_dir>/service.json`` — the older per-folder layout."""
        self._write(
            "services/specs/smtp-relay/service.json",
            {
                "name": "smtp-relay",
                "service_id": "eb2f4631-ae82-408d-bf6f-b3b0c3c1c09b",
                "status": "unchanged",
            },
        )
        self.assertEqual(
            sd._service_ids_from_sidecars(self.root),
            {"eb2f4631-ae82-408d-bf6f-b3b0c3c1c09b"},
        )

    def test_both_layouts_in_one_repo(self) -> None:
        """Repos mid-migration carry both shapes; the union is the id set."""
        self._write("services/specs/a/service.json", {"service_id": "aaaa"})
        self._write("services/specs/b/thing.service.json", {"service_id": "bbbb"})
        self.assertEqual(sd._service_ids_from_sidecars(self.root), {"aaaa", "bbbb"})

    def test_ignores_listing_and_param_files(self) -> None:
        """Listing / param / template files carry no id and must not confuse it."""
        self._write("services/specs/x/listing.json", {"display_name": "X", "currency": "USD"})
        self._write("services/specs/x/offering.json", {"display_name": "X"})
        self._write("services/specs/x/param.json", {"parameters": {"a": 1}})
        self._write("services/templates/listing.json.j2", "{{ not json }}")
        self._write("services/specs/x/service.json", {"service_id": "only-this-one"})
        self.assertEqual(sd._service_ids_from_sidecars(self.root), {"only-this-one"})

    def test_tolerates_malformed_and_idless_sidecars(self) -> None:
        """A broken sidecar must not take down discovery for the whole repo."""
        self._write("services/specs/bad/service.json", "{not valid json")
        self._write("services/specs/list/service.json", [1, 2, 3])
        self._write("services/specs/idless/service.json", {"status": "created"})
        self._write("services/specs/good/service.json", {"service_id": "kept"})
        with captured_stdout():
            ids = sd._service_ids_from_sidecars(self.root)
        self.assertEqual(ids, {"kept"})

    def test_empty_repo_yields_empty_set(self) -> None:
        self.assertEqual(sd._service_ids_from_sidecars(self.root), set())

    def test_malformed_sidecar_warning_names_the_path(self) -> None:
        """"service.json" alone identifies nothing — report where it lives."""
        self._write("services/specs/http-relay/service.json", "{not valid json")
        with captured_stdout() as buf:
            sd._service_ids_from_sidecars(self.root)
        self.assertIn("services/specs/http-relay/service.json", buf.getvalue())


class BreakdownTests(unittest.TestCase):
    """Counting backend service records into the table's three count cells."""

    def test_channel_types_populate_listing_type_counts(self) -> None:
        """``ServicePublic`` exposes ``channel_types`` (a list), not ``listing_type``."""
        services = [
            {"status": "active", "visibility": "public", "channel_types": ["managed"]},
            {"status": "active", "visibility": "public", "channel_types": ["managed", "byok"]},
            {"status": "draft", "visibility": "unlisted", "channel_types": ["byoe"]},
        ]
        _lifecycle, _visibility, listing_type, _types = sd._breakdown_for_services(services)
        self.assertEqual(listing_type, {"managed": 2, "byok": 1, "byoe": 1})

    def test_legacy_scalar_listing_type_still_counted(self) -> None:
        """Older backends returned a scalar ``listing_type``; keep reading it."""
        services = [{"status": "active", "visibility": "public", "listing_type": "regular"}]
        _lifecycle, _visibility, listing_type, _types = sd._breakdown_for_services(services)
        self.assertEqual(listing_type, {"regular": 1})

    def test_lifecycle_and_visibility_counts(self) -> None:
        services = [
            {"status": "active", "visibility": "public"},
            {"status": "active", "visibility": "unlisted"},
            {"status": "draft", "visibility": "private"},
        ]
        lifecycle, visibility, _lt, _types = sd._breakdown_for_services(services)
        self.assertEqual(lifecycle, {"active": 2, "draft": 1})
        self.assertEqual(visibility, {"public": 1, "unlisted": 1, "private": 1})

    def test_revisions_bucket_separately_and_skip_visibility_and_channels(self) -> None:
        """Revisions are staged edits — counted in lifecycle only."""
        services = [
            {"status": "active", "visibility": "public", "channel_types": ["managed"]},
            {
                "status": "rejected",
                "visibility": "unlisted",
                "channel_types": ["managed"],
                "revision_of": "some-parent-id",
            },
        ]
        lifecycle, visibility, listing_type, _types = sd._breakdown_for_services(services)
        self.assertEqual(lifecycle, {"active": 1, "rejected revision": 1})
        self.assertEqual(visibility, {"public": 1})
        self.assertEqual(listing_type, {"managed": 1})

    def test_service_types_collected_and_sorted(self) -> None:
        services = [
            {"status": "active", "service_type": "llm"},
            {"status": "active", "service_type": "image"},
            {"status": "active", "service_type": "llm"},
        ]
        _lc, _vis, _lt, types = sd._breakdown_for_services(services)
        self.assertEqual(types, ["image", "llm"])


class ListingTypeCellTests(unittest.TestCase):
    """The rendered cell uses the current channel-type vocabulary."""

    def test_renders_channel_types_in_operator_order(self) -> None:
        cell = sd._listing_type_cell({"byok": 1, "managed": 3, "enrollable": 2})
        self.assertEqual(cell, "3 managed · 1 byok · 2 enrollable")

    def test_legacy_values_map_to_current_names(self) -> None:
        cell = sd._listing_type_cell({"regular": 2, "self_hosted": 1})
        self.assertEqual(cell, "2 managed · 1 byoe")

    def test_empty_renders_dash(self) -> None:
        self.assertEqual(sd._listing_type_cell({}), "—")


if __name__ == "__main__":
    unittest.main()
