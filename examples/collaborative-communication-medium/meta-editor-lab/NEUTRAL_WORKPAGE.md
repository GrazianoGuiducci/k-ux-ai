# MetaEditor — Neutral Static Workpage (candidate, 22 November 2026)

**Owner:** K-UX-AI / Collaborative Communication Medium / MetaEditor Evolution  
**Status:** candidate in [PR #2](https://github.com/GrazianoGuiducci/k-ux-ai/pull/2). No public MetaEditor release or maios.it deployment.

## What has been built

This is a **bounded, opt-in editor for trusted static HTML pages** with exactly one \`<main>\` containing top-level sections (\`main > section\`) or article subsections (\`main > article > section\`). It is not a generic importer, CMS or runtime editor.

The existing [source-preserving exporter](static-page-source-adapter.js) owns exact clean HTML export. The [neutral static-page controller](neutral-static-page-editor.js) owns selection, contentEditable, insertion, transfer of inserted blocks and a single Undo/Redo history for this *new carrier*. The [builder](../../../tools/build_metaeditor_neutral_workpage.py) forms a standalone **working copy** from a trusted authored source. No private Bridge11 content or MAIOS draft HTML is bundled with the controller.

Three distinct objects matter:

- **Original source:** immutable HTML text embedded in the private working copy as JSON, used as the baseline for all clean exports.
- **Editable work file:** contains the controller and the original source. It preserves inserted-block identity across save, reopen and Undo/Redo. **It contains the entire original source, including any secrets already present. Do not share this file publicly.**
- **Clean HTML export:** strips transient editor attributes, never serializes the editing UI, and preserves the bytes outside \`main\` exactly. An unchanged page—or a page fully restored by Undo—exports byte-for-byte equal to the original source.

This is not the scene model \`ccm.document.v1\`, and does not change MetaCanvas's native scene controller or its public/private export semantics.

## Build and inspect a work file

Run from a checkout of K-UX-AI:

\`\`\`bash
python tools/build_metaeditor_neutral_workpage.py \
  --source /path/to/trusted-static-original.html \
  --output /path/to/MetaEditor_Work.html
\`\`\`

The builder refuses source/output identity, an already wrapped workpage, ambiguous/missing \`main\`, unsupported active embeds inside \`main\`, malformed body and overly large inputs. **It does not sanitize or sandbox an HTML document. Only run it on trusted source** whose scripts, images and external references you would already allow to run in your browser.

Open the generated working copy in a browser. Click a paragraph/heading/list text to select it; double-click or use “Modifica testo” to edit. The toolbar supports native rich-text bold/italic for a selected range, adding a paragraph or heading, moving an *added* block up/down or into a chosen section, Undo/Redo, working-file export and clean HTML export. Unselected, unsupported and no-op actions do not invent mutations.

After saving a working file, **verify it exists and reopen it**; a browser download request alone is not a durable write receipt. An exported work file retains its own immutable source snapshot and can continue editing without duplicating the UI.

## Evidence

[CI run 45043342858](https://github.com/GrazianoGuiducci/k-ux-ai/actions/runs/45043342858), three successful jobs: native Studio21 regression, repository contracts and the isolated neutral static-page browser test.

The [browser test](../../../tests/metaeditor-neutral-static-page.browser.py) exercises four combinations (1440/390 × two page topologies):

- **MAIOS-like synthetic fixture**, \`main > section\` — deliberately *not* the real MAIOS document.
- **MDN public-domain document (CC0)**, \`main > article > section\` — exact externally authored static HTML fixture, with CSS and links in the original source.

Observed within Linux Chrome: exact no-op export; selection and native bold formatting; text edit; insertion; transfer across sections; no-op check; one Undo/Redo; work save/reopen; inserted-block identity after reopen; pure HTML export preserving unchanged head/footer; full Undo returns exactly to original HTML.

A [separate test path](../../../tests/metaeditor-neutral-static-page.browser.py) accepts \`--site-source\` for **the actual MAIOS site checkout** without copying site HTML into this public tool repository. A [read-only private site workflow](https://github.com/GrazianoGuiducci/maios_it/blob/work/metaeditor-current/.github/workflows/metaeditor-neutral-site-integration.yml) was added to the non-production site branch with the exact \`consulting-ai.html\` blob pinned. **Its CI outcome has not yet been retrieved and must not be asserted as passing.** It does not write to \`maios_it/main\` or deploy.

## Scope and still-open gates

This is an implemented, automatically tested **candidate**, not a stabilized all-purpose editor. It presently excludes complex or dynamically generated content in \`main\`, arbitrary HTML imports, React/CMS mutation, generic moving of protected original components, scene/diagram editing inside arbitrary pages, touch gesture proof, Chrome Windows \`file://\` proof, comprehensive accessibility, paste sanitization and broader hostile-input testing.

The clean-page export preserves authored HTML outside \`main\`, including original scripts and external resources; it **does not detect private information in ordinary text or make a page safe to publish**. The private-data filter for \`ccm.document.v1\` belongs to the separate MetaCanvas Studio carrier.

Before selecting a release, verify the adapter on the **real** MAIOS page and MDN source, extend the actual UX/accessibility and Windows testing, decide whether to integrate Bridge11's richer gestures or keep a narrower product surface, and complete Gate B–F release evidence. Publishing to MAIOS is a separate site-owner effect.

## Causal learning

The first controller history snapshot removed \`data-local-block\` together with transient markers. This made an added block lose its capacity to move after undo, despite visual HTML appearing restored. **A work/history representation must preserve editor-owned object identity; a clean/public representation must not.** After correction, the new tests cover transfer, Undo/Redo, work save/reopen and full restoration of original source.

An early test also searched the whole saved HTML for \`data-local-selected\`, but the string was present legitimately in the embedded controller code. The corrected test inspects the actual \`main\` region instead: source code text is not evidence that a runtime attribute leaked into the exported document.
