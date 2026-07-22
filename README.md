# Planktivore Labelling Guide

A lightweight, portable, multi-format annotation guide for **Planktivore** plankton images. One set of source data produces three outputs from a single git repo:

- an **HTML website** (like the [WHOI IFCB guide](https://whoigit.github.io/whoi-plankton/)),
- a **PDF** of the full guide, and
- a **PowerPoint** training deck.

Built with [Quarto](https://quarto.org). Content is data-driven: you write each class once as metadata plus images, and a generator renders every page and format.

## How it's organised

```
_quarto.yml            site config (nav, theme, formats)
index.qmd              homepage — auto-listed grid of all classes
about.qmd              instrument context + how to use the guide
classes/<id>/
  meta.yml             the class's text (source of truth)
  ideal/               clean, textbook reference images
  challenging/         messy, real-world images
  index.qmd            GENERATED website page (do not hand-edit)
guide.qmd              GENERATED combined document for the PDF (do not hand-edit)
slides/training.qmd    the PPTX / reveal.js training deck
scripts/
  build_pages.py       meta.yml + images  ->  class pages + guide.qmd
  check_meta.py        completeness / consistency checks (run in CI)
  make_thumbnails.py   optional image optimizer
  meta.template.yml    copy this to add a new class
.github/workflows/     CI: build all three formats, deploy the site to Pages
```

The single source of truth is `classes/<id>/meta.yml` plus the two image folders.
**Never hand-edit the generated `index.qmd` / `guide.qmd`** — edit `meta.yml` and re-run the generator.

## One-time setup

1. Install [Quarto](https://quarto.org/docs/get-started/).
2. Install Python deps: `pip install -r requirements.txt`
3. For the PDF, install LaTeX once: `quarto install tinytex`

## Everyday workflow

```bash
make check      # validate metadata
make gen        # regenerate class pages + guide.qmd from meta.yml
make preview    # live-preview the website in your browser
make pdf        # build the PDF
make slides     # build the PPTX
make all        # everything
```

(No `make`? Run the underlying commands: `python scripts/build_pages.py`,
then `quarto render`, `quarto render guide.qmd --to pdf`,
`quarto render slides/training.qmd --to pptx`.)

## Adding a class

1. `cp scripts/meta.template.yml classes/<class_id>/meta.yml` and fill it in.
2. Add images to `classes/<class_id>/ideal/` and `classes/<class_id>/challenging/`.
3. `make check && make gen && make preview`.
4. Commit and push — CI rebuilds and redeploys all three formats.

## Deployment

Pushing to `main` triggers `.github/workflows/publish.yml`, which validates metadata, generates pages, renders the HTML/PDF/PPTX, deploys the website to **GitHub Pages**, and attaches the PDF and PPTX as downloadable artifacts. Enable Pages once under **Settings → Pages → Source: GitHub Actions**, and replace the `CeNCOOS` placeholders in `_quarto.yml`.

## Notes

- Three example classes are included as a first pass: **Eucampia**, **Pseudo-nitzschia** and **Chaetoceros**. 
- Image footprint is small (tens of KB per PNG), so plain git is fine; no Git LFS needed.