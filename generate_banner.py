#!/usr/bin/env python3
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUTPUT = ROOT / "banner.png"
FONT = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
GREEN = (39, 174, 96)
LOGO_PX = 120
FONT_PX = 72
GAP = 24
PAD_X = 48
PAD_Y = 32


def render_svg(path: Path, size: int) -> Image.Image:
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        _ = subprocess.run(
            [
                "rsvg-convert",
                "-w",
                str(size),
                "-h",
                str(size),
                "-o",
                tmp.name,
                str(path),
            ],
            check=True,
        )
        return Image.open(tmp.name).copy()


def generate_banner() -> None:
    logo = render_svg(ROOT / "logo.svg", LOGO_PX)
    font = ImageFont.truetype(FONT, FONT_PX)

    bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
        (0, 0),
        "libcaptcha",
        font=font,
    )
    tw = int(bbox[2] - bbox[0])
    th = int(bbox[3] - bbox[1])

    w = PAD_X + LOGO_PX + GAP + tw + PAD_X
    h = PAD_Y + max(LOGO_PX, th) + PAD_Y
    banner = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    cx = (w - LOGO_PX - GAP - tw) // 2
    banner.paste(logo, (cx, (h - LOGO_PX) // 2), logo)

    draw = ImageDraw.Draw(banner)
    draw.text(
        (cx + LOGO_PX + GAP, (h - th) // 2 - bbox[1]),
        "libcaptcha",
        font=font,
        fill=GREEN,
    )

    banner.save(OUTPUT, "PNG")
    print(f"Saved {OUTPUT} ({w}x{h})")


if __name__ == "__main__":
    generate_banner()
