> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Model Lifecycle & Deprecations

This page maintains model retirement dates, status, replacements and migration paths. See [Model Overview](/docs/en/guides/models/overview) for capabilities and pricing links.

## Lifecycle Index

| Status | Effective date | Scope and migration |
| - | - | - |
| Retired | 2026-07-08 | Replacement table and migration steps below |
| Scheduled retirement | 2026-10-10 | [Image Model Deprecation](/docs/en/guides/image-offline-notice) |

## July 2026 Retirement Record

To continue improving model quality and service reliability, the following models were retired on **July 8, 2026** and no longer serve inference requests. Applications that still call them will not receive valid responses.

<Warning>
  If you still call any of the models below, replace the model, tune the relevant parameters, and complete full business validation as soon as possible to restore and protect your production services.
</Warning>

## Retired models and recommended replacements

The table below lists the models being retired and the recommended replacement for each. In most cases, migrating means replacing the `model` field in your request with the replacement model ID.

| Model being retired | Recommended replacement |
| - | - |
| `step-1-8k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-1-32k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-1v-8k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-1v-32k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-2-mini` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-1o-vision-32k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-2-16k` | [`step-1o-turbo-vision`](/docs/en/guides/models/vision) |
| `step-3` | [`step-3.7-flash`](/docs/en/guides/models/step-3.7-flash) |
| `step-1x-medium` | [`step-2x-large`](/docs/en/guides/models/image) |

<Note>
  The recommended replacement for `step-1x-medium` is `step-2x-large`. That interim replacement ended its limited-time free period on June 12, 2026 and is billed based on the number of images generated at **\$0.02 per image**. Because `step-2x-large` is scheduled for retirement on October 10, 2026, plan a follow-up migration for image-generation workloads.
</Note>

<Note>
  `step-2x-large` will be retired on October 10, 2026, and the text-to-image, image-to-image, and image editing APIs will stop serving requests. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

## How to migrate

1. Find the model you currently use in the table above and note its recommended replacement.
2. Replace the `model` field value in your API requests with the replacement model ID — for example, change `step-3` to `step-3.7-flash`.
3. Review the replacement model's capabilities on its model page (linked above) and its rates on [Pricing & Rate Limits](/docs/en/guides/pricing/details). We recommend running full validation before switching production traffic.

For new projects or upgrades involving software engineering, professional knowledge work, or multimodal input, also consider [Step 5 Preview](/docs/en/guides/models/step-5-preview), with text, image, and video input and a 1M-token context window. The table above preserves the original retirement migration mappings. Step 5 Preview does not replace image-generation or audio models; check parameters, prices, and account access and validate your workload before switching.

If you have questions, see the [FAQ](/docs/en/faq/common-questions) or contact [platform@stepfun.com](mailto:platform@stepfun.com).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.