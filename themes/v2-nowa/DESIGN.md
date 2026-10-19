# v2-nowa: „Karta wizyt”. Dokument projektowy motywu

Specyfikacja dla budowniczego motywu `themes/v2-nowa`. Strona gabinetu lek. stom. Doroty
Rożdżestwieńskiej, Legnica, ul. Złotoryjska 16/18 m. 10, od 1995 roku. Treść i dane (`content/`,
`data/`) są wspólne z v1 i się ich nie zmienia. Zmieniamy wygląd, nie dane.

Ten dokument jest ostateczny. Gdy brief kierunku (`scratchpad/kier-a|b|c/BRIEF.md`) mówi co innego,
obowiązuje ten plik. Wartości liczbowe są punktem wyjścia: zmienia się je po zrzutach ekranu
(krytyka z `references/critique.md`), a każdą zmianę zapisuje tutaj.

---

## 0. Werdykt sędziego (skąd ten kierunek)

Zwycięzca: **kierunek B, „Karta wizyt”** (druk dwukolorowy, oś 42%, `editorial-report` z taste-skill
i kandydat nr 4 z `concept-seed` impeccable, `seed:044a918db497e42d`).

Przeszczepy z pozostałych kierunków:

| Skąd | Co bierzemy | Gdzie w tym dokumencie |
|---|---|---|
| A „Teczki” | rozmiar `h2` zależny od długości nagłówka (nagłówki pisze klientka) | §9.6 |
| A | deterministyczny przydział pól koloru i reguła sąsiedztwa | §9.1 |
| A | zdjęcie każdej usługi w `lista_uslug` = pierwsze zdjęcie jej podstrony | §10 `lista_uslug` |
| A | ciemny tryb z polem marki, które nie jaśnieje pod białym tekstem | §3.1 |
| C „Adres jako zdanie” | linia adresu w stopce z ramką wysokości wiersza ze zdjęciem wejścia (strzałka) | §6 |
| C | bramka zgody mapy pokazuje zdjęcie wejścia obok tekstu zgody | §10 `mapa` |
| C | numer telefonu w CTA w jednym wierszu także przy 390 px, liczony arytmetycznie | §10 `cta` |
| C | wejścia części sekcji ukryte wyłącznie pod `prefers-reduced-motion: no-preference` i klasą `.js` | §12 |

Odrzucone świadomie: stos pięciu teczek w hero (A: kostium, zakładki-trapezy powtarzają menu,
pacjent 60+ nie rozpozna ich jako nawigacji), przypięta taśma zdjęć na 2,5 ekranu (C: przejmuje
przewijanie, a zdjęcie wejścia ma 300 px), wąskie wersaliki Big Shoulders (C: słabsza czytelność
długich polskich nagłówków dla starszych pacjentów), FAQ w akordeonie (A: ukrywa treść).

---

## 1. Idea

> **Na tej stronie nieregularny tydzień gabinetu z ul. Złotoryjskiej (pon., śr., czw. rano, wtorek
> po południu, od piątku zamknięte) i jego jedyna droga zapisu, telefon 699 904 989, stają się kartą
> wizyt wydrukowaną w dwóch kolorach: jej rubryki tworzą oś 42%, a jej pola koloru niosą całą stronę.**

Test konkurenta: gabinet dwie ulice dalej ma inne godziny, inny numer, nie ma „od 1995”, lokalu
„m. 10” ani wejścia od strony Optyka. Karta (urządzenie) wyrasta z kategorii, ale jej treść należy
tylko do tego gabinetu. Dlatego karta zawsze pokazuje **prawdziwe dane z `data/gabinet.yaml`**, nigdy
ozdobny kartonik. Budowniczy nie może pominąć trzech rzeczy, które przypinają ideę do podmiotu:
tydzień przyjęć z zamalowanym dniem dzisiejszym, numer telefonu jako akcja w działającej formie
(`tel:`), adres „16/18 m. 10” ze zdjęciem wejścia.

Druk dwukolorowy: na stronie są tylko dwie farby, **atrament** (prawie czarny) i **farba nakładu**
(kolor palety z panelu: bordo z fotela, morska, granat albo szałwia). Cztery palety to cztery nakłady
tej samej odbitki: ta sama kompozycja, inna farba, żadnej zmiany układu.

Gdzie żyje karta (zasięg na wszystkie powierzchnie):

- hero strony głównej: kafelek rejestracji w mozaice (§7);
- każda ramka `bok` i blok `godziny` (§10);
- `cta` na końcu każdej strony: wiersze z numerem i godzinami (§10);
- stopka: godziny i linia adresu ze zdjęciem wejścia (§6);
- 404: karta z telefonem i adresem (§11).

Wszędzie wygląda tak samo: płaski prostokąt w tonie `--papier-2` albo w polu `--pole`, rubryki
oddzielone odstępem, bez linii i bez cieni.

Tryby powierzchni (impeccable): strona główna = **Persuade** (akcja: telefon, na pierwszym ekranie,
w działającej formie). Podstrony usług, „Pierwsza wizyta”, „O gabinecie”, polityka = **Read**
(rama niesie świat, kolumna do czytania jest spokojna). Cennik z wyszukiwarką = **Operate** w ramie
Read. Domyślny motyw jasny: scena to starsza osoba z telefonem w dziennym świetle; ciemny według
`prefers-color-scheme` i przełącznika, jak v1.

---

## 2. Argument strony głównej

Kolejność bloków ustala `content/_index.md`; szablon jej nie zmienia. Każdy blok czegoś dowodzi,
a jego forma z tego wynika. Sąsiednie sekcje mają zawsze inną kompozycję.

| # | Blok | Twierdzenie | Forma (słowo układu) |
|---|---|---|---|
| 1 | `hero` | Gabinet jednej lekarki w centrum Legnicy, od 1995. Dzwonisz pod ten numer. | mozaika |
| 2 | `pasek_zaufania` | Diagnostyka na miejscu, bez jeżdżenia po mieście. | nazwy w kolumnach |
| 3 | `lista_uslug` | Wiesz, na co się umawiasz, zanim zadzwonisz. | tabela z miniaturami |
| 4 | `tekst` wyróżniony (bruksizm) | Specjalność: szyna Michigan. | kwadratowa plansza na polu |
| 5 | `tresc_z_bokiem` + `kroki` + `tekst` + `przycisk` | Pierwsza wizyta nie zaskoczy. | schodki + karta wizyt |
| 6 | `karty` (ceny) + `przycisk` | Ceny są jawne. | menu cen |
| 7 | `tekst` (portret) + `cytat` + `przycisk` | Ta sama lekarka od 1995. | portret jako inicjał |
| 8 | `faq` | Odpowiedzi na pytania, które padają przez telefon. | pasmo na pytanie |
| 9 | `cta` | Zadzwoń. Kiedy i dokąd. | wiersze wystawowe na polu |
| 10 | stopka | Gdzie, kiedy, jak dojechać. | kolumny + linia adresu |

Szablon podstrony: pasek → pasmo tytułowe (§7.3) → bloki treści na osi → `powiazane` → `cta` →
stopka.

---

## 3. Tokeny

Plik stylów: **`themes/v2-nowa/assets/css/style.css`** (ścieżka wymagana przez
`tools/sprawdz-kontrakt.py`, kontrola 13: blok `:root[data-paleta="x"]` dla każdej palety poza bordo).
Wszystkie kolory wyłącznie przez tokeny z tej sekcji; żadnego koloru wpisanego w regułę komponentu.

### 3.1 Kolory

Mechanika jak v1: `:root` = bordo (brak atrybutu `data-paleta`),
`:root[data-paleta="morska|granat|szalwia"]` nadpisuje tylko tokeny marki. Tryb ciemny dwa razy:
`@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {…} }` oraz
`:root[data-theme="dark"] {…}`, i **dla każdej palety** oba warianty ciemne
(`:root[data-paleta="morska"]:not([data-theme="light"])` w media query oraz
`:root[data-paleta="morska"][data-theme="dark"]`). Każdy token ma wartość w każdym trybie.
`color-scheme: light` / `dark` ustawione na `:root`. `body` ma jawne `background: var(--papier)`.

**Neutralne (wspólne dla palet)**

| Token | Jasny | Ciemny | Rola |
|---|---|---|---|
| `--papier` | `#ffffff` | `#121416` | podłoże, kolumna do czytania |
| `--papier-2` | `#eef0f2` | `#1b1e22` | stopień tonu: pasmo tytułowe, karta wizyt, pasma FAQ, hover wierszy |
| `--papier-3` | `#e2e5e9` | `#252a2f` | drugi stopień: nagłówek tabeli, linie wierszy `<table>`, dni nieczynne |
| `--pismo` | `#16181b` | `#f1f2f4` | cały tekst |
| `--pismo-ciche` | `#4a5058` | `#b9bfc7` | podpisy, „nieczynne”, notki (≥ 7:1 na `--papier` i `--papier-2`) |
| `--atrament` | `#16181b` | `#0b0c0e` | kafelek atramentowy w mozaice, stopka |
| `--na-atramencie` | `#f1f2f4` | `#f1f2f4` | tekst na atramencie |
| `--na-atramencie-ciche` | `#b9bfc7` | `#a9b0b8` | drugorzędny tekst stopki |
| `--uwaga-tlo` / `--uwaga-pismo` | `#fdf1d8` / `#5c3d00` | `#332714` / `#f0c674` | ramka `uwaga`, `<mark>`, pasek informacyjny |
| `--ok-tlo` / `--ok-pismo` | `#e2f3e8` / `#174f2f` | `#12301f` / `#8fdcab` | ramka `ok` |
| `--cien` | `0 12px 32px rgb(22 24 27 / .16)` | `0 12px 32px rgb(0 0 0 / .5)` | tylko elementy, które naprawdę unoszą się (§3.5) |

**Marka (farba nakładu), tryb jasny**

| Token | bordo (domyślna) | morska | granat | szalwia | Rola |
|---|---|---|---|---|---|
| `--pole` | `#6a1222` | `#0f3b3e` | `#1d355e` | `#203b2d` | pełne pola: wyróżnione sekcje, `cta`, kafel „od 1995”, dzisiejszy dzień |
| `--pole-2` | `#7d1a2c` | `#164a4e` | `#25406f` | `#294a39` | drugi ton pola: naprzemienne wiersze CTA, hover na polu, ramka na polu |
| `--na-polu` | `#ffffff` | `#ffffff` | `#ffffff` | `#ffffff` | tekst na polu |
| `--na-polu-ciche` | `#f1d4da` | `#cbe6e8` | `#d3ddef` | `#d3e4da` | drugorzędny tekst na polu (≥ 7:1 także na `--pole-2`) |
| `--akcent` | `#9b1c31` | `#18585d` | `#2c4f8c` | `#305844` | przycisk główny, linki, ptaszki, podkreślenie aktywnego menu (wartości = v1 `--brand-700`) |
| `--akcent-ciemny` | `#7d1628` | `#124549` | `#223f72` | `#264636` | hover i `:active` przycisku głównego |
| `--akcent-tlo` | `#f5e9eb` | `#e1eeef` | `#e8ecf2` | `#e7edea` | ramka `info`, `::selection` |
| `--na-akcencie` | `#ffffff` | `#ffffff` | `#ffffff` | `#ffffff` | napis na przycisku głównym |

**Marka, tryb ciemny** (pole zostaje głębokie, bo niesie biały tekst; akcent jaśnieje, bo stoi na
ciemnym papierze; wartości akcentu = v1 w trybie ciemnym)

| Token | bordo | morska | granat | szalwia |
|---|---|---|---|---|
| `--pole` | `#4a0d18` | `#0c2e30` | `#162a4b` | `#182e23` |
| `--pole-2` | `#5a1220` | `#123a3d` | `#1d3459` | `#1f3a2c` |
| `--na-polu` | `#ffffff` | `#ffffff` | `#ffffff` | `#ffffff` |
| `--na-polu-ciche` | `#ecc6cd` | `#bfe0e2` | `#c9d5ec` | `#c9dfd2` |
| `--akcent` | `#f08a9b` | `#28b9c3` | `#89a9e0` | `#70b693` |
| `--akcent-ciemny` | `#f7b7c1` | `#62d9e1` | `#b4c9ec` | `#9ccfb3` |
| `--akcent-tlo` | `#3a1a22` | `#152728` | `#1c2432` | `#1c2621` |
| `--na-akcencie` | `#121416` | `#121416` | `#121416` | `#121416` |

