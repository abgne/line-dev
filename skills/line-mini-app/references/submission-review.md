# Submission & Review Process

> **Prerequisite:** LINE MINI App channels start as unverified with restricted features. To become verified, the app must pass review by LY Corporation.

> **Taiwan / Thailand:** Only LINE MINI App channels under a **certified provider** can apply for verification review.

## Pre-Review Checklist

Before submitting, confirm all of the following:

| Area | Requirements |
|------|-------------|
| **Design** | Icon specs ([guidelines.md § Icon](guidelines.md#icon-specifications)), safe area ([guidelines.md § Safe Area](guidelines.md#safe-area-for-notched-devices)), loading icon ([features.md § Loading Icon](features.md#loading-icon)) |
| **Performance** | Follows [performance guidelines](https://developers.line.biz/en/docs/line-mini-app/develop/performance-guidelines/) |
| **Policy** | Adheres to [LINE MINI App Policy](https://terms2.line.me/LINE_MINI_App?lang=en) and [guidelines.md § Policy Rules](guidelines.md#line-mini-app-policy-rules) |
| **Console accuracy** | Provider name = actual service provider company |
| | Channel description accurately describes the service (see [console-setup.md § Channel Description](console-setup.md#channel-description)) |
| | Privacy policy company name matches provider name |
| **LIFF URL consistency** | Published channel and Review channel LIFF URLs reflect the same service. Settings are auto-copied to the Review channel when review begins (see [console-setup.md § Settings Reflection](console-setup.md#settings-reflection)) |

## Submitting the Application

### Step 1: Enter required information

Go to the LINE Developers Console > your LINE MINI App channel > **Review request** tab.

- Review results are displayed on the Console and sent to the registered email address
- If the Endpoint URL uses **basic authentication**, provide credentials in **Reference materials for the review**

### Step 2: Provide test materials (if applicable)

Services involving **reservations, payments, or orders** must enter test scenarios in **Reference materials for the review**:
- Test accounts
- Test products
- Test stores

### In-app purchase coordination

| Constraint | Detail |
|------------|--------|
| Must apply for IAP separately first | Turn on "Apply to publish in-app purchase" toggle in the Review request tab |
| Cannot submit verification review while IAP application is under review | Wait for IAP approval first |
| Cannot apply for IAP while verification review is ongoing | Submit one at a time |

See [in-app-purchase.md](in-app-purchase.md) for IAP details.

## Cancellation Rules

| Review status | Can cancel? | Can change settings? |
|---------------|:-----------:|:-------------------:|
| Before review begins | ✅ (Cancel review request button) | ✅ |
| Reviewing | ❌ | ❌ |

During "Reviewing" status, the Review channel's LIFF URL is accessible to LY Corporation reviewers.

## Review Period

- Approximately **1–2 weeks**
- If rejected: allow a few more days for re-application and re-review
- **Cannot specify a completion date**

## Multiple MINI Apps

To submit multiple LINE MINI Apps:

1. Submit **one** first
2. After that app is approved, request **batch review** for the remaining apps

## After Approval

### First-time submission

```
Status flow: "Approved" → immediately "Reflected" (live, but not yet searchable)
```

1. Status automatically changes to "Approved" → immediately "Reflected" (app is live and accessible via URL, but **not searchable** in LINE yet)
2. Use the **Search enable** button on the Review request tab to make the MINI App searchable in LINE
3. If Search enable is **not clicked within 30 days** → auto-enabled at 9:00 AM JST on day 31 (may delay 1–2 hours)
4. After search is enabled, status returns to "Not yet reviewed" — settings can be changed and resubmitted

### Re-review (already published)

```
Status flow: "Approved" → (manual) → "Reflected"
```

1. Status changes to "Approved"
2. Use the **Publish changes** button to change status to "Reflected"
3. If Publish changes is **not clicked within 30 days** → auto-reflected at 9:00 AM JST on day 31
4. After reflection, status returns to "Not yet reviewed"

**Changes do not affect the published MINI App** until the review passes AND Publish changes is clicked (or auto-reflected after 30 days).

For which Console settings trigger a re-review, see [console-setup.md § Re-review](console-setup.md#re-review-after-updating-a-verified-mini-app).

## Provider Certification

| Region | Effect of passing review |
|--------|------------------------|
| **Japan** | Provider becomes a **certified provider** |
| Other regions | No automatic certification |

Certified provider status affects features like the [OA friend add-friend option](features.md#oa-friend-inducement-add-friend-option) being enabled by default.

See [Submitting LINE MINI App](https://developers.line.biz/en/docs/line-mini-app/submit/submission-guide/).
