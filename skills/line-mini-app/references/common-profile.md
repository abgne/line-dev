# Common Profile Quick Fill

> **Verified MINI Apps only.** Must apply to use Quick-fill. See [Steps for using Quick-fill](#application-process).

> **Generally available since August 2025.** Quick Fill was previously limited to enterprise partners. As of August 2025, all certified (verified) MINI Apps can apply to use Quick Fill.

> **LIFF browser only.** `liff.$commonProfile` APIs are not available in external browsers (iOS / Android only).

> **Quick-fill UI is currently Japanese only.** The Quick-fill modal screen displays in Japanese regardless of the user's LINE app language setting. The data itself reflects what the user registered in their Account Center.

## Overview

Quick-fill automatically fills form fields with the user's Common Profile data from LINE's Account Center. The user confirms their profile in a modal before data is filled.

Common Profile data is created by combining the profile registered with **LINE and Yahoo! JAPAN**. If the user doesn't use the Account Center, LINE profile information is filled in automatically.

## Application Process

### Step 1: Prepare a verified MINI App

Quick-fill is only available in verified MINI Apps. See [Development to Release](guidelines.md#development-to-release).

### Step 2: Apply and develop

1. **Apply for Quick-fill** — submit usage application form, receive approval via email
   - [Single application form (Excel, Japanese)](https://workers-hub.ent.box.com/s/06w8vzqxfwx2e031oq2q9ztj7ca8p7h8)
   - [Multiple applications form (Excel, Japanese)](https://workers-hub.ent.box.com/s/xrwjm892d1uxsiblptfgoj07r0v5zwbp)
   - [Submit via application form (Japanese)](https://form-business.yahoo.co.jp/claris/enqueteForm?inquiry_type=miniapp-quick-fill)
2. **Configure Console scopes** — in LINE Developers Console → target channel → Web app settings → Scope
3. **Integrate Quick-fill** — install LIFF plugin, implement API calls
4. **Submit for review** — via Review request tab in LINE MINI App channel

## Environment Requirements

| Requirement | Version |
|-------------|---------|
| LIFF SDK | **≥ v2.19.0** (LIFF plugin support required) |
| Node.js | **≥ 18.15.0** (npm install only; not needed for CDN) |
| Platform | LINE for iOS / LINE for Android only |

LIFF apps only work at or below the registered Endpoint URL (e.g. `https://example.com/path/to/lower`).

## Plugin Installation

### npm (recommended)

```bash
npm install @line/liff-common-profile-plugin
```

```javascript
import liff from "@line/liff";
import { LiffCommonProfilePlugin } from "@line/liff-common-profile-plugin";

liff.use(new LiffCommonProfilePlugin());
await liff.init({ liffId: "YOUR_LIFF_ID" });

// Now liff.$commonProfile is available
```

### CDN

```html
<script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
<script src="https://static.line-scdn.net/5/liff-common-profile/edge/production/1.0.0/index.umd.cjs"></script>
```

```javascript
liff.use(new liffCommonProfile.LiffCommonProfilePlugin());
await liff.init({ liffId: "YOUR_LIFF_ID" });
```

**Note:** CDN exposes `liffCommonProfile` on the `window` object. Use `liffCommonProfile.LiffCommonProfilePlugin`, not a direct import.

If the plugin is not installed, calling `liff.$commonProfile` methods throws:
```
LiffCommonProfilePlugin isn't installed properly. Did you call liff.use(new LiffCommonProfilePlugin()) before using it?
```

## Console Scopes vs API Scopes

The LINE Developers Console configures **6 broad permission groups**. The API uses **15 fine-grained scopes**. Users consent to the broad groups; the API returns individual fields.

| Console Scope | API Scopes |
|---------------|------------|
| `commonprofile.name` | `family-name`, `given-name`, `family-name-kana`, `given-name-kana` |
| `commonprofile.email` | `email` |
| `commonprofile.address` | `postal-code`, `address-level1`, `address-level2`, `address-level3`, `address-level4` |
| `commonprofile.gender` | `sex-enum` |
| `commonprofile.birthday` | `bday-year`, `bday-month`, `bday-day` |
| `commonprofile.phone` | `tel` |

Users cannot selectively allow individual scopes on the consent screen — they allow or disallow all as "Management Information (Common Profile) in the Account Center" in bulk.

**Known issue:** If both Quick-fill and [Channel consent simplification](https://developers.line.biz/en/docs/line-mini-app/develop/channel-consent-simplification/) are enabled, users cannot disable the Common Profile toggle on the consent screen. A fix is planned.

## Available Scopes

| # | Scope | Description | Type | Max (half-width) | Max (full-width) | formatOptions |
|---|-------|-------------|------|-------------------|-------------------|---------------|
| 1 | `family-name` | Family name | string | 100 | 50 | `excludeEmojis` |
| 2 | `given-name` | Given name | string | 100 | 50 | `excludeEmojis` |
| 3 | `family-name-kana` | Phonetic family name | string | 100 | 50 | — |
| 4 | `given-name-kana` | Phonetic given name | string | 100 | 50 | — |
| 5 | `sex-enum` | Gender | number | 1 (fixed) | — | — |
| 6 | `bday-day` | Day of birth | number | 2 | — | — |
| 7 | `bday-month` | Month of birth | number | 2 | — | — |
| 8 | `bday-year` | Year of birth | number | 4 | — | — |
| 9 | `tel` | Phone number | string | 200 | — | `excludeNonJp` |
| 10 | `email` | Email address | string | 200 | — | — |
| 11 | `postal-code` | Postal code | string | 47 | — | `digitsOnly` |
| 12 | `address-level1` | Prefecture / State | string | 53 | 53 | — |
| 13 | `address-level2` | City | string | 53 | 53 | — |
| 14 | `address-level3` | Town / Street | string | 100 | 69 | — |
| 15 | `address-level4` | Additional address | string | 100 | 69 | — |

`sex-enum` values: `0` = Male, `1` = Female, `2` = Other, `3` = No answer

## liff.$commonProfile.get()

Gets the user's Common Profile. Displays a confirmation modal — user must tap **Auto-fill** to approve.

```javascript
liff.$commonProfile.get(scopes, options);
```

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scopes` | String[] | Yes | Profile scopes to retrieve |
| `options.formatOptions` | Object | No | Format options per scope (use camelCase key, e.g. `given-name` → `givenName`) |

### formatOptions

All default to `true`. Specify `false` to disable.

| Option | Type | Default | Applicable Scopes | Description |
|--------|------|---------|-------------------|-------------|
| `excludeEmojis` | Boolean | `true` | `givenName`, `familyName` | Remove emojis from string |
| `excludeNonJp` | Boolean | `true` | `tel` | Exclude phone numbers with 12+ digits. If `true`, returns empty string + error for non-JP numbers |
| `digitsOnly` | Boolean | `true` | `postalCode` | Exclude postal codes containing non-numeric characters. If `true`, returns empty string + error for non-numeric codes |

### Return Value

`Promise<{ data: Partial<CommonProfile>, error: Partial<CommonProfileError> }>`

**`data` property values:**
- **Value present** — user authorized and data exists
- **`undefined`** — scope not requested, or user did not authorize that item
- **`null`** — user hasn't set a value, or an error occurred retrieving it

```javascript
// data example
{
  "family-name": "Yamada",
  "given-name": "Taro",
  "email": "sample@example.com",
  "tel": "09001234567",
  "postal-code": "1020094"
}

// error example
{
  "tel": ["Phone number has 12 or more digits"],
  "postal-code": ["Postal code contains non-numeric characters"]
}
```

### Error Responses

Promise rejected with `LiffError`:
- Plugin not installed → `LiffCommonProfilePlugin isn't installed properly...`
- Not in LIFF browser → `liff.$commonProfile API is available only in LIFF browser.`

## liff.$commonProfile.getDummy()

Gets dummy profile data for testing. Displays a confirmation modal with dummy data.

```javascript
liff.$commonProfile.getDummy(scopes, options, caseId);
```

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scopes` | String[] | Yes | Profile scopes to retrieve |
| `options.formatOptions` | Object | No | Same as `get()` |
| `caseId` | Number | Yes | Dummy dataset ID (`1` to `10`) |

### Return Value

Same as `get()`: `Promise<{ data: Partial<CommonProfile>, error: Partial<CommonProfileError> }>`

**`data` values:**
- **`undefined`** — scope not requested
- **`null`** — dummy dataset has no value for that item

### Dummy Data Characteristics

Each `caseId` tests different edge cases:

| caseId | Characteristics |
|--------|----------------|
| 1 | Complete standard data (all fields populated) |
| 2 | Missing name fields, non-JP postal code (`N5X 1N7`), missing address-level2 |
| 3 | Missing given-name, very long email (200+ chars), hyphenated postal code (`102-0094`) |
| 4 | Missing family-name, very long postal code with mixed formats, missing address-level4 |
| 5 | Romanized names (`Daimta`, `Damio`), English addresses, missing email |
| 6 | Numeric names (`1234`, `4321`), hyphenated phone (`090-1234-5678`), half-width katakana addresses, missing postal code/bday-day |
| 7 | Half-width katakana names, very long phone (200+ chars), missing address fields |
| 8 | Names with symbols (`！？`, `@`), emoji addresses (`🍀`), missing bday-month |
| 9 | Emoji names (`🐶🐶🐶`, `ダミ💚`), very long addresses (max-length test), missing phone |
| 10 | Max-length names (50 full-width chars each), non-JP postal code, missing address-level1 |

```json
// caseId 1 — complete standard data
{
  "family-name": "見本田",
  "given-name": "見本夫",
  "family-name-kana": "ダミータ",
  "given-name-kana": "ダミーオ",
  "sex-enum": 0,
  "bday-day": 12,
  "bday-month": 3,
  "bday-year": 1998,
  "tel": "09001234567",
  "email": "dummy_39@yahoo.co.jp",
  "postal-code": "1020094",
  "address-level1": "東京都",
  "address-level2": "千代田区",
  "address-level3": "紀尾井町1-2",
  "address-level4": "東京ガーデンテラス紀尾井町"
}
```

### Error Responses

Same as `get()`.

## liff.$commonProfile.fill()

Automatically fills form fields using `data-liff-autocomplete` HTML attributes.

```javascript
liff.$commonProfile.fill(profile);
```

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile` | Partial\<CommonProfile\> | Yes | Profile data to fill (typically `data` from `get()` or `getDummy()`) |

### Return Value

None.

### HTML Attribute Mapping

The `data-liff-autocomplete` attribute value must match the scope name:

```html
<input type="text" data-liff-autocomplete="family-name" />
<input type="text" data-liff-autocomplete="given-name" />
<input type="text" data-liff-autocomplete="family-name-kana" />
<input type="text" data-liff-autocomplete="given-name-kana" />
<input type="email" data-liff-autocomplete="email" />
<input type="tel" data-liff-autocomplete="tel" />
<input type="text" data-liff-autocomplete="postal-code" />
<select data-liff-autocomplete="address-level1">...</select>
<input type="text" data-liff-autocomplete="address-level2" />
<input type="text" data-liff-autocomplete="address-level3" />
<input type="number" data-liff-autocomplete="bday-year" />
<input type="number" data-liff-autocomplete="bday-month" />
<input type="number" data-liff-autocomplete="bday-day" />
<select data-liff-autocomplete="sex-enum">
  <option value="0">Male</option>
  <option value="1">Female</option>
  <option value="2">Other</option>
  <option value="3">No answer</option>
</select>
```

### Custom Formatting Before Fill

If you need to transform data before filling (e.g. pad date values), use `fill()` with modified data instead of the raw `get()` result:

```javascript
const { data } = await liff.$commonProfile.get([
  "bday-year", "bday-month", "bday-day",
]);

liff.$commonProfile.fill({
  "bday-year": data["bday-year"],
  "bday-month": data["bday-month"]?.toString().padStart(2, '0'),
  "bday-day": data["bday-day"]?.toString().padStart(2, '0'),
});
```

For fully custom mapping (e.g. combining fields into `YYYYMMDD`), use `document.getElementById().value` or `document.querySelector().value` directly instead of `fill()`.

## Implementation Pattern

```javascript
// 1. Install plugin before init
import liff from "@line/liff";
import { LiffCommonProfilePlugin } from "@line/liff-common-profile-plugin";

liff.use(new LiffCommonProfilePlugin());
await liff.init({ liffId: "YOUR_LIFF_ID" });

// 2. Get profile (shows consent modal)
const { data, error } = await liff.$commonProfile.get(
  ["family-name", "given-name", "email", "tel", "postal-code"],
  {
    formatOptions: {
      tel: { excludeNonJp: false },
      postalCode: { digitsOnly: false },
    },
  }
);

// 3. Handle errors per field
if (error) {
  for (const [field, messages] of Object.entries(error)) {
    console.warn(`${field}: ${messages.join(', ')}`);
  }
}

// 4. Auto-fill form
liff.$commonProfile.fill(data);
```
