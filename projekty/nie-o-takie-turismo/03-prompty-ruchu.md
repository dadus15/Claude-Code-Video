# Prompty ruchu (wideo) — składane z Cinedance Block Library

Status: 🟨 prompty gotowe, nic nie wyrenderowano.

Zasady składania:
- Kolejność bloków jak w Cinedance (część 4). **FACE i BODY Karimy usunięte** — w ich miejsce idzie `[HERO LOCK]` z `02-prompty-klatek.md`.
- MODEST, WIND, WATER, RAIN, LIVING-BACKGROUND pominięte, bo nie dotyczą tych ujęć.
- GAZE jest odwrócony względem domyślnej wersji: prowadzący **ma** patrzeć w obiektyw w wyznaczonych momentach. Poza nimi nie patrzy.
- Dźwięk: `generate_audio: false` we wszystkich klipach. Cały dźwięk powstaje w montażu (`05-VO-montaz-dzwiek.md`). Przy ujęciach z kwestią (A, B, C, H) podaj **swoje nagranie kwestii** jako `audio_references`, żeby model zsynchronizował usta.
- Grafiki i napisy nigdy nie trafiają do renderu. Dodajemy je jako osobne warstwy.

Czas każdego klipu jest renderowany z zapasem po obu stronach cięcia.

---

## GRADE-LOCK (wspólny dla A–H, wklej w każdy prompt)
```
GRADE-LOCK — identical in every shot: neutral-to-cool white balance, true blacks, clean whites, moderate contrast, natural saturation, fine grain. Exceptions that keep their force: the red practical/red accent light, the crystal emblem sparkle, the Gloss Silver highlights. No orange-teal, no purple, no bloom, no glow overlay, no lens-flare graphics.
```

## STOP-BASE (skrócony, wspólny)
```
No CG or game-engine look on people, no plastic or waxy skin, no beauty filter, no morphing face, no extra people, no second face, no extra hands, no extra fingers, no fused fingers, no text, no captions, no subtitles, no watermarks, no gibberish lettering, no slow motion, no speed ramp, no freeze frame, no style drift.
```

---

## A | 0:01.6–0:06 | render 5 s
Ustawienia: `seedance_2_0`, `mode: std`, `720p`, `9:16`, `duration: 5`, start = **KF-A0**, end = **KF-A9**, image_references: [1] @HERO, [2] KF-G1, [3] @GT. audio_references: nagranie „Chyba nie o takie Turismo nam chodzi”.
Bloki: GAZE, RESTRAINED, ACTING, CAM-LIVING-TRIPOD, ANATOMY, COUNT, NO-FREEZING, SOUND-SWITCH (w montażu).
```
SCENE: a gamer realises this is not the "Turismo" he meant — a deadpan beat in a dark black-red-white game room.
FORMAT: 5 s, one continuous shot, 9:16, no music, no text.
ONE PERSON ONLY: the man from @HERO. Image 2 supplies the room only; image 3 supplies the shirt print only.
MOST IMPORTANT: (1) the shot opens exactly on the start frame — tight on his thumb pressing pause — and ends exactly on the end frame — his right hand close to the lens, thumb pressed to middle finger, frozen an instant before the snap. (2) Exactly ONE finger snap is prepared and it is NOT completed in this shot. IF THE SNAP HAPPENS IN THIS SHOT — THE SHOT IS WRONG.
[HERO LOCK]
LAYOUT (near → far): controller and hands; him on the sofa, black T-shirt with the white chest logo of image 3; low black table; white shelves of racing-car models washed by one red vertical practical on the black wall.
TIMING: 0.0–0.3 s thumb presses pause. 0.3–1.2 s the camera eases back from the thumb to a medium shot (knees to head) and settles. 1.2 s his eyes leave the paused game (just above lens) and land in the lens. 1.3–3.2 s he says one short line to camera, dry and amused. 3.3 s he places the controller on the sofa cushion beside his right thigh. 3.6–5.0 s he raises his right hand toward the lens; the hand, not the camera, travels forward until it fills the central half of the frame, thumb pad pressed to middle fingertip, his face soft behind it.
ACTING: he is not annoyed, he is amused at himself. Motive: he wants a different "Turismo". Tactic: one sideways look to camera, a two-millimetre brow lift, a small exhale through the nose. Gaze in lens ONLY from 1.2 s to 3.5 s.
CAMERA: locked tripod with faint life after the initial ease-back; no zoom, no orbit.
OPTICS: 50 mm normal lens look, f/2.8, natural falloff.
LIGHT: soft neutral fill from the paused screen at the lens position; red rim from the practical at frame right; deep but readable shadows.
ANATOMY: two hands, five fingers each, correct thumb opposition, snap pose readable.
COUNT: one man, one controller, one sofa, one red practical.
NO-FREEZING: breathing, small weight shifts, the hand keeps micro-moving even in the last frame.
[GRADE-LOCK]
STOP-INVERSION: the snap is not completed; no second snap; no camera push-in onto the hand; no zoom; he does not keep looking at the lens after 3.5 s; no wide grin; no laugh; no controller left in his hands at the end; no purple or neon; no posters.
[STOP-BASE]
```

