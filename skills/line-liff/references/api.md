# LIFF v2 API Reference

## 1. Initialization & Environment

### `liff.init(config)`
Initialize the LIFF app. Must be called before any other LIFF API (except pre-init methods).

- **Parameters**:
  - `liffId` (string, required) — LIFF app ID
  - `withLoginOnExternalBrowser` (boolean, optional) — auto-trigger login in external browser
  - `successCallback` (function, optional)
  - `errorCallback` (function, optional)
- **Return**: `Promise<void>`
- **Errors**: INIT_FAILED, INVALID_ARGUMENT, INVALID_CONFIG

```javascript
liff.init({ liffId: '1234567890-AbcdEfgh', withLoginOnExternalBrowser: true })
  .then(() => { /* Start using API */ })
  .catch(err => console.error(err.code, err.message));
```

**Critical rules:**
- `liff.init()` only works on URLs at or below the registered Endpoint URL
- Do not modify `liff.*` query parameters before init resolves
- Do not log primary redirect URLs (they contain `access_token` values — credential leak risk)
- For endpoints with query strings, call `liff.init()` at both primary and secondary redirect URLs
- Since v2.11.0, credential info is stripped from URL when init resolves — send pageviews in `.then()`

### `liff.ready`
A `Promise` that resolves when `liff.init()` has completed. Available pre-initialization.

Note: if `liff.init()` fails, `liff.ready` will NOT be rejected.

### `liff.id`
LIFF app ID string. `null` until `liff.init()` is called.

### Pre-initialization Methods
These methods work **before** `liff.init()`:

| Method | Return | Notes |
|--------|--------|-------|
| `liff.ready` | `Promise` | Property, not method |
| `liff.getOS()` | `'ios'` \| `'android'` \| `'web'` | Based on OS in user agent, not browser type |
| `liff.getAppLanguage()` | Language code (RFC 5646) | SDK v2.24.0+, LINE 14.11.0+ |
| `liff.getLanguage()` | Language string | **Deprecated** — use `getAppLanguage()` |
| `liff.getVersion()` | SDK version string | |
| `liff.getLineVersion()` | LINE version string \| `null` | `null` in external browser |
| `liff.isInClient()` | `boolean` | `true` = LIFF browser; `false` = external or LINE's in-app browser |
| `liff.closeWindow()` | `void` | Pre-init since v2.4.0 |
| `liff.use()` | `liff` object | For pluggable SDK / plugins |
| `liff.i18n.setLang()` | `Promise` | |

---

## 2. Authentication & User Profile

### Login / Logout

| Method | Description | Availability |
|--------|-------------|-------------|
| `liff.login(loginConfig?)` | Trigger login (external browser only) | **Not available** in LIFF browser |
| `liff.logout()` | Log out the user | |
| `liff.isLoggedIn()` | Check login status → `boolean` | |

`loginConfig`: `{ redirectUri?: string }`

**Login behavior by environment:**
- **LIFF browser**: automatic login during `liff.init()` — `liff.login()` is unavailable
- **External browser**: manual `liff.login()` or set `withLoginOnExternalBrowser: true`
- **Authorization requests within LIFF browser are NOT guaranteed** — always use `liff.login()` for external browser, not LINE Login authorize URL directly

#### `redirectUri` Matching Rules

