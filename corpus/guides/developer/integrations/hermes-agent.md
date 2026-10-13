> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hermes Agent

Hermes-Agent is an open-source AI Agent framework developed by Nous Research. It supports code generation, file editing, and task automation via natural language in the terminal. Hermes-Agent can connect to Step models to access reasoning capabilities from the command line or messaging platforms.

This guide covers how to configure the Step API in Hermes-Agent and verify that the model is available.

## Overview

Hermes-Agent is an AI programming assistant designed for server or local terminal environments. Once configured, you can interact with the Agent through a terminal TUI or messaging platforms like Telegram to perform code generation, file operations, scheduled tasks, and other automated workflows.

## Prerequisites

### Operating System

Hermes-Agent supports the following systems:

* Linux (Ubuntu/Debian recommended)
* macOS
* Windows (requires WSL2)

### Install Hermes-Agent

Hermes-Agent provides a one-click installation script that automatically handles dependency installation and configuration.

**Via installation script (recommended):**

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

The installation script automatically detects and installs the following components:

* `uv` (Python package manager)
* `Python 3.9+`
* `Node.js` (required by some skills)
* `ripgrep`, `ffmpeg`, and other tools

After installation, reload your shell configuration:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
source ~/.bashrc   # Bash users
# or
source ~/.zshrc    # Zsh users
```

Verify the installation:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hermes --version
```

If a version number is returned (e.g., `Hermes Agent v0.6.0`), the installation was successful.

### Subscribe to Step Plan

Before configuring, ensure your account has an active Step Plan subscription. Model calls and quota usage will only work after the corresponding plan or calling permissions are in place.

To subscribe or purchase, visit: [Step Plan Subscription](https://platform.stepfun.ai/step-plan)

### Obtain a Step API Key

Get your API Key from the [StepFun Open Platform](https://platform.stepfun.ai/interface-key) for authentication and request authorization. We recommend creating a new Key via the console and avoiding hardcoding it in your code repository.

Best practices:

* Store the Key in environment variables
* Or manage the Key through local configuration files

## Configuration Steps

Hermes-Agent reads API service addresses and authentication information from environment variables or configuration files.

### Option 1: Hermes-Agent Setup Wizard

If this is your first installation or you want to re-run the guided setup:

Open your terminal and run:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hermes setup
```

During the guided process:

1. When prompted to select a model provider, choose **"More providers"** then select **"Custom endpoint"**.

2. Enter the Base URL: `https://api.stepfun.ai/step_plan/v1`

3. Enter the API Key you obtained in the first step.

4. For Model ID, enter: `<model_id>`

5. Set the context length as needed. Step 5 Preview supports a 1M-token context window; Step 3.7 Flash and the Step 3.5 Flash series support 256K. Use the limit for your selected model.

### Option 2: Configuration File

The Hermes-Agent configuration file is located at `~/.hermes/config.yaml`.

Open the configuration file, find the `model` settings, and add or modify the following:

```yaml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
model:
  provider: openai
  api_key: "YOUR_STEP_API_KEY"
  base_url: "https://api.stepfun.ai/step_plan/v1"
  model: "<model_id>"
```

> **Note**: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.

### Select Model

After configuration, run the following command to select a model:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hermes model
```

## Test the Integration

After completing configuration, start Hermes-Agent and send a test message:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hermes
```

In the chat interface, type:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hello
```

If a normal response is returned, the API call was successful.

### Code Generation Test

Input:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Create a hello world script in Python
```

Expected output:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
print("Hello, world!")
```

### File Operation Test

Input:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Create a file named test.txt in the current directory with the content "Hermes-Agent test"
```

If the Agent successfully creates the file, the model call pipeline is working correctly.

## Troubleshooting

### Model List is Empty or Won't Load

If `hermes model` does not show Step-related models, check:

1. Whether your network can reach `api.stepfun.ai`.
2. Whether the Base URL is set to `https://api.stepfun.ai/step_plan/v1`.
3. Whether your API Key has Step Plan permissions.
4. Whether Hermes-Agent is up to date (`hermes update` to upgrade).

### API Key Error

If you see this error:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
401 Incorrect API key
```

Check:

* Whether the Key was copied completely
* Whether the Key belongs to the correct environment
* Whether the Base URL points to the Step Plan endpoint

### Connection Timeout or Failure

Check:

* Whether your network environment is normal (configure proxy if needed)
* Whether the API endpoint is reachable (`curl https://api.stepfun.ai/step_plan/v1` to test connectivity)

### Model Returns Errors

Verify that the Model ID is correct, for example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
<model_id>
```

Recommended models (verified examples; replace according to your account permissions):

* `step-5-preview` (Flagship model for agentic work, supports image and video understanding)
* `step-3.7-flash` (High-speed multimodal reasoning model, supports image and video understanding)
* `step-3.5-flash-2603` (Agent-optimized version, stronger reasoning)
* `step-3.5-flash` (Standard version, faster response)

## Advanced Configuration (Optional)

### Enable Tool Calling

Hermes-Agent supports automatic tool calling. Enable it in `~/.hermes/config.yaml`:

```yaml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
tools:
  enabled:
    - terminal
    - file
    - browser
    - code_execution
```

### Configure Memory System

Hermes-Agent's persistent memory is stored in `~/.hermes/memories/`. You can use natural language to tell the Agent to remember important information, which will be automatically recalled in future conversations.

### Messaging Gateway (Telegram/Discord)

To chat with Hermes-Agent on your phone via Telegram, start the gateway:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
hermes gateway start
```

On first run, you'll be prompted to configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS`. You can obtain these from @BotFather on Telegram.

## Summary

After completing environment variable or configuration file setup, Hermes-Agent can execute code generation, file editing, task automation, and other development tasks through the Step API in the terminal or messaging platforms. We recommend starting with a minimal example (like hello world) to verify connectivity, then gradually exploring skill creation, memory management, scheduled tasks, and other advanced features.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.