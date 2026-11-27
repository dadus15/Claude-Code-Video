# Prompt: launch film Turismo Forged C26 × Mercedes-Benz S 560 (W222), TikTok / YouTube Shorts

Wersja promptu „$1M launch film” dostosowana do naszego projektu. Animacja zaczyna się dopiero po ujęciu z prowadnicy W222 v2.

```
ROLE
You are a senior motion designer, 3D artist and creative technologist. Build a premium, "$1M launch film" quality
vertical product film for a real forged-wheel brand: real 3D objects, frosted-glass UI, bouncy interactions,
rendered in code and in Blender, composited with REAL project photos.

BRAND / PRODUCT (fixed, do not invent)
- Brand: Turismo Wheels (client's own brand). Use ONLY the supplied logo files brand/turismo_logo_navy.svg and
  brand/turismo_logo_white.svg (navy #0A1B2B, red accent #C7222A). Never redraw or recolour it beyond those two inks.
- Product: Turismo Forged C26, 22 × 10.5J, 40 straight spokes in a deep concave dish, 5 bolts in teardrop pockets,
  centre cap with the Turismo emblem, finish BRUSHED SILVER (radial grain). True 3D geometry = the client's CAD
  (Turismo_C26_22x10.5j.obj, normalised scene: scratch c26/c26_m.blend). Never invent other finishes, sizes, prices
  or performance claims.
- Car: Mercedes-Benz S 560 4MATIC L (W222 facelift, obsidian black). The car appears ONLY in the 12 real project
  photos (turismo-wheels.com/en/projects/mercedes-benz-s-w222-s560-2/, files C26_01..C26_12.jpg) and in scene 0.
  Never re-create the Mercedes star, grille or any Mercedes logo in 3D or UI; never alter, repaint or AI-extend the
  real photos (crop, scale, blur, grade only).
- Tagline: UNLOCK YOUR STYLE (STYLE in red). Contact: Daniel Chmielewski · +48 501 404 861 ·
  daniel.chmielewski@turismo-wheels.com.
- Copy: Polish headline + small English subtitle under it (house style of the INVENTA reel). Invent all other UI
  copy yourself; never copy text from the references.
- Season: winter. Snow particles in the finale; the client's 3D Santa hat (edit/w222/santa_hat.py, Cycles, alpha)
  lands on the Turismo "T" mark in the last scene.

FORMAT
- 9:16 vertical for TikTok and YouTube Shorts. Master 2160x3840, delivery copy 1080x1920.
- 24 fps for the WHOLE film (scene 0 is 24 fps; never resample it to 30 fps: duplicated frames stutter and frame
  interpolation warps the 40 spokes).
- Length ~32 s: scene 0 = 12.96 s (fixed) + four animated scenes ~19 s.
- H.264 MP4, no voice-over, no baked music (the music is a TikTok trend added in-app). Write a cue list:
  drop 1 = 5.58 s (car pulls away), drop 2 = 12.96 s (first animated frame), beat grid 120 BPM after that.
- Safe zones (at 1080x1920, double them for 4K): nothing important in the top 150 px, the bottom 480 px
  (caption + buttons) or the right 140 px (TikTok/Shorts action rail).

SCENE 0 (FIXED, DO NOT EDIT)
renders/w222_c26_guide_v2_720x1280.mp4 (later: the Seedance re-render of it, same timing): the rig camera on the
front-left corner of the S 560, reverse on full left lock, stop, steer right until the C26 face looks into the
lens, pull away. Play all 311 frames untouched. The animation starts on frame 312. Its last frame gives the exact
hub position and rim radius for the first match cut (edit/w222/rig_hub.json, per frame: x, y, rim_px).

REFERENCES (style only)
- The supplied "$1M launch film" references: glass UI, floating devices, fanned cards, huge background type.
- The client's INVENTA reel (WeTransfer, 44 s): dark charcoal with deep red radial glow and dust, red kicker
  "| LABEL", Lora serif headline with one red accent word + small EN subtitle, white product tiles popping in,
  2x2 tile grid, red counter badge (24 h -> 72 h), photo carousel with arrows/dots/progress line, RGB-split
  glitch and diagonal light-leak transitions, contact box with a red outline.

=== PHASE 1: ANALYZE (no code yet) ===
Write a short style bible that merges both reference sets with the C26 / S-Class material:
- palette (hex): obsidian black, charcoal #0B0B0D-#1A1A1E, Turismo navy #0A1B2B, Turismo red #C7222A, brushed
  silver, warm cream subtitle #E9D6A0, snow white; lighting: soft studio light, long softbox highlights along the
  spokes, cool rim light, red under-glow
- materials: brushed aluminium with radial anisotropy (the wheel), obsidian clear-coat paint (in photos only),
  frosted glass cards, matte titanium, glossy red ceramic (the logo square), velvet + fur (the Santa hat)
- camera language: tilted 3/4 hero of the wheel, floating objects, soft contact shadows, slow push/orbit
- typography: ONE grotesk for UI/display (Inter Display) + Lora serif only for the INVENTA-style headlines;
  tight tracking at display sizes
- composition: the wheel always anchored on the same screen point at every cut (match cuts), glass chips and pills
  around it, real photos as glass cards fanned in depth, huge marquee background type "C26" / "FORGED"
- for each reference: one line on what makes it feel expensive
Recurring logo mark: the Turismo "T" extruded in 3D (matte titanium + red ceramic square), NOT a new invented
mark. It appears small in scenes 1-3 and as the hero of scene 4.

=== STORY (adapt timings, keep the order) ===
S0  0.00-12.96  rig shot (fixed).
S1  12.96-18.2  "Czterdzieści szprych." HERO 3D. Match cut: the rig frame pushes into the hub, the real CAD C26
    (Blender Cycles, alpha) takes over at the same hub position and rim size, spins down on a heavy spring and
    turns to a 3/4 hero on a dark studio set with red under-glow; huge marquee "C26" behind; glass chips pop
    around it: "40 SPOKES", "22 × 10.5J", "BRUSHED SILVER", "FORGED". Touch: tap on "BRUSHED SILVER" -> ripple,
    a light sweep travels along the radial grain of every spoke (no recolour: only the real finish exists).
S2  18.2-23.4   "Na Mercedesie S 560." REAL PHOTOS. Transition: iris THROUGH THE 40-SPOKE FACE (the wheel
    flies at the camera, its spoke gaps are the alpha cut-out that reveals the next scene). Real photos _07, _08,
    _12, _05, _09 as frosted-glass cards fanned in depth, idle drift, contact shadows; counter "W222 · S 560 4MATIC L";
    touch: the front card is swiped away, the next one springs forward; a 2x2 tile grid pops as in the INVENTA reel.
S3  23.4-27.8   "Zapytaj o swój projekt." PHONE. Push into a 3D phone (titanium frame, frosted back glass with the
    Turismo mark): screen = invented "Turismo Projects" app showing the real photo _07, a finish chip and a
    button "Wyceń dla mojego auta / Get a quote". Touch: button squish + state morph -> a toast drops in on a
    bouncy spring ("Daniel Chmielewski · Turismo Wheels" / "Wiadomość wysłana"), icon pops a beat later, the
    phone does a haptic wiggle. Transition: the app-opening panel matches the dark finale background.
S4  27.8-32.0   FINALE (winter). The 3D Turismo T mark rises on a heavy spring, the Santa hat drops onto it
    (heavy spring, one soft settle, snow puff on landing), snow falls, red kicker "| TURISMO WHEELS · UNLOCK YOUR
    STYLE", big "Odezwij się!" / "Get in touch", glass contact card with a red outline (name, phone, e-mail),
    one light sweep, hold 1.5 s for the loop.

=== PHASE 2: STORYBOARD (stop for approval) ===
Render 5 key frames at full 2160x3840: the last frame of S0 with the first transition overlay, and one per scene
S1-S4 at the moment with the most on screen. Inspect every frame at full size, including detail crops (spoke edges,
text, glass edges, photo sharpness, hat fur), and fix before sending: clipping, blown highlights on the brushed face,
washed-out colour, overlapping text, objects too big or too small, anything inside the safe zones, stray template
text. Send the frames + a labelled contact sheet (one line per scene), then WAIT for my approval.
If the quality cannot be reached, name the external assets that would help (e.g. higher-resolution originals of the
project photos, a vector of the C26 centre-cap emblem, an HDRI of a studio).

=== PHASE 3: ANIMATE (only after approval) ===
Write a beat sheet with timings for every scene before coding. Nothing may simply slide in.
Motion language (time-based, deterministic):
- Springs, closed form: x(t) = 1 - e^(-z*w*t) * (cos(wd*t) + (z*w/wd) * sin(wd*t)).
  Heavy objects (wheel, phone, logo, hat): f 0.9-1.2 Hz, damping 0.55-0.8. UI pops (chips, pills, toasts):
  f 2.0-2.6 Hz, damping 0.38-0.5.
- Pop-in: scale 0.3-0.6 -> spring overshoot, opacity over 0.2 s, blur 10 px -> 0, small settling rotation.
- Text: split into words/characters, rise 0.4-0.6 em, fade + un-blur 8-22 px, ease-out-expo ~0.9 s,
  stagger 30-90 ms; exits reverse with blur. Polish diacritics must survive the split.
- One simulated touch per scene (circle, squish, ripple ring, visible UI response).
- Live UI: counter 0 -> 40 spokes, rim size 18" -> 22", progress lines with a moving shine, carousel dots.
- Never dead: idle drift (sum of slow sines), slow camera push/orbit, marquee type, breathing red glow, animated
  film grain (offset every frame), slow snowfall in S4.
- Real motion blur on 3D: 180-degree shutter, 1 sample when slow, 6-7 when the wheel spins fast; the spinning
  C26 must keep 40 readable spokes when it settles (no wagon-wheel strobing: pick spin speeds that are not
  multiples of 9 deg per frame).
- Scenes 4.2-5.4 s. Transitions are designed match cuts only: hub push from S0 into the 3D wheel; iris through
  the spoke gaps; push into the phone screen; app panel -> finale background. Optional accents from the INVENTA
  reel: RGB-split glitch (max 3 frames) and one diagonal light leak per scene.

=== TECHNICAL APPROACH ===
- Wheel: render from the CAD in Blender 5 (Cycles, the existing brushed-silver anisotropic material, studio
  softboxes key/strip/rim + red under-light), RGBA EXR/PNG sequences per scene with the exact camera and spin
  curves from the beat sheet; motion blur from Cycles or from averaged sub-frames. Decimated copy (~150k tris)
  only if a WebGL view is needed.
- Glass UI, text, chips, phone screens: HTML/CSS pages with window.SCENE.frame(t), rendered in headless Chromium
  via Playwright at 1080x1920 CSS with deviceScaleFactor 2 (= 2160x3840), served from a local HTTP server.
- Phone and T mark: WebGL2 triangle rasterizer or Blender (rounded-slab phone: titanium frame, curved black glass,
  camera plateau; T mark extruded from the SVG with a bevel). Screens = HTML screenshots uploaded as textures.
- Real photos: decoded once, placed as textured cards (perspective warp), never upscaled beyond 2x of their native
  pixels in any card; full-screen use only with a slow push.
- Contact shadows: blurred radial gradients scaled by object height.
- Composite all layers in numpy/OpenCV, pipe raw frames to ffmpeg once (libx264, -preset medium, -crf 15,
  yuv420p, +faststart, 24 fps), write to a temp name, rename on success.

=== QUALITY CONTROL ===
- Before full render: every scene at 1/4 resolution every ~0.4 s -> contact sheets -> check timing, framing,
  transitions, safe zones. Fix and re-check.
- Full-resolution crops of: spoke edges and grain, the cap emblem, glass edges, every text block, photo cards,
  the hat fur, the logo edges.
- Verify the final with ffprobe; sample frames around every transition; no single-frame flashes, no black frames,
  even cadence (no repeated frames on moving shots), frame 312 must be the first animated frame.

=== DELIVERABLES ===
1. Phase 2: 5 storyboard frames 2160x3840 + labelled contact sheet, then wait for approval.
2. Phase 3: final 2160x3840 24 fps MP4, a 1080x1920 delivery copy for TikTok/Shorts, the cue list for the music,
   and a short beat-by-beat summary of motion and transitions.
Keep messages short: show results, not process. State up front roughly how long rendering will take.
```