Proporcje strony głównej (jasny, bordo): papier ok. 60%, `--pole` 25–30% (kafel w mozaice, plansza
bruksizmu, nagłówek FAQ, `cta`), `--papier-2` ok. 10%, atrament ok. 5% (kafel faktów, stopka).
Akcent (`--akcent` na papierze) tylko na akcjach i linkach.

**Obowiązek przed pierwszym zrzutem:** skrypt Node w scratchpadzie liczy kontrast WCAG każdej pary
tekst/tło (4 palety × 2 tryby: `--pismo`/`--papier`, `--pismo`/`--papier-2`, `--pismo-ciche`/oba,
`--na-polu`/`--pole`, `--na-polu-ciche`/`--pole` i `--pole-2`, `--na-akcencie`/`--akcent`,
`--akcent`/`--papier`, `--uwaga-pismo`/`--uwaga-tlo`, `--ok-pismo`/`--ok-tlo`). Próg: tekst ≥ 4,5:1,
cel ≥ 7:1 dla tekstu biegnącego. Wynik wpisać jako komentarz na górze `style.css`. Wartość, która nie
przechodzi, poprawić tutaj i w CSS.

`partials/paleta.html`: przejąć **1:1 z v1** (akcenty favicony i `theme-color`).
`partials/kolory-motywu.html`: `dict "jasny" "#ffffff" "ciemny" "#121416"` (= `--papier`).

### 3.2 Typografia: dwa kroje, OFL, self-hosting

| Rola | Krój | Pakiet npm (sprawdzony, OFL-1.1) | Pliki do skopiowania |
|---|---|---|---|
| Nagłówki, ceny w menu, numer w CTA, plakietka „od 1995”, linia adresu w stopce | **Young Serif** 400 (jedyna waga) | `@fontsource/young-serif@5.3.0` | `files/young-serif-latin-400-normal.woff2`, `files/young-serif-latin-ext-400-normal.woff2`, `LICENSE` |
| Tekst, menu, przyciski, tabele, formularze | **Atkinson Hyperlegible Next**, zmienny `wght` 200–800 | `@fontsource-variable/atkinson-hyperlegible-next@5.3.0` | `files/atkinson-hyperlegible-next-latin-wght-normal.woff2`, `files/atkinson-hyperlegible-next-latin-ext-wght-normal.woff2`, `…-latin-wght-italic.woff2`, `…-latin-ext-wght-italic.woff2`, `LICENSE` |

Pobranie: `npm pack <pakiet>@5.3.0` w osobnym, pustym katalogu w scratchpadzie, rozpakowanie tam
(`tar xzf`), skopiowanie tylko plików z tabeli do **`themes/v2-nowa/static/fonts/`**. Licencje jako
`static/fonts/OFL-young-serif.txt` i `static/fonts/OFL-atkinson-hyperlegible-next.txt`. Nic z npm nie
trafia do repo poza tymi plikami. (Paczki są już pobrane w
`scratchpad/fontcheck-sedzia/*.tgz`.)

`@font-face` w `style.css`: osobno `latin` i `latin-ext`, z `unicode-range` skopiowanym z
`index.css` pakietu (polskie ą, ę, ł, ń, ś, ź, ż, ć są w latin-ext, ó w latin), `font-display: swap`,
URL względem `baseURL` (`{{ "fonts/…" | relURL }}` w `head.html` dla preloadu; w CSS ścieżka względna
`../fonts/…` nie zadziała z `assets/`, więc `@font-face` wypisać w partialu `fonty.html` jako `<style>`
z `relURL` albo użyć `resources.Get` + `.RelPermalink` po przeniesieniu fontów do `assets/fonts/`;
wybrać jeden sposób i sprawdzić pod `/test/`). Preload tylko dwóch plików: Atkinson latin normal
i Young Serif latin-ext (nagłówki polskie prawie zawsze mają ogonki). Po pierwszym buildzie sprawdzić
zrzutem napis „Rożdżestwieńska, źródło, łuk, gęś” w obu krojach.

Zapas: `"Young Serif", Georgia, "Times New Roman", serif` i
`"Atkinson Hyperlegible Next", "Segoe UI", system-ui, sans-serif`; `@font-face` zapasu z `local()`
i `size-adjust` (Georgia ok. 96%, Segoe UI ok. 100%), dobranym zrzutem, żeby skok przy `swap` był mały.

Kursywa Atkinson tylko dla `<em>` z treści klientki. Young Serif nie ma kursywy ani pogrubienia:
`font-synthesis: none` na nagłówkach.

**Pięć stopni i nic pomiędzy** (house rule taste-skill)

| Token | Wartość | Krój, interlinia, tracking | Użycie |
|---|---|---|---|
| `--st-maly` | `clamp(0.9375rem, 0.9rem + 0.15vw, 1rem)` (15→16) | Atkinson, 1.45 | okruszki, podpisy zdjęć, uwagi w cenniku, linia prawna, górny pasek |
| `--st-tekst` | `clamp(1.125rem, 1.07rem + 0.25vw, 1.25rem)` (18→20) | Atkinson 400, 1.6, miara 60–68ch | tekst, listy, tabele, przyciski (600) |
| `--st-lead` | `clamp(1.3125rem, 1.15rem + 0.7vw, 1.625rem)` (21→26) | Atkinson 400/700, 1.4 | `wstep`, `nadtytul` jako zdanie, zdanie stanu, nazwy usług, pytania FAQ |
| `--st-naglowek` | `clamp(1.875rem, 1.3rem + 2.4vw, 3rem)` (30→48) | Young Serif, 1.08, −0.015em | `h2` długie, długi `h1`, tytuły kroków, ceny w menu, cytat |
| `--st-wystawa` | `clamp(2.5rem, 1.4rem + 4.6vw, 5.25rem)` (40→84) | Young Serif, 0.98, −0.02em | `h2`/`h1` krótkie, „od 1995 roku”, numer telefonu w CTA, linia adresu w stopce |

Wyjątek mierzony w pikselach, nie nowy stopień: na telefonie numer w CTA i linia adresu w stopce mogą
mieć `font-size` liczony od szerokości (`clamp(2rem, 9vw, 2.6rem)`), bo muszą zmieścić się w jednym
wierszu. To wciąż stopień „wystawa”.

Reguły: `text-wrap: balance` na `h1`–`h3`, `text-wrap: pretty` na akapitach, `hyphens: manual`
(żadnego automatycznego dzielenia nazwiska), `font-variant-numeric: tabular-nums` w cenach,
godzinach, tabelach i liczniku cennika. Wyrównanie do lewej wszędzie; jedyny wyśrodkowany moment to
plakietka „od 1995 roku” w mozaice. Skok tekst → nagłówek ≥ 2,4× (18→48), tekst → wystawa ≥ 4×.

### 3.3 Odstępy

```css
--s-1: 0.25rem;  /* 4  */
--s-2: 0.5rem;   /* 8  */
--s-3: 0.75rem;  /* 12 */
--s-4: 1rem;     /* 16 */
--s-5: 1.5rem;   /* 24 */
--s-6: 2rem;     /* 32 */
--s-7: 3rem;     /* 48 */
--s-8: 4rem;     /* 64 */
--s-sekcja: clamp(4.5rem, 2rem + 8vw, 11rem);   /* 72→176: odstęp między sekcjami */
--s-pole:   clamp(4rem, 2rem + 6vw, 8rem);      /* padding pionowy pól koloru */
--margines: clamp(1.25rem, 4vw, 3.5rem);        /* 20→56: margines strony, równy z obu stron */
--rynna:    clamp(1rem, 2vw, 2rem);             /* 16→32: odstęp kolumn */
```

Wewnątrz sekcji najwyżej `--s-7` (48 px) między grupami. Nad nagłówkiem zawsze więcej miejsca niż pod
nim (nad `h2` w sekcji: `--s-sekcja` albo `--s-7`; pod: `--s-5`). Bloki z `polacz: true` stoją
w tym samym tle z odstępem `--s-7`, bez `--s-sekcja`.

### 3.4 Promienie

**Zero wszędzie** (`--promien: 0`): przyciski, zdjęcia, kafelki, pola formularza, lightbox, menu.
Decyzja podjęta raz. Jedyne koło na stronie: przełącznik motywu jako przycisk 44×44 kwadratowy też.

### 3.5 Cienie, linie, warstwy

- Cień `--cien` tylko na: rozwiniętym podmenu desktopu, szufladzie menu mobilnego, dolnym pasku
  kontaktowym na telefonie, `<dialog>` lightboxa. Nic w spoczynku nie ma cienia.
- Linie tylko w prawdziwych `<table>` (1 px `--papier-3` między wierszami) i w polach formularza
  (obrys 2 px `--pismo-ciche`). Poza tym powierzchnie dzieli stopień tonu.
- `z-index`: pasek główny 50, podmenu 60, dolny pasek 70, szuflada 80, lightbox (top layer `<dialog>`).

### 3.6 Ruch (tokeny)

```css
--ease-wyjscie: cubic-bezier(.16, 1, .3, 1);   /* wejścia, maska nagłówka */
--ease-zwykly:  cubic-bezier(.2, .7, .3, 1);   /* hover, szuflada */
--t-szybki: 150ms;  --t-sredni: 250ms;  --t-wejscie: 600ms;  --t-maska: 900ms;
```

---

## 4. Siatka i oś

- 12 kolumn, `column-gap: var(--rynna)`, marginesy `var(--margines)` **równe** z obu stron, treść
  najwyżej 1440 px, wyśrodkowana; pola koloru (`--pole`, `--papier-2`, `--atrament`) zawsze do
  krawędzi okna.
- **Oś** = początek kolumny 6 (5/12 ≈ 41,7%). Lewa strefa = kolumny 1–5, kolumna treści = 6–12.
  Przy 1280 px kolumna treści ma ok. 680 px, czyli tekst 19–20 px w mierze ok. 64 znaków. Oś jest jedna
  i dokładna w całym serwisie; każdy `h2`, każdy akapit bloku `tekst` bez zdjęcia, każda tabela
  zaczyna się na niej albo na lewym marginesie. Lewe krawędzie tekstu: **lewy margines i oś**, plus
  wcięcia schodków. Nic więcej.
- Poniżej 900 px oś schodzi do lewego marginesu: jedna kolumna, zawartość lewej strefy idzie nad albo
  pod kolumnę (zasady w §10 dla każdego bloku).
- `scroll-margin-top` na każdej kotwicy = wysokość paska głównego + 16 px.

---

## 5. Nagłówek strony i menu

### 5.1 Pasek informacyjny

`ustawienia.pasek_informacyjny` niepusty → pełne pasmo `--uwaga-tlo`, tekst `--st-tekst`
`--uwaga-pismo`, nad wszystkim. Pusty → nic.

### 5.2 Górny pasek (desktop ≥ 900 px)

Pasmo `--papier-2`, wysokość 44 px, `--st-maly`. Widoczne pozycje według `naglowek_strony`:

- z lewej `pasek_godziny` → **zdanie stanu** (skrócona żywa rzecz, §8), bez kropki „live”;
- z prawej `pasek_telefon` → numer jako `tel:` z ikoną słuchawki, `pasek_adres` → adres jako link do
  strony dojazdu (`strona_dojazdu`, logika `cel-linku` v1), `pokaz_przelacznik_motywu` → przycisk
  44×44 z ikoną słońca/księżyca, `aria-label` i `aria-pressed` jak v1.
- Pozycje rozdziela odstęp `--s-6`, nie „·”. Wszystkie wyłączone → pasek nie powstaje.
- Brak przełącznika → skrypt nie stosuje zapamiętanego motywu (zachowanie v1).

### 5.3 Pasek główny (desktop)

- `--papier`, wysokość 72 px, `position: sticky; top: 0`, nieprzezroczysty, bez rozmycia, bez linii
  i bez cienia pod spodem. Po przewinięciu ponad 8 px tło zmienia się na `--papier-2` (150 ms), żeby
  pasek odróżniał się od treści stopniem tonu, nie linią.
- Z lewej: znak (`ustawienia.logo` przez `ikony-strony.html`, a bez niego ząb z v1 w kwadracie
  `--pole`, 40×40, biały rysunek) i nazwa `logo_nazwa` (Young Serif 22 px, czyli `--st-lead` w kroju
  nagłówków, dopuszczalne jako ten sam stopień) z `logo_podpis` pod spodem w `--st-maly`
  `--pismo-ciche`. `logo_bez_napisow: true` → sam znak (nazwa w `aria-label`).
