> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenCode

Open Code is an AI Coding Agent that runs in the terminal, designed for code generation, code editing, and project analysis tasks using natural language. By configuring a Step API Key, Open Code can connect directly to Step models and invoke their inference capabilities within a terminal-based development workflow. This guide covers the prerequisites, configuration steps, and basic verification methods for integrating Open Code with the Step API.

## Overview

Open Code is well-suited for terminal-based development workflows. Once the provider is configured, you can use Step models directly in the terminal to handle common coding tasks.

## Prerequisites

### Development Environment

The following systems are supported:

* macOS
* Linux

A recent version of your operating system and terminal environment is recommended.

### Install Open Code

Open Code can be installed via Homebrew:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
brew install anomalyco/tap/opencode
```

After installation, run the following command to verify it was installed successfully:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
opencode --version
```

If a version number is returned, the installation was successful. To launch Open Code:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
opencode
```

### Subscribe to Step Plan

Before proceeding with configuration, make sure your account has an active Step Plan subscription. Model calls and quota usage will only work correctly once your account has the appropriate plan or access permissions. To subscribe or purchase, visit: [Step Plan subscription](https://platform.stepfun.ai/step-plan)

### Get a Step API Key

Visit the [Step Platform Console](https://platform.stepfun.ai/interface-key) to create an API Key and save it somewhere safe.

## Configuration

### Set Environment Variables

Open your system terminal (Terminal.app or iTerm2) and run the following commands from any directory (`~/.zshrc` is an absolute path and is not affected by your current working directory):

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
echo 'export OPENAI_API_KEY="YOUR_STEP_API_KEY"' >> ~/.zshrc
echo 'export OPENAI_BASE_URL="https://api.stepfun.ai/step_plan/v1"' >> ~/.zshrc
source ~/.zshrc
```

Replace `YOUR_STEP_API_KEY` with the Step API Key you created in the console. After running `source ~/.zshrc`, these variables will be loaded automatically every time you open a new terminal session — no need to run this again.

### Verify Environment Variables

Run the following commands to confirm the variables were written correctly:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL
```

If the output shows your API Key and `https://api.stepfun.ai/step_plan/v1` respectively, the configuration is complete.

### Select a Model

Launch Open Code:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
opencode
```

Press `Ctrl + T` to open the model list (Variants) and select the recommended model:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

> Note: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.

Once selected, the current model information will appear at the bottom of the terminal, for example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Build
<model_id>
StepFun
```

This indicates that the current Open Code session is now using the Step model.

## Test the Integration

After completing the configuration, run a simple task to verify the connection, for example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Create a hello world script in Python
```

If the integration is successful, the model will typically return something like:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
print("Hello, world!")
```

## Troubleshooting

### StepFun Models Not Showing

If you cannot find any `StepFun` models in the model list, check the following:

1. Whether Open Code is up to date.
2. Whether your network connection is working properly.
3. Whether the environment variables were written correctly (run `echo $OPENAI_BASE_URL` to verify).
4. Whether you have fully restarted the terminal before launching Open Code.

### API Key Error

If you see the following error:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
401 Incorrect API key
```

Please check:

* Whether the key was copied in full
* Whether the key belongs to the correct environment (`.ai` / `.com`)

### Model Call Failure

If the model does not return a result, check:

1. Whether the API Key is valid.
2. Whether the model name is correct.

Recommended model:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

## Summary

Once the environment variables are configured and a model is selected, Open Code can use the Step API in the terminal to handle code generation, file editing, and project analysis tasks. It is recommended to first verify connectivity with a minimal example before incorporating it into your own terminal development workflow.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.