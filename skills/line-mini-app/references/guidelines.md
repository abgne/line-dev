# LINE MINI App Guidelines

## What is LINE MINI App

LINE MINI App is a web application that runs on LINE. "LINE MINI App" is the official name. Users use their LINE account to access services within LINE without downloading a separate app. Developers provide services without building a native app.

**Platform scale (November 2025):** 17.5 million monthly active users, 27,800+ released services.

**Common use cases:** Digital membership cards, mobile ordering, reservation & queue management, coupons & stamp cards, games & entertainment, campaigns.

**Industries:** Retail, food service, beauty, sports, education, real estate, finance, government.

LINE MINI App is built on LIFF. All [LIFF app development guidelines](https://developers.line.biz/en/docs/liff/development-guidelines/) also apply. Basic rules are based on [Terms and Policies](https://developers.line.biz/en/terms-and-policies/) and the [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en).

> **Future:** LIFF and LINE MINI App will be integrated into a single brand. See [features.md § LIFF vs MINI App Differences](features.md#liff-vs-mini-app-differences) for details.

---

## LINE MINI App Policy Rules

> Source: [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en). Consult before development and submission.

### Eligibility

| Region | Certified MINI App | Uncertified MINI App |
|--------|-------------------|---------------------|
| Japan | Organizations with Corporate Number, individual business owners | Organizations, individual business owners, individuals |
| Taiwan / Thailand | Organizations with TAX ID | Organizations with TAX ID, individuals |

### Restricted Business Categories

The following categories **cannot** operate LINE MINI Apps (some may be approved on exception — consult LINE before development):

Religious organizations, adult entertainment venues, gambling/slot machines, dating/matchmaking, lending agencies, fundraising/donations/crowdfunding, multi-level marketing, cigarettes/e-cigarettes, weapons/poisons, unapproved overseas medicines, clinical trials, investment/self-development seminars, private investigation, politics, animal/insect sales

### App Naming Rules

| Rule | Detail |
|------|--------|
| Brand alignment | Match existing native app / website name |
| Uniqueness | Different names required for multiple apps from same provider |
| Proper nouns | Use proper nouns; avoid generics like "waiting" or "order" |
| No LINE confusion | Do not imply official LINE association |
| Length | Max **20 characters** (truncated with "..." beyond that) |

### Top Page Requirements

| Requirement | Detail |
|-------------|--------|
| Display trigger | Must display when users open the LIFF URL |
| Load time | Must load within **3 seconds** (1 second recommended) |
| No confusion | Cannot show text-only pages or error screens |
| No redirects | Avoid redirecting away from the top page |

### Privacy and Disclosure

When developer company differs from service provider, the Channel consent screen and privacy policy must show:
- Service company name
- Link to privacy policy page

Privacy policy must disclose third-party data sharing: who receives data, what data, and when.

### Feature Containment

Main features must be provided **only within the LINE MINI App**. Do not redirect users to external apps/websites for core functionality.

**Permitted external redirects:** transaction/auth processes, native app payment flows, privacy/terms/company pages, map apps for location.

### In-App Purchase Mandate

When offering paid digital items, you **must** use LINE's in-app purchase function. No alternative payment systems permitted.

### Content Standards

- Content must be appropriate for all ages
- Endpoint URL must be accessible from Safari and Chrome
- Must hold proper copyright for all materials

### Enforcement

LY Corporation may impose **without obligation to explain**: app deletion, service suspension, contract termination, function suspension, or certification revocation.

---

## Development to Release

```
1. Create LINE MINI App channel → Start developing (unverified MINI App)
2. Submit for review
3. Pass review → Provide service as verified MINI App
```

> **Taiwan / Thailand:** Only channels under a **certified provider** can apply for verification review.

> **Japan:** After passing review, the provider becomes a **certified provider**.

For the full submission and review process, see [submission-review.md](submission-review.md).

### Verified vs Unverified

| Capability | Unverified | Verified |
|------------|:---------:|:--------:|
| Development & testing | ✅ | ✅ |
| Service Messages (Published channel) | ✗ | ✅ |
| Common Profile Quick Fill | ✗ | ✅ (requires application) |
| In-App Purchase | ✗ | ✅ (Japan only, requires application) |
| Custom Path (branded URL) | ✗ | ✅ |
| Home screen shortcut | ✗ | ✅ (LINE ≥14.3.0) |
| Minimize browser | ✗ | ✅ |
| Favorites (Wallet tab) | ✗ | ✅ (Japan, LINE ≥15.18.0) |
| About the service (Provider page) | ✗ | ✅ |
| Verified badge in header | ✗ | ✅ |
| Listed in MINI App directory / Search | ✗ | ✅ |
| Custom action button | ✅ | ✅ |
| OA friend inducement | ✅ | ✅ |
| Payment (LINE Pay, credit cards) | ✅ | ✅ |

For full feature details, see [features.md](features.md).

## Key Documentation by Role

### Service Planners
- [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en) — review before submission

### Developers
- [Specifications](https://developers.line.biz/en/docs/line-mini-app/discover/specifications/) — platform/version support, LIFF support versions
- [Start developing](https://developers.line.biz/en/docs/line-mini-app/develop/develop-overview/)
- [Custom action button (share messages)](https://developers.line.biz/en/docs/line-mini-app/develop/share-messages/)
- [Service messages](https://developers.line.biz/en/docs/line-mini-app/develop/service-messages/)
- [Payment systems](https://developers.line.biz/en/docs/line-mini-app/develop/payment/) — LINE Pay and others
- [Permanent links](https://developers.line.biz/en/docs/line-mini-app/develop/permanent-links/)
- [Console settings](https://developers.line.biz/en/docs/line-mini-app/develop/configure-console/)
- [External browser notes](https://developers.line.biz/en/docs/line-mini-app/develop/external-browser/)
- [Performance guide](https://developers.line.biz/en/docs/line-mini-app/develop/performance-guidelines/)

### Designers
- [Icon specifications and guidelines](https://developers.line.biz/en/docs/line-mini-app/design/line-mini-app-icon/)
- [Safe area for landscape mode](https://developers.line.biz/en/docs/line-mini-app/design/landscape/) — CSS safe area for notched devices
- [Loading icon](https://developers.line.biz/en/docs/line-mini-app/design/loading-icon/) — recommended UI element, use specified files

### Service Operators & Marketers
- [Service operation guide](https://developers.line.biz/en/docs/line-mini-app/service/service-operation/)
- [Ads in LINE MINI Apps](https://developers.line.biz/en/docs/line-mini-app/service/line-mini-app-ads/)
- [Re-review after updates](https://developers.line.biz/en/docs/line-mini-app/service/update-service/)
- [Use LINE Official Account](https://developers.line.biz/en/docs/line-mini-app/service/line-mini-app-oa/)

## Specifications

- **HTML5**: almost all HTML5 specs usable (Geolocation API, Google Maps, media elements). Check [caniuse.com](https://caniuse.com) for browser support
- **Minimum LIFF SDK**: v2.1. All LIFF v2.1.x APIs available
- **Supported platforms**: based on LIFF's [recommended operating environment](https://developers.line.biz/en/docs/liff/overview/#operating-environment). Subject to change without notice
- **External browser**: as of October 2025, users can use MINI App in web browser (previously redirected to LINE app). Design for non-LINE users. See [features.md § External Browser](features.md#external-browser-behavior) and [announcement](https://developers.line.biz/en/news/2025/09/26/mini-app-browser/)
- **Two API types**: LIFF API (called from the MINI App client) and Service Message API (called from server-side). LIFF API is constantly being improved

## LIFF vs MINI App Restrictions

See [features.md § LIFF vs MINI App Differences](features.md#liff-vs-mini-app-differences) for the full comparison table (module mode, multiple LIFF apps).

## MINI App Components

- [Built-in & custom features](features.md) — action button, multi-tab view, custom path, payments, UI components
- [Console setup](console-setup.md) — 3 internal channels, LIFF ID, tokens, settings reflection

---

## Performance Guidelines

Use [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) or [PageSpeed Insights](https://pagespeed.web.dev/) to measure performance.

| Tool | Recommended Score |
|------|------------------|
| Lighthouse | Performance: **50 and above** |

**Measurement notes:**
- Measure **without** executing LINE Login (otherwise the Login page performance is measured, not the MINI App)
- Measure in the **production environment** (network can affect the score)

See [Performance guidelines](https://developers.line.biz/en/docs/line-mini-app/develop/performance-guidelines/).

## Development Recommendations

- Use HTML5 [Geolocation API](https://www.w3.org/TR/geolocation/) for locating users
- Utilize LINE profile information (via LIFF API) to auto-fill forms and reduce manual entry (e.g., restaurant reservations)
- Optimize performance to meet the recommended Lighthouse score
- Design for external browser access — ensure core features work without LINE Login

## Migrating a Web App to LINE MINI App

To implement an existing web app as a LINE MINI App:

1. **Create** a LINE MINI App channel (see [console-setup.md](console-setup.md))
2. **Load** the LIFF SDK (CDN: `https://static.line-scdn.net/liff/edge/2/sdk.js` or npm: `@line/liff`)
3. **Initialize** with `liff.init({ liffId: "..." })`
4. **Implement** features: LIFF API (login, profile), Service Messages, HTML5 APIs
5. **Configure** the Endpoint URL in the channel settings
6. **Submit** for review (unverified → verified)

A Business ID is required to access the LINE Developers Console.

See [Implementing web apps as LINE MINI Apps](https://developers.line.biz/en/docs/line-mini-app/develop/web-app/).

---

## Development Rules

### Prohibiting Mass Requests

Do NOT send mass requests to the LINE Platform for load testing via:
- LIFF scheme (`https://miniapp.line.me/{liffId}`)
- LIFF API
- Service Message API

For load testing, prepare a test environment that does not generate requests to the LINE Platform.

Rate limit exceeded → `429 Too Many Requests`.

## Saving Logs

**LINE does not provide logs.** Developers must save their own logs.

### Service Message API Request Logs

Save the following for each Service Message API request:

| Field | Example |
|-------|---------|
| Time | `Mon, 16 Jul 2021 10:20:23 GMT` |
| Request method | `POST` |
| API endpoint | `https://api.line.me/message/v3/notifier/send?target=service` |
| Status code | `200` |
| `notificationToken` | From response |

**Also useful to log:**
- Request body
- Full response body (beyond `notificationToken`)

## Deauthorize on User Unregistration

When a user **unregisters** from your MINI App or **terminates the link** between your app and LINE:

1. **Call the deauthorize endpoint** on behalf of the user:
   ```
   POST https://api.line.me/user/v1/deauthorize
   ```
   See [Deauthorize API](https://developers.line.biz/en/reference/line-login/#deauthorize).

2. **Disclose in terms/registration flow** that unregistration will notify LY Corporation and terminate the link. Examples:
   - "If you unsubscribe from the service, LY Corporation will be notified and the link between the service and LINE app will be terminated."
   - "If you do this, LY Corporation will be notified and the link between the service and LINE app will be terminated."

### Why This Matters

When a user authorizes a MINI App, it appears in LINE app **Settings > Account > Authorized apps**. If you don't deauthorize on unregistration, the permissions remain authorized even after the user leaves your service.

See [Managing authorized apps](https://developers.line.biz/en/docs/line-login/managing-authorized-apps/).

---

## Quick Fill Design Regulations

> **Violating these rules may result in Quick-fill permission being revoked.**

For full visual examples, see [Common Profile Quick-fill design regulations](https://developers.line.biz/en/docs/line-mini-app/quick-fill/design-regulations/).

### Recommended Screen Transitions

When integrating Quick-fill, use one of these recommended patterns:

| Pattern | Description |
|---------|-------------|
| Immediate modal | Call `get()` immediately when user navigates to registration screen. Place Auto-fill button so user can re-trigger if modal is closed |
| On form focus | Call `get()` when user selects an input field on the form |
| On button tap | Call `get()` when user taps the Auto-fill button |
| Post-consent | After user taps **Allow** on the channel consent screen, transition directly to registration screen and call `get()` immediately. Place Auto-fill button for re-triggering |

### Prohibited Screen Transitions

| Violation | Description |
|-----------|-------------|
| Modal without form | Displaying the Quick-fill modal on a screen that has no form to auto-fill |
| Requesting unused scopes | Getting profile items that don't exist in the form (e.g. requesting phonetic info when there's no kana field) |
| Skipping auto-fill | Moving to confirmation/completion screen after user taps Auto-fill without actually filling the form fields |

### Auto-fill Button Guidelines

LINE provides **4 types / 13 button variants**. You must use these official buttons — custom buttons are prohibited.

**Critical rules:**
- Use buttons **as-is** — no modifications, animations, or effects
- **Do not** zoom, rotate, skew, italicize, add shadows/borders/3D, overlay elements, or hide the button
- **Do not** add text below the button or use custom replacement buttons
- Align button with **left or center** of the form input field
- Leave **10px margin** on all sides of the button
- Place button where the user can **see the form** that will be filled
- **Load button images from the official URL** — do not download and host. URLs may change with notice

### Button Types

| Type | Size | Variants | Description |
|------|------|----------|-------------|
| A | 264×73px | 4 colors (black, white, gray, blue) | With Account Center branding |
| B | 264×73px | 4 colors (black, white, gray, blue) | Simple style |
| C | 264×73px | 1 (white only) | With LY branding |
| D | 288×66px | 4 colors (white, black, gray, blue) | With LINE branding |

**Note:** Button images are served at 2x size. Display at the specified dimensions, not the raw image size.

### Button URLs

**Type A** (ALT: `ユーザー情報を自動入力。LINEやYahoo! JAPANに登録した情報を利用できます`):

| Color | URL |
|-------|-----|
| Black | `https://account-center-fe.line-scdn.net/images/quick_fill_button_AC_black.png` |
| White | `https://account-center-fe.line-scdn.net/images/quick_fill_button_AC_white.png` |
| Gray | `https://account-center-fe.line-scdn.net/images/quick_fill_button_AC_gray.png` |
| Blue | `https://account-center-fe.line-scdn.net/images/quick_fill_button_AC_blue.png` |

**Type B** (same ALT as Type A):

| Color | URL |
|-------|-----|
| Black | `https://account-center-fe.line-scdn.net/images/quick_fill_button_simple_black.png` |
| White | `https://account-center-fe.line-scdn.net/images/quick_fill_button_simple_white.png` |
| Gray | `https://account-center-fe.line-scdn.net/images/quick_fill_button_simple_gray.png` |
| Blue | `https://account-center-fe.line-scdn.net/images/quick_fill_button_simple_blue.png` |

**Type C** (same ALT as Type A):

| Color | URL |
|-------|-----|
| White | `https://account-center-fe.line-scdn.net/images/quick_fill_button_LY_white.png` |

**Type D** (ALT: `LINEで自動入力しますか？氏名、電話番号、メールアドレス、住所など。自動入力`):

| Color | URL |
|-------|-----|
| White | `https://account-center-fe.line-scdn.net/images/quick_fill_button_LINE_white.png` |
| Black | `https://account-center-fe.line-scdn.net/images/quick_fill_button_LINE_black.png` |
| Gray | `https://account-center-fe.line-scdn.net/images/quick_fill_button_LINE_gray.png` |
| Blue | `https://account-center-fe.line-scdn.net/images/quick_fill_button_LINE_blue.png` |

---

## Icon Specifications

The LINE MINI App icon appears on the channel consent screen, the Home tab, LINE messages, and service messages.

### Dimensions

| Property | Value |
|----------|-------|
| Background (canvas) size | 130 × 130 px |
| Logo size (minimum) | 54 × 54 px |
| Logo size (maximum) | 90 × 90 px |
| Recommended logo size | 54 × 54 px to 76 × 76 px |

### Design Rules

- **Prohibited:** Do not include the LINE MINI App logo in your icon
- **Recommended:** Design the logo as a stand-alone icon or wordmark for best visibility at small sizes
- PSD template available: [icon_template_file.psd](https://vos.line-scdn.net/line-developers/docs/media/line-mini/icon_template_file.psd)

### Outline Color by Background

| Background color | Outline color | Outline opacity |
|------------------|---------------|-----------------|
| White (#FFFFFF) | Black (#000000) | 12% |
| Black (#000000) / Dark (#181818) | White (#FFFFFF) | 8% |
| Other colors | Black (#000000) | 8% |

### Upload

- Upload from **Channel icon** in the **Basic settings** tab of the LINE Developers Console
- Accepted formats: **PNG** and **JPEG** only
- The uploaded image is automatically cropped and the icon background becomes transparent
- The logo must fit within the green square shown in the preview

See [Icon specifications and guidelines](https://developers.line.biz/en/docs/line-mini-app/design/line-mini-app-icon/).

---

## Safe Area for Notched Devices

Devices with a notch can obscure parts of the MINI App UI. Apply CSS padding to keep content within the visible safe area.

### Normal Mode

| Edge | Padding |
|------|---------|
| Bottom | 34px |

```css
{
  padding-bottom: 34px;
}
```

### Landscape Mode

| Edge | Padding |
|------|---------|
| Left | 44px |
| Right | 44px |
| Bottom | 21px |

```css
{
  padding-right: 44px;
  padding-bottom: 21px;
  padding-left: 44px;
}
```

See [Safe area for landscape mode](https://developers.line.biz/en/docs/line-mini-app/design/landscape/).

---

## Ads (Monetization)

LINE MINI Apps can display ads for monetization. The only permitted ad network is **Yahoo! JAPAN Ads** (launched **July 15, 2025**).

| Constraint | Detail |
|------------|--------|
| Ad network | Yahoo! JAPAN Ads only |
| Region | **Japan only** (service must be provided in Japan) |
| MINI App type | Both verified and unverified |
| Ad review | All ads reviewed and approved by LY Corporation |

### Setup Process

1. **Read the documentation** (PDF, Japanese only): [Yahoo! JAPAN Ads Network Partner guide](https://s.yimg.jp/images/listing/partnerportal/document/yahooads_networkpartner_lineminiapp.pdf)
2. **Apply to become a Yahoo! JAPAN Ads Network Partner** — [application form](https://form-business.yahoo.co.jp/claris/enqueteForm?inquiry_type=publisher_pn_application) (Japanese only)
3. **Request site review** via the Network Partner Tool (provided after partner approval)
4. **After passing review**, issue ad placement tags and follow provided instructions

All documentation and application forms are currently **Japanese only**.

See [Ads in LINE MINI Apps](https://developers.line.biz/en/docs/line-mini-app/service/line-mini-app-ads/).