- **Menu zaczyna się na osi** (kolumna 6): „Start” (gdy `pokaz_start`; etykieta `napisy.menu_start`
  lub i18n), potem `menu.yaml → pozycje`. Atkinson 600 `--st-tekst`. Aktywny link: podkreślenie 3 px
  `--akcent`, `text-underline-offset: 8px`, `aria-current="page"`. Pozycja z `podmenu` to przycisk
  z ikoną strzałki (`aria-expanded`, `aria-controls="podmenu-<slug>"`): panel `--papier` z `--cien`,
  pozycje w dwóch kolumnach przy 6+ pozycjach, `--st-tekst`, hover `--papier-2`; zamyka Esc i klik
  poza panelem (logika v1).
- Z prawej: **przycisk wypełniony „Umów wizytę”** (`napisy.przycisk_naglowka` albo i18n
  `bookVisit`, jak v1), `tel:` pierwszego numeru.
- Gdy menu nie mieści się w jednej linii (np. 900–1100 px), nazwa traci podpis, a potem menu przechodzi
  w wariant mobilny. Sprawdzić przy 1024 px.

### 5.4 Telefon (< 900 px)

- Pasek 60 px, sticky: znak + `logo_nazwa` (bez podpisu) z lewej, z prawej przycisk „Menu” (słowo,
  nie hamburger bez podpisu; 48 px wysokości, `aria-controls="menu-mobilne"`).
- Górny pasek: tylko zdanie stanu i przełącznik motywu, 40 px.
- **Szuflada `#menu-mobilne`**: pełna wysokość, wysuwa się z prawej (250 ms), tło `--papier`, `--cien`.
  Na górze „Zamknij menu” (i18n `closeMenu`). Pozycje w `--st-lead` co 56 px, podmenu Usług rozwijane
  przyciskiem (`podmenu-…` jak v1), `menu.dodatkowe` niżej w `--st-tekst`. Na dole karta wizyt:
  zdanie stanu, przycisk telefonu na pełną szerokość, godziny w skrócie. Fokus uwięziony w szufladzie,
  Esc zamyka, przewijanie strony zablokowane (logika v1).
- **Dolny pasek kontaktowy** (jak v1): `position: fixed; bottom: 0`, `--pole`, 64 px +
  `env(safe-area-inset-bottom)`, „Zadzwoń 699 904 989” (2/3, ikona słuchawki) i „Dojazd” (1/3, link do
  strony dojazdu), `--na-polu`, Atkinson 700. Chowa się (IntersectionObserver), gdy na ekranie jest
  kafel rejestracji hero albo blok `cta`, żeby akcja nie stała dwa razy. `body` ma
  `padding-bottom: 64px` na telefonie.

---

## 6. Stopka

Odwrócona: `--atrament`, `--na-atramencie`. `min-height: 70svh` na desktopie, `auto` na telefonie.
Bez „przyklejonego odsłaniania”.

1. **Górny rząd, 4 kolumny** (`--st-tekst`, nagłówki kolumn w Young Serif `--st-lead`, teksty
   nagłówków z `napisy.stopka_*` albo i18n):
   - **Gabinet** (`stopka_gabinet`): `gabinet.nazwa`, `lekarz`, adres, `adres.parking`,
     link do strony dojazdu; profile (`gabinet.profile`: Google, ZnanyLekarz) jako linki tekstowe
     z `rel="noopener"` i `target="_blank"`; e-mail **tylko gdy `gabinet.email` niepusty** (dziś pusty,
     więc go nie ma).
   - **Godziny** (`stopka_godziny`): `godziny-tabela.html` jako tabela, dzisiejszy dzień pogrubiony
     i oznaczony słowem „dziś” (Europe/Warsaw, przez skrypt), dni nieczynne słowem „nieczynne”
     w `--na-atramencie-ciche`.
   - **Usługi** (`stopka_uslugi`): `menu.stopka_uslugi`, a gdy puste, kolejność z `uslugi.yaml`.
   - **Strony**: `menu.stopka`. Pod spodem `platnosci` jednym zdaniem („Płatność: gotówka, karta
     płatnicza, BLIK.”, prefiks z i18n).
2. **Linia adresu** (przeszczep z C), od marginesu do marginesu, Young Serif `--st-wystawa`, zwykła
   pisownia: **„Złotoryjska [ramka] 16/18 m. 10”**. `[ramka]` to `<img>` o wysokości jednego wiersza
   (`height: 0.9em` linii, proporcja zdjęcia, nie więcej niż natywne 300×266) z wejściem do kamienicy
   i niebieską strzałką. Źródło zdjęcia: strona dojazdu (`strona_dojazdu`, a gdy puste, logika v1,
   dziś `kontakt`) → pierwszy blok `tekst` ze `zdjecie` → to zdjęcie przez `image.html` (WebP
   ≤ natywnej szerokości, `alt` z treści). Brak zdjęcia → linia bez ramki. Cała linia jest linkiem do
   strony dojazdu (hover: podkreślenie 4 px `--na-atramencie`). Tekst linii składany z
   `gabinet.adres.ulica` (bez „ul. ”, przy pierwszej spacji przed numerem wstawiona ramka); dla
   czytników ekranu pełny adres w `aria-label`, `<img>` ma swój `alt`.
   Telefon: dwa wiersze „Złotoryjska” / „[ramka] 16/18 m. 10”, `clamp(2rem, 11vw, 3rem)`.
3. **Linia prawna** `--st-maly` `--na-atramencie-ciche`: `stopka_dolna` (linki), `rejestrowe`
   (puste pola znikają, nic nie wymyślamy), `stopka_tekst`, „© {rok} {nazwa_krotka}”. Z prawej mały
   przycisk „Zadzwoń”.

Telefon: kolumny 2 × 2, potem linia adresu, potem linia prawna. Pod dolnym paskiem kontaktowym musi
zostać miejsce (padding).

---

## 7. Hero

### 7.1 Strona główna, desktop (≥ 900 px): „mozaika-winieta, tytuł na osi”

**Pasmo mozaiki** zaraz pod paskiem głównym, do krawędzi treści (nie okna), wysokość
`clamp(440px, 56vh, 540px)`, siatka 6 kolumn × 2 rzędy **bez fug** (kafle stykają się krawędzią):

| Kafel | Miejsce | Treść |
|---|---|---|
| zdjęcie | kolumny 1–3, rzędy 1–2 | `hero.zdjecie` (`hero-gabinet.jpg`: fotel w bordo, okno z Katedrą), `object-fit: cover`, `object-position: 65% 50%` (okno), pełny kolor, `fetchpriority="high"`, bez `loading="lazy"`, `sizes="(min-width: 900px) 46vw, 100vw"`; nigdy szerzej niż natywne 794 px CSS przy 1× (przy 1440 px kolumny 1–3 mają ok. 660 px) |
| plakietka | kolumna 4, rząd 1 | `--pole`: `plakietka.wyroznienie` („od 1995 roku”) w `--st-wystawa` złamane na dwa wiersze („od 1995 / roku”, łamanie przez `max-width: 5ch`), wyśrodkowane w pionie i poziomie, `--na-polu` |
| fakty | kolumna 4, rząd 2 | `--atrament`: `plakietka.tekst` („ten sam lekarz, ten sam adres”) w `--st-tekst` `--na-atramencie-ciche` na górze, pod nim `fakty[]` jako wiersze: ikona 20 px (klucz `ikona`, `currentColor`) + tekst Markdown w wierszu, `--st-tekst` (przy szerokości kolumny < 220 px: `--st-maly`) |
| **karta rejestracji** | kolumny 5–6, rzędy 1–2 | `--papier-2`: **jedna żywa rzecz** (§8): nagłówek karty „Rejestracja telefoniczna” (Young Serif `--st-lead`), zdanie stanu `--st-lead`, pasek tygodnia (7 komórek), przycisk główny „Zadzwoń: 699 904 989” na pełną szerokość kafla (56 px), pod nim `bok`-owa notka z v1 o tym, że telefon bywa zajęty (i18n `phoneBusyNote`, treść jak v1, bez obietnic) |

Bez `plakietka` → kafel plakietki i faktów łączy się w jeden atramentowy kafel z faktami. Bez
`fakty` → atramentowy kafel pokazuje adres z `gabinet.yaml`. Bez zdjęcia → zdjęcie zastępuje kafel
`--pole` z nazwą gabinetu w `--st-wystawa` (nie szare pudło).

**Pod pasmem**, na `--papier`, `--s-8` niżej:

- `h1` (= `hero.naglowek`) od lewego marginesu, na pełną szerokość treści, reguła długości (§9.6):
  dziś 82 znaki → `h1--zdanie`, Young Serif `clamp(1.75rem, 1rem + 2.2vw, 2.75rem)` (44 px przy
  1280), **2 wiersze** przy 1280 i 1440 (ok. 53 znaki na wiersz). Treść z emotikonem „:)” zostaje bez
  zmian.
- Lewa strefa (kolumny 1–5): `nadtytul` jako **zdanie pod nagłówkiem**, nie etykieta: „Od 1995 roku
  w centrum Legnicy” w `--st-lead` `--pismo` (ikonę `ikona` pomijamy). Pod nim przyciski:
  „Zadzwoń: 699 904 989” (wypełniony, gdy `pokaz_telefon`) i `przycisk` („Jak wygląda pierwsza
  wizyta”, obrysowy). Na desktopie to drugie wystąpienie telefonu na pierwszym ekranie jest
  świadome: karta jest „teraz”, ten przycisk jest przy treści.
- Kolumna treści od osi (6–12): `hero.tresc` (ok. 600 znaków, wersaliki klientki zostają) w **dwóch
  kolumnach** CSS (`columns: 2; column-gap: var(--s-7)`), `--st-tekst`. Poniżej 1100 px jedna kolumna.

Pierwszy ekran przy 1440×900 i 1280×800: pasek (44 + 72) + mozaika + górna część `h1`. Dominanta
(test jednej sekundy): zdjęcie gabinetu z bordowym fotelem obok bordowego pola „od 1995 roku”.

### 7.2 Strona główna, telefon (390×844)

1. Pasek 60 px (+ górny pasek 40 px ze zdaniem stanu).
2. Mozaika 3 kolumny × 2 rzędy, wysokość 210 px, bez fug: zdjęcie (kolumny 1–2, rzędy 1–2), pole
   „od 1995 roku” (kolumna 3, rząd 1, `--st-lead` w Young Serif), kafel atramentowy (kolumna 3,
   rząd 2) z „m. 10” i ikoną pinezki (pierwszy fakt skrócony do numeru lokalu; pełne fakty są niżej).
3. **Karta rejestracji** na pełną szerokość (`--papier-2`, padding 20 px): zdanie stanu 21 px,
   pasek tygodnia (7 komórek po ok. 46 px; skrót dnia „pon.” nad godzinami w dwóch wierszach 15 px),
   przycisk 56 px na pełną szerokość.
4. `h1` 26–28 px (4 wiersze, cena niezmienialnej treści; patrz §16), `nadtytul` 21 px, przycisk
   „Jak wygląda pierwsza wizyta” na pełną szerokość, `tresc` 18 px w jednej kolumnie, `fakty`.

Rachunek: 40 + 60 + 210 + 16 + ok. 200 (karta) = 526 px, więc karta z przyciskiem telefonu mieści się
w pierwszym ekranie, a `h1` zaczyna się nad zgięciem.

### 7.3 Podstrona: pasmo tytułowe (pierwszy blok `hero` albo tytuł strony)

- Pasmo `--papier-2`, padding pionowy `--s-8`.
- Ze zdjęciem (`hero.zdjecie`): lewa strefa (kolumny 1–5) to zdjęcie dochodzące do **lewej krawędzi
  okna**, kadr 4:5 z Hugo (`Fill` z `anchor: smart`), najwyżej 560 px wysokości i nie szersze niż
  natywne. Od osi: okruszki (`--st-maly`, „Start / Usługi / Higienizacja”, separator „/”
  w `--pismo-ciche`, `aria-label` z i18n, JSON-LD `BreadcrumbList` z `okruszki-model.html`), `h1`
  (reguła długości), `nadtytul` jako zdanie pod `h1`, `tresc` w `--st-lead`, `fakty` jako wiersze
  z ikoną, przyciski (`pokaz_telefon` → wypełniony z numerem, `przycisk` → obrysowy).
  `plakietka` na podstronie → pole `--pole` przyklejone do dolnej krawędzi zdjęcia, 2 wiersze
  (`wyroznienie` `--st-naglowek`, `tekst` `--st-tekst`).
