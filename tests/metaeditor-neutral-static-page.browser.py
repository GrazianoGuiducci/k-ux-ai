#!/usr/bin/env python3
"""Exercise one neutral MetaEditor controller on two real static HTML topologies.

Fixture A resembles the MAIOS main>section structure but contains ONLY
synthetic content. Fixture B is MDN's CC0 HTML (main>article>section).
This is NOT yet a test of the private original MAIOS page or Windows file://.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_metaeditor_neutral_workpage import build, LAB, MODULES
from metaeditor_region_patch import locate_main

FIXTURES = ROOT / 'tests/fixtures/metaeditor'
CASES = [
    ('maios_topology_synthetic.html', 'main > section'),
    ('mdn_original_cc0.html', 'main > article > section')
]


def verify_unmodified_outside(source: str, exported: str):
    first = locate_main(source)
    second = locate_main(exported)
    assert exported[:second.content_start] == source[:first.content_start]
    assert exported[second.content_end:] == source[first.content_end:]
    assert '<script id="me-neutral-' not in exported
    assert 'data-local-' not in second.content(exported)
    assert 'contenteditable=' not in second.content(exported)


def load(page, work: str, address: str):
    page.route('**/*', lambda route: route.abort())
    page.route(address, lambda route: route.fulfill(
        status=200, headers={'content-type':'text/html; charset=utf-8'}, body=work))
    page.goto(address, wait_until='domcontentloaded')
    page.wait_for_function('() => !!window.metaEditorPage')
    assert page.locator('#me-neutral-toolbar').count() == 1
    assert page.locator('#me-neutral-style').count() == 1


def run(browser, name: str, selector: str, width: int, source_path: Path | None = None):
    source = (source_path or (FIXTURES / name)).read_text(encoding='utf-8')
    adapter, controller = [(LAB / path).read_text(encoding='utf-8') for path in MODULES]
    work = build(source, adapter, controller)
    assert source not in work or 'me-neutral-original-source' in work
    page = browser.new_page(viewport={'width':width,'height':844}, accept_downloads=True)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    base = 'https://neutral.test/'
    try:
        load(page, work, base + 'work.html')
        result = page.evaluate('() => window.metaEditorPage.status()')
        assert result['carrier'] == 'static-page' and result['regions'] >= 2
        assert result['regions'] == page.locator(selector).count()
        assert page.evaluate('() => window.metaEditorPage.cleanHtml()') == source, (name,width,'no-op changed source')

        # Select a real author paragraph; editing is opt-in and does not
        # rewrite the remaining original page.
        target = page.locator('main p').first
        page.evaluate('() => window.metaEditorPage.select(document.querySelector("main p"))')
        edited = page.evaluate('() => window.metaEditorPage.edit()')
        assert edited['ok']
        target.fill('Edited paragraph with author-intended content')
        assert target.get_attribute('contenteditable') == 'true'
        # Exercise native contenteditable formatting without a second engine.
        page.evaluate("""() => {
            const node=document.querySelector('main p');
            const range=document.createRange();
            range.selectNodeContents(node);
            const selection=document.getSelection();
            selection.removeAllRanges(); selection.addRange(range);
        }""")
        bold = page.evaluate('() => window.metaEditorPage.format("bold")')
        assert bold['ok'], (name,width,'bold formatting unavailable')
        target.evaluate('(node) => node.blur()')
        assert page.evaluate('() => window.metaEditorPage.status().canUndo')
        assert 'bold' in page.evaluate('() => window.metaEditorPage.cleanHtml()').lower() or (
            '<b>' in page.evaluate('() => window.metaEditorPage.cleanHtml()')
        )

        # The same UI works on both structures. New blocks have the only
        # transfer authority; original HTML sections remain structural.
        page.locator('#me-neutral-section').select_option('0')
        page.locator('[data-me-action="insert-p"]').evaluate('(button)=>button.click()')
        added = page.locator('main [data-local-block]')
        assert added.count() == 1
        assert page.locator(selector).first.locator('[data-local-block]').count() == 1, (
            name, width, selector,
            page.evaluate("""(selector) => ({
                sectionCount: document.querySelectorAll(selector).length,
                sectionHits: [...document.querySelectorAll(selector)].map(
                    s => [...s.querySelectorAll('[data-local-block]')].map(x=>x.outerHTML.slice(0,160))
                ),
                selection: document.querySelector('#me-neutral-section')?.value,
                block: document.querySelector('main [data-local-block]')?.parentElement?.outerHTML.slice(0,220)
            })""", selector)
        )
        page.evaluate('() => window.metaEditorPage.edit()')
        added.fill('Portable added block')
        added.evaluate('(node) => node.blur()')
        page.locator('#me-neutral-section').select_option('1')
        moved = page.evaluate('() => window.metaEditorPage.move("transfer")')
        assert moved['changed'], (name,width,'block did not transfer')
        assert page.locator(selector).nth(1).locator('[data-local-block]').count() == 1
        assert 'Portable added block' in page.locator(selector).nth(1).inner_text()

        # Repeat the same destination: an invalid/no-op movement cannot
        # create a history checkpoint or change the document.
        status_before = page.evaluate('() => window.metaEditorPage.status()')
        repeated = page.evaluate('() => window.metaEditorPage.move("transfer")')
        assert repeated['changed'] is False
        assert page.evaluate('() => window.metaEditorPage.status()') == status_before

        page.evaluate('() => window.metaEditorPage.undo()')
        assert page.locator(selector).first.locator('[data-local-block]').count() == 1
        page.evaluate('() => window.metaEditorPage.redo()')
        assert page.locator(selector).nth(1).locator('[data-local-block]').count() == 1

        clean = page.evaluate('() => window.metaEditorPage.cleanHtml()')
        verify_unmodified_outside(source, clean)
        assert 'Edited paragraph with author-intended content' in clean
        assert 'Portable added block' in clean
        assert 'data-local-block' not in clean
        assert clean != source
        work_saved = page.evaluate('() => window.metaEditorPage.workHtml()')
        assert 'me-neutral-original-source' in work_saved
        assert 'data-local-block' in work_saved
        # The controller code legitimately contains the attribute names as
        # strings: inspect the real document region, not the entire work file.
        work_region = locate_main(work_saved).content(work_saved)
        assert 'data-local-selected' not in work_region
        assert 'contenteditable="true"' not in work_region
        assert not errors, (name,width,errors)

        # Reversing every committed edit in the original working session must
        # restore exact original source bytes, not merely a visual approximation.
        for _ in range(12):
            if not page.evaluate('() => window.metaEditorPage.status().canUndo'):
                break
            assert page.evaluate('() => window.metaEditorPage.undo()')['changed']
        assert page.evaluate('() => window.metaEditorPage.cleanHtml()') == source, (
            name, width, 'full Undo changed original static source'
        )
        second = browser.new_page(viewport={'width':width,'height':844},accept_downloads=True)
        errors2 = []
        second.on('pageerror', lambda error: errors2.append(str(error)))
        try:
            load(second, work_saved, base + 'saved-work.html')
            assert second.evaluate('() => window.metaEditorPage.cleanHtml()') == clean, (name,width,'work reopen drift')
            assert second.locator('main [data-local-block]').count() == 1
            assert second.locator('#me-neutral-toolbar').count() == 1
            assert second.evaluate('() => window.metaEditorPage.status().regions') == page.locator(selector).count()
            # Moving an existing block after reopening must remain possible.
            second.evaluate('() => window.metaEditorPage.select(document.querySelector("main [data-local-block]"))')
            second.locator('#me-neutral-section').select_option('0')
            transferred = second.evaluate('() => window.metaEditorPage.move("transfer")')
            assert transferred['changed'], (name,width,'lost inserted-block identity after reopen')
            assert second.locator(selector).first.locator('[data-local-block]').count() == 1
            assert second.evaluate('() => window.metaEditorPage.undo()')['changed']
            assert second.evaluate('() => window.metaEditorPage.cleanHtml()') == clean
            assert not errors2, (name,width,errors2)
        finally:
            second.close()
        print('PASS',name,width,'no-op exact, format/edit, insert/transfer, Undo/Redo, clean/work/reopen')
    finally:
        page.close()


def negative_cases():
    adapter, controller = [(LAB / path).read_text(encoding='utf-8') for path in MODULES]
    for html in [
        '<html><body><p>No main</p></body></html>',
        '<html><body><main>x</main><main>y</main></body></html>',
        '<html><body><main><script>alert(1)</script></main></body></html>',
        '<html><body><main>Unclosed',
    ]:
        try:
            build(html, adapter, controller)
        except ValueError:
            pass
        else:
            raise AssertionError('unsafe/unbounded document was not rejected')
    src = '<html><body><main><p>x</p></main></body></html>'
    result = build(src, adapter, controller)
    try:
        build(result, adapter, controller)
    except ValueError:
        pass
    else:
        raise AssertionError('work page nested installer accepted')
    print('PASS static-page builder rejected unsupported and nested work pages')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', default=None)
    parser.add_argument('--chromium', default=None)
    parser.add_argument('--site-source', type=Path,
                        help='Trusted original MAIOS HTML from a separate private site checkout')
    parser.add_argument('--site-only', action='store_true',
                        help='Run only the explicit --site-source integration case')
    args = parser.parse_args()
    if args.site_only and not args.site_source:
        parser.error('--site-only requires --site-source')
    negative_cases()
    opts = {'headless': True, 'args':['--no-sandbox']}
    if args.channel: opts['channel'] = args.channel
    if args.chromium: opts['executable_path'] = args.chromium
    with sync_playwright() as play:
        browser = play.chromium.launch(**opts)
        try:
            if not args.site_only:
                for name, selector in CASES:
                    for width in (1440,390):
                        run(browser,name,selector,width)
            if args.site_source:
                if not args.site_source.is_file():
                    raise FileNotFoundError(args.site_source)
                for width in (1440,390):
                    run(browser,'MAIOS-original', 'main > section', width, args.site_source)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
