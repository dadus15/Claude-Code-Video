# Analiza: kaye.creatives, „How To Make Insane Video Editing With Opus 5.5 (Claude Motion)”

Źródło: `kaye_tutorial_claude_motion.mp4` (15:21, 640×360), pobrany z release `referencje-v1`. Transkrypcja: `kaye_transcript.txt`.
Arkusze kadrów co 4 s: `kaye_sheets/`. Kluczowe klatki z promptami: `kaye_frames/`.

## 1. Narzędzia, których używa
| Narzędzie | Do czego |
|---|---|
| **Claude (Opus 5.5, tryb Extra)** w aplikacji Claude, praca w folderze projektu („This computer”), Bypass permissions | Cały montaż na podstawie jednej wiadomości |
| **Higgsfield MCP** (konektor) | B-roll na każde zdanie: zdjęcia, klipy, prowadzący z ruchem ust, muzyka; „Used Higgsfield AI 8 times” |
| **Notion** (konektor) | Notatki |
| **Skill 1: `claude-motion-reels.skill`** (talking head) | Reguły layoutu, „spacing math”, krzywe animacji; mamy go jako `narzedzia/reel` |
| **Skill 2: `claude-motion-design.skill`** (pełne motion design z samego głosu) | Szklane ramki, siatka perspektywiczna, karty, typewriter; mamy go jako `skille-kaye/voiceover-glass-reel` |
| **After Effects** (pliki `reel.jsx`, `motion.jsx`) | Claude buduje kompozycję w AE i renderuje MP4 |
| Referencje: 3 rolki z Instagrama, zrzut fontu (Anton + cienki szeryf), paleta (czerwony / biały / czarny) | Styl |

## 2. Jej przepływ pracy (cztery wejścia + brief)
1. **Surowe nagranie** z telefonu, bez cięcia: Claude sam wycina pauzy i pomyłki.
2. **Skrypt** (txt), żeby napisy i animacje trafiały w słowa.
3. **2–3 referencje wizualne**: rolki, których montaż się podoba, zrzut fontu, paleta z Pinteresta. „Im więcej referencji, tym lepiej”, bo „Claude nie ma intuicji: słabe referencje = generyczny wynik”.
4. **Skill** z regułami layoutu.
5. **Brief prostym językiem**, bez technicznych nazw efektów: co ma się dziać w każdym momencie filmu.
6. **v1 → poprawki liczbowe → v2.** Przykład jej poprawki (cytat z ekranu, 6:18):
   > „Make the pacing 15% tighter between cuts. Increase the size of the kinetic text graphics by 25%, speed up their entry animation so they snap in on the beat of my voice, and add a subtle drop shadow so they stay readable against my shirt.”

### Brief do talking head (cytat z ekranu, 4:36)
> „This is my raw talking-head video, EXPERIMENT, with the script below. Here are three reels for the style I want: [3 linki]. It's about the Emergence AI experiment … Edit it into a vertical 9:16 reel yourself, right here in Claude Code, and use your MCP tools for anything you need, like finding or generating footage. Cut out the long pauses and mistakes, and level the audio for social media. Put the key words in large Anton type, the secondary phrases in a thin serif font, and add subtitles at the bottom. Keep the palette to red, white and black-and-white B-roll. Add B-roll that matches what I'm saying: clips from movies and scenes from the experiment itself. Keep me full screen most of the time, and switch to a split screen with the footage on top and me [at the bottom] …”

### Brief do pełnego motion design (cytaty z ekranu, 9:56 i 10:04)
> „Assets: generate everything in Higgsfield. First make a character sheet for each of the four townspeople and for each location. Then make short video clips, so every sentence has its own picture. Never repeat a clip. … Whenever I'm talking to the camera, show a host on an old TV set … lip-sync it to my voice. Show the logos … only at the moment I say each name. … Make an original music bed. Use free sound effects: typewriter keys, whooshes …”
>
> „In the middle section, where I list the three points …, add a moving perspective grid in the background. Make each keyword … flip colour right as I say it. … Keep the main typography clean and modest in the centre of the frame, and let the glass cards float in calmly.”

