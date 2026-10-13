> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Agents and subagents

Step Code delegates tasks to four built-in roles, supports custom agents defined in Markdown, and uses workflow to coordinate agents in parallel.

## Built-in agents

| Role | Responsibility | Tools |
| - | - | - |
| `general` | General implementation tasks | All tools |
| `explore` | Read-only repository exploration | `read_file`, `find_files`, `search_files`, `list_directory` |
| `review` | Correctness and regression review | Read-only tools and command execution |
| `planner` | Investigation and implementation planning | Read-only tools and command execution |

Subagents return results to the main agent rather than talking directly to the user. Roles with command execution can perform writes, subject to tool permissions.

## Custom agents

Use Markdown frontmatter for metadata and the body for system instructions:

```markdown theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
---
name: db-migrator
description: Design reversible database migrations and review migration scripts
tools: read_file, run_command, edit_file
---

Inspect existing migration conventions before planning. Every migration must include rollback steps.
Do not connect to production databases or run production migrations without explicit authorization.
```

| Item | Description |
| - | - |
| User directory | `~/.stepcode/agent/agents/*.md` |
| Project directory | `.stepcode/agents/` |
| Required fields | `name`, `description` |
| Optional fields | `tools`, `model` |
| Same-name precedence | Project overrides user; user overrides built-in |

`tools` accepts an array or comma-separated list. Include project roles explicitly with `agentScope: "both"` when calling the tool, and confirm when prompted.

See [Agent Skills](/docs/en/step-code/customization/skills) for defining specialized workflows.

See [Plugins](/docs/en/step-code/customization/plugins) for distributing agents through plugins.

## The subagent tool

### single, parallel, and chain

| Mode | Behavior |
| - | - |
| single | One role handles one task |
| parallel | Multiple tasks run concurrently |
| chain | Tasks run sequentially; `{previous}` references the prior result |

The task batch limit is 8, with execution concurrency of 4 by default. Dispatch follows the current approval policy. Subagents cannot recursively create subagents.

Authorize delegation in natural language:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Delegate two read-only tasks in parallel: one checks API error handling, the other checks test coverage. Return evidence and suggestions separately, then summarize them in the main agent. Do not modify files.
```

### Background lanes

`run_in_background: true` creates a background subagent task, called a lane, and immediately returns its ID / alias. Completion arrives as a notification. `agent_send` supports `reply` (queued or inserted immediately) and `stop`, addressed by `agent_id`, `alias`, `group`, or `all`.

Background tasks require the Step Code process to remain running.

## Workflow and ultraloop

Workflow executes JavaScript orchestration in a sandbox VM without network or filesystem access. Primitives include `phase()`, `parallel()`, `pipeline()`, `agent()`, and `iterate()`. Run records are stored in `.stepcode/workflows/runs/` and support resuming. Use `/workflows` to inspect saved workflows and recent runs.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
ultraloop Audit test coverage by module. Each subagent checks only its assigned directory and reports missing scenarios. The main agent deduplicates findings and proposes a testing plan.
```

Multi-agent calls require explicit authorization. This requirement is enforced through instructions; unauthorized calls are logged but not blocked at the execution layer. Include `ultraloop` or `ultracode`, or enable session-level authorization with `/ultraloop on` and disable it with `/ultraloop off`. Single-message authorization does not carry forward and is not inferred from task size.

`STEP_DISABLE_WORKFLOW=1` disables registration.

See [Common use cases](/docs/en/step-code/guides/use-cases) for examples of multi-agent tasks.

## Context isolation and safety

The sandbox VM restricts only the workflow orchestration script. Subtask processes remain subject to OS permissions.

* Subagents have independent context and token usage; the main agent primarily receives summaries.
* Subagents may share the main agent's working directory, so file changes affect the same working tree.
* Assign disjoint files for parallel writes, or explicitly arrange separate Git worktrees.
* Worktrees isolate working trees, not access to other directories, networks, or credentials.
* Review diffs and tests before integrating results. Do not clean up unmerged work blindly.

The default scale is medium, approximately up to 15 agents, unless explicitly expanded.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.