"""Tests for the bounded and source-preserving MetaEditor main region patcher."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from metaeditor_region_patch import locate_main, replace_main, UnsupportedDocument


SOURCE = '''<!doctype html>\r\n<html><head>\n<script>const x = "<main>not real</main>";</script>\n<style>.x:before{content:"<main>"}</style>\n</head><body><!-- <main> in a comment -->\n<header>Original header</header>\n<main id="document" class="page">\n  <article><p id="old">Original</p></article>\n</main >\n<footer>Original footer</footer></body></html>\n'''


class MainPatchTests(unittest.TestCase):
    def test_noop_preserves_every_byte(self):
        inner = locate_main(SOURCE).content(SOURCE)
        self.assertEqual(replace_main(SOURCE, inner).encode(), SOURCE.encode())

    def test_changed_main_preserves_head_nav_footer(self):
        before = '<article><p>Changed</p></article>'
        patched = replace_main(SOURCE, before)
        a, b = locate_main(SOURCE), locate_main(patched)
        self.assertEqual(patched[:b.content_start], SOURCE[:a.content_start])
        self.assertEqual(patched[b.content_end:], SOURCE[a.content_end:])
        self.assertEqual(b.content(patched), before)
        self.assertIn('<script>const x = "<main>not real</main>";', patched)
        self.assertIn('Original footer', patched)

    def test_fail_closed_for_missing_duplicate_unbalanced(self):
        for source in ('<html><body>no main</body></html>',
                       '<main>one</main><main>two</main>',
                       '<main>never closed', '</main>'):
            with self.subTest(source=source), self.assertRaises(UnsupportedDocument):
                locate_main(source)

    def test_reject_nested_main_and_runtime_marker_leak(self):
        for content in ('<main>oops</main>', '<p data-local-block="paragraph">leak</p>',
                        '<aside id="local-editor">leak</aside>'):
            with self.subTest(content=content), self.assertRaises(UnsupportedDocument):
                replace_main(SOURCE, content)

    def test_does_not_execute_or_strip_external_source(self):
        payload = '<section><h2>New</h2></section>'
        result = replace_main(SOURCE, payload)
        self.assertEqual(result.count('<script>'), 1)
        self.assertEqual(result.count('<style>'), 1)
        self.assertEqual(result.count('<main '), 1)


if __name__ == '__main__':
    unittest.main()
