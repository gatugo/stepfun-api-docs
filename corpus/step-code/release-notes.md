> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Release Notes

## v0.1.2

September 30, 2026

### New features

* Add `--non-interactive-denial continue`. In non-interactive runs, such as `-p` mode, a dangerous operation that requires approval is blocked and the reason is returned to the agent so it can attempt a safer approach and continue the task. The default remains `terminate`, which ends the task. Both policies enforce the existing permission restrictions.

### Improvements

* Add search to marketplace plugin lists and remove duplicate entries with the same name. Adding a marketplace in the interactive interface now shows progress, supports cancellation, and opens the plugin list on success.
* Show a preview of long tool results with a file path to the full text, reducing model context usage.
* Display only the most recent successful task plan update in a conversation, including when resuming a session.
* Improve Up Arrow history navigation for single-line input. Add `Ctrl+End` in fullscreen mode to return to the bottom and follow new output.

### Fixes

* Fix the thinking level being forced to the highest setting when starting or switching to a Step model.
* Fix skill scanning hangs and skill commands failing to recognize arguments entered on a new line.
* Fix loaded skill instructions being lost after built-in context compaction.
* Retry compaction after trimming older history when the summary request exceeds a limit.
* Fix skills and prompt commands from installed plugins not loading. Reload resources to make them available.
* Fix plugin MCP configuration recognition, server name recognition, and reuse of login authorization. Local MCP servers now start from the plugin directory by default.
* Fix incomplete loading of paginated MCP tool lists and search failing to find available MCP and extension tools loaded later. Tool lists update in response to server notifications.

## v0.1.1

September 24, 2026

### New features

* Automatically install the StepPage plugin on first launch. It stays uninstalled if the user removes it.

### Improvements

* Reduce redraws in the subagent task list to minimize flicker and improve readability.
* Add a post-installation prompt on macOS and Linux to guide users to run `step`.
* Update the English and Chinese READMEs with StepPage publishing instructions and demos.

### Fixes

* Fix Workflow and Ultraloop being unavailable in release installations. The workflow sandbox now uses QuickJS WebAssembly instead of `isolated-vm`.
* Fix unexpected exits and false timeouts in Workflow involving unawaited asynchronous tasks, long-running parallel tasks, and resource cleanup.
* Correct the billing route for Step Plan web search to use the subscription endpoint.
* Fix plugin diagnostics incorrectly reporting a missing `STEPFUN_API_KEY` for users who are already signed in.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.