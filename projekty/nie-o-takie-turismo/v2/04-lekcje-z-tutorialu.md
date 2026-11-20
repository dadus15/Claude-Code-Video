# Lekcje z filmu kaye.creatives („I Made a Professional Commercial Using Only AI — Step-by-Step”)

Źródło: analiza scena po scenie wykonana przez Higgsfield (`video_analysis`, 0 kr) dla https://www.youtube.com/watch?v=d-TCtUhaLiU.

**Zakres:** analiza objęła **pierwsze 56 s**, czyli gotową reklamę Oakley × Meta pokazaną na początku filmu. **Narracja „krok po kroku” (dalsza część) nie została jeszcze przeczytana**. Brakuje do niej transkrypcji, patrz koniec pliku.

## Co widać w gotowej reklamie (fakty z analizy)
| Scena | Czas | Ujęcie | Dźwięk |
|---|---|---|---|
| 1 | 0:00–0:06 | **Hook z nietypowego kąta**: kamera do góry nogami, zbliżenie twarzy, bohaterka stoi na rękach na krawędzi klifu; powolny odjazd | rozmowa z produktem: „Hey Meta, are you filming?” |
| 2 | 0:06–0:07 | plan ogólny: góry we mgle | niski świst wiatru, klik mechaniczny |
| 3 | 0:07–0:11 | lot w wingsuicie, kamera za nią; **obok leci kruk** | ryk wiatru, okrzyk |
| 4 | 0:11–0:15 | przelot obok trzech wspinaczy | świst przelotu |
| 5 | 0:15–0:17 | **POV przez gogle** w wąskiej szczelinie, kamera drży | wiatr, gwałtowny wdech |
| 6 | 0:17–0:21 | **przejście przez ptaka**: ptak nad drogą, panorama w dół na kolarkę | wiatr → szum opon |
| 7–12 | 0:21–0:39 | kolarstwo, galop na pustyni, nocne wejście w śnieg, surfing w tubie fali | każda scena ma własny, konkretny dźwięk; 2 krótkie dialogi z asystentem |
| 13–17 | 0:39–0:49 | „prawdziwe życie”: uśmiech do kamery, pingwiny, motorówka, **POV z góry na mapę**, ognisko | śmiech, pingwiny, silnik, marker i czajnik, rozmowy |
| 18 | 0:49–0:56 | CTA: zdejmuje gogle, patrzy w obiektyw, **ostrość przechodzi na dłonie składające gogle** | „Over to you…”, metaliczny klik |

## Siedem zasad wyciągniętych z tej reklamy i jak je stosujemy
1. **Krótkie ujęcia.** 18 ujęć w 56 s daje średnio 3,1 s, a poza CTA nic nie trwa dłużej niż ok. 4 s. Generator utrzymuje realizm w krótkich ujęciach, a artefakty (twarz, dłonie, felgi na ścianach) narastają z długością.
   → **Rozbijamy długie ujęcia v2**: hol 7 s zamieniamy na 3 ujęcia (dłoń na klamce / felgi przesuwające się w tle / Ty mówisz), a scenę z laptopem na 2 (wejście / dłonie otwierające klapę).
2. **Jedna postać i jeden produkt w każdym ujęciu.** Gogle są w każdej scenie, na twarzy albo w dłoniach.
   → Felga (na ekranie GT, na ścianach holu, na laptopie, na rolkach) albo znak Turismo na koszulce są w każdym ujęciu.
3. **Przejścia niesie ruch lub obiekt, a nie efekt.** Kruk leci obok → ptak nad drogą → panorama w dół na nową scenę.
   → Pstryk (dłoń), szybka panorama z ekranu na Ciebie, obrót felgi przy podmianie modeli. Bez przenikań i bez efektów „glitch”.
4. **Każde ujęcie ma swój konkretny dźwięk, a cięcie przełącza go natychmiast.**
   → Klik pada, pstryk, uszczelka szklanych drzwi, kroki z pogłosem holu, klawisze laptopa, szum rolek. Muzyka tylko pod tym.
5. **„Szalone kąty” w hooku i w kluczowych momentach:** do góry nogami, POV przez produkt, z góry na stół.
   → Propozycje: (a) 1. klatka spotu z perspektywy ekranu gry, czyli koło GT wypełnia kadr, a kamera „wychodzi” z ekranu nad Twoje ramię; (b) przy wyjmowaniu felgi krótki POV z kamerą przyklejoną do felgi (blok CAM-RIG z Cinedance, robiony w Blenderze). Obie do Twojej decyzji.
