# Prompty klatek kluczowych (obraz)

Status: 🟨 prompty gotowe, nic nie wyrenderowano.

**Ustawienia domyślne** (Higgsfield `gpt_image_2_6`, wycena 9:16): `quality: medium`, `resolution: 1k`, `aspect_ratio: 9:16`, 1 wariant → **0,5 kr/klatkę**.
Zaakceptowana klatka idzie prosto jako start/end do wideo 720p. Nie renderujemy jej drugi raz w wyższej jakości, bo powstałby inny obraz niż ten, który zatwierdziłeś.

Zasada spójności: najpierw powstają **plany bazowe** (G1, O1, O2, O3). Każda następna klatka w tej samej lokacji jest **edycją** planu bazowego, a nie nowym obrazem. Dlatego tło, światło i kamera trzymają się między klatkami.

## Blok stały (dopisywany do każdej klatki z człowiekiem)

```
HERO — IDENTITY LOCK. @HERO (three-panel sheet: front, back, close-up) controls face, hair and body 100%. One man, 31, Polish, 163 cm, compact athletic build: broad chest and shoulders for his height, solid forearms, head about one-seventh of his height. Slightly wide oval face with a firm square jaw, light forehead lines, straight medium-thick brows, hazel-green eyes, straight medium nose, short light stubble on upper lip and chin, ears standing slightly out. Hair: short dark brown with ash-silver highlights on top, brushed up and back sweeping slightly to his left, smooth low skin fade on the sides — no shaved part line, no glasses, no full beard. Fair skin with real pores and natural unevenness, no smoothing. Straight mid-blue jeans with no visible brand tab or patch, plain white low-top leather sneakers. Take ONLY identity from the sheet — not its grey backdrop, not its even studio light, not its layout, not its sceptical squint; his resting expression is relaxed with a trace of amusement. Exactly one person in the image; every hand is his.
Vertical 9:16, natural commercial photography, physically motivated light, readable shadows, fine grain. Leave the lower 22% of the frame calm for Polish captions added in post. No text, no letters, no logos except the ones explicitly requested.
```

---

## Plany bazowe

### KF-G1 — pokój gier, od ekranu w stronę kanapy (baza dla A)
Pliki: [1] @HERO `Postac-FINAL.png`, [2] @GAME `Gamingroom_tk700sti-A.jpg`, [3] @GT **(do podmiany)**
```
Reverse angle of the room layout in image 2: the camera stands just in front of the big screen, at seated eye height, looking back at a dark three-seat sofa with a low black coffee table in front of it. Keep only the spatial relationship sofa – low table – screen from image 2; re-dress the room in black, red and white only: matte black walls, two long white floating shelves on the wall behind the sofa carrying about twelve 1:43 racing-car models, one red practical light strip mounted vertically at the right end of the shelves, washing the dark wall and outlining the models in red. No purple, no neon tubes, no posters, no projector, no figurines. The off-screen game screen throws soft neutral fill onto his face from the lens direction.
He sits centred, forearms on his knees, holding a plain black game controller with no visible brand, looking slightly above the lens at the paused game. He wears the black T-shirt from image 3 with its white logo on the chest (keep the print exactly as in image 3). Medium shot, knees to head, head at 30% from the top.
[HERO LOCK]
```

### KF-O1 — biuro, plan frontalny (baza dla B, C, H)
Pliki: [1] @STAND `brixton-forged-…-wheel-25.jpg` — **wersja pusta, bez postaci**
```
Empty location plate, vertical 9:16, camera at seated eye height (110 cm), straight-on. A compact premium forged-wheel showroom office. Back wall: vertical matte black wooden slats like the background of image 1, with six forged wheels mounted in two rows of three on small white brackets; all wall wheels are matte black or dark gunmetal, different multi-spoke designs, no logos, none of them silver. In front of the wall a low black sofa, seat 45 cm high. In front of the sofa a low black coffee table (top 45 cm). On the left third of the table a closed silver laptop. On the right end of the table, on the same tabletop, a black anodised aluminium wheel stand with the low profile of the stand in image 1 but with two horizontal steel rollers 22 cm apart; no lettering on it. Above the stand keep 70 cm of empty air for a full-size wheel. Light: neutral 4300 K soft key from camera left, a thin red LED accent line running vertically along the right edge of the slat wall, polished dark concrete floor. Take from image 1 only the stand silhouette, the slat texture and the side-led reflection style — not its wheel, not its champagne colour, not its lettering.
```

