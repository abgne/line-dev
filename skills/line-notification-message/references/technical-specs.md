# Technical Specifications

## Table of Contents
- [Phone Number Hashing](#phone-number-hashing)
- [Sending Conditions](#sending-conditions)
- [User Consent](#user-consent)
- [SMS Authentication](#sms-authentication)
- [API Response vs Actual Delivery](#api-response-vs-actual-delivery)
- [Non-Friend User Behavior](#non-friend-user-behavior)
- ["Important Notification" Label](#important-notification-label)
- [System Message](#system-message)
- [UX and Content Restrictions](#ux-and-content-restrictions)
- [API Configuration Warnings](#api-configuration-warnings)
- [Billing](#billing)
- [Service Availability](#service-availability)

---

## Phone Number Hashing

The `to` field in the API requires a phone number normalized to E.164 format and hashed with SHA256.

### Steps
1. **Normalize to E.164**: Include country code, remove hyphens and spaces
   - Japan: `+818000001234` (not `080-0000-1234`)
   - Thailand: `+66812345678`
   - Taiwan: `+886912345678`
2. **Hash with SHA256**: Produce a 64-character lowercase hex string

### Python Example

```python
import hashlib

phone_number = "+818000001234"
hashed = hashlib.sha256(phone_number.encode()).hexdigest()
print(hashed)
# d41e0ad70dddfeb68f149ad6fc61574b9c5780ab7bcb2fba5517771ffbb2409c
```

### Common Mistakes
- Including hyphens: `+81-80-0000-1234` → **wrong**
- Missing country code: `08000001234` → **wrong**
- Using uppercase hex: → **wrong** (must be lowercase)
- Including spaces: → **wrong**

---

## Sending Conditions

A LINE notification message is delivered only if **ALL** of the following conditions are met:

1. The phone number matches the user's LINE account
2. The phone number is valid (user has authenticated by SMS within the required period)
3. User has agreed to receive LINE notification messages
4. User has **not** blocked the LINE Official Account
5. The phone number was issued in **Japan, Thailand, or Taiwan**
6. User has agreed to [LINE's Privacy Policy (revised March 2022)](https://guide.line.me/privacy-policy_update/2022/0001/?lang=en-jp)

If any condition is not met, the message will not be delivered — but the API may still return `200` or `202`.

---

## User Consent

### Three States

| State | Description | Message Behavior |
|-------|-------------|------------------|
| **Agree (on)** | User receives notification messages | Delivered normally |
| **Reject (off)** | User refuses notification messages | Message deleted, not delivered |
| **Not set** | Neither consent nor refuse | Consent prompt sent; 24 hours to agree or message is deleted |

### Key Rules
- **Consent is comprehensive**: Once a user agrees, they receive notification messages from **ALL** LINE Official Accounts — not per-account
- **One-way toggle**: Once changed from "not set" to agree/reject, cannot return to "not set"
- **New accounts (LINE app v8.0.0 or earlier)**: Default state is "not set"
- Users can manage consent at: **Settings → Privacy → Provide usage data → LINE notification messages**

### 24-Hour Window (Not Set State)
When the user's consent is "not set":
1. User receives a consent prompt from the "LINE" system account
2. If user agrees within 24 hours → message is delivered
3. If user does not agree within 24 hours → message is deleted

---

## SMS Authentication

Users must authenticate their phone number by SMS once every **180 days** to receive notification messages.

### Exemptions
SMS authentication is **not** required when:
- Within 180 days of creating a new LINE account
- Within 180 days of changing the phone number registered to the LINE account

### Scope
- SMS authentication is **global** — once authenticated, applies to all LINE Official Accounts for 180 days
- Users can change their registered phone number during the SMS authentication process

---

## API Response vs Actual Delivery

**Critical**: A successful API response (`200` or `202`) does NOT guarantee that the message was delivered.

### Why Messages May Not Be Delivered Despite 200/202

| Scenario | API Response | Actually Delivered? |
|----------|-------------|---------------------|
| User has blocked the OA | 200/202 | **No** |
| User consent is "not set" and they reject | 200/202 | **No** |
| User consent is "not set" and they don't respond in 24h | 200/202 | **No** |
| SMS authentication required but not performed | 200/202 | **No** |
| All conditions met | 200/202 | **Yes** |

### How to Confirm Delivery
- Use the **delivery completion webhook event** (`type: "delivery"`)
- If no webhook received within 24 hours → message was NOT delivered
- Use the **count API** to verify actual send counts for billing

---

## Non-Friend User Behavior

Notification messages can be sent to users who have NOT added the LINE Official Account as a friend.

### What Happens
- User receives the notification message
- User can choose to **add as friend** (triggers `follow` webhook event) or **block** (triggers `unfollow` event)
- You may receive `unfollow` events from users who never sent `follow` events
- **Default rich menu** is displayed (set via LINE Official Account Manager or Messaging API)
- **Per-user rich menu** is NOT displayed for non-friends
- User can send messages to the OA without adding as friend → you may receive `message` or `postback` webhook events from non-friends

---

## "Important Notification" Label

Notification messages display a label next to the LINE Official Account icon.

| LINE App Language | Label Text |
|-------------------|------------|
| Japanese | `重要なお知らせ` |
| Thai | `การแจ้งเตือนสำคัญ` |
| Chinese (Simplified/Traditional) | `重要通知` |
| Other languages | `Important notification` |

Available in LINE version **15.9.0** or later (iOS, Android, iPad).

---

## System Message

Every time a notification message is sent, the "LINE" system account sends a "LINE notification message received" message to the user. This message:
- Is **always sent** — the sender cannot prevent or reduce it
- Is sent from the "LINE" system account (not your Official Account)
- Is NOT sent if the user has blocked your Official Account

---

## UX and Content Restrictions

### Purpose Limitation
LINE notification messages can only be used for purposes deemed **useful and appropriate for users**. They **cannot** be used for:
- Commercial purposes
- Advertising or promotions

### Template Type
Follow the [LINE notification messages (template) UX guidelines](https://www.lycbiz.com/sites/default/files/media/jp/download/LINE_Official_Notification_Template_UXGuideline.pdf) (Japanese only).

### Flexible Type
- Requires **prior UX review** — only messages that pass review can be sent
- Follow the [LINE notification messages (flexible) UX guidelines](https://www.lycbiz.com/sites/default/files/media/jp/download/LINE%E9%80%9A%E7%9F%A5%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8UX%E3%82%AC%E3%82%A4%E3%83%89%E3%83%A9%E3%82%A4%E3%83%B3.pdf) (Japanese only)

### Both Types
- No images, video, or audio in messages

---

## API Configuration Warnings

### Do NOT Restrict Server IP Addresses
Do NOT register server IP addresses in the Messaging API channel's **Security Settings** tab. Notification messages may originate from different IP ranges, and IP restrictions can cause sending failures.

### X-Line-Retry-Key NOT Supported
The notification messages API does not support retry keys. Do not include the `X-Line-Retry-Key` header.

---

## Billing

- Only messages **actually delivered** to the user are billed
- Messages not delivered (blocked, consent rejected, SMS auth not completed) are **not billed**
- Use the count API to check actual delivery numbers:
  - Template: `GET /v2/bot/message/delivery/pnp/templated?date=yyyyMMdd`
  - Flexible: `GET /v2/bot/message/delivery/pnp?date=yyyyMMdd`

---

## Service Availability

- Available in **Japan, Thailand, and Taiwan** only
- Phone numbers must be issued in these countries
- **Corporate users only** — requires application through LINE sales representative or [Sales partners](https://www.lycbiz.com/jp/partner/sales/)
- Cannot be used with personal LINE accounts
