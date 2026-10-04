#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kontrola jakosci i zgodnosci zbudowanej strony (wynik Hugo w public/).

Przeniesienie istoty tools/check-site.py z prototypu gamstom na wynik Hugo - dziala na
gotowym HTML, wiec jest niezalezne od szablonu (v1-klasyczna, v0-test, ...).
Uruchamiane w CI po budowaniu; blad = strona nie zostaje opublikowana.

Sprawdza na kazdej stronie HTML (poza panelem admin/):
  - dokladnie jeden, niepusty <h1>; kolejnosc naglowkow (bez przeskokow);
  - <img>: atrybut alt, width i height; proporcje zgodne z plikiem;
  - linki i zasoby wewnetrzne prowadza do istniejacych plikow (z prefiksem
    adresu strony, np. /gabinet-strona/), kotwice #id istnieja, brak
    powtorzonych id;
  - zadnych zasobow z obcych serwerow (src, srcset, link rel=stylesheet/icon/
    preload..., url() w CSS i atrybutach style); obce sa tylko zwykle odnosniki
    <a>, a ich serwery musza byc na liscie DOZWOLONE_SERWERY;
  - zadnej ramki <iframe> w HTML - mapa powstaje dopiero po kliknieciu
    (element data-map z przyciskiem data-map-load, adres w data-map-src);
  - JSON-LD jest poprawnym JSON-em, FAQPage zgadza sie z widocznymi pytaniami;
  - zwroty niedozwolone w materialach gabinetu lekarskiego (art. 14 ust. 1
    ustawy o dzialalnosci leczniczej) - lista i logika z check-site.py;
  - rezerwacja online (data/gabinet.yaml -> rezerwacja): odnosniki z target
    _blank i rel noopener noreferrer, adres zgodny z danymi, telefon obok,
    brak ReserveAction przed potwierdzeniem, nic o dostawcy przy wylaczonej;
  - tytul, opis, adres kanoniczny, niepodstawione znaczniki, sitemap.xml.
Na koncu zestawienie wagi stron (HTML, CSS, JS, zdjecia) - tylko uwagi.

Tylko biblioteka standardowa Pythona. Kod wyjscia 1 = co najmniej jeden blad.

Uzycie:
    python tools/kontrola-strony.py                  # katalog public/
    python tools/kontrola-strony.py sciezka/do/wyniku
    python tools/kontrola-strony.py public --baseurl https://example.org/podkatalog/
