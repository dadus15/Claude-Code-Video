# Montaż roboczy v1 (23.11.2026), bramka 4: do akceptacji

Plik w repo: `montaz/nie-o-takie-turismo_BF_draft_v1_720p.mp4` (podgląd 720p).
Pełne 1080p, 24 kl./s, -14 LUFS powstaje lokalnie i nie trafia do repo, bo plik ma ok. 800 MB. Skrypt: `../narzedzia/montaz_draft.py`.
Obraz pochodzi z draftów **480p** przeskalowanych do 1080×1920, więc ostrość jest robocza. Rytm, cięcia, dźwięk i napisy są docelowe.

## Oś czasu (67 s)
| Czas | Ujęcie | Źródło (in–out) | Montaż / dźwięk |
|---|---|---|---|
| 0,0–0,8 | HOOK „TO JEST TURISMO” | G1 3,6–4,4 (ekran gry) | boom, fragment dropu muzyki |
| 0,8–1,6 | HOOK „A TO JEST TURISMO” | G7 3,65–4,45 (felga ląduje na rolkach) | boom + stuk felgi |
| 1,6–2,5 | **BLACK FRIDAY · −15% NA KAŻDY PRODUKT** | G7 5,1–6,0 | czerwona belka |
| 2,5–6,2 | najazd na ekran gry | G1 0,9–4,6, lekki dojazd ×1,06 | wejście muzyki, **szarpana panorama** (6 klatek rozmycia) |
| 6,2–9,4 | „Nie o takie Turismo nam chodzi.” → pstryk | G2 1,4–4,6 | cięcie dokładnie na trzasku |
| 9,4–13,0 | **teleport** → „Coś mi nie pasuje.” | G3 0–1,0 + jump-cut 2,3–4,85 (dojazd ×1,12) | swell + uderzenie na cięciu |
| 13,0–17,9 | **zmiana koszulki** → „Od razu lepiej.” → drzwi | G4 0–4,9 | cięcie na trzasku 2 |
| 17,9–27,0 | hol: „W Turismo Wheels projektujemy…”, „Chodźcie…” | G5 0,1–9,2 | wyjście z kadru w prawo |
| 27,0–31,5 | sales room: siadanie, laptop | G6b 0,35–4,95 | — |
| 31,5–37,5 | ekran: turismo-wheels.com → Custom Forged → C01 | nagranie strony (2,6× / 1,25×) | głos z offu (tymczasowy) |
| 37,5–43,5 | **wyjęcie C01 z ekranu** | G7 0–6,0 | muzyka cichnie → **drop** przy wyjęciu (39,0 s) |
| 43,5–54,5 | gama C01 → C19-R → RR | `gama_spin_11s.mp4` (Blender/packshoty) | 3 kwestie z offu, whoosh na podmianach |
| 54,5–58,0 | „Teraz możesz je zamówić z 15% off.” | G8 0–3,6 | **−15%** (pop) + „BLACK FRIDAY · 15% off every wheel” |
| 58,0–63,8 | CTA: „Rozmiar, ET i wykończenie…” | G9 0–5,7 | — |
| 63,8–67,0 | plansza: 3 felgi, −15% · BLACK FRIDAY, „Napisz, czym jeździsz”, telefon, e-mail | render PIL | boom + finałowy akcent muzyki |

Styl Kareemy: krótkie ujęcia, cięcia na akcji i trzasku, natywny dźwięk każdego ujęcia, cisza przed dropem, jedno ziarno, wyostrzenie i winieta na całość.
Napisy TikTok: biały ExtraBold z obrysem, pojawiają się z „wyskokiem”, poza dolnymi 300 px. Etykiety gamy w stylu INVENTA (czerwony kicker, nagłówek, mała linia EN).

