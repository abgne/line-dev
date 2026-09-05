# LINE Creative Product Technical Specifications

Sources:
- LINE Creators Market Official Guidelines (`https://creator.line.me/{lang}/guideline/` — see creators-market-guide.md for language codes)
- Production guidelines for all 7 sticker types, emoji, animated emoji, and themes

> **Two creation paths exist**: (1) **Creators Market web** — full control, all product types, ~10 day review; (2) **LINE Sticker Maker app** — photo/video-based, static + animated stickers only, ~2 day review. Specs below apply to both paths unless noted.

---

## Static Stickers

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images | 8 / 16 / 24 / 32 / 40 | Max 370x320 px | PNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Technical Requirements
- Width and height must be **even numbers**
- Background must be **transparent**
- Resolution: 72 dpi or higher
- Color mode: RGB
- Single file: < 1MB
- ZIP archive: < 60MB
- Maintain approximately **10px margin** on all sides

### Text Field Limits

| Field | Limit |
|-------|-------|
| Creator name | 50 characters |
| Sticker title | 40 characters |
| Description | 160 characters |
| Copyright mark | 50 characters (alphanumeric only) |

> Full-width characters count as 2. Emoji are not supported.

---

## Animated Stickers

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | APNG |
| Animated stickers | 8 / 16 / 24 | Max 320x270 px | APNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### APNG Specifications
- Frames: **5–20 frames**
- **One loop must be exactly 1, 2, 3 or 4 seconds — decimals (e.g. 1.5s) are NOT accepted**
- Loops: **1–4 times**; `one loop × loops` must not exceed **4 seconds**
- Size rule: within 320x270 px, and **one side must be ≥ 270px** (not "exactly 270")
- Single file: < 1MB
- ZIP archive: < 60MB

> **The integer-second rule applies to ONE LOOP, not the total.** `5 frames × 100ms × 4 loops`
> totals 2000ms but each loop is only 500ms — rejected. Pick `frames × per-frame-ms` so the
> loop lands exactly on 1000/2000/3000/4000 ms, e.g. **10 × 100ms**, 8 × 125ms, 20 × 50ms.
> Source: `creator.line.me/{lang}/guideline/animationsticker/detail/`

### File Naming (ZIP upload)
- `main.png` (240×240 APNG) + `tab.png` (96×74 static PNG) + zero-padded `01.png`, `02.png` …
- Put every file at the **ZIP root** — no top-level folder, no unrelated files

### Animated Sticker Notes
- **Remove white borders — crop away transparent area outside the union of ALL frames.**
  Official wording: 「圖片請勿留白邊」. Use one shared bbox for every frame so the character
  does not jitter (all frames must keep identical canvas dimensions).
- All frames within a single APNG must have consistent dimensions
- **First frame** serves as the preview in LINE Store and static display.
  Official guidance: **make the first and last frame the same image** so the loop closes and
  the static preview carries the intended emotion.
- All image backgrounds must be transparent
- Chat room tab image automatically displays a play symbol — do not add manually
- Avoid identical frames across all images (prevents animation playback).
  **Consecutive identical frames may be collapsed into a single frame by APNG tools**, and an
  APNG whose frames are all identical fails at upload. Ensure at least two frames visibly differ.
- **`tab.png` transparency**: stray semi-transparent fragments away from the character trigger
  a rule 1.1 rejection (`背景の一部が部分的に透過漏れしています > tab`). Inspect at ≥6× zoom on a
  checkerboard — a white browser background will not reveal them.
- **Product type is fixed at creation**: a static sticker product cannot be converted to an
  animated sticker product; create a new product with the correct type.
- **Tip**: Images from existing static stickers already on sale can be reused to create animated versions

---

## Custom Stickers (隨你填貼圖)

Custom stickers allow users to input their own text on the sticker after purchase.

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images | 8 / 16 / 24 / 32 / 40 | Max 370x320 px | PNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Key Features
- Creators define **text style information** (font, size, direction, position) embedded in images
- Users can repeatedly edit the text in designated areas after purchase
- Available fonts: Japanese, Western, Traditional Chinese, Thai
- **Does not support animation**
- **Not eligible** for LINE Sticker Premium or Sticker Arranger

### Sales Region Restrictions
| Option | Coverage |
|--------|----------|
| Japan only | Japan |
| Taiwan, Macau, Hong Kong only | Taiwan, Macau, Hong Kong |
| Thailand only | Thailand |
| Custom selection | All other regions (cannot include Japan/Taiwan/HK/Macau/Thailand) |

