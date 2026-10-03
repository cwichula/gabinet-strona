#!/usr/bin/env python3
"""Jednorazowy import danych gabinetu i cennika z repozytorium "gamstom".

Czyta (tylko do odczytu):
  <gamstom>/tresci/gabinet.json        dane gabinetu (plaskie klucze)
  <gamstom>/tresci/cennik.json         "<id>__nazwa" i "<id>__cena" ("650", "250-400")
  <gamstom>/v1/_src/strony/cennik.html kolejnosc pozycji i podzial na grupy (tabela v1)
  <gamstom>/v1/_src/tresci/cennik.json nazwy grup i nota pod cennikiem

Zapisuje:
  data/gabinet.yaml
  data/cennik.yaml

Uzycie:  python tools/importuj-z-gamstom.py [sciezka/do/gamstom]
         (domyslnie ../gamstom obok tego repozytorium)

Po imporcie zrodlem prawdy sa pliki w data/ (edytowane w Sveltia CMS).
Ponowne uruchomienie NADPISUJE zmiany wprowadzone w CMS.

Tylko biblioteka standardowa. YAML piszemy recznie: kazdy napis w cudzyslowie,
liczby i wartosci logiczne bez - tak, zeby nic nie zostalo zle odczytane
(np. "9:00" jako liczba szescdziesiatkowa w YAML 1.1).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DNI = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]


class BladImportu(Exception):
    pass


# ------------------------------------------------------------------ YAML


def yaml_str(s: str) -> str:
    """Napis w podwojnym cudzyslowie, z ucieczka znakow specjalnych."""
    s = str(s)
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{s}"'


def yaml_skalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if v is None:
        return "null"
    return yaml_str(v)


def yaml_emit(obj, wciecie: int = 0) -> list[str]:
    """Minimalny emiter YAML dla slownikow, list i skalarow."""
    pad = " " * wciecie
    linie: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                linie.append(f"{pad}{k}:")
                linie.extend(yaml_emit(v, wciecie + 2))
            elif isinstance(v, dict):
                linie.append(f"{pad}{k}: {{}}")
            elif isinstance(v, list):
                linie.append(f"{pad}{k}: []")
            else:
                linie.append(f"{pad}{k}: {yaml_skalar(v)}")
    elif isinstance(obj, list):
        for el in obj:
            if isinstance(el, dict) and el:
                pod = yaml_emit(el, wciecie + 2)
                # pierwszy klucz w tej samej linii co "- "
                pod[0] = f"{pad}- {pod[0].lstrip()}"
                linie.extend(pod)
            elif isinstance(el, (dict, list)):
                raise BladImportu("pusty slownik/lista jako element listy - nieobslugiwane")
            else:
                linie.append(f"{pad}- {yaml_skalar(el)}")
    else:
        linie.append(f"{pad}{yaml_skalar(obj)}")
    return linie


def zapisz_yaml(sciezka: Path, naglowek: str, dane: dict) -> None:
    tekst = naglowek + "\n".join(yaml_emit(dane)) + "\n"
    sciezka.write_text(tekst, encoding="utf-8", newline="\n")
    print(f"zapisano {sciezka.relative_to(REPO)}")


# --------------------------------------------------------------- cennik

RE_KLUCZ = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*)__(nazwa|cena)")


def parsuj_cene(tekst: str) -> tuple[int, int]:
    """"650" -> (650, 650); "250-400" (tez z polpauza) -> (250, 400)."""
    s = re.sub(r"\s", "", str(tekst))
    czesci = re.split(r"[-–—]", s)
    if not 1 <= len(czesci) <= 2 or not all(re.fullmatch(r"\d+", c) for c in czesci):
        raise BladImportu(f"to nie cena: {tekst!r}")
    od, do = int(czesci[0]), int(czesci[-1])
    if od > do:
        raise BladImportu(f"cena 'od' wieksza niz 'do': {tekst!r}")
    return od, do


def wczytaj_pozycje(plik: Path) -> dict[str, dict]:
    surowe = json.loads(plik.read_text(encoding="utf-8"))
    pozycje: dict[str, dict] = {}
    for klucz, wartosc in surowe.items():
        m = RE_KLUCZ.fullmatch(klucz)
        if not m:
            raise BladImportu(f"{plik}: nieznany klucz {klucz!r}")
        pozycje.setdefault(m[1], {})[m[2]] = wartosc
    for pid, pola in pozycje.items():
        if not str(pola.get("nazwa", "")).strip() or not str(pola.get("cena", "")).strip():
            raise BladImportu(f"{plik}: pozycja {pid!r} bez nazwy albo ceny")
    return pozycje


def grupy_v1(gamstom: Path) -> list[tuple[str, str, list[str]]]:
    """[(id_grupy, nazwa_grupy, [id_pozycji, ...]), ...] wg tabeli w v1/cennik."""
    html = (gamstom / "v1/_src/strony/cennik.html").read_text(encoding="utf-8")
    teksty = json.loads((gamstom / "v1/_src/tresci/cennik.json").read_text(encoding="utf-8"))
    # tylko tabela (JSON-LD na poczatku pliku tez zawiera znaczniki cen)
    tabela = html[html.index('<table class="price-table"'):]
    tabela = tabela[: tabela.index("</table>")]
    grupy: list[tuple[str, str, list[str]]] = []
    for m in re.finditer(r'id="grupa-([a-z]+)">\{\{T:(th_\d+)\}\}|\{\{CENA:([a-z0-9-]+)\}\}', tabela):
        if m[1]:
            grupy.append((m[1], teksty[m[2]], []))
        else:
            if not grupy:
                raise BladImportu("cennik v1: pozycja przed pierwsza grupa")
            grupy[-1][2].append(m[3])
    return grupy


def zbuduj_cennik(gamstom: Path) -> dict:
    pozycje = wczytaj_pozycje(gamstom / "tresci/cennik.json")
    grupy = grupy_v1(gamstom)
    przypisane = [pid for _, _, ids in grupy for pid in ids]
    if sorted(przypisane) != sorted(pozycje) or len(set(przypisane)) != len(przypisane):
        brak = set(pozycje) - set(przypisane)
        nadmiar = set(przypisane) - set(pozycje)
        raise BladImportu(f"grupy v1 nie pokrywaja cennika 1:1 (brak: {brak}, nadmiar: {nadmiar})")
    teksty = json.loads((gamstom / "v1/_src/tresci/cennik.json").read_text(encoding="utf-8"))
    # Ksztalt kontraktu blokow 2: kategorie {id, nazwa} + jedna lista pozycji
    # z polem "kategoria" (relacja Sveltii obsluguje tylko jeden poziom listy).
    kategorie = []
    lista = []
    for gid, nazwa, ids in grupy:
        kategorie.append({"id": gid, "nazwa": nazwa})
        for pid in ids:
            od, do = parsuj_cene(pozycje[pid]["cena"])
            poz = {"id": pid, "kategoria": gid, "nazwa": pozycje[pid]["nazwa"], "cena_od": od}
            if do != od:
                poz["cena_do"] = do
            lista.append(poz)
    return {
        "informacja": teksty["p_005"],
        "kategorie": kategorie,
        "pozycje": lista,
    }


# --------------------------------------------------------------- gabinet


def tel_link(numer: str) -> str:
    """Ta sama regula co w szablonach (partial tel.html): same cyfry, bez
    wiodacego "00" (albo "0" przy 10 cyfrach), +48 dla 9 cyfr."""
    cyfry = re.sub(r"\D", "", numer)
    if cyfry.startswith("00"):
        cyfry = cyfry[2:]
    elif cyfry.startswith("0") and len(cyfry) == 10:
        cyfry = cyfry[1:]
    if len(cyfry) == 9:
        return "+48" + cyfry
    return "+" + cyfry


def zbuduj_gabinet(gamstom: Path) -> dict:
    g = json.loads((gamstom / "tresci/gabinet.json").read_text(encoding="utf-8"))

    telefony = []
    for etykieta, wysw, link in [
        ("Rejestracja (telefon stacjonarny)", "tel_glowny_wyswietlany", "tel_glowny_link"),
        ("Telefon komórkowy", "tel_kom_wyswietlany", "tel_kom_link"),
    ]:
        if tel_link(g[wysw]) != g[link]:
            raise BladImportu(f"{wysw}: numer {g[wysw]!r} nie daje odnosnika {g[link]!r}")
        telefony.append({"etykieta": etykieta, "numer": g[wysw]})

    godziny = []
    for n, dzien in enumerate(DNI, start=1):
        if g.get(f"godziny_{n}_nazwa") != dzien:
            raise BladImportu(f"godziny_{n}_nazwa = {g.get(f'godziny_{n}_nazwa')!r}, oczekiwano {dzien!r}")
        od = g.get(f"godziny_{n}_od", "")
        do = g.get(f"godziny_{n}_do", "")
        if bool(od) != bool(do):
            raise BladImportu(f"godziny_{n}: podano tylko jedna granice")
        godziny.append({"dzien": dzien, "od": od, "do": do})

    klucze = [k for k in g if re.fullmatch(r"platnosci_\d+", k)]
    platnosci = [g[k] for k in sorted(klucze, key=lambda k: int(k.rsplit("_", 1)[1]))]

    return {
        "nazwa": g["nazwa"],
        "nazwa_krotka": g["nazwa_krotka"],
        "lekarz": g["lekarz"],
        "rok_zalozenia": int(g["rok_zalozenia"]),
        "adres": {
            "ulica": g["adres_ulica"],
            "kod": g["adres_kod"],
            "miasto": g["adres_miasto"],
            "dojazd": g["dojazd"],
        },
        "telefony": telefony,
        "email": g["email"],
        "godziny": godziny,
        "rezerwacja": {
            "wlaczona": bool(g["rezerwacja_wlaczona"]),
            "url": g["rezerwacja_url"],
            "etykieta": g["rezerwacja_etykieta"],
            "dostawca": g.get("rezerwacja_dostawca", ""),
            "potwierdzona": bool(g.get("rezerwacja_potwierdzona", False)),
            "nota": g.get("rezerwacja_nota", ""),
        },
        "rejestrowe": {
            "nip": g["rejestrowe_nip"],
            "regon": g["rejestrowe_regon"],
            "pwz": g["rejestrowe_pwz"],
            "rpwdl": g["rejestrowe_rpwdl"],
        },
        "platnosci": platnosci,
    }


NAGLOWEK = (
    "# Plik edytowany w panelu /admin/ (Sveltia CMS). Pierwotnie wygenerowany przez\n"
    "# tools/importuj-z-gamstom.py z repozytorium gamstom - komentarze w tym pliku\n"
    "# znikna przy pierwszym zapisie z CMS.\n"
)


def main() -> int:
    gamstom = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO.parent / "gamstom"
    gamstom = gamstom.resolve()
    if not (gamstom / "tresci/gabinet.json").is_file():
        print(f"BLAD: nie znaleziono {gamstom / 'tresci/gabinet.json'}", file=sys.stderr)
        return 2
    try:
        cennik = zbuduj_cennik(gamstom)
        gabinet = zbuduj_gabinet(gamstom)
    except (BladImportu, KeyError, ValueError) as e:
        print(f"BLAD importu: {e}", file=sys.stderr)
        return 1
    zapisz_yaml(REPO / "data/cennik.yaml", NAGLOWEK, cennik)
    zapisz_yaml(REPO / "data/gabinet.yaml", NAGLOWEK, gabinet)
    liczba = len(cennik["pozycje"])
    print(f"cennik: {len(cennik['kategorie'])} kategorii, {liczba} pozycji")
    return 0


if __name__ == "__main__":
    sys.exit(main())
