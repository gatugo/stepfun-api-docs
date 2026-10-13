> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Step Image Edit 2

<Note>
  `step-image-edit-2` will be retired on October 10, 2026, and its text-to-image and image editing APIs will stop serving requests. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

StepFun's latest lightweight editing model. A single model supports both **text-to-image** and **image editing**. Within the under-6B parameter range, it sets a performance benchmark in its tier and competes cross-tier with 12B-20B open-source large models. Each editing task takes only 1-2 seconds, redefining real-time interactive image editing.

<Columns cols={2}>
  <Card title="Showcase" icon="image" href="#showcase">
    See official sample prompts and generated results.
  </Card>

  <Card title="API quickstart" icon="rocket" href="#quickstart">
    View minimal runnable curl examples.
  </Card>
</Columns>

## Key information

<Columns cols={3}>
  <Card title="Parameters">
    Under 6B<br />Lightweight generation and editing
  </Card>

  <Card title="Prompt length">
    512 characters
  </Card>

  <Card title="Input image limit">
    4096x4096<br />(image editing scenarios)
  </Card>
</Columns>

## Core capabilities

<Columns cols={3}>
  <Card title="🏆 Benchmark performance at lightweight scale">
    Focused on maximizing performance within the under-6B parameter range. Demonstrates exceptional editing capability, currently the strongest image-editing model at this parameter level.
  </Card>

  <Card title="🚀 High intelligence density and cross-tier superiority">
    Optimized architecture for parameter efficiency. With a smaller footprint, it surpasses 12B-20B open-source large models cross-tier. In general editing and reference editing, it matches top-tier closed-source domestic models.
  </Card>

  <Card title="⚡ Sub-second response, real-time interaction">
    Deep architectural optimization yields a qualitative leap in inference speed: 1-2 seconds per editing task. This near-zero latency removes the long-standing bottleneck of large models in real-time interactive image editing.
  </Card>
</Columns>

## API endpoints

<Columns cols={2}>
  <Card title="Text-to-image" href="/docs/en/api-reference/images/image">
    `POST /v1/images/generations`<br />Generate an image from a prompt.
  </Card>

  <Card title="Image editing" href="/docs/en/api-reference/images/edits">
    `POST /v1/images/edits`<br />Modify an image based on input image and prompt.
  </Card>
</Columns>

## Pricing

| Item | Price |
| :- | :- |
| Text-to-image / Image editing | **\$0.003 / image** |

[View full pricing details →](/docs/en/guides/pricing/details)

## Quickstart

<Tabs>
  <Tab title="Text-to-image (curl)">
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

    Supported sizes for text-to-image: `1024x1024`, `768x1360`, `896x1184`, `1360x768`, `1184x896` (format is `height x width`).
  </Tab>

  <Tab title="Image editing (curl)">
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

    For image editing, the result image is returned at the same size as the input image.
  </Tab>
</Tabs>

<Info>`text_mode` is an optimization strategy for text-rendering scenarios; off by default, enable as needed. When `cfg_scale = 1.0`, `negative_prompt` is not passed to the underlying model.</Info>

## Showcase

### Text-to-image

<AccordionGroup>
  <Accordion title="Wide-angle landscape photography">
    <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/t2i-01-landscape.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=f6d0492e5517d4812e3dc647842ef723" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/t2i-01-landscape.png" />

    **Prompt**: A breathtaking wide-angle landscape photograph. A crystal-clear alpine lake serves as a perfect mirror. Towering snow-capped mountains pierce an azure sky dotted with wisps of cloud. On the lakeside slopes, autumn aspens display splendid golden hues. The water reflects mountains, trees and sky with sharp clarity. Hyperrealistic, 8K resolution, National Geographic style, vivid colors, serene atmosphere.
  </Accordion>

  <Accordion title="Cinematic portrait">
    <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/t2i-02-girl.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=ad9b608aa89124db8d90fb869add1e20" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/t2i-02-girl.png" />

    **Prompt**: High-angle cinematic portrait, a young girl standing at a vintage cobblestone street corner during sunset. Long brown hair lifted by the evening breeze, wearing a vintage white floral puff-sleeve dress. Visible details on facial features, hair strands and fabric texture. Subject-centered composition with softly blurred background of old buildings, wooden windows and warm-toned walls as ambiance. Golden-hour sunlight wraps her side profile and shoulders; hair tips and dress edges glow with a faint golden halo. Nostalgic, innocent, quiet summer-evening mood. 35mm film, Kodak Portra 400 tones, soft bloom, shallow depth of field, cinematic portrait, photorealistic.
  </Accordion>

  <Accordion title="Minimalist still life photography">
    <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/t2i-03-vase.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=28934710af494538aca801c2a9777717" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/t2i-03-vase.png" />

    **Prompt**: A minimalist still-life photograph. Centered: a deep-blue glossy glass vase holding a bouquet of vibrant golden tulips. The vase rests on a textured pale-white tabletop against a pure white wall. Strong afternoon sunlight streams in from the side, casting clear, elongated, artistic shadows of leaves and flowers on the wall. High contrast of light and shadow, pure colors, tranquil and warm atmosphere. High quality, 8K resolution.
  </Accordion>

  <Accordion title="Classical oil-painting still life">
    <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/t2i-04-still-life.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=f18eec0bbcc55a1867d45a0b81eae1e6" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/t2i-04-still-life.png" />

    **Prompt**: A classical oil-painting still life, Dutch Golden Age style. Center: a transparent glass vase filled with colorful tulips, lilies and purple flowers (orange, pink, purple). Beside it, a white ceramic teapot and exquisite teacups. The dark wooden foreground table is draped with a flowing green-and-white striped silk cloth. Cut lemons, lemon peel, several cups of tea and scattered petals on the tabletop. Background: a deep textured wall, with a butterfly fluttering near the flowers. Soft, delicate light and shadow, rich detail, heavy oil-painting brushstrokes.
  </Accordion>
</AccordionGroup>

### Image editing

<AccordionGroup>
  <Accordion title="Pose change / dialogue bubble">
    **Prompt**: Make the cat lie on its back showing its belly. Add a dialogue bubble next to it that says "I was wrong".

    | Input | Result |
    | :-: | :-: |
    | <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/edit-01-cat-before.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=2d93863cdfd92f789662e137527958ee" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/edit-01-cat-before.png" /> | <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/edit-01-cat-after.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=b30551f0acc1fcb1d71e43cacfcb7702" alt="" width="1024" height="1024" data-path="images/guide/step-image-edit-2/edit-01-cat-after.png" /> |
  </Accordion>

  <Accordion title="Outfit replacement">
    **Prompt**: Change the man into a suit and shirt, and the woman into a beautiful Western wedding dress with a veil. Both face the camera directly.

    | Input | Result |
    | :-: | :-: |
    | <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/edit-02-couple-before.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=528d232ef19848907ab1fb4cb7cbc9d4" alt="" width="683" height="1024" data-path="images/guide/step-image-edit-2/edit-02-couple-before.png" /> | <img src="https://mintcdn.com/stepfun2/s4l-pPPVlINO6zWj/images/guide/step-image-edit-2/edit-02-couple-after.png?fit=max&auto=format&n=s4l-pPPVlINO6zWj&q=85&s=b19b49ef2cbba82ee4aeb1c9aa8b68b2" alt="" width="683" height="1024" data-path="images/guide/step-image-edit-2/edit-02-couple-after.png" /> |
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.