6. **Naturalne, umotywowane światło i jeden kolor dla całości.** Pochmurne, chłodne, bez połysku CGI.
   → W biurze miękkie światło dzienne z okna plus jeden czerwony akcent. Czerwień tylko w pokoju gier. GRADE-LOCK na całość, a ziarno i ostrość wyrównujemy w montażu.
7. **Finał: kamera zostaje przy produkcie, gdy ten przechodzi z twarzy do dłoni.**
   → Finał zostaje na felgach. Plansza końcowa z trzema modelami, środkowa w miejscu koła z gry.

Kadr z tutorialu (`Tutorial-fragment.jpg`) potwierdza też metodę, którą już stosujemy: **lokacja jest osobną płytą** („@image1 is the LOCATION: the cliff edge plate…”), a postać wchodzi do niej przez referencje.

## Płynność: konkretne ustawienia techniczne
- **Klatkaż:** montaż w natywnym klatkażu generatora. Jeśli Seedance oddaje 24 kl./s, cały spot robimy w 24 kl./s zamiast 25. Konwersja 24→25 powoduje mikroszarpnięcia przy ruchach kamery. Sprawdzimy to na pierwszym teście.
- **Cięcia w ruchu:** każde cięcie wypada w trakcie ruchu (dłoń, panorama, krok), nigdy na nieruchomym kadrze.
- **Rozmycie ruchu:** w Blenderze migawka 180° (0,5), tak jak w kamerze, żeby render felgi miał to samo rozmycie co klipy AI.
- **Ziarno i ostrość:** na końcu jedno wspólne ziarno i lekkie wyostrzenie na całość. Spina to AI, Blendera i nagrania ekranu w jeden materiał.
- **Rozdzielczość:** finał 720p z generatora + Topaz do 1080p. Dla 2–3 najważniejszych ujęć (wyjęcie felgi, CTA) rozważyć finalizację draftu w 1080p.

## Szkic v3 — rytm jak u autorki (ok. 52 s, ok. 20 ujęć, średnio 2,6 s)
| # | Czas | Ujęcie | Źródło |
|---|---|---|---|
| 1 | 0,0–2,4 | najazd nad ramieniem na ekran GT (personalizacja felg) | AI |
| 2 | 2,4–2,8 | szybka panorama | montaż |
| 3 | 2,8–5,8 | Ty z padem: „Nie o takie Turismo nam chodzi.” | AI (lip-sync) |
| 4 | 5,8–6,4 | detal: palce, pstryk | koniec ujęcia 3 |
| 5 | 6,4–7,4 | zmiana świata → wejście do biura | 2 klatki |
| 6 | 7,4–9,0 | detal: dłoń na klamce szklanych drzwi, pchnięcie | AI |
| 7 | 9,0–12,0 | hol, idziesz i mówisz (pierwsza część kwestii) | AI |
| 8 | 12,0–14,0 | felgi na ścianie przesuwają się w płytkiej ostrości (bez ludzi), głos z offu | AI |
| 9 | 14,0–17,4 | „Chodźcie, przedstawię wam…” + gest | AI |
| 10 | 17,4–19,4 | wchodzisz do salonu, siadasz | AI |
| 11 | 19,4–20,4 | detal: dłonie otwierają laptop | AI |
| 12–13 | 20,4–29,4 | ekran: Google → strona → Custom Forged Wheels → C01, z najazdami w montażu | NAGR |
| 14 | 29,4–31,0 | detal: kciuk na rancie obrazu felgi | AI (draft) + BL |
| 15 | 31,0–33,0 | felga wychodzi z ekranu | AI (dłonie) + BL |
| 16 | 33,0–34,4 | styk z rolkami, pchnięcie | BL |
| 17–19 | 34,4–45,0 | gama C01 → C19-R → RR (podmiana w obrocie) + 1 ujęcie Twojej twarzy | BL + AI |
| 20 | 45,0–51,0 | CTA → plansza trzech felg | AI + BL |

Koszt: v3 ma więcej ujęć, ale nie więcej sekund z generatora. Najkrótsza generacja trwa 4 s, więc kilka krótkich ujęć wycinamy z jednej generacji (np. ujęcia 7–9 z jednego klipu z cięciami w prompcie). Szacunek: ok. 36–40 s generacji, **ok. 230–250 kr z 298**. Dokładnie przeliczę, gdy zatwierdzisz strukturę.

## Narracja „krok po kroku”
Transkrypcja otrzymana. Pełna metoda i jej przełożenie na nasz spot: **`05-metoda-kareemy.md`**.
