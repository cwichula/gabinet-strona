# Stara strona — oryginalna kopia strony dobrydentysta.legnica.pl

> **Archiwum.** Dawny katalog `dane/` z zakończonego prototypu `cwichula/gamstom`
> (pełna historia: prywatne, zarchiwizowane repozytorium gamstom). 4 października 2026 r.
> ze zdjęć JPG usunięto EXIF/GPS (piksele bez zmian), a `_meta/MANIFEST.sha256`
> przeliczono. Oryginały z EXIF i notatki z audytu są tylko w kopii lokalnej.

**Data pobrania:** 2026-10-01
**Zrodlo:** http://dobrydentysta.legnica.pl/ (wylacznie HTTP — serwer nie ma waznego certyfikatu HTTPS)
**Metoda:** pobranie curl-em kazdego pliku, do ktorego odwoluje sie HTML, arkusz stylow i skrypt paska cookie
**Zawartosc:** 46 plikow serwisu (2 792 040 B = 2,66 MB) + metadane

## TO JEST FOLDER ZRODLOWY PROJEKTU

Ten folder jest **punktem odniesienia dla wszystkich dalszych zadan**. Jest to stan
"PRZED zmianami", zachowany jako dowod. Zasady:

1. **Nigdy nie modyfikuj niczego w `site/`.** Pracuj na kopiach, poza tym folderem.
2. Integralnosc mozna sprawdzic w kazdej chwili (patrz nizej) — jesli suma kontrolna
   sie nie zgadza, ktos naruszyl kopie i trzeba ja pobrac ponownie.

## Uklad folderu

```
stara-strona/
├── README.md                 <- ten plik
├── _meta/                    <- nasze notatki o kopii (NIE sa czescia serwisu)
│   ├── backup-log.txt        <- log pobrania: kod HTTP + rozmiar w bajtach dla kazdego pliku
│   └── MANIFEST.sha256       <- sumy kontrolne SHA-256 wszystkich 46 plikow serwisu
└── site/                     <- DOKLADNY mirror sciezek z serwera (1:1)
    ├── index.php.html        <- wyrenderowany HTML strony glownej
    ├── uslugi.php.html
    ├── cennik.php.html
    ├── nowosci.php.html
    ├── galeria.php.html
    ├── kontakt.php.html
    ├── default.css           <- jedyny arkusz stylow serwisu (3 959 B)
    ├── whcookies.js          <- pasek cookie z 2011 r., ladowany TYLKO na index.php
    ├── polityka-prywatnosci.pdf  <- 254 744 B, 2 strony, powoluje sie na uchylona ustawe z 1997 r.
    ├── images/               <- img01.jpg, img02.jpg, vv.jpg, zab.bmp (favicon w formacie BMP)
    ├── media/                <- 11.jpg, 11min.jpg, dom.png, cennik_2025.pdf
    └── galeria/
        ├── fancybox/         <- biblioteka lightboxa z 2010 r. (CSS + 2 skrypty)
        └── foto/             <- 13 zdjec wnetrza gabinetu + 13 miniatur
```

## WAZNE ZASTRZEZENIE — co to NIE jest

To jest kopia **wyrenderowanego HTML-a** pobranego po HTTP, a **nie kopia zrodel PHP**
z serwera. Pliki `*.php.html` to to, co widzi przegladarka, a nie tresc plikow `.php`
lezacych na serwerze. Z tej kopii **nie da sie odtworzyc serwera**.

**Przed pierwsza zmiana na serwerze trzeba zrobic osobny, pelny zrzut przez FTP**,
lacznie z plikiem `.htaccess` (jesli istnieje) i wszystkimi plikami `.php`.

## Czego na serwerze NIE MA (kody 404 w logu)

- `ie.css` — wolany komentarzem warunkowym dla Internet Explorera 7
- `jquery-1.4.3.min.js` — zapasowa kopia jQuery, wolana ze sciezki w katalogu glownym
- `robots.txt`, `sitemap.xml` — brak obu

## Jak sprawdzic, czy kopia nie zostala naruszona

Windows, PowerShell, z katalogu `archiwum/stara-strona`:

```powershell
Get-Content _meta\MANIFEST.sha256 | ForEach-Object {
  $s,$f = $_ -split '\s+\*?\./',2
  $h = (Get-FileHash "site\$f" -Algorithm SHA256).Hash.ToLower()
  if ($h -ne $s) { "ZMIENIONY: $f" }
}
```

Git Bash lub Linux, z katalogu `archiwum/stara-strona/site`:

```bash
sha256sum -c ../_meta/MANIFEST.sha256
```

Oczekiwany wynik: zero linii z komunikatem o zmianie / `OK` przy kazdym pliku.
