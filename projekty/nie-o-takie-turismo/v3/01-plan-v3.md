# „Nie o takie Turismo” v3: plan po uwagach z 23.11

Źródła stylu: skille Kareemy **talking-head-reels** (montaż) i **voiceover-glass-reel** (generacje Higgsfield, SFX, muzyka) oraz jej metoda z tutorialu (karty postaci i lokacji, drafty Seedance).

## 1. Twoje uwagi → co zmieniamy
| # | Uwaga | Przyczyna | Rozwiązanie v3 |
|---|---|---|---|
| 1 | Dialog niewyraźny | Głos tymczasowy Seedance z draftów 480p (słaba jakość i pogłos), a muzyka i SFX dodatkowo go zasłaniały | **Twój głos z dyktafonu jest zegarem montażu** (zasada Kareemy). Mastering -14 LUFS / -1,5 dBTP, odszumienie i EQ. Ujęcia generujemy z Twoim nagraniem jako `audio_references`, więc usta mówią Twoim głosem. Muzyka nisko (-20 dB) albo wcale |
| 2 | Montaż zbyt prosty | Wersja v1 była składana prostym skryptem | Pełny styl **talking-head-reels**: co 2–4 s zmiana kadru (punch-in, duże słowo, insert, split); typografia Anton + Didot + napisy słowo po słowie; inserty czarno-białe z czerwonym akcentem #ED3B22 (barwy Turismo); przejścia whip / zoom / bulge, błysk negatywu; halftone, winieta, ziarno. Renderer Kareemy przenoszę z macOS na tę maszynę |
| 3 | Konsola „no name”, gra nie GT | AI nie rysuje marek | **Prawdziwe PS5 i prawdziwe Gran Turismo**: Twoje zdjęcie PS5 (albo oficjalne zdjęcie produktu z playstation.com) jako referencja oraz **Twoje nagranie GT7 z konsoli** wklejone w ekran. Najazd kończy się wejściem w ekran |
| 4 | Efektowne przejście na pstryk + transformacja logo | — | **Pstryk → logo GT zrywa się z koszulki → rozpada na czerwone odłamki → składa w logo Turismo Wheels → logo leci w kamerę i przez jego wnętrze widać biuro** (opis w p. 4). Robione w kodzie, piksel w piksel, bez zgadywania AI |
| 5 | Biuro sztuczne | Biuro było wymyślone przez AI, bez referencji | Karty lokacji z **prawdziwych zdjęć biura**, oświetlenie i optyka jak z kamery, mniej felg i rekwizytów |
| 6 | Bez rolek: scena przy laptopie | — | Nowy blok przy laptopie (p. 3). Montaż pokazuje to, o czym mówisz: wskazania na feldze, przybliżenia, kafelek modelu i realizacje |
| 7 | Za bardzo umięśniony | Karta postaci + obcisła koszulka | Nowa karta postaci: szczupła, przeciętna sylwetka, koszulka regular fit. Najlepiej z Twoim aktualnym zdjęciem całej sylwetki jako referencją |

## 2. Tekst do nagrania (v3.1: opisy modeli z polskiej wersji turismo-wheels.com)
Zasady nagrania jak w `../v2/08-nagranie-glosu.md`: każda kwestia osobno, 3 podejścia, WAV/48 kHz, 15–20 cm od ust, 10 s ciszy na końcu.

