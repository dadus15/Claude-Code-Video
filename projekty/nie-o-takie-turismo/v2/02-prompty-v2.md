# Prompty v2 — klatki i ruch

Status: 🟨 gotowe do wklejenia, nic nie wyrenderowano.
- Blok `[HERO LOCK]`, `[GRADE-LOCK]` i `[STOP-BASE]` są bez zmian z `../02-prompty-klatek.md` i `../03-prompty-ruchu.md`.
- Ustawienia klatek: `gpt_image_2_6`, medium, 1k, 9:16 (0,5 kr).
- Ruch: `seedance_2_0` std 720p (4,5 kr/s). Wyjątek: U8, które idzie przez draft `seedance_2_5`.

Zasada spójności lokacji: każda lokacja ma **jedną klatkę bazową**, a kolejne klatki są jej edycjami.

---

## Klatki

### KF-U2 — kontrplan w pokoju gier (start U2)
Pliki: [1] @HERO, [2] `plansze/G0_pokoj_kolory_Turismo.jpg` (pokój z assetu w barwach Turismo), [3] @GT (do podmiany)
```
Reverse angle inside the room of image 2 — keep its exact style: black brick walls, red LED strips along the wall edges and ceiling, white low media cabinets, dark sofa with red cushions, striped dark rug, low black coffee table. The camera stands beside the big screen at seated eye height and looks back at the sofa. He sits in the middle of the sofa holding a plain black controller, wearing the black T-shirt with the white chest logo of image 3. Behind him: black brick wall with a horizontal red LED strip and a white shelf of small racing-car models. His face is lit softly by the screen from the lens direction; red LED rim light on his hair and shoulders. Medium shot, knees to head.
[HERO LOCK]
```

### KF-U3a / KF-U3b — para do przejścia (wariant A)
U3a: edycja KF-U2. Kadr od pasa w górę, prawa dłoń w pozie pstryknięcia na wysokości barku, wzrok w obiektyw.
```
Edit image 1: reframe to a waist-up shot, his head centred at 28% from the top. His right hand raised at shoulder height in a finger-snap pose (thumb pressed to middle finger), controller gone, eyes in the lens, a faint half smile.
```
U3b: edycja U3a, a w niej **tylko tło i światło**:
```
Edit image 1. Keep him EXACTLY — same pose, same hand, same head size and position, same framing. He is now standing outdoors in front of the glass entrance of a modern forged-wheel showroom: a black facade with vertical slats, a tall frameless glass door with a black handle, the word TURISMO in clean white capital letters on the facade above the door, soft overcast daylight. [Optional: his T-shirt is now the black crew-neck with the small crystal emblem on his LEFT chest from @TWdetail and no chest logo.]
```
Kontrola: nałożenie U3a/U3b w trybie „różnica” — Ty nie możesz się świecić.

### KF-U4a — wejście do biura (start U4a)
= KF-U3b w szerszym kadrze, od kolan w górę: drzwi po jego lewej, dłoń na klamce.

### KF-U4b — hol z felgami (start U4b)
Pliki: [1] @HERO, [2] KF-U4a, [3] @TWback, [4] @TWfront
```
Interior of the same showroom: a straight hallway 2.2 m wide and 9 m long. Both walls are covered floor to ceiling with forged wheels mounted face-out on hidden brackets, in rows, mostly dark finishes (satin black, gunmetal, brushed grey) with a few brushed-bronze accents; no logos on wheels. Black slatted ceiling with a continuous white linear light, thin red LED line at the base of both walls, dark polished concrete floor reflecting the wheels. At the far end an open doorway to a lounge room. He walks toward camera in the middle of the hallway, 3 m from the lens, mid-stride, black crew-neck with the crystal emblem on his LEFT chest, looking into the lens.
[HERO LOCK]
```

### KF-U5 — salon z laptopem (baza dla U5, U8, U9, U10)
Pliki: [1] KF-U4b (styl wnętrza), [2] @STAND
```
The lounge at the end of the same hallway, same materials and light: a low black sofa against a black slatted wall with four dark wheels on white brackets; a low black coffee table in front (top 45 cm); a closed silver laptop on the left third of the table; on the right end of the table a black anodised stand with the low profile of image 2 and two horizontal steel rollers 22 cm apart, no lettering. 70 cm of empty air above the stand. Neutral 4300 K key from camera left, thin red accent line on the right wall edge. Camera at seated eye height, 3/4 from front-right, 30 mm.
```
Następnie klatki z Tobą: siadasz → otwierasz laptop (edycje bazy, jak K1 i K3 w v1). **Felga w U8 nie jest generowana**: w klatkach AI dłonie trzymają neutralny ciemnoszary krążek 54 cm (proxy), który w montażu zastępuje render C01 z Blendera.

