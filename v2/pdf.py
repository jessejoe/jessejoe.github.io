"""WeasyPrint wrapper: renders the print HTML string to a PDF file."""

from pathlib import Path

from weasyprint import HTML

STATIC_DIR = Path(__file__).parent / "static"


def render_pdf(html_string, out_path, page_size=None):
    html_string = _apply_page_size(html_string, page_size)
    HTML(string=html_string, base_url=str(STATIC_DIR)).write_pdf(out_path)


def _apply_page_size(html_string, page_size):
    if not page_size:
        return html_string
    override = f"<style>@page {{ size: {page_size}; }}</style></head>"
    return html_string.replace("</head>", override, 1)