## B | 0:06–0:10.4 | render 5 s
Ustawienia: `seedance_2_0`, `std`, `720p`, `9:16`, `duration: 5`, start = **KF-B0**, end = **KF-C1**, refs: [1] @HERO, [2] KF-O1, [3] @GT. audio_references: „Coś mi nie pasuje”.
Bloki: ANATOMY, GRADE-LOCK, SOUND-SWITCH, GAZE, RESTRAINED, COUNT, NO-FREEZING.
```
SCENE: the snap has teleported him from the game room to the wheel office — the snap completes on the very first frames.
FORMAT: 5 s, one continuous shot, 9:16, no music, no text.
ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) frame 1 matches the start frame exactly — the same hand, same size, same screen position — and the snap is completed within the first 4 frames: middle finger flicks down onto the palm. (2) The shot ends exactly on the end frame: seated, left hand pinching the shirt, right hand raised in a NEW snap pose, eyes on the shirt. Exactly ONE snap happens in this shot. IF A SECOND SNAP HAPPENS — THE SHOT IS WRONG.
[HERO LOCK]
LAYOUT: black slatted wall with six dark wheels; low black sofa; low black table with a closed laptop left and an empty roller stand right.
TIMING: 0.00–0.16 s snap completes, hand drops away. 0.2–1.4 s the camera eases back revealing him standing just in front of the sofa. 1.4–2.2 s he sits down and settles into the cushion (the change from standing to seated happens fully in frame, natural weight). 2.2–2.6 s he glances down at his own T-shirt with the white chest logo. 2.6–3.6 s he looks to camera and says one short line, puzzled. 3.6–5.0 s his left hand pinches a small fold of the shirt 8 cm below his left chest; his right hand rises to shoulder height into a snap pose; his eyes go back to the shirt.
ACTING: something is off and he knows exactly what. Tactic: the look down at the shirt comes before the line; the line is almost to himself.
CAMERA: smooth short ease-back then locked with faint life; same height as the end frame.
LIGHT: neutral 4300 K soft key from frame left, thin red accent line on the right edge of the slat wall.
COUNT: one man, one sofa, one laptop, one empty stand, six wall wheels.
NO-FREEZING.
[GRADE-LOCK]
STOP-INVERSION: no red game-room light in the office; no second snap; the hand does not change size at the start; no shirt change in this shot; the white chest logo stays; he does not stand up again; no wheel on the stand.
[STOP-BASE]
```