- Bez zdjęcia: okruszki i `h1` od lewego marginesu na pełną szerokość (kolumny 1–10), wstęp i reszta
  od osi.
- Strona usługi (`usluga` w front matter, dane z `uslugi.yaml`): pod `h1` jedna linia ceny
  „od 300 zł” (`napisy.karta_cena_od` + `cena_od` przez `cena.html`) w Young Serif `--st-lead`.
  To dane, nie nowa treść.
- Bez bloku `hero` na stronie → to samo pasmo, ale tylko z okruszkami i `title` jako `h1` (opisu SEO
  `description` nie pokazujemy jako treści; zachowanie v1).
- Telefon: zdjęcie nad tytułem w kadrze 3:2 na pełną szerokość (bez marginesów), potem okruszki,
  `h1`, wstęp, przyciski 56 px na pełną szerokość.
- `hero` nie jako pierwszy blok: `h2` w pasie `--papier-2` z tym samym układem, bez okruszków.

---

## 8. Jedna żywa rzecz: „Czy gabinet teraz przyjmuje”

Komponent `partials/karta-wizyt.html` (nowy) rysowany z `gabinet-model.html` (`godziny_dane`)
i atrybutu `data-godziny` w formacie v1 (`"1:9:00-15:00;2:15:00-19:00;…"`). Logikę stanu przejąć
z `app.js` v1 i poprawić:

- **Czas: strefa `Europe/Warsaw`**, nie zegar urządzenia: `Intl.DateTimeFormat('pl-PL',
  {timeZone: 'Europe/Warsaw', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'})`
  → `formatToParts`. v1 używa `new Date().getDay()`; v2 nie.
- Odświeżanie co 60 s (`setInterval`), wstrzymane przy `document.hidden`.
- **Zdania stanu** (i18n, klucze nowe, parametry `{{ .time }}`, `{{ .day }}`, `{{ .left }}`), pełny
  kolor pisma, `aria-live="polite"` tylko na karcie w hero:
  - w godzinach: `statusOpenUntil` = „Gabinet teraz przyjmuje, do {time}.”
  - przed otwarciem tego samego dnia: `statusOpensToday` = „Dziś przyjmujemy od {time}.”
  - po godzinach i w dni nieczynne: `statusClosedOpens` = „Teraz zamknięte. Najbliżej: {day} o {time}.”,
    gdzie `{day}` z mapy i18n `dayNext*`: „jutro” albo „w poniedziałek”, „we wtorek”, „w środę”,
    „w czwartek”, „w piątek”, „w sobotę”, „w niedzielę”;
  - brak godzin w danych: `statusClosed` nie jest pokazywane; karta pokazuje tylko telefon.
  Żadnego „odbierzemy”, „od razu”, „zawsze”. Telefon bywa zajęty i v1 mówi o tym wprost
  (zostawić tę notkę).
- **Pasek tygodnia**: 7 komórek pon.–niedz. (`<ol aria-hidden="true">`), w każdej skrót dnia
  (`--st-maly` 700) i godziny („9–15”, półpauza, `tabular-nums`) albo słowo „nieczynne”
  (`--pismo-ciche`). **Dziś = komórka zamalowana** `--pole` z `--na-polu` i słowem „dziś” (stan
  znakiem i słowem, nie samym kolorem). Dni nieczynne na `--papier-3`. Wersja pionowa (7 wierszy)
  w `bok`, w stopce i w szufladzie.
- **Dla czytników i bez skryptu**: Hugo renderuje pełną `<table>` godzin (`godziny-tabela.html`,
  klasa `visually-hidden` tylko wtedy, gdy pasek jest widoczny, czyli przy `.js`). Bez JS widać tabelę,
  a zdanie stanu ma atrybut `hidden` (zdejmuje go skrypt), więc nigdy nie pokazuje nieaktualnego stanu.
  Pasek bez JS też jest renderowany przez Hugo (bez „dziś”), więc układ się nie zapada.
- Gdzie: zdanie stanu tylko w karcie hero i w górnym pasku (oraz w szufladzie). Pasek tygodnia:
  karta hero, `bok`, blok `godziny`, stopka, 404. Jeden komponent, liczony jedną funkcją.
- Ruch żywej rzeczy (jedyny): komórka „dziś” zamalowuje się od dołu (`transform: scaleY(0 → 1)` na
  `::before`, 500 ms, `--ease-wyjscie`) po wejściu mozaiki. Bez pulsowania, bez kropki.

Druga, istniejąca interakcja z kontraktu, nie druga sygnatura: wyszukiwarka cennika (§10 `cennik`).

---

## 9. Reguły wspólne bloków

### 9.1 `wariant` i pola koloru (reguła sąsiedztwa)

- `wariant: domyslny` → `--papier`.
- `wariant: wyrozniony` → pełne pasmo `--pole` z `--na-polu` (tekst), `--na-polu-ciche` (drugorzędny),
  linki `--na-polu` podkreślone, przyciski: główny = `--papier` z pismem `--pole`, obrysowy = obrys 2 px
  `--na-polu`.
- **Reguła sąsiedztwa** (liczona w `sekcje.html` po kolei, na grupach `polacz`):
  1. blok wyróżniony, którego poprzednia grupa stoi na `--pole`, dostaje `--papier-2`;
  2. na stronie najwyżej trzy grupy na `--pole` poza `cta`; czwarta i dalsze wyróżnione dostają
     `--papier-2`.
  Strona główna wychodzi tak: mozaika (papier) → atuty (papier) → usługi (papier) → **bruksizm
  (pole)** → pierwsza wizyta (papier) → **ceny (pole)** → lekarka (papier) → **FAQ (nagłówek na
  polu, pasma papier/papier-2)** → **cta (pole)** → stopka (atrament). FAQ kończy się pasmem papieru,
  więc `cta` na polu styka się z papierem i reguła jest spełniona.
- `cta` zawsze na `--pole`. Gdy poprzednia grupa kończy się na `--pole`, `cta` dostaje `--papier-2`
  z numerem w `--akcent` (stopka zawsze `--atrament`). Dwa takie same pola nigdy się nie stykają.
- Pole ma padding `--s-pole`; pola stykają się krawędzią, bez linii i bez odstępu.

### 9.2 `waska`

`waska: true` → kolumny 4–10 (ok. 68ch), bez lewej strefy. `faq`, `formularz`, `rezerwacja`
stojące samodzielnie i tak trzymają kolumnę treści.

### 9.3 `polacz`

Grupowanie 1:1 z v1 (`sekcje.html`, z listą kotwic zarezerwowanych i błędami budowania). Blok
dołączony: to samo tło, odstęp `--s-7`, pusty nagłówek = brak nagłówka. Bloki dołączone do bloku
z kolumną boczną (`tekst` ze zdjęciem, `tresc_z_bokiem`, `kontakt`) trafiają do kolumny treści od osi
(zasada v1).

### 9.4 `kotwica`

`id` sekcji, `scroll-margin-top` (§4). Zarezerwowane kotwice i błędy jak v1.

### 9.5 `nadtytul`

**Nigdy nad nagłówkiem, nigdy pigułka.** Zawsze bezpośrednio pod `h1`/`h2`, jako zdanie w
`--st-lead`, kolor `--pismo` (na polu `--na-polu-ciche`). `ikona` przy nadtytule pomijana (kontrakt
pozwala).

### 9.6 Rozmiar nagłówka zależny od długości

Partial `h2.html` (i wariant dla `h1`) liczy `len` (runy) nagłówka:

- `h1`: ≤ 40 znaków → `--st-wystawa`; > 40 → `h1--zdanie` (§7.1: 28→44 px).
- `h2`: ≤ 26 znaków → `--st-wystawa` („Czym się zajmujemy”, „Ile to kosztuje”, „Najczęstsze
  pytania”, „Umów wizytę telefonicznie”); 27–60 → `--st-naglowek`; > 60 → `--st-naglowek`
  z `max-width: 22ch`.
- `h3` (pytania FAQ, tytuły kart): Atkinson 700 `--st-lead`; tytuły kroków: Young Serif
  `--st-naglowek`.

Cel: najwyżej 2 wiersze na desktopie wszędzie, gdzie treść na to pozwala; na telefonie ≤ 3 wiersze
dla `h2`. Nie zmniejszać poniżej stopnia, żeby oszukać pomiar.

### 9.7 Przyciski (wszędzie)

- `glowny`: wypełniony `--akcent`, napis `--na-akcencie`, Atkinson 600 `--st-tekst`, wysokość 52 px
  (56 px na telefonie), padding `0 var(--s-5)`, promień 0. Hover/`:active` → `--akcent-ciemny`,
  `:active` także `translateY(1px)`.
- `obrysowy`: obrys 2 px `--pismo` (to element sterujący, nie dekoracja; obrys 1 px zakazany), tło
  przezroczyste, hover `--papier-2`.
- Strzałka „→” (SVG, nie glif) tylko przy przyciskach prowadzących do innej strony, przesuwa się
  o 4 px przy hover. Telefon zawsze z ikoną słuchawki.
- Przycisk do ukrytej strony znika (`cel-linku.html` v1), `kotwica_celu` doklejana jak v1.

### 9.8 Ikony

Jeden zestaw SVG (`partials/ikony.html` jako sprite + `ikona.html`), kreska 1,75 px,
`stroke-linecap: round`, `currentColor`, 20–28 px, klucze **dokładnie** z listy kontraktu; nieznany
klucz = `errorf` (jak v1). Ikony przerysować spójnie (można wyjść od rysunków v1). Żadnych emoji ani
glifów Unicode jako ikon. Ikona nigdy w kolorowym kwadracie nad kartą.

### 9.9 Zdjęcia

Przez Hugo (`zdjecie-zasob.html` + `image.html` + `figura.html` z v1): WebP 480/800/1200, ale nigdy
szerzej niż oryginał (oryginały mają ≤ 800 px), `alt` z treści, `width`/`height`, `loading="lazy"`
poza hero, `decoding="async"`, `sizes` zgodne z faktycznym miejscem (`100vw` telefon, `42vw` lewa
strefa, `50vw` plansza, `46vw` mozaika). Każde zdjęcie z `podpis` ma `<figcaption>` w `--st-maly`.
Zdjęcia tylko z `assets/images/`; żadnych zdjęć spoza gabinetu.

---

## 10. Każdy typ bloku z `docs/KONTRAKT-BLOKOW.md`

Każdy typ ma `layouts/partials/blocks/<typ>.html` (sprawdza `tools/sprawdz-kontrakt.py`) i czyta te
same pola co v1. Logikę danych przejąć z v1; zmieniać znaczniki i klasy.

### `hero`
§7. `pokaz_telefon` = przycisk wypełniony z pierwszym numerem. `fakty` = wiersze z ikoną.
`plakietka` = kafel w mozaice (główna) / pole przy zdjęciu (podstrona). `ikona` pomijana.

### `tekst`
- **Bez zdjęcia**: `h2` i treść od osi; `nadtytul` pod `h2`; `wstep` `--st-lead`; `tresc`
  `--st-tekst` w mierze 66ch. Lewa strefa nie zostaje pusta przypadkiem: gdy blok ma `ramka`, ramka
  stoi w lewej strefie, przyklejona (`sticky; top: 96px`) na desktopie; bez ramki krótki blok
  (< 600 znaków) przesuwa `h2` na lewy margines i tekst zostaje na osi (nagłówek „wisi” w lewej
  strefie). Ramka na telefonie pod treścią.
- **Ze zdjęciem**: zdjęcie w lewej strefie (kolumny 1–5), w kadrze oryginalnym, najwyżej 520 px
  szerokości, `podpis` pod spodem; tekst i bloki dołączone od osi. `strona_zdjecia: prawa` → lustrzane
  odbicie (zdjęcie w kolumnach 8–12, tekst w 1–7); oś pozostaje dla nagłówka bloku (kontrakt pozwala
  na pominięcie, ale klientka wybiera stronę w panelu, więc ją respektujemy).
- **Wyróżniony ze zdjęciem** (bruksizm): „kwadratowa plansza”. Pełne pasmo `--pole`,
  `min-height: 80svh`, podział 50/50. Zdjęcie w kadrze 1:1 (`Fill 800x800`), wyświetlane do 560 px,
  pionowo wyśrodkowane, `podpis` pod nim `--na-polu-ciche`. Druga połowa: `h2` (reguła długości;
  dziś 64 znaki → `--st-naglowek`, 2–3 wiersze), `nadtytul` jako zdanie, `tresc`, lista z ptaszkami
  (ptaszek `--na-polu`), `przycisk` na dole jako komórka `--papier` z pismem `--pole`, 64 px.
