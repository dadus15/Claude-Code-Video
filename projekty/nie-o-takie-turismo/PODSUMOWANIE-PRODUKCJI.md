# „Nie o takie Turismo” — podsumowanie przed produkcją

Stan na 20.11.2026. Wydane kredyty: **0** (saldo Higgsfield: **298,31 kr**, plan Plus).
Szczegóły: `v2/` (scenariusz, prompty, Blender, metoda), wersja v1 w katalogu głównym tylko do wglądu.

## 1. Koncepcja
Grasz w pokoju z assetu, w barwach Turismo. Na ekranie Gran Turismo zmieniasz felgi. „Nie o takie Turismo nam chodzi.” Pstryk, i jesteś przed biurem Turismo Wheels. Prowadzisz widza holem pełnym felg do salonu, na laptopie otwierasz turismo-wheels.com → Custom Forged Wheels i **wyciągasz C01 z ekranu** na podstawkę z rolkami. Felga zmienia się w obrocie w **C19-R**, a potem w **RR**. Finał to CTA i plansza z trzema felgami w miejscu felgi z gry, więc spot się zapętla.
Format: 9:16, 1080 × 1920, ok. **52 s**, klatkaż według generatora (24 kl./s, jeśli taki oddaje).

## 2. Przebieg (rytm według metody Kareemy: krótkie ujęcia, cięcia w ruchu)
| # | Czas (s) | Ujęcie | Głos | Źródło |
|---|---|---|---|---|
| 1 | 0,0–2,4 | najazd nad Twoim ramieniem na ekran: GT7, personalizacja felg | dźwięk menu | **G1** (AI) + nagranie GT |
| 2 | 2,4–2,8 | szybka panorama na Ciebie | świst | montaż |
| 3 | 2,8–6,4 | Ty z padem na kanapie, potem pstryk | „Nie o takie Turismo nam chodzi.” | **G2** (AI, lip-sync) |
| 4 | 6,4–7,4 | świat zmienia się wokół Ciebie → wejście do biura | — | 2 klatki + cięcie |
| 5 | 7,4–17,4 | dłoń na klamce → hol z felgami (idziesz i mówisz) → felgi przesuwają się w tle → „Chodźcie…” | „W Turismo Wheels projektujemy customowe felgi kute na indywidualne zamówienie. Chodźcie, przedstawię wam naszą gamę modelową.” | **G3** (AI, 10 s, 3 ujęcia) |
| 6 | 17,4–20,4 | salon: siadasz, dłonie otwierają laptop | — | **G4** (AI) |
| 7 | 20,4–29,4 | Google → turismo-wheels.com → Custom Forged Wheels → C01 | „Tutaj znajduje się lista naszych produktów. Weźmy pod lupę na przykład model C01.” | Twoje nagranie ekranu |
| 8 | 29,4–34,4 | kciuk na rancie obrazu → C01 wychodzi z ekranu (zwolnione tempo) → ląduje na dwóch rolkach | cisza | **G5** (AI, dłonie) + Blender |
| 9 | 34,4–45,0 | gama: C01 → podmiana w obrocie → C19-R → RR, plus 1 ujęcie Twojej twarzy | „C01 — nasz bestseller. Wyjątkowo głęboki deep concave i frezowane detale.” · „C19-R ma zintegrowany aero-ring: lepsza aerodynamika i jeszcze więcej charakteru.” · „A RR to klasyka: minimalizm i obrotowy dekiel gravity cap.” | Blender + **G6** (AI) |
| 10 | 45,0–52,0 | CTA do kamery → plansza: 3 felgi + kontakt (tel., e-mail) | „Rozmiar, ET i wykończenie dobieramy pod Twoje auto. Napisz, czym jeździsz. Strzała!” | **G7** (AI) + Blender |

## 3. Metoda (Kareema / kaye.creatives, „Step-by-Step”)
1. **Karty postaci** (Seedream 5.0 Pro, 2k): Ty w koszulce GT z padem, Ty w koszulce Turismo, podstawka z rolkami. Bazą jest zatwierdzona `Postac-FINAL.png`.
2. **Karty lokacji** (Soul Cinema, 2k, 4 widoki każda): pokój gier (z assetu, w barwach Turismo), wejście do biura, hol z felgami, salon z laptopem.
3. **Sceny** (Seedance 2.5): **draft 480p**, kilka prób, aż wyjdzie „złote ujęcie”, potem **ten sam take** w wyższej jakości. Prompty piszę z Twojego skilla Cinedance (to narzędzie Kareemy). Zamiast jej szkiców używam klatek previs z Blendera. Dla ujęć statycznych dopisek „camera does not move”, obiektyw w mm, przy ujęciach z ręki nazwisko operatora.
4. **Blender** (0 kr): felgi C01 / C19-R / RR, podstawka, wyjęcie z ekranu, styk na dwóch rolkach (rolki kręcą się przeciwnie), podmiana modeli w szczycie obrotów, gravity cap RR nieruchomy, plansza końcowa.
5. **Montaż**: cięcia w ruchu, każde ujęcie ze swoim dźwiękiem, jedna kolorystyka i wspólne ziarno dla AI, Blendera i nagrań ekranu, napisy PL z linią EN w stylu INVENTA.

## 4. Co jest gotowe (0 kr)
- Storyboard v1, scenariusz v2.2, prompty klatek i ruchu (EN), lekcje z tutorialu i opis metody.
- Pokój z assetu w barwach Turismo, previs sceny 1 (najazd → panorama → Ty z padem), animatik v1.
- Blender: scena parametryczna (wyjęcie, rolki, podmiana C01 → C19-R → RR, gravity cap), trzy modele felg według packshotów z turismo-wheels.com, podglądy.
- Fakty z kart produktów (C01, C19-R, RR) i packshoty w `v2/referencje_felg/`.
- Dostęp sesji do turismo-wheels.com (środowisko „Claude-Code-Video”).

