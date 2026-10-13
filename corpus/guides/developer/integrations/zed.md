> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Zed

Zed is a high-performance code editor with built-in AI Assistant capabilities, supporting third-party large model integration via OpenAI Compatible API. By configuring a custom API Endpoint, Zed can connect to Step models to perform tasks such as conversation, code generation, code explanation, and code modification directly within the editor.

## Overview

Zed is ideal for using AI Assistant directly within a lightweight editor. Once the interface is configured, you can invoke Step models inside the editor to complete common programming assistance tasks.

## Prerequisites

### Install Zed

Download and install the Zed editor: [https://zed.dev](https://zed.dev)
Launch Zed after installation.

### Subscribe to Step Plan

Before starting the configuration, please confirm that your current account has completed the Step Plan subscription. Model invocations and quota usage will only work properly after the account has the corresponding plan or access permissions.
To subscribe or purchase, visit: [Step Plan subscription](https://platform.stepfun.ai/step-plan)

### Obtain a Step API Key

Obtain an API Key from the [Step Open Platform](https://platform.stepfun.ai/interface-key) for authentication and request authorization.

## Configuration Steps

### Open Agent Panel Settings

Use the command palette (`Cmd+Shift+P`), then type and execute:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
agent: open settings
```

### Add an LLM Provider

In the opened interface, locate the **LLM Providers** section and click the **+ Add Provider** button on the right. Fill in the following information in the form that appears:

* **Provider Name**: `Stepfun` (custom name, can be anything)
* **API URL**: `https://api.stepfun.ai/step_plan/v1`
* **API Key**: Enter the API Key obtained from the Step platform
* **Model Name**: `<model_id>`

> Note: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.
> After filling in the details, click **Save Provider** to save.

## Testing the Integration

### Basic Conversation Test

In the Agent Panel, enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hello
```

If a normal response is returned, the API call was successful.

### Code Generation Test

Enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Write a python hello world program
```

Expected output similar to:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
print("Hello, world!")
```

### Code Explanation Test

Select a snippet of code in a code file, then enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Explain this code
```

If an explanation is returned, the model invocation pipeline is working correctly.

## Frequently Asked Questions

### Unable to Connect to API

Please check:

* Whether the API URL is set to `https://api.stepfun.ai/step_plan/v1`
* Whether the API Key is valid
* Whether the current network can reach the API Endpoint

### Model Returns an Error

Confirm that the Model Name is entered correctly, for example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

### AI Is Unresponsive

It is recommended to re-check the following configuration and restart Zed:

* API URL
* API Key
* Model Name (`<model_id>`)

## Summary

Once the LLM Provider configuration is complete, Zed can provide assistance capabilities such as conversation, code generation, and code explanation via the Step API. It is recommended to first complete a basic conversation test and a minimal code example test before using it in actual development.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.