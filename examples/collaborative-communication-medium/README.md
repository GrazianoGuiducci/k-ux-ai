# AI Collaboration Studio — public preview

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
