> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Step 3.7 Flash Examples

`step-3.7-flash` lets you mix images, video, and text in a single conversation. It's well-suited to turning visual information from the real world into plans, tables, code drafts, or diagnostic findings. This page collects prompt templates for common scenarios to help you quickly decide how to shape your inputs and outputs for each task.

<Info>
  These examples focus on task design and output format. For how to call the API, see the [Quickstart](/docs/en/quickstart/overview). For details on image and video parameters, see [Image understanding best practices](/docs/en/guides/developer/image-chat) and [Video understanding best practices](/docs/en/guides/developer/video-chat).
</Info>

## Usage tips

* Be explicit about the output format: ask for a Markdown table, JSON, CSV rows, or a task list.
* Require evidence for key fields: for amounts, dates, chart values, or task owners, have the model cite the source or mark uncertainty.
* Don't let the model guess missing info: fields that are unclear should be `null`, empty strings, or "cannot confirm".
* For high-risk data such as finance, expenses, contracts, or medical info, always have a human review.

## Whiteboard to plan

Good for meeting whiteboards, sticky-note walls, hand-drawn flowcharts, project-discussion photos. The goal is to convert loose information into an actionable plan, not to transcribe word for word.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
This is a photo of a project-discussion whiteboard. Please:
1. Extract the main topics and conclusions on the whiteboard.
2. Organize them into a project plan with goals, key milestones, risks, and items needing confirmation.
3. Generate a task list with fields: task, owner (null if not determinable), priority, dependencies, suggested due date.
4. Separately list anything that is unclear or needs human confirmation.
```

Suggested output:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
## Project plan
## Task list
## Risks and dependencies
## Items to confirm
```

## Chart to data

Good for report screenshots, dashboard screenshots, bar charts, line charts, pie charts. The goal is to convert chart content into structured data while keeping track of uncertainty.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Extract data from this chart and return it as JSON:
{
  "chart_type": "",
  "title": "",
  "x_axis": "",
  "y_axis": "",
  "series": [
    {
      "name": "",
      "points": [
        {"label": "", "value": null, "confidence": "high|medium|low"}
      ]
    }
  ],
  "insights": [],
  "uncertain_fields": []
}

Requirements:
- If a value can only be estimated, mark confidence as low or medium.
- Do not fabricate information that isn't in the chart.
- If axes, units, or legend are unclear, put them in uncertain_fields.
```

<Note>
  Chart screenshots can be affected by resolution, compression, and axis scaling. When you need exact numbers, prefer the original data source. The model's extraction is best treated as a first draft or as assistance for manual entry.
</Note>

## Receipt to table

Good for receipts, invoices, expense reports, shopping slips. The goal is to convert the document into structured row data that can be pasted directly into a spreadsheet or piped into a system.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Extract structured information from this receipt and return it as JSON:
{
  "merchant": "",
  "date": "",
  "currency": "",
  "total_amount": null,
  "tax_amount": null,
  "items": [
    {
      "name": "",
      "quantity": null,
      "unit_price": null,
      "amount": null
    }
  ],
  "payment_method": "",
  "uncertain_fields": []
}

Requirements:
- Amounts must come from the receipt itself; do not infer.
- Fields that are unclear should be null and written into uncertain_fields.
- Preserve the original currency and date format.
```

If you want to paste directly into a spreadsheet, have the model output CSV instead:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Output the line items in CSV with columns:
merchant,date,item_name,quantity,unit_price,amount,currency,confidence
```

## Screenshot to code

Good for web pages, mobile UIs, component screenshots, and design mockups. The goal is to produce an initial HTML / React / Tailwind draft you can iterate on.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
This is a screenshot of a web page. Use React + Tailwind CSS to recreate it.

Requirements:
1. First describe the page structure, layout, and main visual elements.
2. Then produce runnable React component code.
3. Use semantic naming; don't depend on real-world brand assets from the screenshot.
4. For images and icons you can't determine, use placeholder elements.
5. Keep the layout sensible on both mobile and desktop.
```

<Tip>
  If the screenshot contains a lot of text, have the model do a "page structure analysis" first, then ask it to generate code. This reduces missed layout details.
</Tip>

## Screen-recording diagnostics

Good for software-operation recordings, bug-repro videos, app usage paths, customer-support recordings. The goal is to reconstruct the user's actions, locate the anomaly, and provide debug guidance.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
This is a screen recording of someone using a piece of software. Analyze:
1. What actions did the user take, in order?
2. At which step did the anomaly begin?
3. What does the anomaly look like?
4. What are the likely causes, ordered by probability?
5. Suggested investigation steps and likely fixes.

Output in Markdown, and put anything unclear into a separate "Info needed" section.
```

Suggested output:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
## Action timeline
## Anomaly point
## Likely causes
## Investigation steps
## Info needed
```

## Multi-image comparison

Good for comparing design revisions, product photos, UI-state differences, scanned-page differences.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Compare these images and output:
1. Similarities.
2. Differences, grouped by visual layout, text content, data values, and state changes.
3. Possible impact.
4. Differences requiring human review.

If a difference can't be confirmed, say so explicitly — don't guess.
```

## Structured output tips

When you need to feed the result into a program or spreadsheet, ask for JSON or CSV explicitly and state your null policy:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Return valid JSON only — no Markdown.
If a field can't be confirmed from the image, set it to null.
For fields with uncertain recognition, add the field name and reason to uncertain_fields.
```

If downstream code needs strict JSON parsing, use `response_format` to enable JSON Mode. See [JSON Mode usage tips](/docs/en/guides/developer/json-mode) and [Chat Completions API](/docs/en/api-reference/chat/chat-completion-create#request-parameters).

For tasks that need human review, have the model emit `confidence` alongside values:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "field": "total_amount",
  "value": 128.5,
  "confidence": "medium",
  "evidence": "The 'Total' line at the bottom of the receipt"
}
```

## Next steps

<Columns cols={3}>
  <Card title="Quickstart" href="/docs/en/quickstart/overview">
    Learn the basics of calling images, video, Base64, and the Files API.
  </Card>

  <Card title="Chat Completions API" href="/docs/en/api-reference/chat/chat-completion-create">
    See `messages`, `image_url`, `video_url`, `reasoning_effort`, and other parameters.
  </Card>

  <Card title="Mobile Agent" href="/docs/en/guides/models/step-3.7-flash-mobile-agent">
    Connect to a real Android device via GELab-Zero and have the model plan mobile operations.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.