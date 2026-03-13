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
- Icons must be clear at 78x78 px
- Avoid excessive detail — simplicity first
- Ensure sufficient contrast against background

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

## Common Review Rejection Reasons

| Issue | Solution |
|-------|----------|
| Background image too busy, affecting readability | Reduce background saturation or add semi-transparent overlay |
| Insufficient text contrast | Test WCAG contrast ratio, achieve AA minimum |
| Icons not clear | Simplify icon design, ensure legibility at 78px |
| Normal/selected states indistinguishable | Increase visual difference between the two states |
| Contains copyrighted material | Ensure all elements are original |
| Color settings errors | Test on both iOS and Android |
| Text only, no illustrations | Add visual elements |
| Duplicate of existing marketplace theme | Ensure differentiation (not just color swaps) |

---

## Tips for Passing Review

1. **Test on real devices** — Test all screens on both iOS and Android
2. **Various conversation lengths** — Test display with 1-line and 20-line conversations
3. **Icon check** — Confirm all icons are clear with distinguishable states
4. **Contrast test** — Conversations must be readable against both light and dark backgrounds
5. **Use official Photoshop template** — Official PSD template ensures correct dimensions
6. **Cross-platform preview** — Creators Market dashboard allows iOS / Android preview in different languages
