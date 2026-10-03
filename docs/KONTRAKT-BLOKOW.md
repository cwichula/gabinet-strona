# Kontrakt bloków treści

Wspólna umowa między **treścią** (`content/`, `data/`), **panelem** (`static/admin/config.yml`)
i **szablonami** (`themes/*`). Każdy szablon musi umieć wyświetlić każdy blok opisany
poniżej, a panel może zapisywać tylko pola z tej listy. Dzięki temu zmiana szablonu
(`theme:` w `hugo.yaml`) nie wymaga żadnej zmiany w treści.

Wersja kontraktu: **1** (`params.kontraktBlokow` w `hugo.yaml`).

Pilnuje tego `tools/sprawdz-kontrakt.py` (uruchamiany w CI przed budowaniem):

- każdy typ bloku z `config.yml` ma partial `layouts/partials/blocks/<typ>.html`
  w **każdym** szablonie w `themes/`,
- pola każdego typu w `config.yml` są dokładnie takie jak w tabelach poniżej,
- partial bloku używa tylko pól ze swojej tabeli (`$b.<pole>`),
- katalog `layouts/` w korzeniu repozytorium jest pusty.

## Gdzie są bloki

Strona główna (`content/_index.md`) i każda podstrona (`content/strony/<slug>/index.md`)
mają w front matter (YAML) listę `sekcje`. Każdy element listy to jeden blok:

```yaml
sekcje:
  - type: tekst          # typ bloku - jedna z nazw poniżej
    wariant: domyslny    # opcjonalnie
    naglowek: "O nas"
    tresc: |-
      Akapit w **Markdown**.
```

Front matter podstrony: `title`, `description` (opis SEO, opcjonalny), `draft`
(`true` = strona ukryta, znika też z menu), `sekcje`. Pola `weight` (kolejność)
i `aliases` (przekierowania ze starych adresów) zapisuje sam panel — przy
przeciąganiu stron i przy zmianie adresu. Adres strony to nazwa jej katalogu
(`content/strony/higienizacja/` → `/higienizacja/`); w panelu to „slug”.

Szablon renderuje bloki po kolei: `range .Params.sekcje` →
`partial "blocks/<type>.html" (dict "blok" . "strona" $strona "nr" $indeks)`.
Nieznany typ = ostrzeżenie `warnf`, a w CI ostrzeżenie przerywa publikację.

## Pola wspólne

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `type` | tekst | tak | Nazwa typu bloku (klucz `typeKey` listy w panelu). |
| `wariant` | wybór | nie | `domyslny` albo `wyrozniony`. Szablon może je wyglądać różnie albo ignorować. Brak = `domyslny`. |

## Typy złożone

**Zdjęcie** (`zdjecie` w blokach, element `elementy` w galerii):

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `plik` | ścieżka | tak | Plik obok strony (`gabinet.webp`) albo wspólny `/images/x.webp` (= `assets/images/x.webp`). |
| `alt` | tekst | tak | Tekst alternatywny. Brak = błąd budowania. |
| `podpis` | tekst | nie | Podpis pod zdjęciem. |

**Odnośnik do strony** (`strona`): slug podstrony z `content/strony/` (relacja w panelu,
zmiana nazwy strony poprawia odnośniki automatycznie). Strona ukryta (draft) = brak
odnośnika; strona, której nie ma = błąd budowania.

**Markdown** (`tresc`, `wstep`, `odpowiedz`): renderowany jako blok
(`.RenderString (dict "display" "block")` — jak `markdownify`, ale zawsze z akapitami
i z hookami odnośników strony). Surowy HTML jest wyłączony
(`markup.goldmark.renderer.unsafe: false`). Odnośnik do podstrony piszemy jako
`/slug/` — szablon dokleja ścieżkę bazową serwisu (hook `render-link.html`).

## Bloki

### `hero` — baner

Duży nagłówek na górze strony. Jako pierwsza sekcja zastępuje tytuł strony (`h1`).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | tak | Nagłówek (`h1`, gdy blok jest pierwszy; inaczej `h2`). |
| `tresc` | Markdown | nie | Krótki wstęp. |
| `zdjecie` | zdjęcie | nie | Zdjęcie banera (ładowane od razu, nie leniwie). |
| `przycisk` | obiekt | nie | `etykieta` (tekst) + `strona` (odnośnik do strony), oba wymagane, gdy jest przycisk. |

### `tekst` — tekst

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `tresc` | Markdown | tak | Treść. |
| `zdjecie` | zdjęcie | nie | Zdjęcie obok/nad tekstem. |