> Once a sales region option is selected and submitted, it cannot be changed to a different region group.

---

## Message Stickers (訊息貼圖)

Message stickers allow users to freely input text messages within the sticker.

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images | 8 / 16 / 24 | Max 370x320 px | PNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Key Features
- Users can freely input text messages (up to 100 characters) after purchase
- Text size automatically adjusts based on character count
- System auto-adds white border — **creators do NOT need to add padding/margin**
- **Does not support animation**
- **Does not support tag setting**
- **Not eligible** for LINE Sticker Premium or Sticker Arranger
- Same sales region restrictions as Custom stickers
- Production guidelines: https://creator.line.me/{lang}/guideline/messagesticker/

---

## Big Stickers (大貼圖)

Big stickers are displayed larger than standard stickers in chat.

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images | 8 / 16 / 24 / 32 / 40 | Min 80x524, Max 396x660 px | PNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Key Features
- **Dimensions differ from standard stickers** — portrait-oriented, larger canvas
- System auto-adds white border
- **Does not support animation**
- Eligible for LINE Sticker Premium
- Production guidelines: https://creator.line.me/{lang}/guideline/bigsticker/

---

## Popup Stickers (全螢幕貼圖)

Popup stickers display a full-screen animation or image when sent.

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images (thumbnail) | 8 / 16 / 24 | Max 370x320 px | PNG |
| Popup main image | 1 | 480x480 px | APNG |
| Popup layer images | 8 / 16 / 24 | Max 480x480 px | APNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Popup Layer Size Rules
- Maximum: 480x480 px — **one side must be exactly 480 px**
- If width = 480 → height ≥ 320
- If height = 480 → width ≥ 200

### APNG Specifications (Popup Layer)
- Frames: **5–20 frames**
- Playback duration: max **3 seconds** per sticker
- Loops: **1–3 times**
- File extension must be `.png` (not `.apng`)

### Key Features
- Full-screen popup animation when sticker is tapped/sent
- Includes both a thumbnail sticker and a popup version
- System auto-adds white border to thumbnail stickers only
- **Not eligible** for Sticker Arranger
- Eligible for LINE Sticker Premium
- ZIP upload limit: 51 images total
- Production guidelines: https://creator.line.me/{lang}/guideline/popupsticker/

---

## Effect Stickers (特效貼圖)

Effect stickers display a special visual effect overlaying the chat screen.

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Main image | 1 | 240x240 px | PNG |
| Sticker images (thumbnail) | 8 / 16 / 24 | Max 370x320 px | PNG |
| Effect main image | 1 | 480x480 px | APNG |
| Effect images | 8 / 16 / 24 | Max 480x480 px | APNG |
| Chat room tab image | 1 | 96x74 px | PNG |

### Effect Image Size Rules
- Maximum: 480x480 px — **one side must be exactly 480 px**
- If width = 480 → height ≥ 320
- If height = 480 → width ≥ 200

### APNG Specifications (Effect Layer)
- Frames: **5–20 frames**
- Playback duration: max **3 seconds** per sticker
- Loops: **1–3 times**

### Key Features
- Visual effect overlays the entire chat screen
- Includes both a thumbnail sticker and an effect version
- System auto-adds white border to thumbnail stickers (370×320 → 420×350) — **effect images do NOT get white border**
- **Not eligible** for Sticker Arranger
- Eligible for LINE Sticker Premium
- ZIP upload limit: 51 images total
- Production guidelines: https://creator.line.me/{lang}/guideline/effectsticker/

---

## Sticker Count Summary

| Type | Available Counts |
|------|-----------------|
| Static / Custom / Big | 8, 16, 24, 32, 40 |
| Animated / Message / Popup / Effect | 8, 16, 24 |

---

## Emoji

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Chat room tab image | 1 | 96x74 px | PNG |
| Emoji images | See combinations below | 180x180 px | PNG |

### Quantity Combinations

| Type | Quantity Range |
|------|---------------|
| Emoji only | 8–40 |
| Alphabet (Hiragana + Katakana + English) + Emoji | 273–305 |
| Alphabet (Hiragana + Katakana) + Emoji | 169–201 |
| Alphabet (English) + Emoji | 112–144 |
| Alphabet only (Hiragana + Katakana + English) | 265 |
| Alphabet only (Hiragana + Katakana) | 161 |
| Alphabet only (English) | 104 |

