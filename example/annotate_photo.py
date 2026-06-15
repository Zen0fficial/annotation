from pathlib import Path
from math import atan2, cos, sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PHOTO = ROOT / "photo.png"
OUTPUT = ROOT / "photo_annotated.png"


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def dashed_line(draw, start, end, fill, width=3, dash=18, gap=10):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0
    while pos < length:
        seg_end = min(pos + dash, length)
        draw.line(
            [(x1 + ux * pos, y1 + uy * pos), (x1 + ux * seg_end, y1 + uy * seg_end)],
            fill=fill,
            width=width,
        )
        pos += dash + gap


def arrow(draw, start, end, fill, width=4, dashed=False):
    if dashed:
        dashed_line(draw, start, end, fill, width=width)
    else:
        draw.line([start, end], fill=fill, width=width)

    angle = atan2(end[1] - start[1], end[0] - start[0])
    head = 18
    spread = pi / 7
    p1 = (end[0] - head * cos(angle - spread), end[1] - head * sin(angle - spread))
    p2 = (end[0] - head * cos(angle + spread), end[1] - head * sin(angle + spread))
    draw.polygon([end, p1, p2], fill=fill)
    r = 7
    draw.ellipse((end[0] - r, end[1] - r, end[0] + r, end[1] + r), fill=fill, outline=(255, 255, 255), width=2)


def rounded_box(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    line = ""
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    for word in words:
        test = word if not line else f"{line} {word}"
        if d.textbbox((0, 0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def label_row(draw, x, y, w, title, subtitle, color, font_title, font_body, inferred=False):
    row_h = 72 if len(subtitle) <= 58 else 88
    fill = (24, 24, 24, 235)
    outline = (130, 130, 130, 255) if inferred else color
    rounded_box(draw, (x, y, x + w, y + row_h), 10, fill=fill, outline=outline, width=2)
    draw.rectangle((x + 10, y + 12, x + 28, y + row_h - 12), fill=color)
    if inferred:
        draw.text((x + w - 92, y + 10), "inferred", font=font_body, fill=(210, 210, 210))
    draw.text((x + 38, y + 10), title, font=font_title, fill=(255, 255, 255))
    lines = wrap_text(subtitle, font_body, w - 54)
    for i, line in enumerate(lines[:2]):
        draw.text((x + 38, y + 38 + i * 20), line, font=font_body, fill=(220, 220, 220))
    return row_h


def main():
    photo = Image.open(PHOTO).convert("RGBA")
    w, h = photo.size
    panel_w = 610
    canvas = Image.new("RGBA", (w + panel_w, h), (12, 12, 12, 255))
    canvas.alpha_composite(photo, (0, 0))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    title_font = load_font(30, bold=True)
    h_font = load_font(22, bold=True)
    body_font = load_font(18)
    small_font = load_font(15)

    # Dim only the panel side; keep SEM intensities untouched.
    draw.rectangle((w, 0, w + panel_w, h), fill=(15, 15, 15, 248))
    draw.line((w, 0, w, h), fill=(255, 255, 255, 180), width=2)

    # Small title card on the photo.
    rounded_box(draw, (24, 22, 700, 128), 12, fill=(0, 0, 0, 165), outline=(255, 255, 255, 130))
    draw.text((44, 34), "Annotated SEM cross-section", font=title_font, fill=(255, 255, 255))
    draw.text((46, 75), "Labels transferred from design.png and table.png", font=body_font, fill=(230, 230, 230))
    draw.text((46, 100), "Solid = visually anchored, dashed = design/table inferred", font=small_font, fill=(210, 210, 210))

    px = w + 28
    draw.text((px, 28), "Layer / material / design thickness", font=h_font, fill=(255, 255, 255))

    items = [
        {
            "title": "Bank2 + Bank1",
            "subtitle": "Organic layers, 1000 nm + 500 nm",
            "color": (255, 193, 7, 255),
            "target": (1295, 90),
            "y": 78,
            "inferred": True,
        },
        {
            "title": "Anode",
            "subtitle": "ITO/Ag/ITO, 7/110/10 nm; thin bright conductor",
            "color": (0, 177, 236, 255),
            "target": (730, 47),
            "y": 168,
            "inferred": False,
        },
        {
            "title": "PLN2/3",
            "subtitle": "Organic planarization, 2700 nm; large dark upper fill",
            "color": (170, 170, 170, 255),
            "target": (780, 245),
            "y": 258,
            "inferred": False,
        },
        {
            "title": "SD2",
            "subtitle": "Ti/Al/Ti, 80/700/50 nm; upper source/drain metal",
            "color": (244, 177, 131, 255),
            "target": (860, 542),
            "y": 358,
            "inferred": False,
        },
        {
            "title": "PLN1",
            "subtitle": "Organic planarization, 2000 nm; under SD2",
            "color": (190, 225, 175, 255),
            "target": (1080, 588),
            "y": 458,
            "inferred": True,
        },
        {
            "title": "PV + ILD",
            "subtitle": "PV SiNx 350 nm; ILD SiO2/SiNx 300/200 nm",
            "color": (190, 215, 245, 255),
            "target": (880, 655),
            "y": 548,
            "inferred": True,
        },
        {
            "title": "Right contact stack",
            "subtitle": "SD1 Ti/Al/Ti 80/600/50; GE2 Mo 300; GI2 SiNx 130",
            "color": (255, 220, 150, 255),
            "target": (1450, 625),
            "y": 648,
            "inferred": False,
        },
        {
            "title": "Lower device stack",
            "subtitle": "GE1 Mo 300; GI1 SiO2 130; Poly-Si 45; Buffer SiO2/SiNx 300/50; 3L",
            "color": (255, 235, 59, 255),
            "target": (760, 740),
            "y": 756,
            "inferred": True,
        },
        {
            "title": "Glass substrate",
            "subtitle": "Base substrate; composition listed as O/Si/metal traces",
            "color": (150, 150, 150, 255),
            "target": (620, 910),
            "y": 878,
            "inferred": False,
        },
    ]

    row_x = w + 28
    row_w = panel_w - 56
    for item in items:
        row_h = label_row(
            draw,
            row_x,
            item["y"],
            row_w,
            item["title"],
            item["subtitle"],
            item["color"],
            h_font,
            small_font,
            inferred=item["inferred"],
        )
        start = (row_x, item["y"] + row_h // 2)
        arrow(draw, start, item["target"], item["color"], width=4, dashed=item["inferred"])

    # Highlight a few major interfaces without asserting exact invisible boundaries.
    draw.line((690, 48, 1220, 48), fill=(0, 177, 236, 155), width=4)
    draw.line((420, 545, 1035, 545), fill=(244, 177, 131, 145), width=5)
    draw.line((20, 632, 1185, 632), fill=(190, 215, 245, 130), width=4)
    draw.line((40, 733, 1280, 733), fill=(255, 235, 59, 115), width=4)

    # Footer note over the panel only.
    rounded_box(draw, (w + 28, h - 130, w + panel_w - 28, h - 24), 10, fill=(34, 34, 34, 235), outline=(90, 90, 90, 255))
    note = (
        "Note: adjacent organic/dielectric layers with weak contrast are annotated from "
        "the design/table, not as directly measured SEM boundaries."
    )
    for i, line in enumerate(wrap_text(note, small_font, panel_w - 82)[:4]):
        draw.text((w + 48, h - 112 + i * 21), line, font=small_font, fill=(225, 225, 225))

    canvas.alpha_composite(overlay)
    canvas.convert("RGB").save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
