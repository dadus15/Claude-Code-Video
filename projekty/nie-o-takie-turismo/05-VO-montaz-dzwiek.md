# VO, rozpiska montażu i dźwięku

## Czysty tekst VO (do nagrania próby)
Głos prowadzącego: naturalny, z lekkim rozbawieniem. Pauzy komediowe są zaznaczone `/`. Nagrywasz to sam, bo prowadzący to Twoja postać.

```
Chyba nie o takie Turismo nam chodzi.
/ [pstryk] /
Coś mi nie pasuje.
/ [pstryk] /
Od razu lepiej.
W Turismo Wheels robimy kute felgi na zamówienie. Mamy sporo wzorów. Pokażę Ci jeden.
Ten.
/ cisza ok. 4,5 s /
To C19-R.            ← wymowa: „To ce dziewiętnaście er”
Ten pierścień na obwodzie to zintegrowany aero-ring.
Spójrz, jak głęboko schodzą ramiona.
Rozmiar, ET i wykończenie dobieramy pod Twoje auto.   ← „ET” czytane „e-te”
Napisz, czym jeździsz. Strzała!
```
Przy skracaniu zostają trzy pierwsze kwestie i cisza przy wyciąganiu felgi. Najpierw tniemy „Mamy sporo wzorów”.

Pliki do lip-sync (osobne kawałki, WAV 48 kHz, 0,3 s ciszy na początku i końcu):
`A_chyba.wav`, `B_cos.wav`, `C_od-razu.wav`, `H_rozmiar-strzala.wav`.

## Rozpiska montażu (EDL) — 25 kl./s

| # | Od–do (s) | Klatki | Źródło | Obraz | Głos | Dźwięk |
|---|---|---|---|---|---|---|
| 1 | 0,00–1,60 | 0–40 | gameplay GT (nagranie) | koło auta wypełnia pion | — | silnik, opony; 1,60 klik pauzy ucina silnik |
| 2 | 1,60–6,00 | 40–150 | klip A | kciuk → kanapa → dłoń do obiektywu | 2,40–4,60 „Chyba nie o takie Turismo nam chodzi” | szum konsoli, pad na tapicerkę 4,80 |
| 3 | 6,00–10,40 | 150–260 | klip B (+1 kl. KF-C1 na końcu) | dłoń → biuro → siada → chwyta koszulkę | 8,60–9,60 „Coś mi nie pasuje” | **PSTRYK 1** w 6,00 = twarde przełączenie pogłosu; siedzisko 8,00 |
| 4 | 10,40–13,00 | 260–325 | klip C | C-PO, puszcza materiał | 11,50–12,50 „Od razu lepiej” | **PSTRYK 2** w 10,40 (ostrzejszy), szelest bawełny 10,80 |
| 5 | 13,00–17,00 | 325–425 | klip D + @WEB w ekranie | zza ramienia, plecy, przejście ostrości na ekran | 13,30–18,70 „W Turismo Wheels…” | zawias laptopa 13,10; **muzyka wchodzi 13,00**, pod głosem −18 LUFS |
| 6 | 17,00–19,00 | 425–475 | @WEB pełny ekran | katalog → C19-R → klik | (cd.) | przewijanie 16,50–18,50, klik 18,60 |
| 7 | 19,00–23,00 | 475–575 | klip E + kompozycja 2D→3D | K1→K2→K3 | 19,40 „Ten” | **muzyka i głos odsunięte 19,40–24,00**; przejście przez ramkę 20,00–20,40 (cichy szum), oddech |
| 8 | 23,00–26,00 | 575–650 | klip F + okno detalu | K4, pchnięcie, okno 24,80–25,10 | 24,20–25,40 „To C19-R” | 1 × stuk osadzenia 23,60; szum rolek od 24,00; tik okna 24,90; muzyka wraca 25,50 |
| 9 | 26,00–30,00 | 650–750 | G insert 1 (3D) | frontal, łuk + etykieta | 26,30–29,60 „Ten pierścień…” | łuk rysuje się na „pierścień” 26,60 (cichy świst) |
| 10 | 30,00–34,00 | 750–850 | G insert 2 (3D) | 3/4, punkt na ramieniu | 30,30–32,40 „Spójrz, jak głęboko…” | refleks 31,90 (szklany shimmer, cicho) |
| 11 | 34,00–38,80 | 850–970 | klip H | gospodarz + kręcąca się felga | 34,20–38,60 „Rozmiar…”, „Napisz…”, „Strzała!” | muzyka trzyma |
| 12 | 38,80–40,00 | 970–1000 | 3D / packshot | koło w kompozycji 0:00 + plansza | — | akcent muzyczny na cięciu 38,80, wybrzmienie |

