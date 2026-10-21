# Digital twins voor het energiesysteem en de gebouwde omgeving

Publieksversie van de inventarisatie *Verkenner Digital Twins* (Energy Innovation NL), opgesteld door Martijn van Glabbeek (Bizz4Mation).

Leesbare site: **https://mvglabbeek.github.io/dtverkenner/**

Reageren kan onderaan elke pagina (via GitHub Discussions) of in [Discussions](https://github.com/MvGlabbeek/dtverkenner/discussions).

## Nieuwe versie publiceren

1. Controleer de publieksversie (rapport en register). Beide bestandsnamen moeten `publiek` bevatten, bijvoorbeeld
   `Inventarisatie_digital_twins_NL_EU_2026-10_v13_publiek.docx` en `Register_digital_twins_NL_EU_2026-10_v13_publiek.xlsx`.
2. Upload beide bestanden in de map [`bron/`](bron/) (op github.com: *Add file → Upload files*). Oude versies mogen blijven staan.
3. Commit naar `main`. De workflow *Publiceer site* bouwt en publiceert de site binnen een paar minuten (zie tabblad *Actions*).
4. Optioneel: maak een tag of release (bijv. `v13`) om de versie vast te leggen.

De site gebruikt altijd het bestand met het hoogste versienummer (`_v13`) in de naam. Bestanden zonder `publiek` in de naam worden genegeerd.

## Wat de workflow doet

- `scripts/build_site.py` zet het Word-document met pandoc om naar Markdown, één pagina per hoofdstuk (kop 1), inclusief figuren.
- Het tabblad *Portfolio* van het register wordt een doorzoekbare tabel; beide bestanden staan als download op de site.
- MkDocs Material bouwt de site; GitHub Pages publiceert hem.

Lokaal testen: `pip install -r requirements.txt`, pandoc installeren, dan `python scripts/build_site.py && mkdocs serve`.

## Eenmalige instellingen

1. *Settings → Pages → Build and deployment → Source:* **GitHub Actions**.
2. *Settings → General → Features:* **Discussions** aan; maak een categorie *Reacties* (type *Announcement* of *Open-ended discussion*).
3. Installeer de giscus-app via [giscus.app](https://giscus.app), kies deze repository en de categorie *Reacties*, en zet de getoonde `repo_id` en `category_id` in `mkdocs.base.yml` onder `extra.giscus`. Zolang daar `VUL_IN` staat, wordt het reactieveld niet getoond.
