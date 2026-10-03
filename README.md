# Strona gabinetu stomatologicznego (Hugo + Sveltia CMS)

Strona gabinetu lek. stom. Doroty Rożdżestwieńskiej w Legnicy. Treść (strony, menu,
cennik, dane gabinetu) jest edytowana w panelu pod **`/admin/`** — właścicielka loguje
się swoim kontem GitHub, a każdy zapis w panelu to commit w tym repozytorium, po którym
strona sama się przebudowuje i publikuje.

- Strona: <https://cwichula.github.io/gabinet-strona/>
- Panel: <https://cwichula.github.io/gabinet-strona/admin/>

Etap 1 (ten stan repozytorium): instalacja i test panelu na celowo prostym szablonie
`v0-test`. Wygląd przyjdzie w etapie 2 (szablon v1) — **bez żadnej zmiany w treści**.

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
content/strony/<slug>/index.md   podstrona + jej zdjęcia obok (page bundle)
data/menu.yaml                   menu (dwa poziomy)
data/cennik.yaml                 cennik: kategorie -> pozycje
data/gabinet.yaml                dane gabinetu, godziny, rezerwacja, dane rejestrowe
data/ustawienia.yaml             domyślny opis SEO, tekst stopki
assets/images/                   zdjęcia wspólne (np. strony głównej)
themes/v0-test/                  szablon testowy
layouts/                         PUSTY (nadpisałby każdy szablon) - pilnuje CI
static/admin/                    panel: index.html, config.yml, sveltia-cms.js
docs/KONTRAKT-BLOKOW.md          typy bloków i ich pola
tools/sprawdz-kontrakt.py        kontrola kontraktu (CI)
tools/importuj-z-gamstom.py      jednorazowy import cennika i danych z repo gamstom
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
python tools/sprawdz-kontrakt.py      # wymaga PyYAML
hugo --gc --minify                    # bez ERROR i bez WARN
```

## Logowanie do panelu

Panel zapisuje zmiany przez API GitHuba jako zalogowana osoba, więc każda osoba
edytująca potrzebuje konta GitHub z prawem zapisu (**Write**) do tego repozytorium.

### Konto właścicielki

1. Konto GitHub z włączonym **2FA** i wydrukowanymi kodami zapasowymi.
2. Settings → Collaborators → zaproszenie z rolą **Write**; właścicielka akceptuje zaproszenie.

### Logowanie „Zaloguj się przez GitHub” (docelowe)

GitHub wymaga do tego małego serwera OAuth. Używamy darmowego Cloudflare Workera
[sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth):

1. Wdróż Workera (przycisk „Deploy to Cloudflare Workers” w jego README). Zanotuj adres,
   np. `https://sveltia-cms-auth.<konto>.workers.dev`.
2. GitHub → Settings → Developer settings → **OAuth Apps → New OAuth App**:
   - Homepage URL: `https://cwichula.github.io/gabinet-strona/`
   - Authorization callback URL: `<adres Workera>/callback`
   - Zapisz, potem **Generate a new client secret**.
3. Cloudflare → Worker → Settings → Variables:
   - `GITHUB_CLIENT_ID` = Client ID,
   - `GITHUB_CLIENT_SECRET` = Client secret (zaszyfrowany — **Encrypt**),
   - `ALLOWED_DOMAINS` = `cwichula.github.io`.
4. W `static/admin/config.yml` w sekcji `backend` odkomentuj `base_url:`, wpisz adres
   Workera i usuń linię `auth_methods: [token]`. Commit → po publikacji na ekranie
   logowania pojawia się przycisk „Zaloguj się przez GitHub”. (Do tego czasu jest ukryty:
   bez `base_url` kierowałby do Netlify i nie działał.)

### Logowanie tokenem (działa od razu; do czasu wdrożenia Workera jedyne)

Na ekranie logowania **„Zaloguj się za pomocą tokenu dostępu”** — panel podaje link do
utworzenia tokenu GitHub z właściwymi uprawnieniami (repozytorium: Contents read/write).
Token zostaje w przeglądarce. Wygodne dla wykonawcy, nie dla właścicielki.

Język panelu: polski, gdy przeglądarka ma ustawiony polski (albo wybierz go w ustawieniach
panelu). Sveltia nie ma opcji `locale` w konfiguracji; tłumaczenie pobiera z unpkg.com.

## Co można robić w panelu

