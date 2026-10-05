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
  5. partial bloku - razem z partialami pomocniczymi, ktorym przekazuje caly
     blok ($b := .blok, np. hero-akcje.html) - czyta tylko pola ze swojego
     typu ($b.<pole>) i co najmniej jedno;
  6. nazwy katalogow stron w content/strony/ (= adresy) to tylko a-z, 0-9
     i "-" (Hugo nie zamienia "ł" w adresie; CMS zapisuje slugi poprawnie,
     ale katalog mozna tez utworzyc recznie);
  7. data/cennik.yaml: identyfikatory kategorii i pozycji sa niepuste
     i niepowtarzalne, a kazda pozycja wskazuje istniejaca kategorie
     (bloki na stronach wskazuja pozycje po identyfikatorze);
  8. telefony ("699 904 989") i ceny ("800 zł", "250–400 zł") wpisane recznie
     w content/ i data/ustawienia.yaml wystepuja w data/gabinet.yaml (telefony)
     i data/cennik.yaml (cena_od / cena_do);
  9. klucze front matter w content/**/*.md (strony i ich bloki) i klucze
     w data/*.yaml sa polami odpowiedniej kolekcji w config.yml (rekurencyjnie;
     dla stron dodatkowo klucze Hugo z KLUCZE_HUGO, dla blokow "type");
 10. kotwice zarezerwowane przez szablon - ta sama lista w docs/KONTRAKT-BLOKOW.md,
     we wzorze i komunikacie pola "kotwica" w config.yml i w sekcje.html szablonow;
 11. wersja kontraktu ta sama w hugo.yaml (params.kontraktBlokow), w komentarzu
     config.yml i w docs/KONTRAKT-BLOKOW.md;
 12. strony z data/ustawienia.yaml -> strona_404.linki istnieja.

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
HUGO_YAML = REPO / "hugo.yaml"
POLA_WSPOLNE = {"wariant", "waska", "polacz", "kotwica"}  # pola kazdego typu bloku
# klucze front matter stron spoza pol panelu: weight (kolejnosc - reorder
# w panelu), aliases (panel dopisuje stary adres po zmianie sluga), build
# i cascade (content/strony/_index.md, sekcja-kontener tylko dla Hugo)
KLUCZE_HUGO = {"weight", "aliases", "build", "cascade"}
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
    """5. partial bloku - razem z partialami pomocniczymi, ktorym przekazuje
    caly blok (np. hero-akcje.html) - czyta tylko pola swojego typu i czyta
    co najmniej jedno (inaczej kontrola nic by nie widziala)."""
    bledy = []
    for szablon in szablony:
        pomocnicze, bledy_pomocniczych = partiale_pomocnicze(szablon)
        bledy += bledy_pomocniczych
        for k in katalogi_partiali(szablon):
            if not k.is_dir():
                continue
            for p in sorted(k.glob("*.html")):
                typ = p.stem
                if typ not in typy_cms:
                    print(f"uwaga: {sciezka_wzgledna(p)} - typu '{typ}' nie ma w config.yml")
                    continue
                tekst = p.read_text(encoding="utf-8")
                zrodla = [(p, pola_b(tekst))] + [
                    (h, pola) for h, (nazwa, pola) in pomocnicze.items() if wywoluje_z_blokiem(tekst, nazwa)
                ]
                for plik, uzyte in zrodla:
                    # "type" to klucz typu (typeKey), nie pole
                    for pole in sorted(uzyte - set(typy_cms[typ]) - {"type"}):
                        bledy.append(f"{sciezka_wzgledna(plik)}: pole '$b.{pole}' nie należy do typu '{typ}'")
                if set(typy_cms[typ]) - POLA_WSPOLNE and not set().union(*(u for _, u in zrodla)) - {"type"}:
                    bledy.append(
                        f"{sciezka_wzgledna(p)}: nie znaleziono odczytu żadnego pola typu '{typ}' ($b.<pole>) - "
                        "partial czyta blok inaczej niż przez $b := .blok, więc kontrola pól go nie obejmuje"
                    )
    return bledy


def pola_b(tekst: str) -> set[str]:
    return set(re.findall(r"\$b\.([a-zA-Z0-9_]+)", tekst))


def wywoluje_z_blokiem(tekst: str, nazwa: str) -> bool:
    """Czy partial bloku wywoluje partial pomocniczy `nazwa` z (dict "blok" $b ...)
    wpisanym w samym wywolaniu (dict moze byc rozbity na wiersze, ale nie
    przygotowany wczesniej w zmiennej)."""
    return bool(re.search(rf'partial(?:Cached)?\s+"{re.escape(nazwa)}"\s*\(dict\b[^}}]*?"blok"\s+\$b\b', tekst))


def partiale_pomocnicze(szablon: Path) -> tuple[dict[Path, set[str]], list[str]]:
    """Partiale spoza blocks/ (takze w podkatalogach), ktore dostaja caly blok
    ($b := .blok): sciezka -> (nazwa w wywolaniu partial, czytane pola). Taki partial musi wywolywac co najmniej jeden partial bloku -
    inaczej nie wiadomo, pola ktorego typu sprawdzic."""
    pomocnicze: dict[Path, tuple[str, set[str]]] = {}
    bledy = []
    bloki = [p for k in katalogi_partiali(szablon) if k.is_dir() for p in k.glob("*.html")]
    for katalog in (szablon / "layouts/partials", szablon / "layouts/_partials"):
        if not katalog.is_dir():
            continue
        for p in sorted(katalog.rglob("*.html")):
            if any(k in p.parents for k in katalogi_partiali(szablon)):
                continue
            tekst = p.read_text(encoding="utf-8")
            if not re.search(r"\$b\s*:=\s*\.blok\b", tekst):
                continue
            nazwa = p.relative_to(katalog).as_posix()
            pomocnicze[p] = (nazwa, pola_b(tekst))
            if not any(wywoluje_z_blokiem(b.read_text(encoding="utf-8"), nazwa) for b in bloki):
                bledy.append(
                    f"{sciezka_wzgledna(p)}: partial czyta blok ($b := .blok), ale żaden partial "
                    f'blocks/<typ>.html nie wywołuje go z (dict "blok" $b ...) wpisanym w samo wywołanie partial'
                )
    return pomocnicze, bledy


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


def pola_wg_nazwy(pola) -> dict[str, dict]:
    return {f["name"]: f for f in pola or [] if isinstance(f, dict) and "name" in f}


def dolacz(sciezka: str, dalej: str) -> str:
    return f"{sciezka}.{dalej}" if sciezka else dalej


def klucze_poza_polami(wartosc, pola: dict[str, dict], plik: str, sciezka: str = "", dodatkowe=frozenset()) -> list[str]:
    """Klucze slownika `wartosc` musza byc polami panelu `pola` (rekurencyjnie
    w obiektach i listach) - klucz spoza panelu panel po cichu gubi przy
    zapisie, a szablon moze go czytac albo nie."""
    if not isinstance(wartosc, dict):
        return []
    bledy = []
    for klucz, w in wartosc.items():
        if klucz in dodatkowe:
            continue
        if klucz not in pola:
            gdzie = f" w {sciezka}" if sciezka else ""
            bledy.append(f"{plik}: klucz '{klucz}'{gdzie} nie jest polem panelu (static/admin/config.yml)")
            continue
        bledy += klucze_wartosci(w, pola[klucz], plik, dolacz(sciezka, str(klucz)))
    return bledy


def klucze_wartosci(wartosc, pole: dict, plik: str, sciezka: str) -> list[str]:
    widget = pole.get("widget")
    if widget == "object":
        return klucze_poza_polami(wartosc, pola_wg_nazwy(pole.get("fields")), plik, sciezka)
    if widget != "list" or not isinstance(wartosc, list):
        return []
    bledy = []
    for i, el in enumerate(wartosc):
        miejsce = f"{sciezka}[{i + 1}]"
        if "types" in pole:
            klucz_typu = pole.get("typeKey", "type")
            typy = {t["name"]: t for t in pole["types"]}
            typ = el.get(klucz_typu) if isinstance(el, dict) else None
            if typ not in typy:
                bledy.append(f"{plik}: {miejsce}: nieznany typ {typ!r} (typy w panelu: {', '.join(typy)})")
                continue
            bledy += klucze_poza_polami(
                el, pola_wg_nazwy(typy[typ].get("fields")), plik, f"{miejsce} ({typ})", {klucz_typu}
            )
        elif "fields" in pole:
            bledy += klucze_poza_polami(el, pola_wg_nazwy(pole["fields"]), plik, miejsce)
        elif "field" in pole:
            bledy += klucze_wartosci(el, pole["field"], plik, miejsce)
    return bledy


def front_matter(plik: Path) -> dict | str:
    """Front matter YAML pliku .md albo opis bledu (str)."""
    m = re.match(r"---[ \t]*\r?\n(?:(.*?)\r?\n)?---[ \t]*(\r?\n|$)", plik.read_text(encoding="utf-8"), flags=re.S)
    if not m:
        return "brak front matter (YAML między wierszami ---; TOML +++ nie jest obsługiwany)"
    try:
        dane = yaml.safe_load(m[1] or "")
    except yaml.YAMLError as exc:
        return f"niepoprawny YAML w front matter: {exc}"
    # pusty blok (---/---, same komentarze) Hugo przyjmuje jako brak kluczy
    if dane is None:
        return {}
    return dane if isinstance(dane, dict) else "front matter nie jest mapą klucz: wartość"


def sprawdz_klucze_tresci(config: dict) -> list[str]:
    """9. klucze w content/**/*.md (front matter) i data/*.yaml = pola panelu."""
    bledy = []
    pliki: dict[Path, dict[str, dict]] = {}
    foldery: list[tuple[Path, dict[str, dict]]] = []
    for kol in lista_slownikow(config.get("collections")):
        for f in lista_slownikow(kol.get("files")):
            pliki[(REPO / f["file"]).resolve()] = pola_wg_nazwy(f.get("fields"))
        if "folder" in kol:
            foldery.append(((REPO / kol["folder"]).resolve(), pola_wg_nazwy(kol.get("fields"))))
    for plik in sorted((REPO / "content").rglob("*.md")):
        sciezka = sciezka_wzgledna(plik)
        pola = pliki.get(plik.resolve())
        if pola is None:
            pola = next((p for folder, p in foldery if folder in plik.resolve().parents), None)
        if pola is None:
            bledy.append(f"{sciezka}: plik nie należy do żadnej kolekcji panelu (static/admin/config.yml)")
            continue
        dane = front_matter(plik)
        if isinstance(dane, str):
            bledy.append(f"{sciezka}: {dane}")
            continue
        bledy += klucze_poza_polami(dane, pola, sciezka, dodatkowe=KLUCZE_HUGO)
    for plik in sorted((REPO / "data").glob("*.yaml")):
        sciezka = sciezka_wzgledna(plik)
        if plik.resolve() not in pliki:
            bledy.append(f"{sciezka}: plik nie jest edytowany w panelu (brak w collections.files w config.yml)")
            continue
        try:
            dane = wczytaj_yaml(plik)
        except BladKonfiguracji as exc:
            bledy.append(str(exc))
            continue
        bledy += klucze_poza_polami(dane, pliki[plik.resolve()], sciezka)
    return bledy


def prefiksy_z_wzoru(wzor: str) -> set[str]:
    """'^(grupa|podmenu)-' -> {'grupa-', 'podmenu-'}; 'f[0-9]+-' -> {'f<liczba>-'}
    (zapis z docs/KONTRAKT-BLOKOW.md)."""
    wzor = wzor.lstrip("^").replace("[0-9]+", "<liczba>")
    m = re.fullmatch(r"\(([^()]+)\)(.*)", wzor)
    if m:
        return {f"{w}{m[2]}" for w in m[1].split("|")}
    return {wzor}


def sprawdz_kotwice_zarezerwowane(config: dict, szablony: list[Path]) -> list[str]:
    """10. kotwice zarezerwowane przez szablon: ta sama lista w docs, we wzorze
    pola "kotwica" w panelu (wraz z komunikatem) i w sekcje.html kazdego szablonu."""
    bledy = []
    akapit = re.search(r"\*\*Kotwice zarezerwowane\*\*[^:]*:(.*?`)\.\s", KONTRAKT.read_text(encoding="utf-8"), flags=re.S)
    if not akapit:
        return ["docs/KONTRAKT-BLOKOW.md: brak akapitu „**Kotwice zarezerwowane**” z listą kotwic"]
    lista = re.findall(r"`([^`]+)`", akapit[1])
    nazwy = {k for k in lista if not k.endswith("-")}
    prefiksy = {k for k in lista if k.endswith("-")}

    def porownaj(skad: str, n: set[str], p: set[str]) -> None:
        if n != nazwy:
            bledy.append(f"{skad}: kotwice zarezerwowane {sorted(n)} różnią się od docs/KONTRAKT-BLOKOW.md {sorted(nazwy)}")
        if p != prefiksy:
            bledy.append(f"{skad}: początki kotwic zarezerwowanych {sorted(p)} różnią się od docs/KONTRAKT-BLOKOW.md {sorted(prefiksy)}")

    def pola_kotwica(obj):
        """pole wspolne "kotwica" w typach list "sekcje" (nie kotwica elementu spisu)"""
        if isinstance(obj, dict):
            if obj.get("name") == "sekcje" and "types" in obj:
                for t in lista_slownikow(obj["types"]):
                    yield from (f for f in lista_slownikow(t.get("fields")) if f.get("name") == "kotwica")
            for v in obj.values():
                yield from pola_kotwica(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from pola_kotwica(v)

    wzory = {(tuple(f["pattern"]) if isinstance(f.get("pattern"), list) else None) for f in pola_kotwica(config)}
    if not wzory or None in wzory or any(len(w) != 2 for w in wzory):
        bledy.append("config.yml: pole 'kotwica' musi mieć pattern: [wzór, komunikat]")
        wzory = {w for w in wzory if w and len(w) == 2}
    for wzor, komunikat in sorted(wzory):
        n = set().union(*(m.split("|") for m in re.findall(r"\(\?!\(([a-z|-]+)\)\$\)", wzor)))
        p = set().union(*(prefiksy_z_wzoru(m) for m in re.findall(r"\(\?!(\([a-z|]+\)-|[a-z]+\[0-9\]\+-)\)", wzor)))
        porownaj("config.yml (pattern pola 'kotwica')", n, p)
        for k in sorted(nazwy | prefiksy):
            if k not in komunikat:
                bledy.append(f"config.yml: komunikat wzoru pola 'kotwica' nie wymienia kotwicy zarezerwowanej '{k}'")
    for szablon in szablony:
        plik = szablon / "layouts/partials/sekcje.html"
        if not plik.is_file():
            continue
        tekst = plik.read_text(encoding="utf-8")
        lista_szablonu = re.search(r"\$zarezerwowane\s*:=\s*slice((?:\s+\"[^\"]+\")+)", tekst)
        wzor_szablonu = re.search(r"findRE\s+`([^`]+)`", tekst)
        if not lista_szablonu or not wzor_szablonu:
            bledy.append(f"{sciezka_wzgledna(plik)}: nie znaleziono listy $zarezerwowane albo wzoru findRE kotwic")
            continue
        n = set(re.findall(r"\"([^\"]+)\"", lista_szablonu[1]))
        p = set().union(*(prefiksy_z_wzoru(m) for m in wzor_szablonu[1].split("|^")))
        porownaj(sciezka_wzgledna(plik), n, p)
    return bledy


def sprawdz_wersje_kontraktu(hugo: dict) -> list[str]:
    """11. wersja kontraktu ta sama w hugo.yaml, config.yml i docs."""
    w_docs = re.search(r"Wersja kontraktu: \*\*(\d+)\*\*", KONTRAKT.read_text(encoding="utf-8"))
    w_config = re.search(r"kontrakt blokow w wersji (\d+)", CONFIG.read_text(encoding="utf-8"))
    w_hugo = (hugo.get("params") or {}).get("kontraktBlokow")
    wersje = {
        "docs/KONTRAKT-BLOKOW.md („Wersja kontraktu: **N**”)": w_docs and w_docs[1],
        "static/admin/config.yml (komentarz „kontrakt blokow w wersji N”)": w_config and w_config[1],
        "hugo.yaml (params.kontraktBlokow)": None if w_hugo is None else str(w_hugo),
    }
    bledy = [f"{skad}: brak numeru wersji kontraktu" for skad, w in wersje.items() if not w]
    if not bledy and len(set(wersje.values())) > 1:
        bledy.append("różne wersje kontraktu: " + ", ".join(f"{skad} = {w}" for skad, w in wersje.items()))
    return bledy


def sprawdz_linki_404(ustawienia: dict) -> list[str]:
    """12. strony z data/ustawienia.yaml -> strona_404.linki istnieja (szablon
    pomija brakujaca strone bez bledu, zeby 404 nie przerwala budowania)."""
    aliasy = set()
    for plik in (REPO / "content/strony").glob("*/index.md"):
        dane = front_matter(plik)
        if isinstance(dane, dict):
            aliasy |= {str(a).strip("/") for a in dane.get("aliases") or []}
    bledy = []
    for i, el in enumerate(lista_slownikow((ustawienia.get("strona_404") or {}).get("linki")), 1):
        slug = el.get("strona")
        if slug and not (REPO / f"content/strony/{slug}/index.md").is_file() and str(slug) not in aliasy:
            bledy.append(
                f"data/ustawienia.yaml: strona_404.linki nr {i} wskazuje stronę {slug!r}, której nie ma "
                f"(brak content/strony/{slug}/index.md) - popraw w panelu: Ustawienia, strona 404"
            )
    return bledy


def main() -> int:
    try:
        config = wczytaj_yaml(CONFIG)
        cennik = wczytaj_yaml(CENNIK)
        gabinet = wczytaj_yaml(GABINET)
        ustawienia = wczytaj_yaml(USTAWIENIA)
        hugo = wczytaj_yaml(HUGO_YAML)
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
    bledy += sprawdz_klucze_tresci(config)
    bledy += sprawdz_kotwice_zarezerwowane(config, szablony)
    bledy += sprawdz_wersje_kontraktu(hugo)
    bledy += sprawdz_linki_404(ustawienia)

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
