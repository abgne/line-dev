# Template System

LINE notification messages (template) allow creating messages by combining premade templates, items, and buttons. Added June 2025 as a simpler alternative to the flexible type.

## Message Structure

A template notification message consists of four layers:

```
Template (selected by templateKey)
├── Title + Description (auto-displayed at top, cannot be changed)
├── Emphasized Item (optional, max 1)
│   └── itemKey + content (max 15 chars)
├── Items (optional, max 15)
│   └── itemKey + content (max 300 chars each)
└── Buttons (optional, max 2)
    └── buttonKey + url (max 1000 chars each)
```

Header and footer of the message are fixed and cannot be customized.

## Templates

Select a template by specifying its `templateKey` in the API request. The template provides:
- **Title**: Displayed prominently at the top
- **Description**: Shown below the title

Available templates vary by country (Japan, Thailand, Taiwan) and are automatically determined by the LINE Official Account's registered country.

Template keys use country suffixes: e.g., `shipment_completed_ja`

For available templates, see [Templates](https://developers.line.biz/en/docs/partner-docs/line-notification-messages/template/#templates) in the official documentation.

## Items

Items display label-value pairs in the message body.

| Property | Type | Required | Max Length |
|----------|------|----------|------------|
| `itemKey` | String | Yes | — |
| `content` | String | Yes | **15 chars** (emphasizedItem) / **300 chars** (items) |

```json
{"itemKey": "time_range_001_ja", "content": "A.M."}
```

**Rules:**
- `body.emphasizedItem`: Max 1 object. Content max 15 characters.
- `body.items`: Min 0, max 15 objects. Content max 300 characters each.
- Cannot specify duplicate `itemKey` values within a single message
- Cannot have the same `itemKey` in both `emphasizedItem` and `items`

For available items per country, see [Items](https://developers.line.biz/en/docs/partner-docs/line-notification-messages/template/#items) in the official documentation.

## Buttons

Buttons provide tappable actions that open URLs.

| Property | Type | Required | Max Length |
|----------|------|----------|------------|
| `buttonKey` | String | Yes | — |
| `url` | String | Yes | **1000 chars** |

```json
{"buttonKey": "contact_ja", "url": "https://example.com/ContactUs/"}
```

- `body.buttons`: Min 0, max 2 objects.

For available buttons per country, see [Buttons](https://developers.line.biz/en/docs/partner-docs/line-notification-messages/template/#buttons) in the official documentation.

## Field Limits Quick Reference

| Field | Max |
|-------|-----|
| `emphasizedItem` | 1 object |
| `emphasizedItem.content` | 15 characters |
| `items` | 15 objects |
| `items[].content` | 300 characters |
| `buttons` | 2 objects |
| `buttons[].url` | 1000 characters |

## Country-Specific Keys

Templates, items, and buttons differ by country. The country is automatically determined by the LINE Official Account that sends the message.

| Country | Key Suffix | Example |
|---------|-----------|---------|
| Japan | `_ja` | `shipment_completed_ja`, `date_002_ja`, `contact_ja` |
| Thailand | (varies) | See official documentation |
| Taiwan | (varies) | See official documentation |

You cannot change the country setting — it is tied to the LINE Official Account.

## Complete Example

```json
{
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
}
```
