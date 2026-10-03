# Kontrakt bloków treści

Wspólna umowa między **treścią** (`content/`, `data/`), **panelem** (`static/admin/config.yml`)
i **szablonami** (`themes/*`). Każdy szablon musi umieć wyświetlić każdy blok opisany
poniżej, a panel może zapisywać tylko pola z tej listy. Dzięki temu zmiana szablonu
(`theme:` w `hugo.yaml`) nie wymaga żadnej zmiany w treści.

Wersja kontraktu: **3** (`params.kontraktBlokow` w `hugo.yaml`). Zmiany względem wersji 1
i 2 — na końcu pliku („Zmiany w wersji 2”, „Zmiany w wersji 3”).

Pilnuje tego `tools/sprawdz-kontrakt.py` (uruchamiany w CI przed budowaniem):

- każdy typ bloku z `config.yml` ma partial `layouts/partials/blocks/<typ>.html`
  w **każdym** szablonie w `themes/`,
- pola każdego typu w `config.yml` są dokładnie takie jak w tabelach poniżej
  (+ pola wspólne),
- partial bloku używa tylko pól ze swojej tabeli (`$b.<pole>`),
- katalog `layouts/` w korzeniu repozytorium jest pusty,
- `data/cennik.yaml`: identyfikatory kategorii i pozycji są niepuste i niepowtarzalne,
  a każda pozycja wskazuje istniejącą kategorię.

## Zasady treści

- W treści **nie ma HTML ani klas CSS** — tylko zwykły tekst, a w polach Markdown
  Markdown. Wygląd (kolory, kolumny, ikony, odstępy) to sprawa szablonu.
- Pola opisują **znaczenie**, nie wygląd: „ramka typu ostrzeżenie”, „lista zalet”,
  „ikona: ząb” — szablon sam decyduje, jak to narysować. Szablon może pominąć pole
  czysto wizualne (np. ikonę, liczbę kolumn), ale nie może zgubić treści.
- Ceny są **tylko** w `data/cennik.yaml`. Bloki wskazują kategorie albo pozycje
  cennika po identyfikatorze — nigdy nie przepisują kwot.
- Dane gabinetu (telefony, adres, godziny, rezerwacja) są tylko w `data/gabinet.yaml`;
  bloki „godziny”, „kontakt”, „mapa”, „cta”, „rezerwacja” je pokazują, nie przechowują.

## Gdzie są bloki — model sekcji

Strona główna (`content/_index.md`) i każda podstrona (`content/strony/<slug>/index.md`)
mają w front matter (YAML) **płaską listę** `sekcje`. Każdy element listy to jeden blok:

```yaml
sekcje:
  - type: tekst          # typ bloku - jedna z nazw poniżej
    wariant: domyslny    # opcjonalnie: tło sekcji
    naglowek: "O nas"
    tresc: |-
      Akapit w **Markdown**.
  - type: ramka          # dołączona do sekcji powyżej
    polacz: true
    rodzaj: uwaga
    tresc: "Ważna uwaga pod tekstem."
```

**Każdy blok to osobna sekcja strony**, z własnym nagłówkiem i wstępem. Blok z
`polacz: true` **dołącza do sekcji powyżej** (to samo tło, bez dużego odstępu) — tak
buduje się sekcję z kilku elementów, np. cennik + ramka z informacją + przycisk.

Gdy sekcja zaczyna się blokiem z **kolumną obok** — `tekst` ze zdjęciem,
`tresc_z_bokiem`, `kontakt` z polem `bok` — bloki dołączone stają **w kolumnie
tekstu**, a zdjęcie albo ramka z boku zostaje obok całej kolumny (np. tekst z ramką
godzin + kroki + karta rezerwacji + przycisk). To samo od dołączonego bloku
`tresc_z_bokiem` albo `kontakt` z `bok` (np. nagłówek sekcji w bloku `tekst`, pod nim
tekst z ramką z boku i kroki w jego kolumnie). Do kolumny trafiają bloki „wąskie”:
`tekst` bez zdjęcia, `ramka`, `kroki`, `lista`, `cytat`, `przycisk`, `rezerwacja`,
`godziny`; każdy inny blok (np. `karty`, `tabela`, `powiazane`, `cta`, `tekst` ze
zdjęciem) staje pod spodem, na całą szerokość, i zamyka kolumnę. Szablon bez kolumn
stawia wszystko po prostu pod spodem.

Blok dołączony z **pustym nagłówkiem** nie dostaje nagłówka domyślnego (np. FAQ
dołączone pod tekstem nie ma „Najczęstszych pytań”) — należy do sekcji, która już
ma nagłówek.
Nie ma osobnego poziomu „sekcja → bloki”: panel (Sveltia CMS) nie zagnieżdża list
ze zmiennym typem bezpośrednio, a płaska lista z jednym przełącznikiem jest prostsza
w obsłudze niż dwa poziomy rozwijanych list.

