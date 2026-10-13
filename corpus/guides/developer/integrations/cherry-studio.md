> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cherry Studio

Cherry Studio is a desktop AI client that supports multiple model providers and offers capabilities such as conversation, code generation, and text generation. By configuring a StepFun API key, Cherry Studio can connect directly to Step models, bringing inference capabilities right into your desktop workflow.

This guide covers the prerequisites, configuration steps, and basic testing process for connecting Cherry Studio to the StepFun API.

## Overview

Cherry Studio is well-suited for handling multi-model conversations and development tasks from a unified desktop workspace. Once the provider is configured, you can call Step models directly from the client.

## Prerequisites

### System Requirements

Cherry Studio is available on:

* macOS
* Windows
* Linux

We recommend using the latest version of Cherry Studio.

### Install Cherry Studio

Download the installer from the [Cherry Studio website](https://cherry-ai.com).

Launch Cherry Studio after installation.

### Subscribe to Step Plan

Before configuring the provider, make sure your account has an active Step Plan subscription. Model calls and quota usage will only work correctly once your account has the appropriate plan.

To subscribe, visit: [Step Plan subscription](https://platform.stepfun.ai/step-plan)

### Get Your StepFun API Key

Go to the [Step Platform Console](https://platform.stepfun.ai/interface-key) to create an API key. Copy and store it securely.

## Configuration

### Add the Provider

Open Cherry Studio and navigate to the model configuration screen:

1. In the model provider list, select **StepFun**.
2. Enter your `StepFun API Key`.
3. In the API URL field, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
https://api.stepfun.ai/step_plan/v1
```

4. Save the configuration.

5. Add a model: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, or `step-3.5-flash`.

Click **+ Add**, then fill in the following fields in the dialog:

* Model ID: `<model_id>`
* Model Name: a recognizable name matching the selected model, such as `Step 5 Preview`
* Group Name: StepFun (or any suitable group name)

> Note: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.

Click **Add Model** to save.

## Test the Connection

Click the **Test** button next to the API key field. If it reports success, the setup is complete. If you see an error, double-check that both the API key and the base URL are entered correctly.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.