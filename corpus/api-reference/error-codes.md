> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Error Codes

This guide lists the error codes you may encounter from the API and describes their causes and recommended fixes.

## Common Error Codes

| Code | Reason | Resolution |
| :-: | - | - |
| 400 | Request parameters are invalid. Common causes: <br /> 1. Image cannot be downloaded <br /> 2. Image count exceeds the limit <br /> 3. The model does not support video input <br /> 4. Model does not exist or you lack permission <br /> 5. Parameter value is invalid | Check the docs and pass the parameters correctly. |
| 401 | Invalid authentication | Make sure you are using the correct API key. |
| 402 | Insufficient balance | Add funds to your account. |
| 404 | Incorrect request path | Update the request path per the docs. |
| 429 | Resource or rate limit exceeded, usually because requests are too frequent | Retry after a short delay. |
| 451 | The request or response content failed review | Modify the request and try again. |
| 500 | Server-side issue on our end | Retry shortly; contact us if it persists. |
| 503 | Server is currently overloaded | Retry after a short delay. |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.