Szablon renderuje bloki po kolei: `range .Params.sekcje` →
`partial "blocks/<type>.html" (dict "blok" . "strona" $strona "nr" $indeks …)`.
Nieznany typ = ostrzeżenie `warnf`, a w CI ostrzeżenie przerywa publikację.
Szablon może pominąć `polacz` (każdy blok osobno — tak robi `v0-test`); szablon
`v1-klasyczna` grupuje bloki w `<section class="section">`.

Pierwszy blok typu `hero` jest **nagłówkiem strony** (`h1`): na stronie głównej duży
baner, na podstronie nagłówek z tytułem i wstępem. Strona bez `hero` na początku
dostaje nagłówek z tytułu strony (`title`).

## Pola strony (front matter)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `title` | tekst | tak | Tytuł strony: karta przeglądarki i wyniki wyszukiwania (z nazwą gabinetu), okruszki, karty usług, stopka, „Powiązane strony”; nagłówek `h1`, gdy strona nie zaczyna się banerem. |
| `seo_tytul` | tekst | nie | Pełny tytuł do karty przeglądarki i wyników wyszukiwania (np. „Cennik stomatologiczny Legnica \| Gabinet Rożdżestwieńska”). Brak = `title` z nazwą gabinetu. |
| `description` | tekst | nie | Opis SEO (do 170 znaków). Brak = `ustawienia.seo_opis`. |
| `draft` | tak/nie | nie | `true` = strona ukryta (znika też z menu). |
| `weight` | liczba | — | Kolejność stron; zapisuje panel przy przeciąganiu. |
| `aliases` | lista | — | Stare adresy (przekierowania); zapisuje panel przy zmianie adresu. |
| `usluga` | obiekt | nie | Strona usługi — patrz niżej. |
| `sekcje` | lista | nie | Bloki strony. |

Adres strony to nazwa jej katalogu (`content/strony/higienizacja/` → `/higienizacja/`);
w panelu to „slug”.

**`usluga`** (tylko podstrony) — oznacza stronę jako usługę gabinetu. Taka strona
pojawia się w bloku `lista_uslug`, w kolumnie „Usługi” stopki i w danych dla
wyszukiwarek (`availableService`).

```yaml
usluga:
  wyrozniona: false          # tak/nie - blok lista_uslug może pokazać tylko wyróżnione
  nazwa: "Licówki kompozytowe"   # nazwa na karcie usługi, opcjonalnie (brak = title)
  ikona: "iskry"             # klucz ikony (lista niżej), opcjonalnie
  skrot: "Usunięcie kamienia, piaskowanie, lakierowanie fluorem i lakowanie bruzd."
  cena_od: "lakierowanie"    # id pozycji cennika - karta pokaże "od 150 zł", opcjonalnie
```

## Pola wspólne każdego bloku

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `type` | tekst | tak | Nazwa typu bloku (klucz `typeKey` listy w panelu). |
| `wariant` | wybór | nie | Tło sekcji: `domyslny` (zwykłe) albo `wyrozniony` (kolorowe). Brak = `domyslny`. Szablon może je wyglądać różnie albo ignorować. |
| `waska` | tak/nie | nie | `true` = sekcja do czytania: węższa, wyśrodkowana kolumna. Bloki `faq`, `formularz` i `rezerwacja` szablon może zawsze stawiać wąsko. Szablon może pominąć. |
| `polacz` | tak/nie | nie | `true` = blok dołącza do sekcji powyżej. Tło, szerokość i kotwica sekcji są wtedy brane z bloku, który ją zaczyna. Ignorowane dla `hero` i dla pierwszego bloku strony. |
| `kotwica` | tekst | nie | Krótka nazwa (`a-z`, `0-9`, `-`), np. `ceny` → odnośnik `/cennik/#ceny` przewija do bloku. Ta sama kotwica dwa razy na stronie albo kotwica zarezerwowana (niżej) = błąd budowania. |

**Kotwice zarezerwowane** — `id` używane przez szablony; panel ich nie przyjmie, a szablon
zatrzyma budowanie: `tresc`, `menu-mobilne`, `lightbox`, `cennik-tabela`, `szukaj-ceny`
oraz wszystko, co zaczyna się od `grupa-`, `podmenu-` albo `f<liczba>-`. Grupy pełnego
cennika mają kotwice `grupa-<id kategorii>` (np. `/cennik/#grupa-stawy`) w każdym
szablonie.

## Typy złożone

**Zdjęcie** (`zdjecie` w blokach, element `elementy` w galerii):