## Dźwięk
- **Muzyka:** ElevenLabs Music v2.5, 65 s, instrumentalna, 100 BPM (`klipy/audio/muzyka_draft.mp3`). Wstęp jest zapętlony o 5,3 s, żeby drop trafił w wyjęcie felgi. Muzyka jest automatycznie ściszana pod głosem.
- **Głos na kamerze (G2–G5, G8, G9):** tymczasowy głos Seedance z draftów.
- **Głos z offu (ekran, gama):** tymczasowy klon głosu z G5 (Seed Audio), `klipy/audio/vo06/08/09/10.wav`.
- **Do wersji finalnej:** podmiana na Twoje nagrania z dyktafonu (`08-nagranie-glosu.md`).
- Kwestie gamy skróciłem, żeby zmieściły się w rytmie:
  - „C01. Nasz bestseller, głęboki deep concave.”
  - „C19-R. Zintegrowany aero-ring.”
  - „RR. Klasyka z gravity capem.”
- SFX: swell teleportu i klik (Mirelo). Uderzenia (boom) i whoosh syntetyczne (0 kr).

## Koszt montażu
Muzyka 9,45 + głos tymczasowy 4 × 0,6 + SFX 4 × 0,5 = **13,85 kr**.
Saldo 23.11 po montażu: **629,96 kr**. Automatyczne doładowanie zadziałało (+545 kr).

## Drafty użyte w montażu (do finalizacji przez `draft_job_id`, ważne 7 dni od generacji)
| Klip | job_id | Długość | Uwagi |
|---|---|---|---|
| G1 | 97999749-6515-4f63-84af-32ac780bf460 | 5 s | z tyłu koszulki GT jest nadruk, którego nie powinno być (drobne) |
| G2 | 2361fbd2-f53d-4aec-9b19-78208e3ad09a | 5 s | |
| G3 | f80a5992-aded-4c90-83fe-4778a64fb092 | 5 s | |
| G4 | 5b6a2e75-ad7f-40d9-a95e-a9bd52447765 | 5 s | |
| G5 | feb14f4f-3ba4-4e51-9792-3f7c7a532eff | 10 s | |
| G6b | 5b45a421-c3bb-44e0-a0bb-7924da36a5a5 | 5 s | (G6 4f1125c2… odrzucony: logo Apple) |
| G7 | 2343127b-dd3f-4010-ac87-8e728a4cce9e | 6 s | |
| G8 | 825bf2ac-3330-42ab-94bb-494949ce080f | 5 s | |
| G9 | 27101ec5-2c89-437a-916a-38d0a374fd50 | 6 s | mówi „Na razie!” zamiast „Strzała!” |

## Finalizacja: wycena Higgsfield z 23.11
⚠️ **Korekta kosztorysu.** Wycena finalizacji draftu wynosi **16 kr/s niezależnie od wybranej rozdzielczości**:

| Wybrana rozdzielczość | G2 (5 s) |
|---|---|
| 480p | 80 kr |
| 720p | 80 kr |
| 1080p | 80 kr |
| 4k | 140 kr |

Wcześniej zakładaliśmy 7 kr/s za 720p, ale ta stawka dotyczy tylko nowej generacji, a nowa generacja daje inne ujęcie. Skoro finalizacja i tak kosztuje tyle co 1080p, **finalizujemy w 1080p**.

| Wariant | Co | Koszt |
|---|---|---|
| A | finalizacja wszystkich 9 ujęć (52 s) w 1080p | **832 kr** |
| B | finalizacja ujęć „produktowych” i z twarzą na zbliżeniu: G2, G4, G5, G7, G8, G9 (36 s); reszta przez upscale | 576 kr + upscale (wyceniany dopiero przy zleceniu) |
| C | tylko upscale draftów (Topaz / ByteDance) | najtaniej, ale 480p → 1080p nie dorysuje detali felg i twarzy |

Rekomenduję **A**. Felgi (G7) i twarz w zbliżeniu (G8, G9) muszą być ostre, a pozostałe ujęcia też są na pełnym ekranie.
Saldo 630 kr nie wystarczy na A. Automatyczne doładowanie dorzuci 545 kr, gdy saldo spadnie poniżej 100.
