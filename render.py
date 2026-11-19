"""Render entry.png from verified news JSON; requires Pillow, offline only."""
from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "news-2026-11-19.json"
SIZE = (1024, 1024)
INK = "#17212B"
MUTED = "#59636E"
PAPER = "#FAF8F3"
ACCENTS = ("#A84430", "#315E73", "#71633A", "#65557E", "#38684F", "#8A5738")
REGULAR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def lines(draw, text, fnt, width):
    words = text.split()
    result, line = [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=fnt) > width:
            result.append(line)
            line = word
        else:
            line = candidate
    if line:
        result.append(line)
    return result


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    stories = data["stories"]
    if data["date"] != "2026-11-19" or not 5 <= len(stories) <= 6:
        raise ValueError("Expected five or six verified stories dated 2026-11-19")
    for story in stories:
        if story.get("date") != data["date"]:
            raise ValueError(f"Wrong story date: {story.get('title')}")
        for field in ("title", "summary", "source", "link"):
            if not story.get(field):
                raise ValueError(f"Missing {field} in {story.get('title')}")

    im = Image.new("RGB", SIZE, PAPER)
    d = ImageDraw.Draw(im)
    d.text((58, 42), "WORLD BRIEFING", font=font(16, True), fill=MUTED)
    d.text((58, 76), "Thursday 19 November 2026", font=font(38, True), fill=INK)
    d.text((58, 130), "World News in One Image", font=font(27), fill=MUTED)
    d.line((58, 178, 966, 178), fill="#C9C7C0", width=2)
    y = 190
    for index, story in enumerate(stories, 1):
        accent = ACCENTS[index - 1]
        d.rounded_rectangle((58, y + 1, 88, y + 31), radius=4, fill=accent)
        d.text((73, y + 16), str(index), font=font(16, True), fill="white", anchor="mm")
        headline = font(21, True)
        summary = font(18)
        title_lines = lines(d, story["title"], headline, 842)
        for line in title_lines:
            d.text((108, y), line, font=headline, fill=INK)
            y += 30
        y += 1
        for line in lines(d, story["summary"], summary, 842):
            d.text((108, y), line, font=summary, fill="#37434E")
            y += 28
        d.text((108, y + 1), story["source"], font=font(16), fill=MUTED)
        y += 33
        if index < len(stories):
            d.line((108, y, 966, y), fill="#DDDAD2", width=1)
            y += 10
    if y > 988:
        raise ValueError(f"Content overflows layout: ends at y={y}; shorten the copy")
    d.line((58, 987, 966, 987), fill="#C9C7C0", width=1)
    d.text((58, 1000), "A snapshot of the day’s reporting · Summaries from the cited sources",
           font=font(14), fill=MUTED)
    im.save(ROOT / "entry.png", format="PNG", optimize=True)
    print(f"Rendered entry.png: {SIZE[0]}×{SIZE[1]}, {(ROOT / 'entry.png').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
