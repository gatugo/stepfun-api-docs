> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Tool Call to extend your app

LLMs know a lot, but they may lack up-to-date info (news, weather), precise calculations, or domain expertise. When they do, they might invent plausible but wrong answers.

To solve this, Stepfun provides Tool Calls. Tool Calls let the model execute extra actions—search, calculations, database lookups, etc.—to return accurate information. They can also help generate function call signatures so your app can act, not just chat.

## How it works

You can use Tool Calls in two ways:

* Fetch information the model was not trained on to enrich context and answer precisely.
* Operate local application logic to perform business actions.

### Overview

<img src="https://mintcdn.com/stepfun2/LB7Z4XEbvwu-9ERC/images/tool_call_en.png?fit=max&auto=format&n=LB7Z4XEbvwu-9ERC&q=85&s=321cff660d74b206b27a12e696506fdd" alt="" width="2208" height="1034" data-path="images/tool_call_en.png" />

The first pattern calls predefined functions to retrieve precise data. The second triggers application logic to perform tasks.

### Use Tool Call to fetch information

Example: a weather skill that users access via natural language.

Steps:

* Prepare the weather API endpoint and key; implement the query function.
* Define a `get_weather` tool with the function signature.
* The model detects weather intent and fills parameters.
* Call the weather API with those parameters and return the result.

Reference code (Python):

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from openai import OpenAI
import requests
import json

# Weather API settings (using AMap here; choose any provider you like)
get_weather_url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
get_weather_key = "YourGaoDeAPIkey"
COMPLETION_MODEL = "step-5-preview"

# Initialize Stepfun client
STEPFUN_KEY = "YOUR_STEP_API_KEY"
client = OpenAI(base_url="https://api.stepfun.ai/v1", api_key=STEPFUN_KEY)

# Weather lookup function

def get_weather(city):
    params = {
        "city": city,
        "key": get_weather_key,
        "extensions": "base",  # Current weather
    }
    response = requests.get(url=get_weather_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Sorry, I couldn’t get the weather for that location.")

# Tool definition

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Check the weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name (Chinese)"}
                },
                "required": ["city"],
            },
        },
    }
]

# Call the model

def query_weather(prompt):
    completion = client.chat.completions.create(
        model=COMPLETION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        tool_choice="auto",
        tools=tools,
    )
    print(completion)
    # If the model triggers the tool, call the API
    if completion.choices[0].message.content.strip() == "":
        if completion.choices[0].message.tool_calls[0].function.name == "get_weather":
            city_name = json.loads(
                completion.choices[0].message.tool_calls[0].function.arguments
            )
            get_weather(city_name["city"])
        else:
            print("Weather tool not triggered")
    else:
        print("Unexpected response")

# Query weather
query_weather("What’s the weather in Shanghai right now?")
```

Response example:

```jsonc theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
// The model recognized the intent and proposed a tool call with parameters
{
    "id": "291c59ebf4017a937a2a42a8ed52581f.c2669ebc05a491c70f821b4e568b6433",
    "object": "chat.completion",
    "created": 1722505763,
    "model": "step-5-preview",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_brg23SRcTgmpm_V0jfP-iA",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": "{\"city\": \" Shanghai \"}"
                        }
                    }
                ]
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "cached_tokens": 48,
        "prompt_tokens": 94,
        "completion_tokens": 16,
        "total_tokens": 110
    }
}
# Then call the weather API with those parameters and return the result
{
    "status": "1",
    "count": "1",
    "info": "OK",
    "infocode": "10000",
    "lives": [
        {
            "province": "Shanghai",
            "city": "Shanghai",
            "adcode": "310000",
            "weather": "Sunny",
            "temperature": "37",
            "winddirection": "NW",
            "windpower": "≤3",
            "humidity": "42",
            "reporttime": "2024-08-02 10:01:14",
            "temperature_float": "37.0",
            "humidity_float": "42.0"
        }
    ]
}

# Append the API result to messages as context and continue generation.
```

### Use Tool Call to perform actions

When your app needs to act (not just fetch data), Tool Calls can trigger local capabilities. Example: sending emails via natural language.

Steps:

* Implement a local email-sending function.
* Define a `send_email` tool with the function signature.
* The model detects intent and fills parameters.
* Call the email function with those parameters.

#### Reference code (Python & Swift)

Local email function:

```swift theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
func sendEmail(subject: String, body: String, recipient: String) {
    // Use MFMailComposeViewController to send email
}
```

Server-side call to Stepfun:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from openai import OpenAI

# Initialize Stepfun client
STEPFUN_KEY = "YOUR_STEP_API_KEY"
client = OpenAI(base_url="https://api.stepfun.ai/v1", api_key=STEPFUN_KEY)

# Tool definition

tools = [
    {
        "type": "function",
        "function": {
            "name": "senEmail",
            "description": "Send an email with the given subject and body to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Email subject (max 255 characters)",
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body (max 4096 characters)",
                    },
                    "recipient": {"type": "string", "description": "Recipient address"},
                },
                "required": ["subject", "body", "recipient"],
            },
        },
    }
]

# Ask the model for a call signature

def get_call_sign(user_input):
    completion = client.chat.completions.create(
        model=COMPLETION_MODEL,
        messages=[{"role": "user", "content": user_input}],
        tool_choice="auto",
        tools=tools,
    )
    if completion.choices[0].message.content.strip() == "":
        if completion.choices[0].message.tool_calls[0].function.name == "senEmail":
            arguments = json.loads(
                completion.choices[0].message.tool_calls[0].function.arguments
            )
            send_to_client("sendEmail", arguments)
```

### Notes

* Write clear function descriptions so the model understands when to call them; this improves hit rate.
* Describe parameter fields clearly (including expected language) so the model can produce valid arguments.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.