### Technical Requirements
- Background transparent
- Resolution: 72 dpi or higher
- Color mode: RGB
- Single file: < 1MB (static emoji); < 300KB (animated emoji)
- ZIP archive: < 20MB

### Emoji Design Tips
- **Thick, dark outlines** maximize visibility at small sizes
- **Minimize blank space** — utilize full 180x180 px canvas
- Design expressions that remain clear at small display sizes
- Place frequently-used emoji first
- Include varied poses and full-body variations
- Sequential emoji can create narrative effects
- Maintain legible spacing for alphabet combinations
- Avoid sparkles, hearts, comic-style lines — keep designs bold and simple

---

## Animated Emoji

### Required Images

| Item | Quantity | Size | Format |
|------|----------|------|--------|
| Chat room tab image | 1 | 96x74 px | PNG |
| Animated emoji images | Same combinations as static emoji | 180x180 px | APNG |

### APNG Specifications
- Frames: **5–20 frames**
- **One loop must be exactly 1, 2, 3 or 4 seconds — decimals are NOT accepted**
- Loops: **1–4 times**; `one loop × loops` must not exceed **4 seconds**
- Single file: **< 300KB**
- ZIP archive: < 20MB
- Background must be transparent
- File extension must be `.png`
- File naming: zero-padded `001.png`, `002.png` … plus `tab.png`, all at the **ZIP root**

> Same integer-second rule as animated stickers — it governs ONE LOOP, not the total.
> Source: `creator.line.me/{lang}/guideline/animationemoji/detail/`
> Trimming transparent margin matters more here: the 180×180 canvas is small, and official
> guidance warns against letting the artwork shrink (可視性 drops).

### Design Tips
- Animations must be clearly visible at small display sizes
- Use bold, dynamic movements
- Same quantity combinations as static emoji

### Emoji vs Sticker Differences

| Feature | Emoji | Sticker |
|---------|-------|---------|
| Usage | Embedded in text | Standalone message |
| Size | 180x180 px | Max 370x320 px |
| Design focus | Small-size legibility, thick lines | Rich expression detail |
| Best for | Message accents, quick reactions | Full emotional expression |

---

## Themes

> Snapshot 2026-09-05. Sources: the detail guideline (`creator.line.me/{lang}/guideline/theme/detail/`) and the official Photoshop template ZIP (`line_creators_theme_template.zip`, last modified 2026-07-07). The overview page (`/guideline/theme/`) still says 34 menu buttons / 60 images; the detail page and the template both hold 36 / 62. Follow the template — it is what you actually export.

### Required Images (59 required + 3 optional = 62 max)

| Type | Quantity | Required? | Purpose |
|------|----------|-----------|---------|
| Main images (thumbnails) | 3 | Yes | Store display (iOS / Android / LINE STORE) |
| Menu button images — standard | 18 | Yes | 9 buttons × OFF/ON, iOS 25 and earlier + Android |
| Menu button images — iOS 26 | 18 | Yes | Same 9 buttons × OFF/ON, iOS 26 and later (`_g` suffix) |
| Menu background | 1 | Optional | Menu backdrop |
| Password screen images | 16 | Yes | 4 positions × OFF/ON × iOS/Android |
| Profile images | 4 | Yes | 2 types × iOS/Android |
| Chat background images | 2 | Optional | Chat room background |

### Main Image (Thumbnail) Sizes

| Platform | Filename | Size |
|----------|----------|------|
| iOS | `ios_thumbnail.png` | 200x284 px |
| Android | `android_thumbnail.png` | 136x202 px |
| LINE STORE | `store_thumbnail.png` | 198x278 px |

> Main thumbnails must NOT have transparent backgrounds.

### Menu Button Images

Since iOS 26 (Liquid Glass tab bar) every button needs **two** images per state. Both sets ship in the template ZIP and both must be provided when submitting for review; the detail guideline dates the iOS 26 set as "applied from August 2026 onward".

| Set | Applies to | Filename | Size | Icon margin | Notification badge |
|-----|-----------|----------|------|-------------|--------------------|
| Standard | iOS 25 and earlier, Android | `i_NN.png` | 128x150 px (portrait) | ~10px around the icon | 33x33 px, 49px from top, 21px from right |
| iOS 26 | iOS 26 and later | `i_NN_g.png` | 80x56 px (landscape) | Keep the icon balanced top/bottom/left/right | 32x32 px, top-right of the image area |

