> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retrieve file content

Retrieve the parsed content of a file. Only files with `purpose=file-extract` are supported.

## Endpoint

`GET https://api.stepfun.ai/v1/files/{file_id}/content`

## Path parameters

* `file_id` `string` ***required***
  <br />
  Unique file ID.

## Response

Returns the file's parsed content as plain text.

## Example

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    content = client.files.content("file-abc123")
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
        const file = await openai.files.content("file-abc123");

        console.log(file);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/files/file-abc123/content \
      -H "Authorization: Bearer $STEP_API_KEY"
    ```
  </Tab>
</Tabs>

```text filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
File content
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.