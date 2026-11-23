# MetaEditor — Neutral Static Workpage (candidate, 22 November 2026)

## 23 November — Template-first entry for non-expert authors

The bounded neutral editor remains unchanged as a workpage controller. A separate [beginner chooser](starter-templates/README.md) now supplies four **synthetic, trusted static HTML source templates** and uses the existing builder to prepare individually editable files. The launcher is HTML-only, does not replace any already open document, and offers a recommended introductory page plus project, article and almost-empty options. MetaCanvas `metacanvas.templates.v1` scene templates are not interchangeable with these source HTML files. The [CI 45124239776](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45124239776) exercised chooser-to-work-to-save/reopen/clean-export/Undo for all models over real Linux Chrome `file://` at two widths. Human Windows usability remains unverified; no site deployment.

## 22 November — Source-identical live MAIOS test and bounded usability additions

**Verified outside a synthetic page:** [Actions 45045287380](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45045287380) passed all four jobs. The read-only `neutral-live-site-browser` job downloaded `https://maios.it/consulting-ai.html` and checked its complete Git blob against `0fda8ce0d9c1da544999d39fe5d9c05f54bc771d` from `maios_it/consulting-ai.html`; only then did the browser test run on the full published MAIOS source at 1440/390. **No production edit was attempted.**

The neutral controller now offers an explicitly labelled **element picker**, so an author can reach text without clicking it in the page, with scroll-to-target; and **duplicate/delete for newly inserted blocks only**, each with native work history. It refuses to duplicate a block containing `id` attributes, or to delete untouched author content. Those behaviors and source-fidelity roundtrip were exercised in the synthetic and live-page browser jobs. They do **not** imply the much broader edit gestures of Bridge11.

**Human Windows verification is available, not yet passed:** the same CI run produced artifact `metaeditor-neutral-windows-preview` (GitHub artifact ID `14762989805`), containing only a standalone work HTML generated from the synthetic fixture and [the acceptance protocol](WINDOWS_ACCEPTANCE_20261122.md). Download it from the run's Artifacts section, extract and open in Windows Chrome under `file://`. The [Bridge11 capability comparison](BRIDGE11_COMPARISON_20261122.md) distinguishes tested parity from remaining gaps: richer find/format/preview, editor usability, accessibility, paste/HTML trust and Windows behavior. Release Gate B is still partial.

**Owner:** K-UX-AI / Collaborative Communication Medium / MetaEditor Evolution  
**Status:** candidate in [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2). No public MetaEditor release or maios.it deployment.

## What has been built

This is a **bounded, opt-in editor for trusted static HTML pages** with exactly one `<main>` containing top-level sections (`main > section`) or article subsections (`main > article > section`). It is not a generic importer, CMS or runtime editor.

The existing [source-preserving exporter](static-page-source-adapter.js) owns exact clean HTML export. The [neutral static-page controller](neutral-static-page-editor.js) owns selection, contentEditable, insertion, transfer of inserted blocks and a single Undo/Redo history for this *new carrier*. The [builder](../../../tools/build_metaeditor_neutral_workpage.py) forms a standalone **working copy** from a trusted authored source. No private Bridge11 content or MAIOS draft HTML is bundled with the controller.

Three distinct objects matter:

- **Original source:** immutable HTML text embedded in the private working copy as JSON, used as the baseline for all clean exports.
- **Editable work file:** contains the controller and the original source. It preserves inserted-block identity across save, reopen and Undo/Redo. **It contains the entire original source, including any secrets already present. Do not share this file publicly.**
- **Clean HTML export:** strips transient editor attributes, never serializes the editing UI, and preserves the bytes outside `main` exactly. An unchanged page—or a page fully restored by Undo—exports byte-for-byte equal to the original source.

This is not the scene model `ccm.document.v1`, and does not change MetaCanvas's native scene controller or its public/private export semantics.

## Build and inspect a work file

Run from a checkout of K-UX-AI:

```bash
python tools/build_metaeditor_neutral_workpage.py \
  --source /path/to/trusted-static-original.html \
  --output /path/to/MetaEditor_Work.html
```

The builder refuses source/output identity, an already wrapped workpage, ambiguous/missing `main`, unsupported active embeds inside `main`, malformed body and overly large inputs. **It does not sanitize or sandbox an HTML document. Only run it on trusted source** whose scripts, images and external references you would already allow to run in your browser.

Open the generated working copy in a browser. Click a paragraph/heading/list text to select it; double-click or use “Modifica testo” to edit. The toolbar supports native rich-text bold/italic for a selected range, adding a paragraph or heading, moving an *added* block up/down or into a chosen section, Undo/Redo, working-file export and clean HTML export. Unselected, unsupported and no-op actions do not invent mutations.

After saving a working file, **verify it exists and reopen it**; a browser download request alone is not a durable write receipt. An exported work file retains its own immutable source snapshot and can continue editing without duplicating the UI.

## Evidence

[CI run 45043342858](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45043342858), three successful jobs: native Studio21 regression, repository contracts and the isolated neutral static-page browser test.

The [browser test](../../../tests/metaeditor-neutral-static-page.browser.py) exercises four combinations (1440/390 × two page topologies):

- **MAIOS-like synthetic fixture**, `main > section` — deliberately *not* the real MAIOS document.
- **MDN public-domain document (CC0)**, `main > article > section` — exact externally authored static HTML fixture, with CSS and links in the original source.

Observed within Linux Chrome: exact no-op export; selection and native bold formatting; text edit; insertion; transfer across sections; no-op check; one Undo/Redo; work save/reopen; inserted-block identity after reopen; pure HTML export preserving unchanged head/footer; full Undo returns exactly to original HTML.

A [separate test path](../../../tests/metaeditor-neutral-static-page.browser.py) accepts `--site-source` for **the actual MAIOS site checkout** without copying site HTML into this public tool repository. A [read-only private site workflow](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/.github/workflows/metaeditor-neutral-site-integration.yml) was added to the non-production site branch with the exact `consulting-ai.html` blob pinned. **Its CI outcome has not yet been retrieved and must not be asserted as passing.** It does not write to `maios_it/main` or deploy.

## Scope and still-open gates

This is an implemented, automatically tested **candidate**, not a stabilized all-purpose editor. It presently excludes complex or dynamically generated content in `main`, arbitrary HTML imports, React/CMS mutation, generic moving of protected original components, scene/diagram editing inside arbitrary pages, touch gesture proof, Chrome Windows `file://` proof, comprehensive accessibility, paste sanitization and broader hostile-input testing.

The clean-page export preserves authored HTML outside `main`, including original scripts and external resources; it **does not detect private information in ordinary text or make a page safe to publish**. The private-data filter for `ccm.document.v1` belongs to the separate MetaCanvas Studio carrier.

Before selecting a release, verify the adapter on the **real** MAIOS page and MDN source, extend the actual UX/accessibility and Windows testing, decide whether to integrate Bridge11's richer gestures or keep a narrower product surface, and complete Gate B–F release evidence. Publishing to MAIOS is a separate site-owner effect.

## Causal learning

The first controller history snapshot removed `data-local-block` together with transient markers. This made an added block lose its capacity to move after undo, despite visual HTML appearing restored. **A work/history representation must preserve editor-owned object identity; a clean/public representation must not.** After correction, the new tests cover transfer, Undo/Redo, work save/reopen and full restoration of original source.

An early test also searched the whole saved HTML for `data-local-selected`, but the string was present legitimately in the embedded controller code. The corrected test inspects the actual `main` region instead: source code text is not evidence that a runtime attribute leaked into the exported document.
