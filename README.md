# Graphite & Bronze — photo slider

A cinematic slideshow of the graphite Ferrari on bronze Turismo Forged wheels.
Plain HTML/CSS/JavaScript: no build step, no dependencies, no network calls.

## Open it

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

Any static server works (`npx http-server`, etc.). Opening `index.html` directly
from disk also works, but then only the exact names `photos/90241.jpg`–`90248.jpg`
are found. A server that lists directories lets the slider match prefixed names too.

## Photos

Put `90241.jpg`–`90248.jpg` in `photos/`. Names are matched by suffix, so
`01-90248.jpg` works. The folder currently holds 90241–90245; 90246, 90247 and 90248
still need adding. Until they're there, the slider skips them, lists them under
the stage, and offers **Import photos**. You can pick files or drag them onto
the page. They're read locally as object URLs and never uploaded.

Slide order, captions, alt text and Ken Burns keyframes are in the `SLIDES` array
at the top of `app.js`.

## Controls

| Action | Input |
| --- | --- |
| Previous / next | ← / →, the chevron buttons, swipe on touch |
| Play / pause | Space, centre button |
| Jump to a photo | Thumbnail strip (toggle with the thumbnails button) |
| Full photo (no crop, no motion) | Full photo button |
| Full screen | Full screen button (hidden where unsupported) |

With `prefers-reduced-motion: reduce`, pan/zoom is disabled and autoplay starts
paused. Playback pauses while the tab is hidden.
