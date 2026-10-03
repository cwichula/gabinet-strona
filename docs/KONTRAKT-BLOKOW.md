# Kontrakt bloków treści

Wspólna umowa między **treścią** (`content/`, `data/`), **panelem** (`static/admin/config.yml`)
i **szablonami** (`themes/*`). Każdy szablon musi umieć wyświetlić każdy blok opisany
poniżej, a panel może zapisywać tylko pola z tej listy. Dzięki temu zmiana szablonu
(`theme:` w `hugo.yaml`) nie wymaga żadnej zmiany w treści.

Wersja kontraktu: **2** (`params.kontraktBlokow` w `hugo.yaml`). Zmiany względem wersji 1
— na końcu pliku („Zmiany w wersji 2”).

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
| `title` | tekst | tak | Tytuł strony (karta przeglądarki, okruszki, karty usług). |
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
  ikona: "iskry"             # klucz ikony (lista niżej), opcjonalnie
  skrot: "Usunięcie kamienia, piaskowanie, lakierowanie fluorem i lakowanie bruzd."
  cena_od: "lakierowanie"    # id pozycji cennika - karta pokaże "od 150 zł", opcjonalnie
```

## Pola wspólne każdego bloku

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `type` | tekst | tak | Nazwa typu bloku (klucz `typeKey` listy w panelu). |
| `wariant` | wybór | nie | Tło sekcji: `domyslny` (zwykłe) albo `wyrozniony` (kolorowe). Brak = `domyslny`. Szablon może je wyglądać różnie albo ignorować. |
| `polacz` | tak/nie | nie | `true` = blok dołącza do sekcji powyżej. Tło i kotwica sekcji są wtedy brane z bloku, który ją zaczyna. Ignorowane dla `hero` i dla pierwszego bloku strony. |
| `kotwica` | tekst | nie | Krótka nazwa (`a-z`, `0-9`, `-`), np. `ceny` → odnośnik `/cennik/#ceny` przewija do bloku. Ta sama kotwica dwa razy na stronie = błąd budowania. |

## Typy złożone

**Zdjęcie** (`zdjecie` w blokach, element `elementy` w galerii):

```yaml
zdjecie:
  plik: "instruktaz.jpg"           # obok strony albo wspólne "/images/x.webp" (= assets/images/x.webp)
  alt: "Opis tego, co widać"       # wymagany - brak = błąd budowania
  podpis: "Podpis pod zdjęciem"    # opcjonalnie; szablon może go pominąć (np. w banerze)
```

**Odnośnik do strony** (`strona`): slug podstrony z `content/strony/` (relacja w panelu;
zmiana nazwy strony poprawia odnośniki automatycznie). Strona ukryta (draft) = brak
odnośnika; strona, której nie ma = błąd budowania.

**Przycisk** (`przycisk` w `hero`, `tekst`, `cta`): `{etykieta, strona}` — oba wymagane,
gdy przycisk jest. Przycisk do strony ukrytej znika.

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
treści (na telefonie pod treścią) z danymi z `data/gabinet.yaml`:

```yaml
bok:
  naglowek: "Godziny przyjęć"   # opcjonalnie; brak = "Godziny przyjęć" albo "Kontakt"
  godziny: true                 # tabela godzin; brak = tak
  telefony: true                # przyciski z numerami; brak = tak
  adres: false                  # adres gabinetu; brak = nie
  notka: "Rejestracja wyłącznie telefoniczna."   # opcjonalnie
```

## Bloki

### `hero` — baner (początek strony)

Duży nagłówek na górze strony. Jako pierwsza sekcja zastępuje tytuł strony (`h1`):
na stronie głównej to baner ze zdjęciem, na podstronie nagłówek z okruszkami i wstępem.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | tak | Nagłówek (`h1`, gdy blok jest pierwszy; inaczej `h2`). Pusty = tytuł strony. |
| `nadtytul` | tekst | nie | Krótki napis nad nagłówkiem. |
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
| `tresc` | Markdown | tak | Treść. |
| `wypunktowanie` | wybór | nie | Wygląd list w treści: `zwykle` (kropki, domyślnie) albo `ptaszki` (lista zalet). |
| `ramka` | obiekt | nie | Ramka pod treścią: `{rodzaj, tresc}` — jak blok `ramka`. |
| `zdjecie` | zdjęcie | nie | Zdjęcie obok tekstu (na telefonie nad/pod tekstem). |
| `strona_zdjecia` | wybór | nie | `prawa` (domyślnie) albo `lewa`. Szablon może pominąć. |
| `przycisk` | przycisk | nie | Przycisk pod treścią. |

