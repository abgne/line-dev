# LIFF Navigation & URLs

## 1. LIFF URL Format

### Current Format
```
https://liff.line.me/{liffId}
https://liff.line.me/{liffId}/path?query=value#fragment
```

### LINE MINI App Format
```
https://miniapp.line.me/{liffId}
```

### Deprecated Formats (do not use)
```
https://line.me/R/app/{liffId}     ← deprecated
line://app/{liffId}                 ← deprecated
```

---

## 2. How LIFF URLs Open

LIFF URLs use **Universal Links** (iOS) and **App Links** (Android) to open inside the LINE app.

**No guarantee** which environment opens — behavior depends on OS, WebView implementations, and third-party app handling. Design your app to work in both LIFF browser and external browser.

### Redirect Flow

```
User clicks LIFF URL
  → LINE app opens LIFF browser
  → Primary redirect: LIFF server → Endpoint URL (liff.init() runs here)
  → Secondary redirect: SDK processes liff.state → final page displayed
```

---

## 3. liff.state Parameter

When a LIFF URL includes extra path/query/fragment, the SDK encodes it as `liff.state`:

```
LIFF URL: https://liff.line.me/{liffId}/path_A/?key1=value1#hash

Primary redirect:
  https://example.com/app/?liff.state=%2Fpath_A%2F%3Fkey1%3Dvalue1%23hash

Secondary redirect (after liff.init()):
  https://example.com/app/path_A/?key1=value1#hash
```

The secondary redirect URL concatenates:
1. Domain from Endpoint URL
2. Paths/query from Endpoint URL
3. Additional path/query/fragment from LIFF URL

### Composition Example

```
LIFF URL:     https://liff.line.me/{liffId}/path_A/?key1=value1#fragment
Endpoint URL: https://example.com/2020campaign/?key=value

Secondary redirect URL:
  https://example.com/2020campaign/path_A/?key=value&key1=value1#fragment
```

Domain + base path come from Endpoint URL; extra path + query + fragment come from the LIFF URL suffix.

---

## 4. Permanent Links

Generate shareable LIFF URLs that route to specific pages within your app.

### `liff.permanentLink.createUrl()`
Create permanent link for the **current page**:
```javascript
// Current URL: https://example.com/app/page1?foo=bar
const link = liff.permanentLink.createUrl();
// → https://liff.line.me/{liffId}/page1?foo=bar
```

### `liff.permanentLink.createUrlBy(url)`
Create permanent link from an **arbitrary URL**:
```javascript
const link = await liff.permanentLink.createUrlBy('https://example.com/app/page2');
// → https://liff.line.me/{liffId}/page2
```

### `liff.permanentLink.setExtraQueryParam(str)`
Append extra query parameters:
```javascript
liff.permanentLink.setExtraQueryParam('campaign=summer');
const link = liff.permanentLink.createUrl();
// → https://liff.line.me/{liffId}/page1?foo=bar&campaign=summer
```

**Constraint**: throws `LiffError` if the URL doesn't match the registered Endpoint URL.

---

## 5. LIFF-to-LIFF Transitions

Open another LIFF app from within the current one.

### Requirements
- LIFF SDK v2.4.1+
- Source LIFF app must be **Full** size
- Both apps must be properly initialized

### Behavior by Source Size

| Source Size | Target Size | Behavior |
|-------------|-------------|----------|
| Full | Full | Smooth transition, stays full screen |
| Full | Tall / Compact | Still displays full screen (target size ignored); **action button hidden** after transition |
| Tall / Compact | Any | Browser closes first, then destination opens |

Check support: `liff.isApiAvailable('multipleLiffTransition')`

### `chat_message.write` Scope After Transition

| How target is accessed | `chat_message.write` scope |
|----------------------|:---:|
| Via LIFF URL (`https://liff.line.me/{liffId}`) | Enabled |
| Via Endpoint URL directly | **Disabled** |

If disabled, `liff.sendMessages()` will fail with 403.

### liff.referrer Parameter
During LIFF-to-LIFF transitions via LIFF URL, the destination receives `liff.referrer` query parameter containing the percent-encoded previous URL.

```
Source: https://first.example.com/
Target URL: https://second.example.com/?liff.referrer=https%3A%2F%2Ffirst.example.com%2F
```

**Known bug**: `liff.referrer` is **not appended** in LINE versions 12.13.0 – 13.19.x. Not included when accessing via Endpoint URL directly.

### Transition Message
When the destination has a different LIFF ID, a message appears: "Switched to the {LIFF app name} app." This only indicates a LIFF ID change, not success/failure.

---

## 6. Browser Minimization

Suspend a LIFF browser to perform other actions in LINE. The browser appears as a floating icon.

### Requirements (ALL must be met)
- LINE for iOS 12.18.0+ or Android 15.0.0+
- Android: **Settings > Apps > LINE > Display over other apps** must be enabled
- LIFF app configured with **Full** view size
- `chat_message.write` scope **disabled**
- No overlapping modal windows
- iPadOS: not yet supported (TBD)

**LIFF-to-LIFF caveat**: After transition, even if the target displays in Full mode, minimization only works if the target's **configured** size is Full. A Tall/Compact app forced to Full display does NOT qualify.

### User Actions

| Action | Method |
|--------|--------|
| Minimize | Action button → "Minimize browser", swipe down, or tap in-app alert |
| Maximize | Tap the floating icon |
| Move | Drag the floating icon |

**Close behavior by LINE version:**

| LINE Version | iOS | Android |
|-------------|-----|---------|
| < 15.20.0 | Swipe icon off screen | Drag to close icon at bottom |
| ≥ 15.20.0 | Tap close button (top-right of icon) | Tap close button (top-right of icon) |

### Floating Icon Priority
1. Channel icon (LINE Login channel)
2. Favicon (LIFF app)
3. Default link icon (fallback)

---

## 7. Opening External URLs

### `liff.openWindow(params)`
```javascript
// Open in LINE's in-app browser
liff.openWindow({ url: 'https://example.com' });

// Open in external browser
liff.openWindow({ url: 'https://example.com', external: true });
```

- Default: opens in LINE's in-app browser
- External site transitions display a popup notification to the user
