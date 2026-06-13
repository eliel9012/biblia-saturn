# Saturn Bible Bitmap Legibility Prompt

Use this prompt when improving a low-legibility Bible bitmap for the Sega Saturn.

```text
Improve this Sega Saturn Bible screen bitmap for maximum readability on a real 4:3 CRT display and Saturn emulator capture.

Target format: 320x240 pixels, Sega Saturn era, low-resolution console UI, final output must survive conversion to TGA and display through VDP backgrounds.

Primary goal: make the Bible text readable first. Preserve the original composition and sacred/Bible theme, but simplify all decorative detail behind text.

Visual requirements:
- high contrast text area, dark matte reading panel, light cream/white text
- large pixel-friendly typography, no tiny serifs, no thin strokes
- clear separation between foreground text and background art
- keep important content inside a safe area: at least 12 px from left/right and 10 px from top/bottom
- use restrained warm parchment/gold accents only outside the reading area
- avoid busy texture, glow, blur, heavy gradients, ornate borders near text, and photographic detail behind text
- preserve 4:3 layout and 320x240 readability; do not upscale the final composition style beyond what Saturn-era assets can represent

Negative prompt:
tiny unreadable letters, thin font, modern vector UI, smartphone UI, excessive bloom, noisy parchment, detailed background behind text, low contrast, washed out colors, oversharpened halos, text touching screen edges, cropped text, 16:9 layout

Deliverable:
one clean 320x240 image, flat enough for paletted/TGA conversion, with a strong dark reading area and readable Bible text.
```

Post-process checklist before putting it in the ROM:

- Downsample or export at exactly 320x240.
- Check at 1x size, not only zoomed.
- Keep text inside the safe area.
- Convert to TGA and inspect again after conversion.
- Prefer fewer larger words over dense paragraphs baked into art; runtime text should remain drawn by the Saturn font layer when possible.
