# CURRENT — K-UX-AI UI source cabinet and Nautico v3 laboratory

**8 October 2026 · private branch candidate · public product version remains `0.1.0-alpha.1`**

```text
owner: GrazianoGuiducci/k-ux-ai
branch: work/ux-ai-ui-library-20261008
starting_main: 68cb9c82631aae2d1d5ad4fa22cd255d67e5f57b
semantic_owner: Meta_Skill / ux-ai-kernel-design
design_owner: D-ND Design Kernel / Agentic UX Seed
first_domain: Kernel Nautico
receiving_site: MAIOS (separately owned, not modified)
status: CANDIDATE_SOURCE_CABINET + TWO_STANDALONE_LABS
effect: no release, merge, installation or public site update
```

## Begin here

1. Read the [K-UX-AI Kernel](../../KERNEL.md) and the published [medium contract](../../docs/interface.md).
2. Read [the module catalog](../../ui-library/catalog.v0.1.json): **20 exact source references across five owners, nine behavior families**.
3. Read [the complete surface composition contract](OPERATING_CONTRACT.md), then the [source-by-source adoption map](SOURCE_ADOPTION_20261008.md).
4. Open [Griglia del fare v3](../../labs/nautico-ui-v3/01-griglia-del-fare.html) and [Campo a quattro fonti v3](../../labs/nautico-ui-v3/02-campo-quattro-fonti.html) as standalone **synthetic probes**. Read their [receipt](../../labs/nautico-ui-v3/EVIDENCE.json) before making claims about what is tested.
5. Only when a real Nautico/coder integration is selected, resolve the **current** owner-native state and source SHA again. These commits are readback coordinates, not permanent freshness claims.

## What moved

The operator requested that the behavior of the Lab D-ND HTML/JavaScript assistant and adjacent original UI modules be made reachable within K-UX-AI, **before any new HTML generation or Codex site integration**. The need is to recover full behavior (drag, resize, inverse motion, two-pane modals, mobile, manager, guided forms, scroll/focus, state and effect boundaries), not to import its look.

Lab D-ND original source:

- `lab-d-nd-site@bc92ae3f90786ceaaf84d6042aef0aec876a50cb/assets/js/domus-widget.js` (JS, 6k+ lines, host-specific backend and admin logic).

Related original carriers:

- `d-nd_com@8ad776c76f735fb36c87df2a6f73b082c2e4813d`: THIA React, intake, SITEMAN Studio and Dashboard.
- `d-nd-ux-ai-seed@972349d5c38a851f40ff6d8c87f541cd0da70f9e`: THIA/AgenticChatSystem, Shell3Col, SplitPanel, MegaMenu, HoverPopover, primitives, source-parity and design contracts.
- `MAIOS_CLIENT_SETUP@21303ec074bd7bf395f4150ebc11764e0c2d1931`: context-aware guided form, chat/form pairing, animated focus/scroll and dependency invalidation.
- `kernel-nautico@82896de01829752614d04cfa6e3ffacbd9544a0a`: first domain object, actual public views and separate owner-native case state.

**No upstream runtime or full page was copied.** The branch contains two original self-contained v3 demo HTML files produced in this conversation and documents source references to the implementation owners. The Lab source's auth, provider, server API and storage must not become default K-UX-AI behavior.

## Sufficient observed distinctions

- A single entity can appear as **avatar, concise card, floating window, dock, split plane or full-page**, with its semantic/domain identity unchanged.
- The **canvas wins vertical space** over large titles, duplicated statuses and toolbars; secondary commands can remain available in a compact megamenu.
- Manual window geometry is distinct from system-generated arrangements and must be recoverable, including mobile → desktop restoration.
- A module may need an **internal responsive** mode according to its own width, not just the viewport width.
- A chat/form workspace can be side-by-side in a wide frame and one-pane-at-a-time on compact frames; retaining unsent drafts is necessary.
- Movement should communicate origin/destination and causal change, not simply delay the UI. Interruptions, ESC, focus and reduced-motion parity are part of the action contract.
- Tool-specific backend authority and the host's data/credentials do not become transferable when its visual component is reused.
- Notifications are owner-source events, not new UI renderings or arbitrary decorative pulses.

## Evidence and absence

The historical local laboratory run records **63/63 correlated Playwright assertions**, with zero JS page errors, on v3 standalone HTML with synthetic state. The files are now in the branch, but **that browser suite has not been rerun against the GitHub copy in this movement**.

The product's `createMedium()` code is unchanged. No chat transport, real THIA model, authenticated manager, enterprise/vessel data, domain effects, simultaneous writable nautical panes, independent human comprehension validation or deployed Site is produced by this cabinet.

The license declared by the upstream Agentic UX Seed package is **PolyForm-Noncommercial-1.0.0**. If the selected MAIOS product requires a different use, qualify the appropriate grant with the source owner. Mere common authorship or catalog entry is not a distribution right.

## Next material movement

From the user's review of v3 plus the source contracts, choose the smallest whole UI module that makes the Nautico work materially more understandable and operable. Adapt a **real source-owned event** through `createMedium()` into the selected module. Compare this with the historical synthetic example; test keyboard, touch, geometry, persistence, responsive, resize, host effects and actual operator comprehension.

Only after a selected candidate works in its host should Codex Site receive an integration packet. Do not publish/update MAIOS or mutate Kernel Nautico from this source cabinet by inertia.

## Status of adjacent owners

- Meta_Skill / UX-AI: kernel–human comprehensibility and code-medium competence, can receive later source-bound learning.
- Design/Agentic UX Seed: component and perceptual construction owner, not overwritten.
- Nautico: case, product, events and domain meaning owner.
- MAIOS Site/Codex: actual page host, agent providers and public integration authority.

Current result: **source availability and a candidate kernel-product cabinet**, not completion of the final UI.