## C | 0:10.4–0:13 | render 4 s
Ustawienia: `seedance_2_5`, `mode: omni_reference`, **`draft: true`** (480p, test), `9:16`, `duration: 4`, start = **KF-C2**, refs: [1] @HERO, [2] @TWdetail, [3] @TWfront. audio_references: „Od razu lepiej”. Finał = finalize zaakceptowanego draftu.
Bloki: COUNT, ANATOMY, RESTRAINED, CAM-LIVING-TRIPOD, GAZE, NO-FREEZING.
```
SCENE: right after the second snap — he is already wearing the brand shirt; the camera has not moved at all.
FORMAT: 4 s, one shot, 9:16, locked camera, no music, no text.
ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) frame 1 is the start frame exactly; the camera does not move by a single pixel for the first 0.6 s. (2) The crystal emblem from image 2 stays on the wearer's LEFT chest the whole time, same size, following the fabric. IF THE EMBLEM MOVES, CHANGES SIDE, GROWS, MULTIPLIES OR A WHITE CHEST LOGO REAPPEARS — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–0.15 s the snap's follow-through: his right middle finger lands on the palm, hand relaxes. 0.4 s his left hand releases the fold; the cotton settles flat in 0.3 s. 0.8 s his eyes come up from the shirt into the lens. 1.1–2.1 s one short line with a half smile, satisfied. 2.1–4.0 s small nod, hands rest on his thighs, he keeps eye contact.
ACTING: quiet satisfaction, not a show; the smile lives in the eyes and one corner of the mouth.
CAMERA: locked tripod, faint organic drift of 2 px at most, after 0.6 s.
COUNT: one emblem, on the left chest; no print anywhere else on the front.
NO-FREEZING.
[GRADE-LOCK]
STOP-INVERSION: no camera move at the start; no second snap; no emblem on the right chest; no large logo; no back print visible; no change of neckline; no change of sofa position; no jump in his posture at frame 1.
[STOP-BASE]
```

## D | 0:13–0:17 | render 4 s
Ustawienia: `seedance_2_0`, `std`, `720p`, `9:16`, `duration: 4`, start = **KF-D0** (= KF-O3), end = **KF-D9**, refs: [1] @HERO, [2] @TWback, [3] KF-O1.
Bloki: CAM-OVER-SHOULDER (wersja statyczna), GAZE, INTEGRATION, NO-FREEZING.
```
SCENE: over his shoulder as he opens the laptop — the crystal TURISMO wheel on his back is seen for one beat, then focus moves to the screen.
FORMAT: 4 s, one shot, 9:16, no music, no text.
ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) the back print from image 2 (word TURISMO above a crystal wheel outline) is readable for the first second, then goes soft. (2) The laptop screen stays a flat even light-grey surface with all four corners visible and unobstructed in every frame — it will be replaced in post. IF A HAND, A REFLECTION OR ANY IMAGE COVERS A SCREEN CORNER — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–1.0 s he leans forward from the sofa edge, back three-quarters to camera, opens the lid from 45° to 110°; crystals catch the key light. 1.0–1.8 s focus racks from his back to the screen with a real transitional beat where nothing is sharp. 1.8–4.0 s his right hand rests near the trackpad, small finger movements of scrolling; camera holds the final position.
CAMERA: locked high over-the-shoulder position, no drift after 1.8 s (tracking plate).
LIGHT: neutral key from frame left; the screen emits soft cool light onto his hands.
NO-FREEZING.
[GRADE-LOCK]
STOP-INVERSION: the screen shows nothing readable; no website, no wheel image on the screen; no camera move after 1.8 s; the back print is not mirrored; no logo on the laptop.
[STOP-BASE]
```

