> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mobile Agent

`step-3.7-flash`'s multimodal understanding works well for mobile GUI Agent scenarios: the model reads screenshots, task descriptions, and history, decides the next action, and then the runtime executes that action on a real Android device.

Today we recommend [GELab-Zero](https://github.com/stepfun-ai/gelab-zero) for running this end-to-end. GELab-Zero is a GUI Agent runtime for Android — it handles device connection, screenshot capture, multimodal model calls, action execution, and logging.

<Info>
  Mobile Agent involves a real device, ADB, model calls, and a local runtime — best treated as an advanced scenario. For your first run, complete the [Quickstart](/docs/en/quickstart/overview) first to confirm your API key and model calls are healthy.
</Info>

## How it works

GELab-Zero strings model decisions and device actions into a complete loop:

1. You give the Agent a natural-language task.
2. Your computer connects to the Android phone via ADB and captures a screenshot.
3. The runtime sends the current screenshot, action history, and task description to the multimodal model.
4. The model outputs the next action — e.g. `AWAKE`, `CLICK`, `TYPE`, `SLIDE`.
5. The runtime executes the action on the phone.
6. Every step's screenshot, action, and model output is logged.
7. After the task completes, you can replay the full run from the visualization UI by `Session ID`.

## Prerequisites

You need:

* An Android phone with Developer Mode and USB Debugging enabled
* ADB / platform-tools
* Python 3.12+
* The GELab-Zero repo and its dependencies
* A valid Step API key

Connect the phone via USB and confirm ADB sees it:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
adb devices
```

If the device shows `unauthorized`, accept the USB debugging prompt on the phone.

## Install GELab-Zero

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
git clone https://github.com/stepfun-ai/gelab-zero
cd gelab-zero
pip install -r requirements.txt
```

It's recommended to run subsequent commands from the GELab-Zero project root.

## Configure the model service

GELab-Zero reads model configuration from `model_config.yaml` and makes requests via the OpenAI-compatible interface. First, configure the Step API in `model_config.yaml`:

```yaml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
stepfun:
  api_base: "https://api.stepfun.ai/v1"
  api_key: "YOUR_STEP_API_KEY"
```

Then in `examples/run_single_task_state_compress.py`, point the model provider at `stepfun` and use `step-3.7-flash`:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
local_model_config = {
    "task_type": "parser_0920_summary_adv_state_compress",
    "model_config": {
        "model_name": "step-3.7-flash",
        "model_provider": "stepfun",
        "args": {
            "temperature": 1,
            "top_p": 0.95,
            "frequency_penalty": 0.05,
            "max_tokens": 32768,
        },
    },
    "config": {
        "enable_state_compression": True,
        "state_compression_interval": 10,
        "state_compression_recent_window": 10,
        "state_compression_max_field_items": 10,
    },
    "max_steps": 400,
    "delay_after_capture": 3,
    "debug": False,
}
```

<Note>
  The GELab-Zero minimal-run guide recommends keeping `temperature` at `1` — don't change it to `0.1` or `0.5`. For long-horizon tasks, enable state compression to prevent the history context from growing unbounded.
</Note>

## Run a mobile task

Confirm the phone is still online:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
adb devices
```

Then run a single task:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
python examples/run_single_task_state_compress.py \
  --task "Show me what's trending on Weibo entertainment hot search and give me a summary"
```

If multiple devices are connected, specify the device explicitly:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
python examples/run_single_task_state_compress.py \
  --device-id AN2CVB4C28000731 \
  --task "Show me what's trending on Weibo entertainment hot search and give me a summary"
```

After running, the terminal prints the `Session ID`, per-step duration, current action, and total elapsed time. Task logs are written by default to:

* `running_log/server_log/os-copilot-local-eval-logs/traces`
* `running_log/server_log/os-copilot-local-eval-logs/images`

## Review the run

GELab-Zero ships a local visualization UI for inspecting each step's screenshot, model thinking, and action result:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
streamlit run visualization/pages/main_page.py \
  --server.address 127.0.0.1 \
  --server.port 33503
```

Open:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
http://localhost:33503
```

Copy the `Session ID` from the task terminal and paste it into the page's input box to replay the entire run.

## Reference

<Card title="GELab-Zero minimal-run guide" href="https://github.com/stepfun-ai/gelab-zero/blob/main/%E6%9E%81%E7%AE%80%E8%BF%90%E8%A1%8C%E6%8C%87%E5%8D%97_CN.md">
  Android device setup, State Compress entry points, recommended parameters, and visualization usage.
</Card>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.