# Budżet Higgsfield i bramki akceptacji

Saldo w chwili planowania: **298,31 kr** (plan Plus). Wszystkie stawki poniżej to wyceny z Higgsfield dla 9:16 bez dźwięku. Wycena była bezpłatna i niczego nie zleciła.

## Stawki (sprawdzone)
| Model | Ustawienie | Koszt |
|---|---|---|
| `gpt_image_2_6` (klatki) | low 1k / **medium 1k** / high 1k / high 2k | 0,25 / **0,5** / 1,5 / 2,75 kr za obraz |
| `seedance_2_0_mini` | 480p / 720p | 2 / 4 kr za 4 s (0,5 / 1 kr/s) |
| `seedance_2_0` std | 720p / 1080p | 18 / 48 kr za 4 s (**4,5** / 12 kr/s) |
| `seedance_2_5` | **draft 480p** / 720p / 1080p | 12 / 28 / 64 kr za 4 s (**3** / 7 / 16 kr/s) |

Kluczowa funkcja: `seedance_2_5` ma tryb **draft**. Najpierw płacisz za tani podgląd 480p. Po Twojej akceptacji **ta sama generacja** jest finalizowana w wyższej rozdzielczości, do 7 dni. Czyli płacisz pełną cenę tylko za wersję, którą już widziałeś i zatwierdziłeś. To dokładnie Twoja zasada płatności.

1080p z Seedance jest za drogie dla tego salda (31 s × 16 kr = ~500 kr). Finał renderujemy w 720p. Do 1080 × 1920 skalujemy lokalnie za 0 kr albo przez Topaz w Higgsfield, po teście jednego ujęcia (tego narzędzia nie da się wycenić z góry).

## Sekundy z generatora
A 5 s · B 5 s · C 4 s · D 4 s · E 4 s · F 4 s · H 5 s = **31 s**.
Za 0 kr: gameplay (0–1,6 s), @WEB (17–19 s), G (3D, 26–34 s), plansza końcowa (38,8–40 s), okno detalu, podmiana 2D→3D, wszystkie grafiki.

## Rekomendacja: wariant HYBRYDA

| Bramka | Co | Wyliczenie | Kredyty |
|---|---|---|---|
| **0 — teraz** | storyboard, makiety C i E–F, animatik, wszystkie prompty | lokalnie | **0** |
| 1 | lokacje: G1, O1, O2, O3 | 4 × 0,5 | 2 |
| 2 | kontaktówka: A0, A9, B0, C1, C2, D9, K1–K4, H0 | 11 × 0,5 | 5,5 |
| — | rezerwa na poprawki klatek (~50%) | | 4 |
| 3a | test ruchu A, B, D, H (blocking, gesty, tempo) — `seedance_2_0_mini` 480p | 19 s × 0,5 | 9,5 |
| 3b | **drafty efektów C, E, F** — `seedance_2_5` draft | 3 × 12 | 36 |
| **4 — finał, tylko po Twoim „akcept”** | C, E, F: finalize zaakceptowanych draftów 720p | ~3 × 28 | ~84 |
| | A, B, D, H: `seedance_2_0` std 720p z zatwierdzonych klatek | 85,5 | 85,5 |
| **Razem** | | | **~226,5** |
| Rezerwa | np. 2 powtórki draftu (24) + 1 powtórka std (22,5) | | ~72 |

Dlaczego hybryda: ujęcia z efektem (C, E, F) muszą być dokładnie tym, co zatwierdzisz, więc idą przez draft i finalize. W ujęciach z dialogiem (A, B, D, H) kompozycję trzymają zatwierdzone klatki start/koniec, a test mini pokazuje gest i tempo. Finał może się różnić tylko drobnym ruchem.

## Alternatywy
| Wariant | Opis | Kredyty | Uwagi |
|---|---|---|---|
| PEŁNA ZGODNOŚĆ | wszystkie 31 s przez draft → finalize 720p | 93 + 217 + 11,5 = **~321** | każde ujęcie płacone dopiero po akceptacji; **przekracza saldo**, wymaga doładowania |
| OSZCZĘDNY | wszystko `seedance_2_0` std 720p po testach mini | 139,5 + 15,5 + 11,5 = **~167** | najtaniej, ale finał C/E/F to nowa generacja, inna niż test |

## Zasady wydawania (stałe)
1. Przed każdą bramką podaję dokładną wycenę i czekam na Twoje „OK”. Nic nie generuję bez akceptacji.
2. Jedna zmiana naraz. Jeśli test nie wyjdzie, poprawiam prompt lub klatkę, a nie rozdzielczość.
3. Finalizujemy tylko drafty z Twoim wyraźnym „akcept”.
4. Lip-sync (audio_references) może zmienić stawkę. Wycenię go po wgraniu Twoich nagrań, przed bramką 4.
5. Publikacja na TikToku tylko po Twojej wyraźnej zgodzie.
