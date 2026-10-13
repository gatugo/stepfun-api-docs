> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DeepSeek Harness

DeepSeek Harness (`dsh`) is an open-source agent harness developed by DeepSeek. This guide connects Step 5 Preview through a custom provider and covers the Web UI, configuration files, verification, and troubleshooting.

<Note>
  dsh is in developer preview, so its interface and configuration may change. This guide follows the current official model configuration documentation. Read the project's [safety notice](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md) before running it, use a trusted working directory, and review permissions for file operations and command execution.
</Note>

## Configuration reference

| Setting | Value |
| - | - |
| Provider ID | `stepfun` |
| API protocol | `openai-completions` |
| Step Plan Base URL | `https://api.stepfun.ai/step_plan/v1` |
| Pay-as-you-go API Base URL | `https://api.stepfun.ai/v1` |
| Model ID | `step-5-preview` |
| Context window | 1,000,000 tokens |
| API Key | [Console key management](https://platform.stepfun.ai/interface-key) |

## Prerequisites

### Install and start dsh

Prepare Node.js 22.19+ (22.x) or 24+ and npm. A current LTS release is recommended; follow dsh's official requirements. Run this command in a trusted working directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
npx -y @deepseek-ai/dsh web
```

The first run downloads the required packages. A local launch opens `http://127.0.0.1:3080` by default; an SSH launch may only print the address. See the [official dsh repository](https://github.com/deepseek-ai/deepseek-harness) for launch options.

### Obtain an API Key

Create an API Key in the [console](https://platform.stepfun.ai/interface-key). For Step Plan, confirm your [subscription](https://platform.stepfun.ai/plan-subscribe) and model access. For pay-as-you-go access, check your account balance and permissions. Never commit a real key or share it in screenshots.

## Option 1: Configure through the Web UI

<Warning>
  To use Step Plan quota, select `/step_plan/v1` and ensure your subscription and model access are active. The standard `/v1` endpoint uses pay-as-you-go billing; a Step Plan subscription does not automatically apply to it. Examples below use Step Plan. For pay-as-you-go access, replace the Base URL consistently.
</Warning>

<Steps>
  <Step title="Open model settings">
    In the dsh Web UI, open **Settings → Models** and choose **Add a custom provider**.
  </Step>

  <Step title="Configure the provider">
    | Field | Value |
    | - | - |
    | Provider ID | `stepfun`: a provider identifier, not a model name |
    | Display name | `StepFun` |
    | Base URL | `https://api.stepfun.ai/step_plan/v1` |
    | API protocol | `openai-completions` |
    | API key | Your StepFun API Key |

    A saved Provider ID cannot be renamed directly. Create a new provider to use a different identifier.
  </Step>

  <Step title="Add models">
    Choose **Add model** and set both the model ID and display name to `step-5-preview`. Under **Model options**, set the context window to `1000000` (1,000,000 tokens; enter the value without commas). For image input, keep **Text** selected and enable **Image** under **Input types**.

    Optionally add `step-3.7-flash` with a context window of 256,000 tokens (enter `256000`). See [Step 5 Preview](/docs/en/guides/models/step-5-preview) and [Step 3.7 Flash](/docs/en/guides/models/step-3.7-flash) for the respective model specifications. Model availability depends on your account permissions.

    <Warning>
      Model IDs cannot be empty. Clicking Add model without entering an ID prevents saving. The Provider ID is `stepfun`; the model ID is `step-5-preview`.
    </Warning>
  </Step>

  <Step title="Save and select the model">
    Click **Create provider**, start a new session, select `step-5-preview` under StepFun in the model picker, and send a simple message. An existing session may retain its previous model.
  </Step>
</Steps>

<Info>
  Keys saved through the Web UI are stored in `$DSH_HOME/.credentials.yaml` on the machine running dsh, while settings retain a credential reference. If dsh runs on a remote server, the key is stored there. Model requests still send the key to the configured API service for authentication. Verify the Base URL.
</Info>

## Option 2: Configure through YAML

<Warning>
  To use Step Plan quota, select `/step_plan/v1` and ensure your subscription and model access are active. The standard `/v1` endpoint uses pay-as-you-go billing; a Step Plan subscription does not automatically apply to it. Examples below use Step Plan. For pay-as-you-go access, replace the Base URL consistently.
</Warning>

Edit `~/.dsh/settings.yaml`. If `DSH_HOME` is set, use `settings.yaml` in that directory instead. Merge this configuration into the existing `llm-pi-ai.providers` section without overwriting other providers or duplicating YAML keys.

```yaml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
llm-pi-ai:
  providers:
    stepfun:
      apiKeyEnv: STEPFUN_API_KEY
      api: openai-completions
      baseURL: https://api.stepfun.ai/step_plan/v1
      compat:
        supportsDeveloperRole: false
        maxTokensField: max_tokens
      models:
        - id: step-5-preview
          name: step-5-preview
          contextWindow: 1000000
          input: [text, image]
        - id: step-3.7-flash
          name: step-3.7-flash
          contextWindow: 256000
          input: [text, image]
```

`compat` uses a compatible role for system instructions and `max_tokens` for the output limit; see [dsh request compatibility](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md#request-compatibility). `input` declares what dsh can send, rather than every modality the model supports.

### Configure credentials

Choose one method:

* **Web UI (recommended)**: Start dsh, open **Settings → Models**, edit `stepfun`, enter the API Key, and save.
* **Environment variable**: Replace `YOUR_STEP_API_KEY` with your API Key, set the variable in the same terminal that starts dsh, then launch the process. These commands target Bash or Zsh on macOS / Linux / WSL:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEPFUN_API_KEY="YOUR_STEP_API_KEY"
npx -y @deepseek-ai/dsh web
```

<Note>
  Changes to `settings.yaml` and credentials saved through the Web UI normally take effect on the next request without a restart. A running process does not inherit new variables exported in another shell. When using environment variables, restart dsh from the terminal where the variable is set.
</Note>

## Verify the configuration

First confirm that a **new dsh session** selects `step-5-preview` under `stepfun`, send a simple message, and check the response.

To test API connectivity separately, set `STEPFUN_API_KEY` in your terminal and run the following command. Saving a key only in the Web UI does not set a terminal environment variable.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl --silent --show-error --fail-with-body \
  --write-out '\nHTTP %{http_code}\n' \
  https://api.stepfun.ai/step_plan/v1/chat/completions \
  -H "Authorization: Bearer $STEPFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "step-5-preview",
    "messages": [{"role": "user", "content": "Say hello briefly."}],
    "max_tokens": 1024
  }'
```

HTTP 200 with a valid `choices` response means this API request succeeded; it does not independently verify dsh's provider, credentials, or session selection. If output is truncated, increase `max_tokens` and retry. Test requests consume the corresponding account quota.

## Troubleshooting

| Symptom | What to check |
| - | - |
| `MISSING_CREDENTIAL` | Match `apiKeyEnv` to `STEPFUN_API_KEY` and ensure the dsh process receives the variable, or save the key through the Web UI. Update or remove an old environment variable and restart so it does not shadow a new UI-saved key. |
| Model ID cannot be empty | A model ID identifies the model in API requests: use `step-5-preview` for Step 5 Preview or `step-3.7-flash` for Step 3.7 Flash. Fill in each model's ID or remove empty rows. The Provider ID is `stepfun`; do not confuse it with a model ID. |
| `401 Unauthorized` | Check that the key is valid and belongs to the platform account for the selected API endpoint. |
| `404` / model not found | Check the Base URL, `step-5-preview` spelling, and model access. Do not include `/chat/completions` in the Base URL. |
| Requests reject fields despite a valid key and URL | Check `compat.supportsDeveloperRole: false` and `compat.maxTokensField: max_tokens` in YAML, then retry in a new session. |
| Configuration changes do not apply | Check `DSH_HOME`, YAML indentation, and duplicate keys. Select the model again and start a new session. Restart dsh when supplying a new environment variable. |
| Model discovery fails | Discovery depends on the server's model-list endpoint. Add model IDs manually instead. |

## Related documentation

* [Step 5 Preview](/docs/en/guides/models/step-5-preview)
* [Step 3.7 Flash](/docs/en/guides/models/step-3.7-flash)
* [Step Plan quickstart](/docs/en/step-plan/quick-start)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.