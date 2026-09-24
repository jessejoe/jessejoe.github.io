"""Jinja2 rendering for the web (index.html) and print (print.html) templates."""

import urllib.parse
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Mirrors the shapes in templates/partials/icons.html. Duplicated here (rather
# than parsed out of the template) because the PDF path can't use inline <svg>
# icons at all -- WeasyPrint drops the PDF link annotation for the first of
# several same-page <a> elements that contain one (confirmed via isolated
# testing). Rendering the icon as a CSS background-image on a <span> instead
# sidesteps that entirely, but that requires the raw shape data in Python to
# build a data: URI, so the two need to stay in sync by hand.
_ICON_SHAPES = {
    "mail": ("stroke", '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>'),
    "phone": ("fill", '<path d="M6.6 10.8c1.4 2.7 3.6 4.9 6.3 6.3l2.1-2.1c.3-.3.7-.4 1.1-.2 1.1.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.9 21 3 13.1 3 3.6c0-.6.4-1 1-1h3.6c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1.1z"/>'),
    "location": ("stroke", '<path d="M12 22s7-6.5 7-12a7 7 0 10-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.4"/>'),
    "globe": ("stroke", '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.8 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.8-3.8-9S9.5 5.6 12 3z"/>'),
    "github": ("fill", '<path d="M12 2C6.5 2 2 6.6 2 12.3c0 4.5 2.9 8.4 7 9.7.5.1.7-.2.7-.5v-1.9c-2.9.6-3.5-1.4-3.5-1.4-.5-1.2-1.1-1.6-1.1-1.6-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.3-.3-4.7-1.2-4.7-5.2 0-1.1.4-2 1-2.8-.1-.3-.5-1.4.1-2.9 0 0 .8-.3 2.7 1a9.2 9.2 0 015 0c1.9-1.3 2.7-1 2.7-1 .5 1.5.2 2.6.1 2.9.6.8 1 1.7 1 2.8 0 4-2.4 4.9-4.7 5.1.4.3.7 1 .7 2v3c0 .3.2.6.7.5 4.1-1.3 7-5.2 7-9.7C22 6.6 17.5 2 12 2z"/>'),
    "stackoverflow": ("fill", '<path d="M15.725 0l-1.72 1.277 6.39 8.588 1.716-1.277L15.725 0zm-3.94 3.418l-1.369 1.644 8.225 6.85 1.369-1.644-8.225-6.85zm-3.15 4.465l-.905 1.94 9.702 4.517.904-1.94-9.701-4.517zm-1.85 4.86l-.44 2.093 10.473 2.201.44-2.092-10.473-2.203zM1.89 15.47V24h19.19v-8.53h-2.133v6.397H4.021v-6.396H1.89zm4.265 2.133v2.13h10.66v-2.13H6.154Z"/>'),
    "link": ("stroke", '<path d="M10 14a5 5 0 007 0l3-3a5 5 0 00-7-7l-1.5 1.5M14 10a5 5 0 00-7 0l-3 3a5 5 0 007 7l1.5-1.5"/>'),
    "bug": ("stroke", '<rect x="8" y="7" width="8" height="11" rx="4"/><path d="M12 7V4M9 4l1.5 1.5M15 4l-1.5 1.5M4 10l4 1M4 17l4-1M20 10l-4 1M20 17l-4-1M9 18l-2 3M15 18l2 3"/>'),
    "pr": ("stroke", '<circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M6 8.2V15.8M18 8.2v5c0 1.5-1 2.8-3 2.8h-3"/>'),
}


def _icon_data_uri(name, color):
    mode, inner = _ICON_SHAPES[name]
    attrs = f'fill="none" stroke="{color}" stroke-width="1.8"' if mode == "stroke" else f'fill="{color}"'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" {attrs}>{inner}</svg>'
    return "data:image/svg+xml," + urllib.parse.quote(svg)


def make_env(icon_color="#5B6B7A"):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=["jinja2.ext.do"],
    )
    env.globals["icon_data_uri"] = lambda name: _icon_data_uri(name, icon_color)
    return env


def render_web(env, content, sections_meta, theme, *, build_date, pdf_links, noindex=False, asset_prefix=""):
    template = env.get_template("index.html")
    context = {
        **content,
        "content": content,
        "sections": sections_meta,
        "theme": theme,
        "pdf": False,
        "noindex": noindex,
        "build_date": build_date,
        "pdf_links": pdf_links,
        "asset_prefix": asset_prefix,
    }
    return template.render(**context)


def render_print(env, content, sections_meta, theme, mode):
    template = env.get_template("print.html")
    context = {
        **content,
        "content": content,
        "sections": sections_meta,
        "theme": theme,
        "pdf": True,
        "mode": mode,
    }
    return template.render(**context)
