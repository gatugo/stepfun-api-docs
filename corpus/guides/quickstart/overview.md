> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

export const StepQuickstartPage = ({children}) => <div className="step-quickstart-page">{children}</div>;

<StepQuickstartPage>
  This guide provides a common set of API examples. Select a model ID from the table, then use the tabs below to switch between text chat, image understanding, and video understanding.

  ## Choose a model ID

  | Model | Model ID | Input capabilities |
  | :- | :- | :- |
  | Step 5 Preview | `step-5-preview` | Text, images, and video |
  | Step 3.7 Flash | `step-3.7-flash` | Text, images, and video |
  | Step 3.5 Flash | `step-3.5-flash` | Text only |

  Replace `YOUR_MODEL_ID` in the examples below with one of the model IDs in the table, and replace `YOUR_STEP_API_KEY` with your API key.

  Throughout the docs, `YOUR_STEP_API_KEY` is a placeholder to replace, not a real credential. Names such as `STEP_API_KEY` and `STEPFUN_API_KEY` are variables used by examples or tools: `export STEPFUN_API_KEY="YOUR_STEP_API_KEY"` sets a variable, and `Bearer $STEPFUN_API_KEY` reads its value. Keep variable names consistent within an example and preserve the configuration field names required by each tool.

  ## Get an API key

  Sign in to the [StepFun Open Platform](https://platform.stepfun.ai/) and create and copy an API key on the [Interface Keys](https://platform.stepfun.ai/interface-key) page.

  ## Set up your environment

  ### Install the Python dependency

  The Python examples use the OpenAI SDK:

  <Tabs>
    <Tab title="macOS / Linux">
      ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
      python3 -m pip install --upgrade "openai>=1.0"
      ```
    </Tab>

    <Tab title="Windows">
      ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
      py -m pip install --upgrade "openai>=1.0"
      ```
    </Tab>
  </Tabs>

  ## Send a request

  <Tabs>
    <Tab title="Text chat">
      This example works with all three models. Replace `YOUR_MODEL_ID` with the model you want to call.

      <Tabs>
        <Tab title="Python">
          ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from openai import OpenAI

          client = OpenAI(
              api_key="YOUR_STEP_API_KEY",
              base_url="https://api.stepfun.ai/v1",
          )

          response = client.chat.completions.create(
              model="YOUR_MODEL_ID",
              messages=[
                  {"role": "user", "content": "Hello, please introduce yourself in one sentence."}
              ],
          )

          print(response.choices[0].message.content)
          ```
        </Tab>

        <Tab title="cURL">
          ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          curl https://api.stepfun.ai/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer YOUR_STEP_API_KEY" \
            -d '{
              "model": "YOUR_MODEL_ID",
              "messages": [
                {
                  "role": "user",
                  "content": "Hello, please introduce yourself in one sentence."
                }
              ]
            }'
          ```
        </Tab>
      </Tabs>
    </Tab>

    <Tab title="Image understanding">
      Step 5 Preview and Step 3.7 Flash support image input. Step 3.5 Flash does not support image input; use a model that supports images instead.

      <Tabs>
        <Tab title="Python">
          ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from openai import OpenAI

          client = OpenAI(
              api_key="YOUR_STEP_API_KEY",
              base_url="https://api.stepfun.ai/v1",
          )

          response = client.chat.completions.create(
              model="YOUR_MODEL_ID",
              messages=[{
                  "role": "user",
                  "content": [
                      {"type": "text", "text": "Extract the key information from this image and summarize the main conclusions."},
                      {
                          "type": "image_url",
                          # Replace this placeholder with the URL of your own accessible image.
                          "image_url": {"url": "https://example.com/image.jpg"},
                      },
                  ],
              }],
          )

          print(response.choices[0].message.content)
          ```
        </Tab>

        <Tab title="cURL">
          ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          # Replace this placeholder with the URL of your own accessible image.
          curl https://api.stepfun.ai/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer YOUR_STEP_API_KEY" \
            -d '{
              "model": "YOUR_MODEL_ID",
              "messages": [{
                "role": "user",
                "content": [
                  {"type": "text", "text": "Extract the key information from this image and summarize the main conclusions."},
                  {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image.jpg"}
                  }
                ]
              }]
            }'
          ```
        </Tab>
      </Tabs>
    </Tab>

    <Tab title="Video understanding">
      Step 5 Preview and Step 3.7 Flash support video input through `video_url`. Step 3.5 Flash does not support video input; use a model that supports video instead.

      <Tabs>
        <Tab title="Python">
          ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from openai import OpenAI

          client = OpenAI(
              api_key="YOUR_STEP_API_KEY",
              base_url="https://api.stepfun.ai/v1",
          )

          response = client.chat.completions.create(
              model="YOUR_MODEL_ID",
              messages=[{
                  "role": "user",
                  "content": [
                      {"type": "text", "text": "Summarize the main content of this video in chronological order."},
                      {
                          "type": "video_url",
                          # Replace this placeholder with the URL of your own accessible video.
                          "video_url": {"url": "https://example.com/video.mp4"},
                      },
                  ],
              }],
          )

          print(response.choices[0].message.content)
          ```
        </Tab>

        <Tab title="cURL">
          ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          # Replace this placeholder with the URL of your own accessible video.
          curl https://api.stepfun.ai/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer YOUR_STEP_API_KEY" \
            -d '{
              "model": "YOUR_MODEL_ID",
              "messages": [{
                "role": "user",
                "content": [
                  {"type": "text", "text": "Summarize the main content of this video in chronological order."},
                  {
                    "type": "video_url",
                    "video_url": {"url": "https://example.com/video.mp4"}
                  }
                ]
              }]
            }'
          ```
        </Tab>
      </Tabs>
    </Tab>
  </Tabs>

  ## Read the response

  For a non-streaming request, generated content is available in `choices[0].message.content`:

  ```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  {
    "model": "YOUR_MODEL_ID",
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "The model's response"
        },
        "finish_reason": "stop"
      }
    ]
  }
  ```

  The full response also includes the request ID, token usage, and other fields. See the [Chat Completions API](/docs/en/api-reference/chat/chat-completion-create) for details.

  If a request fails, use the returned error information and refer to the [error codes](/docs/en/api-reference/error-codes) documentation.

  ## Explore further

  <Columns cols={2}>
    <Card title="Model capability overview" href="/docs/en/guides/models/overview">
      Compare the positioning and capabilities of Step 5 Preview, Step 3.7 Flash, and Step 3.5 Flash.
    </Card>

    <Card title="Image understanding best practices" href="/docs/en/guides/developer/image-chat">
      Learn about image formats, input methods, and parameter recommendations.
    </Card>

    <Card title="Video understanding best practices" href="/docs/en/guides/developer/video-chat">
      Learn about video input methods, limits, and common issues.
    </Card>

    <Card title="API reference" href="/docs/en/api-reference/chat/chat-completion-create">
      See the complete request parameters, response fields, and usage information.
    </Card>
  </Columns>
</StepQuickstartPage>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.