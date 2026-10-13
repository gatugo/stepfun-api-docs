> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JSON Mode and JSON Schema structured outputs

StepFun models can drive application logic such as sentiment analysis, information extraction, and content scoring. [Step 5 Preview](/docs/en/guides/models/step-5-preview) supports both JSON Mode and JSON Schema structured outputs. Choose the format that fits your application.

## Choose an output format

| Mode | Request parameters | When to use it |
| - | - | - |
| JSON Mode | `response_format: {"type": "json_object"}` | You need parseable JSON without API-level constraints on specific fields or types |
| JSON Schema | `response_format.type: "json_schema"` with `json_schema.strict: true` | You need schema constraints on fields, types, and required properties |

Describing a structure or including a JSON Schema in the prompt can guide JSON Mode, but does not provide strict API-level schema constraints. For strict structure constraints, use the `json_schema` parameter rather than only including a schema in the prompt.

## JSON Schema: constrain structure through the API

The following approach applies to `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, and `step-3.5-flash-2603`.

Set `response_format.type` to `json_schema` and provide these fields in `response_format.json_schema`:

* `name`: The schema name.
* `strict`: Set to `true` to enable strict mode.
* `schema`: The expected JSON structure, including properties, types, and required fields.

This example uses `step-5-preview` to extract a person's name and age. The schema is passed directly through the API parameters; it does not need to be repeated in the prompt. Replace `YOUR_STEP_API_KEY` with your API key and set the `STEPFUN_API_KEY` environment variable before sending the request; `$STEPFUN_API_KEY` reads its value. These commands use Bash or Zsh and the pay-as-you-go API.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEPFUN_API_KEY="YOUR_STEP_API_KEY"

curl --silent --show-error --fail-with-body \
  https://api.stepfun.ai/v1/chat/completions \
  -H "Authorization: Bearer $STEPFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "step-5-preview",
    "messages": [{"role": "user", "content": "Extract the person: Wang Ming, age 28."}],
    "stream": false,
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "person",
        "strict": true,
        "schema": {
          "type": "object",
          "additionalProperties": false,
          "required": ["name", "age"],
          "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
          }
        }
      }
    },
    "max_tokens": 1024
  }'
```

`choices[0].message.content` is a string containing JSON. After parsing, an example result is:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{"name": "Wang Ming", "age": 28}
```

Here, `required` makes both fields mandatory, while `additionalProperties: false` disallows extra fields. Schema constraints do not guarantee factual or business-level correctness; validate the extracted values in your application. See the [Chat Completions API](/docs/en/api-reference/chat/chat-completion-create) for parameter details.

## JSON Mode: return parseable JSON

### How to use it

To use JSON Mode, do three things:

1. Explicitly request JSON in the system prompt and describe the expected structure. You can include a JSON Schema as prompt guidance, but this does not provide strict schema constraints.
2. Set `response_format` to `{ "type": "json_object" }` so the model returns parsable JSON.
3. Parse the result and validate it. Once it matches expectations, pass it into your business logic.

### Sample code

Here’s an example sentiment analyzer that returns JSON:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from openai import OpenAI

# Initialize Stepfun client
STEPFUN_KEY = "YOUR_STEP_API_KEY"

client = OpenAI(
    base_url="https://api.stepfun.ai/v1",
    api_key=STEPFUN_KEY
)

# Define the system prompt
system_prompt = """
You are a review analyst. Based on the user's input, identify sentiment and output the analysis result.
## Rules
1. If the review contains negative words, set emotion to negative.
2. If the review contains positive words, set emotion to positive.
3. If neither, set emotion to neutral.
## Positive words
- good
- great
- excellent
## Negative words
- bad
- terrible
- awful
## Examples
### Example 1
#### Input
"This product is really good. I love it."
#### Output
{
    "emotion": "positive",
    "score": 0.9,
    "reason": "The review contains positive words"
}
### Example 2
#### Input
"This product is trash. I hate it."
#### Output
{
    "emotion": "negative",
    "score": 0.9,
    "reason": "The review contains negative words"
}
## Input
User review text
## Output
Return JSON with the following structure:

class Response:
    emotion: str # Sentiment of the review: positive, negative, or neutral
    score: float # Sentiment score between 0 and 1
    reason: str # Explanation for the sentiment

"""

response = client.chat.completions.create(
  model="step-5-preview",
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Is this product any good?"}
  ],
  response_format={ "type": "json_object" },
)

print(response)
```

### Optional: use a schema in the prompt to guide JSON Mode

JSON Schema describes output fields, types, and required properties. Including a schema in a JSON Mode prompt can guide the output structure, but does not enforce strict constraints.

The following schema defines an object with two required fields, `url` and `notes`:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
	"$schema": "http://json-schema.org/draft-07/schema#",
	"title": "User input parsing",
	"type": "object",
	"properties": {
		"url": {
			"type": "string",
			"description": "The URL provided by the user"
		},
		"notes": {
			"type": "string",
			"description": "The user's comments about the URL"
		}
	},
	"required": ["url", "notes"]
}
```

Include the schema in your prompt and set `response_format: {"type": "json_object"}` to guide the output structure. The following is still a prompt example, not an example of the API's `json_schema` parameter:

```markdown theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
You are a text-processing engineer. Extract the URL and the user's comments from the input and return them as JSON.

## Constraint

- Return data that conforms to the JSON Schema below.

{
"$schema": "http://json-schema.org/draft-07/schema#",
"title": "User input parsing",
"type": "object",
"properties": {
"url": {
"type": "string",
"description":"The URL provided by the user"
},
"notes": {
"type": "string",
"description":"The user's comments about the URL"
}
},
"required": [
"url",
"notes"
]
}
```

## Notes

* For both modes, check that the request succeeded and `finish_reason` is `stop`. If it is `length`, the output may have been truncated by `max_tokens` and must not be treated as complete JSON. Consider increasing the output limit and retrying.
* Handle request failures, refusals, and missing usable `content` separately rather than parsing them as business data.
* After parsing `choices[0].message.content`, validate the values against your business requirements. With JSON Mode, also validate fields, types, and required properties yourself.
* Input/output examples in a JSON Mode prompt can improve adherence to the intended structure, but do not establish strict schema compliance.
* When using a proxy or gateway, ensure that `response_format` and its nested fields reach the API server intact. Including a field in the client request does not prove that intermediaries preserve it.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.