```yaml
zdjecie:
  plik: "instruktaz.jpg"           # obok strony albo wspólne "/images/x.webp" (= assets/images/x.webp)
  alt: "Opis tego, co widać"       # wymagany - brak = błąd budowania
  podpis: "Podpis pod zdjęciem"    # opcjonalnie, Markdown w wierszu (np. link); szablon może go pominąć (np. w banerze)
```

**Odnośnik do strony** (`strona`): slug podstrony z `content/strony/` (relacja w panelu;
zmiana nazwy strony poprawia odnośniki automatycznie). Strona ukryta (draft) = brak
odnośnika; strona, której nie ma = błąd budowania.

**Przycisk** (`przycisk` w `hero`, `tekst`, `cta` i w polu `bok`):
`{etykieta, strona, styl, kotwica_celu}` — `etykieta` i `strona` wymagane, gdy przycisk
jest. `styl`: `glowny` (wypełniony) albo `obrysowy`; brak = wygląd zwykły dla tego
miejsca (w `tekst` wypełniony, w `hero`, `cta` i panelu z boku obrysowany).
`kotwica_celu`: kotwica na stronie docelowej (`/cennik/#grupa-stawy`). Przycisk do
strony ukrytej znika.

**Pozycja cennika** (`cena`, `cena_od`, `pozycje`): identyfikator pozycji z
`data/cennik.yaml` (`pozycje[].id`). Szablon bierze z cennika nazwę i aktualną cenę.
Identyfikator, którego nie ma w cenniku = błąd budowania.

**Ikona** (`ikona`): klucz znaczeniowy — szablon dobiera do niego własną grafikę (albo
ją pomija). Dozwolone klucze: `zab`, `iskra`, `iskry`, `korona`, `warstwy`, `ksiezyc`,
`puls`, `rtg`, `dziecko`, `tarcza`, `serce`, `gwiazdka`, `aparat`, `sms`, `karta`,
`telefon`, `zegar`, `kalendarz`, `pinezka`, `mapa`, `parking`, `poczta`, `dokument`,
`dostepnosc`, `platek`, `ptaszek`, `info`, `uwaga`. Nieznany klucz = błąd budowania
w szablonie, który rysuje ikony.

**Markdown** (`tresc`, `wstep`, `odpowiedz`, `ramka.tresc`, opisy kart i kroków):
renderowany jako blok (`.RenderString (dict "display" "block")` — jak `markdownify`,
ale zawsze z akapitami i z hookami odnośników strony). Surowy HTML jest wyłączony
(`markup.goldmark.renderer.unsafe: false`); pominięty HTML nie przerywa publikacji,
a `<br>` zamienia się na złamanie wiersza (partial `markdown.html` — każdy szablon
renderuje pola Markdown tak samo). Odnośnik do podstrony piszemy jako `/slug/`
(też `/slug/#kotwica`) — hook `render-link.html` sprawdza stronę jak menu (ukryta =
sam tekst, brak = błąd budowania, stary adres = nowy adres) i dokleja ścieżkę bazową
serwisu; ścieżka z już doklejonym prefiksem albo pełny adres witryny są skracane.

**Markdown w wierszu** (`fakty[].tekst`, punkty `lista`, komórki `tabela`): jeden
wiersz tekstu, w którym działa `**pogrubienie**`, `*kursywa*` i `[odnośnik](/slug/)`.
Szablon renderuje go bez akapitu.

**Ramka z boku** (`bok` w blokach `kontakt` i `tresc_z_bokiem`): wąska kolumna obok
treści (na telefonie pod treścią) z danymi z `data/gabinet.yaml` i `data/cennik.yaml`:

```yaml
bok:
  naglowek: "Godziny przyjęć"   # opcjonalnie; brak = "Godziny przyjęć", "Ceny z cennika" albo "Kontakt"
  godziny: true                 # tabela godzin; brak = tak
  pozycje: ["wypelnienie"]      # pozycje cennika z cenami (+ informacja z cennika); opcjonalnie
  notka: "Rejestracja wyłącznie telefoniczna."   # opcjonalnie
  telefony: true                # przyciski z numerami; brak = tak (przy przycisku - tylko pierwszy)
  przycisk: { etykieta: "Pełny cennik", strona: "cennik" }   # opcjonalnie
  adres: false                  # adres gabinetu; brak = nie
  notka_dol: "Płatność gotówką, kartą i BLIKIEM."   # opcjonalnie, na dole ramki
```

Brak pola `bok` w `tresc_z_bokiem` = godziny i telefony; w `kontakt` = bez kolumny z boku.

