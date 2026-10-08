# Porsche hook (v1)

25.7 s cinematic hook cut from the five clips in `footage/`. Render: `renders/porsche-hook_v1.mp4` (1920x1080, 24 fps).

| Time | Shot | Treatment |
|---|---|---|
| 0.00 | Dark headlight in the rain | — |
| 2.13 | START button | 122% punch-in on the press + click |
| 3.00 | Headlight ignites (3.21) | bass hit on ignition |
| 5.50 | Garage door rises | 110% slow creep |
| 8.21 | Tunnel run | **Animation 1:** tachometer sweep, count-up to 7,500 RPM |
| 11.54 | Spoiler rising | — |
| 13.58 | Brake caliper | — |
| 15.04 | Wheel pull-out | **Animation 2:** HUD lock-on tracking the hub + glass callout; riser starts |
| 18.67 | Mountain-road hero | **Animation 3:** kinetic headline "BUILT TO TURN HEADS" on the bass hit (20.45); 108% creep; fade out |

Audio: the clips' own sound (short crossfades at every cut) plus four sounds from the bundled
HyperFrames/Pixabay library (`composition/assets/sfx/`). Loudness-normalised toward -14 LUFS.

## Rebuild

```bash
python3 build.py all                    # cut + camera moves -> composition/assets/base.mp4, audio -> build/mix.wav
cd composition && npx hyperframes@0.8.141 render . --fps 24 --quality high -o ../build/overlay.mp4
cd .. && python3 build.py mux porsche-hook_v2.mp4
```

The cut list, zooms and sound cues are at the top of `build.py`; the animations and their copy are in `composition/index.html`.
