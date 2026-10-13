"""Keep the standalone first encounter styled from its single CSS owner."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'examples/kernel-mirror/index.html'
page = path.read_text(encoding='utf-8')
page = page.replace('<link rel="stylesheet" href="../../src/ui/kernel-grid.css">', '')
style = '<style id="kernel-grid-styles">' + (ROOT / 'src/ui/kernel-grid.css').read_text(encoding='utf-8') + '</style>'
if 'id="kernel-grid-styles"' in page:
    page = re.sub(r'<style id="kernel-grid-styles">.*?</style>', lambda _: style, page, flags=re.S)
else:
    page = page.replace('</head>', style + '\n</head>', 1)
path.write_text(page, encoding='utf-8', newline='\n')