### KF-U10 — CTA
Edycja KF-U5: plan średni-bliski, siedzi, patrzy w obiektyw, po prawej rozmyta podstawka z obracającą się felgą (proxy, podmiana w BL).

---

## Ruch

### U2 | 5 s | start KF-U2, koniec KF-U3a | audio_references: „To chyba nie to Turismo.”
```
SCENE: a gamer in his black-and-red room realises this is not the Turismo he meant.
FORMAT: 5 s, one shot, 9:16, no music, no text. ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: he ends EXACTLY on the end frame — waist-up, right hand raised in a snap pose, eyes in the lens. The snap is NOT completed in this shot. IF THE SNAP HAPPENS — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–0.6 s eyes on the screen (just above lens), screen light flickers softly on his face. 0.6 s eyes move into the lens. 0.6–2.4 s one short dry line, amused. 2.6 s he puts the controller on the cushion. 2.8–5.0 s the camera eases in from medium to waist-up while he raises his right hand into the snap pose.
CAMERA: slow push-in, no shake. LIGHT: screen fill from the lens direction, red LED rim. 
[GRADE-LOCK]
STOP-INVERSION: no snap; no laugh; no purple or blue light; no posters behind him; controller not in hand at the end.
[STOP-BASE]
```

### U4a | 4 s | start KF-U4a
```
SCENE: he walks into the Turismo showroom.
FORMAT: 4 s, one shot, 9:16, no music, no text. ONE PERSON ONLY.
MOST IMPORTANT: the camera moves BACKWARD through the doorway ahead of him at walking pace and keeps him waist-up. The door is glass and he opens it with his left hand by the black handle. IF THE CAMERA PASSES THROUGH THE GLASS OR THE DOOR OPENS BY ITSELF — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–1.0 s he pulls the door open and steps in. 1.0–4.0 s he walks forward into the hallway; wheels on the walls start to appear at the frame edges; camera retreats ahead of him, smooth steadicam with gentle footstep bounce.
[GRADE-LOCK]  STOP-INVERSION: no second person; no camera cut; the door does not vanish; text on the facade stays exactly TURISMO.
[STOP-BASE]
```

### U4b | 7 s | start KF-U4b | audio_references: dwie kwestie z holu
```
SCENE: walk-and-talk down a hallway lined with forged wheels.
FORMAT: 7 s, one continuous steadicam shot, 9:16, no music, no text. ONE PERSON ONLY, from @HERO.
MOST IMPORTANT: (1) he walks toward the camera at a calm pace (about 0.8 m/s), the camera retreats at the same speed so he stays knees-up and centred. (2) The walls are full of wheels the whole time, wheels never float, morph or multiply. IF A WHEEL CHANGES SHAPE OR HE DRIFTS IN SIZE — THE SHOT IS WRONG.
[HERO LOCK]
TIMING: 0.0–4.2 s first line to the lens while walking, a small open-hand gesture toward the wall at 2.0 s. 4.5–6.4 s second line, an inviting 'follow me' gesture with the right hand at 5.2 s. 6.4–7.0 s he turns his shoulders toward the open lounge doorway on his left.
CAMERA: steadicam backward, footstep bounce, no rotation. LIGHT: white linear ceiling light, red base lines, floor reflections.
[GRADE-LOCK]  STOP-INVERSION: no wheels rolling on the walls; no extra people; no camera orbit; no speed ramp.
[STOP-BASE]
```

### U5 | 4 s | start: Ty w drzwiach salonu (edycja KF-U5), koniec: siedzi, laptop otwarty
```
FORMAT: 4 s, one shot, 9:16. ONE PERSON ONLY.
TIMING: 0.0–1.5 s he enters and sits on the front edge of the sofa. 1.5–4.0 s he opens the laptop to 110°; the screen is a flat even light-grey surface with all four corners visible (replaced in post). The roller stand on the right stays EMPTY.
STOP-INVERSION: nothing readable on the screen; no wheel on the stand; no logo on the laptop.
[HERO LOCK] [GRADE-LOCK] [STOP-BASE]
```

### U8 | 5 s | `seedance_2_5` draft → finalize | start/koniec: K1/K3 z salonu (proxy krążek)
Prompt E z `../03-prompty-ruchu.md` z dwiema zmianami:
1. Felga = **„a neutral dark-grey disc proxy, 54 cm, no spokes”** (dla łatwego roto; C01 wstawia Blender).
2. Laptop i podstawka według KF-U5.

Kolejność warstw i klatki kciuka: `../04-proby-C-i-EF.md` (od kl. 787 = 31,5 s spotu).

### U9 rozmowa (4 s) i U10 CTA (4 s)
Prompt H z `../03-prompty-ruchu.md`: start KF-U10, felga po prawej rozmyta (proxy), audio_references z Twoimi kwestiami.
