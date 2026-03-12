# In-App Purchase

> **Application required.** Must apply to use the in-app purchase feature. See [In-app purchase overview](https://developers.line.biz/en/docs/line-mini-app/in-app-purchase/overview/).

> **Currently available in Japan only.** In-app purchase via app store (App Store / Google Play) is only available for LINE MINI Apps in Japan. For other regions, use LINE Pay or other payment methods. See [Using payment systems](https://developers.line.biz/en/docs/line-mini-app/develop/payment/).

> **Review coordination:** Cannot submit a MINI App verification review while an IAP application is under review, and vice versa. Apply for IAP first, wait for approval, then submit the verification review with the "Apply to publish in-app purchase" toggle enabled. See [submission-review.md](submission-review.md).

> **Consumable only.** Currently, only consumable digital content is available for purchase.

## Requirements

### Use Conditions

The LINE MINI App channel must have both **"Region to provide the service"** and **"Company or owner's country or region"** set to **"Japan"**.

### Environment Requirements

| Requirement | Detail |
|-------------|--------|
| MINI App status | Verified MINI App (unverified works only on Developing and Review channels) |
| LIFF SDK version | **2.26.0** or later |
| Runtime | LIFF browser only (not available in external browsers) |
| User phone | Japanese phone number registered with LINE account |
| LINE version | **15.6.0** or later |

### Environment Check

Use `liff.isApiAvailable()` to check IAP support before showing purchase UI:

```javascript
if (!liff.isApiAvailable("iap")) {
  // Disable MINI App or hide purchase flow
}
```

**Important:** Even if `liff.isApiAvailable()` returns true, IAP can't be used if user consent cannot be obtained or is later revoked.

## Items and Pricing

- Purchasable items are **pre-defined by LY Corporation**, priced in Japanese yen
- You cannot create custom products — only use pre-defined items
- When displaying items, **always use localized prices** from `liff.iap.getPlatformProducts()` to match the user's app store region
- This minimizes discrepancy between displayed price and actual app store price

## System Architecture

| Component | Role |
|-----------|------|
| LINE MINI App | Receives user actions, initiates purchase transaction |
| LINE MINI App server | Reserves purchases, receives webhooks, manages purchase results |
| LINE Platform | Verifies store payments, sends webhook events |
| App store | Performs actual payment (iOS: App Store, Android: Google Play) |

## Purchase Flow

```
1. Client: liff.isApiAvailable("iap")    → Check environment compatibility
2. Client: getPlatformProducts()          → Query available products and prices
3. Client: requestConsentAgreement()      → User agrees to IAP Terms of Use
4. Server: POST /iap/v1/product/reserve   → Reserve purchase, get orderId
5. Client: createPayment({ orderId })     → Launch app store payment screen
6. Server: Webhook (purchaseComplete)     → Confirm payment, grant item
7. Server: Webhook (refundComplete)       → Handle refund, revoke item
```

**A successful reservation does NOT guarantee purchase completion.** Always grant items based on the `purchaseComplete` webhook event, not the reserve response.

## Client APIs

All client APIs are LIFF browser only. Not available in external browsers.

### liff.iap.getPlatformProducts()

Gets available products and localized prices from the app store.

```javascript
liff.iap.getPlatformProducts({ productIds });
```

#### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `productIds` | String[] | Yes | Array of product IDs to retrieve |

#### Return Value

`Promise<Object>` — keyed by product ID:

| Field | Type | Description |
|-------|------|-------------|
| `currency` | String | ISO 4217 currency code (localized to user's app store region) |
| `price` | Number | Price (localized to user's app store region) |
| `productName` | String | Item name (localized) |

```json
{
  "iap_ln_002": {
    "currency": "JPY",
    "price": 100,
    "productName": "LINE Purchase 100"
  }
}
```

#### Errors

| Error Message | Description |
|---------------|-------------|
| Need access_token for api call, Please login first | User not logged in |
| In-App Purchase is not allowed in external browser | Called outside LIFF browser |
| In-App Purchase is not allowed in this LIFF app | MINI App not approved for IAP |

### liff.iap.requestConsentAgreement()

Requests user consent for the [Terms of Use: LINE In-App Purchase System](https://terms.line.me/line_iap_tou_1?lang=en). Displays consent screen if user hasn't agreed or re-consent is needed.

**Always call before starting a purchase** — Terms may be updated, requiring re-consent.

```javascript
await liff.iap.requestConsentAgreement();
```

#### Consent Scope

- Consent is **per user, NOT per MINI App** — if a user already agreed in another MINI App, re-consent is not required
- If Terms of Use are updated, users may need to re-consent
- Users who haven't consented **cannot reserve or initiate purchases**
- Display consent screen at an appropriate time to avoid user drop-off

#### Return Value

`Promise<void>` — resolves if user agrees, rejects otherwise.

#### Errors

| Error Message | Description |
|---------------|-------------|
| The user did not agree to the terms. | User declined (error code: `TERMS_AGREEMENT_ERROR`) |
| Need access_token for api call, Please login first | User not logged in |
| In-App Purchase is not allowed in external browser | Called outside LIFF browser |
| In-App Purchase is not allowed in this LIFF app | MINI App not approved for IAP |

### liff.iap.createPayment()

Launches the app store payment screen (App Store / Google Play) and starts the purchase transaction.

```javascript
liff.iap.createPayment({ productId, orderId });
```

#### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `productId` | String | Yes | Product ID |
| `orderId` | String | Yes | Order ID from the Reserve Purchase response |

#### Return Value

`Promise<void>` — resolves on successful purchase, rejects on cancel or failure.

On success, LINE Platform verifies the payment with the store and sends a `purchaseComplete` webhook event.

#### Error Handling

On cancel or failure, the promise rejects with an object containing `code` and `message`:

```javascript
try {
  await liff.iap.createPayment({ productId, orderId });
} catch (e) {
  // e => { code: "CANCELED", message: "Transaction was canceled." }
  console.error({ code: e.code, message: e.message });
}
```

#### Errors

| Error Message | Description |
|---------------|-------------|
| Need access_token for api call, Please login first | User not logged in |
| In-App Purchase is not allowed in external browser | Called outside LIFF browser |
| In-App Purchase is not allowed in this LIFF app | MINI App not approved for IAP |

## Server APIs

### Response Headers

All IAP server responses include:

| Header | Description |
|--------|-------------|
| `x-line-request-id` | Request ID. **Save to logs** for future inquiries to LY Corporation |

### Error Response Format

4xx/5xx responses return:

| Field | Type | Always | Description |
|-------|------|--------|-------------|
| `errorCode` | String | Yes | Error code |
| `message` | String | Yes | Error message |
| `details` | Array | No | Error details |
| `details[].message` | String | No | Detailed message |
| `details[].property` | String | No | Property where error occurred |

```json
{
  "errorCode": "VALIDATION_ERROR",
  "message": "Request validation failed.",
  "details": [
    {
      "message": "'clientOs' must be 'android' or 'ios'. Actually received: 'INVALID'",
      "property": "clientOs"
    }
  ]
}
```

### Non-Breaking Changes

LINE may make non-breaking additions without advance notice:

- Addition of new endpoints, optional parameters, fields, and headers
- Addition of enum values and webhook event properties
- Changes to property order in responses and webhook objects
- Changes to whitespace or line breaks between data elements

Implement your server to handle these gracefully (e.g., ignore unknown fields, don't rely on property order).

### Reserve Purchase

Reserves a purchase before starting app store payment. **Must be called before `createPayment()`.**

```
POST https://api.line.me/iap/v1/product/reserve
Content-Type: application/json
Authorization: Bearer {user access token}
```

**Note:** Uses **user access token** (from `liff.getAccessToken()`), not channel access token.

**Required:** Before calling this endpoint, use the [Verify access token validity](https://developers.line.biz/en/reference/line-login/#verify-access-token) endpoint to verify the access token validity, channel ID, and token expiry on the server side.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `clientIp` | String | Yes | User's device IP (IPv4 or IPv6), obtained server-side |
| `clientOs` | String | Yes | `ios` or `android` (from `liff.getOS()`) |
| `productId` | String | Yes | Product ID to purchase |
| `shopProductName` | String | Yes | Item name in purchase history. Max 20 chars (UTF-16). No emojis or symbols |

#### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| `orderId` | String | Order ID. **Save for inquiries.** Pass to `createPayment()` |

```json
{ "orderId": "T2025020710000002126002" }
```

#### Error Codes

| Error Code | Description |
|------------|-------------|
| `VALIDATION_ERROR` | Invalid request (e.g. `clientOs` not `ios`/`android`) |
| `WEBHOOK_URL_IS_NOT_SET` | Webhook URL for payment notifications not configured |
| `PRODUCT_ID_NOT_FOUND` | Product ID doesn't exist |
| `BLOCKED_USER` | Fraudulent user, blocked by LINE Platform |
| `INTERNAL_SERVER_ERROR` | Temporary issue. Retry with exponential backoff |
| `TERMS_AGREEMENT_ERROR` | User hasn't agreed to latest Terms of Use |

### Get Webhook Event History

Retrieves webhook events sent by the LINE Platform. Cursor-based pagination, max 100 events per page. Only events from the **past 7 days**.

Currently only `purchaseComplete` events are available. `refundComplete` events will be supported in the future.

```
GET https://api.line.me/iap/v1/webhook/events
Authorization: Bearer {channel access token}
```

**Note:** Uses **channel access token**, not user access token.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `startEpochSeconds` | Number | Yes | Start time (UNIX seconds, within past 7 days, inclusive) |
| `endEpochSeconds` | Number | Yes | End time (UNIX seconds, within past 7 days, inclusive) |
| `pageSize` | Number | Yes | Events per page (1–100) |
| `cursor` | String | No | Pagination cursor. Omit for first request, use `nextCursor` from previous response for subsequent requests |
| `status` | String | No | `SUCCESS` or `FAILED`. Omit for all events |

**Do not change parameters other than `cursor` during pagination.** To change parameters, start from page 1 again.

#### Response (200)

| Field | Type | Always | Description |
|-------|------|--------|-------------|
| `events` | Array | Yes | List of webhook events |
| `events[].transactionType` | String | Yes | Always `PRODUCT` |
| `events[].event` | Object | Yes | Webhook event payload |
| `nextCursor` | String | No | Cursor for next page. `null` if no more pages |

```json
{
  "events": [
    {
      "transactionType": "PRODUCT",
      "event": {
        "type": "purchaseComplete",
        "orderId": "T2025020710000002126002",
        "productId": "iap_ln_002",
        "userId": "U91FC5A...",
        "purchaseTimestamp": 1738672496,
        "channelId": "12345..."
      }
    }
  ],
  "nextCursor": "MTY3NjU0"
}
```

#### Error Codes

| Error Code | Description |
|------------|-------------|
| `VALIDATION_ERROR` | Invalid parameters (e.g. `status` not `SUCCESS`/`FAILED`) |
| `INTERNAL_SERVER_ERROR` | Temporary issue. Retry with exponential backoff |

## Webhook Events

### Signature Verification

Verify the `x-line-signature` request header to prevent forged requests:

1. Calculate HMAC-SHA256 digest of the request body using the **channel secret** as the key
2. Base64-encode the digest
3. Compare with the `x-line-signature` header value

See [Verify webhook signature](https://developers.line.biz/en/docs/messaging-api/verify-webhook-signature/) for details and code examples.

### Webhook Processing Requirements

#### Response

- Return HTTP **2xx** status on successful processing
- Any other status (3xx, 4xx, 5xx) → LINE Platform treats as failure → automatic **redelivery multiple times within 30 minutes**
- The LINE Platform does not verify response content — any payload is accepted

#### Deduplication

The same webhook event may be delivered multiple times due to network conditions. Use `orderId` to:
- Ensure items are not granted multiple times for a single purchase
- Ensure cancel processing is not performed multiple times

#### Recovery

Use the [Get Webhook Event History](#get-webhook-event-history) endpoint to recover missed webhook events.

### Purchase Complete Event

Occurs when user purchases an item and payment is settled by LY Corporation.

**Grant items based on this event, not on reserve success.**

| Field | Type | Description |
|-------|------|-------------|
| `type` | String | `purchaseComplete` |
| `orderId` | String | Order ID (matches reserve response) |
| `productId` | String | Product ID |
| `userId` | String | Purchaser's user ID |
| `purchaseTimestamp` | Number | Payment completion time on LINE Platform (UNIX seconds). Not the user's actual payment time |
| `channelId` | String | MINI App channel ID |

```json
{
  "type": "purchaseComplete",
  "orderId": "T2025020710000002126002",
  "productId": "iap_ln_002",
  "userId": "U91FC5A...",
  "purchaseTimestamp": 1738672496,
  "channelId": "12345..."
}
```

### Refund Event

Occurs when a refund is issued for a purchased item. **Note:** Missed `refundComplete` events cannot be recovered via the Get Webhook Event History endpoint — that endpoint currently only supports `purchaseComplete` events.

| Field | Type | Description |
|-------|------|-------------|
| `type` | String | `refundComplete` |
| `orderId` | String | Order ID of the refunded purchase |
| `productId` | String | Product ID |
| `userId` | String | User who requested refund |
| `purchaseTimestamp` | Number | Original purchase time (matches `purchaseComplete` event). Not the refund time |
| `channelId` | String | MINI App channel ID |

```json
{
  "type": "refundComplete",
  "orderId": "T2025020710000002126002",
  "productId": "iap_ln_002",
  "userId": "U91FC5A...",
  "purchaseTimestamp": 1738672496,
  "channelId": "12345..."
}
```

## Development Guidelines

### Prohibited

- **Don't restrict webhook access by IP address.** The LINE Platform's IP is not disclosed and may change without notice. Use [signature verification](#signature-verification) instead.

### Required

- **Verify access token validity** before calling Reserve Purchase. Use the [Verify access token validity](https://developers.line.biz/en/reference/line-login/#verify-access-token) endpoint to check the token validity, channel ID, and expiry on the server side.

### Recommended

- **Verify webhook signature** — always verify `x-line-signature` to prevent forged requests
- **Deduplicate webhook events** — use `orderId` to prevent granting items or processing cancels multiple times
- **Handle errors properly** — reservation doesn't guarantee payment completion. Retry or prompt user on network errors
- **Don't send duplicate payment notifications** — LINE automatically notifies users on purchase completion and cancellation via the "LINE In-App Purchase Notifications" official account. Don't duplicate from another OA.

## Application & Setup

### Getting Started Flow

| Step | Details |
|------|---------|
| 1. Apply | In-app purchase tab on LINE Developers Console. Can apply even with unverified MINI App |
| 2. Set up | After approval: register webhook URL and testers in In-app purchase settings tab |
| 3. Integrate & test | Implement on Developing channel, perform test payments |
| 4. Verification review | Apply from Review request tab with "Release the in-app purchase feature" toggle on. If adding IAP to already-verified MINI App, re-review is required |
| 5. Release | After verification review approval, release the MINI App |

### IAP Review Period

- Approximately **2 weeks** for LY Corporation to complete review
- Cannot specify completion date
- If rejected: re-application and re-review take additional days
- After IAP approval, the **verification review** has a separate review period

### Application Information

When applying, enter all information accurately. The following must **all match** the "Service company information" on the Business information tab:

| Section | Field |
|---------|-------|
| Business information / LINE MINI App information | Company name |
| Information security | Name of the organization performing the operations |
| LY Corporation business partner information form | Your company information - Company name |
| LY Corporation business partner information form | Payment account information - Account holder name |

### Modifying Application Information

| Scenario | Action |
|----------|--------|
| Status "Applied for review" | Cancel application first, then edit and re-apply |
| Status "Reviewing" | Cannot cancel or edit. Wait for review completion |
| Changes in "In-app purchase settings" tab (webhook URL, testers) | Edit directly — no re-review required |
| Changes in "Apply to use in-app purchase" tab | Must re-apply for IAP review |
| Changes to company information | Complete verification review re-application first, then re-apply for IAP review |

### Webhook URL Registration

Register webhook URLs in the **In-app purchase settings** tab (visible only after IAP approval):

| Environment | Field |
|-------------|-------|
| Developing | Webhook URL for developing (receives test payment notifications) |
| Published | Webhook URL for published |

- URL must start with `https://`
- You can set the same URL for both environments

### Test Payment

Test payments can be made in a **Developing channel** without actual billing. When a tester performs payment on a Developing channel, it's treated as a test payment.

#### Tester Requirements

- Must have **Admin** or **Tester** role on the LINE MINI App channel
- Must have **tester permission** enabled in the In-app purchase settings tab
- Maximum **20 testers**
- Tester permission validity: **30 days** (can extend)

#### Test Procedure

1. Register a tester in the In-app purchase settings tab (select from accounts already added in Roles tab)
2. Share the LIFF URL of the Developing channel with the tester
3. Tester launches the MINI App from the LIFF URL and performs payment

#### Manage Tester Permissions

- **Extend**: Click Extend to reset expiration to 30 days from now
- **Disable**: Immediately revoke test payment permission
- **Re-enable**: Select expired tester from dropdown and enable again

## Cancellation and Refunds

LY Corporation **does not support cancellations** of completed in-app purchases.

For fraudulent use or accidental payment, instruct users to request a refund directly from the app store:

- **Apple**: [Request a refund for apps or content](https://support.apple.com/en-us/118223)
- **Google Play**: [Google Play refund policies](https://support.google.com/googleplay/answer/2479637)

## Purchase History and Notifications

### Automatic Notifications

On purchase completion or cancellation, an automatic message is sent from the **"LINE In-App Purchase Notifications"** official account. Developers don't need to send additional notifications.

- Users **cannot block** this account or change notification settings
- In rare cases, notifications may not be delivered due to environment or server conditions

### User Purchase History

Users can view purchase history via:
1. **LINE Settings** → "In-app purchases"
2. Messages from the "LINE In-App Purchase Notifications" account

**Retention:** Purchase history is viewable for up to **1 year**.

**History display includes:**

| # | Content | Source |
|---|---------|--------|
| 1 | Item name | `shopProductName` from reserve request |
| 2 | Service name | Japanese: "LINEミニアプリ \<service name\>", Other: "LINE MINI App \<service name\>" |
| 3 | App store info | Which store (App Store / Google Play) + item name |
| 4 | Payment time | LINE Platform confirmation time (not user's payment time) |
| 5 | Currency and price | Converted to user's app store region at time of payment |

## Key Constraints

- **Reserve ≠ Purchase** — always wait for `purchaseComplete` webhook before granting items
- **Auth tokens differ by endpoint**: Reserve uses user access token, webhook history uses channel access token
- **orderId**: save it — required for all inquiries to LY Corporation
- **x-line-request-id**: save it — required for debugging with LY Corporation
- **Webhook history**: only past 7 days, only `purchaseComplete` events (refund support coming)
- **Webhook redelivery**: failed deliveries retried multiple times within 30 minutes
- **Pagination**: don't change query params mid-pagination
- **purchaseTimestamp**: LINE Platform settlement time, not user's actual payment time
- **shopProductName**: max 20 UTF-16 chars, no emojis/symbols — displayed as-is in user's purchase history
- **Consumable only**: only consumable digital content is supported
- **No IP restriction on webhook servers**: LINE Platform IP is undisclosed and may change
- **No duplicate notifications**: LINE auto-notifies on purchase and cancellation — don't send additional notifications from your OA
