# Flex Message

Highly customizable message layout based on CSS Flexbox. Three-layer structure: **Container → Block → Component**.

## Limits

| Item | Limit |
|------|-------|
| JSON size (Bubble) | **30 KB** |
| JSON size (Carousel) | **50 KB** |
| `altText` | Max **400** chars |
| Bubbles per Carousel | Max **12** |
| Messages per request | Max 5 (same as all message types) |
| Animated images per message | Max **3**, each max **300 KB** |

These are hard limits — exceeding them returns an error. JSON size is calculated after serialization; use the Flex Message Simulator to check.

## Containers

### Bubble

Single message card. At least one block (header/hero/body/footer) is required.

| Property | Type | Description |
|----------|------|-------------|
| `size` | String | `nano` / `micro` / `deca` / `hecto` / `kilo` (default) / `mega` / `giga` |
| `direction` | String | `ltr` (default) / `rtl`. Affects horizontal layout order and text alignment |
| `action` | Object | Action on tap (entire bubble). Same action types as other contexts |
| `styles` | Object | Per-block style overrides (see Styles section) |

**Size details:**

| Size | Max width | Notes |
|------|-----------|-------|
| `nano` | ~120px | Very compact, limited content |
| `micro` | ~150px | Compact |
| `deca` | ~200px | LINE 13.17.0+ (iOS/Android) |
| `hecto` | ~250px | LINE 13.17.0+ (iOS/Android) |
| `kilo` | ~300px | **Default** |
| `mega` | ~400px | |
| `giga` | ~450px | |

### Carousel

Horizontally scrollable collection of Bubbles.

```json
{"type": "carousel", "contents": [{"type": "bubble", ...}, {"type": "bubble", ...}]}
```

- Max **12** bubbles
- All bubbles share the same `direction` (set on each bubble, but keep consistent)
- **Video in hero block is NOT supported** in Carousel bubbles

## Blocks

Compose a Bubble. Fixed order: **Header → Hero → Body → Footer**. All optional, but at least one required.

| Block | Typical use | Content type |
|-------|-------------|--------------|
| `header` | Title, labels | Box component |
| `hero` | Key visual (image or video) | Image or Video component directly (not wrapped in Box) |
| `body` | Main content | Box component |
| `footer` | Actions, supplementary info | Box component |

Header, body, and footer contain a **Box** as their root component. Hero contains an **Image** or **Video** directly.

## Components

### Box

Layout container. Can be nested.

| Property | Type | Description |
|----------|------|-------------|
| `layout` | String | **Required.** `horizontal` / `vertical` / `baseline` |
| `contents` | Array | Child components |
| `spacing` | String | Gap between children. `none`/`xs`/`sm`/`md`/`lg`/`xl`/`xxl` or pixel (`12px`) |
| `margin` | String | Margin before this box. Same values as spacing. **Overrides parent's `spacing`** for this child |
| `padding` | String | Inner padding. `none`/`xs`/`sm`/`md`/`lg`/`xl`/`xxl`, pixel (`12px`), or percentage (`5%`). Also `paddingTop`/`paddingBottom`/`paddingStart`/`paddingEnd` |
| `flex` | Number | Flex grow factor. Default: **1** in horizontal, **0** in vertical |
| `width` | String | Fixed or max width. Pixel or percentage |
| `height` | String | Fixed or max height. Pixel or percentage |
| `maxWidth` | String | Max width constraint. Pixel or percentage |
| `maxHeight` | String | Max height constraint. Pixel or percentage |
| `justifyContent` | String | Main-axis alignment: `flex-start`/`center`/`flex-end`/`space-between`/`space-around`/`space-evenly` |
| `alignItems` | String | Cross-axis alignment: `flex-start`/`center`/`flex-end` |
| `cornerRadius` | String | Border radius. `none`/`xs`/`sm`/`md`/`lg`/`xl`/`xxl` or pixel. Requires `overflow: hidden` to clip children |
| `background` | Object | Background. Supports `linearGradient` (see below) |
| `position` | String | `relative` (default) / `absolute`. Absolute removes from flow, positioned via offsets |
| `offsetTop` | String | Offset from top. Pixel or percentage. Only when `position: absolute` or relative offset |
| `offsetBottom` | String | Offset from bottom |
| `offsetStart` | String | Offset from start (left in ltr) |
| `offsetEnd` | String | Offset from end (right in ltr) |
| `action` | Object | Action on tap |

