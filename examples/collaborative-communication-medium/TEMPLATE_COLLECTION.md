# MetaCanvas template collection contract — v1

**Format:** UTF-8 JSON, schema `metacanvas.templates.v1`. Its `templates[]` contain `id`, human-readable `name`, and a portable `scene` that follows the scene shape of `ccm.document.v1`.

```json
{
  "schema": "metacanvas.templates.v1",
  "version": 1,
  "templates": [
    {
      "id": "tpl-example",
      "name": "Flusso di lavoro",
      "scene": {
        "id": "scene-example",
        "title": "Flusso di lavoro",
        "notes": "",
        "elements": [
          {"id": "node-a", "type": "card", "text": "Input", "x": 80, "y": 230, "w": 250, "h": 120}
        ],
        "links": []
      }
    }
  ]
}
```

**Use:** inside a standalone document, personal templates are stored under `savedTemplates[]`. They persist when the working HTML is saved. The **public HTML** deliberately removes `savedTemplates[]` and the generated personal-template list. An exported collection can be imported into another editor.

**Insert:** `replace` replaces the active scene after confirmation, `above` inserts immediately before, and `below` immediately after. An entire multi-slide route is one undoable action. Each instantiation gives the slide, nodes and connections **new IDs**, updating connection targets and section `containerId` references so copied relationships do not collide with existing work.

**Data boundaries:** speaker notes, `note` elements and elements marked `private:true` are excluded from a saved template; links referencing such elements are excluded too. Other text, details and incorporated data images can still contain material supplied by the author; **review before export**. Packs are JSON data only, never executable HTML. Import checks schema, unique IDs, link references and image sources, with size/quantity caps (30 templates; import pack max 900 KB). External image URLs in imported packs are rejected.

**License:** the *editor code* remains MPL-2.0; source notices are carried by its exported HTML. This format does not claim authorship or assign rights over the user's original slide content. The licence's treatment of modifications is separate from whatever rights may apply to material included in a template.

**Limits:** import/export transfers templates, not a sync service or cross-document version merge. The in-browser Undo history is not persisted into the exported HTML. An export request does not establish receipt by another person or AI.
