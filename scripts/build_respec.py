"""Bouwt de ReSpec-publicatie uit de nieuwste bron/*publiek*.md.

Gebruik: python scripts/build_respec.py <uitvoermap>   (standaard _site/respec)
- Tekst vóór het eerste hoofdstuk wordt 'Status van dit document', het hoofdstuk Samenvatting de samenvatting.
- Elk hoofdstuk (##) wordt een eigen sectie; 'Bijlage X: ...' wordt een ReSpec-bijlage (eigen nummering).
- Handmatige nummers in koppen van bijlagen (A.1, A.1.2) worden weggehaald; ReSpec nummert zelf.
"""
import re, shutil, sys, datetime, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRON = ROOT / "bron"


def versie(p):
    m = re.search(r"_v(\d+)", p.name)
    return (int(m.group(1)) if m else 0, p.stat().st_mtime)


def main():
    uit = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site" / "respec"
    alle = list(BRON.glob("*publiek*.md"))
    if not alle:
        sys.exit("Geen bron/*publiek*.md gevonden.")
    md = max(alle, key=versie)
    shutil.rmtree(uit, ignore_errors=True)
    (uit / "parts").mkdir(parents=True)
    (uit / "downloads").mkdir()
    shutil.copy(md, uit / "downloads" / md.name)
    extra = ""
    for pat, label in (("*publiek*.docx", "Rapport (Word)"), ("*publiek*.xlsx", "Register (Excel)")):
        kand = list(BRON.glob(pat))
        if kand:
            f = max(kand, key=versie)
            shutil.copy(f, uit / "downloads" / f.name)
            extra += f',\n        {{ value: "{label}", href: "downloads/{f.name}" }}'

    tekst = md.read_text(encoding="utf-8")
    delen = re.split(r"^## (.+)$", tekst, flags=re.M)
    (uit / "parts" / "sotd.md").write_text(delen[0].strip() + "\n", encoding="utf-8")
    secties, n = [], 0
    for i in range(1, len(delen), 2):
        titel, body = delen[i].strip(), delen[i + 1]
        if titel.lower() == "samenvatting":
            (uit / "parts" / "abstract.md").write_text(body.strip() + "\n", encoding="utf-8")
            continue
        n += 1
        naam = f"{n:02d}.md"
        m = re.match(r"Bijlage [A-Z]+:\s*(.+)", titel)
        if m:
            titel = m.group(1)[0].upper() + m.group(1)[1:]
            body = re.sub(r"^(#{3,}) [A-Z](?:\.\d+)+\.? ", r"\1 ", body, flags=re.M)
            klasse = ' class="appendix"'
        else:
            klasse = ""
        (uit / "parts" / naam).write_text(f"## {titel}\n{body}", encoding="utf-8")
        secties.append(f'  <section{klasse} data-include="parts/{naam}" data-include-format="markdown"></section>')

    m = re.search(r"_v(\d+)", md.name)
    sjabloon = (ROOT / "respec" / "index.template.html").read_text(encoding="utf-8")
    pagina = (sjabloon.replace("{{versie}}", m.group(1) if m else "?")
              .replace("{{datum}}", datetime.date.today().isoformat())
              .replace("{{md}}", md.name)
              .replace("{{extra_downloads}}", extra)
              .replace("{{secties}}", "\n".join(secties)))
    (uit / "index.html").write_text(pagina, encoding="utf-8")
    print(f"ReSpec gebouwd uit {md.name}: {n} secties.")


if __name__ == "__main__":
    main()