**Linear gradient background:**
```json
{
  "type": "linearGradient",
  "angle": "0deg",
  "startColor": "#ff0000",
  "endColor": "#0000ff",
  "centerColor": "#00ff00",
  "centerPosition": "50%"
}
```
`angle`: `0deg` (bottom→top) to `360deg`. `centerColor` and `centerPosition` are optional.

**Baseline layout limitations:**
- Only `Text`, `Icon`, `Span`, and `Filler` allowed as direct children
- `Box`, `Button`, `Image` components **cannot** be placed in a baseline box
- `gravity` and `offsetBottom` are ignored in baseline layout

### Text

| Property | Type | Description |
|----------|------|-------------|
| `text` | String | **Required.** Content text |
| `size` | String | `xxs`/`xs`/`sm`/`md`/`lg`/`xl`/`xxl`/`3xl`/`4xl`/`5xl` or pixel |
| `weight` | String | `regular` / `bold` |
| `color` | String | Hex color (e.g., `#888888`) |
| `wrap` | Boolean | `true` to enable line wrapping (default `false` — text truncated) |
| `maxLines` | Number | Max lines when `wrap: true` |
| `decoration` | String | `none`/`underline`/`line-through` |
| `align` | String | `start`/`center`/`end` |
| `gravity` | String | `top`/`center`/`bottom` |
| `adjustMode` | String | `shrink-to-fit`: Auto-shrink text size to fit container width |
| `scaling` | Boolean | `true` to auto-scale text to fit (LINE 13.16.0+) |
| `contents` | Array | Array of `Span` components for inline rich text |
| `action` | Object | Action on tap |

### Image

| Property | Type | Description |
|----------|------|-------------|
| `url` | String | **Required.** HTTPS, JPEG/PNG, max 10MB, max 2000 chars |
| `size` | String | `xxs`~`5xl` or `full`. Also pixel or percentage |
| `aspectRatio` | String | Width:height ratio (e.g., `1:1`, `20:13`, `4:3`). Range 1:3 to 3:1 |
| `aspectMode` | String | `cover` (crop to fill) / `fit` (show entire image) |
| `animated` | Boolean | `true` for APNG animated images. **Max 3 per message, max 300KB each** |
| `action` | Object | Action on tap |

### Button

| Property | Type | Description |
|----------|------|-------------|
| `action` | Object | **Required.** Action object. `label` is required (max 40 chars in Flex) |
| `style` | String | `primary` (filled) / `secondary` (outlined) / `link` (text only) |
| `color` | String | Hex color for primary/secondary background |
| `height` | String | `sm` / `md` |
| `gravity` | String | `top`/`center`/`bottom` |
| `adjustMode` | String | `shrink-to-fit`: Auto-shrink label text |

### Icon

Small decorative image. Only usable inside **horizontal** or **baseline** Box.

| Property | Type | Description |
|----------|------|-------------|
| `url` | String | **Required.** HTTPS, PNG/JPEG, max 240px, max 1MB |
| `size` | String | `xxs`~`5xl` |
| `aspectRatio` | String | Width:height ratio. Range 1:3 to 3:1 |

### Span

Inline styled text segment. Only usable inside `Text` component's `contents` array.

| Property | Type | Description |
|----------|------|-------------|
| `text` | String | **Required.** Content text |
| `size` | String | Same as Text |
| `weight` | String | `regular` / `bold` |
| `color` | String | Hex color |
| `decoration` | String | `none`/`underline`/`line-through` |

### Separator

Horizontal line divider between components.

| Property | Type | Description |
|----------|------|-------------|
| `margin` | String | Margin before separator |
| `color` | String | Hex color |

### Filler

**Deprecated.** Use `margin`, `spacing`, and `padding` instead. Filler was a flexible spacer but is no longer recommended.

## Video in Flex

Video component can **only** be placed in the **hero block** of a Bubble.

### Constraints

- Bubble size must be `kilo`, `mega`, or `giga`
- **Not supported in Carousel** — a Carousel bubble with video will not render the video
- **Flex Message Simulator cannot preview video** — test on actual device
- **Desktop (macOS/Windows) does not support autoplay**
- Autoplay on mobile depends on user's LINE settings (Wi-Fi / mobile data autoplay toggles)

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `url` | String | **Required.** HTTPS video URL (MP4, max 200MB) |
| `previewUrl` | String | **Required.** HTTPS preview image URL (JPEG/PNG, max 1MB) |
| `altContent` | Object | **Required.** Fallback content (typically Image) for clients that don't support video |
| `aspectRatio` | String | Width:height ratio (e.g., `20:13`). Keep consistent with `previewUrl` and `altContent` |
| `action` | Object | URI action button. Label displayed in **3 places**: on the video before play, during playback, and after playback ends |

