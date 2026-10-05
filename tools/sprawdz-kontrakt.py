#!/usr/bin/env python3
"""Kontrola kontraktu blokow (docs/KONTRAKT-BLOKOW.md) - uruchamiana w CI przed budowaniem.

Sprawdza (w tej kolejnosci):
  1. katalog layouts/ w korzeniu repozytorium jest pusty (poza .gitkeep) -
     inaczej nadpisalby szablony z themes/;
  2. kazdy typ bloku z pola "sekcje" w static/admin/config.yml ma partial
     blocks/<typ>.html w KAZDYM szablonie w themes/*;
  3. wszystkie pola "sekcje" w config.yml (Strony, Strona glowna) maja te same typy;
  4. pola kazdego typu w config.yml = pola z tabeli w docs/KONTRAKT-BLOKOW.md
     (+ pola wspolne), a typy w kontrakcie = typy w config.yml;
  5. partial bloku czyta tylko pola ze swojego typu ($b.<pole>);
  6. nazwy katalogow stron w content/strony/ (= adresy) to tylko a-z, 0-9
     i "-" (Hugo nie zamienia "ł" w adresie; CMS zapisuje slugi poprawnie,
     ale katalog mozna tez utworzyc recznie);
  7. data/cennik.yaml: identyfikatory kategorii i pozycji sa niepuste
     i niepowtarzalne, a kazda pozycja wskazuje istniejaca kategorie
     (bloki na stronach wskazuja pozycje po identyfikatorze);
  8. telefony ("699 904 989") i ceny ("800 zł", "250–400 zł") wpisane recznie
     w content/ i data/ustawienia.yaml wystepuja w data/gabinet.yaml (telefony)
     i data/cennik.yaml (cena_od / cena_do).

Wymaga PyYAML (w CI: pip install PyYAML). Kod wyjscia: 0 = bez bledow,
1 = co najmniej jeden blad kontraktu, 2 = blad konfiguracji (brak PyYAML,
brak albo niepoprawny plik YAML, brak sekcji "## Bloki" w kontrakcie).
Uzycie:  python tools/sprawdz-kontrakt.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# polskie litery w konsoli Windows (bez PYTHONUTF8=1)
for strumien in (sys.stdout, sys.stderr):
    if hasattr(strumien, "reconfigure"):
        strumien.reconfigure(encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:  # pragma: no cover
    print("BŁĄD: brak modułu PyYAML (pip install PyYAML)", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "static/admin/config.yml"
CENNIK = REPO / "data/cennik.yaml"
GABINET = REPO / "data/gabinet.yaml"
USTAWIENIA = REPO / "data/ustawienia.yaml"
KONTRAKT = REPO / "docs/KONTRAKT-BLOKOW.md"
POLA_WSPOLNE = {"wariant", "waska", "polacz", "kotwica"}  # pola kazdego typu bloku
WZOR_SLUGA = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
WZOR_TELEFONU = re.compile(r"(?<![\d+])(?:\+48[  ]?)?\d{3}[  -]\d{3}[  -]\d{3}(?!\d)")
WZOR_CENY = re.compile(r"(?<![\d.,])(\d[\d  ]*\d|\d)(?:[  ]?[–-][  ]?(\d[\d  ]*\d|\d))?[  ]?zł")


class BladKonfiguracji(Exception):
    """Nie da sie przeprowadzic kontroli (brak pliku, zly YAML) - kod wyjscia 2."""


def sciezka_wzgledna(plik: Path) -> str:
    return plik.relative_to(REPO).as_posix()


def wczytaj_yaml(plik: Path) -> dict:
    if not plik.is_file():
        raise BladKonfiguracji(f"brak pliku {sciezka_wzgledna(plik)}")
    try:
        dane = yaml.safe_load(plik.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BladKonfiguracji(f"niepoprawny YAML w {sciezka_wzgledna(plik)}: {exc}") from exc
    if dane is None:
        return {}
    if not isinstance(dane, dict):
        raise BladKonfiguracji(f"{sciezka_wzgledna(plik)}: oczekiwano mapy klucz: wartość na najwyższym poziomie")
    return dane


def lista_slownikow(wartosc) -> list[dict]:
    """Elementy listy z YAML, ktore sa slownikami (reszte pomija - zle wpisy
    wychodza w kontrolach jako brakujace pola)."""
    return [e for e in wartosc or [] if isinstance(e, dict)] if isinstance(wartosc, list) else []


def pola_sekcji(obj: object, sciezka: str = "config.yml") -> list[tuple[str, dict[str, list[str]]]]:
    """Zwraca [(sciezka, {typ: [pola]})] dla kazdego pola list o nazwie "sekcje"."""
    wynik = []
    if isinstance(obj, dict):
        if obj.get("name") == "sekcje" and obj.get("widget") == "list" and "types" in obj:
            typy = {}
            for t in obj["types"]:
                typy[t["name"]] = [f["name"] for f in t.get("fields", [])]
            wynik.append((sciezka, typy))
        for k, v in obj.items():
            wynik.extend(pola_sekcji(v, f"{sciezka}/{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            nazwa = v.get("name", i) if isinstance(v, dict) else i
            wynik.extend(pola_sekcji(v, f"{sciezka}/{nazwa}"))
    return wynik


def typy_z_kontraktu() -> dict[str, set[str]]:
    if not KONTRAKT.is_file():
        raise BladKonfiguracji(f"brak pliku {sciezka_wzgledna(KONTRAKT)}")
    tekst = KONTRAKT.read_text(encoding="utf-8")
    czesci = re.split(r"^## Bloki[ \t]*$", tekst, maxsplit=1, flags=re.M)
    if len(czesci) < 2:
        raise BladKonfiguracji(
            f"{sciezka_wzgledna(KONTRAKT)}: brak nagłówka „## Bloki” (pod nim tabele pól typów bloków)"
        )
    tekst = czesci[1].split("\n## ", 1)[0]
    typy: dict[str, set[str]] = {}
    for kawalek in re.split(r"^### ", tekst, flags=re.M)[1:]:
        m = re.match(r"`([a-z0-9_]+)`", kawalek)
        if not m:
            continue
        typy[m[1]] = set(re.findall(r"^\| `([a-z0-9_]+)` \|", kawalek, flags=re.M))
    return typy


def katalogi_partiali(szablon: Path) -> list[Path]:
    return [szablon / "layouts/partials/blocks", szablon / "layouts/_partials/blocks"]


# --- kontrole (kazda zwraca liste bledow) -----------------------------------


def sprawdz_layouts() -> list[str]:
    """1. layouts/ w korzeniu repozytorium jest pusty."""
    layouts = REPO / "layouts"
    if not layouts.exists():
        return []
    return [
        f"layouts/ musi być pusty (nadpisałby szablony z themes/): {sciezka_wzgledna(p)}"
        for p in sorted(layouts.rglob("*"))
        if p.is_file() and p.name != ".gitkeep"
    ]


def sprawdz_partiale(typy_cms: dict[str, list[str]], szablony: list[Path]) -> list[str]:
    """2. kazdy typ bloku ma partial w kazdym szablonie."""
    bledy = [] if szablony else ["brak szablonów w themes/"]
    for szablon in szablony:
        for typ in typy_cms:
            if not any((k / f"{typ}.html").is_file() for k in katalogi_partiali(szablon)):
                bledy.append(f"{sciezka_wzgledna(szablon)}: brak partiala blocks/{typ}.html dla typu bloku '{typ}'")
    return bledy


def sprawdz_sekcje_zgodne(wystapienia: list[tuple[str, dict[str, list[str]]]]) -> list[str]:
    """3. wszystkie pola "sekcje" maja te same typy i pola. Strona glowna uzywa
    dzis aliasu *sekcje, wiec po wczytaniu YAML to ten sam obiekt i kontrola
    przechodzi zawsze - zostaje na wypadek zastapienia aliasu kopia."""
    wzor_sciezka, wzor_typy = wystapienia[0]
    return [
        f"config.yml: pole 'sekcje' w {sciezka} ma inne typy/pola niż w {wzor_sciezka}"
        for sciezka, typy in wystapienia[1:]
        if typy != wzor_typy
    ]


def sprawdz_kontrakt(typy_cms: dict[str, list[str]], kontrakt: dict[str, set[str]]) -> list[str]:
    """4. typy i pola w config.yml = typy i pola w docs/KONTRAKT-BLOKOW.md."""
    bledy = [f"KONTRAKT-BLOKOW.md: typ '{typ}' nie występuje w config.yml" for typ in sorted(set(kontrakt) - set(typy_cms))]
    bledy += [f"config.yml: typ '{typ}' nie jest opisany w docs/KONTRAKT-BLOKOW.md" for typ in sorted(set(typy_cms) - set(kontrakt))]
    for typ in sorted(set(typy_cms) & set(kontrakt)):
        w_cms = set(typy_cms[typ])
        w_kontrakcie = kontrakt[typ] | POLA_WSPOLNE
        if w_cms != w_kontrakcie:
            bledy.append(f"typ '{typ}': pola w config.yml {sorted(w_cms)} różnią się od kontraktu {sorted(w_kontrakcie)}")
    return bledy


def sprawdz_pola_partiali(typy_cms: dict[str, list[str]], szablony: list[Path]) -> list[str]:
    """5. partial bloku czyta tylko pola swojego typu."""
    bledy = []
    for szablon in szablony:
        for k in katalogi_partiali(szablon):
            if not k.is_dir():
                continue
            for p in sorted(k.glob("*.html")):
                typ = p.stem
                if typ not in typy_cms:
                    print(f"uwaga: {sciezka_wzgledna(p)} - typu '{typ}' nie ma w config.yml")
                    continue
                uzyte = set(re.findall(r"\$b\.([a-zA-Z0-9_]+)", p.read_text(encoding="utf-8")))
                # "type" to klucz typu (typeKey), nie pole
                for pole in sorted(uzyte - set(typy_cms[typ]) - {"type"}):
                    bledy.append(f"{sciezka_wzgledna(p)}: pole '$b.{pole}' nie należy do typu '{typ}'")
    return bledy


def sprawdz_slugi() -> list[str]:
    """6. nazwy katalogow stron (= adresy) bez ogonkow i wielkich liter."""
    strony = REPO / "content/strony"
    if not strony.is_dir():
        return []
    return [
        f"content/strony/{k.name}/: nazwa katalogu jest adresem strony - dozwolone tylko "
        "małe litery bez ogonków, cyfry i myślniki (np. leczenie-kanalowe)"
        for k in sorted(p for p in strony.iterdir() if p.is_dir())
        if not WZOR_SLUGA.fullmatch(k.name)
    ]


def sprawdz_cennik(cennik: dict) -> list[str]:
    """7. identyfikatory w data/cennik.yaml."""
    bledy = []
    kategorie = [k.get("id") for k in lista_slownikow(cennik.get("kategorie"))]
    pozycje = lista_slownikow(cennik.get("pozycje"))
    for nazwa, ids in (("kategorii", kategorie), ("pozycji", [p.get("id") for p in pozycje])):
        for i, ident in enumerate(ids, 1):
            if not ident or not WZOR_SLUGA.fullmatch(str(ident)):
                bledy.append(f"data/cennik.yaml: identyfikator {nazwa} nr {i} ({ident!r}) jest pusty albo niepoprawny")
        for ident in sorted({str(i) for i in ids if i and ids.count(i) > 1}):
            bledy.append(f"data/cennik.yaml: identyfikator {nazwa} {ident!r} występuje więcej niż raz")
    for p in pozycje:
        if p.get("kategoria") not in kategorie:
            bledy.append(
                f"data/cennik.yaml: pozycja {p.get('nazwa')!r} wskazuje kategorię "
                f"{p.get('kategoria')!r}, której nie ma na liście kategorii"
            )
    return bledy


def sprawdz_fakty_w_tresci(gabinet: dict, cennik: dict) -> list[str]:
    """8. Telefony i ceny wpisane recznie w tresc (opisy SEO, akapity) musza
    istniec w data/gabinet.yaml i data/cennik.yaml - inaczej po zmianie numeru
    albo ceny w panelu tekst stron po cichu by sie zestarzal."""
    bledy = []
    numery = {re.sub(r"\D", "", str(t.get("numer", ""))) for t in lista_slownikow(gabinet.get("telefony"))}
    ceny = set()
    for p in lista_slownikow(cennik.get("pozycje")):
        for k in ("cena_od", "cena_do"):
            if p.get(k) in (None, ""):
                continue
            try:
                ceny.add(int(p[k]))
            except (TypeError, ValueError):
                bledy.append(f"data/cennik.yaml: pozycja {p.get('nazwa')!r}: {k} = {p[k]!r} nie jest liczbą całkowitą")
    pliki = sorted((REPO / "content").rglob("*.md")) + [USTAWIENIA]
    for plik in pliki:
        sciezka = sciezka_wzgledna(plik)
        for nr, wiersz in enumerate(plik.read_text(encoding="utf-8").splitlines(), 1):
            for tel in WZOR_TELEFONU.findall(wiersz) + re.findall(r"tel:([+\d]+)", wiersz):
                if re.sub(r"\D", "", tel)[-9:] not in numery:
                    bledy.append(f"{sciezka}:{nr}: telefon {tel!r} nie występuje w data/gabinet.yaml (telefony)")
            for m in WZOR_CENY.finditer(wiersz):
                for kwota in filter(None, (m.group(1), m.group(2))):
                    if int(re.sub(r"\D", "", kwota)) not in ceny:
                        bledy.append(f"{sciezka}:{nr}: cena {m.group(0)!r} nie występuje w data/cennik.yaml")
    return bledy


def main() -> int:
    try:
        config = wczytaj_yaml(CONFIG)
        cennik = wczytaj_yaml(CENNIK)
        gabinet = wczytaj_yaml(GABINET)
        if not USTAWIENIA.is_file():
            raise BladKonfiguracji(f"brak pliku {sciezka_wzgledna(USTAWIENIA)}")
        kontrakt = typy_z_kontraktu()
    except BladKonfiguracji as exc:
        print(f"BŁĄD: {exc}", file=sys.stderr)
        return 2

    wystapienia = pola_sekcji(config)
    typy_cms = wystapienia[0][1] if wystapienia else {}
    szablony = sorted(p for p in (REPO / "themes").iterdir() if p.is_dir()) if (REPO / "themes").is_dir() else []

    bledy = sprawdz_layouts()
    if wystapienia:
        bledy += sprawdz_partiale(typy_cms, szablony)
        bledy += sprawdz_sekcje_zgodne(wystapienia)
        bledy += sprawdz_kontrakt(typy_cms, kontrakt)
        bledy += sprawdz_pola_partiali(typy_cms, szablony)
    else:
        bledy.append("static/admin/config.yml: nie znaleziono pola listy 'sekcje' z 'types'")
    bledy += sprawdz_slugi()
    bledy += sprawdz_cennik(cennik)
    bledy += sprawdz_fakty_w_tresci(gabinet, cennik)

    for b in bledy:
        print(f"BŁĄD: {b}", file=sys.stderr)
    if bledy:
        return 1
    print(
        f"Kontrakt bloków OK: {len(typy_cms)} typów ({', '.join(typy_cms)}), "
        f"szablony: {', '.join(s.name for s in szablony)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
