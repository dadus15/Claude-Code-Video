# Porsche hook

Cinematic hook cut from the clips in `footage/`, 1920x1080, 24 fps.

- `renders/porsche-hook_v2.mp4` — **current**, 34.96 s, uses all nine clips
- `renders/porsche-hook_v1.mp4` — first cut, 25.7 s, first five clips

## v2 cut

| Time | Shot | Treatment |
|---|---|---|
| 0.00 | Dark headlight, wide (studio) | — |
| 2.17 | START button | 122% punch-in on the press + click |
| 3.04 | Headlight ignites (3.25) | bass hit on ignition |
| 5.54 | Garage door rises | 110% slow creep |
| 8.25 | Rolls out of the rain garage | — |
| 11.25 | Tunnel run | **Animation 1:** tachometer sweep, count-up to 7,500 RPM |
| 14.58 | Low tunnel wheel | — |
| 16.75 | Taillight in the rain | — |
| 17.83 | Caliper → caliper macro (19.29) | — |
| 20.13 | Wheel pull-out | **Animation 2:** HUD lock-on tracking the hub + glass callout |
| 23.75 | Mountain-road approach | riser builds |
| 28.33 | Clifftop sunset | **Animation 3:** "BUILT TO TURN HEADS" lands with a bass hit (30.90); 108% creep; fade out |

Audio: the clips' own sound (short crossfades at every cut) plus four sounds from the bundled
HyperFrames/Pixabay library (`composition/assets/sfx/`). About -16 LUFS integrated.

`hf_..._bdb38021` was uploaded twice; it's `footage/headlight-rain.mp4` (identical file), so it's stored once.

## Rebuild

```bash
python3 build.py all                    # cut + camera moves -> composition/assets/base.mp4, audio -> build/mix.wav
cd composition && npx hyperframes@0.8.141 render . --fps 24 --quality high -o ../build/overlay.mp4
cd .. && python3 build.py mux porsche-hook_v3.mp4
```

The cut list, zooms and sound cues are at the top of `build.py`; the animations and their copy are in `composition/index.html`.
