> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# List models

Shows all available models, including creation time and owner.

## Endpoint

`GET https://api.stepfun.ai/v1/models`

## Request parameters

None.

## Response

Returns a list of [Model objects](/docs/en/api-reference/models/object).

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    print(client.models.list())
    ```
  </Tab>

  <Tab title="js">
    ```js theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    import OpenAI from "openai";

    const openai = new OpenAI({
        apiKey: "YOUR_STEP_API_KEY",
        baseURL: "https://api.stepfun.ai/v1"
    });

    async function main() {
        const list = await openai.models.list();

        for await (const model of list) {
            console.log(model);
        }
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/models \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "object": "list",
  "data": [
    {
      "id": "step-5-preview",
      "object": "model",
      "created": 1789747200,
      "owned_by": "stepai"
    },
    {
      "id": "stepaudio-2.5-tts",
      "object": "model",
      "created": 1776089669,
      "owned_by": "stepai"
    }
  ]
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.