# „Nie o takie Turismo” — wersja 2.1 (Twój przebieg)

Zmiany względem v1:
- Start w **pokoju z assetu** (zmienione tylko barwy).
- Pstryk przenosi Cię **przed biuro**. Potem wejście, hol z felgami i drugi pokój z laptopem.
- Na laptopie: Google → turismo-wheels.com → Custom Forged Wheels.
- Felgami zajmuje się **Blender**.

Zmiany v2.1:
- **Scena 1** to jeden ruch kamery: najazd na ekran GT, a potem szybka panorama na Ciebie z padem na kanapie.
- **Gama trzech modeli: C01 → C19-R → RR.**

Format: 9:16, 1080 × 1920, 25 kl./s, ok. **54 s**.
Źródła: **AI** = generator (płatny), **BL** = Blender (0 kr), **NAGR** = Twoje nagranie, **2.5D** = ruch kamery po kadrze w montażu (0 kr).

| # | Czas (s) | Obraz | Głos | Źródło |
|---|---|---|---|---|
| S1a | 0,0–3,4 | Pokój z assetu w barwach Turismo. Kamera startuje **nad Twoim ramieniem**: siedzisz tyłem, pad w dłoniach. Powoli najeżdża na duży ekran z GT7 (personalizacja auta, wybór felg), a Twoja głowa wychodzi dołem kadru | dźwięk menu gry, klik wyboru felgi | AI 4 s (wariant A) |
| S1b | 3,4–3,8 | **Szybka panorama** z ekranu na Ciebie, 10 kl. rozmycia. W rozmyciu jest ukryte cięcie | świst panoramy | montaż, 0 kr |
| S1c | 3,8–7,6 | Ty z przodu na kanapie, **pad w dłoniach**. Wzrok z ekranu przechodzi w obiektyw. Kwestia. Odkładasz pad, unosisz prawą dłoń | 4,4–6,4 „Nie o takie Turismo nam chodzi.” | AI 5 s (start w rozmyciu ruchu) |
| U3 | 7,6–9,6 | **PSTRYK** → przejście w stylu tutorialu: stoisz w tym samym miejscu kadru, a świat wokół się zmienia (pokój → wejście do biura). Kamera odjeżdża | — | 2 klatki AI + cięcie |
| U4a | 9,6–12,0 | Otwierasz szklane drzwi i wchodzisz | — | AI 4 s |
| U4b | 12,0–19,0 | Hol pełen felg, idziesz do kamery | 12,4–16,6 „W Turismo Wheels projektujemy customowe felgi kute na indywidualne zamówienie.” · 16,9–18,8 „Chodźcie, przedstawię wam naszą gamę modelową.” | AI 7 s |
| U5 | 19,0–22,5 | Salon: siadasz, otwierasz laptop | — | AI 4 s |
| U6 | 22,5–29,5 | Google → `turismo-wheels.com` → **Custom Forged Wheels** → lista (C01, C19-R i RR widoczne na liście) | 25,8–27,8 „Tutaj znajduje się lista naszych produktów.” | NAGR ekranu |
| U7 | 29,5–31,5 | Klik w C01 → karta C01 | 29,6–31,4 „Weźmy pod lupę na przykład model C01.” | NAGR ekranu |
| U8 | 31,5–36,0 | C01 wychodzi z ekranu i ląduje na dwóch rolkach, pchnięcie, obrót | cisza od kontaktu kciuka do 35,0 | AI 5 s (dłonie) + BL |
| **U9** | 36,0–46,5 | **Gama na podstawce** (zbliżenie BL): C01 się kręci → „dopchnięcie”, obroty rosną do ok. 5 obr./s, model zamienia się w rozmyciu, zwalnia jako **C19-R** → ponownie podmiana na **RR**. Każdy model ma etykietę PL/EN w stylu INVENTA | 36,2–38,8 „C01 — nasz bestseller. Wyjątkowo głęboki deep concave i frezowane detale.” · 39,8–42,4 „C19-R ma zintegrowany aero-ring: lepsza aerodynamika i jeszcze więcej charakteru.” · 43,4–46,0 „A RR to klasyka: minimalizm i obrotowy dekiel gravity cap.” | BL (0 kr) |
| U10 | 46,5–54,0 | CTA do kamery (obok kręci się RR), potem plansza: **trzy felgi obok siebie**, środkowa w miejscu i rozmiarze felgi z gry (pętla) + kontakt | „Rozmiar, ET i wykończenie dobieramy pod Twoje auto. Napisz, czym jeździsz. Strzała!” | AI 4 s + BL |