- **Portret** (zdjęcie pionowe, `strona_zdjecia: lewa`, proporcja wyższa niż 1:1, wykrywane po
  wymiarach pliku, nie po nazwie): „portret jako inicjał”. `h2` w lewej strefie. Od osi pierwszy
  akapit `--st-lead`, portret w kadrze 1:1 z górnej części (`Fill 600x600 top`), `float: left`,
  wysokość ok. 6 wierszy (220–240 px), `shape-outside` nie potrzebny (kwadrat). Reszta tekstu
  `--st-tekst`. Telefon: portret 120 px z opływem.
- `wypunktowanie: ptaszki` → rysowany ptaszek 22 px `--akcent`. `ramka` → blok `ramka` pod treścią.
  `przycisk` domyślnie wypełniony. `pokaz_telefony` → przyciski wszystkich numerów.

### `karty`
**Nie siatka jednakowych kart.**
- Karty z samym tytułem i ceną (`tytul` + `cena`): **menu cen**. `h2` i `wstep` w lewej strefie; od
  osi wiersze: nazwa `--st-lead` z lewej, kwota Young Serif `--st-naglowek` `tabular-nums` z prawej
  na wspólnej linii bazowej, „zł” przy każdej kwocie (format `cena.html`), między nimi pusta przestrzeń
  (bez kropek i linii), odstęp wierszy `--s-5`. ≥ 8 pozycji → dwie kolumny wierszy. `przycisk`
  dołączony pod listą, od osi. Na polu: kwoty `--na-polu`.
- Karty z treścią: lista typograficzna w `kolumny` kolumnach CSS (2/3/4 → 2/3/3 na desktopie, 1 na
  telefonie), od osi albo na pełną szerokość przy 3+ kolumnach. Element: `ikona` 24 px w linii
  tytułu (opcjonalnie), `tytul` Atkinson 700 `--st-lead`, `tresc` `--st-tekst`, `cena` Young Serif
  `--st-lead` pod spodem. Elementy oddziela odstęp `--s-7`, bez tła, bez obrysu, bez cienia.
  `strona` → cały element linkiem: tytuł podkreślony, hover tło `--papier-2` (na polu `--pole-2`),
  strzałka SVG.
- `wypunktowanie: ptaszki` w treści karty → ptaszki jak w `lista`.

### `faq`
„Pasmo na pytanie”. Pierwsze pasmo: `h2` (domyślnie i18n „Najczęstsze pytania”) w `--st-wystawa`
na `--pole` (gdy blok wyróżniony albo na stronie głównej) albo na `--papier-2`. Każda para to pasmo na
pełną szerokość, naprzemiennie `--papier` / `--papier-2`, bez fug: pytanie `<h3>` (Atkinson 700
`--st-lead`) w lewej strefie, odpowiedź od osi w `--st-tekst`, wspólna pierwsza linia bazowa.
**Wszystkie odpowiedzi widoczne**, bez rozwijania. JSON-LD `FAQPage` jak v1 (tekst = widoczny tekst).
Linki w odpowiedziach przez `render-link`. Dołączony z pustym nagłówkiem → same pasma. Telefon:
pytanie nad odpowiedzią, padding 32 px.

### `cennik`
- Prawdziwa `<table id="cennik-tabela">`: kategoria = `<tbody id="grupa-<id>">` z wierszem
  `<th scope="rowgroup" colspan>` w Young Serif `--st-lead` na `--papier-2`; pozycja: nazwa
  (Atkinson 600 `--st-tekst`), `uwagi` pod nią `--st-maly` `--pismo-ciche`, kwota w prawej kolumnie
  `tabular-nums` `white-space: nowrap` (format v1: „250–400 zł” z twardą spacją, `cennik-pozycja.html`
  i `cena.html` bez zmian). Linie wierszy 1 px `--papier-3`. `kolumna` → nagłówek kolumny.
- `wyszukiwarka: true` (strona cennika): lewa strefa przyklejona (`sticky; top: 96px`): `wstep`
  jako podpis, pole „Szukaj zabiegu” (`id="szukaj-ceny"`, 56 px, wypełnione `--papier-2`, obrys 2 px
  `--pismo-ciche`, fokus 3 px `--akcent`, ikona lupy SVG, podpowiedź `napisy.cennik_podpowiedz`),
  licznik na żywo „Pasujące pozycje: 4 z 30” (`aria-live="polite"`), spis kategorii (`kategorie[].skrot`)
  jako pionowa lista zwykłych linków do `#grupa-<id>`, bez pigułek. Tabela od osi. Brak wyników →
  komunikat „Nie znaleziono” z przyciskiem „Wyczyść” i przyciskiem telefonu (logika v1). Bez JS pole
  ukryte (`hidden`, zdejmuje skrypt), tabela pełna.
- `informacja` (art. 66 k.c.) pod tabelą jako ramka `info`.
- Wybrane `kategorie` / `pozycje` na innej stronie → ta sama tabela bez wyszukiwarki i bez spisu,
  od osi.
- JSON-LD `OfferCatalog` jak v1. Telefon: jedna kolumna, nazwa się łamie, kwota nie; wyszukiwarka
  przyklejona pod paskiem, spis kategorii jako `<details>` „Kategorie”.

### `galeria`
„Mozaika bez fug” (sygnatura kierunku). Siatka 6 kolumn, `grid-auto-rows: clamp(140px, 14vw, 200px)`,
`grid-auto-flow: dense`, rozpiętość z proporcji pliku: poziome (≥ 1,2) = 3 kolumny × 2 rzędy, co
trzecie poziome = 4 kolumny × 2 rzędy, pionowe (≤ 0,85) = 2 kolumny × 3 rzędy, pozostałe 2 × 2. Kafel
to `<button>` z `<img>` (`object-fit: cover`) otwierający lightbox. `podpis` (gdy jest) leży pasem
`--st-maly` na `--papier-2` przy dolnej krawędzi kafla **pod** zdjęciem, w obrębie kafla (nie na
zdjęciu). `h2` domyślnie ukryty („Zdjęcia gabinetu”, tylko dla czytników, jak v1); niepusty `naglowek`
i `wstep` widoczne nad mozaiką od osi. Lightbox `id="lightbox"` jak v1 (`<dialog>`, strzałki, Esc,
fokus wraca na kafel, licznik słowami „zdjęcie 3 z 13”, podpis pod zdjęciem). Hover kafla: zdjęcie
`scale(1.03)` w 250 ms w obrębie kafla. Telefon: 2 kolumny bez fug, poziome na pełną szerokość.

### `godziny`
Karta wizyt (§8) bez zdania stanu: `h2` (domyślnie i18n „Godziny przyjęć”) w lewej strefie, pasek
tygodnia od osi (poziomy), tabela dla czytników, `tresc` pod spodem. Dołączony do bloku z kolumną →
wersja pionowa w kolumnie.

### `mapa`
`h2` w lewej strefie. Od osi: adres (`--st-naglowek`), `adres.dojazd`, parking, `tresc` (adres
i dojazd pomijane, gdy strona ma blok `kontakt`, jak v1), link „Otwórz w Mapach Google” (SVG strzałka,
`target="_blank" rel="noopener"`). Pod spodem od osi do prawego marginesu **bramka zgody** (element
z atrybutem bramki jak v1, `data-map`): płaski kafel `--papier-2` 16:9 (4:3 na telefonie), w środku
z lewej zdjęcie wejścia (to samo co w stopce, natywne 300 px, przeszczep z C), z prawej
`napisy.mapa_zgoda` w `--st-tekst` i przycisk wypełniony `napisy.mapa_przycisk` („Pokaż mapę”).
Ramka Google wstawiana dopiero po kliknięciu (logika v1, tytuł ramki z v1). Żadnego rysowanego planu
ulic.

### `cta`
„Wiersze wystawowe” (zamknięcie każdej strony). Pełne pasmo `--pole` (reguła §9.1). `h2`
(`naglowek`, reguła długości) od lewego marginesu, `tresc` `--st-lead` `--na-polu-ciche` od osi. Pod
spodem wiersze na pełną szerokość pola, naprzemiennie `--pole` / `--pole-2`, każdy min. 120 px
(desktop), tekst Young Serif `--st-wystawa`, wcięcie = `--margines`:
1. **„699 904 989”**: cały wiersz to `<a href="tel:+48699904989">`, z prawej słowo „Zadzwoń”
   `--st-tekst` 700 i ikona słuchawki; `wszystkie_telefony: true` → kolejne numery kolejnymi wierszami
   (etykieta numeru `--st-tekst` nad cyframi).
2. Godziny jednym wierszem z danych: „pon., śr., czw. 9–15 · wt. 15–19” (grupowanie dni o tych
   samych godzinach z `gabinet-model.html`, półpauza, `tabular-nums`). Tu „·” jest separatorem
   danych, dopuszczalnym; telefon: dni w jednym wierszu, godziny w drugim.
3. `przycisk` (np. „Dojazd i mapa”) jako wiersz-odnośnik w `--st-naglowek` ze strzałką SVG.
Hover wiersza-odnośnika: tło `--pole-2` ↔ `--pole`, strzałka +4 px. Telefon: numer
`clamp(2rem, 9vw, 2.6rem)` w jednym wierszu (11 znaków × ok. 0,55 em × 36 px ≈ 220 px < 358 px).
Dołączony: bez nagłówka. E-maila nie ma (jak v1).

### `kontakt`
„Adres w wierszach” na papierze. Wiersze na zmianę `--papier` / `--papier-2`: etykieta w lewej
strefie (`--st-tekst` `--pismo-ciche`: „Telefon do rejestracji” z `telefony[].etykieta`, „Adres”,
„Parking”), wartość od osi w Young Serif `--st-naglowek`: telefony (linki `tel:`), adres (link do Map
Google, nowa karta), parking (`adres.parking`), `adres.dojazd` pod adresem w `--st-tekst`. **E-mail
tylko gdy `gabinet.email` niepusty** (dziś pusty → brak wiersza; nie dodawać „e-mail wkrótce”).
`tresc` nad wierszami od osi. `bok` → karta wizyt w lewej strefie, przyklejona; wtedy etykiety
wierszy idą nad wartość, a wiersze od osi. Bloki dołączone (np. `tekst` ze zdjęciem wejścia, `mapa`)
w kolumnie od osi. Telefon: etykieta nad wartością, `bok` pod treścią.

### `lista`
`wstep` nad listą. `ptaszki`: rysowany ptaszek 22 px `--akcent` (na polu `--na-polu`); `minusy`:
kreska 16×3 px `--pismo-ciche` z ukrytym tekstem „nie” dla czytnika (jak v1); `zwykla`: kwadratowa
kropka 6 px `--pismo`. Punkty `--st-tekst` (≤ 4 krótkie punkty: `--st-lead`), odstęp `--s-4`. ≥ 7
punktów → 2 kolumny od 900 px. Bez emoji.

### `ramka`
Płaski kafel bez obrysu i bez kolorowego paska z boku: `info` → `--akcent-tlo`, `uwaga` →
`--uwaga-tlo` z `--uwaga-pismo`, `ok` → `--ok-tlo` z `--ok-pismo` (ikona). Ikona 28 px (`ikona` albo
domyślna dla rodzaju) w linii z pierwszym wierszem, ukryty prefiks „Informacja:” / „Uwaga:” (i18n).
Padding 28/32 px, treść `--st-tekst`, `wypunktowanie` jak w `lista`. Na polu `--pole` ramka staje się
`--pole-2` z `--na-polu`.

### `kroki`
„Schodki”. `<ol>` (numery semantyczne; wizualnie bez „01/02”, kolejność niesie pozycja schodka). Tytuł
kroku Young Serif `--st-naglowek`, `tresc` pod nim `--st-tekst`, miara 34–40ch. Każdy kolejny krok
wcięty o jedną kolumnę siatki (na pełnej szerokości: od osi 6, 7, 8, 9; w kolumnie treści: o 1/8
szerokości kolumny). > 5 kroków → co 4 stopnie powrót do osi. Ostatni krok: tytuł `--akcent` (jedyne
wyróżnienie, cały tytuł, nie słowo). Odstęp między krokami `--s-7`. Telefon: wcięcie 6vw na stopień,
najwyżej 18vw. Bez JS wszystko widoczne (nic się nie rozwija).