## E | 0:19–0:23 | render 4 s
Ustawienia: `seedance_2_5`, `omni_reference`, **`draft: true`**, `9:16`, `duration: 4`, start = **K1**, end = **K3**, image_references (kolejność = numery w prompcie): [1] K2, [2] @WHEEL, [3] @HERO, [4] @STAND, [5] K4. Bez audio.
Bloki: SCALE, INTEGRATION, ANATOMY, COUNT, FAIL, STOP-INVERSION.
```
SCENE: he pulls the wheel he picked out of the laptop screen — the catalogue picture becomes a real full-size wheel in his hands.
FORMAT: 4 s, one continuous-looking shot, 9:16, locked product camera, no music, no text.
ONE PERSON ONLY, from @HERO; every hand is his.
MOST IMPORTANT: (1) ONE wheel, ALWAYS the exact design of image 2 — same spoke count, spoke shape, integrated outer aero-ring, centre cap, Gloss Silver — on the screen and in his hands. (2) Depth order during the pull, near to far: his thumb → the wheel's front lip → his other fingertips → the laptop screen. As the wheel leaves, its upper lip crosses IN FRONT of the laptop's top bezel while the bezel stays visible behind it. IF THE BEZEL IS COVERED BY THE HAND, IF THE WHEEL PASSES BEHIND THE BEZEL, OR IF THE SPOKE COUNT CHANGES — THE SHOT IS WRONG.
SCALE: on the screen the wheel is one-third of the screen width. Out of the screen it grows to its full 54 cm only while crossing the bezel, between 0.6 s and 2.0 s, then its size is LOCKED: as tall as his torso from collarbone to belt, wider than his shoulders, his spread hand covers one-third of its diameter. No size drift after 2.0 s in either direction.
[HERO LOCK]
LAYOUT (near → far): roller stand on the right of the tabletop; laptop on the left, screen turned 25° away from camera; him on the sofa edge behind, leaning in; dark slatted wall with dark wheels.
TIMING: 0.0–0.4 s his right hand arrives; 0.4 s thumb pad lands on the wheel picture's outer lip at 12 o'clock (as image 1), fingertips slip behind the lip. 0.4–0.65 s the thumb stays still on the lip. 0.65–2.0 s the hand draws back toward him and to the right; the wheel comes out face-first, tilting 10° toward the stand, its upper lip passes in front of the top bezel; the screen behind now shows an empty neutral area where the picture was. 1.9–2.5 s his left palm slides under the lip at 6 o'clock and takes the weight. 2.5–4.0 s the wheel travels right and hangs one hand's breadth above the two rollers (end frame).
INTEGRATION: as the wheel leaves the screen the cool screen glow on the metal fades to zero by 2.0 s and the office key light takes over; his fingers cast small shadows on the lip; the wheel reflects the room, not a studio.
ACTING: concentration of someone handling something heavy and expensive; eyes on the lip, not the camera.
ANATOMY: thumb opposition visible, fingers wrap the lip and the tips do not show through the metal.
COUNT: one wheel, one laptop, one stand, two hands.
NO-FREEZING.
[GRADE-LOCK]
STOP-INVERSION: no second wheel; the wheel picture does not stay on the screen after the pull; no wheel growing after 2.0 s; no wheel passing through the hand; no fingers in front of the lip except the thumb; no camera move; no glow, sparkles or magic particles on the exit; no flat 2D card look once it is out — the lip has depth and the barrel is visible at the tilt.
[STOP-BASE]
```

## F | 0:23–0:26 | render 4 s
Ustawienia: `seedance_2_5`, `omni_reference`, **`draft: true`**, `9:16`, `duration: 4`, start = **K3**, image_references: [1] K4, [2] @WHEEL, [3] @STAND, [4] @HERO.
Bloki: INTEGRATION, SCALE, SOUND (w montażu), COUNT, FAIL.
```
SCENE: he sets the wheel on the roller stand and spins it with one push.
FORMAT: 4 s, one shot, locked product camera, 9:16, no music, no text.
ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) the wheel stands upright on TWO contact points — its lower lip on both rollers — and the hub centre stays FIXED in the frame while the wheel spins about its own axle. (2) Wheel and rollers counter-rotate at the contact: the wheel turns clockwise as seen from camera, the rollers turn counter-clockwise. IF THE WHEEL ROLLS OFF, HOPS, WOBBLES SIDEWAYS, OR THE HUB MOVES — THE SHOT IS WRONG.
SCALE: the same locked 54 cm wheel as the start frame — torso-high, wider than his shoulders.
TIMING: 0.0–0.6 s he lowers it; the lower lip touches both rollers at 0.6 s (as image 1). 0.6–1.0 s brief hold, both hands release, the stand stays planted. 1.0 s his right fingertips give the outer lip at 3 o'clock one short downward tangential push. 1.0–4.0 s the wheel spins clockwise at about half a turn per second, slowly decaying; spokes stay sharp enough to count; the rollers turn against it.
ACTING: a small satisfied look from the wheel to the lens at 2.0 s, then back to the wheel.
COUNT: one wheel with the true spoke count of image 2, one centre cap, one stand, two rollers.
NO-FREEZING.
[GRADE-LOCK]
STOP-INVERSION: no wheel sliding along the rollers; no hub translation; no rollers standing still; no rollers turning the same way as the wheel; no spinning before the push; no motion-blur disc hiding the spokes; no change of diameter; no wheel lying flat.
[STOP-BASE]
```
Okno detalu (24,8–25,1 s): **nie w renderze**. To warstwa w montażu: czerwony narożnik wysuwa się z okolicy styku i w 6–8 kl. rozwija w ramkę. W środku jest zbliżenie z tego samego źródła obrotu (3D), z tym samym środkiem i kierunkiem. Do testu wystarczy wycinek tego samego klipu F powiększony 2×.

