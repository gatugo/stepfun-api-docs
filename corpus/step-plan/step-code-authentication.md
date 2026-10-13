> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Platforms and models

Step Code supports subscription login, API keys, cloud platforms, and OpenAI / Anthropic / Google-compatible endpoints through `models.json`, including Ollama, vLLM, and LM Studio.

## Connection methods

| Method | Setup |
| - | - |
| Subscription login | Choose a platform in `/login` and authorize your account |
| API key | Enter a key in `/login`, or set the provider's environment variable before launch |
| Cloud platform | Azure OpenAI, Amazon Bedrock, Google Vertex AI, Cloudflare |
| Custom model | `~/.stepcode/models.json` |

Credential priority, from highest to lowest, is CLI `--api-key`, saved `auth.json`, environment variables, then the custom provider key in `models.json`. `auth.json` uses `0600` permissions.

## Subscription login

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/login
```

Choose Step Plan for an account on `platform.stepfun.com`, or Step Plan Oversea for an account on `platform.stepfun.ai`. OAuth credentials refresh through the login flow. Use `/logout` to clear the corresponding credentials.

| Platform | Website | Billing channel |
| - | - | - |
| Step Plan | `platform.stepfun.com` | Subscription |
| Step Plan Oversea | `platform.stepfun.ai` | Subscription |
| Open Platform API key | `platform.stepfun.com/interface-key` | Pay-as-you-go |
| Open Platform API key | `platform.stepfun.ai/interface-key` | Pay-as-you-go |

Choosing another channel does not automatically use your subscription quota. Available models and allowances depend on the account. See [Step Plan](/docs/en/step-plan/overview).

The login picker also offers Claude Pro/Max, ChatGPT Plus/Pro (Codex), GitHub Copilot, and xAI. Follow each platform's terms and account permissions.

## API key providers

| Provider | Environment variable |
| - | - |
| Step | `STEP_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Kimi For Coding | `KIMI_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| xAI | `XAI_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |

For example, configure Anthropic in Bash or Zsh:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
step --provider anthropic
```

Replace the placeholder with that provider's key. A Step key cannot be used for another provider. Keys saved with `/login` live in `~/.stepcode/auth.json`; do not commit this file.

See [Environment variables](/docs/en/step-code/configuration/environment) for runtime environment variables.

## Cloud platforms

| Platform | Configuration |
| - | - |
| Amazon Bedrock | `AWS_PROFILE`, or `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`; `AWS_REGION` defaults to `us-east-1`; supports ECS task roles and IRSA |
| Google Vertex AI | Run `gcloud auth application-default login`; set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`, such as `us-central1` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_BASE_URL`; the root endpoint normalizes to `/openai/v1`; `AZURE_OPENAI_DEPLOYMENT_NAME_MAP` maps deployment names |

Deployment names, available regions, and IAM permissions are managed by the cloud platform. Confirm access to the target model before selecting it in Step Code.

## Custom models (models.json)

Edit `~/.stepcode/models.json`, then reopen `/model` to load changes. This example connects to local Ollama:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        {"id": "llama3.1:8b"},
        {"id": "qwen2.5-coder:7b"}
      ]
    }
  }
}
```

Prepare these models in Ollama first. `ollama` is a nonempty `apiKey` placeholder. Local services without authentication still require this field to appear in `/model`; authenticated remote services require real credentials.

| Provider field | Description |
| - | - |
| `baseUrl` | Include `/v1` for OpenAI-compatible endpoints; use the `/v1beta` root for `google-generative-ai` |
| `api` | Such as `openai-completions`, `openai-responses`, `azure-openai-responses`, `anthropic-messages`, `google-generative-ai` |
| `apiKey`, `headers` | Credentials and additional request headers |
| `models` | Custom model list |
| `modelOverrides` | Override existing model properties |
| `compat` | Adjust request compatibility to match the server |

Model fields include `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost`, `thinkingLevelMap`, and `samplingParams`. `id` is required. `contextWindow` defaults to 128,000 and `maxTokens` to 16,384; override them to match model specifications.

`samplingParams` merges sampling parameters into OpenAI-compatible requests and may override named request fields. Do not add unsupported fields. Setting only `baseUrl` overrides a built-in provider's endpoint; `models` updates matching IDs and adds new ones.

Ollama / vLLM / SGLang often need `supportsDeveloperRole = false` and `supportsReasoningEffort = false` in `compat`.

See [FAQ](/docs/en/step-code/reference/faq) for model loading and login troubleshooting.

## Switching models

* `/model` opens the picker; Ctrl+S saves the startup default.
* Ctrl+P cycles `enabledModels`; see [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts) for reverse cycling.
* Use `step --provider <provider> --model <model-ID>` on the command line.
* `/thinking` or `/effort` changes thinking level; available levels and effective behavior depend on the model.

See [Configuration files](/docs/en/step-code/configuration/files) for default model settings.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.