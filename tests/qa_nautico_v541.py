"""Bounded Chromium regression checks for the exact K-UX-AI v5.4.1 lab HTML.

Run: python tests/qa_nautico_v541.py
Needs Python Playwright and a Chromium binary (or Playwright chromium install).
Uses page.set_content: no file:// navigation, persistent-storage or hosted app claims.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / 'labs/nautico-ui-v4/16-griglia-continuity-v541.html'
EXPECTED_SHA256 = '7e8a35dc21bdc6940e1ad00db47fbe9327237a33c6aede5a71aaf03f7d8f9716'


async def main():
    passed = []
    errors = []
    raw = HTML.read_bytes()
    def check(label, condition):
        if not condition:
            raise AssertionError(f'FAIL {label}')
        passed.append(label)
    check('source.sha256', hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256)
    async with async_playwright() as playwright:
        executable = os.environ.get('KUX_CHROMIUM') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
        browser = await playwright.chromium.launch(headless=True, executable_path=executable, args=['--no-sandbox'])
        for width, height, reduce in [(1440, 900, 'no-preference'), (390, 844, 'reduce'), (768, 860, 'no-preference'), (1680, 950, 'reduce')]:
            context = await browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=reduce)
            page = await context.new_page()
            page_errors = []
            page.on('pageerror', lambda err: page_errors.append(str(err)))
            await page.set_content(raw.decode('utf-8'), wait_until='domcontentloaded')
            await page.wait_for_timeout(120)
            tag = f'{width}x{height}/{reduce}'
            check(f'{tag}:home', await page.evaluate('window.KUXAIDemo?.perception().screen') == 'home')
            check(f'{tag}:version', await page.evaluate('window.KUXAIDemo?.version') == 'lab-2026-10-10-r5.4.1')
            check(f'{tag}:enter-ready', await page.locator('#startRecommended').is_visible())
            check(f'{tag}:default-prepared', len((await page.evaluate('window.KUXAIDemo.perception().homePreparation.selected'))) >= 1)
            await page.locator('#homeTourButton').click()
            check(f'{tag}:tour-open', await page.locator('#homeTourDialog').evaluate('(e)=>e.open'))
            check(f'{tag}:tour-spotlight', not await page.locator('#kuxTourSpotlight').evaluate('(e)=>e.hidden'))
            await page.locator('#homeTourNext').click()
            check(f'{tag}:tour-step-2', 'PASSO 2' in (await page.locator('#homeTourStep').inner_text()))
            await page.locator('#homeTourNext').click()
            check(f'{tag}:tour-step-3', 'PASSO 3' in (await page.locator('#homeTourStep').inner_text()))
            await page.keyboard.press('Escape')
            check(f'{tag}:tour-closed', not await page.locator('#homeTourDialog').evaluate('(e)=>e.open'))
            await page.locator('#startRecommended').click()
            await page.wait_for_timeout(160)
            check(f'{tag}:first-layout-auto', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'auto')
            await page.locator('#btnWorkMenu').click()
            check(f'{tag}:tools-open', not await page.locator('#workMega').evaluate('(e)=>e.hidden'))
            await page.locator('#layoutTwo').click()
            check(f'{tag}:manual-split', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'split')
            await page.locator('#btnHome').click()
            check(f'{tag}:home-return', (await page.evaluate('window.KUXAIDemo.perception().screen')) == 'home')
            await page.locator('#startRecommended').click()
            await page.wait_for_timeout(160)
            check(f'{tag}:split-restored', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'split')
            # Context-specific views should retain different operator placements.
            await page.locator('#kuxContextTrigger').click()
            await page.locator('#kuxContextChoices [data-work-context="fornitori"]').click()
            check(f'{tag}:supplier-context', (await page.evaluate('window.KUXAIDemo.perception().view.context')) == 'fornitori')
            check(f'{tag}:supplier-default-auto', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'auto')
            await page.locator('#btnWorkMenu').click()
            await page.locator('#layoutThree').click()
            check(f'{tag}:supplier-triple', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'triple')
            await page.locator('#btnHome').click()
            await page.locator('#startRecommended').click()
            check(f'{tag}:supplier-triple-restored', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'triple')
            await page.locator('#kuxContextTrigger').click()
            await page.locator('#kuxContextChoices [data-work-context="poppa"]').click()
            check(f'{tag}:poppa-split-isolated', (await page.evaluate('window.KUXAIDemo.perception().layout')) == 'split')
            # Editor under a simulated source event: value AND caret/focus must survive.
            await page.locator('#btnQuickAdd').click()
            await page.locator('#picker .picker-item').filter(has_text='Fare').first.click()
            editor = page.locator('textarea.note-editor').first
            await editor.fill('Contributo mentre la fonte cambia.')
            await editor.focus()
            await editor.evaluate('(e)=>e.setSelectionRange(12,12)')
            check(f'{tag}:editor-before', await editor.evaluate('(e)=>e.selectionStart') == 12)
            await page.locator('#btnEvent').evaluate('(e)=>e.click()')
            await page.wait_for_timeout(100)
            editor = page.locator('textarea.note-editor').first
            check(f'{tag}:editor-value', await editor.input_value() == 'Contributo mentre la fonte cambia.')
            check(f'{tag}:editor-focused', await editor.evaluate('(e)=>e===document.activeElement'))
            check(f'{tag}:editor-caret', await editor.evaluate('(e)=>e.selectionStart') == 12)
            check(f'{tag}:no-js-errors', len(page_errors) == 0)
            errors.extend([f'{tag}: {x}' for x in page_errors])
            await context.close()
        await browser.close()
    report = {'candidate': 'v5.4.1', 'source_sha256': EXPECTED_SHA256, 'method': 'Chromium Playwright page.set_content (no hosted runtime)', 'checks_passed': len(passed), 'checks_total': len(passed), 'all_passed': True, 'viewport_modes': ['1440x900 normal', '390x844 reduced motion', '768x860 normal', '1680x950 reduced motion'], 'checks': passed, 'page_errors': errors, 'unverified': ['Edge physical browser', 'file:// navigation', 'persistent browser storage across sessions', 'real Nautico controllers', 'real AI/host and permissions', 'touchscreen and assistive technology']}
    print(json.dumps({k: v for k,v in report.items() if k != 'checks'}, ensure_ascii=False, indent=2))
    (ROOT / 'labs/nautico-ui-v4/EVIDENCE_CONTINUITY_V541_20261010.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    asyncio.run(main())
