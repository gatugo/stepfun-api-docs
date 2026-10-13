> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cursor

This guide explains how to integrate StepFun models with Cursor for code generation, file editing, and other development tasks in Chat and Agent.

## Requirements

### Cursor Account Requirements

An active **paid Cursor subscription** (such as Pro or Teams) is required for BYOK (Bring Your Own Key). **Free / Hobby accounts cannot use the method in this guide to call Step models through Cursor's built-in Chat or Agent.**

### Install Cursor

Download and install the editor from the Cursor website. **Cursor 3.15.20 or later** is recommended.

### Choose a Billing Method

* **Standard API (pay-as-you-go)**: Confirm that your account has available balance or credits and permission to use the model.
* **Step Plan (subscription quota)**: Confirm that your [Step Plan subscription](https://platform.stepfun.ai/step-plan) is active, has available quota, and provides access to the model.

### Obtain an API Key

Create an API key on the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Configure Cursor

<Note>
  This configuration applies to Chat and Agent. Code completion (Tab) continues to use Cursor's built-in models.
</Note>

<Warning>
  **Override OpenAI Base URL** is a global override. When enabled, requests using the OpenAI protocol are sent to the custom endpoint. Before using models included in your Cursor subscription, [disable the override](#switch-back-to-cursor-models) and start a new conversation.
</Warning>

<Steps>
  <Step title="Open Model Settings">
    Open **Cursor Settings** and go to **Models**. You can also search for `Cursor Settings` in the command palette.
  </Step>

  <Step title="Configure the Connection">
    Enter the following connection settings on the Models page. The table uses the Step Plan base URL as an example:

    | Field | Value |
    | - | - |
    | OpenAI API Key | `<STEP_API_KEY>` |
    | Use OpenAI API Key | `ON` |
    | Override OpenAI Base URL | `ON` |
    | Base URL | `https://api.stepfun.ai/step_plan/v1` |

    Set **OpenAI API Key** to your Step API key for request authentication.

    <Note>
      Select the base URL for your billing method:

      <p>
        Standard API (pay-as-you-go): `https://api.stepfun.ai/v1`<br />
        Step Plan (subscription quota): `https://api.stepfun.ai/step_plan/v1`
      </p>

      Do not include `/chat/completions` in the base URL; Cursor appends this path automatically.
    </Note>
  </Step>

  <Step title="Add a Custom Model">
    Add a custom model on the Models page and set **Model ID** to `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, or `step-3.5-flash`.

    [`step-5-preview`](/docs/en/guides/models/step-5-preview) has a **1M-token** model context window.
  </Step>

  <Step title="Select the Model and Start a New Conversation">
    Open Chat or Agent, select the Step model you added, and start a new conversation to test the integration.
  </Step>
</Steps>

## Verify the Integration

### Text Connectivity

In a new conversation, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Reply only with OK.
```

**Expected result:** The model returns `OK` without a `401`, `403`, or protocol error.

### Agent Tool Calls

Use a separate test directory on a machine with Python installed. Create a `README.md` file containing `Cursor Step Plan test`, then open that directory in Cursor. In a new **Agent** conversation with the Step model selected, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md in the current workspace.
Create a hello world script in Python named hello.py that prints exactly "Hello, world!".
Run the script with an available Python interpreter and report the command and output.
Do not modify README.md or any other files.
```

Review the proposed file operations and commands before granting any required permissions.

**Expected results:**

1. The conversation shows actual tool calls to read `README.md`, create `hello.py`, and execute a command.
2. `hello.py` exists in the working directory, and you can inspect its contents and changes in the editor.
3. The script outputs `Hello, world!`.

A code snippet returned in chat alone does not verify Agent tool execution.

### Request Routing

In the [Step platform](https://platform.stepfun.ai) usage or request records, confirm that the model ID matches your selection in Cursor and that the billing channel matches the configured standard API or Step Plan base URL.

### Restart Verification (Optional)

Quit Cursor completely and reopen it. Confirm that the Models settings are retained, then repeat the text connectivity test in a new conversation with the same model.

## Switch Back to Cursor Models

Changing the model selector alone does not disable the custom base URL.

1. In **Cursor Settings → Models**, disable **Override OpenAI Base URL**.
2. Disable **Use OpenAI API Key** if needed.
3. Start a new conversation and select the Cursor model you want to use.

## Frequently Asked Questions

<AccordionGroup>
  <Accordion title="Q: Why am I prompted to upgrade or shown a usage limit after adding an API key?">
    First, check the subscription for the account currently signed in to Cursor in the Cursor Dashboard:

    * **Free / Hobby**: Free accounts do not support BYOK. Meet the [Cursor account requirements](#cursor-account-requirements) first.
    * **Active paid subscription**: Confirm that you are signed in to the subscribed Cursor account and have selected the custom Step model in a new conversation. For team accounts, also confirm that the administrator allows BYOK and check team usage limits. Check your Step account's model permissions and balance or subscription quota for the [selected billing method](#choose-a-billing-method).
  </Accordion>

  <Accordion title="Q: How do I resolve Connection error?">
    Check the following in order:

    1. **Override OpenAI Base URL** is enabled and the base URL matches your billing method: `https://api.stepfun.ai/v1` for the standard API or `https://api.stepfun.ai/step_plan/v1` for Step Plan.
    2. The base URL does not include a full API path such as `/chat/completions`.
    3. The API key is valid and **Use OpenAI API Key** is enabled.
    4. The model ID is spelled correctly and your account has access to the model through the selected channel.
    5. Your network can reach `https://api.stepfun.ai`. If you use a proxy, check its configuration as well.
  </Accordion>

  <Accordion title="Q: How do I resolve 401 Incorrect API key?">
    Check that:

    * The key was copied completely, contains no extra spaces or line breaks, and has not been revoked.
    * The key belongs to your international (`.ai`) account, not another site or provider.
    * **Use OpenAI API Key** is `ON`.

    Paste the complete key, enable the toggle, and retry in a new conversation. For permission or quota errors, check your account against the requirements for the [selected billing method](#choose-a-billing-method).
  </Accordion>

  <Accordion title="Q: How do I resolve model not found / BAD_MODEL_NAME?">
    1. Confirm that the model ID is correct, such as `step-5-preview`, and that your account has access to it through the selected channel.
    2. Confirm that the override is enabled and the base URL matches the selected billing method.
    3. Select that custom model in a new Chat or Agent conversation.
  </Accordion>

  <Accordion title="Q: Why does Chat work but Agent cannot execute tasks?">
    * Confirm that you are using **Agent** mode, not only a text conversation mode.
    * Select the custom Step model rather than Auto, then retry the minimal Agent task in a new conversation.
    * Check whether Cursor is waiting for permission to edit files or execute terminal commands. The Python example also requires a working local Python interpreter.
    * Distinguish model request failures from tool execution failures. A missing Python installation or denied command does not indicate a failed model connection.
  </Accordion>
</AccordionGroup>

If the issue persists, provide the Cursor version, model ID, time of the failure, redacted error details, and Cursor Request ID when contacting support.

To copy the Cursor Request ID, open the **…** menu in the top-right corner of the affected Chat or Agent conversation and select **Copy Request ID**.

## Related Documentation

* [Step Plan Quick Start](/docs/en/step-plan/quick-start)
* [Step 5 Preview Model Specifications](/docs/en/guides/models/step-5-preview)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.