### Example

```json
{
  "type": "bubble",
  "size": "mega",
  "hero": {
    "type": "video",
    "url": "https://example.com/video.mp4",
    "previewUrl": "https://example.com/preview.jpg",
    "altContent": {
      "type": "image",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "url": "https://example.com/fallback.jpg"
    },
    "aspectRatio": "20:13",
    "action": {
      "type": "uri",
      "label": "Watch",
      "uri": "https://example.com/video-page"
    }
  }
}
```

## Layout System

Flex Message uses a **CSS Flexbox** model. Key behaviors:

### Flex property defaults

| Layout | Default `flex` | Behavior |
|--------|---------------|----------|
| `horizontal` | **1** | Children share space equally by default |
| `vertical` | **0** | Children take natural size by default |

Set `flex: 0` on a horizontal child to use its natural width. Set `flex: 1` on a vertical child to fill remaining space.

### justifyContent caveat

`justifyContent` only takes effect when **all children have `flex: 0`**. If any child has `flex > 0`, it absorbs available space and `justifyContent` has no visible effect.

### margin overrides spacing

When a child sets `margin`, it **overrides** the parent's `spacing` for that child. Other children without explicit `margin` still use the parent's `spacing`.

### Absolute positioning

Components with `position: absolute` are removed from the normal flow. They are positioned relative to their parent using `offsetTop`/`offsetBottom`/`offsetStart`/`offsetEnd`.

**Rendering order:** Components later in the `contents` array render **on top** of earlier ones. Use this for overlay effects (e.g., text over image).

### Padding units

- Keywords: `none`/`xs`/`sm`/`md`/`lg`/`xl`/`xxl`
- Pixel: `12px`
- Percentage: `5%` (relative to container width)

## Bubble Styles

Per-block style customization via `styles` property on the Bubble:

```json
{
  "type": "bubble",
  "styles": {
    "header": {"backgroundColor": "#ff6b6b"},
    "hero": {"separator": true, "separatorColor": "#cccccc"},
    "body": {"backgroundColor": "#f8f8f8"},
    "footer": {"separator": true}
  }
}
```

| Style property | Description |
|----------------|-------------|
| `backgroundColor` | Hex color |
| `separator` | `true` to show separator line above this block |
| `separatorColor` | Hex color for separator |

## Common Patterns

### Product list (nested horizontal box)
```json
{
  "type": "box",
  "layout": "horizontal",
  "spacing": "md",
  "contents": [
    {"type": "image", "url": "...", "size": "xs", "aspectMode": "cover", "flex": 1},
    {
      "type": "box", "layout": "vertical", "flex": 4,
      "contents": [
        {"type": "text", "text": "Product Name", "size": "sm", "weight": "bold"},
        {"type": "text", "text": "$15.00", "size": "xs", "color": "#888888"}
      ]
    }
  ]
}
```

### Text overlay on image (absolute positioning)
```json
{
  "type": "box",
  "layout": "vertical",
  "contents": [
    {"type": "image", "url": "...", "size": "full", "aspectRatio": "2:1", "aspectMode": "cover"},
    {
      "type": "box", "layout": "vertical",
      "position": "absolute", "offsetBottom": "0px", "offsetStart": "0px", "offsetEnd": "0px",
      "paddingAll": "12px",
      "background": {"type": "linearGradient", "angle": "0deg", "startColor": "#00000099", "endColor": "#00000000"},
      "contents": [
        {"type": "text", "text": "Title", "color": "#ffffff", "weight": "bold"}
      ]
    }
  ]
}
```

## Version Compatibility

| Feature | Minimum LINE version |
|---------|---------------------|
| Flex Message (basic) | LINE 6.7.0+ |
| `deca` / `hecto` bubble sizes | LINE 13.17.0+ |
| `adjustMode: shrink-to-fit` | LINE 10.13.0+ |
| `scaling` on Text | LINE 13.16.0+ |
| `position: absolute` | LINE 10.13.0+ |
| `linearGradient` background | LINE 10.13.0+ |

Older clients display `altText` instead. Ensure `altText` is descriptive and meaningful.
