> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Image Model Retirement Notice

`step-2x-large` and `step-image-edit-2` will be retired on **October 10, 2026**; `step-1x-edit` is no longer available. Starting October 10, 2026, the text-to-image, image-to-image, and image editing APIs will stop serving requests. Applications that continue calling these APIs will not receive valid responses.

<Warning>
  Please complete the required business changes before **October 10, 2026** to keep your production services running.
</Warning>

## Retirement details

| Item | Details |
| - | - |
| Retirement date | October 10, 2026 |
| Models | `step-2x-large` and `step-image-edit-2` (available before October 10, 2026); `step-1x-edit` (no longer available) |
| Capabilities | Text-to-image, image-to-image, and image editing |

## Affected APIs and impact

The following Open Platform API and Step Plan image APIs will stop serving requests on **October 10, 2026**:

| Service | Capability | Method | Endpoint |
| - | - | - | - |
| Open Platform API | Text-to-image | POST | `/v1/images/generations` |
| Open Platform API | Image-to-image | POST | `/v1/images/image2image` |
| Open Platform API | Image editing | POST | `/v1/images/edits` |
| Step Plan | Text-to-image | POST | `/step_plan/v1/images/generations` |
| Step Plan | Image editing | POST | `/step_plan/v1/images/edits` |

* **Open Platform API and Step Plan**: The image APIs above will stop serving requests. Other Step Plan models, including text, reasoning, speech, and smart routing models, are not affected.
* **Studio**: Image generation will no longer be available.

## Frequently asked questions

<AccordionGroup>
  <Accordion title="Can these models still be called before retirement?">
    `step-2x-large` and `step-image-edit-2` can still be called before **October 10, 2026**; `step-1x-edit` is no longer available. Starting October 10, 2026, the Open Platform API and Step Plan image APIs will stop serving requests, and continued calls will not receive valid responses.
  </Accordion>

  <Accordion title="Can step-1x-edit still be called?">
    No. `step-1x-edit` is no longer available. `step-2x-large` and `step-image-edit-2` remain available until October 10, 2026.
  </Accordion>

  <Accordion title="Can I still access images that have already been generated?">
    Image download links have their own validity limits, which are unrelated to this retirement. Download and store any images that need to be retained long term in your own storage service.
  </Accordion>
</AccordionGroup>

For additional help, see the [FAQ](/docs/en/faq/common-questions).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.