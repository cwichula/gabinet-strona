# Strona gabinetu stomatologicznego (Hugo + Sveltia CMS)

Strona gabinetu lek. stom. Doroty Rożdżestwieńskiej w Legnicy. Treść (strony, menu,
cennik, dane gabinetu) jest edytowana w panelu pod **`/admin/`** — właścicielka loguje
się swoim kontem GitHub, a każdy zapis w panelu to commit w tym repozytorium, po którym
strona sama się przebudowuje i publikuje.

- Strona: <https://cwichula.github.io/gabinet-strona/>
- Panel: <https://cwichula.github.io/gabinet-strona/admin/>

Etap 2 (ten stan repozytorium, zakończony): strona ma wygląd makiety v1 — szablon
`themes/v1-klasyczna` — a cała treść (strony, bloki, menu, cennik, dane gabinetu) nadal
pochodzi z panelu. Szablon wybiera jedna linia w `hugo.yaml`; nowy szablon buduje się
z tej samej treści, o ile spełnia kontrakt bloków.

**Przed uruchomieniem strony dla pacjentów:** w panelu „Ustawienia” wyłącz „Ukryj
stronę przed wyszukiwarkami” (teraz włączone, jak w makiecie v1 — w danych są jeszcze
pola do uzupełnienia: dane rejestrowe, godziny, fragmenty
polityki prywatności oznaczone „DO UZUPEŁNIENIA”).

## Z czego to jest zbudowane

