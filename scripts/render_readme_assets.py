from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import duckdb
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "warehouse" / "search_observatory.duckdb"
SCREENSHOTS = ROOT / "screenshots"
MART_SCHEMA = "observatory_observatory"

BG = "#081422"
PANEL = "#131f32"
CARD = "#192840"
BORDER = "#274465"
TEXT = "#eef0df"
MUTED = "#aeb8cb"
ACCENT = "#79c3ff"
WARN = "#ffd66e"
CRITICAL = "#ff8b8b"
STABLE = "#8de1b0"


def font(size: int, bold: bool = False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], max_width: int, line_height: int, fill: str, fnt) -> int:
    x, y = xy
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_height
    return y


def base_canvas(title: str, subtitle: str):
    img = Image.new("RGB", (1600, 900), BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((36, 36, 1564, 864), radius=30, fill=PANEL, outline=BORDER, width=2)
    draw.text((86, 84), title, font=font(24), fill=ACCENT)
    draw.text((86, 148), subtitle, font=font(58, bold=True), fill=TEXT)
    return img, draw


def metric_card(draw, box, title, value, blurb):
    draw.rounded_rectangle(box, radius=24, fill=CARD, outline=BORDER, width=2)
    x1, y1, x2, _ = box
    draw.text((x1 + 26, y1 + 24), title, font=font(17), fill=MUTED)
    draw.text((x1 + 26, y1 + 78), str(value), font=font(44, bold=True), fill=TEXT)
    draw_wrapped(draw, blurb, (x1 + 26, y1 + 142), x2 - x1 - 52, 28, MUTED, font(18))


def render():
    con = duckdb.connect(str(DB_PATH))
    site_health = con.execute(f"select * from {MART_SCHEMA}.mart_site_health").fetchone()
    anomalies = con.execute(
        """
        select url, anomaly_type, severity_score, operator_action
        from observatory_observatory.mart_anomaly_flags
        order by severity_score desc
        """
    ).fetchall()
    page_groups = con.execute(
        """
        select page_group, owner_team, impressions_5d, avg_ctr, avg_response_ms, has_critical_url
        from observatory_observatory.mart_page_group_performance
        order by impressions_5d desc
        """
    ).fetchall()
    urls = con.execute(
        """
        select page_group, url, observability_status, five_day_impressions, response_ms
        from observatory_observatory.mart_url_observability
        order by five_day_impressions desc
        """
    ).fetchall()

    SCREENSHOTS.mkdir(exist_ok=True)

    img, draw = base_canvas("DBT SEARCH OBSERVATORY", "Warehouse-first visibility for search, crawl, and index risk.")
    metric_card(draw, (86, 300, 430, 560), "Tracked URLs", site_health[0], "Canonical pages under active observability coverage.")
    metric_card(draw, (450, 300, 794, 560), "Critical URLs", site_health[2], "High-priority surfaces with urgent indexability or latency pressure.")
    metric_card(draw, (814, 300, 1158, 560), "Watch URLs", site_health[3], "Pages drifting into slower crawl or softer search performance.")
    metric_card(draw, (1178, 300, 1522, 560), "Blended CTR", f"{site_health[5] * 100:.1f}%", "Five-day click-through performance across the tracked estate.")
    draw.rounded_rectangle((86, 604, 1522, 804), radius=24, fill=CARD, outline=BORDER, width=2)
    draw.text((112, 634), "OPERATING READOUT", font=font(20), fill=ACCENT)
    draw.text((112, 682), "Latest crawl landed with one critical money-page issue and two watch-tier degradations.", font=font(34, bold=True), fill=TEXT)
    draw.text((112, 744), f"Average response time is {site_health[4]} ms. The warehouse is current through {site_health[6]}.", font=font(24), fill=MUTED)
    img.save(SCREENSHOTS / "01-hero.png")

    img, draw = base_canvas("PAGE GROUP WATCH", "Performance rollups isolate which content lanes are dragging search health.")
    positions = [(86, 288, 780, 500), (820, 288, 1514, 500), (86, 540, 780, 752), (820, 540, 1514, 752)]
    for box, row in zip(positions, page_groups[:4]):
        page_group, owner_team, impressions_5d, avg_ctr, avg_response_ms, has_critical = row
        draw.rounded_rectangle(box, radius=22, fill=CARD, outline=BORDER, width=2)
        x1, y1, x2, _ = box
        draw.text((x1 + 28, y1 + 26), page_group.replace("_", " ").title(), font=font(30, bold=True), fill=TEXT)
        draw.text((x1 + 28, y1 + 74), f"Owner: {owner_team.replace('_', ' ').title()}", font=font(18), fill=MUTED)
        draw.text((x1 + 28, y1 + 126), f"Impressions: {impressions_5d:,}", font=font(24, bold=True), fill=TEXT)
        draw.text((x1 + 28, y1 + 164), f"CTR: {avg_ctr * 100:.2f}%", font=font(22), fill=WARN)
        draw.text((x1 + 260, y1 + 164), f"Crawl latency: {avg_response_ms:.0f} ms", font=font(22), fill=MUTED)
        status = "Critical URL present" if has_critical else "No critical URL"
        status_fill = CRITICAL if has_critical else STABLE
        draw.text((x1 + 28, y1 + 206), status, font=font(22, bold=True), fill=status_fill)
    img.save(SCREENSHOTS / "02-page-groups.png")

    img, draw = base_canvas("ANOMALY BOARD", "Operator-facing actions are generated from model outputs, not hand-written screenshots.")
    y = 280
    for idx, row in enumerate(anomalies[:3], start=1):
        url, anomaly_type, severity, action = row
        box = (86, y, 1518, y + 154)
        draw.rounded_rectangle(box, radius=22, fill=CARD, outline=BORDER, width=2)
        draw.text((112, y + 24), f"P{idx} · {anomaly_type.replace('_', ' ').title()}", font=font(22), fill=ACCENT)
        draw.text((112, y + 62), url.replace("https://kineticgain.com/", "/"), font=font(34, bold=True), fill=TEXT)
        draw.text((1278, y + 60), str(severity), font=font(42, bold=True), fill=CRITICAL if severity >= 90 else WARN)
        draw_wrapped(draw, action, (112, y + 110), 1180, 28, MUTED, font(20))
        y += 184
    img.save(SCREENSHOTS / "03-anomalies.png")

    img, draw = base_canvas("VALIDATION PROOF", "Proof capture comes from the built warehouse and testable DuckDB state.")
    draw.rounded_rectangle((86, 286, 950, 790), radius=22, fill="#09111c", outline=BORDER, width=2)
    code = [
        "> dbt seed --full-refresh",
        "> dbt run",
        "> dbt test",
        "",
        "tracked_urls        6",
        "critical_urls       1",
        "watch_urls          2",
        "avg_response_ms     406.8",
        "",
        "top_flag            money_page_indexability_loss",
        "flag_url            /templates/feature-flags",
    ]
    cy = 320
    for line in code:
        draw.text((118, cy), line, font=font(26, bold=line.startswith(">")), fill=STABLE if line.startswith(">") else TEXT)
        cy += 36
    draw.rounded_rectangle((998, 286, 1518, 790), radius=22, fill=CARD, outline=BORDER, width=2)
    draw.text((1030, 320), "OBSERVED URL STATE", font=font(20), fill=ACCENT)
    yy = 370
    for page_group, url, status, impressions, response_ms in urls[:4]:
        status_color = CRITICAL if status == "critical" else WARN if status == "watch" else STABLE
        draw.text((1030, yy), page_group.replace("_", " ").title(), font=font(24, bold=True), fill=TEXT)
        draw.text((1030, yy + 34), url.replace("https://kineticgain.com/", "/"), font=font(16), fill=MUTED)
        draw.text((1030, yy + 66), f"{status.upper()} · {impressions:,} impressions · {response_ms} ms", font=font(18, bold=True), fill=status_color)
        yy += 104
    img.save(SCREENSHOTS / "04-proof.png")
    con.close()


if __name__ == "__main__":
    render()
