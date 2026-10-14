# K-UX-AI

**A competence that an LLM uses to make work understandable and actionable,
build its interface code and learn through its use.**

K-UX-AI is a public competence kernel that can be composed with agentic systems
and domain kernels. Its knowledge connects intent, sources, events, focus,
expression and human intervention. It can form websites, concept maps,
interactive environments and work panels through the receiving system's means.

The [Living Web Manifesto](MANIFESTO.md) preserves its horizon: **from the Web
we consult to the Web we inhabit**. The [kernel](KERNEL.md) carries the operating
relation, the [competence](competences/ux-ai/COMPETENCE.md) its method and the
[guide](competences/ux-ai/GUIDE.md) its reasons and practical knowledge.
Kernel Nautico applies this competence to work in a shipyard.

[Italiano](README.it.md) · [English workspace](examples/public-griglia/demo/)
· [Interfaccia italiana](examples/public-griglia/demo/it/)

## Use it in your system

Make the repository accessible or provide the relevant documents to the model.
Start with [BOOT.md](BOOT.md) and the [LLM entry](adapters/llm/ENTRY.md), together
with the sources of the work. A core such as MPK can compose K-UX-AI among its
competences; another harness can use the same methods with its own tools and
controllers.

The competence understands what needs to become possible, composes useful
capabilities and constructs an original form. Movement, text, space, images
and other channels participate as the work requires. Their expression and
consequences can change understanding and code. The guide retains what changes
the next use.

The [receiving-environment guide](docs/receiving-environment.md) connects method
with available means. The domain retains its data, sources and the meaning of
effects; the receiving system keeps its own context and learning.

## Presentation and first use

The [workspace](examples/public-griglia/demo/) introduces K-UX-AI and lets you
try its functions. Introduction, Composition, Tools, Interaction and Learning
are its service topics. Overview prepares activities; Work in progress opens
complementary cards and preserves focus and drafts as what needs to be seen changes.

Cards can present and guide, receive a contribution, check, explore, design,
organise, communicate, resume, experiment, monitor illustrative events, compare
texts and support dialogue. The hosting kernel supplies meaning and sources
through its profile. Kernel Nautico connects owner requirements, design,
construction and vessel life using the sector's terminology.

Serve the repository with a static server:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/examples/public-griglia/demo/`. English is the default;
use the Italiano link for the Italian version. The workspace and cards work
locally. Explicitly submitted questions use the public MAIOS service on a
configured site; a simple static server does not provide that service, and the
UI reports the unavailable connection. Other drafts remain local. Dialogues
and proposals can be exported on request; transfer to the receiving kernel
continues the work and its learning.

The [card guide](docs/public-griglia.md) explains preparation, activities,
dialogue and continuation. [Source documentation](docs/source-and-evolution.md)
retains attribution, construction and references for developers and integrators.
The `0.2.0-alpha.3` source distribution includes the competence kernel,
JavaScript modules and this public interface. The competence can construct
other forms for other situations.

## Connect the runtime

```js
import { createMedium } from './src/medium.js';

const ui = createMedium({
  state: initialPublicState,
  render: state => renderYourInterface(state),
  onAction: action => yourKernel.receiveHumanAction(action),
});

ui.receive({ id: 'event-001', state: nextPublicState });
ui.dispatch({ type: 'compare', objectId: 'your-object' });
ui.observe(record => yourDevelopmentObserver(record));
```

The controller determines the result of the gesture and returns state. Domain
schema, renderer and transport are composed for the receiving environment.
Run `npm test` with Node.js 20+ for the executable contract.

- [JavaScript interface](docs/interface.md)
- [Adaptation and MessagePort](docs/receiving-environment.md)
- [Continuity and learning](docs/continuity.md)
- [Distribution](docs/distribution.md)
- [Sources and evolution](docs/source-and-evolution.md)

The producer continues formation in its own source and transfers selected
updates to this product. Public knowledge supports understanding, construction
and continuation in the adopting environment. Source version: **0.2.0-alpha.3**.
