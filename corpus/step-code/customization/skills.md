> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Agent Skills

Package specialized workflows, scripts, and references as a Skill for on-demand model reading or explicit slash-command invocation.

<a id="what-are-skills" />

## Skill structure

A Skill uses `SKILL.md` as its entry point and follows the [Agent Skills](https://agentskills.io/) format. Startup primarily loads names and descriptions; the model reads full instructions when relevant, avoiding unnecessary context usage.

## Creating a Skill

### Directory structure

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
api-review/
├── SKILL.md
├── scripts/
│   └── check.sh
└── references/
    └── checklist.md
```

Use relative paths in `SKILL.md` to reference package files. `scripts/` and `references/` are optional.

### Frontmatter fields

| Field | Requirement | Description |
| - | - | - |
| `name` | Required | Up to 64 characters: lowercase letters, digits, hyphens; need not match the directory name |
| `description` | Required | Up to 1,024 characters describing purpose and when to use it |
| `license` | Optional | License |
| `compatibility` | Optional | Environment and dependency requirements |
| `metadata` | Optional | Additional metadata |
| `allowed-tools` | Optional | Space-separated tools; experimental |
| `disable-model-invocation` | Optional | `true` hides it from automatic model discovery and leaves manual invocation |

### Validation rules

Step Code issues warnings for uppercase letters, leading or trailing hyphens, consecutive hyphens, and overlong names, but still loads the Skill. Missing `description` prevents loading. For duplicate names, Step Code keeps the first Skill and issues a warning. Unknown frontmatter fields are ignored.

Fix naming and length issues for cross-tool reuse. A Skill's tool declaration does not replace Step Code permissions.

## Locations

Priority from highest to lowest:

| Scope | Location |
| - | - |
| Project | `.stepcode/skills/` and project-scope `.agents/skills/`; requires trust |
| User | `~/.stepcode/agent/skills/`, `~/.agents/skills/` |
| Package | Declared Skills directory in a resource package |
| Launch option | `--skill <path>`, repeatable, still loaded with `--no-skills` |

Project `.agents/skills/` discovery walks upward to the Git root. Add extra directories with the `skills` array in `config.toml`.

See [Plugins](/docs/en/step-code/customization/plugins) for installing and distributing resource packages.

## Invocation

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/skill:api-review Check this interface change
```

`enableSkillCommands` is enabled by default and registers `/skill:<name>`. Arguments are appended to the Skill content as `User: <arguments>`.

The model may use `description` to decide when to read a Skill, but automatic selection is not guaranteed. Use the slash command when you need an explicit workflow. `disable-model-invocation: true` disables automatic discovery.

<a id="reusing-skills-from-other-harnesses" />

## Reusing Skills from other tools

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
skills = ["~/.claude/skills", "~/.codex/skills"]
```

Add existing directories without copying files. Review referenced commands, paths, model capabilities, and tool names for assumptions specific to another tool.

See [Agents and subagents](/docs/en/step-code/customization/agents) for defining and invoking subagents.

## Complete example

Save as `~/.stepcode/agent/skills/api-review/SKILL.md`:

```markdown theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
---
name: api-review
description: Review REST API compatibility and documentation completeness. Use when tasks involve routes, request or response types, or OpenAPI changes.
---

# API change review

1. Use git diff to find the affected routes and types.
2. Check breaking changes, error codes, authentication requirements, and examples.
3. Use references/checklist.md to report review findings.
```

Write the project checklist in `references/checklist.md` under the same Skill directory. Run `/reload`, then `/skill:api-review`. Skills with scripts can execute local commands; load only trusted sources.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.