**Zwykły tekst wielowierszowy** (`cytat.tekst`, `adres.dojazd`, `stopka_tekst`,
`rezerwacja.nota`, `cennik.informacja`, notki w `bok`, teksty `strona_404`): bez
Markdown, ale złamania wiersza wpisane w panelu zostają.

**Wyróżnienie w treści**: `==DO UZUPEŁNIENIA==` w polu Markdown to napis wyróżniony
(`<mark>`; szablon może narysować go jako plakietkę).

## Bloki

### `hero` — baner (początek strony)

Duży nagłówek na górze strony. Jako pierwsza sekcja zastępuje tytuł strony (`h1`):
na stronie głównej to baner ze zdjęciem, na podstronie nagłówek z okruszkami i wstępem.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | tak | Nagłówek (`h1`, gdy blok jest pierwszy; inaczej `h2`). Pusty = tytuł strony. |
| `nadtytul` | tekst | nie | Krótki napis nad nagłówkiem. |
| `ikona` | ikona | nie | Ikona przy nadtytule. Szablon może pominąć. |
| `tresc` | Markdown | nie | Krótki wstęp. |
| `zdjecie` | zdjęcie | nie | Zdjęcie banera (ładowane od razu, nie leniwie). |
| `przycisk` | przycisk | nie | Przycisk do strony. |
| `pokaz_telefon` | tak/nie | nie | `true` = przycisk „Zadzwoń” z pierwszym numerem z `data/gabinet.yaml`. Brak = nie. |
| `fakty` | lista | nie | Krótkie fakty pod tekstem: `{ikona, tekst}` (tekst = Markdown w wierszu). |
| `plakietka` | obiekt | nie | Napis na zdjęciu: `{wyroznienie, tekst}`, np. „od 1995” + „ten sam lekarz…”. |

```yaml
- type: hero
  naglowek: "Dentysta w Legnicy, u którego nie czuć pośpiechu"
  nadtytul: "30 lat praktyki w centrum Legnicy"
  tresc: "Prywatny gabinet…"
  pokaz_telefon: true
  przycisk: { etykieta: "Jak wygląda pierwsza wizyta", strona: "pierwsza-wizyta" }
  fakty:
    - { ikona: "pinezka", tekst: "**ul. Złotoryjska 16/18 m. 10**, 59-220 Legnica" }
  plakietka: { wyroznienie: "od 1995", tekst: "ten sam lekarz, ten sam gabinet" }
  zdjecie: { plik: "/images/hero-gabinet.jpg", alt: "Gabinet zabiegowy…" }
```

### `tekst` — tekst (ze zdjęciem lub bez)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `nadtytul` | tekst | nie | Krótki napis nad nagłówkiem. |
| `ikona` | ikona | nie | Ikona przy nadtytule. Szablon może pominąć. |
| `wstep` | Markdown | nie | Wyróżniony akapit pod nagłówkiem (większą czcionką). |
| `tresc` | Markdown | nie | Treść. Blok bez treści (sam nagłówek i wstęp) zaczyna sekcję, do której dołączają kolejne bloki. |
| `wypunktowanie` | wybór | nie | Wygląd list w treści i w ramce: `zwykle` (kropki, domyślnie) albo `ptaszki` (lista zalet). |
| `ramka` | obiekt | nie | Ramka pod treścią: `{rodzaj, tresc}` — jak blok `ramka`. |
| `zdjecie` | zdjęcie | nie | Zdjęcie obok tekstu (na telefonie nad/pod tekstem). Bloki dołączone stają w kolumnie tekstu. |
| `strona_zdjecia` | wybór | nie | `prawa` (domyślnie) albo `lewa`. Szablon może pominąć. |
| `przycisk` | przycisk | nie | Przycisk pod treścią. |
| `pokaz_telefony` | tak/nie | nie | `true` = pod treścią przyciski ze wszystkimi numerami z `data/gabinet.yaml`. |

### `karty` — karty (zalety, usługi, ceny)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed kartami. |
| `kolumny` | wybór | nie | Kart w rzędzie na dużym ekranie: `2`, `3` (domyślnie), `4`. Szablon może pominąć. |
| `wypunktowanie` | wybór | nie | Wygląd list w kartach: `zwykle` (domyślnie) albo `ptaszki`. |
| `elementy` | lista | tak | Karty: `tytul` (wymagany), `tresc` (Markdown), `ikona`, `cena` (pozycja cennika), `strona` (cała karta odnośnikiem). |

Karta z samym tytułem i ceną to „karta ceny” (np. „Badanie i konsultacja — 100 zł”).

### `faq` — pytania i odpowiedzi

Pytania trafiają też do danych strukturalnych `FAQPage`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Najczęstsze pytania”; w bloku dołączonym — brak). |
| `elementy` | lista | tak | `pytanie` (tekst) + `odpowiedz` (Markdown), oba wymagane. |

