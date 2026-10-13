> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete a file

Delete a previously uploaded file.

## Endpoint

`DELETE https://api.stepfun.ai/v1/files/{file_id}`

## Path parameters

* `file_id` `string` ***required***
  <br />
  Unique file ID.

## Response

Returns the deleted [File object](/docs/en/api-reference/files/object).

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    print(client.files.delete("file-stepabc"))
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
        const file = await openai.files.del("file-stepabc");
        console.log(file);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/files/file-abc123 \
      -X DELETE \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "file-stepabc",
  "object": "file",
  "deleted": true
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.