| Kolekcja | Plik | Co |
|---|---|---|
| Strony | `content/strony/<slug>/index.md` | dodawanie, usuwanie, ukrywanie (szkic), kolejność (przeciąganie), bloki treści, zdjęcia |
| Strona główna | `content/_index.md` | bloki treści strony głównej |
| Menu | `data/menu.yaml` | pozycje, podmenu, kolejność; strona wybierana z listy |
| Cennik | `data/cennik.yaml` | kategorie i pozycje; zmiana ceny widoczna na każdej stronie z blokiem cennika |
| Dane gabinetu | `data/gabinet.yaml` | adres, telefony, e-mail, godziny, rezerwacja online, dane rejestrowe |
| Ustawienia | `data/ustawienia.yaml` | domyślny opis SEO, tekst stopki |

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
  (maks. 2048 px, limit 1 MB po konwersji), a Hugo robi z nich wersje do 1600 px.
  Opis zdjęcia (alt) jest wymagany.
- **Ceny** są tylko w cenniku; bloki cennika na stronach wskazują kategorie.

## Publikacja

Każdy commit na `main` uruchamia `.github/workflows/pages.yml`:

1. `tools/sprawdz-kontrakt.py` — kontrakt bloków i pusty `layouts/`,
2. Hugo 0.167.0 Extended (pobrany z wydania na GitHubie, suma SHA-256 sprawdzana) —
   każdy **ERROR** i każde **WARN** przerywa przebieg,
3. kontrola wyniku (strona główna, panel),
4. publikacja na GitHub Pages.

Błąd na dowolnym kroku = w sieci zostaje poprzednia wersja, a w repozytorium powstaje
zgłoszenie (issue) „Strona nie została opublikowana…” z linkiem do logu. Zmiana jest
w sieci zwykle 1–2 minuty po zapisie (plus do 10 minut pamięci podręcznej Pages).

Jednorazowo w ustawieniach repozytorium: Settings → Pages → Source: **GitHub Actions**.

## Szablony

Szablon to katalog w `themes/` wybierany jedną linią `theme:` w `hugo.yaml`. Każdy
szablon ma ten sam zestaw:

```
themes/<nazwa>/layouts/_default/baseof.html, home.html, single.html
themes/<nazwa>/layouts/404.html
themes/<nazwa>/layouts/_default/_markup/render-link.html   (odnośniki /slug/ w treści)
themes/<nazwa>/layouts/partials/nav.html, footer.html, image.html, sekcje.html ...
themes/<nazwa>/layouts/partials/blocks/<typ>.html          (po jednym na typ bloku)
themes/<nazwa>/assets/css/...
```

Katalog `layouts/` w korzeniu musi zostać pusty — inaczej nadpisałby każdy szablon.

## Kontrakt bloków

Strona to lista bloków (`sekcje`): hero, tekst, karty, faq, cennik, galeria, godziny,
mapa, cta, kontakt. Pola każdego typu opisuje [`docs/KONTRAKT-BLOKOW.md`](docs/KONTRAKT-BLOKOW.md).
Nowy typ bloku = wpis w kontrakcie + typ w `config.yml` + partial we **wszystkich**
szablonach; `tools/sprawdz-kontrakt.py` nie przepuści niekompletnej zmiany.

## Etapy

1. **Etap 1 — instalacja i test panelu** (szablon `v0-test`): repozytorium, publikacja,
   kontrakt bloków, panel z kolekcjami, treść startowa, cennik i dane z `gamstom`.
   Pozostaje: OAuth App + Worker + `base_url`, konto właścicielki (Write, 2FA), lista
   testów z planu — etap zamknięty, gdy przejdzie ją właścicielka na swoim koncie.
2. **Etap 2 — szablon v1 „Klasyczna”**: pocięcie makiety v1 z `gamstom` na szablon;
   kryterium: `theme: v1-klasyczna` i zero zmian w `content/` i `data/`. Kontrola
   zwrotów zakazanych (`check-site.py`) jako krok CI.
3. **Etap 3 — szablony v2 „Wizytówka” i v3 „Klinika”**: ten sam kontrakt; podgląd
   szablonu bez ruszania produkcji (ręczny workflow z `--theme`).

## Import z repozytorium gamstom

`tools/importuj-z-gamstom.py` jednorazowo przeniósł z `gamstom` cennik (30 pozycji,
5 kategorii jak w tabeli v1) i dane gabinetu. Od teraz źródłem prawdy są pliki w `data/`
(edytowane w panelu) — ponowne uruchomienie skryptu nadpisałoby zmiany z panelu.

Dane oznaczone w `gamstom` jako niepotwierdzone (do sprawdzenia z właścicielką):
godziny przyjęć (przykładowe), e-mail, dane rejestrowe (`DO_UZUPEŁNIENIA`) i adres
rezerwacji online (obecnie wyszukiwarka Booksy, a nie profil gabinetu — do zmiany
albo wyłączenia w „Dane gabinetu → Rezerwacja online”).

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

## Licencje

Sveltia CMS — MIT, © Kohei Yoshino (`static/admin/LICENSE-sveltia-cms.txt`).
