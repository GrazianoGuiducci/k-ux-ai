#!/usr/bin/env python3
"""Build an opt-in, local MetaEditor working copy of one trusted static HTML page.

The ORIGINAL is never changed. The generated work page embeds its immutable
original text and the existing source-preserving exporter plus one neutral
static-page controller. This does not make unknown/external HTML safe to open.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from metaeditor_region_patch import locate_main, UnsupportedDocument

HERE = Path(__file__).resolve().parents[1]
LAB = HERE / 'examples/collaborative-communication-medium/meta-editor-lab'
MODULES = ('static-page-source-adapter.js', 'neutral-static-page-editor.js')
MARKER = 'id="me-neutral-original-source"'


def build(original: str, source_adapter: str, editor: str) -> str:
    if not isinstance(original, str) or not original.strip():
        raise ValueError('The HTML source must be non-empty Unicode text.')
    if MARKER in original or 'id="me-neutral-toolbar"' in original:
        raise ValueError('This is already a MetaEditor work file; do not nest another editor.')
    if len(original.encode('utf-8')) > 2_000_000:
        raise ValueError('Input HTML exceeds 2 MB bounded prototype limit.')
    try:
        region = locate_main(original)
    except UnsupportedDocument as e:
        raise ValueError('Unsupported main region: ' + str(e)) from e
    inner = region.content(original)
    if re.search(r'<\s*(?:script|style|iframe|object|embed|template)\b', inner, re.I):
        raise ValueError('Active or embedded content inside main is unsupported.')
    body = list(re.finditer(r'</\s*body\s*>', original, flags=re.I))
    if len(body) != 1:
        raise ValueError('Exactly one closing body tag required.')
    for name, text in zip(MODULES, (source_adapter, editor)):
        if '</script' in text.lower():
            raise ValueError('Refusing unsafe script-close sequence in ' + name)
    # Escape opening angle brackets in embedded JSON: even literal </script>
    # in the original source cannot terminate this inert script element.
    payload = json.dumps({'source': original}, ensure_ascii=True).replace('<', r'\u003c')
    tag = (
        '\n<!-- MetaEditor private opt-in workbench. Do not share this work file:'
        ' it embeds the complete original source. -->\n'
        '<script type="application/json" id="me-neutral-original-source">' + payload + '</script>\n'
        '<script id="me-neutral-source-adapter">' + source_adapter + '</script>\n'
        '<script id="me-neutral-editor-controller">' + editor + '</script>\n'
        '<script id="me-neutral-start">(function(){'
        'const json=document.getElementById("me-neutral-original-source").textContent;'
        'const sourceHtml=JSON.parse(json).source;'
        'window.metaEditorPage=window.MetaEditorNeutralStaticPage.mount({document,sourceHtml});'
        '})();</script>\n'
    )
    return original[:body[0].start()] + tag + original[body[0].start():]


def main():
    parser = argparse.ArgumentParser(description='Create a private local MetaEditor HTML working file.')
    parser.add_argument('--source', type=Path, required=True, help='Trusted original HTML file')
    parser.add_argument('--output', type=Path, required=True, help='New standalone work HTML')
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if source == output:
        parser.error('Source and output must differ; the original will not be overwritten.')
    if output.exists():
        parser.error('Output already exists; explicit overwrite is not supported.')
    raw = source.read_text(encoding='utf-8')
    work = build(raw, *(LAB / module).read_text(encoding='utf-8') for module in MODULES)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(work, encoding='utf-8')
    print('CREATED', output, 'original bytes', len(raw.encode('utf-8')),
          'work bytes', len(work.encode('utf-8')))
    print('The editor is a working copy of trusted HTML only; no source was modified.')


if __name__ == '__main__':
    main()