### KF-O2 — biuro, kamera produktowa 3/4 (baza dla E–F, K1–K4)
Pliki: [1] KF-O1 (zaakceptowana), [2] @STAND
```
Same room, furniture and light as image 1, new camera: shallow three-quarter angle from the front-right, lens at 75 cm above the floor (30 cm above the tabletop), 35 mm full-frame equivalent. Laptop open on the left third of the table, its screen turned about 25° away from camera so all four bezel corners and the top bezel edge are clearly visible; the screen shows a plain light-grey page. The roller stand on the right of the laptop on the same tabletop, its two rollers parallel to the screen. The sofa and the slatted wheel wall soft in the background (f/2.8). Leave empty air above the stand and between the laptop and the stand for a 54 cm wheel and two hands.
```

### KF-O3 — biuro, zza ramienia (baza dla D)
Pliki: [1] @HERO, [2] KF-O1, [3] @TWback, [4] @TWfront
```
Same room as image 2. Camera at the right end of the sofa, 160 cm high, 45° behind his right shoulder, looking down over that shoulder to the laptop on the coffee table. He sits on the front edge of the sofa and leans forward to the laptop, his back turned three-quarters to camera. He wears the black crew-neck T-shirt from images 3 and 4: on the back the crystal word TURISMO above a large crystal wheel outline exactly as in image 3 — at this angle the word and the upper half of the wheel are readable on his upper back. The near shoulder and the back of his head sharp in the left third of the frame; the laptop lid half open (45°), screen plain light-grey.
[HERO LOCK]
```

---

## Klatki ujęć

### KF-A0 — kciuk na pauzie (start A)
Pliki: [1] @HERO, [2] KF-G1
```
Extreme close-up from image 2's room: his right thumb pressing the options/pause button of the plain black controller, the controller held in both hands at chest level, the black T-shirt soft behind. The red practical makes a soft red rim on the knuckles; neutral screen light from the lens direction. Exactly two hands, five fingers each.
[HERO LOCK]
```

### KF-A9 — dłoń przed pstryknięciem (koniec A)
Pliki: [1] @HERO, [2] KF-G1
```
Tight shot in the room of image 2: his right hand raised close to the lens, palm toward camera turned 30° to frame left, thumb pad pressed firmly against the middle fingertip, index finger relaxed and slightly forward, ring and little fingers curled — the instant before a finger snap. The hand fills the central 45% of the frame width, middle-finger tip at 38% from the top. Behind the hand, out of focus: the red-washed shelves of racing models and his face looking into the lens.
[HERO LOCK]
```

### KF-B0 — ta sama dłoń w biurze (start B)
Pliki: [1] KF-A9 (zaakceptowana), [2] KF-O1
```
Edit image 1. Keep the hand EXACTLY — same pose, same size, same position in frame, same finger contact. Replace only the background and the light: behind the hand, out of focus, the office of image 2 — black slatted wall with dark wheels, him standing in front of the sofa, black T-shirt with white chest logo. Neutral 4300 K soft light from frame left on the hand, no red rim. Nothing else changes.
```

### KF-C1 — C-PRZED (koniec B)
Pliki: [1] @HERO, [2] KF-O1, [3] @GT **(do podmiany)**
```
Image 2's room and camera position, medium shot (mid-thigh to head). He sits back on the sofa, centred. He wears the black T-shirt from image 3 with its white chest logo. His LEFT hand pinches a small fold of the shirt fabric 8 cm below his left chest, pulling it 3 cm forward. His RIGHT hand is raised at shoulder height in a finger-snap pose (thumb pressed to middle finger). His eyes look down at the shirt, eyebrows slightly raised. The roller stand on the right end of the table is empty; the laptop is closed on the left.
[HERO LOCK]
```

### KF-C2 — C-PO (start C) — edycja KF-C1
Pliki: [1] KF-C1 (zaakceptowana), [2] @TWdetail, [3] @TWfront
```
Edit image 1. Change ONLY the T-shirt print: remove the white chest logo completely so the chest is plain black cotton, and add the small crystal emblem from image 2 on the wearer's LEFT chest (viewer's right), placed as in image 3: emblem width one-sixth of his shoulder width, its centre 9 cm below the collar seam, over the left chest. Clear and silver-white crystals with the small red crystal cluster at the lower left of the emblem, following the fabric curve and the fold his left hand is pulling. Keep everything else pixel-identical: face, hair, both hands, finger positions, neckline, sofa seam, light, background, framing.
```
Kontrola: nałóż C1 i C2 w trybie „różnica” — poza znakiem i miejscem po logo GT nie może być różnic (patrz `04-proby-C-i-EF.md`).

