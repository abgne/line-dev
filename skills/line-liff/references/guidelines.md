# LIFF Development Guidelines

## 1. Registration & Configuration

### Channel Type
LIFF apps can only be added to:
- **LINE Login** channel — standard LIFF apps
- **LINE MINI App** channel — LIFF apps as LINE MINI Apps

Cannot add LIFF apps to Messaging API or Blockchain Service channels.

> **Future**: LIFF will merge into LINE MINI App as a single brand. New apps are recommended to use LINE MINI App channel.

### Provider & Channel Warnings
- Once created, a **channel cannot be moved** to a different provider
- **User IDs differ per provider** — the same LINE user gets different user IDs across providers
- If your service links LINE Login + Messaging API, create **both channels under the same provider**
- Set **App types** to "Web app" when creating a LINE Login channel for LIFF

### Adding LIFF Apps
Register LIFF apps in [LINE Developers Console](https://developers.line.biz/console/) under a **LINE Login channel**.

- **Limit**: max **30** LIFF apps per channel
- **Name**: cannot include "LINE" or inappropriate strings
- **Endpoint URL**: must be HTTPS, no URL fragments (`#`) allowed

### Required Settings

| Setting | Options | Notes |
|---------|---------|-------|
| View size | Full / Tall / Compact | Full covers entire screen, Tall ~75%, Compact ~50% |
| Scopes | `openid`, `email`, `profile`, `chat_message.write` | Select only what's needed |
| Scan QR | On / Off | Required for `liff.scanCodeV2()` |
| Module mode | On / Off | Full size only; hides action button in header |
| Add friend | On (normal) / On (aggressive) / Off | Prompts user to add linked OA |

### Output
After registration: LIFF ID (e.g., `1234567890-AbcdEfgh`) and LIFF URL (`https://liff.line.me/{liffId}`).

---

## 2. SDK Integration

### CDN

Two path types:

| Type | URL | Behavior |
|------|-----|----------|
| **Edge** | `https://static.line-scdn.net/liff/edge/2/sdk.js` | Auto-updates to latest (major version only) |
| **Fixed** | `https://static.line-scdn.net/liff/edge/versions/2.22.3/sdk.js` | Pinned to exact patch — manual updates |

```html
<script charset="utf-8" src="https://static.line-scdn.net/liff/edge/versions/2.22.3/sdk.js"></script>
```
- Include `charset="utf-8"` if your HTML uses a different encoding

### npm
```bash
npm install @line/liff
```
```javascript
import liff from '@line/liff';
```
- TypeScript definitions included — no separate `@types` package needed
- Webpack v5: SDK v2.16.0 and earlier lack Node.js polyfills — upgrade to v2.16.1+
- Do **not** modify `window.liff` — the SDK manages this object internally
- For tree-shaking, use pluggable SDK (`@line/liff/core`) — see [api.md § Pluggable SDK](api.md)

---

## 3. Endpoint URL Rules

The Endpoint URL is the root of the LIFF app. `liff.init()` only works on URLs at or below this path.

```
Endpoint: https://example.com/app/
  ✅ https://example.com/app/page1
  ✅ https://example.com/app/sub/page2
  ❌ https://example.com/other/
```

- SDK v2.27.2+ displays console warnings for mismatched URLs
- Transitions above the endpoint URL hierarchy are not guaranteed

---

## 4. Authentication Flow

### LIFF Browser vs External Browser

| Behavior | LIFF Browser | External Browser |
|----------|:---:|:---:|
| Login | Automatic during `liff.init()` | Manual: `liff.login()` or `withLoginOnExternalBrowser: true` |
| `liff.login()` available | No | Yes |
| `liff.sendMessages()` | Yes | No |
| `liff.closeWindow()` | Yes | Unreliable |

### Token Security
- **Access token**: valid 12 hours; treat as sensitive
- **ID token**: send raw JWT (`liff.getIDToken()`) to server; never send `liff.getDecodedIDToken()` result
- **Channel Secret**: server-side only; never expose in client code
- For server-side JWT verification → see [server-auth.md](server-auth.md)

---

## 5. Share Target Picker

### Prerequisites
1. Developer must agree to **"Agreement Regarding Use of Information"** in LINE Developers Console (per channel)
2. Check availability: `liff.isApiAvailable('shareTargetPicker')`

### Behavior
- Selectable targets: friends (including OAs) and groups — **no OpenChats**
- `{ isMultiple: true }` allows selecting multiple targets
- Returns `{ status: 'success' }` on send, or resolves with no value if cancelled

---

## 6. Session Behavior

### LINE v15.12.0+ (Recently Used Services)

The action button shows a **multi-tab view** with an options menu (Refresh, Share, Minimize, Permission settings) and a list of recently used LIFF apps (up to **50** items, ordered by recency).

**Display conditions**: LINE 15.12.0+, **Full** view size, module mode **off**.

#### Resume vs Reload

When a user reopens a LIFF app from recently used services:

| Condition | Resume | Reload |
|-----------|:---:|:---:|
| Rule | Within **12 hours** AND in last **10** items | Otherwise |
| Access token | Preserved | Discarded |
| Browsing history | Preserved | Discarded |
| Scroll position | Preserved | Discarded |
| Start page | Restores previous state | Initializes at previous URL |

**Important**: `liff.sendMessages()` does **not** work after a reload from recently used services.

### Earlier LINE Versions (< 15.12.0)

Action button shows an **options menu** (not multi-tab view). Access tokens expire immediately upon LIFF app closure.

---

## 7. UI/UX

### View Sizes

| Type | Coverage | Use Case |
|------|----------|----------|
| Full | 100% screen | Standalone app experience |
| Tall | ~75% | Forms, product details |
| Compact | ~50% | Quick actions, confirmations |

Design responsively for all view types.

### OGP Tags
Set for chat sharing previews:
```html
<meta property="og:title" content="App Title">
<meta property="og:description" content="Description">
<meta property="og:image" content="https://example.com/image.png">
```

### Title
Set `<title>` tag — displayed in LIFF browser header.

---

## 8. Development Rules

### Initialization Rule
`liff.init()` must be called on **every page load**, even within the same LIFF app. If the endpoint URL has query strings, call `liff.init()` at both primary and secondary redirect URLs.

### SPA Routing
Use the [History API](https://html.spec.whatwg.org/multipage/nav-history-apis.html#the-history-interface) (`pushState`, `replaceState`) for SPA routing. LIFF has **limited compatibility with fragment-based routing** (`#/path`) because the SDK uses URL fragments during initialization.

### Device API Permissions
APIs that access device/OS functions must be triggered by **user action** (not on page load):
- Geolocation (getting location)
- Camera access
- Microphone access

### User Privacy & Tracking
- Do not track users with cookies, localStorage, or sessionStorage without **user consent**
- Do not link LINE user data with external session information without consent
- Cookies, localStorage, and sessionStorage are available in LIFF apps, but future OS changes may restrict their use

### Data Leakage Prevention
- LIFF endpoint URLs and URL fragments of LIFF URLs contain sensitive information (access tokens, user IDs) — guard against data leakage
- Do not log primary redirect URLs (they contain `access_token` values)

### HTTPS Requirement
All LIFF app URLs and opened content must use `https`. If `http` is used, the content opens in LINE's in-app browser and does **not** function as a LIFF app.

### Testing
During test phase, limit access privileges for the LIFF app through your web app (e.g., IP restriction, auth gate).

### Load Testing
Do not access via LIFF scheme (`https://liff.line.me/{liffId}`) or send mass LIFF API requests for load testing. Prepare a test environment that does not generate requests to the LINE Platform. Exceeding rate limits returns `429 Too Many Requests`.

### Deauthorization on User Unregistration
When a user unregisters from your app or terminates the link with LINE:

1. Call the [Deauthorize endpoint](https://developers.line.biz/en/reference/line-login/#deauthorize) to revoke permissions on behalf of the user
2. Document this behavior in your terms or near the unlink function:
   - e.g., "If you unsubscribe, the link between this service and LINE app will be terminated."

This ensures the app does not remain in the user's **Settings > Account > Authorized apps** after unregistration.

### LINE Login Guidelines
LIFF uses LINE Login's system. All [LINE Login development guidelines](https://developers.line.biz/en/docs/line-login/development-guidelines/) also apply to LIFF apps.

---

## 9. URL Handling

- Execute URL changes (`window.location.replace`, `history.pushState`) **after** `liff.init()` resolves
- The SDK uses query parameters and fragments during initialization — do not alter `liff.*` params before init
- External site transitions trigger a popup notification to the user (LIFF browser only)
- For LIFF URL format, liff.state, and permanent links → see [navigation.md](navigation.md)

---

## 10. Browser Environments

LIFF apps can run in three browser environments. Understanding their differences is critical for correct behavior.

### Three Browser Types

| Browser | Opens when | `isInClient()` | `getContext().type` |
|---------|-----------|:---:|:---:|
| **LIFF browser** | User taps LIFF URL in LINE chat | `true` | `utou`, `group`, `room`, `none` |
| **LINE's in-app browser** | User taps endpoint URL (not LIFF URL) in LINE chat | `false` | `external` |
| **External browser** | User opens LIFF URL in Chrome, Safari, etc. | `false` | `external` |

**Key insight**: LINE's in-app browser is treated as an **external browser** by the LIFF SDK. `liff.isInClient()` returns `false` and `liff.getContext().type` returns `"external"`.

**No guaranteed environment**: Which browser opens depends on iOS Universal Links, Android App Links, and OS-level behavior. Always design apps to work in **both** LIFF browser and external browser.

### Feature Availability by Browser

| Feature | LIFF Browser | LINE In-App Browser | External Browser |
|---------|:---:|:---:|:---:|
| View size (compact/tall/full) | Yes | - | - |
| Action button in header | Yes | - | - |
| Multi-tab view | Yes | - | - |
| `liff.login()` | - (auto at init) | Yes | Yes |
| `liff.sendMessages()` | Yes | - | - |
| `liff.shareTargetPicker()` | Yes | - | Yes (SSO note) |
| `liff.scanCodeV2()` | Full size only | - | Yes (WebRTC) |
| `liff.closeWindow()` | Yes | Unreliable | Unreliable |
| `liff.openWindow()` | Yes | Not guaranteed | Not guaranteed |
| `liff.getLineVersion()` | Version string | `null` | `null` |
| LIFF-to-LIFF transition | Yes | - | - |
| External site popup warning | Yes | - | - |
| Browser minimization | Yes | - | - |

### UI Identification

| UI Element | LIFF Browser | LINE In-App Browser |
|-----------|:---:|:---:|
| Minimizing button | - | Yes |
| Action button | Yes (hidden in module mode) | - |
| Footer bar | - | Yes |

### WebView Engine & Limitations

LIFF browser runs on **WKWebView** (iOS) and **Android WebView**. The following web technologies are **not supported**:

| Unsupported Technology | Impact |
|----------------------|--------|
| Service Workers | No offline support, no background sync, no push notifications, **no PWA** |
| Add to Home Screen (A2HS) | Cannot prompt install (LINE MINI Apps use `liff.createShortcutOnHomeScreen()` instead) |
| `<a download>` attribute | Cannot trigger file downloads via anchor tags |
| `<meta name="theme-color">` | Cannot customize browser chrome color |

These limitations may be lifted in future updates.

### Cache Behavior

- LIFF browser caches content according to HTTP headers (`Cache-Control`)
- **There is no way to manually clear cache** stored in LIFF browser
- Control caching via proper HTTP headers on your server

### API Availability Check

Always check before using environment-dependent APIs:
```javascript
if (liff.isApiAvailable('shareTargetPicker')) {
  // show share button
}
```

---

## 11. SDK Versioning & Lifecycle

### Versioning Policy

Since v2.2.0, LIFF follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

| Version | Meaning |
|---------|---------|
| MAJOR | Backwards-incompatible changes (e.g., v1 → v2) |
| MINOR | New backwards-compatible features (e.g., v2.26 → v2.27) |
| PATCH | Backwards-compatible bug fixes (e.g., v2.27.2 → v2.27.3) |

### CDN Update Behavior

| CDN Path | Update behavior |
|----------|----------------|
| **Edge** (`/edge/2/sdk.js`) | Auto-updates to latest MINOR + PATCH within same MAJOR |
| **Fixed** (`/edge/versions/2.x.x/sdk.js`) | Never auto-updates; developer controls timing |
| **Compat** (`/edge/2.1/sdk.js`) | Same as edge; **may be discontinued** without following lifecycle schedule |

### SDK Lifecycle

Each MAJOR version progresses through these phases:

| Status | Description | Duration |
|--------|-------------|----------|
| **Active** | Current version; new features and improvements | Until next MAJOR release |
| **Maintaining** | Bug fixes and security patches only | 12 months after Active ends |
| **Deprecated** | No updates; still usable | 6 months after Maintaining ends |
| **End-of-life** | CDN paths disabled; apps stop working | — |

**Current status:**

| Version | Status | Notes |
|---------|--------|-------|
| LIFF v1 | End-of-life (Oct 1, 2021) | All CDN paths disabled |
| LIFF v2 | Active (since Oct 16, 2019) | Current version |
| LIFF v3 | TBD | — |

**Warning**: An end-of-life SDK means LIFF apps using it **cannot be opened at all**. Monitor lifecycle schedule and migrate before deprecation ends.

### Key Breaking Changes by Version

| Version | Change | Impact |
|---------|--------|--------|
| v2.8.0 | `liff.init()` now resolves **after** secondary redirect (was double-resolving before) | Code in `.then()` no longer runs twice; analytics/init logic may need review |
| v2.11.0 | Credential info (access_token, id_token) stripped from URL when init resolves | Must send pageviews/analytics in `.then()`, not before init |
| v2.21.0 | `liff.init()` now **fails** with invalid LIFF ID (was silently succeeding) | Apps with wrong LIFF ID will break; ensure correct ID |
| v2.25.0 | `permanentLink.createUrlBy()` URL encoding changed for RFC 3986 compliance | `+` → `%2B`, `*` → `%2A`, `%20` no longer becomes `+`; test URL-sensitive logic |
| v2.27.2 | Console warning if `liff.init()` URL doesn't match endpoint URL | Not breaking, but surfaces misconfigurations visibly |

### Deprecations

| Deprecated | Replacement | Since |
|-----------|-------------|-------|
| `liff.scanCode()` | `liff.scanCodeV2()` | v2.15.0 |
| `liff.getLanguage()` | `liff.getAppLanguage()` | v2.24.0 |
| `liff.permanentLink.createUrl()` | `liff.permanentLink.createUrlBy()` | v2.18.0 (may be removed in v3) |
