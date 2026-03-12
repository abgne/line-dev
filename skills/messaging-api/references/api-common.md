# Common Specifications

## Domain Name

| Domain | Usage |
|--------|-------|
| `api.line.me` | Most endpoints |
| `api-data.line.me` | Get content, Audience file upload, Rich Menu image upload/download |

## Rate Limits

Calculated per **Channel** × **endpoint**. Exceeding limits returns `429 Too Many Requests`.

| Endpoint | Limit |
|----------|-------|
| Narrowcast, Broadcast, Sent message count, Friend count, Demographic stats, Operational stats, Unit stats, Webhook test | 60 req/hr |
| Audience create/update/delete/get (all 12 endpoints) | 60 req/min |
| Webhook URL set/get | 1,000 req/min |
| Rich Menu create/delete, Alias delete, Batch progress | 100 req/hr * |
| Rich Menu batch replace/unreplace | 3 req/hr |
| Multicast, Membership, Coupon | 200 req/sec |
| Loading Animation | 100 req/sec |
| Short-lived Channel Access Token issue | 370 req/sec |
| **All other endpoints** | **2,000 req/sec** |

\* Rich Menu create/delete via LINE Official Account Manager is not subject to this limit.

### Scope of Rate Limits

- Same URL with different HTTP methods = different endpoints
- URL parameters and request body content are not distinguished
- Source IP is not distinguished
- Different Channels under the same LINE Official Account are counted independently

### Audience Concurrent Processing

Audience create/update endpoints have an additional concurrency limit: **10 parallel requests** (per audienceGroupId). Exceeding returns `429`. Check the `jobs` property via Get audience data to see in-progress requests (`QUEUED` / `WORKING`).

## Status Codes

| Code | Description |
|------|-------------|
| 200 OK | Request succeeded |
| 400 Bad Request | Invalid request |
| 401 Unauthorized | Invalid channel access token |
| 403 Forbidden | No permission to access this resource. Verify account or plan authorization |
| 404 Not Found | Information not found. Possible causes: userId doesn't exist, user hasn't consented to profile retrieval, not a friend, or blocked |
| 409 Conflict | A request with the same retry key has already been accepted |
| 410 Gone | Resource no longer exists |
| 413 Payload Too Large | Request exceeds the 2MB limit |
| 415 Unsupported Media Type | Uploaded file format is not supported |
| 429 Too Many Requests | Rate limit exceeded, concurrent limit exceeded, or monthly free message quota exceeded |
| 500 Internal Server Error | Server internal error |

## Response Headers

| Header | Description |
|--------|-------------|
| `X-Line-Request-Id` | Unique ID for each request, used for debugging |
| `X-Line-Accepted-Request-Id` | When a retry key is duplicated, returns the request ID of the previously accepted request (may not always be present) |

## Error Responses

Errors return JSON:

```json
{
  "message": "The request body has 2 error(s)",
  "details": [
    {"message": "May not be empty", "property": "messages[0].text"},
    {"message": "Must be one of the following values: [text, image, ...]", "property": "messages[1].type"}
  ]
}
```

- `message`: Error summary
- `details[]`: Error detail array (may be empty or absent)
- `details[].message`: Specific error description
- `details[].property`: Error field (JSON field name or query parameter)

### Common Error Messages

| Message | Description |
|---------|-------------|
| The request body has X error(s) | Request body JSON has X errors, see `details` |
| Invalid reply token | replyToken expired or already used |
| The property, XXX, in the request body is invalid | Invalid property |
| The request body could not be parsed as JSON | Malformed JSON |
| Authentication failed due to the following reason: XXX | Authentication failure |
| Access to this API is not available for your account | Account lacks permission for this API |
| Failed to send messages | Send failed (e.g., userId doesn't exist) |
| You have reached your monthly limit. | Monthly free or purchased message quota exceeded |
| The API rate limit has been exceeded. | Rate limit exceeded |
| Not found | User not found (not a friend, blocked, or hasn't consented) |

## Retrying an API Request

Use the `X-Line-Retry-Key` header to prevent duplicate processing:

- Hexadecimal UUID (e.g., `123e4567-e89b-12d3-a456-426614174000`)
- Supported endpoints: Push, Multicast, Narrowcast, Broadcast (NOT Reply)
- **Must be included in the first request** — a request sent without a retry key cannot be retried safely later
- **Retry request must be identical** to the original (same messages, same recipients) — changing content invalidates deduplication
- Valid for **24 hours**. Using the same key after 24 hours is treated as a new request, causing duplicate delivery
- Retry requests with a retry key still count toward API call limits
- Using `X-Line-Retry-Key` on unsupported endpoints returns **400 Bad Request**
- A request accepted with `200` cannot be retried even if delivery failed (e.g., user blocked the bot)

**When to retry:**

| Response | Action |
|----------|--------|
| `200` OK | Do not retry |
| `409` Conflict | Do not retry (already accepted) |
| `4xx` (other) | Do not retry (client error) |
| `500` | Retry with exponential backoff |
| Timeout | Retry with exponential backoff |

409 Response example:
```
HTTP/1.1 409 Conflict
x-line-request-id: 123e4567-e89b-12d3-a456-426655440002
x-line-accepted-request-id: 123e4567-e89b-12d3-a456-426655440001

{"message": "The retry key is already accepted", "sentMessages": [{"id": "461230966842064897", "quoteToken": "IStG5h1Tz7b..."}]}
```

## Forward Compatibility

The Messaging API may receive **non-breaking additions without advance notice**:

- New endpoints
- New optional parameters, fields, and headers in requests
- New fields and headers in responses
- New properties in webhook event objects
- New enum values (e.g., new event `type` values)
- Changed property order in responses and webhook events
- Added or removed whitespace/line breaks between data elements

**Implementation rules:**
- Do NOT use strict/exhaustive schema validation — unknown fields must be ignored, not rejected
- Do NOT assume response objects contain only documented fields
- Do NOT depend on property order in JSON responses
- Handle unknown enum values gracefully (e.g., log and skip, not crash)

## Logging

LINE does not provide logs for API requests or webhooks. Developers must implement their own logging.

### API Request Logs

| Field | Source | Description |
|-------|--------|-------------|
| Request ID | `X-Line-Request-Id` response header | Essential for debugging with LINE support |
| Timestamp | Application | When the request was made |
| HTTP Method | Application | GET, POST, PUT, DELETE |
| Endpoint | Application | API path called |
| Status Code | Response | HTTP status returned |

### Webhook Receipt Logs

| Field | Source | Description |
|-------|--------|-------------|
| Sender IP | Request | IP of webhook sender |
| Timestamp | Application | When webhook was received |
| HTTP Method | Request | Always POST |
| Request Path | Request | Webhook endpoint path |
| Response Code | Application | Status code your server returned |

## Other Common Specifications

### URL Encoding

URLs specified in request body properties must use UTF-8 percent-encoding.

Example: domain `example.com`, path `/path`, query `q=Good morning`, fragment `Good afternoon`
→ `https://example.com/path?q=Good%20morning#Good%20afternoon`

### Request Body Limit

2MB. Exceeding returns `413 Payload Too Large`.