### `cennik` — cennik

Ceny zawsze z `data/cennik.yaml` — blok tylko wskazuje kategorie albo pozycje.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Cennik”; w bloku dołączonym — brak). |
| `wstep` | Markdown | nie | Krótki opis tabeli (szablon może użyć go jako podpisu tabeli). |
| `kategorie` | lista | nie | Identyfikatory kategorii (`kategorie[].id`). Nieznany identyfikator = błąd budowania. |
| `pozycje` | lista | nie | Identyfikatory pozycji (`pozycje[].id`) — zamiast kategorii, w podanej kolejności. |
| `wyszukiwarka` | tak/nie | nie | Pole „Szukaj zabiegu” i spis kategorii (krótkie nazwy `kategorie[].skrot`) nad tabelą — na stronie z pełnym cennikiem; ta strona dostaje też dane `OfferCatalog` dla wyszukiwarek. Szablon może pominąć pole i spis. |
| `kolumna` | tekst | nie | Nagłówek kolumny z nazwami, np. „Zabieg”. Brak = „Usługa”. |

Puste `kategorie` i `pozycje` = cały cennik. Format ceny: `cena_od` = „650 zł”;
`cena_od` + `cena_do` = „250–400 zł” (półpauza, twarda spacja przed „zł”). Przy
tabeli `informacja` z `data/cennik.yaml`.

### `galeria` — galeria zdjęć

Elementy listy to obiekty (a nie zagnieżdżone listy) — ograniczenie list ze zmiennym
typem w Sveltia/Decap: lista nie może być bezpośrednio typem, musi być polem obiektu.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed zdjęciami. |
| `elementy` | lista | tak | Zdjęcia: `plik`, `alt` (wymagane), `podpis`. |

### `godziny` — godziny przyjęć

Godziny z `data/gabinet.yaml` (`godziny[]`: `dzien`, `od`, `do`; puste = nieczynne).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Godziny przyjęć”; w bloku dołączonym — brak). |
| `tresc` | Markdown | nie | Tekst pod tabelą godzin. |

### `mapa` — mapa i dojazd

Adres i opis dojazdu z `data/gabinet.yaml` (szablon może je pominąć, gdy strona ma
blok `kontakt`). Osadzoną mapę (ramkę Google Maps) wolno wczytać **dopiero po
kliknięciu** odwiedzającego (bramka zgody, jak w makiecie v1; tekst zgody —
`ustawienia.napisy.mapa_zgoda`); zawsze jest też zwykły odnośnik do mapy albo
nawigacji w nowej karcie.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Jak do nas trafić”; w bloku dołączonym — brak). |
| `tresc` | Markdown | nie | Dodatkowe wskazówki. |

### `cta` — zaproszenie do kontaktu

Przycisk „Zadzwoń” (pierwszy numer z `data/gabinet.yaml`), opcjonalnie przyciski
z pozostałymi numerami i przycisk do strony.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Umów wizytę”). |
| `tresc` | Markdown | nie | Tekst zachęty. |
| `wszystkie_telefony` | tak/nie | nie | `true` = także przyciski z pozostałymi numerami telefonów. |
| `przycisk` | przycisk | nie | Drugi przycisk, np. „Dojazd i mapa” → strona kontaktu. |

### `kontakt` — dane kontaktowe

Telefony, e-mail, adres i parking (albo opis dojazdu) z `data/gabinet.yaml`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Kontakt”; w bloku dołączonym — brak). |
| `tresc` | Markdown | nie | Tekst przed danymi. |
| `bok` | ramka z boku | nie | Kolumna z godzinami i telefonami obok danych; bloki dołączone stają w kolumnie z danymi. |

### `lista` — lista (zalety, zakres)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed listą. |
| `styl` | wybór | tak | `ptaszki` (zalety, korzyści), `minusy` (czego nie robimy, przeciwwskazania), `zwykla`. |
| `elementy` | lista | tak | Punkty — lista napisów (Markdown w wierszu). |

```yaml
- type: lista
  naglowek: "Czego w tym gabinecie nie robimy"
  styl: minusy
  elementy: ["wszczepiania implantów zębowych", "ortodoncji z aparatami stałymi"]
```

### `ramka` — ramka (informacja, ostrzeżenie)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `rodzaj` | wybór | tak | `info` (informacja), `uwaga` (ostrzeżenie), `ok` (potwierdzenie). |
| `tresc` | Markdown | tak | Treść ramki. |
| `ikona` | ikona | nie | Ikona zamiast domyślnej dla rodzaju (np. `karta` przy formach płatności). |
| `wypunktowanie` | wybór | nie | Wygląd list w ramce: `zwykle` (domyślnie) albo `ptaszki`. |

