"""Generates favicon/app-icon assets from personal_info.photo at build time,
instead of hand-maintaining a separate set of pre-baked icon files."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

# Circular crop for these -- matches the circular photo treatment already
# used in the page header, and is how the old hand-generated favicon looked.
_CIRCULAR_PNG_SIZES = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "android-chrome-192x192.png": 192,
}
_ICO_SIZES = [(16, 16), (32, 32), (48, 48)]
_APPLE_TOUCH_SIZE = 180


def _square_crop(im):
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    return im.crop((left, top, left + side, top + side))


def _circular(square_im, supersample=4):
    """Masks a square RGBA image to a circle, anti-aliased by masking at a
    higher resolution first and downsampling back (a plain same-size mask
    leaves visibly jagged/stair-stepped edges, especially once shrunk further
    to 16px)."""
    size = square_im.size[0]
    big = square_im.resize((size * supersample, size * supersample), Image.LANCZOS)
    mask = Image.new("L", big.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big.size[0], big.size[1]), fill=255)
    big.putalpha(mask)
    return big.resize((size, size), Image.LANCZOS)


def generate(photo_path, out_dir, *, name, theme_color, background_color):
    out_dir.mkdir(parents=True, exist_ok=True)
    square = _square_crop(Image.open(photo_path).convert("RGBA"))
    circular = _circular(square)

    for filename, size in _CIRCULAR_PNG_SIZES.items():
        circular.resize((size, size), Image.LANCZOS).save(out_dir / filename)
    circular.save(out_dir / "favicon.ico", sizes=_ICO_SIZES)

    # NOT circular: iOS renders transparent pixels as solid black and applies
    # its own rounded-corner mask on top, so apple-touch-icon needs a plain
    # opaque square -- a transparent circle here would show up with black
    # corners on an iPhone home screen instead of a clean circle.
    apple = Image.alpha_composite(Image.new("RGBA", square.size, background_color), square).convert("RGB")
    apple.resize((_APPLE_TOUCH_SIZE, _APPLE_TOUCH_SIZE), Image.LANCZOS).save(out_dir / "apple-touch-icon.png")

    manifest = {
        "name": name,
        "short_name": name,
        "icons": [{"src": "img/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"}],
        "theme_color": theme_color,
        "background_color": background_color,
        "display": "standalone",
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