| # | Kwestia | Gdzie |
|---|---|---|
| 01 | „Nie o takie Turismo nam chodzi.” | kanapa, pad (pstryk zaraz po) |
| 02 | „Od razu lepiej.” | przed biurem, po transformacji logo |
| 03 | „W Turismo Wheels projektujemy felgi kute na indywidualne zamówienie.” | hol |
| 04 | „Chodźcie, przedstawię wam naszą gamę.” | hol → salon |
| 05 | „Otwieramy przeglądarkę i wpisujemy turismo-wheels.com.” | laptop |
| 06 | „Wybieramy zakładkę Felgi aluminiowe… i Felgi kute na zamówienie.” | laptop. Nazwy zakładek mówisz po polsku (PL wersja strony) albo po angielsku: „Aluminum wheels… Custom forged wheels”. Wybierz jedną wersję |
| 07 | „Co my tu mamy? Na przykład nasz unikatowy bestseller: C01.” | laptop (klik) |
| 08 | „Wyjątkowo głęboki deep concave i agresywne linie z charakterystycznymi frezowanymi detalami.” | C01 (strona: „Wyjątkowo głęboki deep concave i agresywne linie z charakterystycznymi frezowanymi detalami…”) |
| 09 | „Kute aluminium 6061: większa wytrzymałość i mniejsza masa niż w felgach odlewanych.” | C01 (strona: „zwiększona wytrzymałość przy jednoczesnej redukcji masy felgi”) |
| 10 | „Tak wygląda na BMW M4 i na Ferrari F8.” | C01, realizacje (Twoje zdjęcia: BMW M4 G83 Satin Bronze, Ferrari F8 Gloss Black) |
| 11 | „C19-R to kolejna odsłona naszego popularnego wzoru C19, wzbogacona o zintegrowany aero-ring.” | C19-R (strona) |
| 12 | „Poprawia aerodynamikę, a wyraźnie zarysowane ramiona dają jej głębię i sportowy charakter.” | C19-R, realizacje (Drive: Audi RS5, BMW M8, VW Passat B9, BMW X7) |
| 13 | „RR to klasyczny wzór frezowany z aluminium 6061. Elegancja i minimalizm, stworzone dla luksusowych limuzyn.” | RR (strona) |
| 14 | „Całość dopełnia rotacyjny dekiel gravity cap, a ręcznie szczotkowane wykończenie podkreśla każdy detal.” | RR: felga się kręci, a dekiel stoi |
| 15 | „Tak wygląda na BMW i7.” | RR, realizacja (Twoje zdjęcia) |
| 16 | „A w Black Friday każdą z nich zamówisz 15% taniej.” | laptop (propozycja, to spot BF) |
| 17 | „To tylko kilka z naszych propozycji. Zapraszam do kontaktu w sprawie doradztwa i cennika. Strzała!” | zamykasz laptop |

## 3. Plan montażu (beat sheet, ok. 70 s)
Oznaczenia:
- **P** = prowadzący (wide/tight);
- **IN** = insert;
- **DUŻE** = słowo w Anton;
- *serif* = akcent w Didot;
- napisy słowo po słowie są pod każdą kwestią.

| ok. s | Słowa | Obraz | Tekst / efekt |
|---|---|---|---|
| 0–2,5 | (hook) | ekran GT7 → C01 na Ferrari 296 (kolor) → belka | **TO JEST** / *Turismo* → **A TO JEST** / **TURISMO** (czerwone) → **BLACK FRIDAY −15%**; błysk sylwetki na wejściu |
| 2,5–6 | — | pokój gier: najazd zza ramienia na TV, PS5 pod telewizorem → **zoom w ekran** → GT7 (Twoje nagranie) w pełnym kadrze | dźwięk menu GT |
| 6–9 | 01 | P tight na kanapie z padem → pstryk | *nie o takie* / **TURISMO** pod brodą |
| 9–10,5 | — | **TRANSFORMACJA LOGO** (p. 4) | trzask, whoosh, metaliczny szum, uderzenie |
| 10,5–13 | 02 | P przed biurem w koszulce Turismo, rusza do drzwi | *od razu* / **LEPIEJ** |
| 13–21 | 03, 04 | P idzie holem, cięcie na kroku; IN: frezowanie CNC (cz-b), kucie | **KUTE**, *na zamówienie*; **GAMA** |
| 21–25 | — | salon: siadasz, otwierasz laptop | dźwięk zawiasu |
| 25–28 | 05 | IN: okno przeglądarki, wpisywanie `turismo-wheels.com` litera po literze | klawiatura; split: ekran u góry, Ty na dole |
| 28–31 | 06 | IN: prawdziwa strona, kursor klika Aluminium wheels → Custom forged wheels | **CUSTOM FORGED**, klik |
| 31–34 | 07 | P tight → **klik myszy** → kafelek C01 wyskakuje nad ekran (karta z packshotem, „BESTSELLER”) | *unikatowy* / **BESTSELLER** |
| 34–39 | 08 | IN: C01 duży plan, kamera wjeżdża w concave (strzałka i obrys), potem makro na frezowane krawędzie | **DEEP CONCAVE** → *frezowane detale* |
| 39–42 | 09 | IN: realizacje jedna na drugiej (zdjęcie na zdjęciu): Ferrari 296 → Mercedes E63, w kolorze | **FERRARI 296 GTB** / **E63** |
| 42–47 | 10, 11 | klik → kafelek C19-R; czerwony okrąg rysuje się po aero-ringu; realizacje | **AERO-RING**, *więcej charakteru* |
| 47–53 | 12, 13 | klik → kafelek RR; felga się kręci, a dekiel stoi (animacja gravity cap); Rolls-Royce Wraith | **GRAVITY CAP**, *klasyka* |
| 53–56 | 14 | P tight | **−15%** (czerwone, duże) / *w Black Friday* |
| 56–63 | 15 | P zamyka laptop, mówi do kamery | *doradztwo i cennik* / **NAPISZ** |
| 63–66 | — | plansza: 3 felgi, logo, −15% · BLACK FRIDAY, telefon i e-mail | uderzenie, akcent muzyki |