### `kroki` — kroki (przebieg wizyty, zabiegu)

Numery kroków dodaje szablon.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed krokami. |
| `elementy` | lista | tak | Kroki: `tytul` (wymagany) + `tresc` (Markdown). |

### `tabela` — tabela porównawcza

Ogólna tabela (np. porównanie rodzajów protez). Ceny nie wpisuje się w komórki —
wiersz wskazuje pozycję cennika, a szablon dokłada ostatnią kolumnę „Cena”.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed tabelą. |
| `podpis` | tekst | nie | Podpis tabeli (`caption`). |
| `kolumny` | lista | tak | Nagłówki kolumn — lista napisów. |
| `wiersze` | lista | tak | Wiersze: `komorki` (lista napisów w kolejności kolumn; Markdown w wierszu) + `cena` (pozycja cennika, opcjonalnie). |

```yaml
- type: tabela
  naglowek: "Rodzaje protez"
  podpis: "Cztery rodzaje protez. Kwoty z cennika."
  kolumny: ["Rodzaj protezy", "Dla kogo", "Materiał"]
  wiersze:
    - { komorki: ["Elastyczna", "Braki częściowe", "Tworzywo elastyczne"], cena: "proteza-elastyczna" }
```

### `lista_uslug` — lista usług (automatyczna)

Karty powstają same ze stron z polem `usluga` (w kolejności stron): tytuł strony,
`usluga.skrot`, „od” + cena pozycji `usluga.cena_od`, odnośnik do strony.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed kartami. |
| `tylko_wyroznione` | tak/nie | nie | `true` = tylko strony z `usluga.wyrozniona: true`. |
| `kolumny` | wybór | nie | `2`, `3` (domyślnie), `4`. Szablon może pominąć. |

### `pasek_zaufania` — pasek atutów

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek (szablon może pokazać go tylko czytnikom ekranu). |
| `elementy` | lista | tak | Atuty: `ikona`, `tytul` (wymagany), `tekst` (krótki opis). |

### `cytat` — cytat

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `tekst` | tekst | tak | Cytat (zwykły tekst). |
| `autor` | tekst | nie | Autor cytatu. |

### `powiazane` — powiązane strony

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`, np. „Zobacz też”. Brak = same odnośniki, bez nagłówka. |
| `elementy` | lista | tak | `strona` (wymagana) + `etykieta` (napis odnośnika; pusty = tytuł strony) + `opis` (krótki; pusty = `usluga.skrot` tej strony). Strona ukryta jest pomijana. |

### `rezerwacja` — rezerwacja online

Karta rezerwacji z `data/gabinet.yaml` (`rezerwacja`: adres, serwis, nota; telefony jako
druga droga). Wyłączona rezerwacja (albo brak adresu) = blok nic nie pokazuje.
Odnośnik do serwisu otwiera się w nowej karcie z `rel="noopener noreferrer"`;
`rezerwacja.potwierdzona: false` = przy przycisku uwaga, że rezerwacja online jest
w przygotowaniu.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Rezerwacja online”; w bloku dołączonym — brak). |
| `tresc` | Markdown | nie | Tekst przed kartą rezerwacji. |

### `formularz` — formularz kontaktowy (pokazowy)

Formularz z polami imię, telefon, e-mail, temat, wiadomość i zgodą RODO (administrator
z `data/gabinet.yaml`). **Nic nie jest wysyłane** — strona na GitHub Pages nie ma
serwera pocztowego; szablon mówi o tym wprost pod formularzem i po jego wypełnieniu.
Tekst zgody, ostrzeżenie o danych o zdrowiu i notka pod formularzem — z
`ustawienia.napisy` (puste = teksty domyślne szablonu).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Napisz do nas”; w bloku dołączonym — brak). |
| `wstep` | Markdown | nie | Tekst przed formularzem. |
| `tematy` | lista | nie | Tematy do wyboru (napisy). Puste = „Umówienie wizyty”, „Pytanie o cenę”, „Pytanie o leczenie”, „Inne”. |

### `tresc_z_bokiem` — tekst z ramką z boku

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Wstęp (wyróżniony akapit). |
| `tresc` | Markdown | nie | Treść. Bloki dołączone (kroki, rezerwacja, przycisk…) stają pod nią, w tej samej kolumnie. |
| `bok` | ramka z boku | nie | Kolumna z godzinami, cenami, telefonami, przyciskiem, adresem, notkami. Brak = godziny i telefony. |

### `przycisk` — przycisk z odnośnikiem

Pojedynczy przycisk, zwykle dołączony do sekcji powyżej (`polacz: true`), np.
„Zobacz pełny cennik” pod kartami cen.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `etykieta` | tekst | tak | Napis na przycisku. |
| `strona` | odnośnik | tak | Strona docelowa. Strona ukryta = przycisk znika. |
| `kotwica_celu` | tekst | nie | Kotwica na stronie docelowej, np. `grupa-stawy` → `/cennik/#grupa-stawy`. |
| `styl` | wybór | nie | `glowny` (wypełniony, domyślnie) albo `obrysowy` (drugorzędny). |

