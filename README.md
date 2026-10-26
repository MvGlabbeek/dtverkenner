# Digital twins voor het energiesysteem en de gebouwde omgeving

Publieksversie van de inventarisatie *Verkenner Digital Twins* (Energy Innovation NL), opgesteld door Martijn van Glabbeek (Bizz4Mation).

Startpagina: **https://mvglabbeek.github.io/dtverkenner/**, met twee weergaven van dezelfde inhoud:

- **MkDocs** (per hoofdstuk, zoekfunctie, doorzoekbaar register): https://mvglabbeek.github.io/dtverkenner/mkdocs/
- **ReSpec** (één doorlopend document met genummerde secties): https://mvglabbeek.github.io/dtverkenner/respec/

## Nieuwe versie publiceren

1. Controleer de publieksversie. Alle bestandsnamen moeten `publiek` en het versienummer bevatten:
   - `Inventarisatie_digital_twins_NL_EU_2026-10_v14_publiek.docx` en `Register_..._v14_publiek.xlsx` voor de MkDocs-weergave;
   - `Inventarisatie_digital_twins_NL_EU_2026-10_v14_publiek.md` (rapport in Markdown) voor de ReSpec-weergave, met de figuren los in [`bron/figuren/`](bron/figuren/) (zie hieronder).
   Ontbreekt een van beide sets, dan wordt alleen de andere weergave gebouwd.
2. Upload de bestanden in de map [`bron/`](bron/) (op github.com: *Add file → Upload files*). Oude versies mogen blijven staan.
3. Commit naar `main`. De workflow *Publiceer site* bouwt en publiceert de site binnen een paar minuten (zie tabblad *Actions*).
4. Optioneel: maak een tag of release (bijv. `v14`) om de versie vast te leggen.

De site gebruikt altijd het bestand met het hoogste versienummer (`_v14`) in de naam. Bestanden zonder `publiek` in de naam worden genegeerd.

## Figuren (ReSpec-weergave)

Het Markdown-rapport bevat geen ingebedde afbeeldingen, maar verwijst naar figuren met een vast nummer in `bron/figuren/`: `0001.png` tot en met `9999.png`. Het nummer zegt niets over de plaats in het rapport; een nieuwe figuur krijgt het eerstvolgende vrije nummer en een nummer wordt niet hergebruikt.

| Bestand | Figuur in het rapport (versie 13) |
|---|---|
| `0001.png` | Figuur 1: Datamodel van het register |
| `0002.png` | Figuur 2: Initiatieven naar rol en focus |
| `0003.png` | Figuur 3: Primaire functie x schaalniveau (Energie) |
| `0004.png` | Figuur 4: Functies over alle initiatieven |
| `0005.png` | Figuur A.1: Lagenmodel referentiearchitectuur |
| `0006.png` | Figuur A.2: Drie scopes |

Een figuur vervangen: upload een nieuw bestand met precies dezelfde naam in `bron/figuren/` en commit. PNG is de standaard; een `.svg`, `.jpg` of `.webp` met hetzelfde nummer (zonder `.png`-variant) wordt automatisch gebruikt. Breedte en hoogte volgen uit het bestand zelf (maximaal de tekstbreedte), dus een andere verhouding is geen probleem. Een ontbrekende figuur geeft een waarschuwing in de workflow. Een nieuwe figuur: kies het eerstvolgende vrije nummer, zet in het md `<img src="figuren/0007.png" alt="..." style="max-width:100%" />` en upload het bestand.

## Nummering van initiatieven

Initiatieven hebben een vast volgnummer DT-001, DT-002, ... (kolom ID in het register). Het soort initiatief staat apart in de kolommen Categoriecode (K, R, T, B, C, E, L, I) en Categorie; de legenda staat in het rapport (paragraaf Opbouw van het register) en op het tabblad Toelichting van het register.

## Wat de workflow doet

- `scripts/build_site.py` zet het Word-document met pandoc om naar Markdown, één pagina per hoofdstuk (kop 1), inclusief figuren.
- Het tabblad *Portfolio* van het register wordt een doorzoekbare tabel; beide bestanden staan als download op de site.
- MkDocs Material bouwt de site in `/mkdocs/`.
- `scripts/build_respec.py` kopieert `bron/figuren/` ongewijzigd mee en deelt het Markdown-rapport op in secties en zet ze in een ReSpec-pagina in `/respec/` (sjabloon `respec/index.template.html`). Tekst vóór het eerste hoofdstuk wordt *Status van dit document*, het hoofdstuk Samenvatting de samenvatting en *Bijlage X: ...* een ReSpec-bijlage. ReSpec nummert zelf; handmatige nummers in bijlagekoppen worden weggehaald.
- `site_root/index.html` is de startpagina; GitHub Pages publiceert het geheel.

Lokaal testen: `pip install -r requirements.txt`, pandoc installeren, dan `python scripts/build_site.py && mkdocs serve`.

## Eenmalige instellingen

1. *Settings → Pages → Build and deployment → Source:* **GitHub Actions**.
Later, als reacties gewenst zijn:

2. *Settings → General → Features:* **Discussions** aan; maak een categorie *Reacties* (type *Announcement* of *Open-ended discussion*).
3. Installeer de giscus-app via [giscus.app](https://giscus.app), kies deze repository en de categorie *Reacties*, en zet de getoonde `repo_id` en `category_id` in `mkdocs.base.yml` onder `extra.giscus`. Zolang daar `VUL_IN` staat, wordt het reactieveld niet getoond.
