> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# File object

Description of a single File object.

## Attributes

* `id` `string`<br />Unique File ID.
* `object` `string`<br />Object type, always `file`.
* `bytes` `int`<br />File size in bytes.
* `created_at` `int`<br />File creation time as a Unix timestamp (seconds).
* `filename` `string`<br />File name.
* `purpose` `string`<br />Upload purpose. Only `storage` is supported for file uploads.
* `status` `string`<br />Processing status: `success` or `processed`.

## Example

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "id": "file-abc123",
    "object": "file",
    "bytes": 140,
    "created_at": 1613779121,
    "filename": "productImage.png",
    "purpose": "storage",
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.