## 5. Kosztorys pełnej produkcji (wyceny Higgsfield z 20.11.2026)
Stawki: Seedance 2.5 **draft 3 kr/s**, finalizacja **720p 7 kr/s**, **1080p 16 kr/s**; Seedream 5.0 Pro 2,5 kr; Soul Cinema 1 kr (dokładnie 0,12 kr).
Finalizacja draftu kosztuje tyle co render w tej rozdzielczości: 720p 4 s = 28 kr, 5 s = 35 kr, 10 s = 70 kr.

**Generacje wideo (pełny wariant A, 38 s):**
| Gen. | Długość | 1 draft | Finał 720p | Finał 1080p |
|---|---|---|---|---|
| G1 najazd na ekran | 4 s | 12 | 28 | 64 |
| G2 Ty z padem + pstryk | 5 s | 15 | 35 | 80 |
| G3 drzwi + hol (3 ujęcia) | 10 s | 30 | 70 | 160 |
| G4 salon + laptop | 5 s | 15 | 35 | 80 |
| G5 wyjęcie felgi (slow-mo) | 5 s | 15 | 35 | 80 |
| G6 twarz przy gamie | 4 s | 12 | 28 | 64 |
| G7 CTA | 5 s | 15 | 35 | 80 |
| **Suma** | **38 s** | **114** | **266** | **608** |

**Assety:** 3 karty × 2,5 + 4 lokacje × 1 + 2 klatki przejścia × 2,5 + ok. 50% powtórek ≈ **25 kr**.

**Razem:**
| Scenariusz prób | Finał 720p | 720p + G5 i G7 w 1080p | Wszystko 1080p |
|---|---|---|---|
| optymistyczny (1 draft/ujęcie) | **405 kr** (~22 USD) | 495 kr | 747 kr |
| **realistyczny (2 drafty/ujęcie)** | **519 kr** (~29 USD) | **609 kr** (~34 USD) | 861 kr |
| ostrożny (3 drafty/ujęcie) | **633 kr** (~35 USD) | 723 kr | 975 kr |

Wariant B (skrócony, 27 s AI, bez G4 i G6): realistycznie **376 kr**, czyli też ponad saldo.
Dla porównania: reklama Kareemy kosztowała ~1180 kr.

**Wniosek:** obecne saldo 298 kr nie wystarczy na pełną produkcję w żadnym realistycznym scenariuszu.
- **Rekomendacja: wariant A, realistyczny, 720p + 1080p dla dwóch kluczowych ujęć (wyjęcie felgi i CTA) ≈ 609 kr.** Brakuje ok. 311 kr, więc najlepiej pasuje pakiet **500 kr za 29,41 USD** (ważny 90 dni). Daje to ok. 190 kr zapasu na dodatkowe próby.
- Pozostałe pakiety: 1000 kr = 55,56 USD, 2000 kr = 105,26 USD.

Poza kredytami (0 zł): Blender, montaż, nagrania ekranu i gry. Do decyzji: muzyka z biblioteki TikToka (darmowa w aplikacji) albo Epidemic Sound (subskrypcja, konektor wymaga autoryzacji). Nie wyceniłem z góry: Topaz upscale (bez wyceny wstępnej) i ewentualny wpływ lip-syncu na cenę. Wycenię je przy pierwszym użyciu.

## 6. ⚠️ Automatyczne doładowanie
Na Twoim koncie Higgsfield jest **włączone automatyczne doładowanie**: przy saldzie poniżej **100 kr** system sam pobierze **30 USD (545 kr)**. Przy tej produkcji saldo na pewno spadnie poniżej 100. Jeśli chcesz płacić tylko świadomie, wyłącz je w ustawieniach Higgsfield przed startem albo potraktuj je jako zaplanowane doładowanie.

## 7. Bramki akceptacji (nic bez Twojego „OK”)
| Bramka | Co | Koszt |
|---|---|---|
| 1 | karty postaci + karty lokacji | ~25 kr |
| 2 | drafty G1–G7 (pierwsza partia), wybór złotych ujęć | ~114 kr na partię |
| 3 | finalizacja zaakceptowanych ujęć | 266–608 kr zależnie od rozdzielczości |
| 4 | montaż, dźwięk, napisy → wersja do akceptacji | 0 kr |
| 5 | publikacja na TikToku | tylko na Twoje wyraźne polecenie |

## 8. Od Ciebie przed bramką 2
| Materiał | Do ujęcia |
|---|---|
| Nagranie Twoich kwestii (lip-sync) | G2, G3, G7 |
| Nagranie GT7: personalizacja felg, felga w środkowej 1/3 obrazu | 1 |
| Nagranie ekranu laptopa: Google → turismo-wheels.com → Custom Forged Wheels → C01 | 7 |
| Zdjęcie przodu koszulki GT (albo decyzja: koszulka bez logo) | karta CS1, G1, G2 |
| Logo Turismo Wheels w wektorze | plansza |
| (najlepiej) pliki 3D C01 / C19-R / RR od producenta | Blender, ujęcia 8–10 |

## 9. Ryzyka
- **Prawa Sony/Polyphony** (gameplay i logo GT) oraz **plakaty z assetu** (Cyberpunk, Back to the Future). Plakaty podmienimy na rendery Turismo w montażu, za 0 kr.
- **Jakość felg w Blenderze** bez plików 3D od producenta: modele proceduralne wystarczą do ruchu, ale nie do zbliżeń. Bez CAD zbliżenia oprzemy na packshotach i referencjach w AI.
- **Hol z setkami felg (G3)** to najtrudniejsze ujęcie dla AI, więc tam przewiduję najwięcej draftów.
