> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Upload a file

Upload a file to the file service.

## Endpoint

`POST https://api.stepfun.ai/v1/files`

## Request body

* `purpose` `string` ***required***<br />Upload intent. Only `storage` is supported for file uploads (image/video understanding, voice cloning, etc.).

* `url` `string` ***optional***<br /> Remote file URL. Supported formats match the `file` field. If both `file` and `url` are provided, `file` takes precedence.

* `file` `File` ***optional***<br /> File to upload. Each user can upload up to 1,000 files. Omit when using `url`.<br />
  `storage` supported formats (max 128 MB):
  * Video (mp4)
  * Images (jpg/jpeg, png, webp, static gif)
  * Audio (mp3, wav). For voice cloning, audio length should be 5–10 seconds.

## Response

Returns a single [File object](/docs/en/api-reference/files/object).

## Examples

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    client.files.create(
        file=open("productImage.png", "rb"),
        purpose="storage"
    )
    ```
  </Tab>

  <Tab title="js">
    ```js theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    import OpenAI from "openai";
    import fs from "fs";

    const openai = new OpenAI({
        apiKey: "YOUR_STEP_API_KEY",
        baseURL: "https://api.stepfun.ai/v1"
    });

    async function main() {
        const file = await openai.files.create({
            file: fs.createReadStream("productImage.png"),
            purpose: "storage"
        });

        console.log(file);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/files \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -F purpose="storage" \
      -F file="@productImage.png"
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "file-abc123",
  "object": "file",
  "bytes": 140,
  "created_at": 1613779121,
  "filename": "productImage.png",
  "purpose": "storage",
  "status": "processed"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.