Adres strony (i prefiks sciezki) domyslnie z <link rel=canonical> strony
glownej, a gdy go brak - z baseURL w hugo.yaml.
"""

from __future__ import annotations

import argparse
import gzip
import html as html_mod
import json
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent

# Katalogi wyniku, ktorych nie sprawdzamy jak stron serwisu (panel CMS laczy
# sie z GitHubem z definicji).
POMIJANE = ("admin/",)

# Serwery, do ktorych wolno prowadzic ZWYKLYM odnosnikiem <a> (nic nie jest
# pobierane przy wejsciu na strone). Odnosnik do innego serwera = uwaga.
DOZWOLONE_SERWERY = {
    "booksy.com", "www.booksy.com",          # rezerwacja online (data/gabinet.yaml)
    "www.google.com", "google.com", "maps.google.com",  # nawigacja / mapa
    "goo.gl", "maps.app.goo.gl",
    "www.gov.pl", "gov.pl", "rpwdl.ezdrowie.gov.pl", "nil.org.pl",
    "uodo.gov.pl", "www.uodo.gov.pl",
}

# Atrybut z obcym adresem, ktory skrypt laduje dopiero po zgodzie (klik).
# Wolno go uzyc tylko na elemencie z atrybutem "brama" i tylko dla tych serwerow.
BRAMY_ZGODY = {
    "data-map-src": {"brama": "data-map", "przycisk": "data-map-load",
                     "serwery": {"www.google.com", "google.com", "maps.google.com"}},
}

# Atrybuty <link rel=...>, ktore cos POBIERAJA (canonical/alternate nie).
REL_POBIERA = {"stylesheet", "icon", "shortcut", "apple-touch-icon", "manifest",
               "preload", "prefetch", "preconnect", "dns-prefetch", "modulepreload",
               "mask-icon"}

# Zrodla w kodzie, ktore nie sa adresami do pobrania (przestrzenie nazw).
NIE_ADRESY = ("http://www.w3.org/", "https://www.w3.org/", "http://www.sitemaps.org/",
              "https://schema.org", "http://schema.org", "https://ogp.me/")

# Zwroty niedozwolone w materialach gabinetu lekarskiego (art. 14 ust. 1 ustawy
# o dzialalnosci leczniczej - informacja tak, reklama nie). Lista i logika
# przeniesione 1:1 z check-site.py z prototypu gamstom.
#
# ZAKAZANE to zwroty, ktore sa reklama bez wzgledu na kontekst (blad).
# PODEJRZANE w jednym zdaniu sa reklama, a w drugim zwyklym polskim - uwaga
# do przeczytania przez czlowieka, nie blad blokujacy publikacje.
ZAKAZANE = [
    r"\bgwarantujemy\b",
    r"\bgwarancj\w*\s+(?:sukcesu|efektu|wyleczenia|rezultatu)",
    r"\b100\s*%\s*(?:skuteczn|gwarancj|pewn)",
    r"\bpromocj\w*\b", r"\brabat\w*\b", r"\bzni[zż]k\w*\b",
    r"\bbezbole[sś]nie\b",
    r"\bnajlepsz\w*\s+(?:dentyst|stomatolog|gabinet|klinik|lekarz|specjalist|w\s+Legnicy|na\s+rynku)",
    r"\bjeste[sś]my\s+najlepsi\b", r"\bnumer\s+jeden\b", r"\bnr\s*1\b",
    r"\blepsi\s+ni[zż]\b", r"\bjedyny\s+taki\b",
    r"\bnajta[nń]sz\w*\b",
]

PODEJRZANE = [
    r"\bbez\s+b[oó]lu\b", r"\bnajlepsz\w*\b", r"\bbez\s+stresu\b",
    r"\bnajnowocze[sś]niejsz\w*\b", r"\bunikaln\w*\b",
]

# Zwroty podejrzane WYLACZNIE w zdaniu o rezerwacji online (obietnica terminu,
# ktorej gabinet nie moze dac). Zawsze uwaga, nigdy blad.
PODEJRZANE_REZERWACJA = [
    r"\b24\s*/\s*7\b",
    r"\bca[lł]odobow\w*\b", r"\bprzez\s+ca[lł][aą]\s+dob[eę]\b",
    r"\bnatychmiast\w*\b",
    r"\bw\s+kilka\s+sekund\b",
    r"\bbez\s+czekania\b",
]

# Progi zestawienia wagi (orientacyjne, jak w Lighthouse "unikaj ogromnych
# ladunkow sieciowych") - przekroczenie to uwaga, nie blad.
PROG_STRONA = 1_600_000      # cala strona przy najwiekszych wariantach zdjec
PROG_STRONA_START = 600_000  # to, co laduje sie od razu (bez loading=lazy)
PROG_ZDJECIE = 250_000       # pojedynczy plik zdjecia
PROG_HTML = 100_000
PROG_CSS = 100_000
PROG_JS = 60_000

NAGLOWKI = ("h1", "h2", "h3", "h4", "h5", "h6")


# ---------------------------------------------------------------- narzedzia

def zaprzeczone(przed: str) -> bool:
    """Czy tuz przed trafieniem stoi zaprzeczenie ("Nie oferujemy rabatu")."""
    return bool(re.search(r"\b(?:nie|bez|nigdy|[zż]adn\w*|wykluczamy|zakaz\w*)\b[^.!?]{0,60}$",
                          przed, re.I))


def normalizuj(t: str) -> str:
    return re.sub(r"\s+", " ", html_mod.unescape(t)).strip()


def luzno(t: str) -> str:
    """Do porownan tekstu z JSON-LD z HTML: same litery i cyfry, male litery
    (znaczniki wierszowe typu <strong>100 zł</strong>. wstawiaja odstepy)."""
    return re.sub(r"[\W_]+", "", t.lower())


def kandydaci_srcset(wartosc: str) -> list[tuple[str, str]]:
    """srcset -> [(adres, deskryptor)]. Adresy Hugo nie zawieraja przecinkow."""
    wynik = []
    for czesc in wartosc.split(","):
        czesc = czesc.strip()
        if not czesc:
            continue
        kawalki = czesc.split()
        wynik.append((kawalki[0], kawalki[1] if len(kawalki) > 1 else ""))
    return wynik


def wymiary_obrazu(plik: Path) -> tuple[int, int] | None:
    """Szerokosc i wysokosc pliku PNG/JPEG/WebP/GIF (tylko naglowek)."""
    try:
        dane = plik.read_bytes()
    except OSError:
        return None
    try:
        if dane[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", dane[16:24])
        if dane[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", dane[6:10])
        if dane[:4] == b"RIFF" and dane[8:12] == b"WEBP":
            rodzaj = dane[12:16]
            if rodzaj == b"VP8 ":
                w, h = struct.unpack("<HH", dane[26:30])
                return w & 0x3FFF, h & 0x3FFF
            if rodzaj == b"VP8L":
                b = dane[21:25]
                w = 1 + (((b[1] & 0x3F) << 8) | b[0])
                h = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
                return w, h
            if rodzaj == b"VP8X":
                w = 1 + int.from_bytes(dane[24:27], "little")
                h = 1 + int.from_bytes(dane[27:30], "little")
                return w, h
        if dane[:2] == b"\xff\xd8":
            i = 2
            while i < len(dane) - 9:
                if dane[i] != 0xFF:
                    i += 1
                    continue
                znacznik = dane[i + 1]
                if znacznik in (0xD8, 0x01) or 0xD0 <= znacznik <= 0xD7:
                    i += 2
                    continue
                dlugosc = struct.unpack(">H", dane[i + 2:i + 4])[0]
                if znacznik in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", dane[i + 5:i + 9])
                    return w, h
                i += 2 + dlugosc
    except (struct.error, IndexError):
        return None
    return None


def kb(n: int) -> str:
    return f"{n / 1024:,.0f} KB".replace(",", " ")


# ------------------------------------------------------- dane gabinetu (YAML)

def wczytaj_rezerwacje() -> dict:
    """data/gabinet.yaml -> rezerwacja (bez PyYAML: plik ma prosty, plaski blok).

    Brak pliku albo bloku nie jest bledem - kontrole rezerwacji sie pomija."""
    plik = REPO / "data" / "gabinet.yaml"
    if not plik.is_file():
        return {}
    try:
        import yaml  # type: ignore
        dane = yaml.safe_load(plik.read_text(encoding="utf-8")) or {}
        rez = dane.get("rezerwacja")
        return rez if isinstance(rez, dict) else {}
    except ImportError:
        pass
    except Exception:
        return {}
    rez: dict = {}
    w_bloku = False
    for wiersz in plik.read_text(encoding="utf-8").splitlines():
        if re.match(r"^rezerwacja:\s*$", wiersz):
            w_bloku = True
            continue
        if w_bloku:
            if wiersz and not wiersz.startswith((" ", "\t", "#")):
                break
            m = re.match(r"^\s+([A-Za-z_]+):\s*(.*?)\s*$", wiersz)
            if not m:
                continue
            klucz, wartosc = m.groups()
            if wartosc.startswith(("'", '"')) and wartosc.endswith(wartosc[0]) and len(wartosc) > 1:
                wartosc = wartosc[1:-1]
            if wartosc.lower() in ("true", "false"):
                rez[klucz] = wartosc.lower() == "true"
            else:
                rez[klucz] = wartosc
    return rez


# ------------------------------------------------------------- parser strony

class Strona(HTMLParser):
    """Jeden przebieg po HTML: naglowki, obrazki, odnosniki, zasoby, id, JSON-LD."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.naglowki: list[tuple[str, str]] = []
        self.obrazki: list[dict] = []
        self.odnosniki: list[dict] = []     # <a href>, <area href>
        self.zasoby: list[tuple[str, str, str]] = []  # (adres, skad, rodzaj)
        self.ramki: list[dict] = []
        self.jsonld: list[str] = []
        self.ids: list[str] = []
        self.style_atr: list[str] = []
        self.style_bloki: list[str] = []
        self.bramy: list[dict] = []         # elementy z bramy zgody
        self.podsumowania: list[str] = []   # tekst <summary>
        self.bledy_bram: list[str] = []
        self.meta: dict[str, str] = {}
        self.link_rel: list[tuple[str, str]] = []
        self.tytul = ""
        self.html_lang = None
        self.obce_atrybuty: list[tuple[str, str, str]] = []
        self._stos: list[str] = []
        self._naglowek: str | None = None
        self._tekst_n: list[str] = []
        self._ld = False
        self._ld_tekst: list[str] = []
        self._styl = False
        self._styl_tekst: list[str] = []
        self._summary = False
        self._summary_tekst: list[str] = []
        self._tytul = False
        self._brama_glebokosc: list[int] = []
        self._obraz_w_picture: list[dict] = []
        self._zrodla_picture: list[tuple[str, str]] = []

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr"}

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        linia = self.getpos()[0]
        if tag not in self.VOID:
            self._stos.append(tag)
        if tag == "html":
            self.html_lang = a.get("lang")
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "name" in a:
            self.ids.append(a["name"])
        if "style" in a:
            self.style_atr.append(a["style"])
        if tag in NAGLOWKI:
            self._naglowek = tag
            self._tekst_n = []
        if tag == "title":
            self._tytul = True
        if tag == "summary":
            self._summary = True
            self._summary_tekst = []
        if tag == "style":
            self._styl = True
            self._styl_tekst = []
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._ld = True
            self._ld_tekst = []
        if tag == "meta":
            klucz = a.get("name") or a.get("property")
            if klucz:
                self.meta[klucz.lower()] = a.get("content", "")
                if klucz.lower() in ("og:image", "twitter:image"):
                    self.zasoby.append((a.get("content", ""), f"<meta {klucz}>", "meta"))
        if tag == "picture":
            self._zrodla_picture = []
        if tag == "source":
            if a.get("srcset"):
                for adres, _ in kandydaci_srcset(a["srcset"]):
                    self.zasoby.append((adres, "<source srcset>", "zasob"))
                self._zrodla_picture.append((a.get("type", ""), a["srcset"]))
            if a.get("src"):
                self.zasoby.append((a["src"], "<source src>", "zasob"))
        if tag == "img":
            obr = {"attrs": a, "linia": linia,
                   "zrodla": list(self._zrodla_picture) if "picture" in self._stos else []}
            self.obrazki.append(obr)
            if a.get("srcset"):
                for adres, _ in kandydaci_srcset(a["srcset"]):
                    self.zasoby.append((adres, "<img srcset>", "zasob"))
        if tag in ("a", "area") and "href" in a:
            self.odnosniki.append({"href": a["href"], "attrs": a, "linia": linia, "tag": tag})
        if tag == "link" and a.get("href"):
            rel = set(a.get("rel", "").lower().split())
            self.link_rel.append((a.get("rel", ""), a["href"]))
            rodzaj = "zasob" if rel & REL_POBIERA else "link"
            self.zasoby.append((a["href"], f"<link rel={a.get('rel', '')}>", rodzaj))
        for atr in ("src", "poster", "data"):
            if a.get(atr) and not (tag == "source" and atr == "src"):
                self.zasoby.append((a[atr], f"<{tag} {atr}>", "zasob"))
        if tag in ("svg", "use", "image") or "use" in self._stos:
            for atr in ("href", "xlink:href"):
                if a.get(atr) and tag in ("use", "image"):
                    self.zasoby.append((a[atr], f"<{tag} {atr}>", "zasob"))
        if tag == "iframe":
            self.ramki.append({"attrs": a, "linia": linia})
        # atrybuty data-* z adresami (np. podglad zdjecia w okienku)
        for k, v in a.items():
            if not k.startswith("data-") or not v:
                continue
            if k in BRAMY_ZGODY:
                regula = BRAMY_ZGODY[k]
                if regula["brama"] not in a:
                    self.bledy_bram.append(
                        f"{k} poza elementem z {regula['brama']} (linia {linia}) — "
                        "obcy adres bez bramy zgody")
                host = urlsplit(v).hostname or ""
                if host not in regula["serwery"]:
                    self.bledy_bram.append(f"{k} wskazuje nieoczekiwany serwer: {v}")
                continue
            if re.match(r"^(https?:)?//", v):
                self.obce_atrybuty.append((k, v, tag))
            elif v.startswith("/") or re.search(r"\.(?:jpe?g|png|webp|avif|gif|svg)$", v):
                self.zasoby.append((v, f"<{tag} {k}>", "zasob"))
        for regula in BRAMY_ZGODY.values():
            if regula["brama"] in a and tag not in self.VOID:
                self.bramy.append({"linia": linia, "przycisk": False, "regula": regula,
                                   "glebokosc": len(self._stos)})
        for brama in self.bramy:
            if brama.get("zamknieta"):
                continue
            if brama["regula"]["przycisk"] in a:
                brama["przycisk"] = True

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if tag in self._stos:
            while self._stos:
                zdjety = self._stos.pop()
                if zdjety == tag:
                    break
        for brama in self.bramy:
            if not brama.get("zamknieta") and len(self._stos) < brama["glebokosc"]:
                brama["zamknieta"] = True
        if tag == self._naglowek:
            self.naglowki.append((tag, normalizuj("".join(self._tekst_n))))
            self._naglowek = None
        if tag == "title":
            self._tytul = False
        if tag == "summary" and self._summary:
            self.podsumowania.append(normalizuj("".join(self._summary_tekst)))
            self._summary = False
        if tag == "style" and self._styl:
            self.style_bloki.append("".join(self._styl_tekst))
            self._styl = False
        if tag == "script" and self._ld:
            self.jsonld.append("".join(self._ld_tekst))
            self._ld = False
        if tag == "picture":
            self._zrodla_picture = []

    def handle_data(self, data):
        if self._naglowek:
            self._tekst_n.append(data)
        if self._tytul:
            self.tytul += data
        if self._summary:
            self._summary_tekst.append(data)
        if self._styl:
            self._styl_tekst.append(data)
        if self._ld:
            self._ld_tekst.append(data)