### `tabela`
Prawdziwa `<table>` z `<caption>` = `podpis` (`--st-maly`, nad tabelą), nagłówki kolumn Atkinson 700
`--st-tekst` na `--papier-3`, komórki Markdown w wierszu, linie wierszy 1 px `--papier-3`, ostatnia
kolumna „Cena” z cennika (Young Serif `--st-lead`, `tabular-nums`, do prawej). Desktop: od osi do
prawego marginesu; 4+ kolumny → pełna szerokość. **Telefon: każdy wiersz jako blok** (`display: grid`,
etykieta kolumny z `data-label` nad wartością), bez przewijania w bok.

### `lista_uslug`
„Tabela z miniaturami”. `h2` (reguła długości) od lewego marginesu na pełną szerokość, `wstep`
`--st-lead` w lewej strefie, wyrównany do dołu względem pierwszego wiersza. Od osi lista (`<ul>`)
wierszy, każdy w całości linkiem do strony usługi:
miniatura 3:2 szerokości 120 px (**pierwsze zdjęcie strony usługi**: jej `hero.zdjecie`, a gdy go
brak, pierwszy `zdjecie` w `sekcje`; brak → bez miniatury, wiersz bez dziury; `alt=""`, bo nazwa
usługi stoi obok), nazwa (`usluga.nazwa` / `title`) Atkinson 700 `--st-lead`, `usluga.skrot`
`--st-tekst` pod nią, z prawej „od 300 zł” (`napisy.karta_cena_od` / i18n + `cena_od` przez
`cena.html`) Young Serif `--st-lead` i strzałka SVG. Wiersze oddziela odstęp `--s-5` (bez linii);
hover/fokus: tło `--papier-2`, strzałka +4 px. `tylko_wyroznione` przestrzegane; `kolumny` (2+) →
od 1200 px dwie kolumny wierszy na pełnej szerokości, poniżej jedna. Telefon: miniatura 88 px z lewej,
nazwa i cena w pierwszym wierszu, skrót pod spodem. Ta lista daje stronie głównej ≥ 9 dodatkowych
zdjęć (podłoga zdjęć taste-skill).

### `pasek_zaufania`
„Nazwy w kolumnach”. `h2` w lewej strefie (`--st-naglowek`, widoczny). Od osi siatka 2 × 2 (4
atuty; 3 → 3 kolumny, 5–6 → 3 kolumny): `tytul` Atkinson 700 `--st-lead`, `tekst` `--st-tekst`
`--pismo-ciche`. `ikona` 24 px w linii tytułu, w kolorze pisma (bez kwadratu). Bez ramek, bez tła,
bez hover. Telefon: `h2`, potem 2 × 2 (1 kolumna poniżej 360 px).

### `cytat`
`<blockquote>` Young Serif `--st-naglowek` od osi (≤ 3–4 wiersze na desktopie; dłuższy cytat →
`--st-lead` Atkinson), `autor` w `<cite>` `--st-tekst` `--pismo-ciche` po półpauzie. Bez ozdobnych
cudzysłowów w dużym rozmiarze (cudzysłowy „ ” z treści zostają). Na polu `--na-polu`.

### `powiazane`
„Zobacz też”: od osi wiersze-odnośniki, `etykieta` (albo tytuł strony) Atkinson 700 `--st-lead`
z podkreśleniem 2 px i strzałką SVG, `opis` (albo `usluga.skrot`) `--st-tekst` `--pismo-ciche` pod
spodem. 4+ elementy → 2 kolumny. Hover tło `--papier-2` na całym wierszu. Bez nagłówka → same wiersze.
Odnośniki do ukrytych stron znikają (`cel-linku`).

### `rezerwacja`
Jak v1: `wlaczona: false` albo brak `url` → nic (dziś nic). Włączona: karta wizyt (`--papier-2`)
z przyciskiem głównym do serwisu (`target="_blank" rel="noopener noreferrer"`, etykieta z danych),
`potwierdzona: false` → ramka `uwaga` „w przygotowaniu” (i18n), `nota`, telefony jako druga droga.

### `formularz`
**Zachowanie identyczne z v1.** Dziś blok jest zakomentowany w treści, więc nic się nie renderuje.
Partial musi istnieć i działać jak v1, gdy blok wróci: te same pola i teksty (`napisy.formularz_*`),
ostrzeżenie o danych o zdrowiu w ramce `uwaga`, zgoda, pole-pułapka, `method="post"`, notka, że nic nie
jest wysyłane, komunikat po wypełnieniu. Wygląd pól: etykieta nad polem, wysokość 56 px, tło
`--papier`, obrys 2 px `--pismo-ciche`, fokus obrys 3 px `--akcent`, `accent-color: var(--akcent)`
dla pola zgody, błąd = tekst `--uwaga-pismo` pod polem z ikoną i nazwą problemu. Bez e-maila
gabinetu.

### `tresc_z_bokiem`
Treść (nagłówek, `wstep`, `tresc`, bloki dołączone: `kroki`, `tekst`, `przycisk`) od osi; **karta
wizyt (`bok`) w lewej strefie, przyklejona** (`sticky; top: 96px`), `--papier-2`: nagłówek boku
(Young Serif `--st-lead`), `godziny: true` → pasek tygodnia pionowy, `pozycje` z cenami
(`cennik-pozycja`) i `informacja`, `notka`, przyciski telefonów (wypełnione), `przycisk`, `adres`,
`notka_dol`. Brak `bok` → godziny i telefony (zachowanie v1). Telefon: karta pod treścią (kontrakt);
na stronie głównej karta stoi zaraz pod `wstep`.

### `przycisk`
§9.7. Pojedynczy przycisk od osi (albo w kolumnie bloku, do którego jest dołączony).

### `spis`
„Na tej stronie”: w lewej strefie, przyklejony (`sticky; top: 96px`), pionowa lista zwykłych linków
`--st-tekst` z podkreśleniem; aktywna sekcja (IntersectionObserver) pogrubiona i z kwadratem 6 px
`--akcent` przed linkiem (nie tylko kolor). `naglowek` tylko dla czytników. Telefon: `<details>`
„Spis treści” (i18n) pod pasmem tytułowym, otwierany dotknięciem. Bez pigułek, bez przewijania w bok.

---

## 11. Podstrony

- **Usługa** (`/higienizacja/` itd.): pasmo tytułowe ze zdjęciem i linią ceny „od”, kolumna do
  czytania na osi, bloki wg §10, `powiazane` → `cta` → stopka. Tryb Read: tekst 19–20 px, pełny
  kontrast, interlinia 1.6, żadnego ruchu w treści poza wejściami części sekcji.
- **Cennik** (`/cennik/`): pasmo tytułowe bez zdjęcia, blok `cennik` z wyszukiwarką (§10), ramka
  `informacja`, `cta`. Zdjęć brak i nie dodajemy ich (WARN podłogi zdjęć inspektora jest tu
  uzasadniony).
- **Kontakt** (`/kontakt/`): pasmo tytułowe, `kontakt` z kartą wizyt w lewej strefie, `tekst` ze
  zdjęciem wejścia, `mapa` z bramką zgody (zdjęcie wejścia + zgoda), `cta`.
- **Galeria** (`/galeria/`): pasmo tytułowe, mozaika bez fug na pełną szerokość treści, lightbox.
- **O gabinecie** (`/o-mnie/`): portret jako inicjał, cytat, karty z treścią.
- **Pierwsza wizyta**: schodki na pełnej szerokości (od osi 6–9), karta wizyt w `bok`.
- **Polityka prywatności**: tryb Read, `waska`, bez lewej strefy, `spis` gdy jest.
- **404** (`404.html`, dane `strona_404`): pasmo tytułowe bez zdjęcia; `nadtytul` („Błąd 404”) jako
  zdanie pod `h1` (`naglowek`), `tresc`, przycisk „Wróć na stronę główną” (wypełniony), `notka`
  `--pismo-ciche`; „Dokąd dalej” (`linki_naglowek`, `linki_wstep`) jako wiersze `powiazane` z
  `linki[]` (+ strona główna z `opis_glownej`); karta wizyt z `ramka_telefon` (przycisk telefonu)
  i `ramka_adres` (adres). Linki 404 z prefiksem `baseURL` (działa pod `/test/`).
- **robots.txt**, `noindex` (`ukryj_przed_wyszukiwarkami` albo `params.robocza`), JSON-LD
  (`jsonld.html`), okruszki, `render-link.html` (odnośniki `/slug/` → `relref`/`RelPermalink`
  z `baseURL`), shortcode `gabinet`, `og-zdjecie.html`, favicon i manifest: **1:1 z v1**.

---

## 12. Ruch

Tylko `transform`, `opacity`, `clip-path`. Wszystko z odpowiednikiem
`@media (prefers-reduced-motion: reduce)`: brak przesunięć i masek, treść widoczna od razu, przejścia
kolorów ≤ 150 ms zostają. Budżet inspektora: ≥ 8 poruszających się elementów, jedna sygnatura.

1. **Sygnatura: maskowany nagłówek** (`h1` strony głównej; na podstronach `h1` pasma, 600 ms). Po
   `document.fonts.ready` skrypt dzieli `h1` na wiersze (`Range.getClientRects` po słowach), każdy
   wiersz w `<span>` z `overflow: clip`, wejście `translateY(105%) → 0`, `--t-maska`,
   `--ease-wyjscie`, kolejne wiersze +110 ms. Przy zmianie rozmiaru okna bez ponownej animacji
   (scalenie z powrotem w tekst). Domyślny stan jest widoczny; klasę chowającą dodaje skrypt tuż przed
   animacją.
2. **Druk się układa**: kafle mozaiki wchodzą kolejno (zdjęcie, plakietka, fakty, karta) przez
   `clip-path: inset(0 0 100% 0) → inset(-6px)`, `--t-wejscie`, odstęp 80 ms. Jeden ruch. Stan
   końcowy musi być wartością `inset()`: przejścia `inset() ↔ none` przeglądarka nie interpoluje.
3. **Dziś się zamalowuje** (§8), po mozaice.
4. **Jeden ruchomy obraz**: zdjęcie w mozaice `scale(1) → 1.04` przez 18 s, `ease-out`, raz.
5. **Wejścia części sekcji**: nagłówek → tekst → zdjęcie/lista, `translateY(24px)` + `opacity`,
   600 ms, odstęp 70 ms, raz (IntersectionObserver, `rootMargin: 0px 0px -10% 0px`). Schodki wchodzą
   stopień po stopniu z przesunięciem poziomym 16 px. Stan ukryty **wyłącznie** w
   `@media (prefers-reduced-motion: no-preference) { .js [data-wejscie]:not(.widoczne) {…} }`;
   `.js` dodaje skrypt na `<html>` na samym początku `<head>`. Bez JS i przy ograniczeniu ruchu nic nie
   jest ukryte (v1 tego testu nie przechodził). Treść nad zgięciem nie czeka na wejście.
6. **Odpowiedź kontrolek**: przyciski (ton + `translateY(1px)`), wiersze-odnośniki (tło + strzałka
   4 px, 150 ms), kafle galerii (`scale(1.03)`), podmenu (`opacity` + `translateY(-4px → 0)`, 150 ms),
   szuflada (z prawej, 250 ms), linki (grubość podkreślenia 1 → 2 px).
7. Zakazane: odbijanie, pętle, pulsująca kropka, unoszenie kart, paralaksa tła, przejmowanie
   przewijania, przypinanie sceny na kilka ekranów.

---

## 13. Telefon (390 px jako osobna kompozycja)

- Marginesy 20 px (16 px poniżej 360), jedna kolumna, oś = lewy margines. Zero przewijania w bok
  (tabele jako bloki, spis w `<details>`).
- Telefon do rejestracji zawsze pod kciukiem: karta w pierwszym ekranie, dolny pasek (chowany przy
  karcie i `cta`), szuflada. Wszystkie `tel:+48699904989` (format z `gabinet-model.html`).
- Cele dotyku ≥ 48×48 px, przyciski główne 56 px na pełną szerokość, odstęp między linkami w listach
  ≥ 12 px. Tekst ≥ 18 px, nic poniżej 15 px.
- Zawartość lewej strefy trafia nad lub pod kolumnę (zdjęcie nad nagłówkiem, karta wizyt pod wstępem
  na głównej, pod treścią na podstronach). Każdy ekran ma nagłówek sekcji.
- Nagłówki przyklejone na desktopie nie przyklejają się na telefonie (`position: static` < 900 px),
  z wyjątkiem wyszukiwarki cennika.