### `karty` — karty (zalety, usługi, ceny)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed kartami. |
| `kolumny` | wybór | nie | Kart w rzędzie na dużym ekranie: `2`, `3` (domyślnie), `4`. Szablon może pominąć. |
| `elementy` | lista | tak | Karty: `tytul` (wymagany), `tresc` (Markdown), `ikona`, `cena` (pozycja cennika), `strona` (cała karta odnośnikiem). |

Karta z samym tytułem i ceną to „karta ceny” (np. „Badanie i konsultacja — 100 zł”).

### `faq` — pytania i odpowiedzi

Pytania trafiają też do danych strukturalnych `FAQPage`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Najczęstsze pytania”). |
| `elementy` | lista | tak | `pytanie` (tekst) + `odpowiedz` (Markdown), oba wymagane. |

### `cennik` — cennik

Ceny zawsze z `data/cennik.yaml` — blok tylko wskazuje kategorie albo pozycje.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Cennik”). |
| `wstep` | Markdown | nie | Krótki opis tabeli (szablon może użyć go jako podpisu tabeli). |
| `kategorie` | lista | nie | Identyfikatory kategorii (`kategorie[].id`). Nieznany identyfikator = błąd budowania. |
| `pozycje` | lista | nie | Identyfikatory pozycji (`pozycje[].id`) — zamiast kategorii, w podanej kolejności. |
| `wyszukiwarka` | tak/nie | nie | Pole „Szukaj zabiegu” i spis kategorii nad tabelą (najlepiej na stronie z pełnym cennikiem; szablon może pominąć). |

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
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Godziny przyjęć”). |
| `tresc` | Markdown | nie | Tekst pod tabelą godzin. |

### `mapa` — mapa i dojazd

Adres i opis dojazdu z `data/gabinet.yaml`. Osadzoną mapę (ramkę Google Maps) wolno
wczytać **dopiero po kliknięciu** odwiedzającego (bramka zgody, jak w makiecie v1);
zawsze jest też zwykły odnośnik do mapy albo nawigacji w nowej karcie.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Jak do nas trafić”). |
| `tresc` | Markdown | nie | Dodatkowe wskazówki. |

### `cta` — zaproszenie do kontaktu

Przycisk „Zadzwoń” (pierwszy numer z `data/gabinet.yaml`) i opcjonalny przycisk do strony.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Umów wizytę”). |
| `tresc` | Markdown | nie | Tekst zachęty. |
| `przycisk` | przycisk | nie | Drugi przycisk, np. „Dojazd i mapa” → strona kontaktu. |

### `kontakt` — dane kontaktowe

Telefony, e-mail, adres i dojazd z `data/gabinet.yaml`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Kontakt”). |
| `tresc` | Markdown | nie | Tekst przed danymi. |
| `bok` | ramka z boku | nie | Kolumna z godzinami i telefonami obok danych. |

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
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Powiązane strony”). |
| `elementy` | lista | tak | `strona` (wymagana) + `opis` (krótki; pusty = `usluga.skrot` tej strony). Strona ukryta jest pomijana. |

### `rezerwacja` — rezerwacja online

Karta rezerwacji z `data/gabinet.yaml` (`rezerwacja`: adres, serwis, nota; telefony jako
druga droga). Wyłączona rezerwacja (albo brak adresu) = blok nic nie pokazuje.
Odnośnik do serwisu otwiera się w nowej karcie z `rel="noopener noreferrer"`;
`rezerwacja.potwierdzona: false` = przy przycisku uwaga, że rezerwacja online jest
w przygotowaniu.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Rezerwacja online”). |
| `tresc` | Markdown | nie | Tekst przed kartą rezerwacji. |

### `formularz` — formularz kontaktowy (pokazowy)

Formularz z polami imię, telefon, e-mail, temat, wiadomość i zgodą RODO (administrator
z `data/gabinet.yaml`). **Nic nie jest wysyłane** — strona na GitHub Pages nie ma
serwera pocztowego; szablon mówi o tym wprost pod formularzem i po jego wypełnieniu.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Napisz do nas”). |
| `wstep` | Markdown | nie | Tekst przed formularzem. |
| `tematy` | lista | nie | Tematy do wyboru (napisy). Puste = „Umówienie wizyty”, „Pytanie o cenę”, „Pytanie o leczenie”, „Inne”. |

