# LINE Developers Console Setup

## Creating a LINE MINI App Channel

Anyone who is a permitted customer in the [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en) can create a LINE MINI App channel.

### Creation Steps

1. Access the [LINE Developers Console](https://developers.line.biz/console/) and select a provider
2. Click **Channels** > **Create a new channel** > **LINE MINI App**
3. Fill in channel fields (see table below)
4. Check the authority warranty box
5. Click **Create**
6. Read "Regarding Consent to Usage of Information" and click **Accept**

The channel is created as an **unverified MINI App**.

> **Apple Developer Program no longer required.** As of July 2025, an Apple Developer Program account is no longer needed to create or publish a LINE MINI App. Previously this was required for iOS distribution.

> **Cannot create a channel?** Link the Business ID used to log in to the Console to your LINE account. See [Link your Business ID](https://developers.line.biz/en/docs/line-developers-console/login-account/#link-business-account-with-line-account).

### Channel Fields

| Item | Required | Description |
|------|:--------:|-------------|
| Channel type | ✅ | Select **LINE MINI App** |
| Provider | ✅ | The channel's provider (shown on consent screen) |
| Region to provide the service | ✅ | Japan, Thailand, or Taiwan. Create separate channels for multiple regions |
| Channel icon | ❌ | See [guidelines.md § Icon Specifications](guidelines.md#icon-specifications) for specs |
| Channel name | ✅ | Cannot contain "LINE" or similar strings. Enter in English; use Localization for other languages |
| Channel description | ✅ | If dev company and service provider differ, notify user |
| Email address | ✅ | Email for important channel updates |
| Privacy policy URL | ✅* | App's privacy policy URL |
| Terms of use URL | ❌ | App's terms of use URL |
| Service company's country or region | ✅ | Must match region to provide service |
| LY Corporation Privacy Policy | ** | Required only for Thailand |

\* Only **certified providers** can set Privacy policy URL at channel creation time. Non-certified providers must set it after creating the channel.

\** Read and acknowledge [LY Corporation Privacy Policy](https://line.me/th/terms/policy/) (Thailand only).

Three agreement checkboxes are also required: LINE Developers Agreement, LINE MINI App Platform Agreement, and LINE MINI App Policy.

### Channel-Provider Linkage Precautions

- Once created, a channel **cannot be moved** to another provider
- User IDs differ per provider — the same user cannot be identified across different providers
- Special attention needed when: channels are managed by individuals/companies, unrelated services share a provider, or channels are under a service company's provider

See [Best practices for provider and channel management](https://developers.line.biz/en/docs/line-developers-console/best-practices-for-provider-and-channel-management/).

---

## Three Internal Channels

When you create a LINE MINI App channel, three internal channels are automatically created:

| Channel | Purpose | Status | Who can access |
|---------|---------|--------|----------------|
| **Developing** | Development and testing | Always "Developing" | Granted admins + testers |
| **Review** | LY Corporation reviews your app | Always "Developing" | Granted admins + LY reviewers |
| **Published** | Published to end users | Always "Published" | End users |

- Channel status **cannot be changed**
- To add testers, enroll them as testers of the LINE MINI App channel (see [Managing roles](https://developers.line.biz/en/docs/line-developers-console/managing-roles/))

## LIFF ID and Endpoint URL

Each internal channel has its **own LIFF ID** and **Endpoint URL**. You must deploy separate LIFF apps per channel.

```
Developing:  liff.init({ liffId: 'DEVELOPING_LIFF_ID' })  → deploy to Developing Endpoint URL
Review:      liff.init({ liffId: 'REVIEW_LIFF_ID' })      → deploy to Review Endpoint URL
Published:   liff.init({ liffId: 'PUBLISHED_LIFF_ID' })    → deploy to Published Endpoint URL
```

**Key rules:**
- Each `liff.init()` must use the LIFF ID matching the internal channel it runs on
- LIFF ID is part of the LIFF URL — share messages must use the URL matching the channel
- Cannot add multiple LIFF apps to a single internal channel

### LIFF URL Format

As of December 13, 2023:
```
Current:  https://miniapp.line.me/{liffId}
Previous: https://liff.line.me/{liffId}  ← still works (redirects)
```

Existing QR codes using the old URL continue to work.

### Basic Authentication for Pre-Release Access

Basic authentication restricts access to MINI Apps before release.

**How to use:** In the **Web app settings** tab, specify the URL with basic auth in the **Endpoint URL** for Developing or Review. A dialog box will prompt username/password in the LIFF browser.

**Conditions** (all must be met):
- Channel status is **"Not yet reviewed"** or **"Reviewing"**
- Opened in **LIFF browser** only

**Limitations:**
- Not available for LIFF Apps or MINI Apps with "Reflected" status
- Not available after a LIFF-to-LIFF transition
- Digest authentication is not supported
- Basic auth is a simple access restriction — LINE does not recommend or guarantee its security

## Channel Access Token

**Issue a separate token for each internal channel.** Do not use the Developing channel's token for Review or Published.

Channel ID and Channel Secret are found under **Channel basic settings** tab.

| Token Type | MINI App Support |
|------------|-----------------|
| **Stateless** (recommended) | ✅ Unlimited issuances, no lifecycle management |
| Short-lived | ✅ Supported but not recommended |
| Long-lived | ❌ Cannot be used |
| v2.1 (user-specified expiration) | ❌ Cannot be used |

## Country/Region Setting

When creating a channel, you must confirm that the **region to provide the service** matches the **company's country or region**. This is displayed to users on the consent screen.

- **Cannot be edited** after channel creation
- To change: include the request in **Reference materials for the review** when submitting for review

---

## Console Settings Display Mapping

Settings registered on the Console are displayed to users on various screens.

### Provider Settings

| Item | Displayed on |
|------|-------------|
| **Provider name** | Verification screen, Channel consent screen |

### Channel Basic Settings

| Item | Displayed on | Notes |
|------|-------------|-------|
| **Channel icon** | Action button, Multi-tab view, Verification screen, Channel consent screen, Service message footer, Add Shortcut screen | |
| **Channel name** | Same as icon | Enter in English. Auto-copied to **LIFF app name** under Web app settings. Use Localization for other languages |
| **Channel description** | Verification screen, Channel consent screen | Enter in English. Use Localization for other languages |
| **Privacy policy URL** | Channel consent screen | |
| **Localization** | Channel consent screen | |

### Channel Description for Outsourced Development

When the development company differs from the service provider, the channel description **must** contain:
1. Service company name
2. Development company name
3. Actual company name(s) to whom user data is provided

### Web App Settings

| Item | Displayed on |
|------|-------------|
| **Endpoint URL** | Add Shortcut screen |

### Consent Screen Details

- **Verified MINI Apps**: verified badge shown next to channel name
- **Uncertified provider**: note shown — "LY Corporation hasn't verified this service provider."

### Localization (Multi-Language Support)

Display language is determined by the user's **LINE language settings**. If content is not localized for the user's language, **English** is shown.

- Must localize in the major language(s) of the countries where the service is offered
- Localizable items: **Channel name** and **Channel description** (via Localization settings in Basic settings tab)

---

## Channel Consent Simplification Setup

Configurable only when:
- **Region** is "Japan"
- **Status** is "Not yet reviewed"

For channels created **before** January 8, 2026: turn on the toggle in the **Channel consent simplification** section on the **Web app settings** tab.

For channels created **on or after** January 8, 2026: **always enabled** — no configuration needed.

> Enabling automatically enables `openid` in the Scope section.

For behavioral details, see [features.md § Channel Consent Simplification](features.md#channel-consent-simplification).

---

## Channel Description

Used for two purposes:
1. Help users understand your service
2. Help LY Corporation reviewers understand your service during review

| | Channel name | Channel description |
|---|---|---|
| ❌ Bad | LINE FRIENDS STORE | LINE FRIENDS STORE is a store for LINE character goods. |
| ✅ Good | LINE FRIENDS STORE | This is a mobile ordering service at the LINE FRIENDS STORE. You can order and pay in advance and receive your merchandise at the store. |

## Web App Settings vs LINE Login LIFF Tab

The LINE MINI App channel's **Web app settings** tab has these restrictions compared to a LINE Login channel's LIFF tab:

| Restriction | Description |
|-------------|-------------|
| No additional LIFF apps | Cannot add apps beyond the default MINI App per internal channel |
| No per-app scope config | Cannot change scope or add friend option per LIFF app |
| No Module mode | Cannot configure Module mode (action button always visible) |

## Header Subtext Display

| Channel | Unverified | Verified |
|---------|-----------|----------|
| Developing | Domain of current page | Domain of current page |
| Review | Domain of current page | Domain of current page |
| Published | Domain of current page | **MINI App name + verified badge** |

---

## Settings Reflection

### Unverified MINI Apps

Changes on the LINE Developers Console reflect from **Developing → Published** automatically.

**Exceptions** (not reflected until verification review passes):
- Service message template
- Channel consent simplification

### Verified MINI Apps

Changes only apply to the **Developing** channel immediately. This allows free development without affecting live users.

| Channel | When settings are reflected |
|---------|---------------------------|
| Developing | Immediately on save |
| Review | Copied from Developing when **review begins** |
| Published | Copied from Developing when **published** |

---

## Re-review After Updating a Verified MINI App

After a MINI App becomes verified, certain Console changes trigger a mandatory re-review. All other settings can be updated freely.

### Settings That Require Re-review

| Console Tab | Fields |
|-------------|--------|
| **Basic settings** | Channel icon, Channel name, Channel description, Email address, Privacy policy URL, Terms of use URL, Localization, Linked LINE Official Account |
| **Web app settings** | shareTargetPicker, Channel consent simplification (*), Endpoint URL for Published, Scopes, Add friend option |
| **Business information** | Service company info, Development company info, Provider info |
| **Contact information** | All fields |
| **Service message template** | All fields |
| **In-app purchase** | All fields within "Apply to use in-app purchase" tab (also triggers a separate IAP re-review) |

(*) Channel consent simplification can only be updated for Japan channels created before January 8, 2026.

### Additional Rules

- **Changes outside the Console** (e.g., content served at Endpoint URL) do not require re-review but must comply with the [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en)
- **Inappropriate expressions** found in a released MINI App require immediate correction — failure may result in penalties
- **Temporary maintenance:** Replacing the Endpoint URL temporarily for maintenance does not require re-review. The page switch takes effect immediately

See [Re-review after updates](https://developers.line.biz/en/docs/line-mini-app/service/update-service/).