`redirectUri` must start with the Endpoint URL (query params and fragments don't affect matching):

```
Endpoint URL: https://example.com/path1/path2?query1=value1

✅ https://example.com/path1/path2?query2=value2
✅ https://example.com/path1/path2#fragment
✅ https://example.com/path1/path2/path3
❌ https://example.com/path1
❌ https://example.com/
```

### Token Access

| Method | Return | Required Scope |
|--------|--------|---------------|
| `liff.getAccessToken()` | Access token string | — |
| `liff.getIDToken()` | Raw JWT string | `openid` |
| `liff.getDecodedIDToken()` | Decoded ID token object | `openid` (+ `email` for email) |

- Access token is valid for **12 hours**
- When user closes LIFF app, access token may be revoked even if not expired (see session behavior in [guidelines.md](guidelines.md))

**Security — never send decoded data to server:**
- `liff.getDecodedIDToken()` result → client-side only
- `liff.getProfile()` result → client-side only
- To send user data to server, use `liff.getIDToken()` (raw JWT) and verify server-side → see [server-auth.md](server-auth.md)

### User Profile

| Method | Return | Required Scope | Notes |
|--------|--------|---------------|-------|
| `liff.getProfile()` | `Promise<{userId, displayName, pictureUrl?, statusMessage?}>` | `profile` | Main profile only (no subprofile) |
| `liff.getFriendship()` | `Promise<{friendFlag: boolean}>` | `profile` | Requires linked LINE Official Account on same channel |

`pictureUrl` and `statusMessage` are not returned if not set by user.

### Permissions

| Method | Description |
|--------|-------------|
| `liff.permission.query(scope)` | Check permission state → `Promise<{state: 'granted'\|'prompt'\|'unavailable'}>` |
| `liff.permission.getGrantedAll()` | Get all granted scopes → `Promise<string[]>` |
| `liff.permission.requestAll()` | Request all scopes (**LINE MINI Apps only**, requires Channel consent simplification enabled in Console) |

Available scopes: `profile`, `openid`, `email`, `chat_message.write`

**`getContext().scope` vs `permission.getGrantedAll()`**: `getContext().scope` returns scopes configured for the LIFF app; `permission.getGrantedAll()` returns scopes the user actually consented to.

---

## 3. Interaction & Messages

### `liff.sendMessages(messages)`
Send messages on behalf of user to current chat room.

- **Parameters**: Array of message objects (max **5**)
- **Return**: `Promise<void>`
- **Required scope**: `chat_message.write`

**All conditions must be met:**
- Within LIFF browser (launched from 1-on-1, group, or multi-person chat)
- `chat_message.write` scope enabled and user granted permission
- LIFF app NOT reloaded from "recently used services"

**Will fail (403 error) when:**
- Accessed via Keep Memo
- Accessed via URL scheme redirect from external site
- `chat_message.write` scope lost after LIFF-to-LIFF transition
- User didn't grant `chat_message.write` scope

**Supported message types with restrictions:**

| Type | Restriction |
|------|-----------|
| Text | `emojis` and `quoteToken` properties NOT available |
| Sticker | `quoteToken` NOT available |
| Image | — |
| Video | `trackingId` NOT available |
| Audio | — |
| Location | — |
| Template | **Only URI action allowed** (no postback, message, etc.) |
| Flex Message | **Only URI action allowed** (no postback, message, etc.) |

**Webhook behavior**: Template and Flex Messages sent via `liff.sendMessages()` do NOT trigger a webhook. Other message types do trigger webhooks, with `contentProvider.type = 'external'` for image/video/audio.

### `liff.shareTargetPicker(messages, options?)`
Open target picker for user to select friends/groups and send messages.

- **Parameters**:
  - `messages` — Array of message objects (max **5**, same type restrictions as `sendMessages`)
  - `options` — `{ isMultiple?: boolean }` — default is **`true`**
- **Return**: `Promise<{status: 'success'}>` or resolve with no value if cancelled
- **Prerequisite**: Developer must agree to "Agreement Regarding Use of Information" in Console
- **Check first**: `liff.isApiAvailable('shareTargetPicker')`
- **Restriction**: Only friends (incl. OAs) and groups selectable — no OpenChats

**`isMultiple: false` caveat**: Setting to `false` only limits the picker UI to one friend per invocation. Users can still call the picker multiple times — enforce uniqueness server-side if needed.

**External browser note**: In external browser, share target picker requires SSO login session. If user logged in via auto login (not SSO), an email login screen may appear instead of the picker.

**Warning**: Do not use `alert()` in the Promise callback — LIFF app won't work on some devices.

---

## 4. Navigation & Device

### `liff.openWindow(params)`
Open URL in browser.

- **Parameters**: `{ url: string, external?: boolean }` (default `external: false`)
- **Not guaranteed** to work in external browser

**Behavior differs by LINE version (Universal Links / App Links):**

| LINE Version | `external: false` (default) | `external: true` |
|---|---|---|
| Earlier than 14.20.0 | iOS: in-app browser; Android: transitions to app | iOS: transitions to app; Android: default browser |
| 14.20.0 – 15.19.x | Transitions to corresponding app | Transitions to corresponding app |
| **15.20.0 or later** | **Opens in LINE's in-app browser** | Transitions to corresponding app |

### `liff.closeWindow()`
Close the LIFF app window. Available pre-init (v2.4.0+). Not guaranteed in external browsers.

### `liff.scanCodeV2()`
Launch 2D code (QR) reader. Internally uses [jsQR](https://github.com/cozmo/jsQR) library.

- **Return**: `Promise<{value: string}>`
- **Requires**: "Scan QR" enabled in Console

**Compatibility:**

| OS | Version | LIFF Browser | External Browser |
|---|---|:---:|:---:|
| iOS | 11–14.2 | - | Yes (WebRTC) |
| iOS | 14.3+ | **Full size only** | Yes (WebRTC) |
| Android | All | **Full size only** | Yes (WebRTC) |
| PC | All | - | Yes (WebRTC) |

`liff.scanCode()` is **deprecated** — use `liff.scanCodeV2()`.

### `liff.createShortcutOnHomeScreen(params)`
Display screen for adding shortcut to home screen. **Verified LINE MINI Apps only.**

- **Parameters**: `{ url: string }` — LIFF URL, permanent link, or endpoint URL
- **Return**: `Promise<void>` (resolves when screen displays; cannot confirm if user actually added)
- **Requirements**: LINE MINI App, SDK v2.23.0+, LINE 13.20.0+
- **Check first**: `liff.isApiAvailable('createShortcutOnHomeScreen')`
- **iOS**: Safari works all versions; Chrome requires iOS 16.4+; other browsers not guaranteed

### `liff.isApiAvailable(apiName)`
Check if specific API is available in current environment.

- **Supported names**: `shareTargetPicker`, `createShortcutOnHomeScreen`, `multipleLiffTransition`, `iap`
- Returns `false` if: LINE version too old, external browser for browser-only API, terms not accepted, not logged in, access token expired

---

## 5. Context & Links

### `liff.getContext()`
Get current launch context.

**Return object properties:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | `'utou'` (1-on-1), `'group'`, `'room'`, `'external'`, `'none'` (e.g., Wallet tab) |
| `userId` | string | User ID. Included for all types except may be `null` when `external` |
| `liffId` | string | LIFF app ID |
| `viewType` | string | `'compact'` / `'tall'` / `'full'` — only when `type` ≠ `'external'` |
| `endpointUrl` | string | Service endpoint URL |
| `accessTokenHash` | string | First half of SHA256 hash of access token |
| `availability` | object | Feature availability per API |
| `scope` | string[] | Scopes configured for the LIFF app |
| `menuColorSetting` | object | LIFF browser header color settings |
| `miniAppId` | string | Custom Path string (LINE MINI App only) |
| `miniDomainAllowed` | boolean | Whether `miniapp.line.me` domain is available |
| `permanentLinkPattern` | string | Always `'concat'` |

**Discontinued properties (Feb 2023):** `utouId`, `groupId`, `roomId` — company internal chat identifiers are no longer provided to LIFF apps.

**LIFF apps are NOT compatible with OpenChat** — retrieving user profiles through LIFF isn't possible in OpenChat.

### Permanent Links

| Method | Description | Status |
|--------|-------------|--------|
| `liff.permanentLink.createUrlBy(url)` | Create permanent link from arbitrary URL → `Promise<string>` | **Recommended** |
| `liff.permanentLink.createUrl()` | Create permanent link for current page → string | May be deprecated in next major version |
| `liff.permanentLink.setExtraQueryParam(str)` | Add query parameters to current page link | May be deprecated — use `createUrlBy()` instead |

Format: `https://liff.line.me/{liffId}/{path}?{query}#{fragment}`

Throws `LiffError` if URL doesn't start with Endpoint URL.

`setExtraQueryParam()` overwrites previously set params each call. Params are discarded on page navigation.

---

## 6. Internationalization

### `liff.i18n.setLang(language)`
Set the language of text displayed by the LIFF SDK.

- **Parameters**: `language` (string, required) — RFC 5646 / BCP 47 language tag
- **Return**: `Promise<void>`
- Falls back to `'en'` if no translation available
- Available pre-initialization
- Pluggable SDK module: `@line/liff/i18n`

```javascript
liff.i18n.setLang('ja');
```

---

## 7. Pluggable SDK (npm only)

Reduce bundle size ~34% by importing only needed modules. Requires LIFF SDK v2.22.0+ via npm.

```javascript
import liff from '@line/liff/core';
import GetOS from '@line/liff/get-os';
import GetProfile from '@line/liff/get-profile';

liff.use(new GetOS());       // Must call liff.use() BEFORE liff.init()
liff.use(new GetProfile());

liff.init({ liffId: '...' }).then(() => {
  console.log(liff.getOS());
});
```

Core import (`@line/liff/core`) includes only: `liff.id`, `liff.ready`, `liff.init()`, `liff.getVersion()`, `liff.use()`.

### Module Map

| LIFF API | npm Module |
|----------|-----------|
| `liff.getOS()` | `@line/liff/get-os` |
| `liff.getAppLanguage()` | `@line/liff/get-app-language` |
| `liff.getLineVersion()` | `@line/liff/get-line-version` |
| `liff.getContext()` | `@line/liff/get-context` |
| `liff.isInClient()` | `@line/liff/is-in-client` |
| `liff.isLoggedIn()` | `@line/liff/is-logged-in` |
| `liff.isApiAvailable()` | `@line/liff/is-api-available` |
| `liff.login()` | `@line/liff/login` |
| `liff.logout()` | `@line/liff/logout` |
| `liff.getAccessToken()` | `@line/liff/get-access-token` |
| `liff.getIDToken()` | `@line/liff/get-id-token` |
| `liff.getDecodedIDToken()` | `@line/liff/get-decoded-id-token` |
| `liff.permission.*` | `@line/liff/permission` |
| `liff.getProfile()` | `@line/liff/get-profile` |
| `liff.getFriendship()` | `@line/liff/get-friendship` |
| `liff.openWindow()` | `@line/liff/open-window` |
| `liff.closeWindow()` | `@line/liff/close-window` |
| `liff.sendMessages()` | `@line/liff/send-messages` |
| `liff.shareTargetPicker()` | `@line/liff/share-target-picker` |
| `liff.scanCodeV2()` | `@line/liff/scan-code-v2` |
| `liff.permanentLink.*` | `@line/liff/permanent-link` |
| `liff.i18n.setLang()` | `@line/liff/i18n` |
| `liff.createShortcutOnHomeScreen()` | `@line/liff/create-shortcut-on-home-screen` |

---

## 8. Error Handling

### LiffError Object

```json
{
  "code": "INIT_FAILED",
  "message": "Failed to init LIFF SDK",
  "cause": ...
}
```

- `code` (string) — always present
- `message` (string) — not always included; **subject to change without notice**
- `cause` (unknown) — not always included

**Identify errors by both `code` AND `message`** — don't rely on exact message string matching alone, as messages may change.

### SDK Error Codes

| Code | Description |
|------|-------------|
| INIT_FAILED | `liff.init()` failed |
| INVALID_ARGUMENT | Invalid parameter passed |
| UNAUTHORIZED | User not logged in, no access token, or shareTargetPicker called before login |
| FORBIDDEN | Permission denied, or unsupported environment |
| INVALID_CONFIG | Invalid LIFF config (missing liffId, or `createUrl()` URL doesn't match endpoint) |
| INVALID_ID_TOKEN | ID token verification failed |
| EXCEPTION_IN_SUBWINDOW | Sub-window error (e.g., target picker idle >10 minutes) |
| UNKNOWN | Unclassified error |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request — check parameters and JSON format |
| 401 | Unauthorized — check authorization header |
| 403 | Forbidden — check account/plan authorization |
| 429 | Rate limited |
| 500 | Temporary API server error |

---

## API Availability Matrix

| API | LIFF Browser | External Browser | Notes |
|-----|:---:|:---:|-------|
| `liff.login()` | - | Yes | Auto-login in LIFF browser |
| `liff.sendMessages()` | Yes | - | Requires `chat_message.write` |
| `liff.shareTargetPicker()` | Yes | Yes | Check `isApiAvailable` first |
| `liff.scanCodeV2()` | Full only | Partial (WebRTC) | |
| `liff.closeWindow()` | Yes | Unreliable | |
| `liff.openWindow()` | Yes | Not guaranteed | |
| `liff.getLineVersion()` | Yes | Returns `null` | |
| `liff.createShortcutOnHomeScreen()` | Yes | - | Verified MINI Apps only |
