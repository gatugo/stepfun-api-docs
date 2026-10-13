> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Core Concepts

## Reasoning models

> Reasoning models like `step-5-preview` are designed for tasks requiring deep logical analysis, multi-step problem solving, and long-context reasoning.

**Reasoning models excel at:**

* **Complex Logic**: Breaking down intricate problems into manageable steps.
* **Mathematics & Coding**: Solving advanced equations and debugging software.
* **Long-context Agents**: Maintaining stability and reasoning over massive datasets.

See [Reasoning Model](/docs/en/guides/models/reasoning) for model details.

## Audio models

> Audio models such as `stepaudio-2.5-tts` convert text into natural speech and support voice cloning.

**Audio models can be used for tasks including, but not limited to:**

* **Voice assistants**: customer service and smart speakers.
* **Audiobooks and podcasts**: text narration with consistent voice.
* **Games and NPCs**: character voices at scale.
* **Media production**: quick voiceover drafts.

See [Audio Models](/docs/en/guides/models/audio) for model details and [Generate audio](/docs/en/api-reference/audio/create-audio) for the API.

## Context length

> **Context length** is the amount of input text a model considers when generating or predicting. It limits how much information the model processes in a single request.

**Why it matters**

* **Quality**: Context length governs how much the model can remember and use, affecting understanding and generation.
* **Performance**: Larger contexts can improve accuracy but also increase compute cost.
* **Cost**: Longer contexts may help in certain scenarios but raise usage costs, so balance quality and spend.

**Where it applies**

* **Chat systems**: affects coherence and context retention across turns.
* **Creative writing**: longer contexts can produce more coherent, logical narratives.
* **Research papers**: helps the model digest background, data, and detailed discussion.
* **Novels and literature**: captures plot progression and character relationships.

## Token

> A token is the basic unit of text a model processes. It can be a character, word, phrase, or sentence depending on the tokenizer and training data. In Chinese, tokenization is especially important because words are not separated by spaces.

**Token length**

* **Chinese characters vs. tokens**: Roughly 1 token equals about 1.5–2 Chinese characters, though actual counts vary by content.

**Context limits**

* **Maximum context**: The combined input (prompt) and output must stay within the model’s context window.
* **Why the limit matters**: It keeps processing efficient and avoids errors from overly long text.

**Practical considerations**

* **Plan text length**: Fit your text within the maximum context so the model can process everything.
* **Optimize tokens**: Remove unnecessary tokens or reorganize text to stay within the limit.

## Rate limits

> Rate limits protect service stability and fairness by capping how many requests a user can make within a given time. Three main measures:

**RPM (requests per minute)**: Number of requests allowed per minute. If RPM is 20, you can make at most 20 requests in any rolling one-minute window.

**TPM (tokens per minute)**: Number of tokens you can send per minute across requests and responses. Many short requests may hit RPM before TPM.

**Concurrency (simultaneous requests)**: Number of in-flight requests. If the limit is 20, only 20 concurrent requests are allowed; new ones are rejected until earlier ones finish.

**When rate limits trigger**: Any one of the above can hit first. For example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
If your limits are RPM=20 and TPM=200K, and you send 20 requests to ChatCompletions with 100 tokens each,
TPM is still under 200K, but hitting 20 requests triggers the RPM limit.
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.