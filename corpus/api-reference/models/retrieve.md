> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get a single model

Retrieve metadata for a model, including creation time and owner.

## Endpoint

`GET https://api.stepfun.ai/v1/models/{model}`

## Path parameters

* `model` `string` ***required***
  <br />
  Model ID.

## Response

Returns a single [Model object](/docs/en/api-reference/models/object).

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    print(client.models.retrieve("step-5-preview"))
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
        const model = await openai.models.retrieve("step-5-preview");

        console.log(model);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/models/step-5-preview \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "step-5-preview",
  "object": "model",
  "created": 1789747200,
  "owned_by": "stepai"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.