# omni-mode

A high-agency working discipline for coding agents, packaged as an Agent Skill.

**Status:** draft. Loadable and reviewable; not yet validated by a comparison run. See
[Verification status](#verification-status).

## What it does

When explicitly invoked, it applies four things:

- **Maximum autonomy inside the permissions the host already grants** — reversible, in-scope
  work proceeds without asking. Questions are batched, not serialized.
- **Scope-bound write access** — "review this" and "diagnose this" are read-only. Autonomy
  is about *how* you work, never about widening what was asked.
- **Risk-proportional verification** — done means you exercised the changed path. A rename
  needs a build; a payment path needs tests. Unverifiable work is reported as unverified.
- **Outcome-first replies** — result first, no filler, no activation banner.

It is a behavior overlay. It does **not** change the model, reasoning effort, permission
mode, sandbox, or tool availability, and it cannot bypass host approval prompts.

## Install

Copy the skill directory into a skills path your host scans:

```bash
git clone https://github.com/dongwookim-prog/omni-mode.git
cp -r omni-mode/skills/omni-mode ~/.gemini/skills/omni-mode
```

| Host | Path |
|---|---|
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` (user) · `.gemini/skills/` or `.agents/skills/` (workspace) |
| Claude Code | `~/.claude/skills/` (user) · `.claude/skills/` (project) |
| Other | wherever that host scans for `SKILL.md` |

Then in Gemini CLI: `/skills reload`, and confirm with `/skills list`.

Only `skills/omni-mode/` belongs in the skills path — do not copy the repo root (its
`README.md` and `.git` are not part of the skill).

## Activation

Agent Skills activate **semantically from the frontmatter `description`**, not from a slash
command. Ask for it in words:

```
omni 모드로 이 마이그레이션 처리해줘
use omni-mode for this refactor
```

To stop, say so ("omni 모드 꺼줘"). There is no `/omni-mode` command — this repo ships a
skill, not a custom command or extension. Building one would require a Gemini custom-command
TOML or an extension manifest, which is out of scope here.

The discipline is not guaranteed to survive compaction or a new session. Ask again when you
need it later.

## Provenance

Synthesized from three same-owner overlays (none carried a license file; this repo's own text
is MIT):

| Source | Repo | Commit | What was taken |
|---|---|---|---|
| apex-mode | [dongwookim-prog/apex-mode](https://github.com/dongwookim-prog/apex-mode) | `e71bc9c` | Identity/capability guards, self-contained subagent capsule, host-precedence, compaction caveat |
| fable-mode | [dongwookim-prog/fable-mode](https://github.com/dongwookim-prog/fable-mode) | `cab0325` | Outcome-first communication, finish-line rule, assumptions/evidence discipline |
| sol-mode | [dongwookim-prog/sol-mode](https://github.com/dongwookim-prog/sol-mode) | `feb0838` | Lean packaging, depth-matched-to-complexity, explicit-trigger-only |

Not inherited from any of them, added here: the scope→write-access matrix, the definition of
"failure", the risk-proportional verification rule, and the overlay precedence table.

## Verification status

What has been checked:

- Frontmatter parses under Gemini CLI's actual loader regex
  ([`skillLoader.ts`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/skillLoader.ts)
  `FRONTMATTER_REGEX`) — `evals/cases.yaml` case D1, runnable.

What has **not** been checked:

- Live discovery in a Gemini CLI session (D2–D4)
- Every behavior and safety case (B1–B8, S1–S4)
- Any before/after comparison against apex/fable/sol

Do not call this production-ready until `evals/cases.yaml` passes its thresholds. The
thresholds are in that file.

## Relationship to apex / fable / sol

Same genre — do not stack them. Prefer the host-native overlay (apex on Grok, fable on
Claude, sol on Codex); reach for omni-mode when you want one contract across hosts. If more
than one is invoked, the most recent wins, and precedence against host rules and project
files is spelled out in the skill itself.

## License

MIT — see [LICENSE](LICENSE).
