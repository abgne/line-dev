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
- Playback duration: max **4 seconds**
- Loops: **1–4 times** (total playback must not exceed 4 seconds)
- Size rule: within 320x270 px, one dimension must reach 270px
- Single file: < 1MB
- ZIP archive: < 60MB

### Animated Sticker Notes
- Remove white borders; no padding needed
- All frames within a single APNG must have consistent dimensions
- **First frame** serves as the preview in LINE Store and static display
- All image backgrounds must be transparent
- Chat room tab image automatically displays a play symbol — do not add manually
- Avoid identical frames across all images (prevents animation playback)
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
- Playback duration: max **4 seconds** (total including all loops)
- Loops: **1–4 times**
- Single file: **< 300KB**
- ZIP archive: < 20MB
- Background must be transparent
- File extension must be `.png`

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

### Required Images (41 required + 3 optional = 44 max)

| Type | Quantity | Required? | Purpose |
|------|----------|-----------|---------|
| Main images (thumbnails) | 3 | Yes | Store display (iOS / Android / LINE STORE) |
| Menu button images | 18 | Yes | 9 buttons × OFF/ON states |
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
- **9 buttons × 2 states (OFF/ON) = 18 images**
- **Size: 128x150 px** each
- **~10px margin** around icon design
- Notification badge: 33x33 px (positioned at top-right, 49px from top, 21px from right)

| Button | OFF Filename | ON Filename |
|--------|-------------|-------------|
| Home | `i_29.png` | `i_30.png` |
| Chat | `i_03.png` | `i_04.png` |
| VOOM | `i_33.png` | `i_34.png` |
| Shopping | `i_35.png` | `i_36.png` |
| Call | `i_07.png` | `i_08.png` |
| News | `i_25.png` | `i_26.png` |
| TODAY | `i_31.png` | `i_32.png` |
| Wallet | `i_27.png` | `i_28.png` |
| MINI | `i_37.png` | `i_38.png` |

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
Customizable areas: chat bubbles (self/other), text color, navigation bar text, menu text, timestamp, read receipt, link color.

### Color Settings
Customizable areas: chat bubbles (self/other), text color, navigation bar text, menu text, timestamp, read receipt, link color. A `colorskin_brown.zip` template is available as reference.

### Theme Design Tips
- **Contrast**: Ensure text is clearly readable against background
- **Consistency**: Maintain a cohesive color palette throughout
- **Readability**: Avoid overly vibrant or dark combinations
- **Long-term use**: Avoid visual fatigue
- Tile mode requires seamless pattern design
- Normal/selected (OFF/ON) icon states must be clearly distinguishable
- Adobe Photoshop CS6+ required for official PSD template
- ZIP archive: < 30MB
- For detailed design best practices, see [theme-specs.md](theme-specs.md)