### `karty` — karty (usługi, kroki, zalety)

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `wstep` | Markdown | nie | Tekst przed kartami. |
| `elementy` | lista | tak | Karty: `tytul` (tekst, wymagany), `tresc` (Markdown), `strona` (odnośnik, opcjonalny). |

### `faq` — pytania i odpowiedzi

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Najczęstsze pytania”). |
| `elementy` | lista | tak | `pytanie` (tekst) + `odpowiedz` (Markdown), oba wymagane. |

### `cennik` — cennik

Ceny zawsze z `data/cennik.yaml` — blok tylko wskazuje kategorie.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Cennik”). |
| `wstep` | Markdown | nie | Tekst przed tabelą. |
| `kategorie` | lista | nie | Identyfikatory kategorii (`kategorie[].id` w `data/cennik.yaml`). Pusta = cały cennik. Nieznany identyfikator = błąd budowania. |

Format ceny: `cena_od` = „650 zł”; `cena_od` + `cena_do` = „250–400 zł” (półpauza,
twarda spacja przed „zł”). Pod tabelą `informacja` z `data/cennik.yaml`.

### `galeria` — galeria zdjęć

Elementy listy to obiekty (a nie zagnieżdżone listy) — ograniczenie list ze zmiennym
typem w Sveltia/Decap: lista nie może być bezpośrednio typem, musi być polem obiektu.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2`. |
| `elementy` | lista | tak | Zdjęcia: `plik`, `alt` (wymagane), `podpis`. |

### `godziny` — godziny przyjęć

Godziny z `data/gabinet.yaml` (`godziny[]`: `dzien`, `od`, `do`; puste = nieczynne).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Godziny przyjęć”). |
| `tresc` | Markdown | nie | Tekst pod tabelą godzin. |

### `mapa` — mapa i dojazd

Adres i opis dojazdu z `data/gabinet.yaml`. Bez osadzonej mapy i bez zewnętrznych
skryptów — odnośnik do wyszukiwania adresu w Google Maps.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Jak do nas trafić”). |
| `tresc` | Markdown | nie | Dodatkowe wskazówki. |

### `cta` — zaproszenie do kontaktu

Przycisk „Zadzwoń” (pierwszy numer z `data/gabinet.yaml`) i — gdy
`rezerwacja.wlaczona` — przycisk rezerwacji online (`rezerwacja.url`, `rezerwacja.etykieta`).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Umów wizytę”). |
| `tresc` | Markdown | nie | Tekst zachęty. |

### `kontakt` — dane kontaktowe

Adres, telefony i e-mail z `data/gabinet.yaml`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `naglowek` | tekst | nie | Nagłówek `h2` (domyślnie „Kontakt”). |
| `tresc` | Markdown | nie | Tekst przed danymi. |

## Dane wspólne (`data/`)

| Plik | Zawartość |
|---|---|
| `menu.yaml` | `pozycje[]`: `etykieta`, `strona` (slug), `link_zewnetrzny`, `podmenu[]` (te same pola, bez dalszego zagnieżdżania). Pozycja bez strony, linku i podmenu = błąd budowania. |
| `cennik.yaml` | `informacja`, `kategorie[]`: `id`, `nazwa`, `pozycje[]`: `id`, `nazwa`, `cena_od`, `cena_do` (opcjonalnie), `uwagi` (opcjonalnie). |
| `gabinet.yaml` | `nazwa`, `nazwa_krotka`, `lekarz`, `adres` {`ulica`, `kod`, `miasto`, `dojazd`}, `telefony[]` {`etykieta`, `numer`}, `email`, `godziny[]` {`dzien`, `od`, `do`}, `rezerwacja` {`wlaczona`, `url`, `etykieta`}, `rejestrowe` {`nip`, `regon`, `pwz`, `rpwdl`}, `platnosci[]`. |
| `ustawienia.yaml` | `seo_opis` (domyślny opis SEO), `stopka_tekst`. |

Odnośnik `tel:` szablon wylicza z `numer`: same cyfry, `+48` dla numeru 9-cyfrowego.

## Nowy typ bloku — kolejność pracy

1. Tabela w tym pliku (nowa sekcja `### \`typ\``).
2. Typ w `static/admin/config.yml` (lista `types` pola `sekcje`) z tymi samymi polami.
3. `layouts/partials/blocks/<typ>.html` w **każdym** szablonie w `themes/`.
4. `python tools/sprawdz-kontrakt.py` i `hugo` lokalnie — bez błędów i ostrzeżeń.
