# Webhook Events Reference

## Webhook Request

LINE Platform sends an HTTPS POST request to the webhook URL.

```json
{
  "destination": "U...",
  "events": [...]
}
```

- `destination`: Bot's userId (`U[0-9a-f]{32}`)
- `events`: Array of webhook event objects. LINE Platform may send an empty array (`[]`) to confirm connectivity
- Bot server **must return `2xx` status code within 2 seconds** — otherwise LINE considers delivery failed
- **Process events asynchronously** — respond `200` immediately, then process in background. Blocking will cause timeouts
- LINE Platform IP addresses are not disclosed; use signature validation instead of IP whitelisting
- **LIFF `sendMessages()` does NOT trigger webhook** — template/flex messages sent via LIFF are invisible to the bot server
- Webhook endpoint requires **HTTPS with TLS 1.2+** and a certificate from a public CA (Let's Encrypt is OK)

### Signature Validation

Header: `x-line-signature` (case-insensitive, may change without notice)

Algorithm: HMAC-SHA256 the **raw request body** using Channel Secret as key, then base64 encode. Compare with the header value. **Reject the request if validation fails.**

```sh
echo -n '{"destination":"U8e742f...","events":[]}' \
  | openssl dgst -sha256 -hmac '<channel_secret>' -binary \
  | openssl base64
```

**Common signature verification failures:**
- Parsing/deserializing the body before verifying (changes formatting)
- Escape characters (`\n`) being interpreted instead of kept literal
- Non-UTF-8 encoding (must use UTF-8)
- Proxy or load balancer modifying the request body or headers
- Using the wrong Channel Secret (or it was reissued — **old secret is invalidated immediately**)

### Webhook Redelivery

When redelivery is enabled (off by default), undelivered webhooks are resent.

- Retry count and interval are **not disclosed** and may change without notice
- Redelivered events have `deliveryContext.isRedelivery` = `true`
- **Reply tokens in redelivered events are still valid**
- Use `webhookEventId` (ULID) for **deduplication** — same event may arrive multiple times
- Use `timestamp` to determine event order (delivery order may differ)
- If redelivery volume spikes and is deemed to affect LINE Platform, it **may be force-disabled**

## Common Properties

Shared by all event objects:

| Property | Type | Description |
|----------|------|-------------|
| `type` | String | Event type identifier |
| `mode` | String | `active`: Can reply/push messages. `standby`: Waiting (no replyToken, should not send messages) |
| `timestamp` | Number | UNIX time when event occurred (ms). Retains original time on redelivery; order may differ from delivery order |
| `source` | Object | Source user/group/room. May be absent on failed accountLink |
| `webhookEventId` | String | Unique event ID (ULID format) |
| `deliveryContext.isRedelivery` | Boolean | `true`: Redelivered. `false`: First delivery |

### Source Types

| Type | Fields | Description |
|------|--------|-------------|
| `user` | `userId` | 1-on-1 chat |
| `group` | `groupId`, `userId`? | Group chat. `userId` included only in message events when user has granted consent |
| `room` | `roomId`, `userId`? | Multi-person chat. Same as group |

## Message Event

User sends a message. Has `replyToken`.

### text

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `text` |
| `text` | String | Message text. LINE emoji appears as `(hello)`, mentions appear as `@name` |
| `quoteToken` | String | Quote token for this message |
| `markAsReadToken` | String | Read token (no expiration) |
| `emojis[]` | Array? | LINE emoji details |
| `emojis[].index` | Number | Position in text (0-based) |
| `emojis[].length` | Number | Length of emoji string |
| `emojis[].productId` | String | Emoji set product ID |
| `emojis[].emojiId` | String | Emoji ID within the set |
| `mention` | Object? | Mention details |
| `mention.mentionees[].index` | Number | Position in text |
| `mention.mentionees[].length` | Number | Length of mention string |
| `mention.mentionees[].type` | String | `user`: User or bot. `all`: Entire group |
| `mention.mentionees[].userId` | String? | Mentioned userId (only when type=user and user has granted consent) |
| `mention.mentionees[].isSelf` | Boolean? | Whether the mention targets this bot (only when type=user) |
| `quotedMessageId` | String? | Message ID of the quoted message |

### image

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `image` |
| `quoteToken` | String | Quote token |
| `markAsReadToken` | String | Read token |
| `contentProvider.type` | String | `line`: Download via Get content API. `external`: URL provided below |
| `contentProvider.originalContentUrl` | String? | Image URL (when external) |
| `contentProvider.previewImageUrl` | String? | Preview image URL (when external) |
| `imageSet.id` | String? | Set ID when multiple images are sent simultaneously |
| `imageSet.index` | Number? | Position of this image in the set (1-based) |
| `imageSet.total` | Number? | Total number of images in the set |

Note: When multiple images are sent simultaneously, webhook delivery order is not guaranteed to match `imageSet.index`.

### video

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `video` |
| `quoteToken` | String | Quote token |
| `markAsReadToken` | String | Read token |
| `duration` | Number? | Video duration (ms) |
| `contentProvider.type` | String | `line` / `external` (same as image) |
| `contentProvider.originalContentUrl` | String? | Video URL (when external) |
| `contentProvider.previewImageUrl` | String? | Preview image URL (when external) |

### audio

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `audio` |
| `markAsReadToken` | String | Read token |
| `duration` | Number? | Audio duration (ms) |
| `contentProvider.type` | String | `line` / `external` (same as image) |
| `contentProvider.originalContentUrl` | String? | Audio URL (when external) |

### file

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `file` |
| `markAsReadToken` | String | Read token |
| `fileName` | String | File name |
| `fileSize` | Number | File size in bytes |

**Downloading content:** For image, video, audio, and file messages with `contentProvider.type` = `line`, use the Content Retrieval API to download the binary data. See [message-objects.md](message-objects.md#content-retrieval) for endpoints. Video/audio may require transcoding — check status before downloading. **Content has a limited retention period (exact duration undisclosed); download promptly after receiving the webhook.**

### location

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `location` |
| `markAsReadToken` | String | Read token |
| `title` | String? | Location name |
| `address` | String? | Address |
| `latitude` | Decimal | Latitude |
| `longitude` | Decimal | Longitude |

### sticker

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Message ID |
| `type` | String | `sticker` |
| `quoteToken` | String | Quote token |
| `markAsReadToken` | String | Read token |
| `packageId` | String | Package ID |
| `stickerId` | String | Sticker ID |
| `stickerResourceType` | String | See table below |
| `keywords` | String[]? | Up to 15 descriptive keywords (randomly selected; experimental) |
| `text` | String? | User-entered text (MESSAGE type only, max 100 chars) |
| `quotedMessageId` | String? | Message ID of the quoted message |

**stickerResourceType values:**

| Value | Description |
|-------|-------------|
| `STATIC` | Still image |
| `ANIMATION` | Animated sticker |
| `SOUND` | Sticker with sound |
| `ANIMATION_SOUND` | Animated sticker with sound |
| `POPUP` | Pop-up or effect sticker |
| `POPUP_SOUND` | Pop-up or effect sticker with sound |
| `CUSTOM` | Custom sticker (user-entered text cannot be retrieved) |
| `MESSAGE` | Message sticker |

Note: Sticker Arranging feature is not supported. Combined stickers always return packageId `30563`, stickerId `651698630`, type `STATIC`. New resource types may be added in the future.

## Follow Event

User adds bot as friend or unblocks. Has `replyToken`.

| Property | Type | Description |
|----------|------|-------------|
| `follow.isUnblocked` | Boolean | `false`: New friend. `true`: Unblocked. Accuracy is not guaranteed 100% |

```json
{"type": "follow", "follow": {"isUnblocked": false}, "replyToken": "..."}
```

## Unfollow Event

User blocks the bot. No `replyToken`.

## Join / Leave Event

- `join`: Bot is invited to a group or multi-person chat. Has `replyToken`. For groups: triggered on invitation. For multi-person chats: triggered on the first event after bot is added.
- `leave`: Bot is removed or leaves. No `replyToken`.

## Member Join / Member Left Event

A member joins or leaves a group/room where the bot is already present. `memberJoined` has `replyToken`.

```json
{
  "type": "memberJoined",
  "joined": {"members": [{"type": "user", "userId": "U..."}]},
  "source": {"type": "group", "groupId": "C..."},
  "replyToken": "..."
}
```

## Postback Event

User triggers a postback action. Has `replyToken`.

| Property | Type | Description |
|----------|------|-------------|
| `postback.data` | String | Postback data |
| `postback.params` | Object? | Parameters from datetime picker or Rich Menu switch |

### Datetime picker params

| Property | Format | Description |
|----------|--------|-------------|
| `date` | full-date | Date selected (date mode) |
| `time` | HH:mm | Time selected (time mode) |
| `datetime` | yyyy-MM-ddTHH:mm | Date and time selected (datetime mode) |

### Rich Menu switch params

| Property | Description |
|----------|-------------|
| `newRichMenuAliasId` | Target Rich Menu Alias ID (absent on failure) |
| `status` | `SUCCESS` / `RICHMENU_ALIAS_ID_NOTFOUND` / `RICHMENU_NOTFOUND` / `FAILED` |

## Video Play Complete Event

type: `videoPlayComplete`. User finishes viewing a video with a `trackingId`. Has `replyToken`.

| Property | Description |
|----------|-------------|
| `videoPlayComplete.trackingId` | Same value as the `trackingId` in the video message |

Note: Watching multiple times in a single session does not trigger duplicate events. Videos in Imagemap/Flex messages are not supported.

## Beacon Event

User enters LINE Beacon range. Has `replyToken`. **Available in Japan, Taiwan, and Thailand only.**

| Property | Description |
|----------|-------------|
| `beacon.hwid` | Beacon hardware ID |
| `beacon.type` | `enter`: Entered range. `banner`: Tapped banner (enterprise only). `stay`: Stayed in range |
| `beacon.dm` | Beacon Device Message (hex string, optional) |

**Trigger conditions (all must be met):**
- User's Bluetooth is enabled
- User has enabled "Use LINE Beacon" in LINE Settings > Privacy
- User has added the beacon's linked LINE Official Account as a friend
- Beacon device is powered on and in range

One beacon can only be linked to one LINE Official Account. Multiple beacons can be linked to the same account. Register beacons via LINE Official Account Manager.

## Account Link Event

User completes account linking. Has `replyToken`.

| Property | Description |
|----------|-------------|
| `link.result` | `ok`: Success. `failed`: Failure |
| `link.nonce` | Nonce used during linking |

`source` may be absent when account linking fails.

## Unsend Event

User unsends a message. No `replyToken`.

| Property | Description |
|----------|-------------|
| `unsend.messageId` | Message ID of the unsent message |

Recommendation: Respect the user's intent and ensure the unsent message is no longer viewable or usable.

## Membership Event

User joins, renews, or leaves a Membership Plan.

| Property | Description |
|----------|-------------|
| `membership.membershipNo` | Membership plan number |
| `membership.membershipStatus` | `joined` / `renewed` / `left` |

`joined` and `renewed` have `replyToken`.

## Webhook Settings

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Set webhook URL | PUT | `/v2/bot/channel/webhook/endpoint` |
| Get webhook info | GET | `/v2/bot/channel/webhook/endpoint` |
| Test webhook | POST | `/v2/bot/channel/webhook/test` |

- URL rules: HTTPS, max 500 characters
- Changes may take up to 1 minute to take effect (caching)
- Rate limit: 1,000 req/min
