# Turismo Wheels | „Nie o takie Turismo” — produkcja

> **Podsumowanie i kosztorys: [`PODSUMOWANIE-PRODUKCJI.md`](PODSUMOWANIE-PRODUKCJI.md)** · **Aktualny przebieg: [`v2/README-v2.md`](v2/README-v2.md)** (pokój z assetu, pstryk → biuro, hol, laptop, C01 w Blenderze). Poniżej v1 — zostają z niej karta postaci, bloki Cinedance i mechanika podmiany pod kciukiem.

Spot 9:16, 40 s, 1080 × 1920, 25 kl./s. Bohater produktowy (założenie robocze): **Turismo Forged C19-R, Gloss Silver**.

## Stan (20.11.2026)
| Kategoria | Co jest |
|---|---|
| 🟩 Gotowe klipy | **brak** — nie wydano ani jednego kredytu |
| 🟨 Prompty gotowe | wszystkie klatki kluczowe (17) i wszystkie ujęcia ruchu A–H |
| 🟥 Plan kompozycji | storyboard A–H, makieta znaku dla C, 4 klatki E–F z osią czasu, animatik 40 s |

## Pliki
| Plik | Zawartość |
|---|---|
| `01-storyboard.md` | A–H: pliki referencyjne, pierwsza/ostatnia klatka, akcja, kamera, dialog, dźwięk, braki |
| `02-prompty-klatek.md` | prompty obrazów (EN) + blok `HERO LOCK` zastępujący FACE/BODY z Cinedance |
| `03-prompty-ruchu.md` | prompty wideo (EN) złożone z bloków Cinedance, ustawienia generatora per klip |
| `04-proby-C-i-EF.md` | pierwsze próby: zmiana koszulki i felga z ekranu na rolki, klatka po klatce |
| `05-VO-montaz-dzwiek.md` | czysty tekst VO, EDL z klatkami, napisy, dźwięk, checklista odbioru |
| `06-budzet-higgsfield.md` | stawki, bramki akceptacji, warianty kosztowe |
| `storyboard/00_storyboard_A-H.png` | kontaktówka: pierwsza i ostatnia klatka każdego ujęcia |
| `storyboard/01_E-F_4_klatki_os_czasu.png` | K1–K4 + oś czasu 19–26 s (moment kciuka) |
| `storyboard/02_C_makieta_znaku.png` | znak z @TWdetail na zatwierdzonej karcie — pozycja i skala |
| `storyboard/03_animatik_40s.mp4` | próba montażowa z plansz z rozpisanymi kwestiami (bez dźwięku) |
| `narzedzia/` | skrypty, które generują plansze i animatik (PIL + ffmpeg) |

Referencje z pakietu (`Referencje/…`) nie są w repo. Nazwy plików w dokumentach odpowiadają ZIP-owi `Turismo-Wheels-Claude.zip`.

## Brakujące materiały („do podmiany”)
| # | Materiał | Blokuje | Stan |
|---|---|---|---|
| 1 | **Packshot C19-R Gloss Silver** (przód, najlepiej też 3/4) | K1–K4, E, F, H | Na Drive są tylko rendery na autach: `AUDI-RS5-8W-C19-R-NEODYME_00x`, `BMW-M8-GC-C19-R-NEODYME_00x`, `FERRARI-ITALIA-C19-R-B-R-GD_00x`, `VW-PASSAT-B9-C19-R-…`. Nie ma Gloss Silver ani osobnego packshotu |
| 2 | **Model 3D C19-R** (OBJ/FBX/GLB/STEP z konfiguratora) lub nagranie obrotu egzemplarza | G w całości, okno detalu, warstwa 3D w E–F, plansza końcowa | Rendery na Drive powstały z CAD, więc model istnieje — zapytaj Turismo |
| 3 | **@WEB** — nagranie ekranu turismo-wheels.com (strona główna → Turismo Forged → kilka modeli → karta C19-R Gloss Silver) | D, ekran w E | brak; ta sesja nie ma dostępu sieciowego do turismo-wheels.com |
| 4 | **@GT** — przód koszulki GT 25-lecie | KF-G1, A, B, C1 | brak; playstation.com zablokowane w tej sesji |
| 5 | **Gameplay GT** 0–1,6 s (koło auta wypełnia pion, nagranie z konsoli) | A | brak |
| 6 | **Logo Turismo Wheels** (wektor) | plansza końcowa | na Drive nie znalazłem; awaryjnie plansza tekstowa |
| 7 | **Twoje nagranie kwestii** (próba) | lip-sync A, B, C, H; blokada montażu | brak |
| 8 | Zdjęcie prawdziwego biura (opcjonalnie) | podmiana @OFFICE | brak — generujemy O1–O3 |

## Decyzje do akceptacji
1. Wariant budżetu — rekomenduję **HYBRYDĘ** (~227 kr z 298, rezerwa ~72).
2. Biuro: kamera „zza ramienia” z boku kanapy, bo kanapa stoi pod ścianą. Felgi na ścianie ciemne, żeby srebrna C19-R była jedynym jasnym srebrem w kadrze.
3. Napisy: nagłówki PL + mała linia EN w stylu INVENTA, co godzi brief z zasadą profilu „napisy po angielsku”.
4. Głos: Twój własny, nie lektor TTS, bo prowadzący mówi do kamery jako Ty.

## Ryzyko: prawa do Gran Turismo
Logo Gran Turismo na koszulce i gameplay z GT to znaki i treści Sony/Polyphony Digital. W materiale reklamowym, zwłaszcza płatnie promowanym, wymagają zgody właściciela praw. TikTok może też zablokować rolkę za cudze treści. Bezpieczniejszy wariant zachowuje żart: koszulka i gra bez logo, a cały gag niesie kwestia „Chyba nie o takie Turismo…”. Decyzja należy do Ciebie, prompty działają w obu wariantach (podmiana @GT).
