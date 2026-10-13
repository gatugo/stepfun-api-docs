> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Build multi-turn conversations and manage context

Compared to traditional models, large language models let you anchor personas with custom prompts and pass conversation context, making multi-turn dialogs straightforward.

Stepfun’s Chat Completion API accepts an array as the message list. Simply store user and assistant messages in order and send them back to the model to enable multi-turn conversations.

## Implementing multi-turn chat

Persist conversations and messages in your system to build the conversation history.

* Create a Chat when the user starts a conversation.
* When the user sends a message, create a Message; fetch Messages in chronological order and pass them to the model so it can generate with context.
* When the model responds, create another Message.

### Conversation flow

<img src="https://mintcdn.com/stepfun2/LB7Z4XEbvwu-9ERC/images/multiple_round.jpeg?fit=max&auto=format&n=LB7Z4XEbvwu-9ERC&q=85&s=3d69a050cd1b3fe548f8976e3ab3fcab" alt="" width="1196" height="500" data-path="images/multiple_round.jpeg" />

### Code example

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from openai import OpenAI
from datetime import datetime

# Initialize Stepfun client
STEPFUN_KEY = "YOUR_STEP_API_KEY"

client = OpenAI(
  base_url="https://api.stepfun.ai/v1",
  api_key=STEPFUN_KEY
)

# Data structures
class Chat:
  id: str
  user_id: str

class Message:
  chat_id: str
  role : str # system, user, assistant, tool
  content: str # user input or model output
  created_at: datetime

# Fetch messages from the database

# messages_from_db = orm.order_by("created_at","asc").first(5)

messages_from_db = [
  {
    "chat_id":"chat_1",
    "role":"system",
    "content":"You are the Stepfun assistant",
    "created_at": "2024-01-01 10:01:00"
  },
  {
    "chat_id":"chat_1",
    "role":"user",
    "content":"How is the weather today?",
    "created_at": "2024-01-01 10:02:00"
  },
  {
    "chat_id":"chat_1",
    "role":"assistant",
    "content":"Sorry, I can’t answer weather questions.",
    "created_at": "2024-01-01 10:03:00"
  },
  {
    "chat_id":"chat_1",
    "role":"user",
    "content":"Is Beijing a good place to travel?",
    "created_at": "2024-01-01 10:04:00"
  }
]

def clean_msg(msg):
  del msg["chat_id"]
  del msg["created_at"]
  return msg

messages_for_chat = [clean_msg(item) for item in messages_from_db]

# Call the completion API

stream = client.chat.completions.create(
  model="step-5-preview",
  messages=messages_for_chat,
  stream=True,
)

# Render streaming output

for chunk in stream:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
```

## Managing conversation context

`step-5-preview` supports a 1M-token context window; `step-3.7-flash` and the Step 3.5 Flash series support 256K. Manage history according to the selected model's window and reserve space for output. Conversation history counts toward input tokens and cost, so choose an appropriate history length rather than always sending the full conversation.

* For casual chat, keep roughly 10 turns.
* For deep, high-context scenarios, pass the full conversation to the model.

## FAQ

* To achieve correct multi-turn behavior, store timestamps and supply messages to the model in chronological order so it can understand the context properly.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.