- Sprawdzić: 360, 390, 768, 1024, 1280, 1440; powiększenie tekstu 200% (układ na `rem`).

---

## 14. Dostępność i powierzchnie przeglądarki

- Fokus widoczny wszędzie: `outline: 3px solid var(--pismo)` z `outline-offset: 2px` na papierze,
  `--na-polu` na polu, `--na-atramencie` na stopce. Link „Przejdź do treści” (i18n jak v1) jako
  pierwszy element.
- `::selection` = `--akcent-tlo` + `--pismo`; `caret-color: var(--akcent)`; `accent-color:
  var(--akcent)`; `text-underline-offset: .2em`, `text-decoration-thickness: 2px` (hover 3 px);
  pasek przewijania szuflady i lightboxa w tonach `--papier-3`/`--pismo-ciche`
  (`scrollbar-color`); `tabular-nums` w danych.
- Kolor nigdy nie jest jedynym znakiem stanu („dziś”, „nieczynne”, pogrubienie aktywnej sekcji spisu).
- `lang="pl"`, jeden `h1` na stronę, hierarchia nagłówków bez przeskoków, `aria-current` w menu
  i okruszkach.

---

## 15. Struktura motywu i co przejąć z v1

```
themes/v2-nowa/
  DESIGN.md                      (ten plik)
  assets/css/style.css           tokeny (§3) + komponenty; bloki [data-paleta] dla morska/granat/szalwia
  assets/css/hugo.css            (jeśli v1 go potrzebuje do składni Hugo — przejrzeć i przejąć)
  assets/js/app.js               przepisany z v1: motyw, szuflada, podmenu, stan (Europe/Warsaw),
                                 lightbox, mapa (zgoda), cennik (filtr), wejścia, maska h1, dolny pasek
  assets/meta/favicon.svg, site.webmanifest   z v1 (kolory przez paleta.html / kolory-motywu.html)
  i18n/pl.yaml                   wszystkie stałe napisy (klucze v1 + nowe: §8, „dziś”, „nieczynne”,
                                 „Rejestracja telefoniczna”, dayNext*, „Pasujące pozycje: {n} z {m}”)
  layouts/_default/baseof.html, home.html, single.html, _markup/render-link.html
  layouts/404.html, robots.txt, shortcodes/gabinet.html
  layouts/partials/…             *-model.html, jsonld, okruszki*, cel-linku, menu-link, cena,
                                 cennik-pozycja, markdown*, image/figura/zdjecie-zasob, og-zdjecie,
                                 paleta, kolory-motywu, sekcje (z regułą pól §9.1), h2 (§9.6),
                                 ikony/ikona, godziny-tabela, tel/telefon-btn/telefony-*,
                                 karta-wizyt.html (nowy), mozaika-hero.html (nowy), fonty.html (nowy)
  layouts/partials/blocks/<23 typy>.html
  static/fonts/*.woff2 + OFL-*.txt
  static/favicon.svg, apple-touch-icon.png   z v1
```

Przejmowanie: kopiować partiale danych z v1 i zmieniać tylko znaczniki/klasy. Nie zmieniać
`content/`, `data/`, `static/admin/`, `hugo.yaml`, `themes/v1-klasyczna/`; `layouts/` w korzeniu
pusty. Kod nie może zawierać tekstów kontraktu kierunku (tezy, opisów idei) jako komentarzy-kostiumów
w HTML; komentarze w szablonach tylko techniczne.

---

## 16. Zakazy

**Tells taste-skill i house rules**
- Eyebrow, pigułka, etykieta nad nagłówkiem (v1 ma ją przy `nadtytul`). `nadtytul` zawsze zdaniem
  pod nagłówkiem.
- Rzędy jednakowych kart z ikoną w kolorowym kwadracie (v1: usługi, atuty, karty), bento, karty
  w kartach.
- Cienie na elementach w spoczynku, zaokrąglenia, obrysy 1 px, cienkie linie dekoracyjne, separatory.
- Gradienty (także `.cta-band` z v1), tekst gradientowy, szkło, rozmycie, poświaty.
- Krem, pergamin, terakota, fiolet, indygo, neon na czerni. Tło to chłodna biel.
- Monospace, małe rozstrzelone wersaliki, wersaliki dłuższe niż 3 słowa (wersaliki klientki w treści
  zostają), numeracja 01/02/03, „Krok 2”.
- Wyróżnione jedno słowo w nagłówku (kursywa, kolor, podkreślenie).
- Więcej niż dwa kroje; więcej niż pięć stopni pisma.
- Wyśrodkowane bloki tekstu (wyjątek: plakietka „od 1995 roku”).
- Szary tekst „dla elegancji”: `--pismo-ciche` tylko na notki i nadal ≥ 7:1.
- Puste pół ekranu, pas pustki wyższy niż pół ekranu, nierówne marginesy.
- Mikro-meta: współrzędne, czas lokalny jako ozdoba, „Scroll”, ciągi rozdzielone „·” jako dekoracja.
- Słowa-wypełniacze w napisach motywu: „Dowiedz się więcej”, „Zacznij”, „Odkryj”. Przyciski nazywają
  czynność („Zadzwoń: 699 904 989”, „Zobacz pełny cennik”, „Pokaż mapę”, „Wróć na stronę główną”).
- Myślnik jako nawyk w napisach motywu (w treści klientki zostaje).

**Antywzorce impeccable (`craft-floor.md`)**
- Szablon „hero z dużą liczbą” (30 lat + rząd statystyk). „od 1995 roku” to plakietka z panelu.
- Kolorowy `border-left` / `border-right` > 1 px w ramkach, cytatach, listach.
- Twarde przesunięte cienie; geometryczne maski udające kontur postaci (portret jest kwadratem).
- Emoji i glify Unicode zamiast ikon (strzałki to SVG).
- Systemowy krój jako głos wystawowy (Young Serif self-hosted).
- Modal tam, gdzie nie trzeba (jedyny `<dialog>`: lightbox).
- Domyślne powierzchnie przeglądarki (§14).

**Zasady gabinetu (twarde)**
- Art. 14 ustawy o działalności leczniczej: w `i18n/pl.yaml`, `alt`, `aria-label`, `title` żadnych
  „najlepszy”, „gwarancja/gwarantujemy”, „bezboleśnie”, „bez bólu”, „bez stresu”, „promocja”,
  „rabat”, „numer jeden”, „najtańszy”, obietnic efektu (pełna lista w `tools/kontrola-strony.py`).
  Zdanie stanu nie obiecuje, że ktoś odbierze.
- Zero zasobów z obcych serwerów: fonty w motywie, ikony inline SVG, zdjęcia tylko z `assets/images/`,
  Google Maps dopiero po kliknięciu zgody. Bez Google Fonts, bez CDN, bez picsum/Unsplash.
- E-mail i formularz dokładnie jak v1 (e-mail tylko gdy niepusty, formularz tylko gdy w treści).
- Cennik z `data/cennik.yaml` jest źródłem prawdy; motyw tylko go wyświetla.
- Żadnych wymyślonych opinii, gwiazdek, liczników pacjentów, logotypów, statystyk.
- Zdjęcia nigdy powyżej natywnej rozdzielczości (wszystkie ≤ 800 px).

---

## 17. Bramki i podgląd

Przed oddaniem (dla `--theme v2-nowa`):

1. `python tools/sprawdz-kontrakt.py` → OK (23 partiale bloków, palety w `style.css` i `paleta.html`).
2. Build bez WARN/ERROR:
   `HUGO_RESOURCEDIR=<katalog>/res HUGO_PARAMS_ROBOCZA=true hugo --gc --minify --theme v2-nowa --baseURL http://localhost:<PORT>/test/ -d <katalog>/site/test`
3. `python tools/kontrola-strony.py <katalog>/site/test --baseurl http://localhost:<PORT>/test/` → 0 błędów.
4. `node .claude/skills/design-taste-frontend/scripts/lint.mjs themes/v2-nowa` i
   `node …/inspect.mjs http://localhost:<PORT>/test/` przy 1440/768/390 → 0 FAIL poza uzasadnionymi
   w §18 (długi `h1` na telefonie, podłoga zdjęć na cenniku, brak filmu).
5. Krytyka `references/critique.md` (maks. 3 rundy, zapis w formacie ROUND n) na zrzutach: strona
   główna, usługa, cennik, kontakt, galeria, 404; jasny i ciemny; 4 palety (palety sprawdzać kopią
   danych w osobnym katalogu roboczym albo zmienną środowiskową, nigdy zmianą `data/ustawienia.yaml`).
6. `impeccable detect --json` raz na końcu na zbudowanym HTML.
7. Wersja dla klientki: `--baseURL http://dobrydentysta.legnica.pl/test/`, z `noindex`
   (`HUGO_PARAMS_ROBOCZA=true` albo `ukryj_przed_wyszukiwarkami: true`) i `Disallow: /`.

---

## 18. Ryzyka i pytania do klientki (lista na prezentację)

1. **Nagłówek banera** ma 82 znaki (14 słów). Na desktopie mieści się w 2 wierszach (44 px), na
   telefonie zajmuje 4. Propozycja do wpisania w panelu (decyzja klientki, motyw niczego nie skraca):
   krótki `h1`, np. „Twoja dentystka na Złotoryjskiej”, a motto jako `cytat` przy portrecie. Wtedy
   `h1` dostaje stopień wystawowy.
2. **Długi wstęp banera** z wersalikami („BOISZ SIĘ DENTYSTY I IGIEŁ ??”) stoi w dwóch kolumnach
   od osi; redakcja w panelu dałaby lepszy pierwszy ekran.
3. **Zdjęcia mają najwyżej 800 px**, dlatego żadne nie jest pokazywane szerzej niż ok. 660 px CSS;
   na ekranach 2× są miękkie. Nowe zdjęcia z panelu (do 2048 px) poprawią to bez zmian układu.
4. **FAQ jest w całości rozwinięte**, więc na stronie głównej zajmuje więcej miejsca niż w v1; to
   świadomy wybór dla starszych pacjentów.
5. Przy paletach innych niż bordo „kolor fotela” znika ze skojarzenia, ale kompozycja zostaje
   (cztery nakłady tej samej odbitki).
6. Brak filmu (WARN `no-footage`) jest świadomy: nie ma uczciwego nagrania tego gabinetu.
7. Runda decyzji z klientką się nie odbyła (podagent bez kanału do użytkownika). Na prezentacji pod
   `/test/` warto zapytać o punkt 1 i o to, czy pełne pola bordo nie są za mocne.

---

## 19. Zmiany po zrzutach (budowa motywu)

Wartości zmienione po krytyce zrzutów (taste-skill `inspect.mjs`, `critique.md`):

- Mozaika strony głównej: kolumny `7fr 2.4fr 4fr`, wysokość `clamp(460px, 68vh, 620px)` (zdjęcie
  ≥ 1/3 pierwszego ekranu, wciąż ≤ natywnych 794 px). Tablet 600–899 px: zdjęcie na całą szerokość
  (380 px), pod nim plakietka i fakty w lewej kolumnie, karta rejestracji w prawej.
- Plakietka „od 1995 roku”: `min(--st-wystawa, 20cqi)`, `max-width: 7ch` (5ch łamało „od / 1995”).
- Pasek tygodnia: flex zamiast siatki 7 kolumn; kolejne dni nieczynne złączone w jeden kafel
  („pt.–niedz. nieczynne”), godziny bez łamania.
- `h1`: ≤ 44 znaki → wystawa (powyżej 24 znaków na telefonie stopień nagłówka), 45–60 → nagłówek,
  > 60 → „zdanie”. Pasmo tytułowe: tytuł na pełną szerokość.
- `h2` dłuższy niż 40 znaków w bloku `tekst` ze zdjęciem i w planszy: osobny wiersz nad zdjęciem
  i tekstem (2 wiersze na desktopie zamiast 3).
- Cytat: `clamp(1.5rem, …, 2.25rem)` (wypowiedź ≤ 36 px, reguła taste-skill), nie `--st-naglowek`.
- Galeria: wiersze równej wysokości (flex, szerokość z proporcji pliku), bez przycinania i bez dziur,
  zamiast siatki 6 kolumn z rozpiętościami (dawała puste pola).
- Miniatury w `lista_uslug` 180 px (zamiast 120; próg „prawdziwego zdjęcia” inspektora), miniatury
  także w `powiazane` (pierwsze zdjęcie strony docelowej, `alt=""`).
