# Reverse engineering: „Tire → Wheel Reveal” (ref. @titantirewheels)

Źródło: nagranie ekranu (WhatsApp, 368×448, 14,0 s) rolki TikTok @titantirewheels,
opis: „Got plans this weekend? A litt…”.
Statystyki widoczne na nagraniu: ~61,6 tys. polubień, 202 komentarze, 2 921 repostów, 3 150 udostępnień, 4 209 zapisów.
Zapisy ≈ 7% polubień, czyli bardzo dużo. Ludzie zapisują to jako inspirację, a to sygnał zakupowy.

Klatki co 0,25 s: `oryginal_klatki_co_0.25s.jpg`

## 1. Struktura (pomiar ffmpeg, klatka po klatce)

| Czas | Co widać | Funkcja |
|---|---|---|
| 0,0–3,3 s | Koło skręcone do oporu „od kamery”. Widać tylko bieżnik i bok opony, felgi nie widać wcale. | **Hook / luka ciekawości**: „co tam jest?” |
| 3,3–4,6 s | Kierownica wraca do prostej, koło obraca się w osi skrętu i odsłania front felgi (~1,3 s). | **Reveal** |
| 4,6–12,9 s | Felga en face. Auto toczy się powoli do przodu, felga się obraca, widać zacisk (zielony), pod spodem przesuwają się linie na asfalcie, latarnie dryfują w tle. | **Beauty shot / payoff** |
| 12,9 s | Oryginał się kończy i TikTok zapętla go od początku. Na nagraniu ekranu widać restart. | **Pętla**: koniec (felga) → start (opona) znów buduje napięcie |

- **Długość właściwa: ~12,9 s.** Jedno ujęcie, **zero cięć** (detekcja scen nie znalazła żadnego cięcia).
- **Brak tekstu na ekranie i brak lektora.** Przekaz jest czysto wizualny i działa w każdym języku.

## 2. Kamera i obraz

- Ultraszeroki kąt (action cam / telefon 0.5×), **~10–15 cm nad asfaltem**.
- Kamera **zamocowana do auta** (próg / boczek za przednim kołem), patrzy do przodu i lekko w górę.
  Dowód: nadkole stoi w kadrze nieruchomo, a tło (latarnie, linie) się przesuwa.
- Lekki przechył (dutch angle ~10°), duża perspektywa: nadkole „wchodzi” w kamerę.
- Grade: jasny, prześwietlone białe niebo, mocno nasycony kolor auta (hot pink), neutralny szary asfalt.
  Kontrast: kolorowe nadwozie, srebrna felga, czarna opona.
- Ruch auta: tempo spacerowe (~3–5 km/h). Rotacja felgi jest wolna i czytelna, wygląda jak delikatne slow-mo.

## 3. Audio (analiza RMS + pasma <150 Hz co 0,25 s)

- 0–5,7 s: muzyka **bez basu** (intro/filtrowana wokalówka), krótkie „oddechy” ~2,0 s, ~3,0 s i 5,0–5,5 s.
- **~6,0 s: drop basu.** Dalej uderzenia basu mniej więcej co 0,75 s (≈80 BPM half-time / 160 BPM): 8,25 / 9,0 / 9,75 / 12,0 / 12,75 s.
- Wniosek: trendujący dźwięk typu phonk/edit z budowaniem napięcia, a drop wypada tuż po odsłonięciu felgi.

## 4. Dlaczego to działa

1. **Luka ciekawości w 0 s**: widz widzi oponę, a felga jest ukryta. Zostaje do odsłonięcia.
2. **Nietypowy punkt widzenia** (żabia perspektywa, kamera na aucie). Tak nie wygląda zwykły katalog felg.
3. **Pętla**: koniec przechodzi płynnie w początek, więc rośnie liczba obejrzeń i watch time > 100%.
4. **Krótko (13 s), zero tekstu**: nic nie spowalnia, działa globalnie.
5. **Produkt jest bohaterem.** Felga zajmuje 60% kadru przez 8 s.