## G | 0:26–0:34 | 0 kredytów
Źródło: **model 3D C19-R** (render w Blenderze, 0 kr) albo nagranie obrotu egzemplarza. Prompt jest dla renderera lub operatora i nie trafia do Seedance. AI nie utrzyma tu geometrii ramion na zbliżeniu.
```
Insert 1 (26–30 s): near-frontal, 100 mm macro look, the actual C19-R rolling slowly clockwise (0.15 rev/s) on the same roller stand, dark slatted background. A broad silver highlight separates the integrated outer aero-ring from the spokes. Insert 2 (30–34 s): three-quarter close-up, same rotation phase continued, a narrow strip light reflection travels down one spoke toward the hub, revealing the depth of the spoke profile. Machined edges legible, Gloss Silver, no text.
```
Bez modelu: frontalny test obrotu z packshotu (obrót 2D w montażu, 0 kr). Insert 2 dostaje wtedy status **„wymaga materiału”**.

## H | 0:34–0:38.8 | render 5 s
Ustawienia: `seedance_2_0`, `std`, `720p`, `9:16`, `duration: 5`, start = **KF-H0**, refs: [1] @HERO, [2] @TWfront, [3] @TWdetail, [4] @WHEEL. audio_references: „Rozmiar, ET i wykończenie dobieramy pod Twoje auto. Napisz, czym jeździsz. Strzała!”.
```
SCENE: he closes the pitch straight to one driver, the silver wheel still turning on the stand beside him.
FORMAT: 5 s, one shot, 9:16, locked camera with faint life, no music, no text.
ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) eye contact with the lens for the whole shot except one short glance at the wheel at 1.0 s. (2) The emblem stays on his LEFT chest. IF HE LOOKS AWAY FOR MORE THAN 0.5 s OR THE EMBLEM CHANGES — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–3.0 s he speaks a short practical sentence, a small open-hand gesture at chest level on the third key word; 1.0 s quick glance to the spinning wheel and back. 3.1–3.9 s short invitation, leaning 5 cm toward the lens. 4.0–4.5 s one last word with a brief real smile. 4.5–5.0 s holds the smile, a small nod.
BACKGROUND: the wheel at frame right, out of focus, keeps turning slowly clockwise on the stand (it will be replaced by the 3D render in post — keep it soft).
ACTING: confident, warm, unhurried; he talks to one person, not to an audience.
[GRADE-LOCK]
STOP-INVERSION: no wide grin; no pointing at the camera; no wheel stopping; no wheel in sharp focus; no emblem on the right chest; no text.
[STOP-BASE]
```
Plansza końcowa 38,8–40 s: render 3D lub obracany packshot (0 kr). Koło ma ten sam środek i średnicę co koło gry w 0:00 (środek 540 × 900 px, średnica ok. 820 px), a po rancie przesuwa się studyjny refleks.
