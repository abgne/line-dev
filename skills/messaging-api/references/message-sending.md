# Message Sending

All endpoints require `Authorization: Bearer {channel access token}` and `Content-Type: application/json`.

## Sending Endpoints

| Mode | Endpoint | Target | Rate limit |
|------|----------|--------|------------|
| Reply | `POST /v2/bot/message/reply` | replyToken from webhook | 2,000 req/sec |
| Push | `POST /v2/bot/message/push` | userId / groupId / roomId | 2,000 req/sec |
| Multicast | `POST /v2/bot/message/multicast` | Array of userIds (max 500) | 200 req/sec |
| Narrowcast | `POST /v2/bot/message/narrowcast` | Audience + demographic filters | 60 req/hr |
| Broadcast | `POST /v2/bot/message/broadcast` | All friends | 60 req/hr |

All endpoints accept max 5 message objects per request.

## Message Counting (Billing)

- **Reply messages are FREE** — not counted toward monthly quota
- **Push, Multicast, Narrowcast, Broadcast are COUNTED** toward quota
- Counting is **per recipient**, not per message object — sending 5 messages to 1 user in one request = **1** counted message
- Messages to blocked users or non-existent user IDs are **not counted**
- When monthly quota is exceeded, sending endpoints return an error and messages are not delivered
- Quotas and plans vary by region — check via quota/consumption endpoints below
- **Do NOT quote specific pricing from memory** — plans, free-tier limits, and per-message costs differ by region and change over time. Direct users to check the LINE Official Account pricing page for their region

**Design implication:** Maximize use of reply messages (free) over push messages (counted) when possible.

## Reply Message

Sends a reply message in response to a webhook event.

```json
{
  "replyToken": "nHuyWiB7...",
  "messages": [{"type": "text", "text": "Hello!"}]
}
```

### Reply Token Rules

- Reply tokens can only be used **once**
- Must be used **within 1 minute** after receiving the webhook (subject to change without notice)
- Redelivered webhooks include a usable reply token, valid within 1 minute of redelivery, unless:
  - The original reply token has already been used
  - 20 minutes have passed since the event occurred
- Use reply tokens as soon as possible — don't rely on the time limit

## Push Message

Sends a message to a user, group chat, or multi-person chat at any time.

```json
{
  "to": "U4af4980629...",
  "messages": [{"type": "text", "text": "Hello!"}],
  "notificationDisabled": false,
  "customAggregationUnits": ["Promotion_a"]
}
```

### Conditions

You can send push messages to:
- Users who have added your LINE Official Account as a friend
- Group chats or multi-person chats the bot has joined
- Users who sent a message to your LINE Official Account within 7 days (even if not a friend)

Status `200` is returned but message won't be delivered to:
- Users who deleted their LINE account
- Users who blocked the LINE Official Account
- Users who haven't added the LINE Official Account as a friend (except within the 7-day window)

### Response

```json
{
  "sentMessages": [
    {"id": "461230966842064897", "quoteToken": "IStG5h1Tz7b..."}
  ]
}
```

`quoteToken` is only included when a quotable message object was sent (text, textV2, sticker, image, video, template, flex).

### Quoting Messages

Only **Reply** and **Push** endpoints support sending quoted messages. Multicast, Narrowcast, and Broadcast do **not** support `quoteToken`.

- Quote token has **no expiration** and can be reused
- Token is only valid within the **same chat** where the original message was sent
- When the quoted message is unsent or chat history is deleted, the quote area shows "Message unavailable."
- Template and Flex messages, when quoted, display only their `altText`

## Multicast Message

Sends the same message to multiple user IDs efficiently. Cannot send to group chats or multi-person chats.

```json
{
  "to": ["U4af4980629...", "U0c229f96c4..."],
  "messages": [{"type": "text", "text": "Hello!"}]
}
```

- `to`: Array of user IDs (max 500). Use `userId` values from webhook events, not LINE IDs.
- For a single recipient, use push message instead (lower latency)
- Response: `200` with empty JSON object `{}`

## Narrowcast Message

Sends a message to multiple users filtered by attributes (age, gender, OS, region) or audiences. Sent asynchronously — check delivery status via the progress endpoint.

```json
{
  "messages": [{"type": "text", "text": "Hello!"}],
  "recipient": {
    "type": "operator",
    "and": [
      {"type": "audience", "audienceGroupId": 5614991017776},
      {"type": "operator", "not": {"type": "audience", "audienceGroupId": 4389303728991}}
    ]
  },
  "filter": {
    "demographic": {
      "type": "operator",
      "and": [
        {"type": "gender", "oneOf": ["male", "female"]},
        {"type": "age", "gte": "age_20", "lt": "age_25"},
        {"type": "area", "oneOf": ["jp_23", "jp_05"]},
        {"type": "appType", "oneOf": ["android", "ios"]},
        {"type": "subscriptionPeriod", "gte": "day_7", "lt": "day_30"}
      ]
    }
  },
  "limit": {"max": 100, "upToRemainingQuota": true}
}
```

### Recipient Objects

| Type | Description |
|------|-------------|
| `audience` | Specify by `audienceGroupId` |
| `redelivery` | Specify by `requestId` of a previously sent narrowcast (within 14 days, delivery completed) |
| `operator` | Combine with `and`, `or`, `not` |

Max 10 combined audience + redelivery objects per request. No limit on operator objects.

### Demographic Filter Types

