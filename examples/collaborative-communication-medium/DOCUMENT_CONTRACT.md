# Portable document and AI collaboration

The document is a **single editable HTML file**. Its canonical state is JSON under `<script id="ccm-data" type="application/json">`, schema `ccm.document.v1`; rendered SVG/cards are views, not separate sources of truth.

- `scenes[]`: ordered editable slides/workspaces with stable IDs and titles.
- `elements[]`: labels, cards, notes, images, shapes and sections, with properties/geometry.
- `links[]`: semantic references through `from` and `to` node IDs, labels, endpoints, optional ports, route and arrowheads.
- `ui`: operator preferences, **not** assertions about external reality.
- Notes/private elements: usable in the working document but to be excluded from the public copy and checked before sharing.

**Suggested LLM request:** “Read the JSON document model rather than relying only on a screenshot. Summarize the relation between nodes and links, identify uncertainty, then propose a clearer structure for [audience/objective]. Preserve my original concepts and private notes in the working copy, distinguish your changes, return a complete editable HTML and summarize the differences.”

Do not break `from`/`to` IDs when reorganizing. The HTML carries the editor source and its MPL notice when exported; keep the license/copyright notice. Do not mistake downloaded/previewed files for verified external effects. No AI service is embedded in this file.
