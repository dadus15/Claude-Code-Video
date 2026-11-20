# „Nie o takie Turismo” — podsumowanie przed produkcją

Stan na 20.11.2026. Wydane kredyty: **0** (saldo Higgsfield: **298,31 kr**, plan Plus).
Szczegóły: `v2/` (scenariusz, prompty, Blender, metoda), wersja v1 w katalogu głównym tylko do wglądu.

## 1. Koncepcja
Grasz w pokoju z assetu, w barwach Turismo. Na ekranie Gran Turismo zmieniasz felgi. „Nie o takie Turismo nam chodzi.” Pstryk, i jesteś przed biurem Turismo Wheels. Prowadzisz widza holem pełnym felg do salonu, na laptopie otwierasz turismo-wheels.com → Custom Forged Wheels i **wyciągasz C01 z ekranu** na podstawkę z rolkami. Felga zmienia się w obrocie w **C19-R**, a potem w **RR**. Finał to CTA i plansza z trzema felgami w miejscu felgi z gry, więc spot się zapętla.
Format: 9:16, 1080 × 1920, ok. **52 s**, klatkaż według generatora (24 kl./s, jeśli taki oddaje).

## 2. Przebieg (v2.3; rytm metody Kareemy: krótkie ujęcia, cięcia w ruchu) — szczegóły przejść: `v2/06-przejscia-i-ruch.md`
| # | Ujęcie | Głos | Źródło |
|---|---|---|---|
| 1 | najazd nad Twoim ramieniem na ekran: GT7, personalizacja felg | dźwięk menu | **G1** + nagranie GT |
| 2 | szybka panorama → Ty z padem | „Nie o takie Turismo nam chodzi.” | **G2** |
| 3 | **PSTRYK 1 = teleport**: ten sam kadr, świat się zmienia → stoisz przed biurem Turismo (nadal w koszulce GT) | — | cięcie na akcji, 2 identyczne klatki |
| 4 | patrzysz na koszulkę, chwytasz materiał | „Coś mi nie pasuje.” | **G3** |
| 5 | **PSTRYK 2 = zmiana koszulki** GT → Turismo (kamera stoi), puszczasz materiał | „Od razu lepiej.” | **G4**, 2 identyczne klatki |
| 6 | drzwi otwierają się do środka → hol pełen felg (idziesz i mówisz) → „Chodźcie…” → skręt do sales roomu | „W Turismo Wheels projektujemy customowe felgi kute na indywidualne zamówienie. Chodźcie, przedstawię wam naszą gamę modelową.” | **G5** (10 s, 3 ujęcia) + Twoje nagranie ruchu |
| 7 | sales room: siadasz na kanapie, otwierasz laptop | — | **G6** + Twoje nagranie ruchu |
| 8 | Google → turismo-wheels.com → Custom Forged Wheels → C01 | „Tutaj znajduje się lista naszych produktów. Weźmy pod lupę na przykład model C01.” | Twoje nagranie ekranu |
| 9 | C01 wychodzi z ekranu (zwolnione tempo) → dwie rolki | cisza | **G7** (packshot jako referencja) + Blender |
| 10 | gama: C01 → C19-R → RR w obrocie (prawdziwe packshoty FRONT) + Twoja twarz | 3 zdania o modelach | packshoty + Blender + **G8** |
| 11 | CTA → plansza z 3 felgami + kontakt | „Rozmiar, ET i wykończenie dobieramy pod Twoje auto. Napisz, czym jeździsz. Strzała!” | **G9** + plansza |

Długość: ok. 60 s.

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

**Generacje wideo (v2.3, 9 klipów, 48 s):**
| Gen. | Długość | 1 draft | Finał 720p | Finał 1080p |
|---|---|---|---|---|
| G1 najazd na ekran | 4 s | 12 | 28 | 64 |
| G2 Ty z padem + pstryk 1 | 5 s | 15 | 35 | 80 |
| G3 przed biurem (GT) | 5 s | 15 | 35 | 80 |
| G4 po pstryku 2 (Turismo) → drzwi | 5 s | 15 | 35 | 80 |
| G5 drzwi + hol + skręt (3 ujęcia) | 10 s | 30 | 70 | 160 |
| G6 sales room: siadanie + laptop | 5 s | 15 | 35 | 80 |
| G7 wyjęcie felgi (slow-mo) | 5 s | 15 | 35 | 80 |
| G8 twarz przy gamie | 4 s | 12 | 28 | 64 |
| G9 CTA | 5 s | 15 | 35 | 80 |
| **Suma** | **48 s** | **144** | **336** | **768** |

**Assety:** 3 karty postaci/produktu × 2,5 + 4 lokacje × 1 + 3 klatki przejść × 2,5 + ok. 50% powtórek ≈ **29 kr**.

**Razem:**
| Scenariusz prób | Finał 720p | 720p + G7 i G9 w 1080p | Wszystko 1080p |
|---|---|---|---|
| optymistyczny (1 draft/klip) | 509 kr (~28 USD) | 599 kr | 941 kr |
| **realistyczny (2 drafty/klip)** | **653 kr (~36 USD)** | **743 kr (~41 USD)** | 1085 kr |
| ostrożny (3 drafty/klip) | 797 kr (~44 USD) | 887 kr | 1229 kr |

Dla porównania: reklama Kareemy kosztowała ~1180 kr.

**Wniosek:** saldo 298 kr nie wystarczy. **Rekomendacja: realistyczny, 720p + 1080p dla wyjęcia felgi i CTA ≈ 743 kr.** Brakuje ok. 445 kr.
- **Pakiet 1000 kr za 55,56 USD** (ważny 90 dni): z zapasem ok. 555 kr na trudniejsze ujęcia, np. hol czy drzwi.
- Pakiet 500 kr za 29,41 USD + automatyczne doładowanie jako bufor: na styk.

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
| Nagranie Twoich kwestii (lip-sync) | G2–G5, G9 |
| Nagranie GT7: personalizacja felg, felga w środkowej 1/3 obrazu | 1 |
| Nagranie ekranu laptopa: Google → turismo-wheels.com → Custom Forged Wheels → C01 | 7 |
| ✅ Koszulka GT pobrana z playstation.com (`v2/referencje_koszulki/`) | karta CS1, G1–G3 |
| Logo Turismo Wheels w wektorze | plansza |
| **Packshoty FRONT** C01 / C19-R / RR z Drive („RENDERY FELG”), załączone w czacie (plików 3D brak, więc gama opiera się na prawdziwych packshotach) | 9–11 |
| **Nagranie Twojego ruchu telefonem**: drzwi → korytarz → siadanie na kanapie, laptop (referencja ruchu dla AI) | G5, G6 |

## 9. Ryzyka
- **Prawa Sony/Polyphony** (gameplay i logo GT) oraz **plakaty z assetu** (Cyberpunk, Back to the Future). Plakaty podmienimy na rendery Turismo w montażu, za 0 kr.
- **Felgi bez plików 3D:** widok z przodu robimy z prawdziwych packshotów (pełna wierność), a ujęcia pod kątem z AI z packshotem jako referencją. Ryzyko drobnych odchyłek wzoru ramion ograniczamy liczbą draftów i ręcznym wyborem najlepszego.
- **Ruch (chód, drzwi, siadanie)** to największe ryzyko realizmu. Minimalizujemy je Twoim nagraniem ruchu jako referencją, cięciami w ruchu i dźwiękiem kroków.
- **Hol z setkami felg (G3)** to najtrudniejsze ujęcie dla AI, więc tam przewiduję najwięcej draftów.