| Element | Co | Gdzie |
|---|---|---|
| Generator | [Hugo Extended](https://gohugo.io/) **0.167.0** (jeden plik, bez npm) | `hugo.yaml`, wersja przypięta w `.github/workflows/pages.yml` |
| Panel | [Sveltia CMS](https://sveltiacms.app/en/docs) **0.227.3**, przypięta kopia | `static/admin/` (`sveltia-cms.js`, `config.yml`) |
| Hosting | GitHub Pages przez GitHub Actions | `.github/workflows/pages.yml` |
| Szablony | wymienne, wspólny kontrakt bloków | `themes/`, `docs/KONTRAKT-BLOKOW.md` |

```
hugo.yaml                        konfiguracja (baseURL, theme, adresy /<slug>/)
content/_index.md                strona główna (bloki w front matter: sekcje)
content/strony/_index.md         kontener podstron (sam nie ma strony w sieci)
content/strony/<slug>/index.md   podstrona (zdjęcia ze wspólnej biblioteki assets/images/)
data/menu.yaml                   menu (dwa poziomy) i listy odnośników stopki
data/cennik.yaml                 cennik: kategorie + pozycje (pozycja wskazuje kategorię)
data/gabinet.yaml                dane gabinetu, godziny, rezerwacja, dane rejestrowe
data/uslugi.yaml                 kolejność kart usług (strona główna, „Usługi”, stopka)
data/ustawienia.yaml             domyślny opis SEO, tekst stopki, napisy szablonu, ukrycie przed wyszukiwarkami
assets/images/                   biblioteka zdjęć (wszystkie strony; pole „plik”: /images/x.jpg)
themes/v1-klasyczna/             szablon v1 „Klasyczna” (używany, theme w hugo.yaml)
themes/v1-klasyczna/i18n/pl.yaml stałe napisy szablonu (klucze po angielsku, tekst po polsku)
layouts/                         PUSTY (nadpisałby każdy szablon) - pilnuje CI
static/admin/                    panel: index.html, config.yml, sveltia-cms.js
docs/KONTRAKT-BLOKOW.md          typy bloków i ich pola
docs/LOGOWANIE.md                logowanie do panelu (OAuth, token)
docs/HOSTING.md                  wysyłka na własną domenę (SFTP/FTPS, .htaccess)
tools/sprawdz-kontrakt.py        kontrola kontraktu (CI)
tools/kontrola-strony.py         kontrola zbudowanej strony: struktura, linki, zasoby, art. 14 (CI)
tools/requirements.txt           zależności narzędzi (PyYAML; wersję podbija Dependabot)
archiwum/stara-strona/          kopia starej strony (stan „przed”, źródło przekierowań 301) - build jej nie widzi
```

## Praca lokalna

Instalacja Hugo (Windows):

```
winget install Hugo.Hugo.Extended --version 0.167.0
```

Podgląd na żywo (z widocznymi szkicami: dodaj `-D`):

```
hugo server
```

Strona: <http://localhost:1313/gabinet-strona/>, panel: <http://localhost:1313/gabinet-strona/admin/>.

Panel lokalnie bez logowania: w Chrome lub Edge kliknij **„Pracuj z lokalnym
repozytorium”** i wskaż katalog repozytorium. Zmiany trafiają wtedy do plików na dysku
(commit robisz sam), a `hugo server` od razu je pokazuje.

Przed commitem w kodzie (szablony, konfiguracja):

```
pip install -r tools/requirements.txt # raz: PyYAML dla obu skryptów
python tools/sprawdz-kontrakt.py      # OK
hugo --gc --minify                    # bez ERROR i bez WARN
python tools/kontrola-strony.py       # na public/, 0 błędów (uwagi do przeczytania)
```

## Logowanie do panelu

Każda osoba edytująca potrzebuje konta GitHub z prawem zapisu (**Write**) do tego
repozytorium. Konto właścicielki, logowanie „Zaloguj się przez GitHub” (OAuth App +
Cloudflare Worker) i zapasowe logowanie tokenem: [`docs/LOGOWANIE.md`](docs/LOGOWANIE.md).

## Co można robić w panelu

| Kolekcja | Plik | Co |
|---|---|---|
| Strony | `content/strony/<slug>/index.md` | dodawanie, usuwanie, ukrywanie (szkic), kolejność (przeciąganie), bloki treści, zdjęcia |
| Strona główna | `content/_index.md` | bloki treści strony głównej |
| Kolejność usług | `data/uslugi.yaml` | kolejność kart usług (przeciąganie), też w stopce; usługa spoza listy na końcu |
| Menu | `data/menu.yaml` | pozycje, podmenu, kolejność; pozycje dodatkowe (menu na telefonie), strony w stopce, odnośniki na dole stopki; strona wybierana z listy |
| Cennik | `data/cennik.yaml` | kategorie (z krótką nazwą do spisu nad cennikiem) i pozycje (każda z identyfikatorem i kategorią); zmiana ceny widoczna wszędzie, gdzie strona wskazuje tę pozycję (cennik, karty, tabela, karta usługi, ramka z cenami z boku) |
| Dane gabinetu | `data/gabinet.yaml` | adres (z parkingiem i współrzędnymi dla wyszukiwarek), telefony, e-mail, obszar przyjmowania pacjentów, godziny, rezerwacja online, dane rejestrowe |
| Ustawienia | `data/ustawienia.yaml` | domyślny opis SEO, ukrycie strony przed wyszukiwarkami, tekst stopki, napisy przy logo, pasek informacyjny nad stroną, elementy nagłówka (Start, przycisk motywu, godziny, telefon, adres), napisy szablonu (przycisk w nagłówku, „Start”, nagłówki stopki, „Zobacz szczegóły” i „od” na kartach, podpowiedź w cenniku, teksty formularza i mapy), napisy strony 404 |

Zasady, które chronią stronę:

- **Adres nowej strony** powstaje z tytułu, bez polskich znaków („Leczenie kanałowe” →
  `/leczenie-kanalowe/`). Zmiana adresu zapisanej strony (panel „Slug”) przenosi katalog,
  poprawia menu, przyciski i karty oraz dopisuje przekierowanie ze starego adresu
  (`aliases`). Odnośniki wpisane w treści (`/stary-adres/`) panel zostawia bez zmian,
  ale szablon prowadzi je od razu pod nowy adres.
- **Odnośniki w treści** do własnych stron pisz jako `/slug/` (np. `/cennik/`, także
  `/cennik/#ceny`); wklejony adres z paska przeglądarki też zadziała. Odnośnik do strony
  ukrytej zostaje zwykłym tekstem, a do strony, której nie ma, zatrzymuje budowanie
  z komunikatem, gdzie jest błąd.
- **Linki „zobacz na stronie”** przy wpisach w panelu są wyłączone (`show_preview_links`
  w `config.yml`): Sveltia gubi w nich część adresu `/gabinet-strona/`. Stronę otwiera
  link w menu konta w panelu (`display_url`).
- **Usunięcie strony** wskazywanej w menu: panel czyści odnośnik w menu, a budowanie
  zatrzymuje się z komunikatem, że pozycja menu nie ma celu — w sieci zostaje poprzednia
  wersja, a w repozytorium powstaje zgłoszenie. Popraw menu i zapisz.
- **Zdjęcia** są zmniejszane i zamieniane na WebP w przeglądarce przed zapisem
  (maks. 2048 px, limit 1 MB po konwersji), a Hugo robi z nich wersje 480, 800 i 1200 px.
  Opis zdjęcia (alt) jest wymagany.
- **Ceny** są tylko w cenniku; bloki na stronach wskazują kategorie albo pozycje
  cennika (po identyfikatorze). Identyfikatora istniejącej pozycji nie zmieniaj.
- **Strona usługi**: podstrona z wypełnionym polem „Opis usługi” (nazwa na karcie, ikona,
  krótki opis, cena „od”) pojawia się sama w bloku „Lista usług”, w stopce i w danych
  dla Google.
- **Tytuł w Google**: pole „Tytuł w wyszukiwarce” (np. „Cennik stomatologiczny Legnica |
  Gabinet Rożdżestwieńska”, do ~60 znaków); puste = tytuł strony z nazwą gabinetu.
- **Bloki połączone** („Połącz z blokiem powyżej”) tworzą jedną sekcję. Gdy sekcja
  zaczyna się tekstem ze zdjęciem albo tekstem z ramką z boku, połączone kroki, teksty,
  ramki, cytaty, przyciski i karta rezerwacji stają w kolumnie tekstu (obok zdjęcia
  albo ramki); karty, tabele, powiązane strony i inne szerokie bloki — pod spodem.
  Połączony blok z pustym nagłówkiem nie ma nagłówka.
- **Spis treści** (blok „Spis treści”) prowadzi do bloków tej strony po ich kotwicy;
  kotwica, której nie ma, zatrzymuje publikację. Kilka kotwic zajmuje szablon
  (`tresc`, `menu-mobilne`, `grupa-…` itd.) — panel ich nie przyjmie.
- **Wyróżniony napis** w treści: `==DO UZUPEŁNIENIA==` (plakietka).

## Publikacja

Każdy commit na `main` uruchamia `.github/workflows/pages.yml`:

1. `tools/sprawdz-kontrakt.py` — kontrakt bloków, pusty `layouts/`, klucze treści
   i danych zgodne z panelem, cennik, telefony i ceny w treści (pełna lista
   w [`docs/KONTRAKT-BLOKOW.md`](docs/KONTRAKT-BLOKOW.md)),
2. sumy kontrolne przypiętego panelu Sveltia i archiwum starej strony,
3. Hugo 0.167.0 Extended (pobrany z wydania na GitHubie, suma SHA-256 sprawdzana) —
   każdy **ERROR** i każde **WARN** przerywa przebieg,
4. kontrola wyniku (strona główna, panel, `noindex` kopii na github.io),
5. `tools/kontrola-strony.py` na zbudowanym HTML — dokładnie jeden `h1`, kolejność
   nagłówków, `alt`/`width`/`height` zdjęć, działające linki wewnętrzne (z prefiksem
   `/gabinet-strona/`), żadnych zasobów z obcych serwerów i żadnej ramki bez zgody,
   poprawny JSON-LD i FAQ zgodne z widocznymi pytaniami, zwroty niedozwolone
   w materiałach gabinetu (art. 14 ustawy o działalności leczniczej), odnośniki
   rezerwacji online; na końcu waga każdej strony. Błąd przerywa przebieg, uwagi
   zostają w logu,
6. publikacja na GitHub Pages.

Błąd na dowolnym kroku = w sieci zostaje poprzednia wersja, a w repozytorium powstaje
zgłoszenie (issue) „Strona nie została opublikowana…” z linkiem do logu. Zmiana jest
w sieci zwykle 1–2 minuty po zapisie (plus do 10 minut pamięci podręcznej Pages).

Jednorazowo w ustawieniach repozytorium: Settings → Pages → Source: **GitHub Actions**.

Kopia na GitHub Pages jest **zawsze ukryta przed wyszukiwarkami** (`noindex`,
`Disallow: /`) — niezależnie od ustawienia w panelu (`params.robocza` w `hugo.yaml`,
włączane w workflow zmienną `HUGO_PARAMS_ROBOCZA=true`; CI sprawdza to w wyniku).
Inaczej po uruchomieniu domeny Google widziałby dwie kopie tej samej strony. Wersja
na domenę jest budowana bez tej zmiennej — tam decyduje ustawienie w panelu.

## Hosting na własnej domenie (dobrydentysta.legnica.pl)

Ten sam workflow buduje drugą wersję strony — z adresem domeny, bez panelu `/admin/`
i z plikiem `hosting/.htaccess` — i wysyła ją przez SFTP albo FTPS. Job `hosting`
uruchamia się dopiero, gdy ustawiona jest zmienna `HOSTING_SERWER`. Konfiguracja,
zmienne i kolejność przeniesienia domeny: [`docs/HOSTING.md`](docs/HOSTING.md).

## Szablony

Szablon to katalog w `themes/` wybierany jedną linią `theme:` w `hugo.yaml`
(teraz `v1-klasyczna`). Zmiana szablonu na stronie = zmiana tej linii i commit — treść
(`content/`, `data/`) zostaje bez zmian. Podgląd innego szablonu bez zmiany pliku:
`hugo server --theme <nazwa>` (albo `hugo --theme <nazwa> -d <katalog>` i
`python tools/kontrola-strony.py <katalog>`). Szablon musi przechodzić `hugo` bez
ostrzeżeń i `tools/kontrola-strony.py` bez błędów, także po zapisie wszystkich wpisów
z panelu. Każdy szablon ma ten sam zestaw:

```
themes/<nazwa>/layouts/_default/baseof.html, home.html, single.html
themes/<nazwa>/layouts/404.html
themes/<nazwa>/layouts/_default/_markup/render-link.html   (odnośniki /slug/ w treści)
themes/<nazwa>/layouts/partials/naglowek.html, stopka.html, image.html, sekcje.html ...
themes/<nazwa>/layouts/partials/blocks/<typ>.html          (po jednym na typ bloku)
themes/<nazwa>/layouts/robots.txt                          (Sitemap, ukrycie przed wyszukiwarkami)
themes/<nazwa>/i18n/pl.yaml                                (stałe napisy szablonu)
themes/<nazwa>/assets/css/...
```

Katalog `layouts/` w korzeniu musi zostać pusty — inaczej nadpisałby każdy szablon.

### Szablon v1-klasyczna

Makieta v1 z zakończonego prototypu `gamstom` (szablon strony, strony v1 i markup
z jego generatora) pocięta na szablon Hugo:

- `assets/css/style.css` i `assets/js/app.js` — z makiety, uporządkowane (jeden zestaw
  kolorów na motyw, bez nieużywanych reguł, napisy skryptu z szablonu przez atrybuty
  `data-napis-*`); łączone i z odciskiem w nazwie pliku przez Hugo Pipes;
  `assets/css/hugo.css` — kilka reguł dla rzeczy, których makieta nie miała (lista
  z minusami, blok dołączony do sekcji i do kolumny tekstu, pogrubienie w faktach
  banera, plakietka z `==tekst==`);
- `partials/naglowek.html` (pasek z godzinami, telefon, motyw, menu z rozwijanym
  podmenu, szuflada na telefon), `stopka.html` (usługi, strony, godziny, dane
  rejestrowe, pasek „Zadzwoń / Dojazd” na telefonie), `head.html` (meta, Open Graph,
  ikony, manifest), `jsonld.html` (Dentist, WebSite, WebPage, BreadcrumbList, FAQPage);
- `partials/sekcje.html` grupuje bloki w sekcje v1 (`polacz`): tło, wąska kolumna
  (`waska`), ciaśniejsza sekcja ze spisem treści, bloki połączone w kolumnie tekstu obok
  zdjęcia albo ramki z boku (jak w makiecie); `partials/blocks/*` — po jednym na typ
  bloku, z klasami makiety;
- dane strukturalne: gabinet (z adresem, współrzędnymi, obszarem i lekarzem), rodzaj
  strony (MedicalWebPage, ContactPage, CollectionPage), okruszki, FAQ i cennik z cenami
  (OfferCatalog) na stronie pełnego cennika;
- zdjęcia przez Hugo: `<picture>` z WebP w kilku szerokościach i zapasowym JPEG/PNG,
  `width`/`height`, pierwsze zdjęcie strony bez `lazy` i z `fetchpriority="high"`.
  Hugo nie koduje AVIF, więc (inaczej niż makieta) bez wersji AVIF;
- żadnych zasobów z obcych serwerów; mapa Google ładuje się dopiero po kliknięciu.

## Kontrakt bloków

Strona to płaska lista bloków (`sekcje`), wersja kontraktu 3: hero, tekst, karty, faq,
cennik, galeria, godziny, mapa, cta, kontakt, lista, ramka, kroki, tabela, lista_uslug,
pasek_zaufania, cytat, powiazane, rezerwacja, formularz, tresc_z_bokiem, przycisk, spis.
Każdy blok to sekcja strony; przełącznik „Połącz z blokiem powyżej” dokleja blok do
sekcji nad nim. Pola każdego typu opisuje [`docs/KONTRAKT-BLOKOW.md`](docs/KONTRAKT-BLOKOW.md).
Nowy typ bloku = wpis w kontrakcie + typ w `config.yml` + partial we **wszystkich**
szablonach; `tools/sprawdz-kontrakt.py` nie przepuści niekompletnej zmiany.

## Język nazw

- **Zostają po polsku na stałe** — to części publicznych adresów: adresy stron (slugi,
  `aliases`), kotwice (`kotwica`, `grupa-<id>`), identyfikatory kategorii i pozycji
  cennika, nazwy plików zdjęć. Zmiana = nowe adresy i przekierowania.
- **Tekst dla ludzi po polsku**: stałe napisy szablonu w `themes/<nazwa>/i18n/pl.yaml`
  (klucze po angielsku), napisy zmieniane w panelu w `data/ustawienia.yaml`, etykiety
  i podpowiedzi panelu w `config.yml`, komunikaty CI i błędów budowania.
- **Identyfikatory w kodzie** (zmienne i partiale szablonów, klucze pól w treści
  i danych, typy bloków, narzędzia w `tools/`) są dziś po polsku; docelowo przejdą
  na angielski w osobnym etapie — klucze treści i danych tylko razem z migracją
  `content/`, `data/`, `config.yml` i kontraktu w jednym commicie. Do tego czasu nowe
  nazwy w kodzie trzymają się polskiego stylu (poza kluczami w `i18n/`). Klasy CSS
  z makiety (`hero__media`, `btn--primary`) są po angielsku już teraz.

## Etapy

1. **Etap 1 — instalacja i test panelu** (szablon testowy `v0-test`, usunięty po etapie 2): repozytorium, publikacja,
   kontrakt bloków, panel z kolekcjami, treść startowa, cennik i dane z `gamstom`.
   Logowanie przez GitHub (OAuth App + Cloudflare Worker, `base_url`) działa
   ([`docs/LOGOWANIE.md`](docs/LOGOWANIE.md)). Pozostaje: konto właścicielki (Write, 2FA)
   i lista testów z planu — etap zamknięty, gdy przejdzie ją właścicielka na swoim koncie.
2. **Etap 2 — szablon v1 „Klasyczna”** (zrobione): makieta v1 jako szablon
   `themes/v1-klasyczna`, kontrakt bloków rozszerzony do wersji 2 (12 nowych typów,
   pole strony „usluga”, cennik z pozycjami na jednej liście), a po porównaniu z makietą
   (20 stron, 1280 i 390 px, zachowanie skryptów) do wersji 3: wąskie sekcje, bloki
   w kolumnie obok zdjęcia i ramki z boku, spis treści, ramka z boku z cenami
   i przyciskiem, styl i kotwica przycisków, tytuł SEO, napisy szablonu w ustawieniach,
   pełniejsze dane strukturalne. Treść przeniesiona bez zmiany tekstów i cen.
   Kontrola zwrotów zakazanych i struktury (`tools/kontrola-strony.py`, port
   `check-site.py`) działa jako krok CI. Znane drobne różnice względem makiety:
   ceny zawsze z cennika (np. karty cen zamiast kwot w zdaniu na stronie
   higienizacji i pierwszej wizyty, pełne nazwy pozycji w ramce cen), szablon bez
   wersji AVIF zdjęć, kilka odstępów i rozmiarów zdjęć portretowych.
3. ~~Etap 3 — szablony v2 „Wizytówka” i v3 „Klinika”~~: zarzucony. Szablonem strony
   zostaje v1 „Klasyczna”; makiety v2 i v3 nie są przenoszone.

## Import z prototypu gamstom

Cennik (30 pozycji, 5 kategorii jak w tabeli v1) i dane gabinetu zostały jednorazowo
przeniesione z prototypu `gamstom` skryptem `tools/importuj-z-gamstom.py` (usunięty po
imporcie, jest w historii git). Źródłem prawdy są pliki w `data/` edytowane w panelu.

Dane oznaczone w `gamstom` jako niepotwierdzone (do sprawdzenia z właścicielką):
godziny przyjęć (przykładowe), e-mail, dane rejestrowe (pola w „Dane gabinetu → Dane
rejestrowe” są puste — wiersz w stopce pojawi się po ich wpisaniu).

Rezerwacja online jest wyłączona (bez adresu i serwisu): wizyty umawia się tylko
telefonicznie, pod jednym numerem — komórkowym 699 904 989 (numer stacjonarny
usunięty ze strony). Włączenie w przyszłości: „Dane gabinetu → Rezerwacja online”
(adres profilu gabinetu, nazwa serwisu, nota o danych), plus bloki „Rezerwacja online”
na stronach i punkt o serwisie zewnętrznym w polityce prywatności.

## Archiwum

Katalog `archiwum/` przechowuje to, co warto było zachować z zakończonego prototypu
`cwichula/gamstom` (to repozytorium jest prywatne i zarchiwizowane, z pełną historią).
Hugo, panel i CI go nie czytają, więc nie wpływa na stronę.

- `archiwum/stara-strona/`: kopia starej strony dobrydentysta.legnica.pl z 1 października
  2026 r. (stan „przed”; z niej pochodzą stare adresy `*.php` przekierowywane w
  `hosting/.htaccess`). Zdjęcia bez EXIF/GPS, integralność: `_meta/MANIFEST.sha256`.

Makiety v1–v3, generator i obieg Pages CMS z prototypu nie zostały przeniesione.

## Aktualizacja Sveltia CMS

1. Pobierz nową wersję: `https://cdn.jsdelivr.net/npm/@sveltia/cms@<wersja>/dist/sveltia-cms.js`
   do `static/admin/sveltia-cms.js` (i `LICENSE.txt` do `LICENSE-sveltia-cms.txt`).
2. Zaktualizuj `static/admin/WERSJA-SVELTIA.txt` (wersja, SHA-256) i wersję w komentarzu
   `config.yml` / `index.html`.
3. Lokalnie `hugo server`, otwórz panel — ekran logowania pokazuje błędy konfiguracji,
   jeśli nowa wersja czegoś nie akceptuje. Sprawdź listę zmian: <https://github.com/sveltia/sveltia-cms/releases>.

### Plan awaryjny: Decap CMS

Konfiguracja trzyma się podzbioru zgodnego z Decap CMS 3.x tam, gdzie to możliwe.
Przy podmianie skryptu na Decap: dopisać `locale: pl`, a opcje tylko-Sveltia
(`media_libraries`, `reorder`, `preview_path`/`aliases`, `icon`, `slug.clean_accents`)
Decap zignoruje albo trzeba je usunąć — sprawdzić, czy panel się ładuje.

Znane ograniczenie Sveltii: przycisk szybkiego dodawania strony przy polach „Strona”
(np. w menu) ma napis „Dodaj Strona” — Sveltia składa go z nazwy kolekcji w mianowniku
(`label_singular`), której potrzebują też komunikaty commitów.

## Licencje

Sveltia CMS — MIT, © Kohei Yoshino (`static/admin/LICENSE-sveltia-cms.txt`).