### KF-D0 / KF-D9 — zza ramienia (start i koniec D)
D0 = KF-O3 (zaakceptowany). D9 — edycja KF-O3:
```
Edit image 1. Same camera, same pose but the laptop lid fully open at 110°, his right hand resting near the trackpad, focus now on the screen: the screen is a flat even light-grey surface with all four corners clearly visible and unobstructed (it will be replaced in post). His shoulder and head soft in the left third.
```

### K1–K4 — felga z ekranu na rolki
Pliki dla wszystkich: [1] KF-O2 (zaakceptowany), [2] @HERO, [3] @WHEEL **(do podmiany — packshot C19-R Gloss Silver, przód)**, [4] @STAND.
Wspólny dopisek:
```
The wheel is ALWAYS the exact design of image 3 — same number of spokes, same spoke shape, same integrated outer aero-ring, same centre cap, Gloss Silver. One wheel only. Full size the wheel is 54 cm across: as tall as his torso from collarbone to belt, wider than his shoulders, his spread hand covers about one-third of its diameter. He sits on the sofa edge behind the table, leaning in; his face is visible above the laptop, upper body in frame.
[HERO LOCK]
```
**K1** (19,0 s):
```
Edit image 1. The laptop screen shows image 3 as a catalogue product photo: the wheel seen exactly face-on, centred on a light-grey page, diameter one-third of the screen width; the valve hole visible at 4 o'clock. His right hand approaches from above-right, fingers open, 6 cm in front of the screen, thumb aiming at the top edge of the wheel image.
```
**K2** (19,4 s) — edycja K1:
```
Edit image 1. His right thumb pad now rests on the screen exactly on the outer lip of the wheel image at 12 o'clock, covering the lip. His index, middle and ring fingertips are not visible — they look as if they have slipped behind the wheel's lip into the image. The rest is unchanged.
```
**K3** (23,0 s) — edycja K2:
```
Edit image 1. The wheel is now a real, physical, full-size 54 cm Gloss Silver wheel out of the laptop: held vertically, face toward camera turned 10° to frame left, right thumb on the front lip at 12 o'clock with the fingers behind the lip, his left palm under the lip at 6 o'clock carrying the weight. It hangs one hand's breadth (10 cm) above the two rollers of the stand. The laptop screen behind now shows the same light-grey page with an EMPTY neutral area where the wheel photo was. Cool screen light is gone from the metal: the wheel is lit only by the office key and the side reflection.
```
**K4** (23,6 s) — edycja K3:
```
Edit image 1. The same wheel now rests upright on the stand: its lower lip touches BOTH rollers (two contact points, the hub centre exactly above the midpoint between the rollers). Both hands released, 5 cm away from the lip, his right fingertips near the outer lip at 3 o'clock, ready to push. Stand planted, no tilt of the wheel.
```
Sprawdzenie obok siebie przed ruchem: `storyboard/01_E-F_4_klatki_os_czasu.png` + K1–K4 w jednym rzędzie: ten sam kadr, to samo światło. Zawór (wentyl) na 4:00 w K1 i K3 pozwala śledzić jedno ramię od ekranu do rolek.

### KF-H0 — domknięcie (start H)
Pliki: [1] @HERO, [2] KF-O1, [3] @TWfront, [4] @TWdetail, [5] @WHEEL **(do podmiany)**
```
Image 2's room, closer: medium close-up, chest to head, camera at his eye height, he sits on the sofa slightly turned toward the lens, looking straight into it with a calm, confident half smile. He wears the black crew-neck T-shirt with the small crystal emblem on his LEFT chest (images 3 and 4). On the right edge of frame, slightly behind him and out of focus, the Gloss Silver wheel of image 5 stands upright on the roller stand. Leave the right-centre area of the frame clear for three stacked caption words.
[HERO LOCK]
```

---

## Kolejność generowania i bramki akceptacji
1. **Bramka 1** (4 klatki, ok. 2 kr): G1, O1 → O2, O3. Akceptujesz lokacje.
2. **Bramka 2** (11 klatek, ok. 5,5 kr): A0, A9 → B0, C1 → C2, D9, K1 → K2 → K3 → K4, H0. Akceptujesz kontaktówkę.
3. Dopiero potem ruch (`03-prompty-ruchu.md`).
