> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Goose

Goose is an open-source AI Agent client developed by Block (formerly Square). It is suitable for development tasks such as code generation, file editing, command execution, and project analysis through natural language. By configuring an OpenAI Compatible provider, Goose can connect to Step models and work with local tools in common development workflows.

This document explains the prerequisites, configuration steps, and basic verification methods for integrating the Step API with Goose.

## Overview

Goose supports integrating third-party large language models through the OpenAI Compatible API. After the provider is configured, you can directly use Step models in Goose for conversational tasks, code editing, and tool invocation.

By configuring a custom provider, Goose can use Step models for the following capabilities:

* Autonomous task execution: Automatically edit files and run shell commands.
* Codebase analysis: Understand project structures and answer complex programming questions.
* Automated workflows: Combine with local toolchains to complete end-to-end development tasks.

## Prerequisites

Before starting, make sure the following requirements are met.

### Install Goose

Make sure the Goose command-line tool or desktop client is installed.

* [Official Website](https://block.github.io/goose/)

### Subscribe to Step Plan

Before you start configuring, make sure your current account has an active Step Plan subscription. Only accounts with the required plan or calling permissions can use model calls and quotas normally.

To subscribe or purchase, visit [Step Plan subscription](https://platform.stepfun.ai/step-plan)

### Obtain a Step API Key

Log in to the StepFun Open Platform to obtain the API Key used for authentication, and keep it safe.

### Confirm the Connection Information

Prepare the following connection details in advance:

* Base URL: `https://api.stepfun.ai/step_plan/v1`
* Protocol type: `OpenAI Compatible`

## Configuration Steps

### Open the Provider Settings

In the Goose desktop client, click `Settings`, select `Providers`, and then click `Add Provider`.

### Fill In the Configuration Parameters

In the configuration dialog, enter the following information:

* Provider Type: Select `OpenAI Compatible`
* Display Name: Enter `StepFun`
* API URL: Enter `https://api.stepfun.ai/step_plan/v1`
* API Key: Paste the key you obtained from the Step platform
* Available Models: Enter the following model name

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

> Note: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.

After the configuration is complete, Goose can call Step models through this provider.

## Test the Integration

After configuration, switch to any model under the `StepFun` provider in the main Goose chat window and use the following examples for verification.

### Basic Conversation Test

Input:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Hello, who are you?
```

Expected result: A model identity response provided by StepFun is returned.

### Tool Capability Test

Input:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Please list all files in my current directory.
```

Expected result: Goose calls the local directory listing tool and uses the Step model to summarize the file list.

### Code Editing Test

Input:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Help me create a file named hello.py that outputs the current time.
```

Expected result: Goose generates the code and saves the file to the local disk.

## Common Issues

### Tool Recognition Failure or Connection Timeout

Possible cause: The current network environment may not be able to access the API endpoint directly.

Check the following:

* Whether the proxy or network settings are correct
* Whether the API URL accidentally includes a trailing slash

### Empty Model List

If the model dropdown is empty, make sure specific model identifiers have been entered manually in `Available Models`, for example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

If no model identifiers are entered, the dropdown may not display available options correctly.

## Summary

Through Goose's `OpenAI Compatible` mode, developers can combine the inference capabilities of Step models with Goose's local toolchain for tasks such as code generation, file operations, and project analysis.

It is recommended to use `<model_id>` for integration checks and daily development tasks.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.