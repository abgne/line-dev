# Coupon

Create and manage coupons for LINE Official Account. Coupons are created via API, then **sent as messages** using coupon message objects (see [message-objects.md](message-objects.md)).

## Limits

| Item | Limit |
|------|-------|
| Valid coupons per channel | **5,000** |
| Rate limit (all coupon endpoints) | 200 req/sec |

**Key constraints:**
- Coupons **cannot be edited** after creation — discontinue and recreate
- Discontinued coupons **cannot be reactivated**
- No "draft" status via API (only available in LINE Official Account Manager)
- Image is fetched and stored at creation time — **changing the URL later won't update the image**
- Coupon image displays at **1.51:1** aspect ratio; square images will be cropped top/bottom
- Users cannot reuse a coupon marked as "used" (even accidental)
- "Friend referral" acquisition type can only be created from OA Manager, not API

## Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create | POST | `/v2/bot/coupon` |
| Discontinue | PUT | `/v2/bot/coupon/{couponId}/close` |
| List | GET | `/v2/bot/coupon` |
| Get details | GET | `/v2/bot/coupon/{couponId}` |

All require `Authorization: Bearer {channel access token}`.

## Create Coupon

`POST https://api.line.me/v2/bot/coupon`

```json
{
  "title": "Friends-only coupon",
  "description": "Present this screen at checkout.\nRedeemable once only.",
  "reward": {
    "type": "discount",
    "priceInfo": {"type": "fixed", "fixedAmount": 100}
  },
  "acquisitionCondition": {"type": "normal"},
  "maxUseCountPerTicket": 1,
  "startTimestamp": 0,
  "endTimestamp": 1924959599,
  "timezone": "ASIA_TOKYO",
  "visibility": "UNLISTED"
}
```

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | String | Coupon title. Max **60** chars |
| `reward` | Object | Reward object (see below) |
| `acquisitionCondition` | Object | Acquisition conditions (see below) |
| `maxUseCountPerTicket` | Number | `1`: once only. `-1`: unlimited |
| `startTimestamp` | Number | Start time (UNIX seconds) |
| `endTimestamp` | Number | End time (UNIX seconds). Must be after start and current time |
| `timezone` | String | Timezone for validity period (e.g., `ASIA_TOKYO`, `ASIA_TAIPEI`, `ASIA_BANGKOK`) |
| `visibility` | String | `PUBLIC`: show in LY Corp services. `UNLISTED`: don't show |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `description` | String | Usage guidelines. Max **1,000** chars. Supports `\n` |
| `imageUrl` | String | HTTPS, JPEG/PNG, max 10MB (1MB recommended), max 2000 chars |
| `couponCode` | String | Code displayed after opening. Max **16** chars |
| `barcodeImageUrl` | String | Barcode image URL. Same specs as `imageUrl` |
| `usageCondition` | String | Usage conditions text. Max **100** chars |

### Reward Object

| Property | Type | Description |
|----------|------|-------------|
| `type` | String | **Required.** `discount` / `free` / `gift` / `cashBack` / `others` |
| `priceInfo` | Object | Required when `type` is `discount` or `cashBack` |
| `priceInfo.type` | String | For discount: `fixed` / `percentage` / `explicit`. For cashBack: `fixed` / `percentage` |
| `priceInfo.fixedAmount` | Number | Positive integer. Required when `priceInfo.type` is `fixed` |
| `priceInfo.percentage` | Number | 1–99 (%). Required when `priceInfo.type` is `percentage` |
| `priceInfo.originalPrice` | Number | Original price. Required when `priceInfo.type` is `explicit` |
| `priceInfo.priceAfterDiscount` | Number | Discounted price. Required when `priceInfo.type` is `explicit` |

Currency is auto-set by region: TWD (Taiwan), THB (Thailand), JPY (all others).

### Acquisition Condition Object

| Property | Type | Description |
|----------|------|-------------|
| `type` | String | **Required.** `normal` (no conditions) / `lottery` |
| `lotteryProbability` | Number | 1–99 (%). Required when `type` is `lottery` |
| `maxAcquireCount` | Number | Max winners (1–999999, or `-1` for unlimited). Required when `type` is `lottery` |

### Response

```json
{"couponId": "01JYNW8JMQVFBNWF1APF8Z3FS7"}
```

## Discontinue Coupon

`PUT https://api.line.me/v2/bot/coupon/{couponId}/close`

- Users who received it can no longer acquire it
- Users who already obtained it can no longer use it
- **Cannot be reactivated**
- Returns `200` with `{}`
- `410` if already discontinued, `404` if not found

## List Coupons

`GET https://api.line.me/v2/bot/coupon`

Includes coupons created via both API and LINE Official Account Manager.

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | Number? | Max results (default 20, max 100) |
| `start` | String? | Continuation token from previous response's `next` (valid 24 hours) |
| `status` | String? | Filter: `DRAFT`, `RUNNING`, `CLOSED` (comma-separated for OR) |

Response: `items[]` with `couponId` and `title`, optional `next` token.

## Get Coupon Details

`GET https://api.line.me/v2/bot/coupon/{couponId}`

Returns full coupon object with all creation properties plus:

| Property | Type | Description |
|----------|------|-------------|
| `status` | String | `DRAFT` / `RUNNING` / `CLOSED` |
| `createdTimestamp` | Number | Creation time (UNIX seconds) |
| `maxTicketPerUser` | Number | Coupons per user (1, or 1–30 for referral type) |

## Sending Coupons

Use the coupon message object in any sending endpoint (Reply, Push, Multicast, Narrowcast, Broadcast):

```json
{"type": "coupon", "couponId": "01JYNW8JMQ...", "deliveryTag": "2025_winter_campaign"}
```

- `deliveryTag`: Optional (max 30, `[a-zA-Z0-9_]`). Path name for coupon insights. Defaults to `Unknown`

## Common Timezone Values

| Value | UTC Offset |
|-------|-----------|
| `ASIA_TAIPEI` | UTC+8 |
| `ASIA_TOKYO` | UTC+9 |
| `ASIA_BANGKOK` | UTC+7 |
| `AMERICA_NEW_YORK` | UTC-5 |
| `EUROPE_LONDON` | UTC+0 |
