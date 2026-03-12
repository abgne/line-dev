# Message Objects

JSON objects which contain the contents of the message you send. Max 5 messages per request.

## Common Properties

All message objects support these optional properties:

| Property | Description |
|----------|-------------|
| `quickReply` | Quick reply buttons. If multiple messages sent, only the last message's quickReply is displayed |
| `sender.name` | Custom display name. Max 20 chars. Certain words like `LINE` may not be used |
| `sender.iconUrl` | Custom icon URL (HTTPS, PNG, 1:1 ratio, max 1MB, max 2000 chars) |

```json
{
  "type": "text",
  "text": "Hello, I am Cony!!",
  "sender": {"name": "Cony", "iconUrl": "https://line.me/conyprof"}
}
```

**Sender icon/name display scope:** Custom sender only appears in **message bubbles** (format: `display name from 'account name'`). Chat list, friend list, search results, business profile, and the chat room header bar always show the original LINE Official Account name/icon.

## Text Character Counting

Text lengths are measured in **UTF-16 code units** (not Unicode code points). Multi-code-unit characters count as multiple: e.g., emoji 🍎 = **2 chars**.

**LINE Emoji length trap:** The `$` placeholder is replaced by the emoji's **alternative text** for length calculation. Alt text length is **not publicly disclosed**, so including LINE emoji may cause unpredictable length expansion and send failures. Leave buffer when using LINE emoji near the character limit.

**Exceptions using grapheme clusters:** These properties count by grapheme cluster instead of UTF-16:
- All action `label`, postback `displayText`/`fillInText`/`text`, message action `text`
- Template `text`/`title`, rich menu `chatBarText`/`name`

## Text Message

```json
{"type": "text", "text": "Hello, world!", "quoteToken": "yHAz4Ua2wx7..."}
```

- `text`: Max 5000 chars (UTF-16 code units). Supports LINE emoji (`$` placeholder) and Unicode emoji
- `quoteToken`: Optional. Quote token of a past message to quote
- `emojis`: Optional. Max 20 LINE emoji per message. Each needs `index`, `productId`, `emojiId`

With LINE emoji:
```json
{
  "type": "text",
  "text": "$ LINE emoji $",
  "emojis": [
    {"index": 0, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "001"},
    {"index": 13, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "002"}
  ]
}
```

## Text Message V2

**Preferred for new development** — LINE may only add new features to textV2 going forward.

Unlike text message, textV2 substitutes `{placeholder}` with mentions and emoji. Escape literal braces with `{{` and `}}`.

```json
{
  "type": "textV2",
  "text": "Welcome, {user1}! {laugh}\n{everyone} There is a newcomer!",
  "substitution": {
    "user1": {"type": "mention", "mentionee": {"type": "user", "userId": "U49585cd0d5..."}},
    "laugh": {"type": "emoji", "productId": "5a8555cfe6256cc92ea23c2a", "emojiId": "002"},
    "everyone": {"type": "mention", "mentionee": {"type": "all"}}
  }
}
```

- `text`: Max 5000 chars
- `substitution`: Max 100 objects. Keys: `[0-9a-zA-Z_]`, max 20 chars
- `quoteToken`: Optional

**Mention restrictions:**
- Only works in reply or push messages (not multicast/broadcast)
- Destination must be a group or multi-person chat
- Bot must be a member of the chat
- All mentioned users must be members of the chat
- Max 20 mentions per message

## Sticker Message

```json
{"type": "sticker", "packageId": "446", "stickerId": "1988"}
```

