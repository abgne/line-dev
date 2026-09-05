# LINE Theme Design In-Depth Guide

For basic technical specs (sizes, color settings, file structure), see the "Themes" section of [sticker-specs.md](sticker-specs.md).
This document focuses on theme **design best practices and review considerations**.

---

## Background Image Design

### Tile Mode
- Design seamless tile patterns
- Verify pattern repeats correctly across different device aspect ratios
- Moderate pattern density — too dense makes conversations hard to read

### Stretch Mode
- Ensure important elements stay within the safe zone
- Account for cropping at different screen ratios
- Avoid placing key elements near edges

### Universal Principles
- **Background must not interfere with conversation readability** — this is the most common rejection reason
- Light backgrounds with dark text, or dark backgrounds with light text
- Test display with both long and short conversations

---

## Icon Design

### Normal vs Selected States
- Must be **clearly distinguishable** (not just a subtle opacity change)
- Common approaches: line/fill toggle, color inversion, background addition
- All icons maintain unified style (line/fill/flat/skeuomorphic — pick one)

### Size Legibility
- Icons must read on both canvases: 128x150 px (standard set) and 80x56 px (iOS 26 set). The 80x56 landscape canvas is the real test — design for it first
- Avoid excessive detail — simplicity first
- Ensure sufficient contrast against background

---

## iOS 26 Menu Icons (Liquid Glass)

Status as of 2026-09-05. This is the one theme rule that changed in 2026; re-check the detail guideline before quoting it.

### What changed
- iOS 26 redraws the LINE tab bar in Apple's Liquid Glass style. The menu button canvas went from 128x150 portrait to **80x56 landscape**, and the notification badge from 33x33 (49px from top, 21px from right) to **32x32 at the top-right of the image area**
- Every one of the 9 buttons needs a second OFF/ON pair named `i_NN_g.png` — 18 extra files, 36 menu images in total (filenames in [sticker-specs.md](sticker-specs.md))
- New submissions must include the iOS 26 set; the standard set still serves iOS 25 and Android

### Timeline
- 2026-06: LINE notified creators that iOS 26 icons would be required
- Detail guideline: iOS 26 images "must be provided when submitting for review" and are "applied from August 2026 onward"
- Early 2026-08: buyers of un-updated themes saw LINE's default icons on iOS 26; Japanese tech press covered it
- 2026-08-20 official notice (updated 08-31): LINE would auto-convert un-updated themes in early September 2026; purchasers may request refunds (coins/credits) until 2027-03-31
- For a creator with a back catalogue: every theme still on sale either gets a hand-drawn `_g` set or LINE's auto-converted one. Check what the conversion did to each theme before deciding it is fine

### Design notes for the 80x56 set
- Redraw, don't downscale: a portrait icon squeezed into a landscape box loses its silhouette, and review 1.2 (difficult to recognize) applies
- Keep the same motif as the standard set — review 1.8 rejects the same icon looking significantly different across OS
- Official note: check the icon against a transparent background, since in some situations the menu is drawn over one — expect thin outlines and low-contrast fills to vanish
- Keep the icon balanced on all four sides (the guideline gives no pixel margin for this set, unlike the ~10px of the standard set)
- One colour plus one silhouette per icon is the safe budget at this size; interior detail will not survive

### Creator report — re-registering a back catalogue
Anie (230 themes, about 400 listings once overseas duplicates are counted; note.com, 2026-07-11): each theme needed 18 new files; the bulk ZIP upload the guideline describes did not appear in the dashboard, so files were uploaded one at a time; the 80x56 canvas is small and landscape, yet the review expects the same icon as the portrait original. Budget the update per theme, not per catalogue — a large catalogue is weeks of work.

---

## Chat Bubble Design

- Self and other chat bubbles must have **clearly different colors**
- Bubble color must not clash with text color
- Consider dark/light mode adaptability
- Common color schemes:
  - Self: Brand accent color (e.g., light green #DCF8C6)
  - Other: Neutral color (white or light grey)

---

## Color Planning Strategy

### Recommended Process
1. Select 1 primary color (brand color / character representative color)
2. Select 1 secondary color (complementary)
3. Select a neutral base color (background)
4. Ensure all text achieves WCAG AA contrast ratio against base color

### Color Tips
- **Brand color**: Establish unified color identity
- **Seasonal variations**: Same character in different color themes (spring pink, summer blue, autumn orange, winter white)
- **Avoid pure black backgrounds**: Can cause OLED screen burn-in fatigue

---

## Character Theme Design

### Extending from Sticker Characters to Themes
- Character elements should be **moderate** — don't overshadow functionality
- Use small-scale character patterns for backgrounds, not enlarged to fill
- Icons can incorporate character features (ear shapes, representative colors)
- Chat bubbles can include subtle character element decorations

### Brand Visual System
- Stickers → Emoji → Themes using consistent colors and style
- Complete brand identity increases repurchase rates
- Themes are an important product for building brand value

---

## Production Workflow (creator reports)

Three first-hand write-ups from Japanese theme creators; tool choice differs, the habits repeat.

- **Decide the color skin first, then draw** (みるよっこ / ふわもふアート, CLIP STUDIO + Wacom, blog 2025-07): pick the chat-bubble and text colours before any icon, keep one folder per image class (menu / password / profile / background), keep the source files, and upload one image at a time while checking the preview
- **iPhone-only is possible** (Riiiiiii, note.com 2022, updated 2024): draw in ibisPaint, rename and ZIP with the Documents app. Written before iOS 26 — the file count in that article is out of date, use the workflow only
- **Reuse a component library** (ぐらむ, Illustrator, note.com): 50 themes were possible because icons and backgrounds were assembled from a stock of own parts. The same reuse is what review 1.7 punishes when it turns into colour-only variants, so vary the icon set, not just the palette

---

## Common Review Rejection Reasons

| Issue | Solution |
|-------|----------|
| Background image too busy, affecting readability | Reduce background saturation or add semi-transparent overlay |
| Insufficient text contrast | Test WCAG contrast ratio, achieve AA minimum |
| Icons not clear (review 1.2) | Simplify icon design, ensure legibility at 80x56 px (iOS 26 set) |
| Normal/selected states indistinguishable | Increase visual difference between the two states |
| Contains copyrighted material | Ensure all elements are original |
| Color settings errors | Test on both iOS and Android |
| Icons lack a unified style across the 9 buttons (review 1.3) | Pick one language — line, fill, flat — and redraw the outliers |
| Text only, no illustrations (review 1.3 / 1.4) | Add visual elements |
| Duplicate of existing marketplace theme (review 1.7) | Ensure differentiation — 1.7 explicitly counts "same icons, different color scheme" as a duplicate, and a creator reports colour-only variants of one design being rejected |
| Same icon differs across iOS / Android / iOS 26 sets (review 1.8) | Keep one motif; only the canvas and badge position change |

---

## Tips for Passing Review

1. **Test on real devices** — Test all screens on both iOS and Android
2. **Various conversation lengths** — Test display with 1-line and 20-line conversations
3. **Icon check** — Confirm all icons are clear with distinguishable states
4. **Contrast test** — Conversations must be readable against both light and dark backgrounds
5. **Use official Photoshop template** — Official PSD template ensures correct dimensions for all 62 files, including the iOS 26 `_g` artboards (Photoshop CC; not CS6)
6. **Cross-platform preview** — Creators Market dashboard allows iOS / Android preview in different languages
