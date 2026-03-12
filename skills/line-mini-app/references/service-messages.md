# Service Messages

> **Verified MINI Apps only.** Unverified MINI Apps can test on the Developing channel but cannot use this feature on the Published channel.

## Overview

Service Messages allow LINE MINI Apps to send proactive notifications to users. Requires a **service notification token** (issued per user session) and a pre-registered **template**.

### Allowed Use

Service messages may **only** be sent as a confirmation or response to a user action on the MINI App.

#### Notifications allowed

| Type | Use Case |
|------|----------|
| Action Confirmation | Reservation confirmations, purchase confirmations |
| Action Result | Check-in completion, shipment completion |
| Reminder | Reservation reminders, event reminders for purchased tickets |

#### Notifications disallowed

- Notifications not tied to user actions (e.g., purchase completion when tickets were bought from a vending machine, not the MINI App)
- Advertisements, event notifications, discounts, shopping rewards, new products, coupons, promotions

**Penalty:** If unacceptable content is sent, service message API use will be **temporarily prohibited**. Repeated violations may result in the **MINI App being removed from LINE**.

See [Conditions for service messages](https://developers.line.biz/en/docs/line-mini-app/service/service-operation/#conditions-for-service-messages).

### Notification Chat Room by Region

Service messages appear in a dedicated chat room per region, regardless of which MINI App sends them:

| Region | Chat Room Name |
|--------|---------------|
| Japan | LINEミニアプリ お知らせ |
| Thailand | LINE MINI App Notice |
| Taiwan | LINE MINI App 通知 |

## Notification Token Lifecycle

```
User opens MINI App
  → liff.getAccessToken()
    → Issue notification token (server-side, 1 per LIFF access token)
      → Send service messages (up to 5 per token)
        → Token value is RENEWED after each send (unless expired or count exhausted)
```

### Key Rules

- Token expires **1 year** (31,536,000 seconds) after issuance
- Max **5 service messages** per token — the limit applies per use case (confirmation, result, reminder separately). LY Corporation may adjust per scenario and notifies at review time
- **One token per LIFF access token** — issuing multiple tokens reusing the same `liff.getAccessToken()` result is not allowed
- Each token is **bound to one user** — cannot send to other users
- Token value is **renewed** after each successful send — keep the new token for successive messages
- When `expiresIn` and `remainingCount` are both `0` in send response, the message was sent but the token could not be renewed
- **LIFF access token revocation**: if the user closes the MINI App, the LIFF access token is revoked even if it has not expired. Issue the notification token before the user leaves
- Each user action is identified by `sessionId` in the response

### Channel Access Token

**Stateless channel access tokens are recommended.**

- Long-lived channel access tokens: **cannot be used** for MINI App channels
- Channel access token v2.1 (user-specified expiration): **cannot be used** for MINI App channels
- Stateless channel access tokens: **recommended** (unlimited issuances, no lifecycle management needed)
- Short-lived channel access tokens: supported but not recommended

## Issue Notification Token

```
POST https://api.line.me/message/v3/notifier/token
Content-Type: application/json
Authorization: Bearer {channel access token}
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `liffAccessToken` | String | Yes | LIFF access token from `liff.getAccessToken()` |

### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| `notificationToken` | String | Service notification token |
| `expiresIn` | Number | Seconds until expiry (31,536,000 = 1 year) |
| `remainingCount` | Number | Remaining sends (starts at 5) |
| `sessionId` | String | Session identifier — identifies the user action that triggered the token |

```json
{
  "notificationToken": "34c11a03-b726-49e3-8ce0-949387a9..",
  "expiresIn": 31536000,
  "remainingCount": 5,
  "sessionId": "xD06...."
}
```

### Error Responses

| Status | Description |
|--------|-------------|
| 400 Bad Request | Invalid request body, or same LIFF access token used multiple times in rapid succession |
| 401 Unauthorized | Invalid channel access token or invalid/revoked LIFF access token. Note: LIFF access token is revoked when user closes the LIFF app, even if not expired |
| 403 Forbidden | Channel not authorized to issue service messages |
| 500 Internal Server Error | Server error |

## Send Service Message

```
POST https://api.line.me/message/v3/notifier/send?target=service
Content-Type: application/json
Authorization: Bearer {channel access token}
```

### Query Parameters

| Parameter | Value | Required |
|-----------|-------|----------|
| `target` | `service` | Yes |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `templateName` | String | Yes | Template name with BCP 47 language tag. Format: `{name}_{tag}`. Max 30 characters |
| `params` | Object | Yes | Template variable key-value pairs. Use empty object `{}` if template has no variables |
| `notificationToken` | String | Yes | Service notification token |

#### Template Variables

The `params` object specifies values for template variables. Required variables must be provided or an error is returned.

Button destination URIs can be set dynamically using `button_uri_1`, `button_uri_2`, etc.:

```json
{
  "params": {
    "variable-name": "value",
    "button_uri_1": "detailView?userId=1234&purchaseID=5678"
  }
}
```

### Supported Languages

| Language | BCP 47 Tag |
|----------|------------|
| Japanese | `ja` |
| English | `en` |
| Traditional Chinese | `zh-TW` |
| Thai | `th` |
| Indonesian | `id` |
| Korean | `ko` |

### Response (200)

Returns a **renewed** notification token. Use this for successive sends.

| Field | Type | Description |
|-------|------|-------------|
| `notificationToken` | String | Renewed token (use for next send) |
| `expiresIn` | Number | Seconds until renewed token expires |
| `remainingCount` | Number | Remaining sends after this message |
| `sessionId` | String | Session identifier |

```json
// Token renewed successfully
{
  "notificationToken": "c9884874-bf6a-4241-8999-2767241c...",
  "expiresIn": 31535906,
  "remainingCount": 3,
  "sessionId": "xD06...."
}

// Message sent but token could not be renewed
{
  "expiresIn": 0,
  "remainingCount": 0
}
```

### Error Responses

| Status | Description |
|--------|-------------|
| 400 Bad Request | Invalid request body, or target recipient doesn't exist |
| 401 Unauthorized | Invalid channel access token or invalid service notification token |
| 403 Forbidden | Channel not authorized to send service messages, or specified template not found |

## Template Management

- Add service message templates via the LINE Developers Console on the LINE MINI App channel
- Maximum **20 templates per channel**
- Templates are organized by **category** (store reservations, queue management, delivery notifications) and available in **6 languages**
- Modifying any template on a verified MINI App requires **re-review** (see [console-setup.md § Re-review](console-setup.md#re-review-after-updating-a-verified-mini-app))

### Preview and Testing

In the Console, select the LINE MINI App channel > **Service message template** tab > **Add**. You can:
- Preview messages with template variables
- Send **test messages** to the LINE account logged into the Console

### Template Review

Templates must **pass review by LY Corporation** before they can be used with the Sending service messages API.

### Template Published Status

| Status | Description |
|--------|-------------|
| `DEVELOPING` | Only available for sending to developers with **Admin or Tester** privileges, from a channel ready for publication |
| `PUBLISHING` | Passed review. Used to send to users from the production channel |

### Template Lifecycle Permissions

| Operation | Developing | Reviewing | Published |
|-----------|:---------:|:---------:|:---------:|
| Add new template | ✅ | ❌ | ✅ |
| List all templates | ✅ | ✅ | ✅ |
| View template detail | ✅ | ✅ | ✅ |
| Edit use case | ✅ | ❌ | ✅ |
| Delete template | ✅ | ❌ | ✅ |
| Send test message | ✅ | ✅ | ✅ |

> If templates are used in a manner deviating from the **Use Case** explanation, LY Corporation may prevent their use.

## Template Structure

A service message template consists of four sections:

| Section | Description |
|---------|-------------|
| **(A) Title** | Title (A-1) + Subtitle (A-2) |
| **(B) Detail** | Content area with two layout types (see below) |
| **(C) Button** | Number varies per template. Only buttons with configured URLs are displayed. Use [permanent links](https://developers.line.biz/en/docs/line-mini-app/develop/permanent-links/). First button is required |
| **(D) Footer** | Channel icon + channel name (from Basic settings). Tapping opens the MINI App top page |

> **Footer when not "Reflected":** If status is "Not yet reviewed" or "Reviewing", the LINE icon and "Service Message" text are shown instead of the channel icon and name.

### Detail Layout Types

| Layout | Required keys | Max keys |
|--------|:------------:|:--------:|
| **detailed** | 1 | Template-dependent |
| **simple** | 0 | 1 |

### Character Limits

| Layout | Recommended | Soft limit | Hard limit |
|--------|:-----------:|:----------:|:----------:|
| **detailed** | 10 | 36 | 50 |
| **simple** | 32 | 100 | 150 |

| Characters vs limit | Display |
|--------------------|---------|
| ≤ Recommended | All text displayed |
| > Recommended, ≤ soft limit | May be truncated with `...` |
| > Soft limit, ≤ hard limit | Truncated with `...` |
| > Hard limit | **Error** — message cannot be sent |

Characters are counted in **grapheme cluster** units (not UTF-16 code units). See [Character counting in a text](https://developers.line.biz/en/docs/messaging-api/text-character-count/).

## Sending Flow

### First-Time Send

1. Call `liff.getAccessToken()` in the MINI App to get the LIFF access token
2. Send the LIFF access token to your server
3. Obtain a **channel access token** (stateless recommended)
4. **Issue notification token** using both the channel access token and LIFF access token
5. **Send service message** using the notification token. **Save the renewed token** from the response

> If the user closes the MINI App, the LIFF access token is revoked even if still valid. Issue the notification token before the user leaves.

### Subsequent Sends

Use the notification token from the **previous response**. Do **not** re-issue the token using channel/LIFF access tokens.

Always save the renewed `notificationToken` from each response. You can send as many times as `remainingCount` allows.

## Implementation Pattern

```javascript
// 1. Client: get LIFF access token
const accessToken = liff.getAccessToken();

// 2. Send to your server
const res = await fetch('/api/issue-token', {
  method: 'POST',
  body: JSON.stringify({ liffAccessToken: accessToken })
});

// 3. Server: issue notification token
// POST https://api.line.me/message/v3/notifier/token
// { "liffAccessToken": "<from client>" }
// → Store notificationToken for this user

// 4. Server: send service message (later)
// POST https://api.line.me/message/v3/notifier/send?target=service
// { "templateName": "order_confirm_zh-TW", "params": {...}, "notificationToken": "..." }
// → Store RENEWED notificationToken from response for next send
```
