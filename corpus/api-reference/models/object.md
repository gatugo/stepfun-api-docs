> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Model object

Description of a single Model object.

## Attributes

* `id` `string`<br />Unique model ID.
* `created` `int`<br />Model creation time as a Unix timestamp (seconds).
* `object` `string`<br />Object type, always `model`.
* `owned_by` `string`<br />Owning organization.

## Example

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "step-5-preview",
  "object": "model",
  "created": 1789747200,
  "owned_by": "stepai"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.