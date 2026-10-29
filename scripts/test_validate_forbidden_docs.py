#!/usr/bin/env python3
"""Unit tests for forbidden ops file detection under docs/."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_legal_site import find_forbidden_docs_paths, validate_cname  # noqa: E402


class FindForbiddenDocsPathsTests(unittest.TestCase):
    def test_clean_nested_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "privacy").mkdir(parents=True)
            (root / "privacy" / "index.html").write_text("<html></html>", encoding="utf-8")
            (root / "assets" / "notes").mkdir(parents=True)
            (root / "assets" / "notes" / "readme.txt").write_text("ok", encoding="utf-8")
            self.assertEqual(find_forbidden_docs_paths(root), [])

    def test_nested_forbidden_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "sub" / "dir"
            nested.mkdir(parents=True)
            (nested / "CNAME.pending").write_text("cardscanr.com\n", encoding="utf-8")
            self.assertEqual(find_forbidden_docs_paths(root), ["sub/dir/CNAME.pending"])

    def test_case_insensitive_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "archive").mkdir()
            (root / "archive" / "dns_rollback_record.md").write_text("secret\n", encoding="utf-8")
            self.assertEqual(
                find_forbidden_docs_paths(root), ["archive/dns_rollback_record.md"]
            )


class ValidateCnameTests(unittest.TestCase):
    def test_validate_cname_reports_nested_relative_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ops" / "nested").mkdir(parents=True)
            (root / "ops" / "nested" / "CNAME").write_text("cardscanr.com\n", encoding="utf-8")

            failures: list[str] = []
            notes: list[str] = []
            import validate_legal_site as mod

            original_docs = mod.DOCS
            try:
                mod.DOCS = root
                validate_cname(failures, notes)
            finally:
                mod.DOCS = original_docs

            self.assertEqual(
                failures,
                [
                    "docs/ops/nested/CNAME must not be published; "
                    "keep domain/DNS records in private ops"
                ],
            )
            self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
