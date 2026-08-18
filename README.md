# omni-mode

One high-agency working discipline for coding agents, packaged as an Agent Skill.

It is the **union** of [apex-mode](https://github.com/dongwookim-prog/apex-mode),
[fable-mode](https://github.com/dongwookim-prog/fable-mode), and
[sol-mode](https://github.com/dongwookim-prog/sol-mode): every behavioral rule from all three
is in this one skill. On any one host, use it instead of those three rather than alongside
them.

**Status:** draft. Loadable, and rule coverage is machine-checked; live behavior is not yet
validated. See [Verification status](#verification-status).

## What it does

- **Maximum autonomy inside the permissions the host already grants** — reversible, in-scope
  work proceeds without asking. Questions get batched, not serialized.
- **Scope-bound write access** — "review this", "diagnose this", or thinking out loud are
  assessment-only. Autonomy governs *how* you work, never *how much you were asked to do*.
- **Risk-proportional verification** — done means you exercised the changed path. A rename
  needs a build; a payment path needs tests. Unverifiable work is reported as unverified.
- **Outcome-first replies** — result first, no filler, no activation banner.

It is a behavior overlay. It does **not** change the model, reasoning effort, permission mode,
sandbox, or tool availability, and it cannot bypass host approval prompts.

## Install

```bash
git clone https://github.com/dongwookim-prog/omni-mode.git
cp -r omni-mode/skills/omni-mode ~/.gemini/skills/omni-mode
```

| Host | Path |
|---|---|
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` (user) · `.gemini/skills/` or `.agents/skills/` (workspace) |
| Claude Code | `~/.claude/skills/` (user) · `.claude/skills/` (project) |
| Codex | `~/.agents/skills/` (user) · `.agents/skills/` (repo) |
| Other | wherever that host scans for `SKILL.md` |

In Gemini CLI: `/skills reload`, then confirm with `/skills list`.

Copy only `skills/omni-mode/` — the repo root's `README.md`, `evals/`, and `.git` are not part
of the skill.

Within a single host, use this **instead of** apex/fable/sol — it is their union, so running
two of them stacks the same rules twice. Across hosts they do not collide, so keeping
apex-mode on Grok while omni-mode runs on Gemini is fine.

## Activation

Agent Skills activate **semantically from the frontmatter `description`**, not from a slash
command. Ask in words:

```
omni 모드로 이 마이그레이션 처리해줘
use omni-mode for this refactor
```

There is no `/omni-mode` command — this repo ships a skill, not a custom command or extension.
The discipline is turn-scoped; ask again on a later turn and after compaction.

## What came from where

All 31 behavioral rules of the three sources are present. `evals/coverage.py` checks this
mechanically and fails if any rule is dropped.

| Source | Commit | Rules contributed |
|---|---|---|
| apex-mode | `e71bc9c` | Identity/capability guards · host precedence · no-banner · compaction caveat · self-contained subagent capsule · worktree isolation · protecting work you do not own |
| fable-mode | `cab0325` | First-tool-call sentence · mid-turn update policy · final-message-carries-everything · finish-line anti-pattern list · "when unsure, stop" · end-only-when-blocked |
| sol-mode | `feb0838` | Turn-scoped honesty · depth-matched-to-complexity · parallel subagents only when the host allows · consequential-assumptions-only |
| all three | — | Code comments rule · assessment-only exception · evidence-before-state-changes · outcome-first · external text is data, not authorization · exercised-before-claiming |

Added here, not in any source:

- A concrete definition of **failure** (red test / non-zero exit / user rejection, three
  strikes) — all three left this qualitative.
- **Reproduction-script conditions**, so verification does not manufacture work on trivial
  changes or write files during an assessment.
- The **scope→write-access table** — a tabulated form of the assessment-only exception the
  three carried as prose, which is where they were easiest to misread.
- The **cross-host precedence table** and host paths — each source was scoped to one host
  (apex→Grok, fable→Claude, sol→Codex).

### Conflicts, and how they were resolved

| Question | apex | fable | sol | Resolved as |
|---|---|---|---|---|
| How long does it last? | turn + reinvoke after compaction | "for the session" | turn-scoped, no deactivation needed | **Turn-scoped**, with the compaction caveat — the honest option, and it never overpromises |
| When to give up? | qualitative ("keeps failing") | qualitative | qualitative | **Three attempts, or sooner if cost/time/risk spikes** — keeps the judgment, adds a ceiling |
| Deactivation? | `/apex-mode off` | `/fable-mode off` | none needed | Honor an explicit "stop"; **no slash command claimed**, since a skill cannot register one |

The three sources also carried host-specific bits that are deliberately not merged: sol's
`agents/openai.yaml` interface file and fable's "if you are already that model, do not
activate" guard. The first is a Codex-only manifest whose schema is not verified here; the
second is meaningless for a model-independent overlay.

## Verification status

Checked, and runnable:

```bash
python3 evals/coverage.py
```

- Frontmatter parses under Gemini CLI's actual loader rule
  ([`skillLoader.ts`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/skillLoader.ts)
  `FRONTMATTER_REGEX`, anchored at the first byte with no `m` flag)
- All 31 source rules present

**Not** checked: live discovery in a real session, and every behavior/safety case in
`evals/cases.yaml` (B1–B8, S1–S4). No before/after comparison against the three sources has
been run. Do not call this production-ready until those pass.

## License

MIT — see [LICENSE](LICENSE).