## 5. Odtworzenie na assetach Turismo Wheels

### Dostępne materiały (Google Drive, Shared Drive Turismo)
- Porsche 911 (964): **FP01 Satin Grey + Chrome**, 11 zdjęć (`PORSCHE-911-964-TURISMO-FORGED-FP01-SATIN-GREY-CHROME_01..11.jpg`)
- Ferrari F12 (`f12turismo*`), BMW X7 (`x7turismo*`), Mercedes S63 (`s63turismo*`), Audi RS6 (`rs6turismo*`)

### Ścieżka A: prawdziwe ujęcie (REKOMENDOWANA, 0 kredytów)
Najlepsza jakość i 100% wierny wzór felgi. Zgodne z zasadą „prawdziwe ujęcia aut”.
1. Auto klienta na felgach Turismo, pusty plac/parking, jasne zachmurzone niebo.
2. GoPro / telefon 0.5× na przyssawce na progu za przednim kołem, ~10–15 cm nad ziemią, 4K 60 fps.
3. Koła skręcone do oporu tak, żeby do kamery był zwrócony bieżnik.
4. Start nagrania, 3 s bezruchu, płynny powrót kierownicy do prostej w ~1,5 s,
   potem powolny przejazd (tempo spacerowe) przez ~8–10 s.
5. Montaż lokalnie (ffmpeg, 0 kr): przycięcie do 12,9 s, grade (podbita saturacja koloru auta, jasne niebo),
   ewentualnie lekkie slow-mo 0,8× w fazie przejazdu, eksport 1080×1920.

### Ścieżka B: AI w Higgsfield (gdy nie ma auta pod ręką)
Bazą są prawdziwe zdjęcia z Drive (np. Porsche 964 FP01), żeby wzór felgi był prawdziwy.

| Krok | Model | Koszt (wycena Higgsfield) |
|---|---|---|
| Klatka startowa (opona, koło skręcone) + klatka końcowa (felga FP01 en face), niski kąt 9:16, edycja zdjęć z Drive | gpt_image_2_6 | 0,75 kr / obraz → ~3 kr za 4 warianty |
| Szkic ruchu start→end, 10 s, 480p | seedance_2_5 (draft) | **30 kr** / próbę |
| (alternatywa testowa) 10 s 768p | minimax_h3_max | 25 kr |
| Finalizacja najlepszego szkicu, 720p | seedance_2_5 | **70 kr** (1080p: 160 kr) |

**Budżet ścieżki B: ~3 + 2×30 + 70 ≈ 133 kr** (saldo: 471 kr). Twardy limit: 150 kr.

Optymalizacja kosztów:
- najpierw tanie szkice 480p, finalizujemy tylko zaakceptowany szkic;
- bez audio z modelu (`generate_audio: false`), bo muzykę dobieramy w aplikacji TikTok (trend, 0 kr, większy zasięg);
- montaż, grade, napisy i CTA lokalnie w ffmpeg zamiast płatnych narzędzi;
- Ryzyko: AI potrafi „rozpłynąć” wzór szprych podczas obrotu. Przy marce, której produktem JEST felga, to realny problem.
  Dlatego ścieżka A jest lepsza dla leadów.

### Warstwa sprzedażowa (zasady Turismo)
Oryginał nie ma lektora ani tekstu i jego siła to pętla. Proponowany kompromis:
- 0–3 s: mały napis EN u góry: **„Wait for the reveal…”**;
- 4,6 s (po odsłonięciu): **„Turismo Forged FP01 · Satin Grey + Chrome”**;
- ostatnie ~2 s na jeździe (pętla dalej działa): **„Custom forged · +48 501 404 861”**;
- lektor PL (ElevenLabs „Bram”) **opcjonalnie**, jedno zdanie po dropie, np.
  „Kute felgi na zamówienie. Turismo Wheels. Unlock Your Style.”
  Uwaga: lektor osłabia efekt pętli, dlatego rekomenduję wersję bez niego, z CTA w opisie i przypiętym komentarzu;
- opis: hook + CTA (telefon + e-mail).
