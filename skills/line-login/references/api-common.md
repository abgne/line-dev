# Common Specifications

## Rate Limits

Rate limit thresholds for the LINE Login API are **not disclosed**. If a large number of requests are sent within a short period and it is determined to affect the LINE Platform, requests may be temporarily restricted with `429 Too Many Requests`.

Do NOT perform load testing against LINE's authorization or API endpoints.

## Status Codes

| Code | Description |
|------|-------------|
| 200 OK | Request succeeded |
| 204 No Content | Request succeeded (deauthorize endpoint) |
| 400 Bad Request | Invalid request parameters or JSON format |
| 401 Unauthorized | Invalid or incorrect authorization header |
| 403 Forbidden | Not authorized to use the API. Verify account or plan authorization. |
| 413 Payload Too Large | Request exceeds the 2 MB limit |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Temporary server error |

## Response Headers

| Header | Description |
|--------|-------------|
| `x-line-request-id` | Unique request ID. Include in support inquiries. |

## Error Responses

Error responses return a JSON object:

```json
{
  "error": "invalid_request",
  "error_description": "access token expired"
}
```

### ID Token Verify Error Descriptions

| error_description | Meaning |
|-------------------|---------|
| Invalid IdToken. | Malformed ID token or invalid signature |
| Invalid IdToken Issuer. | Issuer is not `https://access.line.me` |
| IdToken expired. | ID token has expired |
| Invalid IdToken Audience. | `aud` does not match `client_id` in request |
| Invalid IdToken Nonce. | `nonce` does not match the request |
| Invalid IdToken Subject Identifier. | `sub` does not match `user_id` in request |

## Forward Compatibility

As LINE Login features are added and modified, the structure of JSON objects in responses and ID tokens may change **without advance notice**:

- Properties may be added or ordered differently
- Whitespace and line breaks may be added or removed between elements
- Data size may vary

**Implementation rules:**
- Do NOT use strict/exhaustive schema validation — unknown fields must be ignored
- Do NOT depend on property order in JSON responses
- Handle unknown values gracefully (log and skip, not crash)

## client_secret Conditional Requirement

The `client_secret` parameter is conditionally required depending on your channel's **App types** setting (configured in LINE Developers Console):

| App types | client_secret |
|-----------|---------------|
| Web app only | **Required** |
| Mobile app only | Ignored |
| Mobile app + Web app | Ignored |

This applies to the following endpoints:
- Refresh access token (`POST /oauth2/v2.1/token` with `grant_type=refresh_token`)
- Revoke access token (`POST /oauth2/v2.1/revoke`)

**Note**: For Issue access token (`grant_type=authorization_code`), `client_secret` is always required regardless of App types.

## Logging

**LINE does not provide logs of authorization requests or LINE Login API requests, regardless of inquiry.** Developers must build and maintain their own logging infrastructure.

### Authorization Logs

| Log Type | Fields |
|----------|--------|
| Authorization Request | Time of request, all parameters (state, nonce, scope, redirect_uri, etc.) |
| Authorization Response | Receipt time, request method, authorization code, error response |

### API Request Logs

| Field | Source | Description |
|-------|--------|-------------|
| Request ID | `x-line-request-id` response header | Essential for debugging with LINE support |
| Timestamp | Application | When the request was made (RFC 2822 format, e.g., `Mon, 16 Jul 2021 10:20:10 GMT`) |
| HTTP Method | Application | GET, POST |
| Endpoint | Application | API path called |
| Status Code | Response | HTTP status returned |

### Optional Enhanced Logging

For improved debugging and auditing, also consider logging:
- API request body content
- Full response body from LINE Platform

## Channel Constraints

### Provider and userId

- `userId` is unique **per provider**, not per channel. All channels under the same provider share the same `userId` for a given user.
- A channel cannot be moved to a different provider after creation.
- Users authenticated via channels under **different providers** will have **different userIds**, even if it's the same LINE user.

### Channel Status

| Status | Access | Reversible? |
|--------|--------|-------------|
| **Developing** | Only Admin and Tester roles can access | Yes (can publish) |
| **Published** | All LINE users can access | **No** (cannot revert to Developing) |

### Channel Restrictions

- Channel name must **not** contain the word "LINE"
- LINE Login channels are available in: Japan, Thailand, Taiwan, Indonesia (region set at creation, cannot be changed)
