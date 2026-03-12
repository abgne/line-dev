# Common Specifications

## Domain Name

| Domain | Usage |
|--------|-------|
| `api.line.me` | All LINE notification message endpoints |

## Rate Limits

All LINE notification message endpoints: **2,000 requests per second** per channel.

Exceeding limits returns `429 Too Many Requests`.

## Status Codes

For full details, see [Messaging API status codes](https://developers.line.biz/en/reference/messaging-api/#status-codes).

| Code | Description |
|------|-------------|
| 200 OK | Request succeeded (flexible send, count APIs) |
| 202 Accepted | Request accepted (template send) |
| 400 Bad Request | Invalid request (bad destination, invalid message object, unauthorized template) |
| 403 Forbidden | Not authorized to use this endpoint (account lacks notification message permission) |
| 422 Unprocessable Entity | Failed to send — no matching user, wrong country, user refused, or privacy policy not agreed |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Server error |

## Response Headers

| Header | Description |
|--------|-------------|
| `x-line-request-id` | Unique ID for each request. Essential for debugging with LINE support. |

## Error Responses

Errors return JSON:

```json
{
  "message": "Error summary",
  "details": [
    {"message": "Specific error description", "property": "field.name"}
  ]
}
```

- `message`: Error summary
- `details[]`: Array of error details (may be empty or absent)
- `details[].property`: Error field path (e.g., `body.items[0].itemKey`, `to`)

## Retry Keys — NOT Supported

**`X-Line-Retry-Key` is NOT supported** for LINE notification messages. Do not include this header — unlike Messaging API push/multicast, notification messages cannot use retry keys.

For transient errors (500, timeout), implement your own retry logic with exponential backoff.

## IP Address Restriction — Do NOT Use

**Do NOT restrict server IP addresses** in the Messaging API channel's Security Settings tab. Notification messages may originate from different IP ranges than regular Messaging API calls, and IP restrictions can cause sending failures.

## Forward Compatibility

The API may receive non-breaking additions without advance notice:
- New optional parameters, fields, and headers
- New properties in webhook event objects
- New enum values
- Changed property order

**Implementation rules:**
- Do NOT use strict/exhaustive schema validation
- Do NOT assume response objects contain only documented fields
- Handle unknown fields gracefully (ignore, don't reject)

## Logging

LINE does not provide logs. Implement your own:

| Field | Source | Description |
|-------|--------|-------------|
| Request ID | `x-line-request-id` response header | Essential for debugging |
| Timestamp | Application | When request was made |
| HTTP Status | Response | Status code returned |
| Hashed Phone | Application | For correlating send → webhook delivery |
| X-Line-Delivery-Tag | Application | For tracking specific deliveries |
