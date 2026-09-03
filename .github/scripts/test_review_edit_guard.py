from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("review_edit_guard.py")
SPEC = importlib.util.spec_from_file_location("review_edit_guard", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
guard = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = guard
SPEC.loader.exec_module(guard)


def catalog(*entries: str) -> str:
    return "\n\n".join(entry.strip() for entry in entries) + "\n"


def completed(stdout: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


def fake_git(trees: dict[str, dict[str, str]]):
    """Answer the diff and show calls a run makes from an in-memory revision map.

    The diff honours the pathspecs it is given, the way git does, so a file the
    caller never asks about stays invisible to the comparator.
    """

    changed = sorted(
        {path for tree in trees.values() for path in tree},
        key=lambda path: (path.count("/"), path),
    )

    def call(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        if args[0] == "diff":
            pathspecs = args[args.index("--") + 1 :]
            selected = [
                path
                for path in changed
                if any(
                    path == spec or path.startswith(f"{spec}/") for spec in pathspecs
                )
            ]
            return completed("".join(f"{path}\n" for path in selected))
        if args[0] == "show":
            revision, path = args[1].split(":", 1)
            text = trees[revision].get(path)
            if text is None:
                return subprocess.CompletedProcess(
                    args=[],
                    returncode=128,
                    stdout="",
                    stderr=f"fatal: path {path!r} does not exist in {revision!r}",
                )
            return completed(text)
        raise AssertionError(f"unexpected git call: {args}")

    return call


ENTRY_PATH = "standard_names/equilibrium.yml"

# The per-name block of the catalog manifest lives beside the domain files and
# carries every field the pipeline owns, so the reviewable entry holds only the
# name, the two prose fields, and the unit that gives them physical context.
SIDECAR_PATH = "catalog.yml"

ENTRY = """
- name: electron_density
  description: Electron density.
  documentation: Authored documentation.
  unit: m^-3
"""

SECOND_ENTRY = """
- name: electron_temperature
  description: Electron temperature.
  documentation: Authored documentation.
  unit: eV
"""

# The shape the export actually writes at the sidecar path: one mapping of
# release metadata for the whole cut, with the block naming the reviewed cohort
# inside it. Abridged from a real cut; the key order is the writer's.
SIDECAR = """
catalog_name: imas-standard-names-catalog
cocos_convention: 17
grammar_version: 0.8.5
isn_model_version: 0.8.5
dd_version_lineage:
- 4.0.0
generated_by: imas-codex sn export
generated_at: '2026-09-02T23:45:33+02:00'
min_score_applied: 0.65
min_description_score_applied: null
include_unreviewed: false
candidate_count: 410
published_count: 351
export_scope: review
domains_included:
- equilibrium
- transport
review_batch:
- electron_density
- electron_temperature
catalog_commit_sha: 7ed08e562d9d00bfd81e8de6ab51ebfedab6f6dd
edge_model_version: v1
"""

SIDECAR_ENTRY = """
- name: electron_density
  kind: scalar
  status: active
  physics_domain: equilibrium
  links: []
  arguments:
  - name: density
    operator: electron
    operator_kind: population
  sources:
  - kind: imas-dd
    ref: core_profiles/profiles_1d/electrons/density
    version: 4.1.0
"""


class ReviewEditGuardTests(unittest.TestCase):
    def compare(self, before: str, after: str, path: str = ENTRY_PATH):
        return guard.compare_catalogs(
            path,
            guard.load_catalog(before, "base"),
            guard.load_catalog(after, "head"),
        )

    def compare_sidecar(self, before: str, after: str):
        return self.compare(before, after, path=SIDECAR_PATH)

    def test_authored_fields_may_change(self):
        after = ENTRY.replace("electron_density", "free_electron_density", 1)
        after = after.replace("Electron density.", "Free-electron density.")
        after = after.replace(
            "Authored documentation.", "Expanded authored documentation."
        )
        self.assertEqual(self.compare(catalog(ENTRY), catalog(after)), [])

    def test_new_entry_is_allowed(self):
        self.assertEqual(self.compare("", catalog(ENTRY)), [])

    def test_changed_catalog_paths_selects_yaml_below_standard_names(self):
        result = completed("standard_names/equilibrium.yml\nstandard_names/README.md\n")
        with patch.object(guard, "_git", return_value=result) as git:
            self.assertEqual(
                guard.changed_catalog_paths("base", "head"),
                ["standard_names/equilibrium.yml"],
            )
        self.assertEqual(git.call_args.args[-2:], ("standard_names", SIDECAR_PATH))

    def test_changed_catalog_paths_selects_the_root_sidecar(self):
        result = completed(f"{SIDECAR_PATH}\n{ENTRY_PATH}\n")
        with patch.object(guard, "_git", return_value=result) as git:
            self.assertEqual(
                guard.changed_catalog_paths("base", "head"),
                [SIDECAR_PATH, ENTRY_PATH],
            )
        self.assertIn(SIDECAR_PATH, git.call_args.args)

    def test_unit_change_names_identity_field_and_values(self):
        violations = self.compare(
            catalog(ENTRY), catalog(ENTRY.replace("unit: m^-3", "unit: eV"))
        )
        self.assertEqual(
            [(item.identity, item.field, item.base, item.head) for item in violations],
            [("electron_density", "unit", "m^-3", "eV")],
        )
        self.assertIn(
            "Data Dictionary or generated by the pipeline", violations[0].annotation()
        )

    def test_reviewable_entry_carries_only_prose_and_unit(self):
        entry = guard.load_catalog(catalog(ENTRY), "head").entries[0]
        self.assertEqual(set(entry), {"name", "description", "documentation", "unit"})

    def test_kind_status_and_domain_are_machine_owned(self):
        after = (
            SIDECAR_ENTRY.replace("kind: scalar", "kind: vector")
            .replace("status: active", "status: draft")
            .replace("physics_domain: equilibrium", "physics_domain: transport")
        )
        self.assertEqual(
            {
                item.field
                for item in self.compare_sidecar(catalog(SIDECAR_ENTRY), catalog(after))
            },
            {"kind", "status", "physics_domain"},
        )

    def test_source_binding_and_link_fields_are_machine_owned(self):
        after = SIDECAR_ENTRY.replace("kind: imas-dd", "kind: signal")
        after = after.replace(
            "core_profiles/profiles_1d/electrons/density", "summary/local/density"
        )
        after = after.replace("version: 4.1.0", "version: 4.1.1")
        after = after.replace("links: []", "links:\n  - name:electron_temperature")
        self.assertEqual(
            {
                item.field
                for item in self.compare_sidecar(catalog(SIDECAR_ENTRY), catalog(after))
            },
            {"sources[0].kind", "sources[0].ref", "sources[0].version", "links"},
        )

    def test_generated_identity_roles_are_machine_owned(self):
        after = SIDECAR_ENTRY.replace(
            "operator_kind: population", "operator_kind: qualifier"
        )
        violations = self.compare_sidecar(catalog(SIDECAR_ENTRY), catalog(after))
        self.assertEqual(
            [item.field for item in violations], ["arguments[0].operator_kind"]
        )
        self.assertIn(
            "Data Dictionary or generated by the pipeline", violations[0].annotation()
        )

    def test_release_sidecar_loads_as_a_mapping(self):
        loaded = guard.load_catalog(SIDECAR, SIDECAR_PATH)
        self.assertEqual(loaded.entries, [])
        self.assertEqual(loaded.blank_before, ())
        assert loaded.manifest is not None
        self.assertEqual(loaded.manifest["published_count"], 351)
        self.assertEqual(
            loaded.manifest["review_batch"],
            ["electron_density", "electron_temperature"],
        )

    def test_domain_file_still_loads_as_a_list_of_entries(self):
        loaded = guard.load_catalog(catalog(ENTRY, SECOND_ENTRY), ENTRY_PATH)
        self.assertIsNone(loaded.manifest)
        self.assertEqual(
            [entry["name"] for entry in loaded.entries],
            ["electron_density", "electron_temperature"],
        )
        self.assertEqual(loaded.blank_before, (False, True))

    def test_a_scalar_document_is_still_rejected(self):
        with self.assertRaises(ValueError):
            guard.load_catalog("just a string\n", ENTRY_PATH)

    def test_release_metadata_change_is_machine_owned(self):
        after = SIDECAR.replace("published_count: 351", "published_count: 352")
        violations = self.compare_sidecar(SIDECAR, after)
        self.assertEqual(
            [(item.identity, item.field, item.base, item.head) for item in violations],
            [("<catalog>", "published_count", 351, 352)],
        )
        self.assertIn(
            "Data Dictionary or generated by the pipeline", violations[0].annotation()
        )

    def test_name_inside_the_per_name_block_is_machine_owned(self):
        after = SIDECAR.replace("- electron_temperature", "- free_electron_temperature")
        self.assertEqual(
            [
                (item.identity, item.field, item.base, item.head)
                for item in self.compare_sidecar(SIDECAR, after)
            ],
            [
                (
                    "electron_temperature",
                    "review_batch[1]",
                    "electron_temperature",
                    "free_electron_temperature",
                )
            ],
        )

    def test_name_dropped_from_the_per_name_block_is_machine_owned(self):
        after = SIDECAR.replace("- electron_temperature\n", "")
        violations = self.compare_sidecar(SIDECAR, after)
        self.assertEqual(
            [(item.identity, item.field) for item in violations],
            [("<catalog>", "review_batch")],
        )

    def test_release_key_reordering_is_structural(self):
        after = SIDECAR.replace(
            "candidate_count: 410\npublished_count: 351",
            "published_count: 351\ncandidate_count: 410",
        )
        violations = self.compare_sidecar(SIDECAR, after)
        self.assertEqual(
            [(item.identity, item.field) for item in violations],
            [("<catalog>", "<catalog>.<key-order>")],
        )

    def test_first_published_sidecar_is_additive(self):
        self.assertEqual(self.compare_sidecar("", SIDECAR), [])

    def test_removed_sidecar_is_structural(self):
        violations = self.compare_sidecar(SIDECAR, "")
        self.assertEqual(
            [(item.identity, item.field) for item in violations],
            [("<catalog>", "<catalog-present>")],
        )

    def test_entry_removal_is_structural(self):
        violations = self.compare(catalog(ENTRY), "")
        self.assertEqual([item.field for item in violations], ["<entry-present>"])

    def test_entry_reordering_is_structural(self):
        violations = self.compare(
            catalog(ENTRY, SECOND_ENTRY), catalog(SECOND_ENTRY, ENTRY)
        )
        self.assertIn("<entry-order>", {item.field for item in violations})

    def test_removed_blank_line_is_structural(self):
        before = catalog(ENTRY, SECOND_ENTRY)
        after = before.replace(
            "unit: m^-3\n\n- name: electron_temperature",
            "unit: m^-3\n- name: electron_temperature",
            1,
        )
        violations = self.compare(before, after)
        self.assertEqual([item.field for item in violations], ["<entry-separation>"])

    def test_reordered_keys_are_structural(self):
        after = ENTRY.replace(
            "  description: Electron density.\n  documentation: Authored documentation.",
            "  documentation: Authored documentation.\n  description: Electron density.",
        )
        violations = self.compare(catalog(ENTRY), catalog(after))
        self.assertEqual([item.field for item in violations], ["<entry>.<key-order>"])


class GuardRunHarness:
    """Drive the whole guard, so the path selector and the comparator are both live."""

    BASE: ClassVar[dict[str, str]]

    def guard_run(self, head: dict[str, str]):
        trees = {"base": dict(self.BASE), "head": head}
        with patch.object(guard, "_git", side_effect=fake_git(trees)):
            return guard.run("base", "head")

    def exit_status(self, head: dict[str, str]) -> int:
        trees = {"base": dict(self.BASE), "head": head}
        argv = ["review_edit_guard.py", "--base", "base", "--head", "head"]
        with (
            patch.object(guard, "_git", side_effect=fake_git(trees)),
            patch.object(sys, "argv", argv),
            redirect_stdout(io.StringIO()),
        ):
            return guard.main()


class GuardRunTests(GuardRunHarness, unittest.TestCase):
    BASE: ClassVar[dict[str, str]] = {
        ENTRY_PATH: catalog(ENTRY),
        SIDECAR_PATH: catalog(SIDECAR_ENTRY),
    }

    def test_machine_owned_sidecar_edit_is_rejected(self):
        head = dict(self.BASE)
        head[SIDECAR_PATH] = catalog(
            SIDECAR_ENTRY.replace("physics_domain: equilibrium", "physics_domain: mhd")
        )
        violations = self.guard_run(head)
        self.assertEqual(
            [(item.path, item.identity, item.field) for item in violations],
            [(SIDECAR_PATH, "electron_density", "physics_domain")],
        )
        self.assertEqual(self.exit_status(head), 1)

    def test_reviewable_prose_edit_in_a_domain_file_is_accepted(self):
        head = dict(self.BASE)
        head[ENTRY_PATH] = catalog(
            ENTRY.replace("Electron density.", "Density of free electrons.")
        )
        self.assertEqual(self.guard_run(head), [])
        self.assertEqual(self.exit_status(head), 0)


class ReleaseSidecarRunTests(GuardRunHarness, unittest.TestCase):
    """The same run, against the sidecar shape a real cut puts in the tree."""

    BASE: ClassVar[dict[str, str]] = {
        ENTRY_PATH: catalog(ENTRY),
        SIDECAR_PATH: SIDECAR,
    }

    def test_untouched_release_sidecar_passes(self):
        head = dict(self.BASE)
        self.assertEqual(self.guard_run(head), [])
        self.assertEqual(self.exit_status(head), 0)

    def test_release_metadata_edit_is_rejected(self):
        head = dict(self.BASE)
        head[SIDECAR_PATH] = SIDECAR.replace(
            "cocos_convention: 17", "cocos_convention: 11"
        )
        self.assertEqual(
            [(item.path, item.identity, item.field) for item in self.guard_run(head)],
            [(SIDECAR_PATH, "<catalog>", "cocos_convention")],
        )
        self.assertEqual(self.exit_status(head), 1)

    def test_per_name_block_edit_is_rejected(self):
        head = dict(self.BASE)
        head[SIDECAR_PATH] = SIDECAR.replace(
            "- electron_density\n", "- free_electron_density\n"
        )
        self.assertEqual(
            [(item.path, item.identity, item.field) for item in self.guard_run(head)],
            [(SIDECAR_PATH, "electron_density", "review_batch[0]")],
        )
        self.assertEqual(self.exit_status(head), 1)

    def test_reviewable_prose_edit_beside_the_release_sidecar_is_accepted(self):
        head = dict(self.BASE)
        head[ENTRY_PATH] = catalog(
            ENTRY.replace("Electron density.", "Density of free electrons.")
        )
        self.assertEqual(self.guard_run(head), [])
        self.assertEqual(self.exit_status(head), 0)


if __name__ == "__main__":
    unittest.main()
