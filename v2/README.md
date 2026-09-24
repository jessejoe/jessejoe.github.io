# Resume generator

Builds the website + PDF resume from YAML content in `content/`. Replaces the old
Grunt/`grunt-bake` toolchain in `../src/` (untouched for now — see "Swapping this in"
below).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

WeasyPrint (the PDF engine) needs a few system libraries. On Debian/Ubuntu:

```bash
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libcairo2 libffi-dev
```

On macOS: `brew install pango gdk-pixbuf libffi cairo`.

Favicons (`favicon.ico`, the various PNG sizes, `site.webmanifest`) aren't checked-in
static files — `favicon.py` generates them from `personal_info.photo` on every build
(center-cropped to square, resized to each size), so changing the photo is enough;
there's nothing to regenerate by hand.

## Building

```bash
python build.py                      # site + BOTH PDFs -> dist/JesseJarzynkaResume.pdf and ...Summary.pdf
python build.py --mode=summary       # build only the highlights-only PDF
python build.py --mode=full          # build only the full PDF
python build.py --target=acme-corp   # tailored variant -> dist/acme-corp/ (both PDFs, unless the target sets `mode`)
python build.py --target=all         # rebuild every file in targets/
python build.py --list-targets
python build.py --no-pdf             # skip WeasyPrint, just the HTML (faster iteration)
python build.py --page-size=A4       # override the PDF page size (default Letter)
```

`dist/index.html` always renders the *full* site with expand/collapse — `--mode` only
changes which PDF variant(s) get built (the website always ships everything, with
older roles and lower-priority sections previewed a few items at a time behind a
fading "show more" reveal). The page footer links to whichever PDFs were built.

Open `dist/index.html` directly in a browser to preview, or `python -m http.server`
from inside `dist/`.

## Editing your content

Everything lives in `content/*.yaml`. A few things worth knowing:

- **`sections.yaml`** controls section order/column, and whether a section is
  included at all in `--mode=summary` (`summary: true`) or only ever shown on the
  full website behind a click-to-expand toggle (`summary: false`).
- **`experiences.yaml`** bullets and entries can carry a `tier`: `highlight` (always
  shown) or `standard` (tucked behind a "show more" toggle on the web, dropped
  entirely from `--mode=summary` PDFs). Give a bullet as a plain string to default it
  to `standard`, or `{text: "...", tier: highlight}` to promote it.
- **`tags`** on experiences/projects/certificates are used by the tailoring tool
  (see below) — add whatever tags are useful to you, there's no fixed vocabulary.
- **`theme.yaml`** has the handful of colors actually used site-wide.

## Tailoring a resume for a specific role

Copy `targets/_example.yaml` to `targets/<name>.yaml` and edit it — it can override
the profession/summary text, filter experiences/projects by tag or id, reorder
entries, or exclude a section entirely. Then:

```bash
python build.py --target=<name>
```

produces `dist/<name>/index.html` + `dist/<name>/resume.pdf`, without touching the
base site.

## Swapping this in as the live site

When you're happy with the output: copy `dist/` into `../docs/` (GitHub Pages serves
from there), keeping `docs/CNAME` and `docs/other/` as they are, then delete
`../src/`, `../Gruntfile.js`, `../package.json`, `../package-lock.json`, and
`../node_modules/`. Nothing here does that automatically — do it yourself, in one
commit, whenever you're ready.
