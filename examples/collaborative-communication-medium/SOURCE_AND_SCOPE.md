# Source, scope and exercise

This public tool was derived from the **neutral Studio 12** artifact developed through operator/AI collaboration and the AI Collaboration Studio preview, 13 November 2026. It contains only synthetic examples, not customer documents or the operator's internal research/project data. It is an autonomous browser medium, not a change to K-UX-AI's runtime API.

**Owners:** product and public competence: `GrazianoGuiducci/k-ux-ai`, `competences/ux-ai/collaborative-communication-medium/`. Private construction and learning: `GrazianoGuiducci/tm7` on the `gpt/ux-ai-code-competence` work lane. The public source is sufficient to use the tool without private access.

**License scope:** `MPL-2.0` applies to the files in **this directory** (HTML application, documentation, example source), not automatically the rest of K-UX-AI. Copyright on the original tool source: **2026 Graziano Guiducci**. Contributors retain copyrights on their own additions, subject to the MPL terms for covered files. Trademarks and logos are not licensed.

**Verified in local Chromium:** embedded JS syntax, startup and four example scenes, guide access, HTML title edit/download/reopen preserving document JSON and license notice, 390 px viewport without horizontal overflow, no observed JavaScript errors in these pathways. This is not a comprehensive security, accessibility or compatibility certification. Direct `file://` in real user browsers, third-party presentation reception and actual PDF output remain distinct tests.

## MetaCanvas 0.1.1 — continuation evidence (13 November 2026)

Added a bounded round-trip import of `ccm.document.v1` from JSON or a self-contained HTML export, without executing received HTML. Tests exercised JSON/HTML import, undo/redo, rejection of dangling relations and cancelled confirmations, public-copy exclusion of private notes/library markers, retention of the MPL notice, 390px layout and no page errors. This does not claim a full security audit, production site integration or real human comprehension. The standalone file remains the product; MAIOS.it's resources page is owned by a distinct Codex/TM9 workflow.

## Studio 14 — exercised local UI fixes, 13 November 2026

Operator-reported issues: floating Tools resize non-functional, Presenta blank, wasted horizontal space, and difficulty leaving edit mode. Reproduced the empty presentation canvas: editor grid hid its sidebar while the canvas grid column measured zero. Repaired presentation sizing; moved resize affordances to an overlay not clipped or scrolled with the Tools contents; added Flat layout and a compact edit toolbar with OK/undo/redo. The HTML retains original MPL-2.0 notice.

**Local evidence:** Chromium/Playwright tests on four example slides showing nonzero canvas in Presenta and correct navigation/Escape; floating corner drag 574×400→628×494, top/bottom dock height drags; Flat reading 900→1333 px at desktop with two-column CSS and mobile single column; edit toolbar with undo/redo single-step behavior; exported HTML reopened with saved preferences, presentable content and controls intact; public export excludes test private notes/library entries; mobile viewport 390 px without horizontal overflow. JavaScript syntax checked with Node. These are bounded local tests, not physical touch/browser-file-open, full accessibility or security certification. No MAIOS.it deployment or K-UX-AI runtime integration is implied.


## MetaCanvas Studio 15 — reusable template semantics (13 November 2026)

Operator's direct differences: insertion of built-in templates must be undoable and offer explicit replace/above/below; edited templates should be reusable in the same document and portable to others.

**Local test evidence:** Chromium/Playwright 31 browser assertions on built-in template placement, confirmed/cancelled replace, undo/redo, five-slide batch as one undo, named custom saved templates, export/import into a second editor, reference integrity, working HTML save/reopen, public-copy exclusion of personal template data and DOM, and MPL preservation. A second test exercised private-note sanitization and rejection of external image URLs in imported packs. Embedded JavaScript passed Node syntax check. These are not physical touch/browser compatibility, comprehensive security or multi-user collaboration certification. The site deployment remains a separate Codex/TM9 owner.
