> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Image Generation & Editing Models

<Note>
  `step-2x-large` and `step-image-edit-2` will be retired on October 10, 2026; `step-1x-edit` is no longer available. The text-to-image, image-to-image, and image editing APIs will stop serving requests. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

## Model overview

Our text-to-image models generate high-quality, diverse images from text prompts or other inputs. They are widely applicable for art, design, game development, and beyond.

We currently provide the step-1x and step-2x model series:

## Models

### step-2x-large

Our new-generation image model focused on text-to-image generation. Produces more realistic textures and stronger Chinese/English text rendering.

## Key terms

1. **Image resolution**: Pixel width/height of the output. Higher resolution gives more detail but increases generation time and compute.
2. **Image style**: Visual characteristics such as realistic, abstract, cartoon, etc.
3. **Prompt/description**: The text or reference image describing what to generate. More precise descriptions yield outputs closer to expectations.
4. **Model parameters**: Larger models capture more detail and produce higher-quality results. The step-1x line offers a 2B-parameter model.

## Usage limits

1. **Supported input**: Natural-language descriptions of desired content and style.
2. **Images per request**: step-1x models allow up to 1 image per request.
3. **Resolution limits**: Squares: `256x256`, `512x512`, `768x768`, `1024x1024`; 16:9: `1280x800`, `800x1280`.
4. **Generation time**: Varies with prompt complexity and model throughput.
5. **Quality**: Results depend on prompt specificity and training data; multiple attempts may be needed for the best output.
6. **Copyright and usage**: You own generated images but must not use them for illegal purposes or rights violations. Models are evolving, so evaluate and adjust for your scenario.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.