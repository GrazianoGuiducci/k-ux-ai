"""Source-preserving <main> region replacement for trusted static-page adapters.

No script execution, document import, sanitization or DOM reconstruction happens
here. The caller must provide an already reviewed, sanitized main fragment.
This is a candidate building block, not an all-HTML parser or released editor.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import re


class UnsupportedDocument(ValueError):
    """Input cannot be patched without ambiguous ownership of <main>."""


@dataclass(frozen=True)
class MainRegion:
    opening_start: int
    content_start: int
    content_end: int
    closing_end: int

    def content(self, source: str) -> str:
        return source[self.content_start:self.content_end]


class _MainLocator(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.starts = [0]
        for match in re.finditer(r'\n', source):
            self.starts.append(match.end())
        self.open_start = None
        self.content_start = None
        self.region = None

    def absolute_position(self) -> int:
        line, column = self.getpos()
        if not 1 <= line <= len(self.starts):
            raise UnsupportedDocument('invalid parser position')
        return self.starts[line - 1] + column

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != 'main':
            return
        if self.open_start is not None or self.region is not None:
            raise UnsupportedDocument('multiple or nested main elements')
        start = self.absolute_position()
        raw = self.get_starttag_text()
        self.open_start = start
        self.content_start = start + len(raw)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'main':
            raise UnsupportedDocument('self-closing main is unsupported')

    def handle_endtag(self, tag: str) -> None:
        if tag != 'main':
            return
        if self.open_start is None or self.content_start is None:
            raise UnsupportedDocument('unmatched closing main')
        close = self.absolute_position()
        match = re.match(r'</\s*main\s*>', self.source[close:], flags=re.I)
        if not match:
            raise UnsupportedDocument('unrecognized closing main tag')
        self.region = MainRegion(self.open_start, self.content_start, close, close + len(match.group()))
        self.open_start = None


def locate_main(source: str) -> MainRegion:
    if not isinstance(source, str) or not source.strip():
        raise UnsupportedDocument('source must be non-empty Unicode HTML')
    parser = _MainLocator(source)
    try:
        parser.feed(source)
        parser.close()
    except (AssertionError, IndexError) as exc:
        raise UnsupportedDocument('HTML parser could not identify main safely') from exc
    if parser.open_start is not None or parser.region is None:
        raise UnsupportedDocument('exactly one complete main is required')
    return parser.region


def replace_main(source: str, edited_inner_html: str) -> str:
    """Replace only <main> content, preserving every codepoint outside it.

    Edited content must already be trusted and sanitized by the calling editor.
    A no-op returns the original string without serialization changes.
    """
    region = locate_main(source)
    if not isinstance(edited_inner_html, str):
        raise TypeError('edited main content must be a Unicode string')
    if edited_inner_html == region.content(source):
        return source
    if re.search(r'<\s*main(?:\s|>)', edited_inner_html, flags=re.I):
        raise UnsupportedDocument('nested main cannot be inserted')
    if re.search(r'(?:id\s*=\s*["\'](?:local-editor|me08-dialog)["\']|\bdata-local-|\bdata-me(?:0|1))', edited_inner_html, flags=re.I):
        raise UnsupportedDocument('editor runtime markers must be stripped before patching')
    return source[:region.content_start] + edited_inner_html + source[region.content_end:]
