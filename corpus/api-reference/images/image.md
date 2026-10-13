> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Generate images

<Note>
  The image generation API will no longer be available after October 10, 2026. `step-2x-large` and `step-image-edit-2` will be retired on that date. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

Generate images from a user-provided prompt.

### Endpoint

`POST https://api.stepfun.ai/v1/images/generations`

### Request parameters

* `model` `string` ***required***<br />The model name to use. Currently supported:
  * `step-image-edit-2`

* `prompt` `string` ***required***<br />Text description of the image. Maximum length: 512 characters.

* `size` `string` ***optional***<br />The size of the generated image. Default `1024x1024`.
  * `step-image-edit-2` (format is `height x width`, not `width x height`):
    * Square: 1024x1024
    * Rectangular: 768x1360, 896x1184, 1360x768, 1184x896

* `n` `int` ***optional***<br />Number of images to generate. Currently only one image per request is supported.

* `response_format` `string` ***optional***<br />Format of the returned image. Supported: `b64_json` or `url`. Default `url`.

* `seed` `int` ***optional***<br />Random seed.
  * `step-image-edit-2`: range `[0, 2147483647]`. If not provided, the server randomly generates a seed.

* `steps` `int` ***optional***<br />Number of generation steps.
  * `step-image-edit-2`: range `[1, 50]`. Default 8.

* `cfg_scale` `float` ***optional***<br />Classifier-free guidance scale.
  * `step-image-edit-2`: must be >= 1.0, range `[1.0, 10.0]`. Default 1.0.

* `negative_prompt` `string` ***optional***<br />Negative prompt. Up to 512 characters, default `""`. When `cfg_scale = 1.0`, the current implementation does not pass the negative prompt to the underlying model.

* `text_mode` `bool` ***optional***<br />Optimization strategy for text-rendering scenarios. Default `False`, enable as needed.

### Response

* `created` `int`<br />Timestamp of when the image was created (seconds).
* `data` `object array`<br />Array of generated image objects.
  * `seed` `int`<br />The seed used during generation. Same seeds produce similar images.
  * `finish_reason` `string`<br />Reason for completion. `success` indicates successful generation; `content_filtered` indicates successful generation but stopped due to content filtering.
  * `b64_json` `string`<br />Base64-encoded image. Returned when `response_format` is `b64_json`.
  * `url` `string`<br />Image download URL. Returned when `response_format` is `url`. The URL has a limited validity period (currently 2 hours); download and save the image to your own storage to avoid relying on this link.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "created": 1589478378,
  "data": [
    {
      "b64_json": "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1",
      "finish_reason": "success",
      "seed": 123838
    }
  ]
}
```

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/images/generations \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "model": "step-image-edit-2",
        "prompt": "A serene alpine lake at sunset, mirror reflection, photorealistic",
        "response_format": "b64_json",
        "cfg_scale": 1.0,
        "steps": 8,
        "seed": 1,
        "text_mode": true
      }'
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.