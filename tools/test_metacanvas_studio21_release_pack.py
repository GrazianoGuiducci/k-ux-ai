"""Release pack integrity/identity checks for Studio21 IT/EN candidates."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_metacanvas_studio21_release_pack import (
    build_pack, EXAMPLES, MANIFEST, NAMES, VERSION
)
from build_studio21_keyboard_section_move import SOURCE_BLOBS


class Studio21ReleasePackTests(unittest.TestCase):
    def test_two_deterministic_builds_have_complete_safe_contents(self):
        original = {name: (EXAMPLES / name).read_bytes() for name in NAMES}
        with tempfile.TemporaryDirectory(prefix="studio21-release-test-") as tmp:
            folder = Path(tmp)
            one = folder / "first.zip"
            two = folder / "second.zip"
            build_pack(one)
            build_pack(two)
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                expected = set(NAMES) | {
                    "LEGGIMI_RILASCIO.txt", "LICENZA_MPL-2.0.txt",
                    "NOTICE_ORIGINALE.md", MANIFEST,
                }
                self.assertEqual(set(archive.namelist()), expected)
                manifest = json.loads(archive.read(MANIFEST))
                self.assertEqual(manifest["schema"], "metacanvas.studio21.release-candidate.v1")
                self.assertEqual(manifest["version"], VERSION)
                self.assertEqual(manifest["status"], "not-published")
                self.assertEqual(manifest["source_pins_git_blob"], SOURCE_BLOBS)
                self.assertEqual(set(manifest["files_sha256"]), expected - {MANIFEST})
                for name, expected_sha in manifest["files_sha256"].items():
                    self.assertEqual(
                        hashlib.sha256(archive.read(name)).hexdigest(),
                        expected_sha, name,
                    )
                self.assertIn(b"Mozilla Public License Version 2.0",
                              archive.read("LICENZA_MPL-2.0.txt"))
                self.assertIn(b"Graziano Guiducci",
                              archive.read("NOTICE_ORIGINALE.md"))
                for name in NAMES:
                    candidate = archive.read(name)
                    self.assertNotEqual(candidate, original[name])
                    # Four separate privacy projection routes must be patched.
                    self.assertEqual(candidate.count(b"l.private!==true"), 4)
                    self.assertNotIn(b"file:///tmp", candidate)
            for name in NAMES:
                self.assertEqual((EXAMPLES / name).read_bytes(), original[name],
                                 "Candidate packaging modified original source")

    def test_source_drift_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="studio21-drift-test-") as tmp:
            folder = Path(tmp)
            src = folder / "sources"
            src.mkdir()
            for name in NAMES:
                (src / name).write_bytes((EXAMPLES / name).read_bytes())
            (src / "LICENSE").write_bytes((EXAMPLES / "LICENSE").read_bytes())
            (src / "NOTICE.md").write_bytes((EXAMPLES / "NOTICE.md").read_bytes())
            (src / NAMES[0]).write_bytes((src / NAMES[0]).read_bytes() + b" ")
            output = folder / "drift.zip"
            with self.assertRaisesRegex(ValueError, "source drift"):
                build_pack(output, src)
            self.assertFalse(output.exists())

    def test_refuses_to_overwrite_candidate(self):
        with tempfile.TemporaryDirectory(prefix="studio21-existing-") as tmp:
            folder = Path(tmp)
            target = folder / "existing.zip"
            target.write_bytes(b"existing-owner-content")
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                build_pack(target)
            self.assertEqual(target.read_bytes(), b"existing-owner-content")


if __name__ == "__main__":
    unittest.main()
