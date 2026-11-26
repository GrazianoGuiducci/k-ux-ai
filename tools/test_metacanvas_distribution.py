"""Deterministic positive and negative checks for the release preflight."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
from verify_metacanvas_distribution import inspect_html, verify


HTML = ("<!doctype html><html><head><!-- SPDX-License-Identifier: MPL-2.0 -->"
        "</head><body><script id=\"ccm-data\" type=\"application/json\">"
        '{"schema":"ccm.document.v1","scenes":[{"id":"s1","elements":'
        '[{"id":"a"},{"id":"b"}],"links":[{"from":"a","to":"b"}]}]}'
        "</script><script>const ok = true;</script></body></html>")


class ReleasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.source = root / "product/file.html"
        self.target = root / "site/file.bin"
        self.source.parent.mkdir()
        self.target.parent.mkdir()
        self.source.write_text(HTML, encoding="utf-8")
        data = self.source.read_bytes()
        self.target.write_bytes(data)
        self.manifest = {"artifacts": [{
            "name": "sample", "source": "file.html", "site_asset": "file.bin",
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            "scenes": 1,
        }]}
        self.product = self.source.parent
        self.site = self.target.parent

    def tearDown(self):
        self.temp.cleanup()

    def test_matching_artifacts_pass(self):
        self.assertEqual(verify(self.manifest, self.product, self.site, None), [])

    def test_changed_download_detected(self):
        self.target.write_bytes(self.target.read_bytes() + b"\n")
        self.assertTrue(any("site download does not match" in e for e in
                            verify(self.manifest, self.product, self.site, None)))

    def test_changed_source_detected(self):
        self.source.write_text(HTML.replace("const ok = true", "const ok = false"), encoding="utf-8")
        errors = verify(self.manifest, self.product, None, None)
        self.assertTrue(any("source SHA-256 drift" in e for e in errors))

    def test_dangling_link_detected(self):
        corrupt = HTML.replace('"to":"b"', '"to":"not-found"')
        self.assertTrue(any("dangling link" in e for e in inspect_html(corrupt.encode(), "sample", 1, None)))

    def test_missing_license_detected(self):
        corrupt = HTML.replace("SPDX-License-Identifier: MPL-2.0", "notice removed")
        self.assertTrue(any("MPL-2.0 notice absent" in e for e in inspect_html(corrupt.encode(), "sample", 1, None)))


if __name__ == "__main__":
    unittest.main()