- `waska`: kolumny 4–10 jak w §9.2 (nie od osi).
- Spis treści (`spis`): lista „Na tej stronie” od osi, nieprzyklejona (blok stoi w jednej sekcji).
- Telefon: w pasku głównym ikona słuchawki obok „Menu”; dolny pasek kontaktowy pojawia się dopiero
  za pierwszym ekranem i przy przewijaniu w górę (nie zasłania nagłówków).
- Podmenu i szuflada zamknięte = `display: none` (wejście animacją), żeby ukryta treść nie wisiała
  w drzewie dostępności.

---

## 20. Poprawki po przeglądzie (runda 1)

Zmiany, które nadpisują wcześniejsze punkty tego dokumentu (§7, §9.6, §10, §12, §13, §19):

- **Hierarchia nagłówków.** `h2` zawsze w `--st-naglowek`. Stopień „wystawa” jest tylko dla `h1`
  i liczb (cena w menu cen, numer w `cta`, linia adresu w stopce, plakietka). Na stronie z `h1`
  „zdanie” `h2` dostaje stopień `h1` (`--st-zdanie`: 26 px na telefonie, 48 px na desktopie).
  Dzięki temu `h2` nigdy nie jest większy niż `h1`. Nagłówek dłuższy niż 50 znaków w lewej strefie
  dostaje cały wiersz siatki (`h2--szeroki`), a treść od osi schodzi pod niego.
- **Baner strony głównej.** `h1` stoi nad mozaiką na pełnej szerokości. Jest na pierwszym ekranie
  przy 1366×768 i 390×664 i w kolejności czytania wyprzedza kartę rejestracji. Mozaika ma
  wysokość `clamp(420px, 60vh, 600px)`. Poniżej 600 px kafel faktów to pas z pełnym adresem
  („Złotoryjska 16/18 m. 10”) pod zdjęciem. Przy 600–899 px kafel pokazuje pełną listę faktów.
  Na stronie głównej z kartą w banerze górny pasek nie powtarza zdania stanu.
- **Nagłówek na telefonie.** Poniżej 600 px nie ma znaku zęba, a nazwa ma 17 px. Poniżej 380 px
  przycisk „Menu” to sama ikona (napis zostaje dla czytników). Ikona znaku nigdy się nie ściska
  (`flex: none`). Nazwa łamie się najwyżej na dwa wiersze i nigdy nie wchodzi pod przycisk
  słuchawki.
- **Pasek tygodnia.** W kontenerze węższym niż 300 px (karta przy 320 px, powiększenie 200%)
  kafel dni nieczynnych schodzi do drugiego wiersza. W trybie ciemnym „dziś” zamalowuje akcent
  (`--dzis-tlo`/`--dzis-pismo`), bo pole odcinało się od papieru tylko w 1,2:1. Na polu „dziś”
  zamalowuje papier, jak wcześniej.
- **Schodki.** Numer kroku na ekranie (licznik CSS w Young Serif, kolor akcentu). Tytuł kroku
  w `--st-lead`. Do 4 kroków wcięcie po jednej kolumnie. Przy 5 i więcej krokach oraz poniżej
  900 px nie ma wcięć (koniec zygzaka). Ostatni krok nie ma osobnego koloru.
- **Ruch.** Zostaje jeden autorski moment: układanie plakietki, faktów i karty w mozaice oraz
  zamalowanie „dziś”. Kroki wchodzą kolejno, a pozycje list (usługi, atuty, karty, zdjęcia galerii)
  układają się jedna po drugiej. Nagłówki i teksty sekcji nie wjeżdżają. Maski `h1` nie ma (`h1`
  i zdjęcie hero to LCP, widoczne od pierwszego malowania).
- **Lista usług i „Zobacz też”.** Miniatura to pierwsze zdjęcie strony, którego lista jeszcze nie
  pokazała (sekcje, potem galeria). Bez takiego zdjęcia wiersz nie ma miniatury, ale trzyma
  kolumnę tekstu. Poniżej 600 px miniatur nie ma. Widoczny napis wejścia („Zobacz szczegóły” albo
  `napisy.karta_szczegoly` z panelu) ze strzałką stoi przy wierszach usług i przy kartach z polem
  `strona`.
- **Rozwijane listy na telefonie** (spis, kategorie cennika): przycisk z `aria-expanded`
  i chevronem zamiast `<details>`. Bez JS lista jest widoczna, a przycisk ukryty.
- **Stopka.** Linia adresu to sam napis, bez zdjęcia wejścia. Bramka mapy nie powtarza zdjęcia
  wejścia, gdy stoi ono na tej samej stronie.
- **Kolejność w DOM.** W `kontakt` i `tresc_z_bokiem` treść stoi przed kartą z boku. Na desktopie
  kartę ustawia siatka, a na telefonie karta jest pod treścią (bez `order`).
- **`waska`.** Kolumny 4–9: po trzy kolumny wolne z każdej strony.
- **Blok bez nagłówka na początku sekcji** (`tekst`, opis galerii) zaczyna się od lewego
  marginesu, a nie od osi. `spis` od 900 px stoi na całą szerokość.
- **Dostępność.** Fokus kafla galerii to podwójny pierścień nad zdjęciem. Nazwa kafla brzmi
  „Powiększ zdjęcie: opis”. Schowany dolny pasek jest `inert`, a fokus w nim jest na tokenach pola.
  Podmenu otwiera najechanie albo przycisk, ale nie sam fokus. Esc je zamyka. Szuflada ustawia
  `inert` na reszcie strony. Po „Pokaż mapę” fokus przechodzi na ramkę mapy. Cele dotyku
  w okruszkach, stopce i przy „Dojazd i mapa” mają ≥ 44 px.
- **Cennik.** Jedna lewa krawędź w kolumnie nazw. Kwoty w Young Serif (zero bez kreski). Przy
  320–399 px tabela mieści się w kolumnie.
- **Fonty.** Preload Atkinson latin i Young Serif latin.

## 21. Poprawki po przeglądzie (runda 2)

- **Skład.** `partials/sklad.html` przechodzi po gotowym HTML-u nagłówka, treści i stopki.
  Zmienia tylko tekst między znacznikami: po jednoliterowych spójnikach i przyimkach (a, i, o, u,
  w, z) wstawia twardą spację, a grupy cyfr („699 904 989”) skleja. Treść w `content/` zostaje bez
  zmian. Wyszukiwarka cennika traktuje twardą spację jak zwykłą.
- **Skala.** `--st-naglowek` to `clamp(1.625rem, 1.05rem + 2.6vw, 3rem)` (ok. 27 px przy 390).
  `--st-zdanie` to `clamp(1.875rem, 1.2rem + 2.4vw, 3.375rem)` (30 px przy 390, 54 px przy 1440)
  i obejmuje h1 „zdanie” oraz „naglowek”. Na takich stronach h2 = zdanie / 1,3, więc h1 ≥ 1,3 × h2
  na każdej szerokości. Długi h1 strony głównej nie ma miary 34ch i przy 1280/1440 ma 2 wiersze.
- **Pasmo podstrony (§7.3).** Gdy `hero` nie ma zdjęcia, pasmo bierze zdjęcie gabinetu z galerii
  serwisu, którego strona nie pokazuje (`zdjecie-pasma.html`). Strona bez własnych zdjęć, np.
  polityka, zostaje z samym tekstem. Na desktopie zdjęcie ma wysokość pierwszego ekranu (4:5),
  h1 obok ma stopień „zdanie”.
- **Punkty przełamania w em** (75em, 56,25em, 37,5em, 23,75em), a `--tresc-max` w rem. Przy
  większej czcionce przeglądarki nagłówek sam przechodzi na „Menu”. Z rezerwacją online menu
  zwija się poniżej 100em, a przycisk rezerwacji w pasku znika poniżej 75em.
- **Mozaika** ma `min-height`, nie `height`. Rzędy rosną z treścią karty i faktów, zdjęcie nie
  wyznacza ich wysokości.
- **Galeria** ma fugę 3 px w kolorze tła. `sizes` odpowiada układowi rzędów.
- **Cennik i tabela.** Wiersze rozdziela krok tonu (co drugi `--tlo-2`), bez linii 1 px.
- **Lista usług.** Wiersz bez własnego zdjęcia w liście ze zdjęciami dostaje rysowany znak usługi
  (`usluga.ikona`) na `--tlo-2`. Miniatury są ozdobne (`alt=""`, `aria-hidden`).
- **Strona główna < 900 px.** Bez górnego paska. Przełącznik motywu jest w szufladzie, a bez JS
  jest ukryty. Bez JS dolny pasek stoi na końcu strony.
- **Stopka.** W linii © jest pełna nazwa podmiotu (`gabinet.nazwa`). „dziś” stoi pod nazwą dnia.
- **Fonty.** Preload obu podzbiorów (latin i latin-ext).

## 22. Poprawki po przeglądzie (runda 3)

- **Pasmo podstrony na telefonie.** Poziome zdjęcie w paśmie dostaje poniżej 900 px osobne źródło
  (`<source media>`) bez kadru 4:5, więc w polu 3:2 widać całe zdjęcie (`image.html`,
  `telefon_bez_kadru`). Pionowe zdjęcie stoi w polu 4:3 z ogniskiem `50% 15%`.
- **Dolny pasek.** Rezerwa pod paskiem jest w stopce, nie w `body`, więc po schowaniu paska na dole
  strony nie zostaje pas tła strony. Wysokość paska mierzy `app.js` (`--wys-paska-dolnego`,
  ResizeObserver). `html` ma `scroll-padding-bottom`, a `focusin` dosuwa element z fokusem nad
  pasek (WCAG 2.4.11). Kolumny `minmax(0, …)`, napisy się zawijają. Przy dużym tekście
  w przeglądarce strona nie przewija się w poziomie: stopka ma kolumny `auto-fit`, godziny
  w wąskiej kolumnie stają jedna pod drugą (container query), a nagłówek wyższy niż 1/5 okna
  przestaje się przyklejać.
- **Ruch.** Zdjęcia galerii (`data-wejscie-kafle`) wchodzą kafel po kaflu, przez `@keyframes`, nie
  przez `transition`, więc działa to także przy wczytaniu. Wiersze `cta` wchodzą jak pozycje list.
- **Menu cen < 600 px.** Nazwa w `--st-tekst`, kwota w `--st-lead` na linii bazowej ostatniego
  wiersza nazwy. Na telefonie zostaje 7 stopni pisma (15/18/21/24/30/35/43).
- **Ramka `ok`.** Neutralne tło sekcji (`--tlo-2`) i znak w kolorze akcentu, bez zieleni spoza
  palety. Tokeny `--ok-*` zostają nieużywane. Kolejne ramki stoją 16 px od siebie.
- **Pas zdjęć gabinetu** (`pas-zdjec.html`) przed `cta` na stronach, które nad nim pokazały mniej
  niż 4 zdjęcia (dziś kontakt i opinie). Bierze 2–3 zdjęcia z galerii, których strona nie pokazuje,
  z ich altami. Polityka prywatności to dokument prawny i zostaje bez zdjęć.
- **Lista usług.** Wiersz bez własnego zdjęcia dostaje nieużyte zdjęcie gabinetu z galerii.
  Rysowany znak zostaje tylko wtedy, gdy takiego zdjęcia nie ma.
- **Przycisk w nagłówku.** Pusty `napisy.przycisk_naglowka` daje „Umów wizytę”, jak w v1
  i w podpowiedzi panelu.
- **Priorytet zdjęć.** Gdy pasmo podstrony wzięło zdjęcie z galerii, żadne inne zdjęcie strony nie
  dostaje `fetchpriority=high`. Galeria daje priorytet tylko pierwszemu zdjęciu.
- **Skład.** „art. 66 § 1”: skrót, numer, paragraf i jego numer trzymają się twardymi spacjami.
- **Cele dotyku.** Akapit z samym odnośnikiem („Pełny cennik →”, klasa `p-odnosnik`
  z `markdown.html`), telefon w stopce i w bloku kontakt, znak, okruszki i „Start” w menu mają
  ≥ 44 px.
- **Drobne.** Mapa nie powtarza „Mapa dojazdu”, gdy blok ma własny nagłówek. W stopce nie ma
  podwójnego odstępu w adresie. Wstęp galerii na telefonie ma całą szerokość. Akapity po
  akapicie wiodącym nie opływają portretu. Stan godzin: „Otwieramy jutro o 15:00.”. Tytuł strony
  głównej i napisy formularza nie mają pauz.
