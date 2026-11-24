# Librus MCP na Vercel

Projekt Vercel korzysta z katalogu `deploy/vercel`. Punkt końcowy MCP
to `/mcp`, przez HTTPS i z nagłówkiem `Authorization: Bearer <token>`.

W ustawieniach projektu dodaj poniższe zmienne tylko dla środowiska
Production. Wybierz Sensitive i wykonaj ponowne wdrożenie.

| Zmienna | Wartość |
| --- | --- |
| `LIBRUS_USERNAME` | Login rodzica do Librus Synergia |
| `LIBRUS_PASSWORD` | Hasło do Librus Synergia |
| `LIBRUS_MCP_TOKEN` | Losowy token, np. wynik `openssl rand -hex 32` |
| `LIBRUS_CONTEXT_KEY` | Oddzielny losowy klucz z `openssl rand -hex 32` |

Klient MCP potrzebuje tokenu. Klucz kontekstu i poświadczenia Librusa
pozostają w Vercel. Token daje dostęp do danych skonfigurowanego konta.

Wdrożenie wymaga systemowej zmiennej `VERCEL_PROJECT_PRODUCTION_URL`.
Bez kompletnej konfiguracji endpoint odpowiada 503. Przy aktywnej
konfiguracji żądanie bez tokenu otrzymuje 401.

Vercel Functions mają ulotny system plików. W tej konfiguracji wyłączone
są powiadomienia z zapisem stanu, załączniki i wysyłanie wiadomości.
Otwarcie wiadomości odebranej wymaga zgody na oznaczenie jej jako przeczytanej.