| Type | Property | Values |
|------|----------|--------|
| `gender` | `oneOf` | `male`, `female` |
| `age` | `gte`, `lt` | `age_15` through `age_50` (5-year intervals) |
| `appType` | `oneOf` | `android`, `ios` |
| `area` | `oneOf` | Region codes (e.g., `jp_23`, `tw_01`) |
| `subscriptionPeriod` | `gte`, `lt` | `day_7`, `day_30`, `day_90`, `day_180`, `day_365` |

### Limit Object

| Property | Type | Description |
|----------|------|-------------|
| `max` | Number? | Max number of recipients |
| `upToRemainingQuota` | Boolean? | If `true`, limits to the remaining monthly quota |
| `forbidPartialDelivery` | Boolean? | If `true`, cancels the entire delivery when not all recipients can be reached |

### Restrictions

- To use attribute filters, the LINE Official Account's target reach must be ≥ 100 users
- Final recipient count must be ≥ 50 users — **exempt** when sending only to UPLOAD or chat tag audiences created by your own OA (with no attribute filter)
- Each audience must have ≥ 50 recipients — **exempt** for UPLOAD and chat tag audiences created by your own OA
- **Cross-OA caveat:** audiences shared from another LINE Official Account (via Business Manager) do NOT receive the above exemptions — the 50-person rules apply even if the type is UPLOAD or chat tag
- When the 50-person rule is violated, LINE returns `202` at send time but delivery fails afterward — check `GET /v2/bot/message/progress/narrowcast` for `errorCode: 2` (insufficient recipients) or `errorCode: 4` (audience < 50)
- Narrowcast reserves the full target reach count from monthly quota during delivery

### Get Narrowcast Status

`GET https://api.line.me/v2/bot/message/progress/narrowcast?requestId={request_id}`

| Property | Type | Description |
|----------|------|-------------|
| `phase` | String | `waiting` / `sending` / `succeeded` / `failed` |
| `successCount` | Number? | Users who received the message |
| `failureCount` | Number? | Users who failed (e.g., blocked during send) |
| `targetCount` | Number? | Intended recipients |
| `failedDescription` | String? | Failure reason (only when `failed`) |
| `errorCode` | Number? | `1`: internal, `2`: insufficient recipients, `3`: conflict, `4`: audience < 50, `5`: partial delivery canceled |
| `acceptedTime` | String | ISO 8601 (UTC) |
| `completedTime` | String? | ISO 8601 (UTC), only when `succeeded` or `failed` |

Status is available for 14 days after `acceptedTime`.

## Broadcast Message

Sends a message to all users who are friends with your LINE Official Account.

```json
{
  "messages": [{"type": "text", "text": "Hello!"}]
}
```

Response: `200` with empty JSON object `{}`.

## Common Optional Parameters

Available on push, multicast, narrowcast, and broadcast:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `notificationDisabled` | Boolean | `false` | `true`: No push notification sent to user |
| `customAggregationUnits` | String[] | — | Aggregation unit name for statistics (max 1 unit, max 30 chars, alphanumeric + underscore, max 1,000 different unit names per month) |

Push, multicast, narrowcast, and broadcast support `X-Line-Retry-Key` header (UUID) for retry deduplication. See [api-common.md](api-common.md#retrying-an-api-request).

## Mark Messages as Read

`POST https://api.line.me/v2/bot/chat/markAsRead`

Marks all messages sent before the specified message as read.

```json
{
  "markAsReadToken": "{mark as read token}"
}
```

- `markAsReadToken`: From the `markAsReadToken` property in the webhook message event object. **No expiration.**
- **Prerequisite:** Chat must be **enabled** in LINE Official Account Manager's Response settings. When Chat is off, messages are automatically marked as read (API not needed and not usable)
- Marks all messages sent **before** the specified message as read (not just that single message)
- Rate limit: 2,000 req/sec

## Loading Animation

`POST https://api.line.me/v2/bot/chat/loading/start`

Displays a typing animation to indicate the bot is preparing a response.

```json
{
  "chatId": "U...",
  "loadingSeconds": 5
}
```

- `chatId`: userId (**1-on-1 chat only**, not groups or multi-person chats)
- `loadingSeconds`: Integer, **5 to 60** (default 20)
- Animation disappears when: the bot sends a new message, OR the specified seconds elapse
- **Only displayed when the user is actively viewing the chat** — not shown retroactively if the user opens the chat later
- Sending a new request while animation is active **overrides** the timer to the new value
- Rate limit: 100 req/sec

## Validate Message Objects

Pre-validate message objects before sending:

| Mode | Endpoint |
|------|----------|
| Reply | `POST /v2/bot/message/validate/reply` |
| Push | `POST /v2/bot/message/validate/push` |
| Multicast | `POST /v2/bot/message/validate/multicast` |
| Narrowcast | `POST /v2/bot/message/validate/narrowcast` |
| Broadcast | `POST /v2/bot/message/validate/broadcast` |

Request body: `{"messages": [...]}` (same message objects array)

Returns `200` with empty JSON if valid.

## Message Statistics

### Quota and Counts

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get monthly target limit | GET | `/v2/bot/message/quota` |
| Get messages sent this month | GET | `/v2/bot/message/quota/consumption` |
| Get sent reply count | GET | `/v2/bot/message/delivery/reply?date={yyyyMMdd}` |
| Get sent push count | GET | `/v2/bot/message/delivery/push?date={yyyyMMdd}` |
| Get sent multicast count | GET | `/v2/bot/message/delivery/multicast?date={yyyyMMdd}` |
| Get sent broadcast count | GET | `/v2/bot/message/delivery/broadcast?date={yyyyMMdd}` |

Rate limits: Quota endpoints 60 req/hr, delivery count endpoints 2,000 req/sec.
