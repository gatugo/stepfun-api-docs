> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Image editing

<Note>
  The image editing API will no longer be available after October 10, 2026. `step-image-edit-2` will be retired on that date. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

Modify an image based on a user-provided image and prompt.

### Endpoint

`POST https://api.stepfun.ai/v1/images/edits`

### Request parameters

* `model` `string` ***required***<br />The model name to use. Currently supported:
  * `step-image-edit-2`

* `image` `file` ***required***<br />The input image file. Currently only one image is supported.
  * `step-image-edit-2`: maximum input resolution 4096x4096; supports base64-encoded image input.

* `prompt` `string` ***required***<br />Text description for the edit. Maximum length: 512 characters.

* `seed` `int` ***optional***<br />Random seed.
  * `step-image-edit-2`: range `[0, 2147483647]`. If not provided, the server randomly generates a seed.

* `steps` `int` ***optional***<br />Number of generation steps.
  * `step-image-edit-2`: range `[1, 50]`. Default 8.

* `cfg_scale` `float` ***optional***<br />Classifier-free guidance scale.
  * `step-image-edit-2`: must be >= 1.0, range `[1.0, 10.0]`. Default 1.0.

* `size` `string` ***optional***<br />
  * `step-image-edit-2`: this parameter is ignored for editing; the result image is returned at the same size as the input image.

* `negative_prompt` `string` ***optional***<br />Negative prompt. Up to 512 characters, default `""`. When `cfg_scale = 1.0`, the current implementation does not pass the negative prompt to the underlying model.

* `text_mode` `bool` ***optional***<br />Optimization strategy for text-rendering scenarios. Default `False`, enable as needed.

* `response_format` `string` ***optional***<br />Format of the returned image. Supported: `b64_json` or `url`. Default `url`.

### Response

* `created` `int`<br />Timestamp of when the image was created (seconds).
* `data` `object array`<br />Array of generated image objects.
  * `seed` `int`<br />The seed used during generation.
  * `finish_reason` `string`<br />Reason for completion. `success` indicates successful generation; `content_filtered` indicates successful generation but stopped due to content filtering.
  * `b64_json` `string`<br />Base64-encoded image. Returned when `response_format` is `b64_json`.
  * `url` `string`<br />Image download URL. Returned when `response_format` is `url`. The URL has a limited validity period (currently 2 hours); download and save the image to your own storage to avoid relying on this link.

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST "https://api.stepfun.ai/v1/images/edits" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -F 'model=step-image-edit-2' \
      -F 'image=@input.webp' \
      -F 'prompt=Make the character ride a bicycle, holding a sign that says "Saudi Arabia"' \
      -F 'response_format=b64_json' \
      -F 'cfg_scale=1.0' \
      -F 'steps=8' \
      -F 'seed=1' \
      -F 'text_mode=true'
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.