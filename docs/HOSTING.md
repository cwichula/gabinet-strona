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
Pomijane zawsze: `.well-known/`, `cgi-bin/`, `.user.ini`, `.ftpquota`, `.ovhconfig`.

## OVHcloud (Hosting WWW Start)

Wartości w panelu OVH (Web Cloud → Hosting):

| Skąd | Co | Zmienna / sekret |
|---|---|---|
| zakładka **FTP-SSH** | serwer `ftp.clusterNNN.hosting.ovh.net`, port 22 (SFTP) | `HOSTING_SERWER`, `HOSTING_PROTOKOL=sftp` |
| zakładka **FTP-SSH** | login główny i hasło (ustawić w panelu) | `HOSTING_UZYTKOWNIK`, `HOSTING_HASLO` |
| zakładka **Multisite** | katalog główny domeny, domyślnie `www` | `HOSTING_KATALOG=www` |
| zakładka **Informacje ogólne** | adres IPv4 / IPv6 klastra | do testu i do rekordów A / AAAA |

- SFTP musi być włączony w zakładce FTP-SSH. Ograniczeń IP dla FTP nie włączać
  (GitHub Actions łączy się z różnych adresów).
- `HOSTING_SSH_KNOWN_HOSTS`: `ssh-keyscan -p 22 ftp.clusterNNN.hosting.ovh.net`, a odcisk
  porównać z tym, co pokaże jedno ręczne logowanie (`sftp login@ftp.clusterNNN.hosting.ovh.net`
  albo FileZilla).
- `.ovhconfig` (wersja PHP, plik OVH) leży w katalogu głównym konta, nie w `www` — wysyłka
  i tak go pomija.
- **Do czasu certyfikatu strona działa po `http://`:** w `hosting/.htaccess` wymuszenie
  HTTPS jest zakomentowane, a `www.` prowadzi na `http://`; zmienna
  `HOSTING_ADRES=http://dobrydentysta.legnica.pl/` (w HTML są pełne adresy — kanoniczny,
  menu, dane strukturalne — z `https://` prowadziłyby na stronę bez certyfikatu).
  Po wydaniu certyfikatu: odkomentować blok HTTPS w `.htaccess`, w regule `www.` wpisać
  `https://`, usunąć zmienną `HOSTING_ADRES` i uruchomić workflow.
- Certyfikat Let's Encrypt (Multisite → SSL) OVH wydaje dopiero, gdy DNS domeny wskazuje na
  OVH. Przy przełączeniu jest więc krótkie okno bez certyfikatu: dzień wcześniej obniżyć TTL
  rekordów A/AAAA (np. 300 s), certyfikat zamówić zaraz po zmianie DNS.

### Test na OVH bez zmiany DNS

1. Multisite → dodaj domenę `dobrydentysta.legnica.pl` (i `www`), katalog `www`. Dla domeny
   spoza OVH panel poda rekord TXT `ovhcontrol` do dopisania u obecnego dostawcy DNS — nie
   zmienia to działania starej strony.
2. Na swoim komputerze w pliku `hosts` (Windows: `C:\Windows\System32\drivers\etc\hosts`,
   edytor uruchomiony jako administrator) dopisz:
   `<IP klastra> dobrydentysta.legnica.pl` i `<IP klastra> www.dobrydentysta.legnica.pl`.
3. Sprawdź:
   - `curl -I http://dobrydentysta.legnica.pl/` → 200 (po włączeniu SSL: jedno 301 na `https://…`, bez pętli),
   - `curl -I http://www.dobrydentysta.legnica.pl/` → 301 na adres bez `www.`,
   - `curl -I http://dobrydentysta.legnica.pl/cennik.php` → 301 na `/cennik/`,
   - `curl -I http://dobrydentysta.legnica.pl/nie-ma-takiej/` i `/admin/` → 404,
   - `curl -I --compressed http://dobrydentysta.legnica.pl/` → `content-encoding`,
     `x-content-type-options`, `expires`,
   - strona w przeglądarce: zdjęcia, menu, cennik.
4. Usuń wpisy z `hosts`.

Pętla przekierowań na HTTPS (OVH stoi za serwerem pośredniczącym): w `hosting/.htaccess`
zamienić warunki `%{HTTPS}` / `X-Forwarded-Proto` na `RewriteCond %{SERVER_PORT} ^80$`
i powtórzyć test.

## Domena: zmiana DNS czy transfer

Do uruchomienia strony wystarczy **zmiana rekordów A/AAAA** domeny i `www` na adres OVH.
Transfer domeny (zmiana rejestratora) to osobna, nieobowiązkowa sprawa.

1. Rejestrator: WHOIS dla `dobrydentysta.legnica.pl` na <https://dns.pl/whois> (domena
   regionalna, rejestr NASK) — kto ją prowadzi i kto ma dostęp do panelu.
2. **Wariant A — domena zostaje** (prostszy): u obecnego dostawcy DNS rekord TXT
   `ovhcontrol`, potem A/AAAA na OVH. MX (poczta) bez zmian.
3. **Wariant B — transfer do OVH**: sprawdzić w OVH, czy obsługuje `.legnica.pl`; u obecnego
   rejestratora pobrać kod **AuthInfo** (ważny 14 dni) i zamówić w OVH transfer z tym kodem.
   Przed transferem przepisać w strefie DNS OVH wszystkie rekordy (A, AAAA, MX, TXT), żeby
   nic nie przestało działać, gdy domena zacznie używać serwerów DNS OVH.

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
