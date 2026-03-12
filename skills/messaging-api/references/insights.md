# Insights

Statistics on message deliveries, followers, demographics, and user interactions.

All endpoints require `Authorization: Bearer {channel access token}`. Rate limit: **60 req/hr** for all endpoints.

## Get Number of Message Deliveries

`GET https://api.line.me/v2/bot/insight/message/delivery?date={date}`

Returns the number of messages sent from LINE Official Account on the specified date.

**Query:** `date` (required) — Format `yyyyMMdd`, timezone UTC+9.

**Response:**

| Property | Type | Description |
|----------|------|-------------|
| `status` | String | `ready` / `unready` / `out_of_service` (before 2017-03-01) |
| `broadcast` | Number? | Sent via "All Friends" in LINE Official Account Manager |
| `targeting` | Number? | Sent via "Targeting" in LINE Official Account Manager |
| `stepMessage` | Number? | Step messages |
| `autoResponse` | Number? | Auto-response messages |
| `welcomeResponse` | Number? | Greeting messages (friend add) |
| `chat` | Number? | Sent from Chat screen |
| `apiBroadcast` | Number? | Sent via Send broadcast message API |
| `apiPush` | Number? | Sent via Send push message API |
| `apiMulticast` | Number? | Sent via Send multicast message API |
| `apiNarrowcast` | Number? | Sent via Send narrowcast message API |
| `apiReply` | Number? | Sent via Send reply message API |
| `ccAutoReply` | Number? | LINE Chat Plus auto reply |
| `ccManualReply` | Number? | LINE Chat Plus manual reply |
| `pnpNoticeMessage` | Number? | LINE notification messages |
| `thirdPartyChatTool` | Number? | Third-party chat tools |

Properties after `broadcast` are only included when `status` is `ready`.

## Get Number of Followers

`GET https://api.line.me/v2/bot/insight/followers?date={date}`

Returns the number of users who have added the LINE Official Account on or before the specified date.

**Query:** `date` (required) — Format `yyyyMMdd`, timezone UTC+9.

**Response:**