### `spis` — spis treści (skróty do sekcji strony)

Odnośniki do bloków tej samej strony (np. pigułki nad długą stroną). Kotwica, której
nie ma żaden blok tej strony, przerywa budowanie.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nazwa spisu (np. „Spis treści”); szablon może pokazać ją tylko czytnikom ekranu. |
| `elementy` | lista | tak | `etykieta` (krótki napis) + `kotwica` (kotwica bloku na tej stronie), oba wymagane. |

## Dane wspólne (`data/`)

| Plik | Zawartość |
|---|---|
| `menu.yaml` | `pozycje[]`: `etykieta`, `strona` (slug), `link_zewnetrzny`, `podmenu[]` (te same pola, bez dalszego zagnieżdżania). Pozycja bez strony, linku i podmenu = błąd budowania. Hierarchia stron (okruszki) jest tylko tutaj: strona pozycji z podmenu jest „rodzicem” stron z podmenu. Listy płaskie (`etykieta`, `strona`, `link_zewnetrzny`, bez podmenu): `dodatkowe` (mniej ważne strony dopisywane za menu głównym tam, gdzie motyw ma miejsce), `stopka` (strony w stopce; pusta = pozycje menu bez podmenu), `stopka_dolna` (odnośniki w ostatniej linii stopki; pusta = polityka prywatności). Odnośnik „Start” do strony głównej dodaje szablon. |
| `cennik.yaml` | `informacja`, `kategorie[]`: `id`, `nazwa`, `skrot` (krótka nazwa do spisu kategorii, opcjonalnie); `pozycje[]`: `id` (wymagany, niepowtarzalny), `kategoria` (id kategorii), `nazwa`, `cena_od`, `cena_do` (opcjonalnie), `uwagi` (opcjonalnie). Kolejność pozycji = kolejność w tabeli w obrębie kategorii. |
| `gabinet.yaml` | `nazwa`, `nazwa_krotka`, `lekarz` (np. „lek. stom. Imię Nazwisko” — tytuł szablon oddziela w danych dla wyszukiwarek), `rok_zalozenia`, `adres` {`ulica`, `kod`, `miasto`, `region`, `dojazd`, `parking`, `wspolrzedne` („51.207798, 16.158593”)}, `telefony[]` {`etykieta`, `numer`}, `email`, `obszar[]` (obszar przyjmowania pacjentów dla wyszukiwarek, np. „powiat legnicki”; miasto z adresu dochodzi samo), `godziny[]` {`dzien`, `od`, `do`}, `rezerwacja` {`wlaczona`, `url`, `etykieta`, `dostawca`, `potwierdzona`, `nota`}, `rejestrowe` {`nip`, `regon`, `pwz`, `rpwdl`} (puste = wiersz w stopce znika), `platnosci[]`. |
| `ustawienia.yaml` | `seo_opis` (domyślny opis SEO), `stopka_tekst`, `ukryj_przed_wyszukiwarkami` (tak/nie: `noindex` na każdej stronie i `Disallow: /` w `robots.txt`), `logo_nazwa` i `logo_podpis` (napisy przy logo; puste = nazwa krótka, lekarz i miasto), `pasek_informacyjny` (krótki komunikat nad stroną; pusty = brak paska), `napisy` {`przycisk_naglowka`, `stopka_uslugi`, `stopka_gabinet`, `stopka_godziny`, `cennik_podpowiedz`, `formularz_zgoda` (Markdown w wierszu), `formularz_uwaga` (Markdown), `formularz_notka`, `mapa_zgoda`} (stałe napisy szablonu; puste = napis domyślny szablonu), `strona_404` {`tytul`, `opis`, `nadtytul`, `naglowek`, `tresc`, `przycisk`, `notka`, `linki_naglowek`, `linki_wstep`, `opis_glownej`, `linki[]` {`strona`, `opis`}, `ramka_telefon`, `ramka_adres`} (napisy strony 404; puste pole = napis domyślny szablonu, pusta lista `linki` = pozycje menu, telefony i adres z `gabinet.yaml`). |

Odnośnik `tel:` szablon wylicza z `numer`: same cyfry, `+48` dla numeru 9-cyfrowego.

