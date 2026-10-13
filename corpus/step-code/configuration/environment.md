> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Environment variables

Environment variables identify Step Code subprocesses, control permissions and multiple agents, and inject temporary model configuration in CI or containers. Launch Step Code from the same terminal after setting them.

## Process marker

| Variable | Description |
| - | - |
| `AI_AGENT=step` | Lets external tools identify processes launched by Step Code |

Subprocesses inherit this marker. SDK embedding does not set it automatically.

## Runtime switches

| Variable | Description |
| - | - |
| `STEP_PERMISSION_PRESET`, `STEP_APPROVAL_MODE` | Override permission mode; see [Interaction and input](/docs/en/step-code/guides/interaction#permission-modes) |
| `STEP_DISABLE_WORKFLOW` | Set to `1` to disable workflow / ultraloop registration |

## Telemetry

Disable telemetry in the global `config.toml`:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[telemetry]
enabled = false
```

Telemetry includes device and account identifiers, not prompts, code, or paths. Telemetry, model requests, and manually submitted feedback are separate data channels. Disabling telemetry does not stop model calls.

## Injecting models with environment variables

| Variable | Description |
| - | - |
| `STEPCODE_CONFIG_PATH` | JSON model configuration injected into the catalog at startup without writing to `models.json` |
| `STEP_API_KEY` | Default key variable for the `stepcode` platform |
| `STEP_MAX_CONTEXT_TOKENS` | Override the injected model's context window |
| `STEP_MAX_OUTPUT_TOKENS` | Override the injected model's maximum output |

Use this for temporary endpoints in CI or containers. When the model ID used in requests (the wire model ID) matches a model in the built-in catalog, the injected model inherits its capability flags, including adaptive thinking.

See [Platforms and models](/docs/en/step-code/configuration/models) for persistent configuration.

## Provider credentials

Each provider uses its own variables, such as `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. See [API key providers](/docs/en/step-code/configuration/models#api-key-providers).

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEP_API_KEY="YOUR_STEP_API_KEY"
```

Replace `YOUR_STEP_API_KEY` with your key. Credential priority is CLI `--api-key` > `auth.json` > environment variables. Never commit real keys.

The steppage hosting plugin uses `STEPFUN_API_KEY`; preserve the variable name required by that tool.

## Proxies

Use `HTTP_PROXY` / `HTTPS_PROXY` for outbound proxies, or global `httpProxy` in `config.toml`. `NO_PROXY` matches hostnames or suffixes that bypass the proxy.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export HTTPS_PROXY="http://127.0.0.1:7890"
export NO_PROXY="localhost,127.0.0.1"
step
```

Replace the port with your proxy's port. This example bypasses the proxy for loopback requests.

## Next steps

* [Platforms and models](/docs/en/step-code/configuration/models): provider credentials.
* [Data paths](/docs/en/step-code/configuration/data-paths): local directory layout.
* [Configuration files](/docs/en/step-code/configuration/files): related settings.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.