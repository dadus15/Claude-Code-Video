# Nie o takie Turismo, plan v4 (po uwagach do v1, 23.11)

## Uwagi Daniela do v1 → co zmieniamy
| Uwaga | Rozwiązanie w v4 |
|---|---|
| Hook nie przyciąga uwagi | Nowy hook „Ta felga nie jest z gry” (opis niżej) |
| Brak sceny zmiany koszulki GT → TW | Pstryknięcie → logo na piersi zmienia się w TW → zdejmuje koszulkę, materiał zasłania obiektyw → odsłonięcie w koszulce TW przed biurem (cięcie przez materiał) |
| Hol i sales room mało realistyczne | Nowe plansze lokacji z **Twoich zdjęć biura**, kamera z ręki, naturalne światło dzienne, bez „katalogowego” CGI |
| Przy stronie przestajesz mówić, ciało jest nieruchome | Bez stopklatek. Długie ujęcia przy laptopie (ok. 12 s), cały czas mówisz, piszesz, scrollujesz, klikasz; strona na podzielonym ekranie albo w ekranie laptopa |
| Brak powrotu do listy i wyboru C19-R, potem RR | Nowe nagrania strony: wstecz → lista → C19-R → realizacje → wstecz → RR → realizacje; dopisane kwestie |
| Animacje detali felg nie przykuwają uwagi | Styl z rolki Inventa: spokojne najazdy na prawdziwe zdjęcia, karty i podpisy linią do detalu, PL + EN napisy, logo; mniej efektów, więcej klasy |
| Głos | Lektor reklamowy ElevenLabs (próbki: Mark, Bram, Marcus, Callum) |

## Nowy hook (0–3 s)
1. Kadr 1: ekran z grą, felga auta w trybie zdjęć GT7, napis **„TA FELGA NIE JEST Z GRY.”**
2. Kamera wjeżdża w ekran, piksele się rozpadają, wyjazd na **prawdziwą felgę C01 na BMW M4**, która się kręci, z dźwiękiem uderzenia.
3. Cięcie na kanapę: „Chyba każdy spodziewa się innego Turismo…”

Dlaczego to działa: pierwsza klatka to rzecz znana każdemu fanowi motoryzacji (GT), a od razu łamiemy oczekiwanie (gra → rzeczywistość). Ciekawość zatrzymuje kciuk.

## Scenariusz v4 (ok. 80 s)
| # | Scena | Kwestia (PL) |
|---|---|---|
| 1 | Hook: gra → prawdziwa felga | (napis) Ta felga nie jest z gry. |
| 2 | Kanapa, pad | Chyba każdy spodziewa się innego Turismo… |
| 3 | Pstryk → logo na koszulce → zdjęcie koszulki | To co, zmieniamy Turismo? |
| 4 | Przed biurem, koszulka TW | No, od razu lepiej. |
| 5 | Hol (prawdziwy) | W Turismo Wheels projektujemy felgi kute na indywidualne zamówienie. Chodźcie, pokażę wam naszą gamę. |
| 6 | Sales room → laptop | Wpisujemy turismo-wheels.com, zakładka felgi aluminiowe i felgi kute na zamówienie. |
| 7 | Laptop: lista, C01 | Tu macie całą gamę. Na przykład C01, nasz bestseller: deep concave, agresywne linie i frezowane detale. |
| 8 | Realizacje C01 | Tak wygląda na BMW M4… i na Ferrari F8. |
| 9 | Laptop: wstecz → C19-R | Wracamy do listy… C19-R. Nowsza wersja C19, ze zintegrowanym aero-ringiem. |
| 10 | Realizacje C19-R | Audi RS5. Zobaczcie, jak to siedzi. |
| 11 | Laptop: wstecz → RR | I jeszcze RR. Klasyka do luksusowych limuzyn, z rotacyjnym deklem gravity cap. |
| 12 | Realizacje RR | BMW i7 i Mercedes S Coupé. |
| 13 | Zamknięcie laptopa, CTA | To tylko namiastka tego, co oferujemy. Zapraszam do kontaktu w celu przedstawienia cennika i pozostałych szczegółów realizacji. Zapraszam. Strzała! |
| 14 | Plansza | turismo-wheels.com · +48 501 404 861 · e-mail |

## Koszt (kredyty Higgsfield, szacunek)
| Pozycja | Kredyty |
|---|---|
| Ujęcia Seedance 2.5, 720p, ok. 72 s mówionego wideo × 7 kr/s | ok. 505 |
| Hook (wjazd w ekran → prawdziwa felga) i zmiana koszulki | ok. 60 |
| Plansze lokacji i klatki startowe (Seedream / GPT Image) | ok. 20 |
| Lektor ElevenLabs (wszystkie kwestie) | ok. 5 |
| Muzyka | ok. 13 |
| **Razem** | **ok. 600** |
| Rezerwa na poprawki ujęć | 100–150 |

Saldo: 490,34 kr. Przy tym budżecie zadziała automatyczne doładowanie (+545 kr po spadku poniżej 100).

## Potrzebne materiały
1. Rolka Inventa jako plik MP4: YouTube blokuje pobieranie z tego środowiska.
2. Zdjęcia prawdziwego holu i sales roomu: 5–10 z różnych stron, w świetle dziennym, plus wejście do budynku.
3. Kaye / Red Bull: higgsfield.ai nie otwiera się z tego środowiska. Potrzebne zrzuty ekranu bloga albo sam film.
4. Wybór lektora (A Mark, B Bram, C Marcus, D Callum).

## Klatki kluczowe v4 (23.11, Nano Banana Pro 2k, 8 × 2 kr = 16 kr)
`v4/klatki/` (JPG w repo, PNG lokalnie):

| Klatka | Opis | Job |
|---|---|---|
| K0_hook_gra | ekran TV, felga w grze, widoczne subpiksele | 13210ffe-44fd-406c-94a1-3fdee3f111a9 |
| K1_hook_prawdziwa_C01 | prawdziwa C01 Satin Bronze na BMW M4, ten sam kadr | 37e179d7-4347-461c-b715-0268038318ea |
| K2_zdjecie_koszulki | zdejmowanie koszulki GT w pokoju gracza | c8382172-eddb-4113-bf31-afb3b8163c21 |
| K3_odsloniecie_TW | koszulka TW przed biurem, materiał przy obiektywie | 443a8edb-0237-4e9f-889a-6d6336ce0e4d |
| K4_hol_vossen | hol: rząd felg z gamy, listwa światła, oś czasu, logo | 561cb524-4e65-4ff2-98d1-eea2620af24f |
| K5_hol_sciana_felg | detal ściany felg (insert) | be77a3de-0b76-470f-bf7f-8c82174a710b |
| K6_salon_szeroki | sales room: ściana-galeria, stół konsultacyjny | 8b52c3e2-8184-4665-8708-5f45d617cb9c |
| K7_salon_laptop | plan średni przy laptopie (do ujęć z mową) | 2d60b1e8-4834-47c6-a54e-fb049d3728d4 |
