# AI Collaboration Studio — public preview

An **editable standalone HTML** for organizing ideas, diagrams and presentations, exchanging the same working file with an LLM, and presenting results to people.

**Quick start:** open `AI_Collaboration_Studio.html` in an up-to-date browser, edit one of four starter scenes or start blank, save HTML, attach the saved file to your AI chat and ask for a structured revision, then reopen the revised HTML. Use **Presenta** for human presentations. The editor UI is currently Italian. It includes no embedded AI service, server or live synchronization.

The document model resides in `<script id="ccm-data" type="application/json">` under schema `ccm.document.v1`. For meaningful AI collaboration, preserve node IDs and link referents and distinguish the operator's content from proposed additions. The public export removes private notes and library data, but an HTML file remains inspectable.

## License and ownership

**Mozilla Public License 2.0 (MPL-2.0)**, scoped to the files **in this tool directory only**. Everyone may use, modify, distribute and commercialize the tool under the MPL. Distributed modifications of covered files must make their source available under the MPL. Original software contributions remain **Copyright (c) 2026 Graziano Guiducci**; contributors retain rights in their own additions. The license does not grant trademark or logo rights.

[Full license](LICENSE) · [Document contract](DOCUMENT_CONTRACT.md) · [Italian instructions](README.it.md).

This license does not change the licensing of the K-UX-AI kernel, competences or other repository examples. This preview is not a runtime integration or a live MAIOS.it release.
