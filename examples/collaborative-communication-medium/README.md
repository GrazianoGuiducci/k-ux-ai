# AI Collaboration Studio — public preview

## AI Consulting demo — Studio 21 IT/EN

Alongside the generic Studio 20 editor, this repository distributes **two separate standalone demonstration files** adapted from the latest AI consulting page supplied by the operator:

- [**Download Studio 21 — English demo**](MetaCanvas_Studio21_Consulenza_EN.html)
- [**Scarica Studio 21 — demo italiana**](MetaCanvas_Studio21_Consulenza_IT.html)

Each contains seven editable slides, plus **Show demo** and **Blank canvas** controls. The English version uses English slides, main editor controls, guidance and built-in templates; the Italian version remains Italian. Both work without an embedded AI service and preserve an editable HTML file for external model collaboration. The future MAIOS.it resource catalogue will have distinct IT and EN Tool pages pointing to the matching files; no website deployment is claimed. [Site-owner handoff](MAIOS_RESOURCE_TOOL_HANDOFF.md). Studio 20 remains the generic standalone editor.



## Current download — MetaCanvas Studio 20 (13 November 2026)

**[Download the standalone editor](AI_Collaboration_Studio.html)** · [Open the source on GitHub](https://github.com/GrazianoGuiducci/k-ux-ai/blob/main/examples/collaborative-communication-medium/AI_Collaboration_Studio.html) · 272,490 bytes · SHA-256 `c8c1be74c7d9b91d99b0c7888c40cee387579ca26f3079d0fa44ea81f1817a19`.

MetaCanvas is a single-file, offline-capable tool for arranging, editing and presenting diagrams, ideas and slide sequences. It has four neutral starter slides; no AI account or embedded AI service is required. The UI remains Italian. Open the HTML locally in a modern browser, work on your content, then use **Salva lavoro** to download an independent working copy (not a save-over of the original).

**Studio 20 changes:** compact responsive Standard/Flat workspaces, movable editors and tool panels, slide reordering, labelled arrows, reversible reusable templates and a restrained AI exchange flow. **Dati per AI** prompts for whole-document versus selected-slide export; private notes and personal collections are excluded by default. On return, **Importa JSON / HTML** previews new/modified/missing slides and permits selective, undoable integration or a confirmed full replacement, preserving local private notes in selective merges. An optional local browser recovery copy is OFF by default and is not a cloud backup. Thumbnail links follow the diagram routing more closely.

**Sharing:** review all visible text and inserted assets before handing the file to anyone. Data labelled private is filtered by the dedicated public/export actions, but secrets inside ordinary text are not detectable automatically. Import reads structural data only, refuses remote image URLs, and does not execute imported scripts. This is not a full security audit or multiuser/live AI collaboration. The recovery feature was tested with simulated storage; actual `file://` browser storage is subject to the user's browser.

**Historical release notes** below describe the behavior of earlier editions; their older replacement-only workflow does not describe Studio 20.

[Italian instructions](README.it.md) · [document contract](DOCUMENT_CONTRACT.md) · [site resource handoff](MAIOS_RESOURCE_TOOL_HANDOFF.md).


An **editable standalone HTML** for organizing ideas, diagrams and presentations, exchanging the same working file with an LLM, and presenting results to people.

**Quick start:** open `AI_Collaboration_Studio.html` in an up-to-date browser, edit one of four starter scenes or start blank, save HTML, attach the saved file to your AI chat and ask for a structured revision, then reopen the revised HTML. Use **Presenta** for human presentations. The editor UI is currently Italian. It includes no embedded AI service, server or live synchronization.

The document model resides in `<script id="ccm-data" type="application/json">` under schema `ccm.document.v1`. For meaningful AI collaboration, preserve node IDs and link referents and distinguish the operator's content from proposed additions. The public export removes private notes and library data, but an HTML file remains inspectable.

## MetaCanvas 0.1.1 — returning from an LLM

The AI workflow now has a **return path without hand-editing the HTML application source**.

1. In the Italian UI open **Strumenti → Salva ed esporta → Dati per AI** to export JSON.
2. Give the JSON to an LLM and ask it to preserve the `ccm.document.v1` schema, stable scene/element IDs and link `from`/`to` referents.
3. Use **Importa JSON / HTML** in the editor to load returned JSON or an entire MetaCanvas HTML file.
4. Confirm the document title and slide count, review the result, and use Undo if you need to restore the previous document. Save a new standalone HTML when satisfied.

Only the structural JSON is imported; scripts/styles from a received HTML file are **not executed**. Incompatible schema, duplicate IDs, dangling links and oversized files are rejected. Import **replaces the current document after confirmation**, rather than merging two histories. Human verification of AI-proposed content remains necessary.

## Studio 14 — Present, Flat layout, tools and editing

Four interaction fixes are now in the standalone HTML:

1. **Presenta** shows the diagram canvas instead of an empty slide when editor panels are hidden.
2. The **Strumenti** panel can be resized with the edge handle across docking modes; in floating mode drag its lower-right corner to change width and height.
3. **Flat** in the header and Tools panel reduces framing/margins and widens the reading view; large screens can use a two-column reading layout. Diagram coordinates are unchanged.
4. During editing, a compact **OK · Indietro · Avanti** control appears. OK confirms/exits editing; the other actions undo/redo document steps.

Preferences and controls are retained in saved standalone HTML. The application interface is currently in Italian. This remains an offline browser editor without embedded AI or server functions.

## Studio 15 — Reusable templates and placement

Under **Strumenti → Template agentici** (Italian UI), each built-in or user-saved template has **Sostituisci** (replace current slide, after confirmation), **↑ Sopra** (insert before) and **↓ Sotto** (insert after). Each insertion, including the five-slide example route, is a single **Undo/Redo** operation.

Use **☆ Salva questa scheda come template** to save the current edited slide as a named reusable model. Personal templates persist in the **saved working HTML**. Use **↓ Esporta raccolta JSON** to transfer them to another MetaCanvas document and **↑ Importa raccolta JSON** to import without changing the slides. Imported templates are undoable.

Speaker notes and private elements are excluded from saved templates, but review other text and details before sharing. **Public copy** strips the personal template collection and its rendered list from the exported HTML.

[Template collection contract](TEMPLATE_COLLECTION.md) · [Document contract](DOCUMENT_CONTRACT.md).

## License and ownership

**Mozilla Public License 2.0 (MPL-2.0)**, scoped to the files **in this tool directory only**. Everyone may use, modify, distribute and commercialize the tool under the MPL. Distributed modifications of covered files must make their source available under the MPL. Original software contributions remain **Copyright (c) 2026 Graziano Guiducci**; contributors retain rights in their own additions. The license does not grant trademark or logo rights.

[Full license](LICENSE) · [Document contract](DOCUMENT_CONTRACT.md) · [Italian instructions](README.it.md).

This license does not change the licensing of the K-UX-AI kernel, competences or other repository examples. This preview is not a runtime integration or a live MAIOS.it release.
