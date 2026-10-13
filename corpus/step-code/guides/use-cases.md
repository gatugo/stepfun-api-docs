> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Common use cases

## Understanding an unfamiliar project

Start with read-only investigation before deciding what to change. To restrict tool operations, choose Read Only in `/permissions`.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
I just joined this repository. Inspect the entry points and build scripts, then create a newcomer guide organized by startup flow, core modules, and external dependencies. Do not change files yet.
```

After reviewing the findings, use `/init` to capture project conventions in `AGENTS.md`.

See [Migrating from other agents](/docs/en/step-code/guides/migration) for reusing project instructions from other tools.

## Implementing a feature

Provide requirements and acceptance criteria together. Plan first when changes span modules.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Add a shipping-status filter dropdown to the order list. Reuse the existing FilterBar, synchronize the URL query, and keep the mobile layout intact. List the files and implementation order first; wait for my approval before implementing.
```

## Fixing bugs

Include symptoms, reproduction conditions, expected behavior, and relevant files. Attach screenshots or use `!` to add diagnostic command output to context.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
The shopping cart total is occasionally one cent short. The calculation is in src/cart/total.ts. List every rounding path, build a reproducer, and confirm the root cause before making the smallest fix and adding regression tests.
```

## Tests and refactoring

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Add empty-value, month-end, and cross-time-zone tests for the exports in src/utils/date.ts. Preserve behavior first, then extract repeated formatting logic into a private helper. Run the tests and summarize the changes.
```

Use `/fork` to separate conversation experiments. Code changes still share the working directory; use a Git worktree when file isolation is needed.

## Delegating long tasks

Use `/goal` for hours-long work. Step Code continues after you set the goal; check progress with `/goal status`.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/goal Migrate all tests in this repository to vitest and keep them passing. Work module by module, running the full test suite after each module before moving on.
```

Use `/goal pause` to pause and `/goal resume` to continue. Keep the process and network available. See [Goal mode](/docs/en/step-code/guides/interaction#goal-mode).

Ask the model to create a cron schedule for recurring work, such as dependency security checks, and manage it with `/cron`. Scheduled tasks require the Step Code process to remain running.

## Parallel agents

Use workflow for batches of similar tasks, such as audits or comparing alternatives. Explicitly authorize it with `ultraloop` or `ultracode`; task size alone does not enable it.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
ultraloop Translate all English pages under docs/ into Chinese. Assign one subagent per page and another to check terminology consistency. Finish with a consolidated change list.
```

For parallel writes, assign disjoint files or explicitly request separate worktrees. Each agent consumes tokens independently. See [Agents and subagents](/docs/en/step-code/customization/agents).

## Publishing static websites

The built-in steppage plugin publishes a directory as a shareable static website. Install it and set `STEPFUN_API_KEY`:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/plugin install steppage
```

Restart Step Code, confirm the service in `/mcp`, then request deployment:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Publish ./dist as a website: create a site, deploy the current version, and give me a preview link.
```

Manage sites and versions at [platform.stepfun.com/sites](https://platform.stepfun.com/sites). Deployment uploads files, so inspect the output first. See [steppage: publish static websites](/docs/en/step-code/reference/steppage).

See [Plugins](/docs/en/step-code/customization/plugins) for plugin installation and management.

## Generating and maintaining documentation

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Compare the implementation in src/ with docs/ and update outdated sections. Document each new module's purpose, entry point, and examples. List uncertainties instead of inventing details. Check internal links and code examples when finished.
```

Use `/export` to preserve important discussions.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.