`cennik.yaml` ma pozycje na **jednej liście** (z polem `kategoria`), a nie w każdej
kategorii osobno: relacja w Sveltia CMS (`value_field: 'pozycje.*.id'`) działa tylko
na jednym poziomie listy (`kategorie.*.pozycje.*.id` nie jest obsługiwane), a bloki
wskazują pojedyncze pozycje (`cena`, `cena_od`, `pozycje`).

## Szablony a pola — co wolno pominąć

| Szablon | Pomija |
|---|---|
| `v0-test` | `polacz` (każdy blok to osobna `<section>`), `waska`, ikony, `kolumny`, `strona_zdjecia`, `wypunktowanie`, `wyszukiwarka`, `kolumna` cennika, `styl` przycisków, `napisy`; formularz bez skryptu. |
| `v1-klasyczna` | podpis zdjęcia w banerze (`hero`), `wariant` banera (baner ma własne tło); formy płatności (`platnosci`) tylko w danych dla wyszukiwarek, bez wiersza w stopce (stopka v1 ich nie ma). |

## Zmiany w wersji 2

Wszystkie typy z wersji 1 działają bez zmian (nowe pola są opcjonalne). Nowe:

- pola wspólne `polacz` i `kotwica`;
- `hero`: `nadtytul`, `pokaz_telefon`, `fakty`, `plakietka`;
- `tekst`: `nadtytul`, `wypunktowanie`, `ramka`, `strona_zdjecia`, `przycisk`;
- `karty`: `kolumny`, w kartach `ikona` i `cena`;
- `cennik`: `pozycje`, `wyszukiwarka`; `galeria`: `wstep`; `cta`: `przycisk`; `kontakt`: `bok`;
- nowe typy: `lista`, `ramka`, `kroki`, `tabela`, `lista_uslug`, `pasek_zaufania`,
  `cytat`, `powiazane`, `rezerwacja`, `formularz`, `tresc_z_bokiem`, `przycisk`;
- pole strony `usluga`;
- `data/cennik.yaml`: pozycje przeniesione z `kategorie[].pozycje[]` do jednej listy
  `pozycje[]` z polem `kategoria` (migracja jednorazowa, ceny i identyfikatory bez zmian);
- `data/gabinet.yaml`: `rok_zalozenia`, `rezerwacja.dostawca`, `rezerwacja.potwierdzona`,
  `rezerwacja.nota`; `data/ustawienia.yaml`: `logo_nazwa`, `logo_podpis`, `pasek_informacyjny`.

## Zmiany w wersji 3

Po porównaniu szablonu `v1-klasyczna` z makietą v1. Wszystkie nowe pola są opcjonalne;
zmienia się zachowanie trzech pól (niżej, „Zmienione”).

- pole wspólne `waska` (wąska kolumna do czytania);
- pola strony `seo_tytul`, `usluga.nazwa`;
- przycisk: `styl`, `kotwica_celu` (także w bloku `przycisk`);
- `hero`: `ikona` (przy nadtytule);
- `tekst`: `ikona`, `wstep`, `pokaz_telefony`; `tresc` nie jest już wymagana;
- `tresc_z_bokiem`: `tresc` nie jest już wymagana;
- `bok`: `pozycje`, `przycisk`, `notka_dol`;
- `karty` i `ramka`: `wypunktowanie`; `cta`: `wszystkie_telefony`; `cennik`: `kolumna`;
- `powiazane`: w elementach `etykieta`;
- nowy typ `spis` (spis treści);
- `data/cennik.yaml`: `kategorie[].skrot`; `data/gabinet.yaml`: `adres.region`,
  `adres.parking`, `adres.wspolrzedne`, `obszar[]`; `data/ustawienia.yaml`:
  `ukryj_przed_wyszukiwarkami`, `napisy`;
- Markdown: `==tekst==` = wyróżnienie; zdjęcie: `podpis` jako Markdown w wierszu;
- kotwice zarezerwowane (lista w „Pola wspólne każdego bloku”).

Zmienione:

- blok dołączony (`polacz`) z pustym nagłówkiem nie dostaje nagłówka domyślnego;
- `powiazane` bez nagłówka nie dostaje „Powiązanych stron” — same odnośniki;
- w sekcji zaczętej blokiem z kolumną obok bloki dołączone stają w kolumnie tekstu.

## Nowy typ bloku — kolejność pracy

1. Tabela w tym pliku (nowa sekcja `### \`typ\``).
2. Typ w `static/admin/config.yml` (lista `types` pola `sekcje`) z tymi samymi polami
   i polami wspólnymi (`*wariant`, `*waska`, `*polacz`, `*kotwica`).
3. `layouts/partials/blocks/<typ>.html` w **każdym** szablonie w `themes/`.
4. `python tools/sprawdz-kontrakt.py` i `hugo` lokalnie — bez błędów i ostrzeżeń.
