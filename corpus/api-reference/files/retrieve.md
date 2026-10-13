> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get a single file

Retrieve metadata for a single File, including creation time and organization.

## Endpoint

`GET https://api.stepfun.ai/v1/files/{file_id}`

## Path parameters

* `file_id` `string` ***required***
  <br />
  Unique file ID.

## Response

Returns a single [File object](/docs/en/api-reference/files/object).

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    print(client.files.retrieve("file-stepab"))
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
        const file = await openai.files.retrieve("file-stepab");

        console.log(file);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/files/file-abc \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "file-abc123",
  "object": "file",
  "bytes": 140,
  "created_at": 1613779121,
  "filename": "salesOverview.pdf",
  "purpose": "file-extract",
  "status": "success"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.