> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Migrate from OpenAI to StepFun

## Prerequisites

Stepfun models support both personal and enterprise use. Create an API key in the console and call with that key. For quick evaluation, you can also try models directly in the Experience Center.

## Model selection

Stepfun offers multiple model families. Choose the counterpart that best matches what you use today.

### Reasoning and multimodal models

* `step-5-preview`: flagship model for agentic work, with text, image, and video input and a 1M-token context window for software engineering, professional knowledge work, and multi-step tasks.
* `step-3.7-flash`: high-speed multimodal reasoning model. Native image and video understanding, three reasoning effort levels (low/medium/high) — well-suited to agent, coding, and multimodal workloads.
* `step-3.5-flash`: high-speed language reasoning model. Top-tier reasoning quality with fast, reliable execution — suitable for logical reasoning, math, software engineering, and deep research.

### Image generation

<Note>
  The image generation and image editing models will be retired on October 10, 2026, and the corresponding APIs will stop serving requests. See the [image model retirement notice](/docs/en/guides/image-offline-notice).
</Note>

* `step-image-edit-2`: unified text-to-image and image-editing model; a single edit completes in 1-2 seconds.

## API compatibility

Stepfun models are compatible with the OpenAI API spec. You can call them directly via the OpenAI SDK. If your app already uses an OpenAI SDK, migration requires minimal changes.

Supported OpenAI-compatible APIs:

* [Chat Completion](/docs/en/api-reference/chat/chat-completion-create)
* [Upload file](/docs/en/api-reference/files/create)
* [List files](/docs/en/api-reference/files/list)
* [Retrieve file info](/docs/en/api-reference/files/retrieve)
* Retrieve file content
* [Delete file](/docs/en/api-reference/files/delete)
* [List models](/docs/en/api-reference/models/list)
* [Retrieve a model](/docs/en/api-reference/models/retrieve)
* Generate images

## SDK migration guide

### OpenAI Python SDK

Replace `api_key` with your Stepfun API key and add `base_url="https://api.stepfun.ai/v1"`. Set the model name to a Stepfun model.

```python copy theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
# Before
client = OpenAI(
    api_key="OPENAI_KEY"
)

# After
client = OpenAI(
    api_key="YOUR_STEP_API_KEY",
    base_url="https://api.stepfun.ai/v1"
)
```

### OpenAI TypeScript SDK

Replace `apiKey` with your Stepfun API key and add `baseURL: "https://api.stepfun.ai/v1"`. Set the model name to a Stepfun model.

```typescript copy theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
// Before
const openai = new OpenAI({
	apiKey: 'OPENAI_KEY',
})

// After
const openai = new OpenAI({
	apiKey: 'YOUR_STEP_API_KEY',
	baseURL: 'https://api.stepfun.ai/v1',
})
```

### LangChain

When using LangChain, update `openai_api_key`, `openai_api_base`, and `model_name` in `ChatOpenAI` to switch to Stepfun.

```python copy theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from os import getenv
from dotenv import load_dotenv

load_dotenv()

template = """You are the Stepfun assistant. Think step by step and answer based on the user's question: {question}"""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Before
# llm = ChatOpenAI(
#   openai_api_key=getenv("OPENAI_KEY"),
#   model_name="gpt-4o"
# )

# After
llm = ChatOpenAI(
  openai_api_key=getenv("STEP_API_KEY"),
  openai_api_base="https://api.stepfun.ai/v1",
  model_name="step-5-preview"
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "How can Stepfun models help employees be more productive?"

print(llm_chain.run(question))
```

### LangChain.js

For LangChain.js, update `modelName`, `openAIApiKey`, and `basePath` when initializing `ChatOpenAI`.

```typescript theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
// Before
const chat = new ChatOpenAI({
	modelName: 'gpt-4o',
	openAIApiKey: $OPENAI_KEY,
})

// After

const chat = new ChatOpenAI(
	{
		modelName: 'step-5-preview',
		openAIApiKey: $STEP_API_KEY,
	},
	{
		basePath: 'https://api.stepfun.ai/v1',
	},
)
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.