# Hosting na własnej domenie (dobrydentysta.legnica.pl)

Ten sam workflow buduje drugą wersję strony — z adresem domeny, bez panelu `/admin/`
(panel zostaje na github.io, tam działa logowanie) i z plikiem `hosting/.htaccess` —
i wysyła ją na hosting przez **SFTP** albo **FTPS** (`lftp mirror`). Job `hosting`
uruchamia się dopiero, gdy ustawiona jest zmienna `HOSTING_SERWER`; do tego czasu
nic się nie zmienia. Widoczność w Google ustawia się dalej w panelu
(„Ukryj stronę przed wyszukiwarkami”) i dotyczy tylko wersji na domenie.

`hosting/.htaccess` (Apache / LiteSpeed): HTTPS i adres bez `www.`, przekierowania
301 ze starych adresów (`uslugi.php` → `/uslugi/`, `cennik.php` → `/cennik/`,
`nowosci.php` → `/wyposazenie/`, `galeria.php`, `kontakt.php`, stare PDF i zdjęcia),
strona 404, kompresja, pamięć podręczna i nagłówki bezpieczeństwa.

## Konfiguracja (jednorazowo)

Settings → Secrets and variables → Actions:

| Rodzaj | Nazwa | Wartość |
|---|---|---|
| Variable | `HOSTING_SERWER` | adres serwera z panelu hostingu, np. `s123.hosting.pl` |
| Variable | `HOSTING_PROTOKOL` | `sftp` (zalecany) albo `ftps` |
| Variable | `HOSTING_KATALOG` | katalog strony na serwerze, np. `public_html` albo `domains/dobrydentysta.legnica.pl/public_html` |
| Variable | `HOSTING_PORT` | tylko gdy inny niż domyślny (np. SFTP na porcie 2222) |
| Variable | `HOSTING_ADRES` | tylko gdy inny niż `https://dobrydentysta.legnica.pl/` |
| Variable | `HOSTING_SSH_KNOWN_HOSTS` | dla SFTP **wymagane**: wynik `ssh-keyscan -p <port> <serwer>`, sprawdzony z odciskiem klucza od firmy hostingowej (bez tego wysyłka się nie zacznie) |
| Secret | `HOSTING_UZYTKOWNIK` | login FTP/SFTP |
| Secret | `HOSTING_HASLO` | hasło FTP/SFTP |

Bezpieczeństwo plików na serwerze: wysyłka **usuwa** z katalogu pliki, których nie ma
w nowej wersji strony, ale tylko wtedy, gdy w katalogu leży znacznik `.gabinet-strona`
(zostawia go pierwsza udana wysyłka). Pierwsza wysyłka tylko dodaje i nadpisuje.
Pomijane zawsze: `.well-known/`, `cgi-bin/`, `.user.ini`, `.ftpquota`.

## Przeniesienie domeny — kolejność

1. Hosting: dodać domenę `dobrydentysta.legnica.pl`, założyć konto FTP/SFTP do jej katalogu.
2. GitHub: zmienne i sekrety jak wyżej, potem Actions → „Strona…” → **Run workflow**.
   Job `hosting` musi skończyć się na zielono. Strony jeszcze nie widać pod domeną.
3. Poczta: rekord MX domeny wskazuje dziś na stary serwer. Jeśli ktoś używa skrzynki
   `…@dobrydentysta.legnica.pl`, przenieść ją przed zmianą DNS.
4. DNS: rekord A (i AAAA, jeśli hosting podaje) domeny i `www` na adres nowego hostingu.
5. Hosting: włączyć certyfikat SSL (Let's Encrypt) dla domeny i `www` — `.htaccess`
   przekierowuje na HTTPS. Sprawdzić: `https://dobrydentysta.legnica.pl/`,
   `http://…` i `www.…` (przekierowanie), `/cennik.php` (301 na `/cennik/`),
   `/nie-ma-takiej/` (strona 404 gabinetu).
6. Stary hosting wyłączyć po kilku dniach, gdy zmiana DNS rozejdzie się po sieci.
7. Po uzupełnieniu danych (godziny, dane rejestrowe, polityka prywatności):
   panel → Ustawienia → wyłączyć „Ukryj stronę przed wyszukiwarkami”, potem Google
   Search Console: dodać domenę i wysłać `sitemap.xml`.