def tekst_widoczny(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|svg|template)\b.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    return normalizuj(html)


def adresy_css(css: str) -> list[str]:
    wynik = []
    for m in re.finditer(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""", css):
        wynik.append(m.group(2).strip())
    for m in re.finditer(r"""@import\s+(?:url\()?\s*['"]?([^'");\s]+)""", css):
        wynik.append(m.group(1).strip())
    return [u for u in wynik if not u.startswith(("data:", "#"))]


# ---------------------------------------------------------------- kontrola

class Kontrola:
    def __init__(self, katalog: Path, baseurl: str):
        self.katalog = katalog
        self.baseurl = baseurl if baseurl.endswith("/") else baseurl + "/"
        cz = urlsplit(self.baseurl)
        self.host = cz.hostname or ""
        self.schemat = cz.scheme
        self.prefiks = cz.path or "/"
        self.rez = wczytaj_rezerwacje()
        self.strony: dict[Path, Strona] = {}
        self.html: dict[Path, str] = {}
        self.ids: dict[Path, set[str]] = {}
        self.bledy: dict[str, list[str]] = {}
        self.uwagi: dict[str, list[str]] = {}
        self.zestawienie: list[dict] = []
        self.ostrzezone_obrazy: set[str] = set()

    # --- pomocnicze
    def nazwa(self, plik: Path) -> str:
        return plik.relative_to(self.katalog).as_posix()

    def blad(self, gdzie: str, tekst: str):
        lista = self.bledy.setdefault(gdzie, [])
        if tekst not in lista:
            lista.append(tekst)

    def uwaga(self, gdzie: str, tekst: str):
        lista = self.uwagi.setdefault(gdzie, [])
        if tekst not in lista:
            lista.append(tekst)

    def adres_strony(self, plik: Path) -> str:
        wzgl = self.nazwa(plik)
        if wzgl.endswith("index.html"):
            wzgl = wzgl[: -len("index.html")]
        return self.baseurl + wzgl

    def rozwiaz(self, adres: str, baza: str) -> tuple[str, Path | None, str]:
        """-> (rodzaj, plik, kotwica). rodzaj: wewn | obcy | poza | inny | pusty."""
        adres = html_mod.unescape(adres.strip())
        if not adres:
            return "pusty", None, ""
        if re.match(r"^(mailto|tel|sms|data|javascript|blob):", adres, re.I):
            return "inny", None, ""
        pelny = urljoin(baza, adres)
        cz = urlsplit(pelny)
        if cz.scheme not in ("http", "https"):
            return "inny", None, ""
        if (cz.hostname or "") != self.host:
            return "obcy", None, cz.fragment
        sciezka = unquote(cz.path)
        if not sciezka.startswith(self.prefiks):
            return "poza", None, cz.fragment
        wzgl = sciezka[len(self.prefiks):]
        plik = self.katalog / wzgl
        if wzgl == "" or wzgl.endswith("/"):
            plik = plik / "index.html"
        elif plik.is_dir():
            plik = plik / "index.html"
        return "wewn", plik, cz.fragment

    # --- przebieg
    def wczytaj(self):
        for plik in sorted(self.katalog.rglob("*.html")):
            wzgl = self.nazwa(plik)
            if wzgl.startswith(POMIJANE):
                continue
            tekst = plik.read_text(encoding="utf-8", errors="replace")
            p = Strona()
            p.feed(tekst)
            p.close()
            self.strony[plik] = p
            self.html[plik] = tekst
            self.ids[plik] = set(p.ids)

    def ids_pliku(self, plik: Path) -> set[str] | None:
        if plik in self.ids:
            return self.ids[plik]
        if plik.suffix == ".svg" and plik.is_file():
            ids = set(re.findall(r'\bid=["\']?([^"\'\s>]+)', plik.read_text(encoding="utf-8", errors="replace")))
            self.ids[plik] = ids
            return ids
        return None

    def sprawdz_strone(self, plik: Path):
        g = self.nazwa(plik)
        p = self.strony[plik]
        html = self.html[plik]
        baza = self.adres_strony(plik)
        jest_404 = plik.name == "404.html" and plik.parent == self.katalog

        # niepodstawione znaczniki szablonu / wypelniacze z danych
        zostaly = sorted(set(re.findall(r"\{\{[^{}\n]{0,80}\}\}", tekst_widoczny(html))))
        if zostaly:
            self.blad(g, "niepodstawione znaczniki szablonu: " + ", ".join(zostaly[:5]))
        # Wypelniacz z danych importu - uwaga, nie blad: dane rejestrowe uzupelnia
        # wlascicielka, a do tego czasu publikacja innych zmian nie moze stac.
        if re.search(r"DO_UZUPE[LŁ]NIENIA", tekst_widoczny(html)):
            self.uwaga(g, "na stronie widać wypełniacz „DO_UZUPEŁNIENIA” (uzupełnij dane w panelu: "
                          "Dane gabinetu → dane rejestrowe)")
        if re.search(r"ZgotypeZ|%!\w\(|<no value>", html):
            self.blad(g, "w HTML został ślad błędu szablonu (ZgotypeZ / %!v( / <no value>)")

        if (p.html_lang or "").lower()[:2] != "pl":
            self.blad(g, f"<html lang> = {p.html_lang!r}, oczekiwano „pl”")

        # --- naglowki
        h1 = [t for t, _ in p.naglowki if t == "h1"]
        if len(h1) != 1:
            self.blad(g, f"liczba <h1> = {len(h1)}, powinna być dokładnie 1")
        for tag, tekst in p.naglowki:
            if not tekst:
                if tag == "h1":
                    self.blad(g, "pusty <h1> — strona nie ma widocznego tytułu")
                else:
                    self.uwaga(g, f"pusty <{tag}> — sekcja bez nagłówka")
        if p.naglowki and p.naglowki[0][0] != "h1":
            self.uwaga(g, f"pierwszy nagłówek to <{p.naglowki[0][0]}> „{p.naglowki[0][1][:50]}”, a nie <h1>")
        poziomy = [(int(t[1]), tekst) for t, tekst in p.naglowki]
        for (a, _), (b, tb) in zip(poziomy, poziomy[1:]):
            if b > a + 1:
                self.uwaga(g, f"przeskok w hierarchii nagłówków: h{a} → h{b} („{tb[:50]}”)")

        # --- id
        widziane: set[str] = set()
        for i in p.ids:
            if i in widziane:
                self.blad(g, f"powtórzone id=\"{i}\"")
            widziane.add(i)

        # --- obrazki
        for o in p.obrazki:
            a = o["attrs"]
            src = a.get("src", "?")
            if "alt" not in a:
                self.blad(g, f"<img> bez atrybutu alt: {src} (linia {o['linia']})")
            elif not a["alt"].strip() and not any(k.startswith("data-lb") or "podglad" in k
                                                  or "lupa" in k for k in a):
                if a.get("aria-hidden") != "true" and a.get("role") != "presentation":
                    self.uwaga(g, f"<img> z pustym alt (ozdobny?): {src}")
            w, h = a.get("width", ""), a.get("height", "")
            if not w or not h:
                self.blad(g, f"<img> bez width/height (skakanie układu): {src}")
                continue
            if not (w.isdigit() and h.isdigit()):
                self.blad(g, f"<img> z nieliczbowym width/height ({w}×{h}): {src}")
                continue
            rodzaj, cel, _ = self.rozwiaz(src, baza)
            if rodzaj == "wewn" and cel and cel.is_file():
                wym = wymiary_obrazu(cel)
                if wym and int(h) and wym[1]:
                    r_atr = int(w) / int(h)
                    r_pl = wym[0] / wym[1]
                    if abs(r_atr - r_pl) / r_pl > 0.02:
                        self.blad(g, f"<img> width/height {w}×{h} nie zgadza się z proporcjami "
                                     f"pliku {wym[0]}×{wym[1]}: {src}")

        # --- odnosniki
        for o in p.odnosniki:
            href = o["href"]
            a = o["attrs"]
            if href.strip() in ("", "#"):
                if href.strip() == "" :
                    self.blad(g, f"pusty href w <{o['tag']}> (linia {o['linia']})")
                continue
            rodzaj, cel, kotwica = self.rozwiaz(href, baza)
            if rodzaj == "poza":
                self.blad(g, f"odnośnik poza prefiksem {self.prefiks} (na GitHub Pages da 404): {href}")
            elif rodzaj == "wewn":
                self.sprawdz_cel(g, href, cel, kotwica, "odnośnik")
            elif rodzaj == "obcy":
                host = urlsplit(urljoin(baza, html_mod.unescape(href))).hostname or ""
                if host not in DOZWOLONE_SERWERY:
                    self.uwaga(g, f"odnośnik do serwera spoza listy DOZWOLONE_SERWERY: {href}")
                if a.get("target") == "_blank":
                    rel = set(a.get("rel", "").lower().split())
                    if "noopener" not in rel and "noreferrer" not in rel:
                        self.blad(g, f"odnośnik target=_blank bez rel=noopener: {href}")
            elif rodzaj == "inny" and href.lower().startswith("tel:"):
                numer = re.sub(r"[^\d+]", "", unquote(href[4:]))
                if len(numer.lstrip("+")) < 9:
                    self.blad(g, f"podejrzanie krótki numer w odnośniku tel: {href}")

        # --- zasoby (pobierane przy wejsciu)
        for adres, skad, rodzaj_z in p.zasoby:
            if not adres or adres.startswith(NIE_ADRESY):
                continue
            rodzaj, cel, kotwica = self.rozwiaz(adres, baza)
            if rodzaj == "obcy":
                if rodzaj_z == "link":
                    continue  # canonical, alternate - adres, nie pobranie
                if rodzaj_z == "meta":
                    self.blad(g, f"{skad} wskazuje obcy serwer: {adres}")
                    continue
                self.blad(g, f"zasób ładowany z obcego serwera ({skad}): {adres}")
            elif rodzaj == "poza":
                self.blad(g, f"zasób poza prefiksem {self.prefiks} ({skad}): {adres}")
            elif rodzaj == "wewn":
                if rodzaj_z == "link" and "canonical" in skad:
                    self.sprawdz_cel(g, adres, cel, kotwica, "rel=canonical")
                else:
                    self.sprawdz_cel(g, adres, cel, kotwica, skad)
        for k, v, tag in p.obce_atrybuty:
            self.blad(g, f"atrybut {k} na <{tag}> z obcym adresem (skrypt pobierze go bez zgody): {v}")
        for css in p.style_atr + p.style_bloki:
            for adres in adresy_css(css):
                rodzaj, cel, _ = self.rozwiaz(adres, baza)
                if rodzaj == "obcy":
                    self.blad(g, f"url() w stylu wskazuje obcy serwer: {adres}")
                elif rodzaj == "wewn" and cel and not cel.is_file():
                    self.blad(g, f"url() w stylu wskazuje nieistniejący plik: {adres}")

        # --- ramki i bramy zgody
        for r in p.ramki:
            self.blad(g, f"<iframe> osadzony w HTML (linia {r['linia']}, src={r['attrs'].get('src', '')}) — "
                         "ramka z obcego serwera ma powstawać dopiero po kliknięciu (brama zgody)")
        for b in p.bledy_bram:
            self.blad(g, b)
        for brama in p.bramy:
            if not brama["przycisk"]:
                self.blad(g, f"brama zgody (linia {brama['linia']}) bez przycisku "
                             f"{brama['regula']['przycisk']} — mapy nie da się wczytać")
        for m in re.finditer(r"(?is)<(iframe|script|link|img|source|embed|object|video|audio)\b[^>]*>", html):
            if "booksy" in m.group(0).lower():
                self.blad(g, f"serwis rezerwacji osadzony jako <{m.group(1).lower()}> — do Booksy wolno "
                             "prowadzić wyłącznie zwykłym odnośnikiem")

        # --- JSON-LD
        faq_json: list[tuple[str, str]] = []
        for blob in p.jsonld:
            try:
                dane = json.loads(blob)
            except json.JSONDecodeError as exc:
                self.blad(g, f"niepoprawny JSON-LD: {exc}")
                continue
            wezly = dane.get("@graph", [dane]) if isinstance(dane, dict) else dane
            for node in wezly if isinstance(wezly, list) else []:
                if not isinstance(node, dict):
                    continue
                typy = node.get("@type")
                typy = typy if isinstance(typy, list) else [typy]
                if "FAQPage" in typy:
                    for q in node.get("mainEntity", []) or []:
                        pyt = normalizuj(str(q.get("name", "")))
                        odp = normalizuj(str((q.get("acceptedAnswer") or {}).get("text", "")))
                        if not pyt:
                            self.blad(g, "FAQPage: pytanie bez treści (puste name)")
                        if not odp:
                            self.blad(g, f"FAQPage: pytanie bez odpowiedzi: {pyt[:60] or '(puste)'}")
                        faq_json.append((pyt, odp))
            for adres in re.findall(r'"(https?://[^"]+)"', blob):
                rodzaj, cel, kotwica = self.rozwiaz(adres, baza)
                if rodzaj == "wewn" and cel and not cel.exists():
                    self.blad(g, f"JSON-LD wskazuje nieistniejący adres: {adres}")
                if rodzaj == "poza":
                    self.blad(g, f"JSON-LD wskazuje adres poza prefiksem {self.prefiks}: {adres}")
        if not p.jsonld and not jest_404:
            self.blad(g, "brak danych strukturalnych JSON-LD")

        widoczny = tekst_widoczny(html)
        if faq_json:
            widoczny_l = luzno(widoczny)
            for pyt, odp in faq_json:
                if pyt and pyt not in p.podsumowania and luzno(pyt) not in widoczny_l:
                    self.blad(g, f"pytanie z FAQPage, którego nie ma na stronie: „{pyt[:70]}”")
                if odp and luzno(odp[:80]) not in widoczny_l:
                    self.uwaga(g, f"odpowiedź z FAQPage nie zgadza się z widoczną: „{odp[:60]}…”")
            nadmiar = [q for q in p.podsumowania if q and q not in {x for x, _ in faq_json}]
            if nadmiar:
                self.uwaga(g, f"pytania widoczne na stronie, ale nie w FAQPage: {nadmiar[:2]}")
        elif p.podsumowania and any(q.endswith("?") for q in p.podsumowania):
            self.uwaga(g, f"na stronie są pytania ({sum(q.endswith('?') for q in p.podsumowania)}) "
                          "w <details>, ale brak FAQPage w JSON-LD")

        # --- tytul, opis, kanoniczny
        tytul = normalizuj(p.tytul)
        if not tytul:
            self.blad(g, "pusty <title>")
        else:
            if len(tytul) > 68:
                self.uwaga(g, f"tytuł ma {len(tytul)} znaków — w wynikach Google zostanie ucięty: „{tytul}”")
            if "legnic" not in tytul.lower() and not jest_404:
                self.uwaga(g, f"tytuł nie zawiera nazwy miasta (Legnica / w Legnicy): „{tytul}”")
        opis = normalizuj(p.meta.get("description", ""))
        if not opis:
            self.blad(g, "brak meta description")
        elif not 110 <= len(opis) <= 170:
            self.uwaga(g, f"opis (meta description) ma {len(opis)} znaków (zalecane 110–170)")
        kanon = [h for r, h in p.link_rel if "canonical" in r.lower().split()]
        if not kanon and not jest_404:
            self.blad(g, "brak rel=canonical")
        elif kanon and not jest_404:
            oczekiwany = self.adres_strony(plik)
            if html_mod.unescape(kanon[0]) != oczekiwany:
                self.blad(g, f"rel=canonical = {kanon[0]}, oczekiwano {oczekiwany}")
        if jest_404 and "noindex" not in p.meta.get("robots", ""):
            self.uwaga(g, "strona 404 bez <meta name=robots content=noindex>")
        if "viewport" not in p.meta:
            self.blad(g, "brak <meta name=viewport>")

        # --- zakazane zwroty reklamowe (tekst widoczny + tytul/opis/alt)
        do_kontroli = " ".join([widoczny, tytul, opis, normalizuj(p.meta.get("og:description", "")),
                                " ".join(o["attrs"].get("alt", "") for o in p.obrazki)])
        for wzor in ZAKAZANE:
            for m in re.finditer(wzor, do_kontroli, re.I):
                przed = do_kontroli[max(0, m.start() - 60):m.start()]
                ctx = do_kontroli[max(0, m.start() - 45):m.end() + 45].strip()
                if zaprzeczone(przed):
                    self.uwaga(g, f"zwrot reklamowy użyty z zaprzeczeniem — sprawdź sens: …{ctx}…")
                else:
                    self.blad(g, f"zwrot niedozwolony w materiałach gabinetu lekarskiego (art. 14 "
                                 f"ustawy o działalności leczniczej): …{ctx}…")
        for wzor in PODEJRZANE:
            for m in re.finditer(wzor, do_kontroli, re.I):
                ctx = do_kontroli[max(0, m.start() - 45):m.end() + 45].strip()
                self.uwaga(g, f"do przeczytania przez człowieka — zwrot zależny od kontekstu: …{ctx}…")
        for zdanie in re.split(r"(?<=[.!?])\s+", widoczny):
            if not re.search(r"rezerwacj|booksy", zdanie, re.I):
                continue
            for wzor in PODEJRZANE_REZERWACJA:
                m = re.search(wzor, zdanie, re.I)
                if not m:
                    continue
                ctx = zdanie.strip()[:170]
                if zaprzeczone(zdanie[:m.start()]):
                    self.uwaga(g, f"treść o rezerwacji — zwrot z zaprzeczeniem, sprawdź sens: …{ctx}…")
                else:
                    self.uwaga(g, f"treść o rezerwacji — obietnica terminu, której gabinet nie może dać: …{ctx}…")

        # --- rezerwacja online
        rez = self.rez
        adres_danych = str(rez.get("url") or "").strip()
        host_rez = urlsplit(adres_danych).hostname if adres_danych else None
        odnosniki_rez = []
        for o in p.odnosniki:
            adres = html_mod.unescape(o["href"]).strip()
            h = urlsplit(adres).hostname or ""
            if not ("booksy" in adres.lower() or (host_rez and h == host_rez)):
                continue
            odnosniki_rez.append(adres)
            a = o["attrs"]
            if a.get("target", "").strip() != "_blank":
                self.blad(g, f"odnośnik rezerwacji bez target=\"_blank\": {adres}")
            rel = set(a.get("rel", "").lower().split())
            if "noopener" not in rel:
                self.blad(g, f"odnośnik rezerwacji bez rel=\"noopener\": {adres}")
            if "noreferrer" not in rel:
                self.blad(g, "odnośnik rezerwacji bez rel=\"noreferrer\" — serwis zewnętrzny pozna adres "
                             f"podstrony (informację o zdrowiu): {adres}")
        if adres_danych and odnosniki_rez:
            rozjechane = sorted({a for a in odnosniki_rez if a != adres_danych})
            if rozjechane:
                self.blad(g, f"adres rezerwacji w HTML inny niż w data/gabinet.yaml ({adres_danych}): "
                             + ", ".join(rozjechane[:3]))
        if odnosniki_rez and not any(o["href"].lower().startswith("tel:") for o in p.odnosniki):
            self.blad(g, "strona z przyciskiem rezerwacji nie ma odnośnika tel: — telefon ma zostać "
                         "kanałem pierwszym")
        if rez:
            if not rez.get("potwierdzona") and "ReserveAction" in html:
                self.blad(g, "ReserveAction w JSON-LD, a rezerwacja.potwierdzona = false")
            if not rez.get("wlaczona"):
                if odnosniki_rez:
                    self.blad(g, "rezerwacja.wlaczona = false, a na stronie są odnośniki rezerwacji")
                dostawca = str(rez.get("dostawca") or "").strip()
                if dostawca and re.search(re.escape(dostawca), widoczny, re.I):
                    self.blad(g, f"rezerwacja.wlaczona = false, a na stronie nadal jest „{dostawca}”")

        self.zestawienie.append(self.waga(plik, p, baza))

    def sprawdz_cel(self, g: str, adres: str, cel: Path | None, kotwica: str, skad: str):
        if cel is None:
            return
        if not cel.exists():
            self.blad(g, f"{skad} wskazuje nieistniejący plik: {adres}")
            return
        if kotwica:
            ids = self.ids_pliku(cel)
            if ids is not None and unquote(kotwica) not in ids:
                self.blad(g, f"{skad} wskazuje nieistniejącą kotwicę #{kotwica}: {adres}")

    # --- waga strony
    def waga(self, plik: Path, p: Strona, baza: str) -> dict:
        def rozmiar(adres: str) -> tuple[Path | None, int]:
            rodzaj, cel, _ = self.rozwiaz(adres, baza)
            if rodzaj == "wewn" and cel and cel.is_file():
                return cel, cel.stat().st_size
            return None, 0

        html_b = plik.stat().st_size
        html_gz = len(gzip.compress(plik.read_bytes(), 9))
        css = js = 0
        for adres, skad, rodzaj_z in p.zasoby:
            if rodzaj_z != "zasob":
                continue
            if "stylesheet" in skad:
                css += rozmiar(adres)[1]
            elif skad.startswith("<script"):
                js += rozmiar(adres)[1]
        zdj_min = zdj_max = zdj_start = 0
        leniwe = 0
        g = self.nazwa(plik)
        for o in p.obrazki:
            a = o["attrs"]
            kandydaci = []
            # przegladarka bierze pierwsze pasujace <source> (WebP), inaczej <img>
            zrodlo = next((s for t, s in o["zrodla"] if t in ("image/webp", "image/avif", "")), None)
            lista = kandydaci_srcset(zrodlo) if zrodlo else (
                kandydaci_srcset(a["srcset"]) if a.get("srcset") else [(a.get("src", ""), "")])
            for adres, _ in lista:
                cel, n = rozmiar(adres)
                if cel:
                    kandydaci.append((n, adres))
                    if n > PROG_ZDJECIE and adres not in self.ostrzezone_obrazy:
                        self.ostrzezone_obrazy.add(adres)
                        self.uwaga("(zdjęcia)", f"plik {kb(n)} > {kb(PROG_ZDJECIE)}: {adres}")
            if not kandydaci:
                continue
            mn, mx = min(kandydaci)[0], max(kandydaci)[0]
            zdj_min += mn
            zdj_max += mx
            if a.get("loading") == "lazy":
                leniwe += 1
            else:
                zdj_start += mx
        razem_max = html_b + css + js + zdj_max
        start = html_b + css + js + zdj_start
        if razem_max > PROG_STRONA:
            self.uwaga(g, f"waga strony do {kb(razem_max)} (próg {kb(PROG_STRONA)}) — zdjęcia {kb(zdj_max)}")
        if start > PROG_STRONA_START:
            self.uwaga(g, f"przy wejściu ładuje się {kb(start)} (próg {kb(PROG_STRONA_START)}): "
                          f"{len(p.obrazki) - leniwe} zdjęć bez loading=lazy")
        if html_b > PROG_HTML:
            self.uwaga(g, f"HTML ma {kb(html_b)} (próg {kb(PROG_HTML)})")
        return {"strona": g, "html": html_b, "html_gz": html_gz, "css": css, "js": js,
                "zdj": len(p.obrazki), "leniwe": leniwe, "zdj_min": zdj_min,
                "zdj_max": zdj_max, "start": start, "razem": razem_max}

    # --- pliki wspolne
    def sprawdz_wspolne(self):
        g = "(serwis)"
        for nazwa in ("index.html", "404.html", "sitemap.xml", "robots.txt"):
            if not (self.katalog / nazwa).is_file():
                self.blad(g, f"brak pliku {nazwa}")
        # sitemap
        mapa_plik = self.katalog / "sitemap.xml"
        if mapa_plik.is_file():
            mapa = mapa_plik.read_text(encoding="utf-8")
            w_mapie = set()
            for loc in re.findall(r"<loc>([^<]+)</loc>", mapa):
                rodzaj, cel, _ = self.rozwiaz(loc, self.baseurl)
                if rodzaj != "wewn" or cel is None or not cel.is_file():
                    self.blad(g, f"sitemap.xml: adres nie prowadzi do strony: {loc}")
                else:
                    w_mapie.add(cel)
            for plik in self.strony:
                if plik.name == "404.html" and plik.parent == self.katalog:
                    if plik in w_mapie:
                        self.blad(g, "sitemap.xml zawiera stronę 404")
                    continue
                if plik not in w_mapie and "noindex" not in self.strony[plik].meta.get("robots", ""):
                    self.uwaga(g, f"strony nie ma w sitemap.xml: {self.nazwa(plik)}")
        robots = self.katalog / "robots.txt"
        if robots.is_file() and "sitemap:" not in robots.read_text(encoding="utf-8").lower():
            self.uwaga(g, "robots.txt nie wskazuje sitemap.xml (wiersz „Sitemap: …”)")
        # cala strona ukryta przed wyszukiwarkami (Ustawienia -> "Ukryj strone przed
        # wyszukiwarkami") - przypomnienie w logu, zeby nie zostalo po uruchomieniu
        glowna = self.katalog / "index.html"
        if glowna in self.strony and "noindex" in self.strony[glowna].meta.get("robots", ""):
            self.uwaga(g, "strona jest ukryta przed wyszukiwarkami (noindex) — po uruchomieniu "
                          "wyłącz „Ukryj stronę przed wyszukiwarkami” w panelu: Ustawienia")
        # CSS i JS: obce adresy i nieistniejace pliki
        for plik in sorted(self.katalog.rglob("*.css")):
            if self.nazwa(plik).startswith(POMIJANE):
                continue
            css = plik.read_text(encoding="utf-8", errors="replace")
            baza = self.baseurl + self.nazwa(plik)
            for adres in adresy_css(css):
                if adres.startswith(NIE_ADRESY):
                    continue
                rodzaj, cel, _ = self.rozwiaz(adres, baza)
                if rodzaj == "obcy":
                    self.blad(self.nazwa(plik), f"CSS pobiera zasób z obcego serwera: {adres}")
                elif rodzaj == "wewn" and cel and not cel.is_file():
                    self.blad(self.nazwa(plik), f"CSS wskazuje nieistniejący plik: {adres}")
            if plik.stat().st_size > PROG_CSS:
                self.uwaga(self.nazwa(plik), f"arkusz ma {kb(plik.stat().st_size)} (próg {kb(PROG_CSS)})")
        for plik in sorted(self.katalog.rglob("*.js")):
            if self.nazwa(plik).startswith(POMIJANE):
                continue
            js = plik.read_text(encoding="utf-8", errors="replace")
            for adres in sorted(set(re.findall(r"""["'`]((?:https?:)?//[^"'`\s]+)""", js))):
                if adres.startswith(NIE_ADRESY):
                    continue
                self.blad(self.nazwa(plik), f"skrypt zawiera obcy adres (możliwe pobranie bez zgody): {adres}")
            if re.search(r"""createElement\(\s*["']iframe["']\s*\)""", js):
                if not re.search(r"getAttribute\(\s*[\"']data-[a-z-]+-src[\"']\s*\)", js):
                    self.blad(self.nazwa(plik), "skrypt tworzy <iframe>, ale nie z adresu z bramy zgody (data-…-src)")
            if plik.stat().st_size > PROG_JS:
                self.uwaga(self.nazwa(plik), f"skrypt ma {kb(plik.stat().st_size)} (próg {kb(PROG_JS)})")
        if self.rez.get("wlaczona") and not self.rez.get("potwierdzona"):
            self.uwaga(g, "rezerwacja.potwierdzona = false — sprawdź, czy data/gabinet.yaml → rezerwacja.url "
                          "wskazuje profil gabinetu, a nie wyszukiwarkę dostawcy; bez profilu ustaw "
                          "rezerwacja.wlaczona = false")

    # --- raport
    def raport(self) -> int:
        print(f"Kontrola strony: {self.katalog} (adres {self.baseurl}, stron: {len(self.strony)})\n")
        for plik in self.strony:
            g = self.nazwa(plik)
            b, u = self.bledy.get(g, []), self.uwagi.get(g, [])
            znak = "OK  " if not b else "BŁĄD"
            print(f"{znak} {g:<44}" + (f" {len(b)} błędów" if b else "") + (f" {len(u)} uwag" if u else ""))
            for x in b:
                print(f"       x {x}")
            for x in u:
                print(f"       - {x}")
        inne = [k for k in sorted(set(self.bledy) | set(self.uwagi))
                if k not in {self.nazwa(p) for p in self.strony}]
        for g in inne:
            b, u = self.bledy.get(g, []), self.uwagi.get(g, [])
            print(f"{'OK  ' if not b else 'BŁĄD'} {g}")
            for x in b:
                print(f"       x {x}")
            for x in u:
                print(f"       - {x}")

        print("\nWaga stron (bajty z dysku, bez kompresji; zdjęcia: najmniejszy–największy wariant;"
              " „start” = bez loading=lazy):")
        print(f"  {'strona':<40}{'HTML':>8}{'gzip':>8}{'CSS':>8}{'JS':>7}{'zdj.':>6}{'lazy':>6}"
              f"{'zdj. min':>10}{'zdj. max':>10}{'start':>9}{'razem':>9}")
        for z in sorted(self.zestawienie, key=lambda z: -z["razem"]):
            print(f"  {z['strona']:<40}{kb(z['html']):>8}{kb(z['html_gz']):>8}{kb(z['css']):>8}"
                  f"{kb(z['js']):>7}{z['zdj']:>6}{z['leniwe']:>6}{kb(z['zdj_min']):>10}"
                  f"{kb(z['zdj_max']):>10}{kb(z['start']):>9}{kb(z['razem']):>9}")

        bledy = sum(len(v) for v in self.bledy.values())
        uwagi = sum(len(v) for v in self.uwagi.values())
        print(f"\nRAZEM: {bledy} błędów, {uwagi} uwag")
        if bledy:
            print("Błędy (x) blokują publikację. Uwagi (-) są do przeczytania przez człowieka.")
        return 1 if bledy else 0


def adres_bazowy(katalog: Path) -> str:
    glowna = katalog / "index.html"
    if glowna.is_file():
        m = re.search(r"""<link\b[^>]*rel=["']?canonical["']?[^>]*href=["']?([^"'\s>]+)""",
                      glowna.read_text(encoding="utf-8", errors="replace"))
        if m:
            return html_mod.unescape(m.group(1))
    konf = REPO / "hugo.yaml"
    if konf.is_file():
        m = re.search(r"^baseURL:\s*['\"]?([^'\"\s]+)", konf.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    sys.exit("BŁĄD: nie da się ustalić adresu strony — podaj --baseurl")


def main() -> int:
    ap = argparse.ArgumentParser(description="Kontrola jakości i zgodności zbudowanej strony (public/).")
    ap.add_argument("katalog", nargs="?", default=str(REPO / "public"))
    ap.add_argument("--baseurl", help="adres strony (domyślnie z rel=canonical strony głównej)")
    arg = ap.parse_args()
    katalog = Path(arg.katalog).resolve()
    if not (katalog / "index.html").is_file():
        print(f"BŁĄD: w {katalog} nie ma zbudowanej strony (index.html) — najpierw: hugo --gc --minify",
              file=sys.stderr)
        return 2
    k = Kontrola(katalog, arg.baseurl or adres_bazowy(katalog))
    k.wczytaj()
    for plik in list(k.strony):
        k.sprawdz_strone(plik)
    k.sprawdz_wspolne()
    return k.raport()


if __name__ == "__main__":
    raise SystemExit(main())