## Napisy i grafika (warstwy, nigdy w renderze)
Styl @INVENTA: mały czerwony kicker WERSALIKAMI → nagłówek PL (Inter SemiBold, biały, kluczowe słowo czerwone) → mała linia EN (szara). Napisy EN spełniają zasadę profilu, że rolki mają mieć napisy po angielsku. Nagłówki zostają po polsku, zgodnie z briefem.

| Czas | Kicker | Nagłówek PL | EN | Pozycja |
|---|---|---|---|---|
| 26,60–30,00 | C19-R · GLOSS SILVER | Zintegrowany **aero-ring** | Integrated aero-ring | lewa górna ćwiartka, poza konturem felgi |
| 31,90–33,90 | C19-R | Profil **ramion** | Spoke profile | jw. |
| 34,30 / 34,90 / 35,40 → do 37,20 | NA ZAMÓWIENIE | Rozmiar · ET · **Wykończenie** (wchodzą kolejno, zostają razem) | Size · Offset · Finish | prawa połowa, nad felgą |
| 37,30–40,00 | NAPISZ W KOMENTARZU | Napisz, czym **jeździsz** | Tell us what you drive | dół, nad strefą UI TikToka |
| 37,30–40,00 | — | +48 501 404 861 · daniel.chmielewski@turismo-wheels.com | — | pod CTA, małe |
| 38,80–40,00 | — | logo TURISMO WHEELS (**do podmiany**: plik wektorowy; awaryjnie plansza tekstowa) | — | góra |

Zasady: jedna etykieta cechy naraz, minimum 1,5 s, wchodzi na właściwe słowo. Dialog A–C i H może dostać mały napis EN na dole, do decyzji. Strefa bezpieczna TikToka: nic ważnego w dolnych 300 px i prawych 140 px.

## Czerwone zaznaczenia
- Łuk: grubość 6 px przy 1080, kolor #DC1E2D. Rysuje się w 8 kl. po nieruchomym ekranowo fragmencie obwodu (10:00–12:00) i nie obraca się z felgą.
- Punkt na ramieniu: 14 px, przyklejony trackingiem do ramienia kontrolnego, z cienką białą linią do etykiety.
- Okno detalu: ramka 4 px, rozwija się z narożnika w 6–8 kl., bez cienia i bez poświaty.

## Muzyka
Do wyboru po akceptacji obrazu: trend z TikToka przez Higgsfield (`tiktok_music_trending`) albo biblioteka Epidemic Sound. Ta ostatnia wymaga autoryzacji konektora w ustawieniach claude.ai. Tempo 95–110 BPM, z wyraźnym miejscem na stop w 19,40.

## Kontrola końcowa (z briefu)
- [ ] Dokładnie dwa pstryknięcia; koszulka GT do drugiego.
- [ ] Ta sama twarz, fryzura i sylwetka przez oba cięcia.
- [ ] Logo i napisy czytelne, poprawne, znak na lewej piersi noszącego.
- [ ] Jedno ramię (przy wentylu) śledzone od laptopa do rolki; piasta, rant, lakier i kierunek obrotu bez skoków.
- [ ] Kciuk przed rantem, palce za rantem.
- [ ] Dwa punkty podparcia; okno widzi ten sam moment obrotu.
- [ ] Napisy nie zakrywają detalu i wchodzą na właściwe słowo.
- [ ] Telefon: odtworzenie bez dźwięku (czy żart i produkt są czytelne) i z dźwiękiem (pauzy, usta, stuk, CTA).
- [ ] Kadr 0:00 i 0:40 obok siebie, pętla.
