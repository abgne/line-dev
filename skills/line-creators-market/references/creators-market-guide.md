# LINE Creators Market Platform Guide

Sources:
- LINE Creators Market (https://creator.line.me/zh-hant/)
- LINE CREATORS MARKET Manual (https://linecreator-manual-tw.blog.jp/)

---

## Platform Overview

LINE Creators Market is LINE's official marketplace for selling creative digital products.

- **Open to**: Everyone — regardless of profession, age, amateur/professional, individual/corporate
- **Registration requirement**: Active LINE account (with email and password configured)
- **Sales reach**: 230+ countries worldwide
- **Supported products**: Static stickers, animated stickers, popup stickers, custom stickers, message stickers, big stickers, emoji, themes
- **Submission limit**: Maximum **30 submissions per day**

---

## Account Registration

1. Go to https://creator.line.me/zh-hant/
2. Log in with your LINE account
3. Agree to terms of service
4. Enter business information
   - **Business type**: Select "Corporation" or "Individual"
   - **Name**: Enter company name or personal name
5. Receive confirmation email → Click link to verify
6. Log back in to access creator dashboard

> **Email delivery issues**: Some email domains have reported problems receiving registration emails (as of 2023/9): `icloud.com`, `me.com`, `mac.com`, `mikadonguyen.com`, `sniarti.fi`, `ssy.email`, `thma.com.tw`. If no email is received after 30 minutes, retry with a Gmail or other provider. Also check spam/junk folders, and whitelist the domain `line.me` if using domain-based filtering.

> **Business type can only be changed once** after registration. Change requests are accepted from the 1st to the 20th of each month (Japan time). The 21st to month-end is processing time.

---

## AI Usage Declaration

Creators can declare whether AI was used to create or process their products (stickers/emoji/themes).

- Set via the **"AI Usage"** field during product creation or editing
- When set to "Uses AI", a label is automatically displayed on the purchase page in LINE Sticker Shop, Theme Shop, and LINE STORE
- **Must accurately reflect actual usage** — LINE may change the setting based on their judgment
- Products imitating copyrighted characters via AI generation are prohibited
- LINE may request the AI prompts/instructions used during creation; inability to provide may result in rejection or delisting
- For products already on sale: changing only the AI usage flag to "Uses AI" does not require re-review
- After changing AI usage setting, it takes up to 24 hours to apply

---

## Product Registration (Sticker Example)

### Step 1: Create New Product
From your personal page, click "Add New" → Select product type (Sticker / Theme / Emoji)

### Step 2: Text Information — Product Details

| Field | Description | Notes |
|-------|-------------|-------|
| Sticker type | Static / Animated / Custom / Message / Big / Popup / Effect | **Cannot be changed once selected** |
| Language | Supports 12 languages | **English is required** |
| Title | Character limits per language | Must be unique across stickers |
| Description | Character limits per language | English version should include "Sticker" |

> The 12 supported languages: English (required), Japanese, Korean, Simplified Chinese, Traditional Chinese, Thai, Indonesian, German, French, Italian, Portuguese (Brazil), Spanish. Languages not configured will display in English.

### Step 3: Text Information — Sales Details

| Field | Description |
|-------|-------------|
| Creator name | Displayed consistently across all products |
| Copyright mark | Alphanumeric only, <= 50 characters |
| Category | Style and character categories (optional) |
| Sales regions | 230+ countries selectable |
| Privacy setting | Whether to display in "New" and "Rankings" |

#### Privacy Setting Details
When set to "Do not display in LINE STORE / Sticker Shop":
- Does not appear in "New" or "Rankings" categories
- Does not appear in category or keyword search results
- **Direct purchase link remains accessible to all users** (suitable for limited sales)

#### Review-Related Fields
| Field | Purpose |
|-------|---------|
| Photo usage | Review reference |
| Rights certificate | Prove original content (URL or file upload) |
| Additional notes | Extra information for reviewers |

### Step 4: Upload Images

**Upload methods:**
- **ZIP archive**: Bulk upload; filenames must match specifications
- **Individual upload**: No filename format required

**Notes:**
- Sticker count can be changed before submission
- Individual or all images can be deleted at any time
- Technical specs: see [sticker-specs.md](sticker-specs.md)

### Step 5: Set Tags

- **Prerequisite**: Images must be uploaded before tags can be set
- Maximum **9 tags** per sticker or emoji
- Multi-language tags supported
- Tags affect auto-suggest functionality — choose accurately
- Message stickers do not support tag setting

### Step 6: Set Price

#### Sticker Price Options (NTD)
| Price | Availability |
|-------|-------------|
| NTD 30 | Static stickers only (not for animated) |
| NTD 60 | All types |
| NTD 90 | All types |
| NTD 120 | All types |
| NTD 150 | All types |

#### Theme Pricing Note
- NTD 30 and NTD 60: **Not available when Japan is included in sales regions**
- NTD 90 / 120 / 150: Available for all regions

> To change the price of a product already on sale: Suspend sales → wait 3 hours → change price → relaunch. Cannot change price again within 24 hours after relaunching. Suspending sales automatically sets LINE Sticker Premium participation to "Not participating".

### Step 7: Submit for Review
After confirming all settings, click "Submit" to enter the review process.

---

## Theme Registration Notes

Theme registration follows a similar flow to stickers, with additional considerations:

1. **Image count**: 44 images total (main images, menu buttons, lock screen, etc.)
2. **Color settings**: Customizable color scheme and chat background color
3. **Cross-platform preview**: Preview iOS / Android display in different languages
4. **Photoshop template**: Official PSD template available for download
5. Technical specs: see [sticker-specs.md](sticker-specs.md) (Themes section)

---

## Review Process

### Status Flow

```
Submitted → Awaiting Review → Under Review → In Review Processing → Approved / Rejected
```

| Status | Editable? | Description |
|--------|-----------|-------------|
| Editing | Yes | Creator is editing, not yet submitted |
| Awaiting Review | Yes — can return to edit page | Submitted, review has not started |
| Under Review | No — must cancel to edit | Review in progress |
| In Review Processing | No — cannot cancel | Final processing |
| Rejected | Yes — both text and images | Fix and resubmit |
| Approved | Text only — images locked | Ready to launch |
| On Sale | Price/text editable | Product is live |
| Sales Suspended | Can relaunch | Creator suspended sales |
| Not For Sale | Cannot relaunch | Forcibly suspended by LINE |

### Review Timeline
- Typically completed within **10 business days**
- Longer during pre-holiday submission surges (Halloween, Christmas, etc.)
- Products containing non-Japanese languages take longer to review
- Recommend preparing seasonal items **1-2 months** in advance

### Rejection Reason Categories
1. **Terms of Service violation** — Breaching platform agreements
2. **Review Guidelines violation** — Failing to meet review criteria
3. **Production Guidelines violation** — Not meeting technical specs

> Detailed rejection reasons are documented in the "Message Center" and sent via email.

### Handling Rejections
1. Go to item management page, select the rejected product
2. Click the "Message Center" button on the right side of the status column
3. Read the rejection reason and make corrections
4. You can reply to content-related questions through the Message Center
5. Resubmit after corrections are complete

### Complete Review Guidelines

Source: https://creator.line.me/zh-hant/review_guideline/

#### 1. Images (Sticker images, main image, chat room tab image)
| # | Guideline |
|---|-----------|
| 1.1 | Does not comply with company specifications |
| 1.2 | Not suitable for use in conversations or communication |
| 1.3 | Difficult to recognize (e.g., elongated images, full-body 8-head-proportion figures) |
| 1.4 | Overall sticker set is clearly unbalanced (e.g., all pale colors, simple number sequences) |
| 1.5 | Logo/trademark only |
| 1.6 | Text-only images with no illustration |
| 1.7 | Text errors within sticker |
| 1.8 | Contradicts description or title |
| 1.9 | Main image or tab image significantly differs from actual sticker images |
| 1.10 | Duplicates stickers already on sale or under review in the Sticker Shop |

> **Emoji differences**: 1.7 becomes "duplicates within same set"; 1.8 becomes "duplicates existing emoji on sale"
> **Theme differences**: 1.2 becomes "icon corruption, icons blending with background"; 1.7 includes "same icon with only color change"; 1.8 includes "significantly different icons across OS"

#### 2. Text (Title, description, creator name, copyright)
| # | Guideline |
|---|-----------|
| 2.1 | Does not comply with company specifications |
| 2.2 | Text errors |
| 2.3 | Title or description contains announcements (e.g., "Scheduled for sale on XX/XX", "Search for XX") |
| 2.4 | Contains URLs |
| 2.5 | Contains emoji or device-dependent characters |
| 2.6 | Content too short |
| 2.7 | Contradicts sticker images |

#### 3. Morality
| # | Prohibited Content |
|---|-------------------|
| 3.1 | Promotes or encourages criminal activity |
| 3.2 | Depicts violence against children, child abuse, or child pornography |
| 3.3 | Excessively revealing content |
| 3.4 | Encourages excessive alcohol consumption, illegal drugs, or underage purchase of alcohol/tobacco |
| 3.5 | Promotes drunk driving |
| 3.6 | Realistic depictions of illegal weapons or encourages their use |
| 3.7 | Intended for phishing or spam messaging |
| 3.8 | Realistic depictions of killing, attacking, stabbing, or torturing humans or animals |
| 3.9 | Potentially defamatory, slanderous, or attacking toward specific individuals, corporations, nations, or groups |
| 3.10 | Discloses or risks disclosing personal information of third parties or oneself |
| 3.11 | Contains excessively offensive or vulgar content |
| 3.12 | Attacks religion, culture, ethnicity, or nationality, or is particularly offensive to others |
| 3.13 | Solicits or inspires religious conversion, or contains strongly religious elements |
| 3.14 | Contains political or election-related content |
| 3.15 | Design that may confuse or repulse users |
| 3.16 | Contains sexual content |
| 3.17 | Promotes gambling or gambling-like content |
| 3.18 | Intended to obtain user passwords or personal privacy data |
| 3.19 | May be harmful to youth development (e.g., pachinko, horse racing) |
| 3.20 | Induces or promotes suicide, self-harm, or drug abuse |
| 3.21 | Induces or promotes bullying behavior |
| 3.22 | Promotes discrimination or may promote discrimination |
| 3.23 | Contains other anti-social content or may be offensive to others |

#### 4. Business, Advertising, and Others
| # | Guideline |
|---|-----------|
| 4.1 | Requires personal information or ID to purchase |
| 4.2 | Intended for distribution to third parties beyond personal use (e.g., corporate giveaways) |
| 4.3 | References messaging apps, similar services, or related characters |
| 4.4 | Intended for commercial advertising or promotion (including recruitment) |
| 4.5 | For charitable relief or fundraising |
| 4.6 | Solicits membership or donations for political, religious, or anti-social organizations |

#### 5. Rights and Law
| # | Guideline |
|---|-----------|
| 5.1 | Infringes company or third-party intellectual property rights (trademarks, copyrights, patents), or violates third-party usage terms |
| 5.2 | Unclear rights ownership (e.g., fan art / derivative works) |
| 5.3 | Infringes portrait or publicity rights (e.g., using someone's likeness without consent) |
| 5.4 | Cannot prove authorization from rights holders |
| 5.5 | Violates regional laws where the service is provided, or infringes third-party rights/interests |

#### General Provisions
The company may determine stickers as inappropriate during review or suspend their sale. Even if content matches the above situations, stickers may still be deemed appropriate depending on content, sales region, and creator attributes. If photos are used as materials, the company may request copyright verification documents.

---

## Launching for Sale

### Prerequisite
Product status must be "Approved".

### Process
Item Management → Select approved product → Click "Launch".

### Post-Launch Restrictions
- **Images**: Cannot be modified
- **Text information**: Can be modified, but requires re-review
- **Deletion**: Published products cannot be deleted, but sales can be suspended
- **Free download**: Stickers submitted via LINE Sticker Maker (after 2019/6/26) can be downloaded free by the creator only
- Products may take 1-several hours to appear in Sticker Shop/Theme Shop after launch

---

## Revenue Model

### Revenue Calculation — Individual Sales

```
Creator Revenue = (Confirmed Sales - Platform Fees) x 50%
```

#### Platform Fee Rates
| Platform | Fee Rate |
|----------|----------|
| Apple App Store (Japan, from 2026/1/1) | **26%** of sales |
| Apple App Store (non-Japan, or Japan before 2025/12/31) | **30%** of sales |
| Google Play | **30%** of sales |
| LINE STORE (web) | **30%** of sales |

**In practice, creators receive approximately 35-37% of the sale price.**

### Revenue Calculation — LINE Sticker Premium

```
Creator Share = (Premium Total Sales x 30%) x (Users of this product / Total users of all Premium products)
```

- Numerator: number of Premium subscribers who used/applied this product
- Denominator: total user count across all Premium-eligible products (each product counted separately)

### LINE Coin Exchange Rates

Sales via LINE Coins are converted to JPY using LINE's set exchange rate:

| Period | Japan Rate | Non-Japan Rate |
|--------|-----------|---------------|
| Before 2015/4/30 | 1 Coin = ¥1.47 | 1 Coin = ¥1.47 |
| 2015/5/1 – 2023/12/31 | 1 Coin = ¥1.76 | 1 Coin = ¥1.76 |
| 2024/1/1 – 2024/11/30 | 1 Coin = ¥2.16 | 1 Coin = ¥1.76 |
| From 2024/12/1 | 1 Coin = ¥2.13 | 1 Coin = ¥1.76 |

> All amounts in the creator dashboard are displayed in JPY regardless of creator's country.

### Income Tax Withholding

| Creator Type | Tax Rate |
|-------------|----------|
| Japan resident — individual (≤ ¥1,000,000) | 10.21% |
| Japan resident — individual (> ¥1,000,000) | (amount - ¥1,000,000) × 20.42% + ¥102,100 |
| Japan resident — corporation | 0% (not withheld) |
| Non-Japan resident (individual or corporation) | **20.42%** flat rate |

> Non-Japan residents in countries with a tax treaty with Japan can apply for reduction/exemption by submitting the "Application Form for Income Tax Convention". Tax is calculated at the time of withdrawal request.

### Payment Methods

| Location | Payment Method |
|----------|---------------|
| Japan | Domestic bank transfer (fee: ¥495) |
| Non-Japan & non-Thailand | PayPal (**Select or Business accounts only** — personal accounts not accepted) |
| Thailand (Individual) | LINE Pay e-wallet or Thai domestic bank transfer |
| Thailand (Corporate) | Thai domestic bank transfer |

#### Transfer Fees
| Method | Fee |
|--------|-----|
| Japan bank transfer | ¥495 |
| PayPal | 2% of amount (max ¥5,000) + optional currency conversion fee |
| Thailand bank transfer | 50 THB (converted to JPY at request time) |

#### PayPal Notes
- Amounts exceeding ¥1,000,000 may be transferred in installments
- Japan residents cannot use PayPal
- Must configure PayPal to accept JPY payments; unclaimed transfers are cancelled after 30 days

### Requesting Withdrawal

| Item | Details |
|------|---------|
| Minimum threshold | **¥1,000** (cannot request below this) |
| Processing period | Mid-month is settlement period — requests unavailable during this window |
| Transfer timeline | Within **90 days** after withdrawal request |
| Income tax | Automatically withheld at time of request; reduction available via tax treaty |

### Withdrawal Records Include
- Request date, amount, transfer fees
- CSV format transaction details (Revenue Share, VAT, Return, Sales, Share Amount)
- PDF payment statement
- Estimated transfer date (reference only, not guaranteed)

---

## LINE Sticker Premium (Subscription)

- Eligible after products have been on sale for **180+ days**
- **Available countries**: Japan, Taiwan, Indonesia, Thailand only
- Sales regions must include at least one of: Japan, Taiwan, Indonesia, or Thailand
- Users pay monthly fee for unlimited access to all Premium products
- Default setting is "Participate" — opt-out is available
- Changes take effect on the **1st of the following month**

### Eligible Products
| Eligible | Not Eligible |
|----------|-------------|
| Static stickers | Custom stickers (隨你填貼圖) |
| Animated stickers | Message stickers (訊息貼圖) |
| Big stickers | |
| Popup stickers | |
| Effect stickers | |
| Emoji (static & animated) | |
| Themes | |

### Notes
- Products participating in LINE Creators Collaboration cannot join Premium
- Even when participating in Premium, individual sales continue as normal
- Sticker Arranger usage also counts toward Premium revenue share

---

## Platform Tools

### Simulator
Preview stickers in chat room context before submission; check thumbnail legibility.

### LINE Sticker Maker App (LINE拍貼)

Mobile app for creating stickers directly from photos and videos — no design experience required.

**Platforms:**
- iOS: https://itunes.apple.com/jp/app/line/id1239684967
- Android: https://play.google.com/store/apps/details?id=com.linecorp.usersticker

**System Requirements:**
- LINE Sticker Maker 6.4+ (7.0+ for photo-to-animated)
- iOS 15+ / Android 6+
- App languages: Japanese, English, Traditional Chinese, Thai, Indonesian

**Capabilities:**
- Create static stickers from photos (crop, decorate, add text, filters)
- Create animated stickers from video clips or photo sequences
- Built-in editing: auto-crop, outline tracing, eraser, brushes, frames, stickers, text
- On-device face/animal detection for frame positioning (data not stored or shared)
- Submit directly to LINE Creators Market for review

**Sticker Counts in App:**
- Static stickers: 8 / 16 / 24 / 32 / 40
- Animated stickers: **8 / 16 only** (not 24)

**Photo-to-Animated Sticker Timing:**
| Photos Selected | Playback Duration |
|----------------|------------------|
| 1–5 photos | 1 second |
| 6–10 photos | 2 seconds |
| 11–15 photos | 3 seconds |
| 16–20 photos | 4 seconds |

**Animated Sticker Settings (in-app):**
- **Loop**: 1 sec = max 4 loops, 2 sec = max 2 loops, 3+ sec = no loop
- **Frame rate**: Low (5 fps), Medium (10 fps), High (20 fps)
- **Quality**: Low / Medium / High (affects color palette processing)
- File size limit: < 1MB per animated sticker

**Pricing Options (JPY):**
¥120 / ¥250 / ¥370 / ¥490 / ¥610

**Revenue Sharing — Key Difference from Web Submission:**
- Stickers submitted via the app **after 2019/6/26** are **free to download by default** (no creator revenue)
- To earn revenue, creator must select **"Paid download / With revenue sharing"** during submission (requires LINE Sticker Maker 4.0+)
- Creator can **free-download their own stickers** (app-submitted after 2019/6/26, unless set to paid)

**Review Timeline:**
- Approximately **2 days**, fastest within hours (significantly faster than web-submitted ~10 days)

**Review Tips (App-Specific):**
- Minimize sales regions to reduce review scope — fewer regions = fewer items to check
- Do not use content infringing others' rights, celebrities, or cartoon characters
- Do not use immoral or offensive content
- Do not use for commercial or promotional purposes
- Check [portrait rights guidelines](https://creator-mag-tw.weblog.to/archives/27376979.html) before using real-person photos

**Handling Rejected Stickers (App → Web Workflow):**
- Rejected stickers **cannot be edited or resubmitted** through the app
- Must use the web dashboard (LINE Creators Market my page):
  1. Go to [Item Management] > [Stickers], click the sticker set with status [Rejected]
  2. Click [Message Center] next to the status
  3. Read rejection reason and make corrections
  4. Return to [Item Management] > [Stickers], click the corrected set
  5. Click [Submit] at the top right to resubmit
- Rejection notification is also sent to the registered email
- Rejected app stickers are treated as new sticker sets on resubmission (cannot reuse same set name)

**Limitations vs Web (Creators Market):**
- Cannot register a new account through the app — must use web
- Cannot stop sales or manage payment accounts through the app — must use web dashboard
- Cannot edit stickers already submitted for review or on sale — must use web
- Rejected stickers are treated as new sticker sets on resubmission (cannot reuse same name)
- Animated stickers created in app cannot be saved to device or shared (static stickers can)
- Only supports static + animated stickers (no custom, message, big, popup, effect, emoji, or themes)

**Image Processing Notes:**
- System auto-processes images after upload (resizing, compression) — may cause color tone changes
- To minimize processing artifacts: use **sRGB** color space, reduce color variety, minimize file size

### Sales Statistics
- Overview dashboard: Overall sales trends
- Item details: Individual product performance, sales distribution by market

### Display Suggest Tags
After setting tags, stickers/emoji can appear as text input suggestions when users type — significantly increases exposure.

### Sticker Arranger
Users can resize, rotate, and combine stickers creatively.
- Default setting is "Participate" — opt-out available
- **Not available for**: Popup stickers, Effect stickers, Custom stickers, Message stickers
- Products in LINE Creators Collaboration generally cannot use Sticker Arranger
- Sticker Arranger usage counts toward Premium revenue share
- Setting changes take up to 5 business days to apply

### Message Center
- Receive review result notifications
- View rejection reasons
- Communicate with the review team

### LINE PR Stamps (Japan Only)
Businesses can distribute stickers for free via PR Stamps, with configurable download conditions (e.g., following official account). Suitable for brand collaboration promotions.

---

## Product Management

### Suspending / Resuming Sales
- Sales can be suspended at any time
- Suspended products can be relaunched

### Editable After Launch
- Title, description (requires re-review)
- Price (changeable at any time)
- Sales regions

### Cannot Be Changed
- Sticker images (locked after launch)
- Sticker type
- Sticker count (locked after submission)

### Submission Limits
- Maximum **30 review submissions per day**
- No limit on the number of products that can be on sale simultaneously

---

## Official Resources

### Creators Market Multi-Language Portals

| Language | URL |
|----------|-----|
| Japanese | https://creator.line.me/ja/ |
| Traditional Chinese | https://creator.line.me/zh-hant/ |
| English | https://creator.line.me/en/ |
| Thai | https://creator.line.me/th/ |
| Korean | https://creator.line.me/ko/ |
| Indonesian | https://creator.line.me/id/ |
| Simplified Chinese | https://creator.line.me/zh-hans/ |

### Guidelines & Manuals

| Resource | URL |
|----------|-----|
| Static Sticker Guidelines | https://creator.line.me/zh-hant/guideline/sticker/ |
| Animated Sticker Guidelines | https://creator.line.me/zh-hant/guideline/animationsticker/ |
| Custom Sticker Guidelines | https://creator.line.me/zh-hant/guideline/customsticker/ |
| Message Sticker Guidelines | https://creator.line.me/zh-hant/guideline/messagesticker/ |
| Big Sticker Guidelines | https://creator.line.me/zh-hant/guideline/bigsticker/ |
| Popup Sticker Guidelines | https://creator.line.me/zh-hant/guideline/popupsticker/ |
| Effect Sticker Guidelines | https://creator.line.me/zh-hant/guideline/effectsticker/ |
| Emoji Production Guidelines | https://creator.line.me/zh-hant/guideline/emoji/ |
| Animated Emoji Guidelines | https://creator.line.me/zh-hant/guideline/animationemoji/ |
| Theme Production Guidelines | https://creator.line.me/zh-hant/guideline/theme/ |
| Review Guidelines | https://creator.line.me/zh-hant/review_guideline/ |
| Custom Sticker Font List | https://creator.line.me/zh-hant/guideline/customsticker/font/ |
| Creator Manual (Taiwan) | https://linecreator-manual-tw.blog.jp/ |
| Portrait Rights Guide (Taiwan) | https://creator-mag-tw.weblog.to/archives/27376979.html |

### Support

| Resource | URL |
|----------|-----|
| Official Blog | http://creator-mag.line.me/tw/ |
| FAQ | https://help2.line.me/creators/web/ |
| Contact Support | https://contact.line.me/serviceId/10569 |
