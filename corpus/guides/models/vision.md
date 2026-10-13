> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vision Models

## Model overview

Vision models add image and video input to our text models for more complete and accurate understanding and reasoning.

We currently offer the step series of vision models:

## Models

### Step 5 Preview

Recommended. StepFun’s flagship model for agentic work supports text, image, and video input with a 1M-token context window and three reasoning effort levels (low / medium / high). Use it for chart analysis, screenshot Q\&A, video summaries, and multimodal work across documents. See [Step 5 Preview](/docs/en/guides/models/step-5-preview).

### Step 3.7 Flash

Our high-speed multimodal reasoning model with **native image and video understanding** — no extra vision MCP or auxiliary model required. It handles image / video Q\&A and cross-modal analysis directly, with three reasoning effort levels (low / medium / high) and a 256K context window. See [Step 3.7 Flash](/docs/en/guides/models/step-3.7-flash).

## Key terms

1. **Image resolution**: Pixel width/height. Higher resolution conveys more detail but increases cost, latency, and transfer time. Keep longest side under 4096px.
2. **Image token count**: Depends on resolution; images are adaptively scaled to an optimal size.
3. **Supported formats**: JPG/JPEG, PNG, static GIF, WebP.
4. **URL formats**:
   * **http/https**: Must be accessible from mainland China; load time affects first-token latency.
   * **base64**: Follow RFC2394, e.g. `data:image/jpeg;base64,<base64_data_string>`.
   * **References**: [RFC2397](https://www.rfc-editor.org/rfc/rfc2397#section-2), [Data URL Format](https://developer.mozilla.org/en-US/Web/HTTP/Basics_of_HTTP/Data_URLs)

## Usage limits

1. **Images per request**: Step 5 Preview supports up to 60 images per request, also subject to its context window. See the corresponding documentation for other models. For long conversations, summarize images first via a multimodal model, then pass the summaries as text.
2. **Total image size**: Keep combined uploads within 20MB.
3. **Image metadata**: Metadata (path, filename, size, original resolution, author, camera model, location, etc.) is stripped before inference to protect privacy; images are also resized to optimal dimensions.
4. **Small text**: Tiny fonts may reduce recognition quality.
5. **Rotation/cropping**: Incomplete or misaligned images can hurt recognition.
6. **Counting**: Numeric outputs are estimates, not exact counts.
7. **Accuracy**: Descriptions or captions may be imperfect; avoid relying on outputs where errors have serious consequences.

## Quickstart

<Columns cols={2}>
  <Card title="Migrate from OpenAI" href="/docs/en/guides/developer/openai">
    Reuse OpenAI-compatible SDK patterns to adopt Stepfun vision models quickly.
  </Card>

  <Card title="Image understanding" href="/docs/en/guides/developer/image-chat">
    Send images in the conversation and build grounded multimodal interactions.
  </Card>

  <Card title="Video understanding" href="/docs/en/guides/developer/video-chat">
    Pass video links to the model so it can read and reason over video content.
  </Card>

  <Card title="Multi-turn conversations" href="/docs/en/guides/developer/multiple-round">
    Maintain context over multiple turns for continuous multimodal conversations.
  </Card>

  <Card title="JSON Mode" href="/docs/en/guides/developer/json-mode">
    Return structured JSON outputs for downstream application workflows.
  </Card>

  <Card title="Streaming responses" href="/docs/en/guides/developer/stream">
    Stream output progressively to improve perceived latency in the UI.
  </Card>

  <Card title="Tool Call" href="/docs/en/guides/developer/tool-call">
    Combine model reasoning with tools, functions, and external data sources.
  </Card>

  <Card title="Prompt cache" href="/docs/en/guides/developer/prompt-cache">
    Cache repeated context to optimize longer or repeated multimodal requests.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.