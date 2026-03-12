# Action Objects

Shared by Template messages, Rich Menu, Quick Reply, and Flex Message.

## Action Types Overview

| Type | Required Props | Where | Key Limits |
|------|---------------|-------|------------|
| `postback` | `data` | All | data: max 300 |
| `message` | `text` | All | text: max 300 |
| `uri` | `uri` | All | uri: max 1000, schemes: `http`/`https`/`line`/`tel` |
| `datetimepicker` | `data`, `mode` | All | data: max 300, mode: `date`/`time`/`datetime` |
| `camera` | `label` | Quick Reply only | label: max 20 |
| `cameraRoll` | `label` | Quick Reply only | label: max 20 |
| `location` | `label` | Quick Reply only | label: max 20 |
| `richmenuswitch` | `richMenuAliasId`, `data` | Rich Menu only | data: max 300 |
| `clipboard` | `clipboardText` | All (LINE 14.0.0+) | clipboardText: max 1000 |

## Label Specifications

The `label` property has different required/optional and max length rules depending on where the action is used:

| Context | Required | Max chars |
|---------|----------|-----------|
| Template (image carousel) | Optional | 12 |
| Template (other) | **Required** | 20 |
| Rich Menu | Optional (read by accessibility) | 20 |
| Quick Reply | **Required** | 20 |
| Flex (Button component) | **Required** | 40 |
| Flex (other components) | Optional (not displayed) | 40 |

## Postback Action

Tapping returns a postback event via webhook with the `data` value.

```json
{
  "type": "postback",
  "label": "Buy",
  "data": "action=buy&itemid=111",
  "displayText": "Buy",
  "inputOption": "openKeyboard",
  "fillInText": "---\nName: \nPhone: \n---"
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `data` | **Yes** | String returned in `postback.data` webhook property. Max 300 |
| `displayText` | No | Text shown in chat as user message. Max 300. Cannot use with `text` |
| `text` | No | **Deprecated.** Same as displayText but also returned via webhook. Don't use with quick reply. Max 300 |
| `inputOption` | No | UI behavior after tap: `closeRichMenu` / `openRichMenu` / `openKeyboard` / `openVoice`. LINE 12.6.0+ |
| `fillInText` | No | Pre-fill text when keyboard opens. Only when `inputOption` = `openKeyboard`. Supports `\n`. Max 300. LINE 12.6.0+ |

## Message Action

Sends the `text` value as a user message in the chat.

```json
{"type": "message", "label": "Yes", "text": "Yes"}
```

| Property | Required | Description |
|----------|----------|-------------|
| `text` | **Yes** | Text sent as message. Max 300 |

## URI Action

Opens the URI in LINE's in-app browser.

```json
{
  "type": "uri",
  "label": "Menu",
  "uri": "https://example.com/menu",
  "altUri": {"desktop": "https://example.com/pc/menu"}
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `uri` | **Yes** | URI to open. Max 1000. Schemes: `http`, `https`, `line`, `tel`. Must be UTF-8 percent-encoded |
| `altUri.desktop` | No | Alternative URI for LINE desktop (macOS/Windows). Overrides `uri` on desktop. Max 1000. **Works in Flex, NOT in Quick Reply** |

**URI schemes:**
- `https://` / `http://` — web pages
- `tel:09001234567` — phone dialer
- `https://line.me/R/` — LINE deep links (preferred over deprecated `line://`)

Full LINE URL scheme reference → **[url-schemes.md](url-schemes.md)**

## Datetime Picker Action

Opens a date/time picker dialog. Returns selected value in postback event.

```json
{
  "type": "datetimepicker",
  "label": "Select date",
  "data": "storeId=12345",
  "mode": "datetime",
  "initial": "2017-12-25t00:00",
  "max": "2018-01-24t23:59",
  "min": "2017-12-25t00:00"
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `data` | **Yes** | String returned in `postback.data`. Max 300 |
| `mode` | **Yes** | `date` / `time` / `datetime` |
| `initial` | No | Initial value |
| `max` | No | Max selectable value (must be > min) |
| `min` | No | Min selectable value (must be < max) |

**Date/time formats:**

| Mode | Format | Range | Example |
|------|--------|-------|---------|
| `date` | `YYYY-MM-DD` | 1900-01-01 ~ 2100-12-31 | `2017-06-18` |
| `time` | `HH:mm` | 00:00 ~ 23:59 | `06:15` |
| `datetime` | `YYYY-MM-DDThh:mm` | 1900-01-01T00:00 ~ 2100-12-31T23:59 | `2017-06-18T06:15` |

No timezone support.

## Camera / Camera Roll / Location Actions

**Quick Reply only.** Simple actions that open the respective LINE screen.

```json
{"type": "camera", "label": "Camera"}
{"type": "cameraRoll", "label": "Camera roll"}
{"type": "location", "label": "Location"}
```

`label` is required (max 20). Default icons are displayed if `imageUrl` is not set on the quick reply button.

## Rich Menu Switch Action

**Rich Menu only.** Switches the displayed rich menu and triggers a postback event.

```json
{
  "type": "richmenuswitch",
  "richMenuAliasId": "richmenu-alias-b",
  "data": "richmenu-changed-to-b"
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `richMenuAliasId` | **Yes** | Rich menu alias ID to switch to |
| `data` | **Yes** | String returned in `postback.data`. Max 300 |
| `label` | No | For accessibility. Max 20 |

Cannot be used in Flex Messages or Quick Reply. See [rich-menu.md](rich-menu.md) for tab switching setup.

## Clipboard Action

Copies text to the device clipboard. Available on LINE 14.0.0+ (iOS/Android).

```json
{"type": "clipboard", "label": "Copy", "clipboardText": "3B48740B"}
```

| Property | Required | Description |
|----------|----------|-------------|
| `clipboardText` | **Yes** | Text copied to clipboard. Max 1000 |