### `tresc_z_bokiem` — tekst z ramką z boku

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Wstęp (wyróżniony akapit). |
| `tresc` | Markdown | tak | Treść. |
| `bok` | ramka z boku | nie | Kolumna z godzinami, telefonami, adresem, notką. Brak = godziny i telefony. |

### `przycisk` — przycisk z odnośnikiem

Pojedynczy przycisk, zwykle dołączony do sekcji powyżej (`polacz: true`), np.
„Zobacz pełny cennik” pod kartami cen.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `etykieta` | tekst | tak | Napis na przycisku. |
| `strona` | odnośnik | tak | Strona docelowa. Strona ukryta = przycisk znika. |
| `styl` | wybór | nie | `glowny` (wypełniony, domyślnie) albo `obrysowy` (drugorzędny). |

## Dane wspólne (`data/`)

| Plik | Zawartość |
|---|---|
| `menu.yaml` | `pozycje[]`: `etykieta`, `strona` (slug), `link_zewnetrzny`, `podmenu[]` (te same pola, bez dalszego zagnieżdżania). Pozycja bez strony, linku i podmenu = błąd budowania. Hierarchia stron (okruszki) jest tylko tutaj: strona pozycji z podmenu jest „rodzicem” stron z podmenu. |
| `cennik.yaml` | `informacja`, `kategorie[]`: `id`, `nazwa`; `pozycje[]`: `id` (wymagany, niepowtarzalny), `kategoria` (id kategorii), `nazwa`, `cena_od`, `cena_do` (opcjonalnie), `uwagi` (opcjonalnie). Kolejność pozycji = kolejność w tabeli w obrębie kategorii. |
| `gabinet.yaml` | `nazwa`, `nazwa_krotka`, `lekarz`, `rok_zalozenia`, `adres` {`ulica`, `kod`, `miasto`, `dojazd`}, `telefony[]` {`etykieta`, `numer`}, `email`, `godziny[]` {`dzien`, `od`, `do`}, `rezerwacja` {`wlaczona`, `url`, `etykieta`, `dostawca`, `potwierdzona`, `nota`}, `rejestrowe` {`nip`, `regon`, `pwz`, `rpwdl`}, `platnosci[]`. |
| `ustawienia.yaml` | `seo_opis` (domyślny opis SEO), `stopka_tekst`, `logo_nazwa` i `logo_podpis` (napisy przy logo; puste = nazwa krótka, lekarz i miasto), `pasek_informacyjny` (krótki komunikat nad stroną; pusty = brak paska). |

Odnośnik `tel:` szablon wylicza z `numer`: same cyfry, `+48` dla numeru 9-cyfrowego.

`cennik.yaml` ma pozycje na **jednej liście** (z polem `kategoria`), a nie w każdej
kategorii osobno: relacja w Sveltia CMS (`value_field: 'pozycje.*.id'`) działa tylko
na jednym poziomie listy (`kategorie.*.pozycje.*.id` nie jest obsługiwane), a bloki
wskazują pojedyncze pozycje (`cena`, `cena_od`, `pozycje`).

## Szablony a pola — co wolno pominąć

| Szablon | Pomija |
|---|---|
| `v0-test` | `polacz` (każdy blok to osobna `<section>`), ikony, `kolumny`, `strona_zdjecia`, `wypunktowanie`, `wyszukiwarka`; formularz bez skryptu. |
| `v1-klasyczna` | podpis zdjęcia w banerze (`hero`), `wariant` banera (baner ma własne tło). |

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

## Nowy typ bloku — kolejność pracy

1. Tabela w tym pliku (nowa sekcja `### \`typ\``).
2. Typ w `static/admin/config.yml` (lista `types` pola `sekcje`) z tymi samymi polami
   i polami wspólnymi (`*wariant`, `*polacz`, `*kotwica`).
3. `layouts/partials/blocks/<typ>.html` w **każdym** szablonie w `themes/`.
4. `python tools/sprawdz-kontrakt.py` i `hugo` lokalnie — bez błędów i ostrzeżeń.
