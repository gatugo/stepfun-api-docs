> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# List files

List all available files for the current user.

## Endpoint

`GET https://api.stepfun.ai/v1/files`

## Request parameters

None.

## Response

Returns a list of [File objects](/docs/en/api-reference/files/object).

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    client.files.list()
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
        const list = await openai.files.list();

        for await (const file of list) {
            console.log(file);
        }
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/files \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "data": [
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 175,
      "created_at": 1613677385,
      "filename": "productImage.png",
      "purpose": "storage",
      "status": "processed"
    },
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 140,
      "created_at": 1613779121,
      "filename": "intro.mp4",
      "purpose": "storage",
      "status": "processed"
    }
  ],
  "object": "list"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.