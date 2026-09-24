import argparse
import shutil
import tempfile
from datetime import date
from pathlib import Path

import content_loader
import favicon as favicon_module
import filtering
import pdf as pdf_module
import render
import targets as targets_module

GENERATOR_DIR = Path(__file__).parent
STATIC_DIR = GENERATOR_DIR / "static"
DIST_DIR = GENERATOR_DIR / "dist"

PDF_LABELS = {"full": "Full PDF", "summary": "Highlights PDF"}


def _pdf_filename(name, mode):
    base = "".join(name.split()) + "Resume"
    if mode == "summary":
        base += "Summary"
    return base + ".pdf"


def _copy_static(out_dir, favicon_dir):
    for sub in ("css", "img"):
        src = STATIC_DIR / sub
        if src.exists():
            shutil.copytree(src, out_dir / sub, dirs_exist_ok=True)
    if favicon_dir:
        for f in favicon_dir.iterdir():
            shutil.copy2(f, out_dir / "img" / f.name)


def build_one(env, content, sections_meta, theme, *, out_dir, modes, page_size, no_pdf, noindex, favicon_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    _copy_static(out_dir, favicon_dir)

    build_date = date.today().isoformat()
    pdf_links = []

    if not no_pdf:
        for mode in modes:
            filename = _pdf_filename(content["personal_info"]["name"], mode)
            pdf_content = filtering.apply_tier_mode(content, sections_meta, mode)
            print_html = render.render_print(env, pdf_content, sections_meta, theme, mode)
            pdf_module.render_pdf(print_html, out_dir / filename, page_size=page_size)
            print(f"  wrote {out_dir / filename}")
            pdf_links.append({"label": PDF_LABELS[mode], "href": filename})

    html = render.render_web(
        env, content, sections_meta, theme,
        build_date=build_date, pdf_links=pdf_links, noindex=noindex,
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote {out_dir / 'index.html'}")


def main():
    parser = argparse.ArgumentParser(description="Build the resume site and PDF.")
    parser.add_argument("--target", help='Tailored target name (from targets/), or "all"')
    parser.add_argument(
        "--mode", choices=["full", "summary"],
        help="Build only this PDF variant instead of the default of building both full and summary",
    )
    parser.add_argument("--no-pdf", action="store_true", help="Skip WeasyPrint PDF generation (faster HTML/CSS iteration)")
    parser.add_argument("--page-size", default=None, help="Override PDF @page size, e.g. Letter or A4")
    parser.add_argument("--list-targets", action="store_true", help="List available targets and exit")
    args = parser.parse_args()

    if args.list_targets:
        for name in targets_module.list_target_names():
            print(name)
        return

    content = content_loader.load_all()
    sections_meta = content_loader.load_sections()
    theme = content_loader.load_theme()
    env = render.make_env(icon_color=theme["subheadings"])

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    favicon_dir = None
    photo = content["personal_info"].get("photo")
    if photo:
        favicon_dir = Path(tempfile.mkdtemp(prefix="jessejoe-favicon-"))
        favicon_module.generate(
            STATIC_DIR / photo, favicon_dir,
            name=content["personal_info"]["name"],
            theme_color=theme["headings"],
            background_color=theme["background"],
        )
        print(f"Generated favicons from {photo}")

    try:
        print("Building base site...")
        base_modes = [args.mode] if args.mode else ["full", "summary"]
        build_one(
            env, content, sections_meta, theme,
            out_dir=DIST_DIR, modes=base_modes,
            page_size=args.page_size, no_pdf=args.no_pdf, noindex=False,
            favicon_dir=favicon_dir,
        )

        if args.target:
            target_names = targets_module.list_target_names() if args.target == "all" else [args.target]
            for name in target_names:
                target = targets_module.load_target(name)
                print(f"Building target '{name}'...")
                target_content = filtering.apply_target(content, target)
                if args.mode:
                    modes = [args.mode]
                elif target.get("mode"):
                    modes = [target["mode"]]
                else:
                    modes = ["full", "summary"]
                build_one(
                    env, target_content, sections_meta, theme,
                    out_dir=DIST_DIR / target["output_slug"], modes=modes,
                    page_size=args.page_size, no_pdf=args.no_pdf, noindex=True,
                    favicon_dir=favicon_dir,
                )
    finally:
        if favicon_dir:
            shutil.rmtree(favicon_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
