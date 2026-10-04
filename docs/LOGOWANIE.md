# Logowanie do panelu

Panel zapisuje zmiany przez API GitHuba jako zalogowana osoba, więc każda osoba
edytująca potrzebuje konta GitHub z prawem zapisu (**Write**) do tego repozytorium.

## Konto właścicielki

1. Konto GitHub z włączonym **2FA** i wydrukowanymi kodami zapasowymi.
2. Settings → Collaborators → zaproszenie z rolą **Write**; właścicielka akceptuje zaproszenie.

## Logowanie „Zaloguj się przez GitHub”

GitHub wymaga do tego małego serwera OAuth trzymającego tajny klucz. Używamy darmowego
Cloudflare Workera [sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth),
wdrożonego pod adresem **https://sveltia-cms-auth.cwichula.workers.dev**
(konto Cloudflare cwichula@gmail.com):

- Worker wgrany z wiersza poleceń (z klonu repozytorium sveltia-cms-auth):
  `npx wrangler login`, potem `npx wrangler deploy --keep-vars`. Uwaga: przycisk
  „Deploy to Cloudflare” trzeba wskazać na repozytorium **sveltia-cms-auth**, nie na to
  repozytorium — inaczej Cloudflare zgłasza „Could not detect a directory containing
  static files”.
- GitHub → Settings → Developer settings → **OAuth Apps** (nie GitHub Apps) →
  „Panel gabinet-strona”: Homepage `https://cwichula.github.io/gabinet-strona/`,
  Authorization callback URL `https://sveltia-cms-auth.cwichula.workers.dev/callback`.
- Sekrety Workera (`npx wrangler secret put <NAZWA> --name sveltia-cms-auth`):
  `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `ALLOWED_DOMAINS` = `cwichula.github.io`.
  Nowy client secret (np. po wycieku): wygenerować w OAuth App i wgrać tym samym poleceniem.
- `static/admin/config.yml`: `base_url` = adres Workera, `auth_methods: [oauth, token]`.

Błędy: „redirect_uri mismatch” = zły callback URL w OAuth App; komunikat o niedozwolonej
domenie = `ALLOWED_DOMAINS`.

## Logowanie tokenem (zapasowe)

Na ekranie logowania **„Zaloguj się za pomocą tokenu dostępu”** — panel podaje link do
utworzenia tokenu GitHub z właściwymi uprawnieniami (repozytorium: Contents read/write).
Token zostaje w przeglądarce. Wygodne dla wykonawcy, nie dla właścicielki.

Język panelu: polski, gdy przeglądarka ma ustawiony polski. Inaczej: ikona konta (prawy
górny róg) → Ustawienia → Język → Polski — raz w każdej przeglądarce/urządzeniu. Sveltia nie
ma opcji `locale` w konfiguracji; tłumaczenie pobiera z unpkg.com. Kilka nowszych komunikatów
Sveltii nie ma jeszcze polskiego tłumaczenia i wyświetla się po angielsku.
