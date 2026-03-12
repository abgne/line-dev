# Sending API Reference

## Table of Contents
- [Send (Template)](#send-line-notification-message-template)
- [Send (Flexible)](#send-line-notification-message-flexible)
- [Count (Template)](#get-count-template)
- [Count (Flexible)](#get-count-flexible)
- [Template vs Flexible Comparison](#comparison)

---

## Send LINE Notification Message (Template)

Send a notification using premade template keys. No UX review required.

### HTTP Request

`POST https://api.line.me/v2/bot/message/pnp/templated/push`

### Rate Limit

2,000 requests per second

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `application/json` |
| `Authorization` | Yes | `Bearer {channel_access_token}` |
| `X-Line-Delivery-Tag` | No | Tracking string (16–100 chars). Returned in delivery webhook `delivery.data`. |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | String | Yes | SHA256-hashed E.164 phone number |
| `templateKey` | String | Yes | Template key (e.g., `shipment_completed_ja`) |
| `body` | Object | No | Message content object |
| `body.emphasizedItem` | Object | No | Single emphasized item (max 1) |
| `body.items` | Array | No | Item array (max 15) |
| `body.buttons` | Array | No | Button array (max 2) |

#### Item Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `itemKey` | String | Yes | Item key (e.g., `date_002_ja`) |
| `content` | String | Yes | Display value. Max **15 chars** for emphasizedItem, **300 chars** for items. |

#### Button Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `buttonKey` | String | Yes | Button key (e.g., `contact_ja`) |
| `url` | String | Yes | URL opened on tap. Max **1000 chars**. |

**Rules:**
- Cannot specify the same itemKey more than once
- Cannot duplicate itemKey between `emphasizedItem` and `items`

### Example Request

```sh
curl -v -X POST https://api.line.me/v2/bot/message/pnp/templated/push \
-H 'Authorization: Bearer {channel_access_token}' \
-H 'Content-Type: application/json' \
-H 'X-Line-Delivery-Tag: 15034552939884E28681A7D668CEA94C...' \
-d '{
    "to": "d41e0ad70dddfeb68f149ad6fc61574b9c5780ab7bcb2fba5517771ffbb2409c",
    "templateKey": "shipment_completed_ja",
    "body": {
        "emphasizedItem": {
            "itemKey": "date_002_ja",
            "content": "Saturday, August 10, 2024"
        },
        "items": [
            {"itemKey": "time_range_001_ja", "content": "A.M."},
            {"itemKey": "number_001_ja", "content": "1234567"},
            {"itemKey": "price_001_ja", "content": "120 USD"},
            {"itemKey": "name_010_ja", "content": "Frozen Soup Set"}
        ],
        "buttons": [
            {"buttonKey": "check_delivery_status_ja", "url": "https://example.com/CheckDeliveryStatus/"},
            {"buttonKey": "contact_ja", "url": "https://example.com/ContactUs/"}
        ]
    }
}'
```

### Response

Status code `202 Accepted` with empty JSON object `{}`.

### Error Responses

| Code | Description |
|------|-------------|
| 400 | Invalid destination, invalid message object, or unauthorized template |
| 403 | Account not authorized for notification messages |
| 422 | No matching user, wrong country, user refused, or privacy policy not agreed |

```json
// Invalid template (400)
{"message": "Invalid templateKey: reserve_004", "details": [{"message": "The specified template doesn't exist, or you don't have the permission", "property": "templateKey"}]}

// Duplicate item (400)
{"message": "The request body has 1 error(s)", "details": [{"message": "Duplicate itemKey in items or between emphasizedItem and items are not allowed: date_002_ja", "property": "body.emphasizedItem.itemKey"}]}

// Invalid hash (400)
{"message": "The request body has 1 error(s)", "details": [{"message": "The value must be a valid SHA-256 digest.", "property": "to"}]}

// No permission (403)
{"message": "Access to this API is not available for your account"}

// Send failed (422)
{"message": "Failed to send messages"}
```

---

## Send LINE Notification Message (Flexible)

Send a notification using custom message objects. **Requires prior UX review.**

### HTTP Request

`POST https://api.line.me/bot/pnp/push`

### Rate Limit

2,000 requests per second

### Request Headers

Same as template type.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `to` | String | Yes | SHA256-hashed E.164 phone number |
| `messages` | Array | Yes | Array of [message objects](https://developers.line.biz/en/reference/messaging-api/#message-objects). Max **5**. |

**Restrictions:** No images, video, or audio.

### Example Request

```sh
curl -v -X POST https://api.line.me/bot/pnp/push \
-H 'Authorization: Bearer {channel_access_token}' \
-H 'Content-Type: application/json' \
-d '{
    "to": "{hashed_phone_number}",
    "messages": [
        {"type": "text", "text": "Hello, world1"},
        {"type": "text", "text": "Hello, world2"}
    ]
}'
```

### Response

Status code `200 OK` with empty JSON object `{}`.

### Error Responses

| Code | Description |
|------|-------------|
| 400 | Invalid destination or invalid message object |
| 422 | No matching user, wrong country, user refused, or privacy policy not agreed |

Note: Flexible type does **not** return `403` (unlike template type).

---

## Get Count (Template)

Get number of template notification messages sent on a specific date.

### HTTP Request

`GET https://api.line.me/v2/bot/message/delivery/pnp/templated?date={yyyyMMdd}`

### Rate Limit

2,000 requests per second

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer {channel_access_token}` |

### Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `date` | Yes | Date in `yyyyMMdd` format (UTC+9). Example: `20240916` |

### Response

```json
{"status": "ready", "success": 3}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `ready` (data available), `unready` (processing, retry later), `out_of_service` (before 2018-03-31) |
| `success` | Number | Count of sent messages. Only present when `status` is `ready`. |

### Error Response

| Code | Description |
|------|-------------|
| 400 | Invalid or missing date |

---

## Get Count (Flexible)

Get number of flexible notification messages sent on a specific date.

### HTTP Request

`GET https://api.line.me/v2/bot/message/delivery/pnp?date={yyyyMMdd}`

Same parameters, headers, response format, and errors as template count endpoint.

### Example

```sh
curl -v -X GET 'https://api.line.me/v2/bot/message/delivery/pnp?date=20211231' \
-H 'Authorization: Bearer {channel_access_token}'
```

---

## Comparison

| Aspect | Template | Flexible |
|--------|----------|----------|
| Message format | `templateKey` + `body` (items/buttons) | `messages` array (standard message objects) |
| UX Review | Not required | **Required** before sending |
| Send endpoint | `POST /v2/bot/message/pnp/templated/push` | `POST /bot/pnp/push` |
| Count endpoint | `GET /v2/bot/message/delivery/pnp/templated` | `GET /v2/bot/message/delivery/pnp` |
| Send response code | **202** Accepted | **200** OK |
| Error codes | 400, **403**, 422 | 400, 422 |
| Max messages | 1 template per request | 5 message objects per request |
| Media | No images/video/audio | No images/video/audio |
| History | Added June 2025 | Original type (renamed from "LINE notification messages") |