## Scena 1 — trzy sposoby realizacji
Podgląd ruchu: `plansze/S1_previs_ekran-pan-kanapa.mp4`. To szkic z pokoju z assetu i Twojej karty, nie render.

| Wariant | Jak | Kredyty | Ocena |
|---|---|---|---|
| **A (rekomendowany)** | S1a i S1c jako dwa klipy AI, łączone panoramą z rozmyciem | 18 + 22,5 = **40,5** | prawdziwa paralaksa nad ramieniem, ukryte cięcie jest pewne |
| B (oszczędny) | S1a jako najazd 2.5D po jednej wygenerowanej klatce (Ty tyłem) + S1c AI | 0,5 + 22,5 = **23** | brak paralaksy przy Twojej głowie; przy wolnym najeździe i szybkim wyjściu głowy z kadru jest akceptowalny |
| C | jedno ujęcie AI 8–9 s z obrotem kamery o 180° | ok. **40** | najładniejsze w teorii, ale największe ryzyko, że twarz i pokój „popłyną” w trakcie obrotu; odradzam |

Rozmycie panoramy ukrywa cięcie tylko wtedy, gdy oba klipy mają ruch w tym samym kierunku. S1a kończy się ruchem kamery w prawo, a S1c zaczyna się w ruchu w prawo i hamuje na Tobie. Jest to zapisane w promptach.

## Gama C01 → C19-R → RR (U9)
- Podmiana w szczycie obrotów to trik w Blenderze, nie w AI. Przy 5 obr./s i 25 kl./s ramiona zlewają się w dysk, więc w klatce podmiany (kl. 245 i 320 w scenie) zamiany modelu nie widać. Podgląd: `plansze/BL_podmiana_modeli.mp4`.
- Ta sama podstawka, światło i kierunek obrotu, więc pokaz trzech modeli trwa tylko ok. 10 s i nie kosztuje kredytów.
- Wymowa: „ce zero jeden”, „ce dziewiętnaście er”, „er er”.
- ✅ Wyjaśnione: **C19-R ≠ C19.** C19-R to nowsza wersja C19 z zintegrowanym aero-ringiem (karta produktu). Packshoty z turismo-wheels.com są w `referencje_felg/`.
- ✅ Cechy z kart produktów (turismo-wheels.com):
  - **C01**: wyjątkowo głęboki „deep concave”, agresywne linie, frezowane detale; bestseller; 6061, monoblok lub 2-/3-częściowa; wykończenia Brushed Deep Black / Brushed Grey / Satin Black.
  - **C19-R**: najnowsza wersja C19 z **zintegrowanym aero-ringiem** (aerodynamika + wygląd), ostro zarysowane ramiona i głębia; wykończenia Gloss Silver / Neodyme.
  - **RR**: klasyczny, minimalistyczny wzór CNC z 6061, do luksusowych limuzyn, **obrotowy dekiel gravity cap**; zalecane wykończenie szczotkowane ręcznie.
- Zapis fonetyczny do lektora: „dip konkejw”, „grawiti kap”.
- Etykiety PL/EN: C01 „Deep concave” / „Deep concave” · C19-R „Zintegrowany aero-ring” / „Integrated aero-ring” · RR „Gravity cap” / „Floating centre cap”.

## Przejście z tutorialu (U3)
Bez zmian (wariant A, ok. 1 kr). Jeśli w filmie chodzi o inny moment, podaj minutę i sekundę.

## Kwestie
- Scena 1: „Nie o takie Turismo nam chodzi.” — tak jak napisałeś. Wcześniejsze „Chyba nie o takie Turismo nam chodzi” zostaje jako wariant do nagrania.
- CTA w liczbie pojedynczej („Napisz…”). Alternatywa: „Napiszcie, czym jeździcie”.
