> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get account details

Retrieve information for the current account, including the available balance.

## Endpoint

`GET https://api.stepfun.ai/v1/accounts`

## Request parameters

None

## Response

* `object` `string`<br /> Always `account`

* `type` `string` <br /> Account type. Possible values: `prepaid` or `postpaid`.

* `balance` `float` <br /> Current available balance.

* `total_cash_balance` `float`<br /> Total deposited amount.

* `total_voucher_balance` `float`<br /> Total promotional/bonus amount.

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl --location 'https://api.stepfun.ai/v1/accounts' \
    --header 'Authorization: Bearer YOUR_STEP_API_KEY'
    ```
  </Tab>

  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    import requests

    url = "https://api.stepfun.ai/v1/accounts"

    payload = {}
    headers = {
    'Authorization': 'Bearer YOUR_STEP_API_KEY'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    ```
  </Tab>
</Tabs>

**Response**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "object": "account",
    "type": "prepaid",
    "balance": 0.00,
    "total_cash_balance": 0.00,
    "total_voucher_balance": 26.00
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.