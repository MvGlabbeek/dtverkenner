"""Bouwt de MkDocs-bronbestanden uit de publieksversie in bron/.

Gebruik: python scripts/build_site.py
- Neemt het nieuwste rapport  bron/*publiek*.docx  en register  bron/*publiek*.xlsx
  (bestanden zonder 'publiek' in de naam worden geweigerd).
- Zet het rapport met pandoc om naar Markdown, één pagina per hoofdstuk (kop 1).
- Zet het tabblad Portfolio van het register om naar een doorzoekbare tabel.
- Kopieert beide bestanden naar docs/downloads/ en schrijft mkdocs.yml (basis + navigatie).
"""
import re, shutil, subprocess, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRON, DOCS = ROOT / "bron", ROOT / "docs"


def versie(p: Path) -> tuple:
    m = re.search(r"_v(\d+)", p.name)
    return (int(m.group(1)) if m else 0, p.stat().st_mtime)


def nieuwste(patroon: str) -> Path:
    alle = list(BRON.glob(patroon))
    if not alle:
        sys.exit(f"Geen bestand gevonden voor {patroon} in bron/")
    for p in BRON.glob(patroon.replace("*publiek*", "*")):
        if "publiek" not in p.name.lower():
            print(f"Let op: {p.name} heeft geen 'publiek' in de naam en wordt genegeerd.")
    return max(alle, key=versie)


def slug(t: str) -> str:
    t = re.sub(r"[^\w\s-]", "", t.lower(), flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", t).strip("-")[:60] or "hoofdstuk"


def normaliseer(docx: Path) -> Path:
    """Voegt een ontbrekende stijl 'Normal' toe; zonder die stijl herkent pandoc
    de kopstijlen van met docx-js gemaakte documenten niet."""
    import zipfile, tempfile
    with zipfile.ZipFile(docx) as z:
        styles = z.read("word/styles.xml").decode("utf-8")
        if 'w:styleId="Normal"' in styles:
            return docx
        styles = styles.replace("</w:docDefaults>", "</w:docDefaults>"
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:qFormat/></w:style>', 1)
        uit = Path(tempfile.mkdtemp()) / docx.name
        with zipfile.ZipFile(uit, "w", zipfile.ZIP_DEFLATED) as w:
            for item in z.infolist():
                data = styles.encode("utf-8") if item.filename == "word/styles.xml" else z.read(item)
                w.writestr(item, data)
    return uit


def rapport(docx: Path) -> list[tuple[str, str]]:
    bron = normaliseer(docx)
    md = subprocess.run(
        ["pandoc", str(bron), "-t", "gfm-raw_html+pipe_tables", "--wrap=none",
         f"--extract-media={DOCS}"],
        check=True, capture_output=True, text=True).stdout
    md = md.replace(str(DOCS) + "/", "")  # paden relatief maken
    delen = re.split(r"^# (.+)$", md, flags=re.M)
    voorwerk, pages = delen[0].replace("[TABLE]", "").strip() + "\n", []
    for i in range(1, len(delen), 2):
        titel, body = delen[i].strip(), delen[i + 1]
        naam = f"{len(pages)+1:02d}-{slug(titel)}.md"
        tekst = f"# {titel}\n{body}"
        (DOCS / naam).write_text(tekst, encoding="utf-8")
        pages.append((titel, naam))
    (DOCS / "index.md").write_text(
        "# Digital twins voor het energiesysteem en de gebouwde omgeving\n\n"
        f"Publieksversie van de inventarisatie (bron: `{docx.name}`).\n\n"
        "[Download het rapport (Word)](downloads/" + docx.name + "){ .md-button }\n"
        "[Bekijk het register](register.md){ .md-button }\n\n"
        "Reacties zijn welkom onderaan elke pagina.\n\n" + voorwerk,
        encoding="utf-8")
    return pages


def register(xlsx: Path) -> None:
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    ws = wb["Portfolio"]
    rows = list(ws.iter_rows(values_only=True))
    kop = [str(c) for c in rows[0] if c is not None]
    toon = [k for k in ("ID", "Initiatief", "Focus", "Gebied", "Land", "Rol in ecosysteem",
                        "Primaire functie", "Schaalniveau", "Twinniveau", "Volwassenheid",
                        "Kadercodes", "Bron") if k in kop]
    idx = [kop.index(k) for k in toon]
    def cel(v, k):
        s = "" if v is None else str(v)
        if k == "Bron" and s.startswith("http"):
            return f'<a href="{html.escape(s.split()[0])}">bron</a>'
        return html.escape(s)
    regels = ["<table id=\"register\" class=\"display\"><thead><tr>"
              + "".join(f"<th>{html.escape(k)}</th>" for k in toon) + "</tr></thead><tbody>"]
    for r in rows[1:]:
        if not r or r[0] is None:
            continue
        regels.append("<tr>" + "".join(f"<td>{cel(r[i], k)}</td>" for i, k in zip(idx, toon)) + "</tr>")
    regels.append("</tbody></table>")
    (DOCS / "register.md").write_text(
        "---\nhide:\n  - toc\n---\n# Register\n\n"
        f"Alle initiatieven uit `{xlsx.name}`. Zoek en filter in de tabel; "
        f"[download het volledige register (Excel)](downloads/{xlsx.name}).\n\n"
        + "\n".join(regels) + "\n", encoding="utf-8")


def main():
    for p in DOCS.glob("*.md"):
        p.unlink()
    for sub in ("media", "downloads"):
        shutil.rmtree(DOCS / sub, ignore_errors=True)
    (DOCS / "downloads").mkdir(parents=True, exist_ok=True)
    docx, xlsx = nieuwste("*publiek*.docx"), nieuwste("*publiek*.xlsx")
    for f in (docx, xlsx):
        shutil.copy(f, DOCS / "downloads" / f.name)
    pages = rapport(docx)
    register(xlsx)
    nav = ["  - Start: index.md", "  - Register: register.md"] + \
          [f"  - '{t.replace(chr(39), chr(39)*2)}': {n}" for t, n in pages]
    basis = (ROOT / "mkdocs.base.yml").read_text(encoding="utf-8")
    (ROOT / "mkdocs.yml").write_text(basis.rstrip() + "\n\nnav:\n" + "\n".join(nav) + "\n", encoding="utf-8")
    print(f"Gebouwd uit {docx.name} en {xlsx.name}: {len(pages)} hoofdstukken.")


if __name__ == "__main__":
    main()
