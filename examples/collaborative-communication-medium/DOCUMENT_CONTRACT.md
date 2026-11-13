# Portable document and AI collaboration

## Studio 20 — selective AI round-trip (current behavior)

The present editor continues to use `ccm.document.v1` and the same standalone HTML carrier. **Dati per AI** exposes an explicit whole-document/current-scene choice; notes, private-marked nodes, personal library and `savedTemplates` are excluded by default. An operator can opt to include them knowingly. Ordinary unmarked text may still contain sensitive content, so review before transfer.

An incoming JSON/HTML model is validated and **compared before commitment**. The comparison distinguishes changed, new and absent scenes; it does not infer semantic truth. The operator can integrate selected scenes (preserving unrelated local scenes and local private notes) or replace the entire document with a separate confirmation. Both are undoable as one history checkpoint. Incoming HTML scripts and styles are never executed, and remote `image.src` URLs are rejected.

A separate optional browser-local recovery snapshot is initially disabled and is not included in public copies. Storage capability and persistence vary by browser/origin, including `file://`; it cannot substitute for a saved HTML. Current UI/layout preferences do not change semantic object identity. The older 'replacement-only' contract below documents the historical 0.1.1 behavior, not the current Studio 20 workflow.


The document is a **single editable HTML file**. Its canonical state is JSON under `<script id="ccm-data" type="application/json">`, schema `ccm.document.v1`; rendered SVG/cards are views, not separate sources of truth.

- `scenes[]`: ordered editable slides/workspaces with stable IDs and titles.
- `elements[]`: labels, cards, notes, images, shapes and sections, with properties/geometry.
- `links[]`: semantic references through `from` and `to` node IDs, labels, endpoints, optional ports, route and arrowheads.
- `ui`: operator preferences, **not** assertions about external reality.
- Notes/private elements: usable in the working document but to be excluded from the public copy and checked before sharing.

## Studio 15 — personal reusable templates

The working model may include `savedTemplates[]`, a set of user-saved slide patterns with stable collection IDs and transferable scene content. A template instantiation creates a **new scene identity**, remaps element/link IDs and section container references, and inserts one of three ways: replace, above or below the active slide. Each is undoable as one operation. Saving/deleting/importing personal templates are also undoable.

Template packs are JSON under `metacanvas.templates.v1`. They may be exported and imported into another standalone HTML document. **Public export removes both the template collection from the JSON and the rendered personal-template list from the DOM**; ordinary private working HTML preserves the collection. Notes and explicitly private elements are excluded when saving templates, but remaining text/detail fields must be checked by the user.

[Full template contract](TEMPLATE_COLLECTION.md).

## Round-trip import contract (MetaCanvas 0.1.1)

The editor exports its own `ccm.document.v1` state as JSON for an LLM. A later import accepts either a JSON document or an HTML MetaCanvas document containing a `<script id="ccm-data" type="application/json">` payload.

Import uses the *data only*. It never evaluates imported script or replaces the installed editor runtime, CSS or MPL notice. Before replacement it checks document schema, non-empty scenes, stable/unique scene, node and link IDs within their scope, and the validity of link `from`/`to` targets. It limits size and object count. The user confirms the replacement; **Undo** can restore the prior document. Invalid files leave the current document untouched.

The imported source is a new proposed model, **not verified truth**. Do not reuse private notes or secret data unless the operator intends them to remain in the working HTML. Public export removes private notes and library data, while keeping the MPL source notice. Source/content, preview, file download and actual recipient understanding/effects remain distinct.

## Studio 14 — interaction and saved UI state

The document's geometry and semantic references are unchanged by Flat mode. It is a **view preference**, retained in the embedded `state.ui.flatLayout` property; the normal reading area has a narrower maximum width, while Flat may span the available viewport and use two columns on desktop. Presentation mode uses a block canvas shell rather than an editor grid with a hidden rail; it preserves the slide's 16:9 scene.

Tools panel size is a persistent interface setting. Edge and corner resize handles must remain reachable even when the tool catalog scrolls. Save/export preserves these handles inside the exported source; they are moved to the document body at runtime for stable fixed positioning.

The compact editing toolbar applies to contextual editing and advanced properties. **OK** confirms pending text changes and closes; **Indietro/Avanti** navigate the existing undo/redo history rather than adding redundant checkpoints. Saved HTML keeps the toolbar dormant until editing is active. This is an interaction contract, not semantic validation of a user's edits.

**Suggested LLM request:** “Read the JSON document model rather than relying only on a screenshot. Summarize the relation between nodes and links, identify uncertainty, then propose a clearer structure for [audience/objective]. Preserve my original concepts and private notes in the working copy, distinguish your changes, return a complete editable HTML and summarize the differences.”

Do not break `from`/`to` IDs when reorganizing. The HTML carries the editor source and its MPL notice when exported; keep the license/copyright notice. Do not mistake downloaded/previewed files for verified external effects. No AI service is embedded in this file.
