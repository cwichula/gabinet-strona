#!/usr/bin/env python3
"""Kontrola kontraktu blokow (docs/KONTRAKT-BLOKOW.md) - uruchamiana w CI przed budowaniem.

Sprawdza:
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
     ale katalog mozna tez utworzyc recznie).

Wymaga PyYAML (w CI: pip install PyYAML). Kod wyjscia 1 = blad.
Uzycie:  python tools/sprawdz-kontrakt.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("BŁĄD: brak modułu PyYAML (pip install PyYAML)", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "static/admin/config.yml"
KONTRAKT = REPO / "docs/KONTRAKT-BLOKOW.md"
POLA_WSPOLNE = {"wariant"}
WZOR_SLUGA = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")  # "type" to klucz typu (typeKey), nie pole

bledy: list[str] = []


def blad(tekst: str) -> None:
    bledy.append(tekst)


def pola_sekcji(obj, sciezka="config.yml"):
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
    tekst = KONTRAKT.read_text(encoding="utf-8")
    tekst = tekst.split("## Bloki", 1)[1].split("\n## ", 1)[0]
    typy: dict[str, set[str]] = {}
    for kawalek in re.split(r"^### ", tekst, flags=re.M)[1:]:
        m = re.match(r"`([a-z0-9_]+)`", kawalek)
        if not m:
            continue
        typy[m[1]] = set(re.findall(r"^\| `([a-z0-9_]+)` \|", kawalek, flags=re.M))
    return typy


def main() -> int:
    # 1. layouts/ w korzeniu
    layouts = REPO / "layouts"
    if layouts.exists():
        pliki = [p for p in layouts.rglob("*") if p.is_file() and p.name != ".gitkeep"]
        for p in pliki:
            blad(f"layouts/ musi być pusty (nadpisałby szablony z themes/): {p.relative_to(REPO).as_posix()}")

    # 6. nazwy katalogow stron
    strony = REPO / "content/strony"
    if strony.is_dir():
        for k in sorted(p for p in strony.iterdir() if p.is_dir()):
            if not WZOR_SLUGA.fullmatch(k.name):
                blad(
                    f"content/strony/{k.name}/: nazwa katalogu jest adresem strony - dozwolone tylko "
                    "małe litery bez ogonków, cyfry i myślniki (np. leczenie-kanalowe)"
                )

    # 2-3. typy w config.yml
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    wystapienia = pola_sekcji(config)
    if not wystapienia:
        blad("static/admin/config.yml: nie znaleziono pola listy 'sekcje' z 'types'")
        return koniec()
    wzor_sciezka, typy_cms = wystapienia[0]
    for sciezka, typy in wystapienia[1:]:
        if typy != typy_cms:
            blad(f"config.yml: pole 'sekcje' w {sciezka} ma inne typy/pola niż w {wzor_sciezka}")

    szablony = sorted(p for p in (REPO / "themes").iterdir() if p.is_dir())
    if not szablony:
        blad("brak szablonów w themes/")
    for szablon in szablony:
        katalogi = [szablon / "layouts/partials/blocks", szablon / "layouts/_partials/blocks"]
        for typ in typy_cms:
            if not any((k / f"{typ}.html").is_file() for k in katalogi):
                blad(f"{szablon.relative_to(REPO).as_posix()}: brak partiala blocks/{typ}.html dla typu bloku '{typ}'")
        for k in katalogi:
            if k.is_dir():
                for p in sorted(k.glob("*.html")):
                    typ = p.stem
                    if typ not in typy_cms:
                        print(f"uwaga: {p.relative_to(REPO).as_posix()} - typu '{typ}' nie ma w config.yml")
                        continue
                    # 5. partial czyta tylko pola swojego typu
                    uzyte = set(re.findall(r"\$b\.([a-zA-Z0-9_]+)", p.read_text(encoding="utf-8")))
                    nieznane = uzyte - set(typy_cms[typ]) - {"type"}
                    for pole in sorted(nieznane):
                        blad(f"{p.relative_to(REPO).as_posix()}: pole '$b.{pole}' nie należy do typu '{typ}'")

    # 4. kontrakt <-> config.yml
    kontrakt = typy_z_kontraktu()
    for typ in sorted(set(kontrakt) - set(typy_cms)):
        blad(f"KONTRAKT-BLOKOW.md: typ '{typ}' nie występuje w config.yml")
    for typ in sorted(set(typy_cms) - set(kontrakt)):
        blad(f"config.yml: typ '{typ}' nie jest opisany w docs/KONTRAKT-BLOKOW.md")
    for typ in sorted(set(typy_cms) & set(kontrakt)):
        w_cms = set(typy_cms[typ])
        w_kontrakcie = kontrakt[typ] | POLA_WSPOLNE
        if w_cms != w_kontrakcie:
            blad(
                f"typ '{typ}': pola w config.yml {sorted(w_cms)} różnią się od kontraktu {sorted(w_kontrakcie)}"
            )

    if not bledy:
        print(
            f"Kontrakt bloków OK: {len(typy_cms)} typów ({', '.join(typy_cms)}), "
            f"szablony: {', '.join(s.name for s in szablony)}"
        )
    return koniec()


def koniec() -> int:
    for b in bledy:
        print(f"BŁĄD: {b}", file=sys.stderr)
    return 1 if bledy else 0


if __name__ == "__main__":
    sys.exit(main())
