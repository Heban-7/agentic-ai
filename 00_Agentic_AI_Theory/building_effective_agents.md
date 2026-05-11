# Building Effective Agents - Personal Study Notes

> Source: [Anthropic - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

---

## Key Takeaway (TL;DR)

The most successful agent implementations are **not** built with complex frameworks. They use **simple, composable patterns**. Start simple, measure, and only add complexity when it demonstrably improves outcomes.

---

## 1. What Are Agents?

The term "agent" is overloaded in the AI space. Anthropic makes a clear architectural distinction between two types of agentic systems:

| Type          | Description                                                    | Control Flow                      |
| ------------- | -------------------------------------------------------------- | --------------------------------- |
| **Workflows** | LLMs + tools orchestrated through **predefined code paths**    | Developer controls the sequence   |
| **Agents**    | LLMs **dynamically direct** their own processes and tool usage | The model decides what to do next |

**My understanding:** Think of workflows as a recipe the developer writes (step 1, step 2, step 3...), while agents are like giving the LLM a goal and letting it figure out the steps on its own.

---

## 2. When to Use (and NOT Use) Agents

This is a critical decision-making framework:

- **Default:** Start with the simplest solution. A single optimized LLM call with good retrieval and in-context examples is often enough.
- **Workflows:** Use when you need predictability and consistency for well-defined tasks.
- **Agents:** Use when you need flexibility and model-driven decision-making at scale.

**Important tradeoff:** Agentic systems trade **latency and cost** for **better task performance**. Always ask: "Is this tradeoff worth it for my use case?"

---

## 3. Frameworks - Use with Caution

Available frameworks include Claude Agent SDK, Strands Agents SDK (AWS), Rivet, and Vellum.

**Anthropic's advice on frameworks:**

- They simplify boilerplate (calling LLMs, parsing tools, chaining calls).
- **BUT** they add abstraction layers that obscure what's happening underneath.
- They tempt you to over-engineer when a simpler setup would work.

**Best practice:** Start by using LLM APIs directly. Many patterns need only a few lines of code. If you use a framework, make sure you understand what it does under the hood.

---

## 4. The Building Blocks (From Simple to Complex)

### 4.1 The Augmented LLM (Foundation)

This is the fundamental building block. An LLM enhanced with:

- **Retrieval** - ability to search and fetch relevant information
- **Tools** - ability to call external functions/APIs
- **Memory** - ability to retain and recall information across interactions

Modern models can actively use these capabilities: generating search queries, selecting tools, deciding what to remember.

**Key insight:** The Model Context Protocol (MCP) is Anthropic's standardized way to integrate third-party tools. It provides a clean client interface for connecting to an ecosystem of tools.

---

### 4.2 Workflow: Prompt Chaining

**What it is:** Decompose a task into a sequence of steps. Each LLM call processes the output of the previous one. You can insert programmatic "gates" (checks) between steps to verify the process is on track.

**Flow:** `Input → LLM Call 1 → [Gate/Check] → LLM Call 2 → [Gate/Check] → Output`

**When to use:** When a task can be cleanly broken into fixed subtasks. You're trading latency for accuracy by making each individual LLM call simpler.

**Examples:**

- Generate marketing copy → Translate to another language
- Write a document outline → Verify outline meets criteria → Write the full document

---

### 4.3 Workflow: Routing

**What it is:** Classify an input first, then direct it to a specialized handler. This enables separation of concerns - each downstream path has its own optimized prompt/tools.

**Flow:** `Input → Classifier → Route A / Route B / Route C`

**When to use:** When you have distinct categories that benefit from specialized handling, and when classification can be done accurately.

**Examples:**

- Customer service: route general questions vs. refund requests vs. technical support to different pipelines
- Model selection: route easy questions to cheaper models (Haiku) and hard questions to capable models (Sonnet)

**Why it matters:** Without routing, optimizing for one type of input can hurt performance on other types.

---

### 4.4 Workflow: Parallelization

**What it is:** Run multiple LLM calls simultaneously and aggregate results. Two flavors:

1. **Sectioning** - Break task into independent subtasks, run in parallel
2. **Voting** - Run the same task multiple times to get diverse outputs for higher confidence

**When to use:** When subtasks are independent (speed gain), or when multiple perspectives improve confidence.

**Examples:**

- **Sectioning:** One model handles user queries while another screens for inappropriate content (guardrails). Separating these performs better than one model doing both.
- **Voting:** Multiple prompts review code for vulnerabilities - flag if any find a problem.

---

### 4.5 Workflow: Orchestrator-Workers

**What it is:** A central "orchestrator" LLM dynamically breaks down a task, delegates subtasks to "worker" LLMs, then synthesizes their results.

**Flow:** `Input → Orchestrator → [Worker 1, Worker 2, ... Worker N] → Orchestrator → Output`

**Key difference from Parallelization:** The subtasks are NOT pre-defined. The orchestrator decides what workers are needed based on the specific input. This makes it flexible for unpredictable tasks.

**When to use:** Complex tasks where you can't predict the number or nature of subtasks in advance.

**Examples:**

- Coding tools that modify multiple files (which files and what changes depend on the task)
- Research tasks gathering info from multiple sources

---

### 4.6 Workflow: Evaluator-Optimizer

**What it is:** One LLM generates a response, another LLM evaluates it and gives feedback, and this loops until quality is satisfactory.

**Flow:** `Generator → Output → Evaluator → Feedback → Generator → Improved Output → ... (loop)`

**When to use:** When you have clear evaluation criteria AND iterative refinement adds measurable value. Two signs of good fit:

1. A human could articulate feedback to improve the response
2. An LLM can provide that same quality of feedback

**Analogy:** This is like a writer doing multiple drafts with an editor providing feedback each round.

**Examples:**

- Literary translation (evaluator catches nuances missed initially)
- Complex search tasks (evaluator decides if more searching is needed)

---

### 4.7 Autonomous Agents

**What it is:** The most complex pattern. LLMs operate in a loop, using tools based on environmental feedback, with minimal human intervention. They plan, execute, observe results, and adjust.

**Key characteristics:**

- Start from a human command or discussion
- Plan and operate independently
- Get "ground truth" from the environment at each step (tool results, code execution output)
- Can pause for human feedback at checkpoints
- Have stopping conditions (max iterations) to maintain control

**When to use:** Open-ended problems where you can't predict the number of steps or hardcode a fixed path. Requires trust in the model's decision-making.

**Tradeoffs:**

- Higher costs (many LLM calls)
- Potential for compounding errors
- Need extensive testing in sandboxed environments
- Require appropriate guardrails

**Examples:**

- Coding agents solving SWE-bench tasks (editing many files based on a description)
- Computer use agents (Claude controlling a computer to accomplish tasks)

---

## 5. Core Principles for Agent Design

Three principles to follow when implementing agents:

1. **Simplicity** - Keep the agent's design as simple as possible
2. **Transparency** - Explicitly show the agent's planning steps (make reasoning visible)
3. **Careful ACI Design** - Invest heavily in tool documentation and testing (Agent-Computer Interface)

---

## 6. Agents in Practice - Real-World Applications

### Customer Support

A natural fit because:

- Conversations + external actions (refunds, ticket updates)
- Tools pull customer data, order history, knowledge base
- Clear success metrics (resolution rate)
- Some companies use usage-based pricing (charge only for successful resolutions)

### Coding Agents

Particularly effective because:

- Solutions are verifiable via automated tests
- Agents can iterate using test results as feedback
- Problem space is well-defined and structured
- Quality is objectively measurable

---

## 7. Prompt Engineering Your Tools (Important!)

**Key insight from Anthropic:** They spent MORE time optimizing tools than the overall prompt when building their SWE-bench agent.

### Tool Format Guidelines:

- Give the model enough tokens to "think" before writing
- Keep formats close to what the model has seen in training data (internet text)
- Avoid formatting overhead (don't require counting lines, escaping strings, etc.)

### Agent-Computer Interface (ACI) Design:

- **Empathize with the model** - If a tool is confusing for you, it's confusing for the model
- **Name things clearly** - Good parameter names and descriptions matter (like writing docstrings for a junior dev)
- **Test extensively** - Run many inputs, observe mistakes, iterate
- **Poka-yoke (error-proof)** - Design tool arguments so mistakes are hard to make

**Real example:** Anthropic found their agent made errors with relative file paths. Fix: require absolute file paths always. Result: flawless usage.

---

## My Key Learnings Summary

1. **Simplicity wins** - Don't reach for agents when a well-crafted prompt will do
2. **Composable patterns** - These patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, agents) can be mixed and matched
3. **Tools are critical** - The quality of tool definitions matters more than most people think
4. **Ground truth matters** - Agents need real feedback from the environment, not just LLM-generated assumptions
5. **Human oversight** - Even autonomous agents should have checkpoints and guardrails
6. **Measure everything** - Only add complexity when measurements show it helps