| Property | Type | Description |
|----------|------|-------------|
| `status` | String | `ready` / `unready` / `out_of_service` (before 2016-11-01) |
| `followers` | Number? | Total times a user added this account as friend (doesn't decrease on block/delete) |
| `targetedReaches` | Number? | Users reachable via targeted messages (active users with high-certainty demographics) |
| `blocks` | Number? | Users currently blocking the account (decreases on unblock) |

Values are `null` when `status` is not `ready`.

## Get Friend Demographics

`GET https://api.line.me/v2/bot/insight/demographic`

Retrieves demographic breakdown of the LINE Official Account's friends.

**Requirements:**
- Target reach ≥ 20 users
- LINE Official Account created by user in JP, TH, or TW
- Data is ~3 days old (not real-time)

**Response:**

| Property | Type | Description |
|----------|------|-------------|
| `available` | Boolean | `true` if demographic info is available |
| `genders[]` | Array | `{gender, percentage}` — values: `male`, `female`, `unknown` |
| `ages[]` | Array | `{age, percentage}` — values: `from0to14` through `from70`, `unknown` |
| `areas[]` | Array | `{area, percentage}` — JP prefectures, TW counties/cities, TH regions |
| `appTypes[]` | Array | `{appType, percentage}` — values: `ios`, `android`, `others` |
| `subscriptionPeriods[]` | Array | `{subscriptionPeriod, percentage}` — values: `within7days`, `within30days`, `within90days`, `within180days`, `within365days`, `over365days`, `unknown` |

Arrays are empty when `available` is `false`.

## Get User Interaction Statistics

`GET https://api.line.me/v2/bot/insight/message/event?requestId={requestId}`

Returns statistics about how users interact with narrowcast or broadcast messages. Statistics per message or per bubble.

**Query:** `requestId` (required) — Request ID from `X-Line-Request-Id` response header of a narrowcast or broadcast.

Interactions are updated for 14 days from the time the message was sent.

**Privacy protection:** Values are `null` if < 20, or if the actual unique user count is < 20 even when the event count is ≥ 20.

**Response:**

```json
{
  "overview": {
    "requestId": "f70dd685-...",
    "timestamp": 1568214000,
    "delivered": 320,
    "uniqueImpression": 82,
    "uniqueClick": 51,
    "uniqueMediaPlayed": null,
    "uniqueMediaPlayed100Percent": null
  },
  "messages": [
    {
      "seq": 1,
      "impression": 136,
      "mediaPlayed": null,
      "mediaPlayed25Percent": null,
      "mediaPlayed50Percent": null,
      "mediaPlayed75Percent": null,
      "mediaPlayed100Percent": null,
      "uniqueMediaPlayed": null,
      "uniqueMediaPlayed25Percent": null,
      "uniqueMediaPlayed50Percent": null,
      "uniqueMediaPlayed75Percent": null,
      "uniqueMediaPlayed100Percent": null
    }
  ],
  "clicks": [
    {
      "seq": 1,
      "url": "https://line.me/",
      "click": 41,
      "uniqueClick": 30,
      "uniqueClickOfRequest": 30
    }
  ]
}
```

| Section | Properties |
|---------|------------|
| `overview` | `requestId`, `timestamp`, `delivered`, `uniqueImpression`, `uniqueClick`, `uniqueMediaPlayed`, `uniqueMediaPlayed100Percent` |
| `messages[]` | `seq`, `impression`, `mediaPlayed` (+ 25/50/75/100%), `uniqueMediaPlayed` (+ 25/50/75/100%) |
| `clicks[]` | `seq`, `url`, `click`, `uniqueClick`, `uniqueClickOfRequest` |

## Get Statistics Per Unit

`GET https://api.line.me/v2/bot/insight/message/event/aggregation?customAggregationUnit={unit}&from={from}&to={to}`

Statistics for push and multicast messages aggregated by unit name. Same response structure as user interaction statistics (overview, messages, clicks) but without `overview.delivered` and `overview.requestId`.

**Query parameters:**
- `customAggregationUnit` (required): Unit name (case-sensitive). Assigned via `customAggregationUnits` when sending messages.
- `from` (required): Start date `yyyyMMdd` (UTC+9)
- `to` (required): End date `yyyyMMdd` (UTC+9, max 30 days after `from`)

Same privacy protection rules and 14-day interaction window as user interaction statistics.

### Unit-Based Statistics Limits

- Each message can specify only **one** unit name
- Unit name **cannot be changed** after the message is sent
- Max **1,000 different unit names per calendar month** (resets on the 1st). Excess names are treated as unspecified
- Only **Push** and **Multicast** support `customAggregationUnits`
- Check usage: `GET /v2/bot/insight/message/event/aggregation/uniqueCount` (current month count) and `GET /v2/bot/insight/message/event/aggregation/list` (list of unit names)

## Impression Measurement

**Platform:** Only counts impressions on LINE iOS/Android app. **PC and Chrome versions are not counted.**

**100% visibility rule:** A message bubble must be **100% visible** on screen to count as an impression:
- Top and bottom edges fully within the viewport
- Not overlapping with Rich Menu or service menu bar
- For Carousel messages: all four edges (including left/right) must be visible

**Counting rules:**
- `uniqueImpression`: One count per user per message/bubble, regardless of how many times viewed
- `impression`: Can count multiple times for the same user — once per chat session. Leaving and re-entering the chat starts a new session
- Scrolling within a single chat session does not trigger duplicate impressions
- Statistics are updated for **14 days** (1,209,600 seconds) from send time, then frozen

**Not counted as impressions:** Marking messages as read via batch operations (e.g., Android "mark all as read" from chat list, iOS swipe-to-read) without actually viewing the chat.

**Design tip:** Avoid overly tall message bubbles that cannot be 100% visible on screen. Ensure bubbles don't overlap with the Rich Menu.
