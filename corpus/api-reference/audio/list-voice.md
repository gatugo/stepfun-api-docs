> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# List cloned voices

Use this API to query the cloned voices under the current account. For the built-in system voices, see [Get system voices](/docs/en/api-reference/audio/system-voices).

### Endpoint

`GET https://api.stepfun.ai/v1/audio/voices`

### Request parameters

All parameters are query parameters.

* `limit` `integer` ***optional***<br />Page size. Default 20, min 1, max 100. A value outside this range returns `400`.

* `order` `string` ***optional***<br />Sort order by creation time, `asc` or `desc` (default).<br /> `asc`: older voices first <br /> `desc`: newer voices first

* `before` `string` ***optional***<br /> Cursor voice ID. Returns the page of voices that precede this ID in the current sort order.

* `after` `string` ***optional***<br /> Cursor voice ID. Returns the page of voices that follow this ID in the current sort order.

<Note>
  `before` / `after` must be a voice ID that belongs to your account; otherwise the request fails with `400 voice ... not found or does not belong to this user`. Combine a cursor with `limit` and `order` to page through results, and use `last_id` from the previous response as the next `after` value.
</Note>

### Response

* `object` `string`<br />Always `list`.

* `data` `array`<br /> Voice entries:
  * `id` `string` <br /> Voice ID for audio generation.
  * `file_id` `string`<br /> Source audio File ID used for cloning.
  * `created_at` `integer`<br /> Creation time, as a Unix timestamp in seconds.

* `has_more` `boolean`<br /> Whether more pages exist.

* `first_id` `string`<br /> ID of the first voice in the page.

* `last_id` `string`<br /> ID of the last voice in the page.

<Note>
  The response does not indicate which model a voice was cloned with. Keep track of the model you used when creating each voice — see [Clone a voice](/docs/en/api-reference/audio/create-voice).
</Note>

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl --location 'https://api.stepfun.ai/v1/audio/voices' \
      --header 'Authorization: Bearer YOUR_STEP_API_KEY'
    ```
  </Tab>

  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    import requests

    url = "https://api.stepfun.ai/v1/audio/voices"

    payload = {}
    headers = {
        "Authorization": "Bearer YOUR_STEP_API_KEY"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    ```
  </Tab>
</Tabs>

**Response**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "object": "list",
  "data": [
    {
      "id": "voice-tone-FmBrMBqicC",
      "file_id": "file-FmBrMBqicC",
      "created_at": 1742374363
    }
  ],
  "has_more": false,
  "first_id": "voice-tone-FmBrMBqicC",
  "last_id": "voice-tone-FmBrMBqicC"
}
```

### Pagination example

Request the oldest voice first, then use `last_id` as the cursor for the next page.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl --location 'https://api.stepfun.ai/v1/audio/voices?limit=1&order=asc' \
  --header 'Authorization: Bearer YOUR_STEP_API_KEY'

curl --location 'https://api.stepfun.ai/v1/audio/voices?limit=1&order=asc&after=voice-tone-FmBrMBqicC' \
  --header 'Authorization: Bearer YOUR_STEP_API_KEY'
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.