## 3. Techniki montażu (z jej filmu i obu testów)
**Hook i tempo**
- Hook to prowokacyjne pytanie z obietnicą: „What if I told you the safest AI tool you use every day is actually lying to you? Let me explain.”
- Pierwsze 5 s muszą być szybkie, a nagłówek duży. To jej pierwsza poprawka v1.
- Nie więcej niż ok. 2–4 s samej twarzy bez ruchu na ekranie („4 s on my face” to błąd).
- Tekst „snapuje” na akcent głosu, nie wjeżdża powoli.

**Talking head (test 1)**
- Duże słowa kluczowe w Anton, frazy poboczne cienkim szeryfem, napisy na dole.
- Split screen: footage na górze, prowadzący na dole.
- B-roll czarno-biały, akcent czerwony; generowany na każde zdanie, nigdy powtórzony.
- Wersja człowieka: kamera „oddycha” z głosem (push-in na akcentach), organiczny rytm whooshy i uderzeń.

**Motion design (test 2)**
- Klipy w pływających szklanych ramkach z cienką świecącą krawędzią i płynnym push-in.
- Ruchoma siatka perspektywiczna w tle, a słowa kluczowe zmieniają kolor dokładnie na słowie.
- Strony typewriter, jedno gigantyczne słowo z czerwoną etykietą, karty-polaroidy z logo w chwili wymówienia nazwy.
- Prowadzący na starym telewizorze z ruchem ust (host).
- Wersja człowieka: przejścia kamerą 3D między tematami i mikro-odbicia ikon.

**Jej własny montaż tutorialu**
- Jasne tło z brzoskwiniowo-koralowym gradientem i dużym szeryfowym nagłówkiem („My exact Claude workflow.”).
- Karty UI: czat, tabela, pigułki kroków „1 Raw clip · 2 Script · 3 References · 4 Motion skill”.
- Karty A/B do zgadywania, tabela wypełniana wiersz po wierszu na słowach, waveform z tagami „pauses / mistakes”.
- Podpisy w talking head: mała linia sans plus pochyły koralowy szeryf („quick setup step”, „the final”).
- Okienko z twarzą w kółku (PiP) przy nagraniach ekranu, zbliżenia z kursorem na detal.
- Animowany przycisk Subscribe, wezwania do komentarza („lock your guess in the comments”).

## 4. Co z tego bierzemy do v4 „Nie o takie Turismo”
1. **Hook jako prowokacja z obietnicą**: „Ta felga NIE jest z gry.” i od razu dowód (wjazd w ekran → prawdziwa C01). Pierwsze 5 s: cięcie co ≤1 s, duży nagłówek.
2. **Brief jak do montażysty**: piszę do siebie brief na każdy moment (już w planie v4) i robię v1 → poprawki liczbowe → v2.
3. **Detale felg w stylu skill 2**: każda cecha (deep concave, frezowania, aero-ring, gravity cap) dostaje szklaną ramkę z push-in, ruchomą siatkę w tle i słowo kluczowe zmieniające kolor na słowie; realizacje jako karty-polaroidy z logo marki auta w chwili, gdy pada nazwa.
4. **Maks. 2–4 s samej twarzy**: przy laptopie split screen (strona u góry, Ty na dole), zbliżenia z kursorem na klikany element, okienko z twarzą (PiP) przy pełnoekranowej stronie.
5. **Tekst snap na akcent**, cień pod tekstem, Anton + cienki szeryf + napisy na dole (EN).
6. **B-roll nigdy powtórzony**, generowany pod konkretne zdanie (Higgsfield).
7. **CTA z zaangażowaniem**: pytanie do komentarzy, np. „Który model założyłbyś na swoje auto? Napisz w komentarzu.”

Ograniczenie techniczne: skill 2 Kaye buduje film w After Effects na Macu. Tutaj (Linux, chmura) odtwarzam ten sam wygląd w naszym rendererze Python/FFmpeg: szklane ramki, siatkę i karty jako inserty.
