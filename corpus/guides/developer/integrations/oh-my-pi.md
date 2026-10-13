> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Oh My Pi

Oh My Pi (OMP, the `oh-my-pi` npm package) extends Pi with task categories, specialist roles, and skills. It uses Pi's provider configuration to connect to Step Plan through the Anthropic Messages API.

## Requirements

* Pi 0.87.1 installed and connected to Step Plan, with a successful conversation test as described in the [Pi integration guide](/docs/en/guides/developer/integrations/pi).
* `STEP_API_KEY` set in the terminal that launches Pi.

## Install OMP

1. Install `oh-my-pi` 0.2.0 from your terminal.

   ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
   pi install npm:oh-my-pi@0.2.0
   ```

2. List installed packages.

   ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
   pi list
   ```

The list should include `npm:oh-my-pi@0.2.0`. Pi loads the extension in new sessions.

## Configure the orchestrator

To customize the orchestrator name and prompt template, merge this configuration into `.oh-my-pi.jsonc` in your project root. Preserve existing fields, or create the file if it does not exist.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "orchestrator": {
    "agentName": "stepfun",
    "promptTemplate": "sisyphus"
  }
}
```

After saving, run `/oh-my-pi-reload` in an existing Pi session or restart Pi.

## Start Pi

Run this command from your project directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi --provider stepfun --model step-5-preview
```

## Verify the integration

### Check extension status

Enter this command in a Pi session:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/oh-my-pi-doctor
```

The report should show `Healthy` with no configuration errors.

### Test a conversation

Run this command in your terminal:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi --provider stepfun --model step-5-preview --print "Reply only with OK."
```

Expected output: `OK`.

### Test tool calls

1. Create a separate test directory on a machine with Python installed. Add a `README.md` containing `Oh My Pi Step Plan test`.

2. Start Pi from that directory.

3. Enter the following task.

   ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
   Read README.md and create hello.py that prints exactly "Hello, StepFun!".
   Run hello.py with an available Python interpreter and report the command and output.
   Do not modify other files.
   ```

4. Check the file-reading, creation, and command records. Confirm that `hello.py` outputs `Hello, StepFun!`.

### Test a specialist role

In a Pi session in the same test directory, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Use the oh_my_pi_subagent tool to ask oracle to review hello.py for output correctness and portability.
Give a brief assessment without changing any files.
```

Check that the tool records include `oh_my_pi_subagent` and that the current session returns a review.

### Check the request channel

Pi's Step Plan Base URL is `https://api.stepfun.ai/step_plan`, with requests sent to `/step_plan/v1/messages`. To confirm routing or billing attribution, provide the request time, model ID, and Request ID to technical support.

## Common questions

<AccordionGroup>
  <Accordion title="Q: What if Pi cannot find the package during installation?">
    Use the `npm:` prefix for npm package sources. Run `pi install npm:oh-my-pi@0.2.0`, then check the result with `pi list`.
  </Accordion>

  <Accordion title="Q: Can oracle use a separate model?">
    In 0.2.0, `oh_my_pi_subagent` returns role instructions to the current session. Subsequent requests use the model selected in Pi. This version does not implement model switching through `agents.oracle.model` or a task category's `model` field. Select the model with Pi's `--provider` and `--model` arguments.
  </Accordion>

  <Accordion title="Q: How do I disable OMP?">
    Run `pi remove npm:oh-my-pi@0.2.0` in your terminal, then restart Pi.
  </Accordion>

  <Accordion title="Q: How do I troubleshoot authentication, request paths, or context settings?">
    OMP uses Pi's model and credential configuration. Follow the [Pi integration guide](/docs/en/guides/developer/integrations/pi) to check `STEP_API_KEY`, `baseUrl` in `models.json`, and the model's `contextWindow`.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.