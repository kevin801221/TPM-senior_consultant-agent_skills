![AI Thinking OS: frame problems, challenge proposals, design validation](assets/img/01-hero.png)

# AI Thinking OS

**56 thinking techniques for AI consultants and product managers who need to make a decision.**

Use an AI agent to frame a vague request, challenge a proposal, organize ideas, or design a validation experiment. The skill selects a relevant technique, separates assumptions from evidence, and stops when the requested work is done.

[繁體中文](README.md) · [Technique index](references/routing.md) · [Worked example](examples/ai-consulting.md)

The technique library and worked examples are currently in Traditional Chinese. This file is an English introduction.

## Start with one decision

Download the repository and keep `SKILL.md` together with `references/`. In an agent that can read local files, use the actual path to the skill:

```text
Read ./ai-thinking-os/SKILL.md and use the pm-thinking skill.

Decision: Should we invest in a customer-support AI pilot?
Known: Agents frequently search product documentation. We have no timing baseline yet.
Constraints: Two weeks, two engineers, no production integration.

Choose one useful technique. Separate facts, inferences, and assumptions.
Give me a concrete next step. Respond in English.
```

If your agent is already at the repository root, use `./SKILL.md`. In a chat tool, paste the skill instructions and the selected technique alongside your context.

## Choose your entry point

| Situation | Technique | Useful output |
| --- | --- | --- |
| A client asks for “AI transformation” | #44 Problem slicing | A bounded problem to investigate |
| A proposal needs scrutiny | #31 Executive critique | Simulated objections and evidence gaps |
| An agent workflow may fail | #30 Risk review | Failure causes, mitigations, residual risks |
| A workshop produced too many ideas | #21 Idea clustering | Groups with traceable source IDs |
| A demo needs a business decision | #37 Validation test | Baseline, experiment, decision conditions |
| Product value is unclear | #33 Future press release | A clearly labeled future scenario |

<br>

![AI Thinking OS Method Map: 56 thinking techniques across 6 categories](assets/img/04-method-map.png)

## How it works

The agent reads [SKILL.md](SKILL.md), selects a method through the [routing guide](references/routing.md) when needed, and loads only the selected technique. Additional methods are used when an unresolved question warrants them. All 56 techniques are optional tools, not a mandatory sequence.

Simulated stakeholder views are not interviews. A future press release is not demand validation. Market and competitor claims require actual sources; the library does not include a live search service.

<br>

![Skill Workflow: select technique by decision, complete when sufficient](assets/img/05-skill-flow.png)

## Contribute

Share a concrete decision, the technique you used, and what remained unclear. Remove confidential information before contributing. See [contribution guidance](CONTRIBUTING.md) and [content attribution and licensing status](ATTRIBUTION.md).
