> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CodeGPT

CodeGPT is a VS Code coding assistant extension with Chat and Agent modes. Its OpenAI-compatible Custom provider connects to Step Plan models for conversations and code changes.

## Requirements

* VS Code with the CodeGPT extension, ID `danielsanmedium.dscodegpt`. These configuration steps apply to CodeGPT 3.24.73.
* A signed-in CodeGPT account with access to Local / Custom in model management.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan), available quota, and access to the model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Configure the connection

1. Open Manage AI Models in the CodeGPT panel.
2. Select Local, then Custom (any OpenAI-compatible server).
3. Enter the connection settings.

| Setting | Value |
| - | - |
| Base URL / endpoint | `https://api.stepfun.ai/step_plan/v1` |
| API Key | Your StepFun API key |

CodeGPT appends `/chat/completions` to the base URL. This URL uses Step Plan subscription quota.

4. Click Test. When `Connected` appears and the model list loads, select `step-5-preview`.
5. Click Save & close.
6. Select `step-5-preview` under Custom in the chat model picker and start a new conversation.

Configure the Custom provider's URL, key, and model in the model management panel.

## Verify the integration

### Test a conversation

In Chat, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Reply only with OK.
```

Expected output: `OK`.

### Test tool calls

Create a separate test directory on a machine with Python installed. Add a `README.md` containing `CodeGPT Step Plan test` and open the directory in VS Code.

Switch to Agent mode, confirm that `step-5-preview` under Custom is selected, and enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md and create hello.py that prints exactly "Hello, StepFun!".
Run hello.py with an available Python interpreter and report the command and output.
Do not modify other files.
```

Approve the required file operations and commands. Check the tool records, the generated `hello.py`, and the `Hello, StepFun!` output.

### Check usage

In the [StepFun platform](https://platform.stepfun.ai) usage details, match the request time, model ID, and billing source to confirm that the call used Step Plan.

## Common questions

<AccordionGroup>
  <Accordion title="Q: What should I check if Test fails?">
    Check the base URL, API key, and network connection. Use `https://api.stepfun.ai/step_plan/v1` with a key from the corresponding platform account, then click Test again.
  </Accordion>

  <Accordion title="Q: Why is the model list empty or missing the model I need?">
    Confirm that Test shows `Connected`, and check your account's Step Plan subscription and model permissions. Test the connection again before selecting a model.
  </Accordion>

  <Accordion title="Q: How do I confirm that a Step model is selected?">
    Choose `step-5-preview` under Custom in the model picker. Check the model and billing source for the request in the StepFun platform usage details.
  </Accordion>

  <Accordion title="Q: Why does Chat work but Agent cannot execute tasks?">
    Confirm that Agent mode is selected and a project directory is open. Check file and terminal permissions. The Python example also requires a working local Python interpreter.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.