## 4. Przejście na pstryk: transformacja logo (1,4 s, kod, 0 kr)
1. Klatka trzasku: zamrożenie na 2 klatki, **błysk negatywu**.
2. Logo GT zostaje wycięte z koszulki, podnosi się i rośnie do środka kadru, a tło za nim przechodzi w czerń.
3. Logo rozpada się na ok. 800 trójkątnych odłamków, które w obrocie przechodzą z bieli w czerwień #ED3B22. Rozmycie ruchu jak z migawki 180°.
4. Odłamki składają się w **logo Turismo Wheels** z krótkim błyskiem na krawędziach.
5. Logo leci na kamerę, a jego wnętrze staje się oknem na **biuro Turismo**: przejście maską logo, Ty już w koszulce Turismo.
6. Dźwięk: trzask palców → odwrócony whoosh → szum metalu → uderzenie basu na składaniu → otoczenie ulicy.

Potrzebne pliki:
- logo Turismo Wheels w wektorze (albo pobiorę je ze strony turismo-wheels.com);
- logo GT pobiorę ze zdjęcia koszulki z playstation.com.

## 5. Generacje i koszt (wyceny Higgsfield z 23.11)
| Pozycja | Ile | Koszt |
|---|---|---|
| Karty postaci (szczuplejsza sylwetka): koszulka GT i koszulka Turismo, Seedream, z powtórkami | 4 | 10 kr |
| Karty lokacji z prawdziwych zdjęć: pokój gier z PS5, wejście, hol, salon | 4 + powtórki | 15 kr |
| Ujęcia ruchu: pokój gier, kanapa, wejście, hol, salon (30 s): draft (1,5 podejścia) → finał **1080p** (16 kr/s) | 30 s | 135 + 480 = **615 kr** |
| Ujęcia przy laptopie, mówione (ok. 36 s): bezpośrednio **720p** (7 kr/s), bez draftu, bo ruch jest prosty | 36 s | **252 kr** (+ powtórki ok. 70) |
| Muzyka (nowa pod nowy rytm) | 1 | 9 kr |
| **Razem wariant standard** | | **ok. 970 kr (~54 USD)** |
| Wariant premium: ujęcia przy laptopie też w 1080p | | ok. 1300 kr (~72 USD) |

0 kr:
- transformacja logo;
- okno przeglądarki i wpisywanie adresu;
- kafelki modeli, wskazania i okręgi;
- animacja gravity cap;
- realizacje ze strony;
- napisy, przejścia i SFX;
- plansza końcowa.

Saldo: 629,96 kr. Automatyczne doładowanie (+545 kr) zadziała raz przy standardzie i raz lub dwa razy przy premium.

Uwagi do wyceny:
- Finalizacja draftu kosztuje 16 kr/s niezależnie od rozdzielczości, dlatego ujęcia przy laptopie generujemy bez draftu.
- Drafty v2 (G1–G9) nie wejdą do v3, bo sylwetka do zmiany.