- `quoteToken`: Optional. Supports quoting past messages
- Only stickers listed in the [official sendable sticker list](https://developers.line.biz/en/docs/messaging-api/sticker-list/) can be sent via API. User-owned and promotional stickers cannot be sent
- Available [LINE emoji list](https://developers.line.biz/en/docs/messaging-api/emoji-list/) for text message `emojis` property (39 product IDs)

## Image Message

```json
{
  "type": "image",
  "originalContentUrl": "https://example.com/original.jpg",
  "previewImageUrl": "https://example.com/preview.jpg"
}
```

- Image: JPEG/PNG, max 10MB. URL max 2000 chars, HTTPS
- Preview: JPEG/PNG, max 1MB. URL max 2000 chars, HTTPS

## Video Message

```json
{
  "type": "video",
  "originalContentUrl": "https://example.com/video.mp4",
  "previewImageUrl": "https://example.com/preview.jpg",
  "trackingId": "track-001"
}
```

- Video: MP4, max 200MB. URL max 2000 chars, HTTPS
- Preview: JPEG/PNG, max 1MB. Aspect ratio should match video
- `trackingId`: Optional (max 100 chars, `[a-zA-Z0-9]` + `-.=,+*()%$&;:@{}!?<>[]`). Pairs with `videoPlayComplete` webhook event. **Cannot be used in group/multi-person chats**

## Audio Message

```json
{
  "type": "audio",
  "originalContentUrl": "https://example.com/audio.m4a",
  "duration": 60000
}
```

- Format: M4A or MP3, max 200MB. URL max 2000 chars, HTTPS
- `duration`: milliseconds (required)

## Location Message

```json
{
  "type": "location",
  "title": "LINE Office",
  "address": "Tokyo, Japan",
  "latitude": 35.6895,
  "longitude": 139.6917
}
```

- `title`: Max 100 chars (required)
- `address`: Max 100 chars (required)

## Imagemap Message

Define multiple tappable areas on an image. Can overlay video with post-playback link.

```json
{
  "type": "imagemap",
  "baseUrl": "https://example.com/imagemap",
  "altText": "Imagemap",
  "baseSize": {"width": 1040, "height": 1040},
  "video": {
    "originalContentUrl": "https://example.com/video.mp4",
    "previewImageUrl": "https://example.com/preview.jpg",
    "area": {"x": 0, "y": 0, "width": 1040, "height": 585},
    "externalLink": {"linkUri": "https://example.com/more", "label": "See More"}
  },
  "actions": [
    {
      "type": "uri",
      "linkUri": "https://example.com",
      "area": {"x": 0, "y": 586, "width": 520, "height": 454}
    },
    {
      "type": "message",
      "text": "Hello",
      "area": {"x": 520, "y": 586, "width": 520, "height": 454}
    }
  ]
}
```

- `baseUrl`: HTTPS, max 2000 chars. **Do NOT include file extension** — LINE appends `/{width}` (240/300/460/700/1040) to fetch appropriate resolution
- `altText`: Max 1500 chars
- `baseSize.width`: Must be 1040. Height corresponds proportionally
- `actions`: Max 50. Imagemap uses its own action types (`uri` with `linkUri`, `message` with `text`, `clipboard`), each with an `area` object — these are NOT the same as regular action objects
- `video`: Optional. Video overlay with `externalLink` label (max 30 chars) shown after playback

## Coupon Message

```json
{"type": "coupon", "couponId": "01JYNW8JMQ...", "deliveryTag": "2025_winter_campaign"}
```

- `couponId`: Required. From Create Coupon API response
- `deliveryTag`: Optional (max 30, `[a-zA-Z0-9_]`). Path name for coupon insights. Defaults to `Unknown`

## Template Message

Common: `altText` required (max 1500 chars). Use Flex Message for more flexible layouts.

### Buttons Template
```json
{
  "type": "template",
  "altText": "Menu",
  "template": {
    "type": "buttons",
    "thumbnailImageUrl": "https://example.com/image.jpg",
    "imageAspectRatio": "rectangle",
    "imageSize": "cover",
    "title": "Menu",
    "text": "Please select",
    "defaultAction": {"type": "uri", "label": "Detail", "uri": "https://example.com"},
    "actions": [
      {"type": "postback", "label": "Buy", "data": "action=buy"},
      {"type": "uri", "label": "Website", "uri": "https://example.com"}
    ]
  }
}
```

- `thumbnailImageUrl`: Optional. JPEG/PNG, max 1024px wide, max 10MB
- `imageAspectRatio`: `rectangle` (1.51:1, default) / `square` (1:1)
- `imageSize`: `cover` (default) / `contain`
- `imageBackgroundColor`: RGB hex, default `#FFFFFF`
- `title`: Optional, max 40 chars
- `text`: Required. **Max 160 chars** (no image/title) / **max 60 chars** (with image or title)
- `defaultAction`: Optional. Action when image/title/text area tapped
- `actions`: Max **4** action objects

### Confirm Template
```json
{
  "type": "template",
  "altText": "Confirm",
  "template": {
    "type": "confirm",
    "text": "Are you sure?",
    "actions": [
      {"type": "message", "label": "Yes", "text": "yes"},
      {"type": "message", "label": "No", "text": "no"}
    ]
  }
}
```

- `text`: Max 240 chars
- `actions`: Exactly **2** action objects

### Carousel Template
```json
{
  "type": "template",
  "altText": "Carousel",
  "template": {
    "type": "carousel",
    "imageAspectRatio": "rectangle",
    "imageSize": "cover",
    "columns": [
      {
        "thumbnailImageUrl": "https://example.com/item1.jpg",
        "title": "Item 1",
        "text": "Description",
        "defaultAction": {"type": "uri", "label": "Detail", "uri": "https://example.com/1"},
        "actions": [{"type": "uri", "label": "Detail", "uri": "https://example.com/1"}]
      }
    ]
  }
}
```

- Max **10** columns. `imageAspectRatio` and `imageSize` apply to all columns
- Column: `thumbnailImageUrl` (optional, JPEG/PNG, 1024px, 10MB), `title` (optional, max 40), `defaultAction` (optional)
- Column `text`: Required. **Max 120 chars** (no image/title) / **max 60 chars** (with image or title)
- Column `actions`: Max **3** action objects
- **Consistency rule**: If any column uses image or title, all columns must use them. Keep action count consistent

### Image Carousel Template
```json
{
  "type": "template",
  "altText": "Image carousel",
  "template": {
    "type": "image_carousel",
    "columns": [
      {
        "imageUrl": "https://example.com/item1.jpg",
        "action": {"type": "uri", "label": "View", "uri": "https://example.com/1"}
      }
    ]
  }
}
```

- Max **10** columns. Each has one `imageUrl` and one `action`
- Image: HTTPS, JPEG/PNG, 1:1 ratio, max 1024px wide, max 10MB, URL max 2000 chars
- `label` in action is optional (max 12 chars) — differs from other templates

## Flex Message

```json
{
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [{"type": "text", "text": "Hello, Flex!"}]
    }
  }
}
```

Full Flex Message specs → [flex-message.md](flex-message.md)

## Action Types

9 action types shared across Template, Rich Menu, Quick Reply, and Flex Message. Some are context-restricted (`camera`/`cameraRoll`/`location` = Quick Reply only, `richmenuswitch` = Rich Menu only).

Full specifications, required fields, label rules, and char limits → **[action-objects.md](action-objects.md)**

## Quick Reply

Add quick reply buttons to any message:
```json
{
  "type": "text",
  "text": "Select your favorite",
  "quickReply": {
    "items": [
      {
        "type": "action",
        "action": {"type": "message", "label": "Sushi", "text": "sushi"}
      },
      {
        "type": "action",
        "action": {"type": "location", "label": "Location"}
      },
      {
        "type": "action",
        "action": {"type": "camera", "label": "Camera"}
      }
    ]
  }
}
```

Quick Reply action types: `message`, `postback`, `uri`, `datetimepicker`, `camera`, `cameraRoll`, `location`, `clipboard`. Max 13 items.

Each button can have an optional `imageUrl` (HTTPS, PNG, 1:1 ratio, max 1MB, max 2000 chars). For `camera`/`cameraRoll`/`location` actions, a default icon is shown if `imageUrl` is omitted. Other actions show no icon if `imageUrl` is not set.

**Platform:** Quick Reply is **iOS and Android only** — not displayed on LINE desktop (macOS/Windows).

**Button lifecycle:**
- Buttons disappear after the user taps one — **except** `camera`, `cameraRoll`, `datetimepicker`, and `location` which persist until the data is sent
- Buttons disappear when any new message arrives in the chat (from the bot, user, or other members)
- If the message that caused buttons to disappear is deleted, buttons **reappear**

## Content Retrieval

Gets images, videos, audio, and files sent by users using message IDs received via the webhook. Only available when `contentProvider.type` is `line` in the webhook event.

| Operation | Method | Endpoint | Domain | Supported types |
|-----------|--------|----------|--------|-----------------|
| Get content | GET | `/v2/bot/message/{messageId}/content` | `api-data.line.me` | image, video, audio, file |
| Get preview | GET | `/v2/bot/message/{messageId}/content/preview` | `api-data.line.me` | image, video |
| Verify transcoding | GET | `/v2/bot/message/{messageId}/content/transcoding` | `api-data.line.me` | video, audio |

**Get content:**
- Response: binary data. The `Content-Type` response header indicates the file format
- Large video/audio may return `202` while binary data is being prepared — use the transcoding endpoint to check readiness
- Content may be internally transformed (e.g., shrunk). No guaranteed storage period; download promptly after webhook
- No API exists for retrieving text — text content is only available in the webhook event object

**Verify transcoding:** Gets the preparation status to get the video or audio sent by users using message IDs received via the webhook. Status values: `processing` | `succeeded` | `failed`

**Get preview:** Gets a preview image of the image or video sent by users using message IDs received via the webhook. The preview image is image data converted to a smaller data size than the original content.

**Error responses:**

| Code | Description |
|------|-------------|
| `400` | Invalid content type for this endpoint (e.g., text message ID for transcoding) |
| `404` | Message ID not found |
| `410` | Content gone (e.g., user unsent the message) |
