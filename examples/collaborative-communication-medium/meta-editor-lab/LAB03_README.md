# MetaEditor Lab 03 — gestures before themes

Date: 17 November 2026 · Status: autonomous neutral HTML example in K-UX-AI, not Studio 20/21 runtime or MAIOS.it deployment.

## Open the tool

[MetaEditor Lab 03](MetaEditor_Lab03_Elementi.html) is a single-file HTML editor evolved from Lab 02. The Themes tab is retained but the Elements tab is the ordinary entry.

- **Object first:** single-click selects; double-click on text, including a diagram node label, edits in place. A compact floating bar offers direct actions; a local object panel is placed above the document outline in the rail.
- **Structure:** explicit section selection and outline, move section up/down, duplicate, guarded delete, layout 1/2/3 columns, and insert another diagram+notes section non-destructively.
- **Elements:** insert by type at the selected point (not automatically a text block), duplicate, reorder, delete, move to another section without drag, insert above or below, convert title/text/card, align content, resize typography and span all grid columns. Drag remains optional.
- **Diagrams:** add/duplicate/delete nodes; edit text directly; shapes; link mode by clicking destination node; remove a specific link; move node via grip or keyboard; distribute nodes in rows to reduce overlap. Source data and links remain in the HTML model.
- **Keyboard:** Ctrl+D duplicate, Alt+Up/Down reorder, Delete remove, Ctrl+Z/Y undo/redo, Esc close, arrow keys to nudge selected nodes (Shift = larger increment). Text inputs keep normal keyboard behavior.

## Verification

Node --check of the final runtime; Chromium/Playwright via page.set_content. Paths exercised: section selection/layout/undo, direct element edit, duplication/reorder, align/full-width/insertion, section duplicate/delete, diagram node duplication/link/shape/edit/keyboard movement/distribution, visual non-overlap of five arranged nodes, change to D-ND theme, HTML export/clean reopen with exactly one runtime inspector/toolbar, 390px without page-wide overflow, conversion of element type, cross-section move, remove a link. No pageerror observed in exercised paths. Export removes transient selection/picker/inspector from the serialized document and reconstructs UI on reopen.

**Limits:** file:// navigation blocked with ERR_BLOCKED_BY_ADMINISTRATOR by the available test browser; no claim of test on operator's Chrome Windows. No arbitrary web page import, live CMS editor, full slide system, multi-selection/grouping or completed user usability evaluation. Demo data is synthetic, and production sites are unchanged.

## Learning returned to the owner competence

1. **Function availability != easy interaction.** R4 tested an inspector input, not the actual gesture of editing the label. Lab 03 keeps the gesture in the element and moves the local inspector in front of structural management when the element is selected.
2. **Selection has levels:** section, element, diagram node. A structure list lets the operator reach the intended object; its controls must not compete with node controls.
3. **Each action has an effect corresponding to its verb:** change the selected layout vs add a new section; move vs duplicate; link two nodes vs add another linked node. Deletion of populated sections asks for confirmation and can be undone.
4. **Rendered geometry is an additional test:** five nodes distributed on one horizontal line passed functional assertions but visually overlapped on desktop/mobile. Re-layout uses multiple rows; the browser test now measures node rectangles to detect collisions.
5. **Round-trip matters:** the HTML source of the editable artifact retains the document/theme model, while temporary UI overlays are reconstructed and not serialized as active duplicate state.

Owner skill: [MetaEditor Evolution](../../../competences/ux-ai/collaborative-communication-medium/meta-editor/SKILL.md). D-ND Design governs perceptual quality; CCM governs the broader medium and collaboration. Site content, public release and Codex checkout remain separate effects.