## 6. Ryzyko: PS5 i Gran Turismo
Prawdziwe PS5, gameplay GT7 i logo GT to znaki i treści Sony / Polyphony Digital.
- **Zwykły post organiczny:** zwykle przechodzi.
- **Reklama płatna (Spark Ads / Promote) albo zgłoszenie od Sony:** grozi wyciszenie albo blokada.
- Higgsfield może też odrzucić generację z marką PS5 (`ip_detected`). Wtedy PS5 i ekran wklejam w montażu z Twoich zdjęć i nagrań, zamiast je generować.

Decyzja należy do Ciebie. Robię tak, jak prosisz, a ostrzeżenie zapisuję.

## 7. Potrzebne od Ciebie (w kolejności ważności)
1. **Nagrania głosu (p. 2).** Bez nich nie ruszy ani jedna generacja z mówieniem, bo usta synchronizujemy z Twoim głosem.
2. **Biuro:** 15–30 zdjęć prawdziwego biura (wejście z zewnątrz, drzwi, hol, salon z kanapą i stolikiem), poziomo i pionowo, przy dziennym świetle. Do tego najlepiej 30–60 s nagrania telefonem, jakbyś wchodził.
   - Z YouTube nie pobieram, ale **zrzuty ekranu z filmu z Patrykiem Mikiciukiem** mogą posłużyć jako referencja.
   - Na stronie adres firmy to Gorzów Wlkp., a film jest z Wrocławia. Napisz, które biuro pokazujemy.
3. **GT7 z Twojej konsoli:** 20–30 s nagrania (przycisk Create) z GT Auto, czyli zmiana felg, oraz auto w garażu. Plus zdjęcie Twojego PS5 pod telewizorem. Alternatywnie zgoda na oficjalne zdjęcia z playstation.com.
4. **Twoje aktualne zdjęcie całej sylwetki** w zwykłej koszulce, do nowej karty postaci.
5. **Zdjęcia realizacji z C19-R.** Na Drive są rendery Audi RS5, BMW M8 i Ferrari 458 z C19-R. Czy mogę ich użyć jako „projektów”?
6. **Wektorowe logo Turismo Wheels.** Jeśli go nie masz, pobiorę logo ze strony.
7. Decyzje: wariant **standard czy premium** i czy zostaje kwestia 14 (−15% w Black Friday).
8. Blog Kareemy na higgsfield.ai ładuje treść skryptami z serwerów Higgsfield, do których ta sesja nie ma dostępu. Wklej tekst wpisów albo linki do konkretnych postów, tak jak transkrypcję.

## 8. Harmonogram do Black Friday (pt 27.11)
- Wt 24.11: Twoje materiały, karty postaci i lokacji, renderer Kareemy na tej maszynie, transformacja logo.
- Śr 25.11: generacje, montaż roboczy v3 z Twoim głosem.
- Czw 26.11: poprawki, finał 1080p.
- Publikacja 26.11 wieczorem albo 27.11 rano, wyłącznie na Twoje polecenie.

## 9. Postęp 23.11 (po południu)
- Assety v3 (Seedream, 3 × 2,5 = **7,5 kr**), w `assety/`:
  - `L1_pokoj_ps5_gt7.jpg`: pokój z assetu, PS5 Slim, DualSense, na ekranie GT7 (GT Auto);
  - `CS1_GT_slim.jpg`, `CS2_TW_slim.jpg`: karty postaci, szczuplejsza sylwetka, koszulki regular fit.
- Ekran gry to **oficjalne screenshoty GT7 z playstation.com** (`assety/referencje_gt_ps5/`): GT Auto, edytor malowania, wyścigi. Oficjalne logo GT posłuży do transformacji.
- Logo Turismo Wheels w wektorze: `assety/logo/turismo-wheels-logo.svg` (wyciągnięte z kodu strony) + sygnet PNG.
- Realizacje:
  - C01: BMW M4 G83 Satin Bronze ×3, Ferrari F8 Gloss Black ×3;
  - RR: BMW i7 G70 ×3;
  - `MERCEDES-BENZ-S-COUPE-C257-TURISMO-FORGED-C26` ma w nazwie **C26**, nie RR. Do wyjaśnienia;
  - C19-R: na Drive są pliki 4–15 MB (Audi RS5 8W Neodyme, BMW M8 GC Neodyme, VW Passat B9, BMW X7). Konektor Drive przesyła pliki jako tekst, więc takich nie pobierze. Do uzupełnienia ZIP-em jak C01/RR.
