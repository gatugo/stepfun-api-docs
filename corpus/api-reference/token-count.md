> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Token Count

Calculate the token count for a conversation. The request format is similar to the Chat Completion API.

## Endpoint

`POST https://api.stepfun.ai/v1/token/count`

## Request parameters

* `model` `string` ***required***<br />Model name to use.
* `messages` `object array` ***required***<br />Conversation so far, including user and assistant messages.

<Expandable>
  - System message `object`

      <Expandable>
        * `role` `string`<br />Always `system`.
        * `content` `string`<br />System message text.
      </Expandable>

  - User message `object`

      <Expandable>
        * `role` `string`<br />Always `user`.
        * `content` `string or object array`<br />User message content: either a `multipart` list or a plain text string.

              <Expandable>
                * `Plain text` `string`<br />Directly pass a string as the message content.
                * `multipart` list `object array`<br />Structured multimodal message.

                        <Expandable>
                          * Text message `object`

                                    <Expandable>
                                      * `type` `string`<br />Always `text`.
                                      * `text` `string`<br />Text content.
                                    </Expandable>

                          * Image message `object`

                                    <Expandable>
                                      * `type` `string`<br />Always `image_url`.
                                      * `image_url` `object`

                                                  <Expandable>
                                                    * `url` `string`<br />Image URL or base64 string.
                                                      <p>URLs support only http and https.</p>
                                                      <p>Base64 example: `data:image/jpeg;base64,${base64_string}` (replace jpeg with your format and the encoded data).</p>
                                                      <p>Supported image formats: jpg/jpeg, png, webp, static gif.</p>
                                                  </Expandable>
                                    </Expandable>
                        </Expandable>
              </Expandable>
      </Expandable>

  - Assistant message `object`

      <Expandable>
        * `role` `string`<br />Always `assistant`.
        * `content` `string | null`<br />Assistant message text.
      </Expandable>
</Expandable>

## Response

* `data` `object`<br />Token count result.
  <Expandable>
    * `total_tokens` `int`<br />Total tokens in the request.
  </Expandable>

## Examples

<Tabs>
  <Tab title="Text chat">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/token/count \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "model": "step-5-preview",
        "messages": [
          {
            "role": "system",
            "content": "You are an AI assistant provided by StepFun. You excel at conversations in Chinese, English, and other languages. While keeping user data safe, you should answer quickly and accurately, and reject any content related to pornography, drugs, gambling, violence, or terrorism."
          },
          {
            "role": "user",
            "content": "Hi, please introduce StepFun'\''s AI!"
          }
        ]
      }'
    ```

    ```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "data": {
        "total_tokens": 85
      }
    }
    ```
  </Tab>

  <Tab title="Mixed media">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/token/count \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "model": "step-5-preview",
        "messages": [
          {
            "role": "system",
            "content": "You are an AI assistant provided by StepFun. You excel at Chinese, English, and many other languages, and you can describe user-provided images precisely. Keep user data safe, answer quickly and accurately, and refuse content related to pornography, drugs, gambling, violence, or terrorism."
          },
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "Describe this picture in elegant language."
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": "https://www.stepfun.com/assets/section-1-CTe4nZiO.webp"
                }
              }
            ]
          }
        ]
      }'
    ```

    ```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "data": {
        "total_tokens": 497
      }
    }
    ```
  </Tab>

  <Tab title="Base64 image">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    # Load an image into memory (demo only; read from a file as needed)
    image_base64="data:image/webp;base64,"$(curl -s "https://www.stepfun.com/assets/section-1-CTe4nZiO.webp" | base64)

    curl https://api.stepfun.ai/v1/token/count \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d "{
        \"model\": \"step-5-preview\",
        \"messages\": [
          {
            \"role\": \"system\",
            \"content\": \"You are an AI assistant provided by StepFun. You excel at Chinese, English, and many other languages, and you can describe user-provided images precisely. Keep user data safe, answer quickly and accurately, and refuse content related to pornography, drugs, gambling, violence, or terrorism.\"
          },
          {
            \"role\": \"user\",
            \"content\": [
              {
                \"type\": \"text\",
                \"text\": \"Describe this image in elegant language.\"
              },
              {
                \"type\": \"image_url\",
                \"image_url\": {
                  \"url\": \"${image_base64}\"
                }
              }
            ]
          }
        ]
      }"
    ```

    ```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "data": {
        "total_tokens": 497
      }
    }
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.