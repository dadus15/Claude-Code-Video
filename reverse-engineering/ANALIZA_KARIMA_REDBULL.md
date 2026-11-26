# Analiza: reklama Red Bull F1 (Karima, YouTube) i co przenosimy do projektu Turismo

Źródło: plik z WeTransfer (18 min, 640×360, 23,976 fps) + transkrypcja.
Uwaga: skill **cinedance-block-library**, z którego już korzystamy, to jej biblioteka bloków (stąd „Karima's face lock” w jego opisie).

## 1. Silnik i algorytm (z transkrypcji)
| Etap | U niej | U nas |
|---|---|---|
| Assety najpierw | arkusze postaci / auta / byka / lokacji (Seedream, Cinema Studio) zanim powstanie jakiekolwiek wideo | arkusz felgi V05 (5 widoków), arkusz RS5 satin black, arkusz lokacji (zimowy parking): obraz → potem wideo |
| Prompty | zawsze pisze Claude (Opus), nigdy ręcznie | tak robimy (cinedance-block-library + cinema-worldbuilder) |
| „Optical block” | stały dopisek do promptu lokacji: dystorsja anamorficzna, grading, ziarno filmowe | bloki OPT-WIDE + GRADE-BRIGHT + GRADE-LOCK + ziarno; dla nas obiektyw action-cam, nie anamorfa |
| Wideo | Seedance 2.5, najpierw niska jakość, potem upscale | szkic 480p (~46 kr) → 1080p (~259 kr) |
| Precyzyjny ruch | Blender (wtyczka Higgsfield + Opus pisze Python) → render → Seedance z poleceniem „kamera i fizyka identyczne z referencją Blendera” | to jest nasz pipeline (prowadnica v4, 3D Jutsu) |
| Poprawki | nie przepisuje promptu, gdy ruch jest dobry: generuje kilka razy i skleja najlepsze fragmenty | 2–3 warianty szkicu, montaż z najlepszych |
| Genjutsu | podmiana obiektu w gotowym klipie z zachowaniem ruchu kamery (auto → byk) do match cutów | match cut: obracająca się felga → logo Turismo / zdjęcie RS5 |

## 2. Montaż reklamy (pomiar cięć, 0–40 s)
- **Hook 0–8,6 s:** jedno długie ujęcie (postać + auto w dymie), bez cięć.
- **Rozwinięcie 8,6–20 s:** ujęcia 0,6–1,3 s, inserty makro (puszka, wlew, opona z wyładowaniem).
- **Przejście „flash”:** złoty płyn wypełnia kadr → biel → nowa scena (cięcie ukryte w jasności).
- **Transformacja:** białe auto → malowanie Red Bull z błyskawicami (reveal w ruchu).
- **Hero 19,8–24,2 s:** jedno dłuższe ujęcie 4,4 s (oddech przed dropem).
- **Kulminacja 27,8–28,7 s i 36,4–38,5 s:** cięcia co 0,12–0,25 s, zsynchronizowane z bitem (strobe montage).
- **Match cut auto ↔ byk:** ten sam ruch kamery, podmieniony obiekt.
- **Grade:** nocny stadion, teal/blue z ciepłymi akcentami, flary, ziarno.

## 3. Plan dla Turismo (po zatwierdzeniu głównego ujęcia)
1. **0–13 s:** główne ujęcie rig (prowadnica v4 → Seedance), jak oryginał TikToka.
2. **Przejście:** felga kręci się coraz szybciej → spin blur → biały flash (jak złoty płyn u Karimy) → match cut na zdjęcie RS5 _01 (koło w tym samym miejscu kadru).
3. **Strobe ze zdjęć RS5 (0,25 s/zdjęcie, na bit):** _15, _04, _11, _13, _06 z lekkim push-in i dopasowaniem pozycji felgi (felga zawsze w tym samym punkcie kadru = „match cut” na zdjęciach).
4. **End card:** iris przez piastę → TURISMO WHEELS · UNLOCK YOUR STYLE · Daniel Chmielewski · +48 501 404 861 · e-mail.