- **9 buttons × 2 states (OFF/ON) × 2 sets = 36 images**
- The iOS 26 canvas is landscape and less than half the height of the standard one — redraw the icon, don't scale the 128x150 file down (review 1.2 catches illegible icons)
- Official note for the iOS 26 set: check how the icon looks when placed over a transparent background — in some situations the menu is drawn over one
- Both sets must read as the same icon (review 1.8 rejects icons that look significantly different across OS)

| Button | Standard OFF | Standard ON | iOS 26 OFF | iOS 26 ON |
|--------|-------------|-------------|------------|-----------|
| Home | `i_29.png` | `i_30.png` | `i_29_g.png` | `i_30_g.png` |
| Chat | `i_03.png` | `i_04.png` | `i_03_g.png` | `i_04_g.png` |
| VOOM | `i_33.png` | `i_34.png` | `i_33_g.png` | `i_34_g.png` |
| Shopping | `i_35.png` | `i_36.png` | `i_35_g.png` | `i_36_g.png` |
| Call | `i_07.png` | `i_08.png` | `i_07_g.png` | `i_08_g.png` |
| News | `i_25.png` | `i_26.png` | `i_25_g.png` | `i_26_g.png` |
| TODAY | `i_31.png` | `i_32.png` | `i_31_g.png` | `i_32_g.png` |
| Wallet | `i_27.png` | `i_28.png` | `i_27_g.png` | `i_28_g.png` |
| MINI (Apps) | `i_37.png` | `i_38.png` | `i_37_g.png` | `i_38_g.png` |

### Menu Background
- Filename: `i_11.png`
- Size: **1472x150 px** (height range: 100–150 px)
- 0–100px area: must NOT be transparent; 101–150px area: may be transparent
- Left-aligned; **image repeats/tiles** — ensure seamless edge connection

### Password Screen Images

| Position | iOS (OFF/ON) | iOS Size | Android (OFF/ON) | Android Size |
|----------|-------------|----------|------------------|--------------|
| 1st | `i_12.png` / `i_13.png` | 120x120 px | `a_12.png` / `a_13.png` | 116x116 px |
| 2nd | `i_14.png` / `i_15.png` | 120x120 px | `a_14.png` / `a_15.png` | 116x116 px |
| 3rd | `i_16.png` / `i_17.png` | 120x120 px | `a_16.png` / `a_17.png` | 116x116 px |
| 4th | `i_18.png` / `i_19.png` | 120x120 px | `a_18.png` / `a_19.png` | 116x116 px |

> All 4 positions can use the same image, or each position can have a unique design.

### Profile Images
- Auto-cropped to circle on display

| Type | iOS Filename | iOS Size | Android Filename | Android Size |
|------|-------------|----------|-----------------|--------------|
| Personal | `i_20.png` | 240x240 px | `a_20.png` | 247x247 px |
| Group | `i_21.png` | 240x240 px | `a_21.png` | 247x247 px |

### Chat Room Background

| Spec | iOS | Android |
|------|-----|---------|
| Filename | `i_22.png` | `a_22.png` |
| Max size | 1482x1334 px | 1300x1300 px |
| Min size | 60x60 px | 60x60 px |
| Recommended (portrait) | 640x1334 px | — |
| Position | Above message input | Below message input (overlaps) |

> Transparent backgrounds are supported — transparent images layer over the color scheme background. Match background colors to prevent visual gaps on larger screens.

### Color Settings
Customizable areas: chat bubbles (self/other), text color, navigation bar text, menu text, timestamp, read receipt, link color. The template ZIP includes `colorskin_brown.zip` (all 62 PNGs in one brown skin): upload it on the Edit Theme page's Images tab in Creators Market to preview a color skin before drawing your own.

### Theme Design Tips
- **Contrast**: Ensure text is clearly readable against background
- **Consistency**: Maintain a cohesive color palette throughout
- **Readability**: Avoid overly vibrant or dark combinations
- **Long-term use**: Avoid visual fatigue
- Tile mode requires seamless pattern design
- Normal/selected (OFF/ON) icon states must be clearly distinguishable
- Draw the 80x56 iOS 26 icon first, then the 128x150 one — what survives the small landscape canvas scales up; the reverse does not hold
- Official PSD template uses artboards: Photoshop CC required, **not compatible with CS6 or older**. File > Generate > Image Assets exports the numbered folders and files
- ZIP archive: < 30MB
- For detailed design best practices, see [theme-specs.md](theme-specs.md)
