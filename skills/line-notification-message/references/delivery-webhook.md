# Delivery Completion Webhook Event

When a LINE notification message is successfully delivered to the user, a dedicated webhook event is sent from the LINE Platform to your bot server's webhook URL.

## Event Structure

| Property | Type | Description |
|----------|------|-------------|
| `type` | String | Always `"delivery"` |
| `delivery` | Object | Contains delivery data |
| `delivery.data` | String | Hashed phone number, OR the string specified in `X-Line-Delivery-Tag` header |
| `mode` | String | Channel mode (e.g., `"active"`) |
| `timestamp` | Number | Unix timestamp in milliseconds |
| `webhookEventId` | String | Unique webhook event ID |
| `deliveryContext` | Object | Contains `isRedelivery` (boolean) |

## What This Event Indicates

The delivery completion event means the notification message has been **delivered to the user and can now be viewed**.

It does **NOT** indicate:
- ~~Successful API request~~
- ~~User received consent prompt~~
- ~~User consented to receive~~
- ~~User received SMS authentication prompt~~
- ~~User performed SMS authentication~~
- ~~User opened or read the message~~

## X-Line-Delivery-Tag

Used to track which message was delivered.

| When Sending | `delivery.data` Contains |
|-------------|--------------------------|
| Without `X-Line-Delivery-Tag` | Hashed phone number |
| With `X-Line-Delivery-Tag` | The same string you specified in the header |

- Min 16 characters, max 100 characters
- Useful for correlating sent messages with delivery confirmations

## Examples

### Without X-Line-Delivery-Tag

```json
{
  "destination": "Uc7472b39e21dab71c2347e02714630d6",
  "events": [
    {
      "type": "delivery",
      "delivery": {
        "data": "68df277462529930889fab80ecffdc0883906320591df93c25efc08300410fc2"
      },
      "webhookEventId": "01G17DAF0QJ7A3ERC5EJ9MAMH8",
      "deliveryContext": {
        "isRedelivery": false
      },
      "timestamp": 1650590038721,
      "mode": "active"
    }
  ]
}
```

### With X-Line-Delivery-Tag

```json
{
  "destination": "Uc7472b39e21dab71c2347e02714630d6",
  "events": [
    {
      "type": "delivery",
      "delivery": {
        "data": "15034552939884E28681A7D668CEA94C147C716C0EC9DFE8B80B44EF3B57F6BD0602366BC3menu01"
      },
      "webhookEventId": "01G17EJCGAVV66J5WNA7ZCTF6H",
      "deliveryContext": {
        "isRedelivery": false
      },
      "timestamp": 1650591346705,
      "mode": "active"
    }
  ]
}
```

## Signature Verification

- Use **channel secret** for webhook signature verification
- For LINE Chat Plus channels: use **Switcher Secret** instead

Verification method is the same as Messaging API webhooks: HMAC-SHA256 of the raw request body, base64-encoded, compared against the `x-line-signature` header.

## When Webhook Is NOT Received

If no delivery completion event is received within **24 hours** after an API response of `200` or `202`:

| Reason | Details |
|--------|---------|
| User blocked the OA | API returns 200/202 but message is not sent, no webhook fired |
| User didn't consent | Consent was "not set" and user either rejected or didn't respond in 24 hours |
| SMS auth not completed | SMS authentication was required but user didn't perform it |

## User Consent Flows

There are 4 flows depending on consent state and SMS authentication status:

### Flow 1: Already Agreed + No SMS Needed (Simplest)

```
API request → 200/202
  → "LINE notification message received" system message sent
  → Notification message delivered
  → Delivery webhook fired
```

### Flow 2: Not Agreed + No SMS Needed

```
API request → 200/202
  → "Set up to receive LINE notification messages" consent prompt
  → User clicks "Set" → consent screen
  → If agreed within 24h → message delivered → webhook fired
  → If not agreed in 24h → message deleted, no webhook
```

### Flow 3: Not Agreed + SMS Needed (Most Complex)

```
API request → 200/202
  → Consent prompt
  → User agrees → SMS auth dialog (can change phone number)
  → SMS with PIN sent → user enters PIN
  → After verification → message delivered → webhook fired
```

### Flow 4: Already Agreed + SMS Needed

```
API request → 200/202
  → "Phone number authentication" prompt
  → User clicks "Set" → phone auth screen → "Send SMS"
  → SMS with PIN sent → user enters PIN
  → After verification → message delivered → webhook fired
```

## Integration Recommendations

| Task | Approach |
|------|----------|
| Track deliveries | Use `X-Line-Delivery-Tag` to correlate sends with webhooks |
| Detect failures | If no webhook within 24 hours, treat as undelivered |
| Detect blocks | Cannot distinguish from other failures via API response alone |
| Signature verification | Always verify webhook signatures using channel secret |
| Redelivery handling | Check `deliveryContext.isRedelivery` to avoid duplicate processing |
