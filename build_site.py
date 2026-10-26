"""Build the static drag-calculator site from pseo_pages_list.csv.

The CSV is the source of truth. This script reads it and never writes it.
"""
import csv
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(ROOT, "pseo_pages_list.csv")
ORIGIN = "https://dragcalculators.com"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9.]+)*$")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

COLUMNS = [
    "slug",
    "target_keyword",
    "category",
    "role",
    "nav_label",
    "transmission",
    "rear_gear",
    "tire_diameter",
    "rpm",
    "hp",
    "boost",
    "fuel",
    "turbo_count",
    "crank_pulley",
    "blower_pulley",
    "blower_type",
    "growth",
]
NUMERIC_FIELDS = [
    "rear_gear",
    "tire_diameter",
    "rpm",
    "hp",
    "boost",
    "crank_pulley",
    "blower_pulley",
    "growth",
]
CATEGORY_FIELDS = {
    "Transmission": ["transmission", "rear_gear", "tire_diameter", "rpm"],
    "Turbo": ["hp", "boost", "fuel", "turbo_count"],
    "Suspension": [],
    "Exhaust": ["hp"],
    "Supercharger": ["blower_type", "crank_pulley", "blower_pulley", "boost", "rpm"],
    "RearGear": ["rear_gear", "tire_diameter"],
    "Tire": ["tire_diameter", "rear_gear", "growth"],
    "Wastegate": ["hp", "boost"],
    "Fuel": ["hp", "fuel"],
    "Electrical": [],
    "CAS": ["boost"],
}
FUELS = {"gasoline", "e85", "methanol"}
BLOWER_TYPES = {"roots", "twin-screw", "centrifugal"}

TRANSMISSIONS = {
    "th400": ("TH400 / 4L80E (2.48 / 1.48 / 1.00)", [2.48, 1.48, 1.00]),
    "powerglide": ("Powerglide (1.76 / 1.00)", [1.76, 1.00]),
    "th350": ("TH350 (2.52 / 1.52 / 1.00)", [2.52, 1.52, 1.00]),
    "4l60e": ("4L60E / 4L70E (3.06 / 1.62 / 1.00 / 0.70)", [3.06, 1.62, 1.00, 0.70]),
    "6l80": ("6L80 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67)", [4.027, 2.364, 1.532, 1.152, 0.852, 0.667]),
    "8l90": ("8L90 (4.56 / 2.97 / 2.08 / 1.69 / 1.27 / 1.00 / 0.85 / 0.65)", [4.56, 2.97, 2.08, 1.69, 1.27, 1.00, 0.85, 0.65]),
    "c4": ("C4 (2.46 / 1.46 / 1.00)", [2.46, 1.46, 1.00]),
    "c6": ("C6 (2.46 / 1.46 / 1.00)", [2.46, 1.46, 1.00]),
    "aod": ("AOD (2.40 / 1.47 / 1.00 / 0.67)", [2.40, 1.47, 1.00, 0.67]),
    "4r70w": ("4R70W (2.84 / 1.55 / 1.00 / 0.70)", [2.84, 1.55, 1.00, 0.70]),
    "10r80": (
        "10R80 (4.70 / 2.99 / 2.15 / 1.77 / 1.52 / 1.28 / 1.00 / 0.85 / 0.69 / 0.64)",
        [4.696, 2.985, 2.146, 1.769, 1.520, 1.275, 1.000, 0.854, 0.689, 0.636],
    ),
    "727": ("Torqueflite 727 (2.45 / 1.45 / 1.00)", [2.45, 1.45, 1.00]),
    "904": ("Torqueflite 904 (2.74 / 1.54 / 1.00)", [2.74, 1.54, 1.00]),
    "zf8hp": (
        "8HP70 / 8HP90 (4.71 / 3.14 / 2.11 / 1.67 / 1.29 / 1.00 / 0.84 / 0.67)",
        [4.714, 3.143, 2.106, 1.667, 1.285, 1.000, 0.839, 0.667],
    ),
    "t56": ("Tremec T56 / Magnum (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50)", [2.66, 1.78, 1.30, 1.00, 0.74, 0.50]),
    "tr6060": ("Tremec TR-6060 (2.66 / 1.78 / 1.30 / 1.00 / 0.80 / 0.63)", [2.66, 1.78, 1.30, 1.00, 0.80, 0.63]),
    "tkx": ("Tremec TKX (2.87 / 1.89 / 1.28 / 1.00 / 0.81)", [2.87, 1.89, 1.28, 1.00, 0.81]),
    "jerico": ("Jerico 4-speed / Liberty (1.80 / 1.40 / 1.16 / 1.00)", [1.80, 1.40, 1.16, 1.00]),
    "bmwzf5": ("BMW ZF 5-speed (4.20 / 2.49 / 1.66 / 1.24 / 1.00)", [4.20, 2.49, 1.66, 1.24, 1.00]),
    "bmwzf6": ("BMW ZF 6-speed (4.23 / 2.53 / 1.67 / 1.23 / 1.00 / 0.83)", [4.23, 2.53, 1.67, 1.23, 1.00, 0.83]),
}
TRANSMISSION_GROUPS = [
    ("GM Automatic", ["th400", "powerglide", "th350", "4l60e", "6l80", "8l90"]),
    ("Ford Automatic", ["c4", "c6", "aod", "4r70w", "10r80"]),
    ("Chrysler / Mopar Automatic", ["727", "904", "zf8hp"]),
    ("Manual", ["t56", "tr6060", "tkx", "jerico", "bmwzf5", "bmwzf6"]),
]
TRANS_SHORT = {
    "th400": "TH400",
    "powerglide": "Powerglide (2-Speed)",
    "th350": "TH350",
    "4l60e": "4L60E",
    "6l80": "6L80",
    "8l90": "8L90",
    "c4": "Ford C4",
    "c6": "Ford C6",
    "aod": "AOD",
    "4r70w": "4R70W",
    "10r80": "10R80",
    "727": "Torqueflite 727",
    "904": "Torqueflite 904",
    "zf8hp": "8HP70 / 8HP90",
    "t56": "Tremec T56",
    "tr6060": "TR-6060",
    "tkx": "Tremec TKX",
    "jerico": "Jerico / Liberty",
    "bmwzf5": "BMW ZF 5-speed",
    "bmwzf6": "BMW ZF 6-speed",
}
FUEL_LABEL = {"gasoline": "gasoline", "e85": "E85", "methanol": "methanol"}
BLOWER_LABEL = {
    "roots": "roots blower",
    "twin-screw": "twin-screw blower",
    "centrifugal": "centrifugal blower",
}
TURBO_FUELS = [
    ("gasoline", "Gasoline (91/93)"),
    ("e85", "E85"),
    ("methanol", "Methanol"),
    ("race", "Race gas"),
    ("diesel", "Diesel"),
]
INJECTOR_FUELS = [
    ("gasoline", "Gasoline (91/93)"),
    ("e85", "E85"),
    ("methanol", "Methanol"),
    ("race", "Race gas"),
    ("diesel", "Diesel"),
]
BLOWER_OPTIONS = [
    ("roots", "1.20", "Roots (~1.20)"),
    ("twin-screw", "1.45", "Twin-Screw (~1.45)"),
    ("centrifugal", "1.65", "Centrifugal (~1.65)"),
]

VERIFICATION = (
    '    <meta name="impact-site-verification" value="b2bb3042-cfc7-4ed4-b783-57a9b5a6451f">\n'
    '    <meta name="google-site-verification" content="google9e7c88791a3f2f72">'
)

STYLES = """:root {
    --bg-dark: #121212;
    --card-bg: #1c1c1c;
    --panel: #181818;
    --accent-red: #e50914;
    --text-main: #f5f5f5;
    --text-muted: #a3a3a3;
    --border-color: #2e2e2e;
    --input-bg: #141414;
    --ok: #d6d6d6;
}
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg-dark);
    color: var(--text-main);
    margin: 0;
    padding: 20px;
    line-height: 1.5;
}
.back-row { max-width: 1350px; margin: 0 auto; }
.back-link { color: var(--accent-red); font-weight: 700; font-size: 0.85rem; text-decoration: none; }
.layout-grid {
    max-width: 1350px;
    margin: 16px auto 0;
    display: grid;
    grid-template-columns: 240px minmax(340px, 520px) 1fr;
    gap: 25px;
    align-items: start;
}
.nexus-sidebar {
    position: sticky;
    top: 20px;
    max-height: 90vh;
    overflow: auto;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px;
}
.nav-list { display: flex; flex-direction: column; gap: 4px; }
.nav-item {
    display: block;
    padding: 9px 12px;
    color: var(--text-muted);
    text-decoration: none;
    border-radius: 6px;
    font-size: 0.78rem;
    border: 1px solid transparent;
}
.nav-item.active {
    background: var(--accent-red);
    border-color: var(--accent-red);
    color: #fff;
    font-weight: 700;
}
.nav-item:hover { background: #242424; color: var(--text-main); }
.nav-item.active:hover { background: var(--accent-red); color: #fff; }
.sticky-calculator, .content-box, .narrow-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 22px;
}
.sticky-calculator { display: flex; flex-direction: column; gap: 15px; }
.content-column { display: flex; flex-direction: column; gap: 20px; }
.content-box h2 {
    color: var(--accent-red);
    font-size: 0.95rem;
    text-transform: uppercase;
    margin: 0 0 8px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
}
.master-header { text-align: center; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
.master-header h1 {
    color: var(--text-main);
    font-size: 1.15rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 0 6px;
}
.spec, .content-box p, .narrow-card p { color: var(--text-muted); font-size: 0.9rem; }
.spec { font-size: 0.82rem; margin: 0; }
.field-stack { display: flex; flex-direction: column; gap: 14px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-items: end; }
.field { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.field-hint { margin: 0; color: var(--text-muted); font-size: 0.75rem; }
label { display: block; margin: 0; font-weight: 650; font-size: 0.72rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); }
input, select, textarea {
    width: 100%;
    height: 42px;
    padding: 0 12px;
    background: var(--input-bg);
    border: 1px solid #3a3a3a;
    color: var(--text-main);
    border-radius: 8px;
    font-size: 0.92rem;
    font-family: inherit;
}
textarea { height: auto; min-height: 120px; padding: 10px 12px; resize: vertical; }
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--accent-red); }
input:disabled { opacity: 0.65; }
input[type="range"] {
    height: 22px;
    padding: 0;
    border: 0;
    background: transparent;
    accent-color: var(--accent-red);
}
.narrow-card form > div { margin-bottom: 14px; }
.accordion {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--panel);
}
.accordion summary {
    cursor: pointer;
    padding: 12px 14px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    list-style: none;
}
.accordion summary::-webkit-details-marker { display: none; }
.accordion summary::after { content: "+"; float: right; color: var(--accent-red); font-size: 1rem; line-height: 1; }
.accordion[open] summary::after { content: "–"; }
.accordion[open] summary { color: #fff; }
.accordion-body { padding: 0 14px 14px; }
.readout {
    background: #161616;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
}
.readout-top { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }
.readout-kicker, .readout-label {
    color: var(--text-muted);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.readout-value {
    margin-top: 4px;
    font-size: 2.5rem;
    line-height: 1;
    font-weight: 750;
    letter-spacing: -0.03em;
    color: var(--accent-red);
}
.readout-suffix { margin-left: 8px; font-size: 1rem; font-weight: 650; color: var(--text-main); letter-spacing: 0; }
.readout-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 16px;
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid var(--border-color);
}
.readout-extra span { display: block; color: var(--text-muted); font-size: 0.68rem; letter-spacing: 0.04em; text-transform: uppercase; }
.readout-extra strong { display: block; margin-top: 2px; font-size: 0.95rem; font-weight: 650; color: var(--text-main); }
.duty-card, .assess, .table-scroll {
    background: #161616;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 14px;
}
.duty-head { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; color: var(--text-muted); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }
.duty-head strong { font-size: 1.05rem; letter-spacing: 0; text-transform: none; }
.duty-track { height: 10px; margin-top: 10px; border-radius: 999px; background: #2a2a2a; overflow: hidden; }
.duty-fill { height: 100%; width: 0; border-radius: 999px; background: #3dd68c; }
.duty-scale { display: flex; justify-content: space-between; margin-top: 6px; color: #6f6f6f; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.04em; }
.assess { color: var(--text-main); font-size: 0.88rem; }
.assess strong { color: #fff; }
.table-scroll { overflow-x: auto; padding: 8px; }
.size-sub { color: var(--text-muted); font-size: 0.68rem; margin-top: 2px; }
tr.is-rec td { background: rgba(229, 9, 20, 0.14); }
tr.is-small td { color: #8d8d8d; }
.badge { display: inline-block; padding: 2px 6px; border-radius: 999px; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
.badge-rec { background: var(--accent-red); color: #fff; }
.badge-ok { background: rgba(61, 214, 140, 0.16); color: #3dd68c; }
.badge-tight { background: rgba(245, 165, 36, 0.16); color: #f5a524; }
.badge-no { background: #2a2a2a; color: #8d8d8d; }
.tone-ok { color: #3dd68c; }
.tone-tight { color: #f5a524; }
.tone-over { color: var(--accent-red); }
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; }
.pill-group { display: inline-flex; border: 1px solid #3a3a3a; border-radius: 999px; overflow: hidden; background: #141414; }
.pill {
    border: 0;
    background: transparent;
    color: var(--text-muted);
    padding: 6px 12px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    cursor: pointer;
    font-family: inherit;
}
.pill.active { background: var(--accent-red); color: #fff; }
.action-btn {
    width: 100%;
    margin-top: 0;
    background: var(--accent-red);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    cursor: pointer;
    text-transform: uppercase;
}
.action-btn:hover { background: #c40812; }
table { width: 100%; margin-top: 4px; border-collapse: collapse; background: #161616; }
th, td { padding: 7px 4px; border: 1px solid var(--border-color); text-align: center; font-size: 0.72rem; }
th { background: #202020; color: var(--accent-red); text-transform: uppercase; font-size: 0.62rem; }
.formula {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    color: var(--ok);
    font-size: 0.82rem;
    background: var(--input-bg);
    padding: 10px;
    border-radius: 6px;
    margin: 0;
}
.variant-list { list-style: none; padding: 0; margin: 0; }
.variant-list a {
    display: block;
    padding: 6px 0;
    border-bottom: 1px dashed var(--border-color);
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.82rem;
}
.variant-list a:hover { color: var(--text-main); }
.config-drawer { background: var(--card-bg); }
.config-drawer summary { color: var(--text-muted); }
.config-scroll { max-height: 160px; overflow: auto; padding-right: 6px; }
.config-scroll::-webkit-scrollbar { width: 8px; }
.config-scroll::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 8px; }
.config-scroll .variant-list a { font-size: 0.78rem; padding: 5px 0; }
.cheat-list { margin: 0 0 14px; padding-left: 18px; color: var(--text-muted); font-size: 0.84rem; }
.cheat-list li { margin: 0 0 6px; }
.faq-item { margin: 0 0 12px; }
.faq-item h3 { margin: 0 0 3px; font-size: 0.84rem; color: var(--text-main); font-weight: 650; }
.faq-item p { margin: 0; }
.site-footer {
    max-width: 1350px;
    margin: 40px auto 20px;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
}
.site-footer a { color: var(--text-muted); text-decoration: none; }
.site-footer a.accent { color: var(--accent-red); font-weight: 700; }
.narrow { max-width: 720px; margin: 20px auto; }
.narrow-card h1 { color: var(--text-main); font-size: 1.3rem; text-transform: uppercase; margin-top: 0; }
.narrow-card h2 {
    color: var(--text-main);
    font-size: 1.05rem;
    margin-top: 25px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
}
.tool-note { font-size: 0.75rem; color: var(--text-muted); text-align: center; margin: 0 0 8px; }
.sponsor a { color: var(--accent-red); font-weight: 700; text-decoration: none; }
@media (max-width: 1100px) {
    .layout-grid { grid-template-columns: 1fr; }
    .nexus-sidebar { position: static; max-height: none; }
}
@media (max-width: 700px) {
    body { padding: 12px; }
    .grid-2, .readout-grid { grid-template-columns: 1fr; }
    .sticky-calculator, .content-box, .narrow-card { padding: 16px; }
    .readout-value { font-size: 2rem; }
}
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <meta name="description" content="{{DESCRIPTION}}">
    <link rel="canonical" href="{{CANONICAL}}">
{{VERIFICATION}}
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{CANONICAL}}">
    <meta property="og:title" content="{{TITLE}}">
    <meta property="og:description" content="{{DESCRIPTION}}">
    <meta property="og:image" content="{{ORIGIN}}/social-banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{TITLE}}">
    <meta name="twitter:description" content="{{DESCRIPTION}}">
    <meta name="twitter:image" content="{{ORIGIN}}/social-banner.jpg">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {{BACK_ROW}}
    <div class="layout-grid">
        <aside class="nexus-sidebar">{{SIDEBAR}}</aside>
        <section class="sticky-calculator">
            <header class="master-header">
                <h1>{{H1}}</h1>
                {{SPEC}}
            </header>
            {{TOOL}}
        </section>
        <div class="content-column">
            {{CONTENT}}
        </div>
    </div>
    {{FOOTER}}
    <script>
{{SCRIPT}}
    </script>
</body>
</html>
"""

NARROW_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <meta name="description" content="{{DESCRIPTION}}">
    <link rel="canonical" href="{{CANONICAL}}">
{{VERIFICATION}}
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{CANONICAL}}">
    <meta property="og:title" content="{{TITLE}}">
    <meta property="og:description" content="{{DESCRIPTION}}">
    <meta property="og:image" content="{{ORIGIN}}/social-banner.jpg">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="narrow">
        <a href="index.html" class="back-link">&larr; Back to Master Hub</a>
        <article class="narrow-card">
            {{CONTENT}}
        </article>
    </div>
    {{FOOTER}}
</body>
</html>
"""


def esc(value):
    return html.escape(str(value), quote=True)


def fill(template, **tokens):
    def replace(match):
        key = match.group(1)
        if key not in tokens:
            raise SystemExit(f"Missing template token {key}")
        return tokens[key]

    return TOKEN_RE.sub(replace, template)


def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    return path


def cell(row, key):
    return (row.get(key) or "").strip()


def field(row, key, default):
    value = cell(row, key)
    return value if value else default


def fail(slug, message):
    raise SystemExit(f"{slug}: {message}")


def load_pages(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("pseo_pages_list.csv is missing a header row")
        missing = [column for column in ("slug", "target_keyword", "category") if column not in reader.fieldnames]
        if missing:
            raise SystemExit("pseo_pages_list.csv is missing columns: " + ", ".join(missing))
        pages = []
        seen = set()
        hub_categories = {}
        for raw in reader:
            page = {column: (raw.get(column) or "").strip() for column in COLUMNS}
            slug = page["slug"]
            if not slug or not SLUG_RE.fullmatch(slug):
                fail(slug or "(blank)", "slug must be lowercase letters, numbers, dots, and hyphens")
            if slug in seen:
                fail(slug, "duplicate slug")
            seen.add(slug)
            if not page["target_keyword"]:
                fail(slug, "target_keyword is required")
            if page["category"] not in CATEGORY_FIELDS:
                fail(slug, f"unknown category {page['category']!r}")
            if page["role"] not in ("hub", "variant"):
                fail(slug, "role must be hub or variant")
            if page["role"] == "hub":
                if not page["nav_label"]:
                    fail(slug, "hub rows need nav_label")
                if page["category"] in hub_categories:
                    fail(slug, f"category {page['category']} already has hub {hub_categories[page['category']]}")
                hub_categories[page["category"]] = slug
            elif page["nav_label"]:
                fail(slug, "nav_label is only for hub rows")
            for key in NUMERIC_FIELDS:
                value = page[key]
                if value and not NUMBER_RE.fullmatch(value):
                    fail(slug, f"{key} must be a positive number, got {value!r}")
                if value and float(value) <= 0:
                    fail(slug, f"{key} must be greater than zero")
            if page["transmission"] and page["transmission"] not in TRANSMISSIONS:
                fail(slug, f"unknown transmission {page['transmission']!r}")
            if page["fuel"] and page["fuel"] not in FUELS:
                fail(slug, f"unknown fuel {page['fuel']!r}")
            if page["turbo_count"] and page["turbo_count"] not in {"1", "2"}:
                fail(slug, "turbo_count must be 1 or 2")
            if page["blower_type"] and page["blower_type"] not in BLOWER_TYPES:
                fail(slug, f"unknown blower_type {page['blower_type']!r}")
            pages.append(page)
    if not pages:
        raise SystemExit("pseo_pages_list.csv has no pages")
    return pages


def spec_text(row):
    parts = []
    for key in CATEGORY_FIELDS[row["category"]]:
        value = cell(row, key)
        if not value:
            continue
        if key == "transmission":
            parts.append(TRANS_SHORT[value])
        elif key == "rear_gear":
            parts.append(f"{value} rear gear")
        elif key == "tire_diameter":
            parts.append(f"{value} inch tire")
        elif key == "rpm":
            parts.append(f"{value} RPM shift point")
        elif key == "hp":
            parts.append(f"{value} HP")
        elif key == "boost":
            parts.append(f"{value} PSI boost")
        elif key == "fuel":
            parts.append(FUEL_LABEL[value])
        elif key == "turbo_count":
            parts.append("twin turbo" if value == "2" else "single turbo")
        elif key == "crank_pulley":
            parts.append(f"{value} inch crank pulley")
        elif key == "blower_pulley":
            parts.append(f"{value} inch blower pulley")
        elif key == "blower_type":
            parts.append(BLOWER_LABEL[value])
        elif key == "growth":
            parts.append(f"{value}% growth estimate")
    if not parts:
        return ""
    return "Loaded defaults: " + ", ".join(parts) + "."


def description(row):
    spec = spec_text(row)
    keyword = row["target_keyword"].rstrip(".")
    if spec:
        return f"{keyword}. {spec}"
    return f"{keyword}. Adjust the inputs to calculate this combination."


def options(choices, current):
    parts = []
    for value, label in choices:
        selected = " selected" if value == current else ""
        parts.append(f'<option value="{esc(value)}"{selected}>{esc(label)}</option>')
    return "\n".join(parts)


UI_SCRIPT = r"""
const unitState = { power: "bhp", system: "imperial" };
let lastReadout = [];

function crankHorsepower(raw) {
    const hp = parseFloat(raw);
    const entered = Number.isFinite(hp) ? hp : 0;
    if (unitState.power !== "whp") return entered;
    const lossInput = document.getElementById("dt-loss");
    const lossPct = lossInput ? parseFloat(lossInput.value) : 15;
    const loss = Math.min(0.4, Math.max(0, (Number.isFinite(lossPct) ? lossPct : 15) / 100));
    return entered / Math.max(0.05, 1 - loss);
}

function formatUnit(value, unit) {
    const metric = unitState.system === "metric";
    const n = Number(value);
    if (unit === "text") return { text: String(value), suffix: "" };
    if (!Number.isFinite(n)) return { text: "—", suffix: "" };
    switch (unit) {
        case "mph":
            return metric ? { text: (n * 1.60934).toFixed(1), suffix: "km/h" } : { text: n.toFixed(1), suffix: "MPH" };
        case "in":
            return metric ? { text: (n * 25.4).toFixed(1), suffix: "mm" } : { text: n.toFixed(1), suffix: "in" };
        case "psi":
            return metric ? { text: (n * 0.0689476).toFixed(2), suffix: "bar" } : { text: n.toFixed(1), suffix: "PSI" };
        case "lbmin":
            return metric ? { text: (n * 0.453592).toFixed(2), suffix: "kg/min" } : { text: n.toFixed(1), suffix: "lb/min" };
        case "cfm":
            return metric ? { text: (n * 0.0283168).toFixed(2), suffix: "m3/min" } : { text: Math.round(n).toLocaleString("en-US"), suffix: "CFM" };
        case "tempf":
            return metric ? { text: ((n - 32) * 5 / 9).toFixed(0), suffix: "C" } : { text: Math.round(n).toString(), suffix: "F" };
        case "lbhr":
            return metric ? { text: (n * 0.453592).toFixed(1), suffix: "kg/h" } : { text: n.toFixed(1), suffix: "lb/hr" };
        case "ft":
            return metric ? { text: (n * 0.3048).toFixed(2), suffix: "m" } : { text: n.toFixed(1), suffix: "ft" };
        case "rpm":
            return { text: Math.round(n).toLocaleString("en-US"), suffix: "RPM" };
        case "ratio":
            return { text: n.toFixed(2), suffix: ":1" };
        case "sec":
            return { text: n.toFixed(2), suffix: "s" };
        case "pct":
            return { text: Math.round(n).toString(), suffix: "%" };
        case "pct1":
            return { text: n.toFixed(1), suffix: "%" };
        case "cc":
            return { text: Math.round(n).toLocaleString("en-US"), suffix: "cc/min" };
        case "gph":
            return metric ? { text: (n * 3.78541).toFixed(1), suffix: "L/h" } : { text: n.toFixed(1), suffix: "gal/hr" };
        case "amp":
            return { text: n.toFixed(1), suffix: "A" };
        case "mm":
            return { text: String(Math.round(n)), suffix: "mm" };
        case "awg":
            return { text: String(value), suffix: "AWG" };
        default:
            return { text: String(value), suffix: unit || "" };
    }
}

function joinReading(shown) {
    if (!shown.suffix) return shown.text;
    if (shown.suffix.charAt(0) === ":") return shown.text + shown.suffix;
    return shown.text + " " + shown.suffix;
}

function reading(value, unit) {
    return joinReading(formatUnit(value, unit));
}

function publishReadout(items) {
    lastReadout = items;
    const body = document.getElementById("readout-body");
    if (!body || !items.length) return;
    const primary = items.find(item => item.primary) || items[0];
    const rest = items.filter(item => item !== primary);
    const main = formatUnit(primary.value, primary.unit);
    const extras = rest.map(item => {
        return '<div class="readout-extra"><span>' + item.label + '</span><strong>' + reading(item.value, item.unit) + '</strong></div>';
    }).join("");
    body.innerHTML = '<div class="readout-label">' + primary.label + '</div>'
        + '<div class="readout-value">' + main.text + (main.suffix ? '<span class="readout-suffix">' + main.suffix + '</span>' : '') + '</div>'
        + (extras ? '<div class="readout-grid">' + extras + '</div>' : '');
}

function bindCalc(fn, ids) {
    window.refreshCalc = fn;
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener("input", fn);
        el.addEventListener("change", fn);
    });
    fn();
}

document.querySelectorAll(".pill").forEach(button => {
    button.addEventListener("click", () => {
        if (!button.dataset.unitGroup) return;
        unitState[button.dataset.unitGroup] = button.dataset.unit;
        button.parentElement.querySelectorAll(".pill").forEach(pill => {
            pill.classList.toggle("active", pill === button);
        });
        if (typeof window.refreshCalc === "function") window.refreshCalc();
        else if (lastReadout.length) publishReadout(lastReadout);
    });
});
"""

LOSS_FIELDS = """
<p class="field-hint">BHP uses the power entry as flywheel power. WHP treats it as wheel power and converts with this drivetrain loss.</p>
<div class="grid-2">
    <div class="field"><label for="dt-loss">Drivetrain loss (%)</label><input type="number" id="dt-loss" value="15" min="0" max="40" step="1"></div>
</div>
"""


def calculator_shell(primary, advanced, print_label, extra="", power_toggle=False, results_extra=""):
    power = ""
    if power_toggle:
        power = """
                <div class="pill-group" role="group" aria-label="Power unit">
                    <button type="button" class="pill" data-unit-group="power" data-unit="whp">WHP</button>
                    <button type="button" class="pill active" data-unit-group="power" data-unit="bhp">BHP</button>
                </div>"""
    return f"""
    <div class="field-stack">{primary}</div>
    <details class="accordion">
        <summary>Advanced / Conditions</summary>
        <div class="accordion-body field-stack">{advanced}</div>
    </details>
    <div class="readout" id="results">
        <div class="readout-top">
            <span class="readout-kicker">Result</span>
            <div class="pill-row">{power}
                <div class="pill-group" role="group" aria-label="Units">
                    <button type="button" class="pill active" data-unit-group="system" data-unit="imperial">Imperial</button>
                    <button type="button" class="pill" data-unit-group="system" data-unit="metric">Metric</button>
                </div>
            </div>
        </div>
        <div id="readout-body"></div>
    </div>
    {results_extra}
    <button type="button" class="action-btn" onclick="window.print()">{esc(print_label)}</button>
    {extra}
"""


def transmission_html(row):
    current = field(row, "transmission", "th400")
    groups = ['<option value="custom">Custom ratios</option>']
    for label, keys in TRANSMISSION_GROUPS:
        opts = options([(key, TRANSMISSIONS[key][0]) for key in keys], current)
        groups.append(f'<optgroup label="{esc(label)}">\n{opts}\n</optgroup>')
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="trans">Transmission</label><select id="trans">{''.join(groups)}</select></div>
        <div class="field"><label for="rear-gear">Rear gear</label><input type="number" id="rear-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="custom-ratios">Custom ratios</label><input type="text" id="custom-ratios" placeholder="2.48, 1.48, 1.00" inputmode="decimal" autocomplete="off"></div>
        <div class="field"><label for="converter-slip">Converter slip (%)</label><input type="number" id="converter-slip" value="0" min="0" max="40" step="0.5"></div>
    </div>
    <p class="field-hint">Type a ratio list to switch to Custom ratios. Leave slip at 0% for a manual or a locked converter. 5% to 8% is a typical loose converter at the shift.</p>
    <div class="grid-2">
        <div class="field"><label for="tire-dia">Tire diameter (in)</label><input type="number" id="tire-dia" value="{esc(field(row, 'tire_diameter', '28.0'))}" step="0.1"></div>
        <div class="field"><label for="max-rpm">Shift RPM</label><input type="number" id="max-rpm" value="{esc(field(row, 'rpm', '7500'))}" step="100"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="veh-wt">Vehicle weight (lb)</label><input type="number" id="veh-wt" value="3200" step="50"></div>
        <div class="field"><label for="veh-hp">Power</label><input type="number" id="veh-hp" value="{esc(field(row, 'hp', '1100'))}" step="25"></div>
    </div>
    {LOSS_FIELDS}
    """
    table = """
    <table>
        <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift speed</th><th>RPM drop</th></tr></thead>
        <tbody id="gear-body"></tbody>
    </table>
    """
    return calculator_shell(primary, advanced, "Print track sheet", table, power_toggle=True)


DRIVETRAIN_SCRIPT = """
const ratios = %%RATIOS%%;
function parseRatios(text) {
    return String(text || "").split(/[^0-9.]+/).map(parseFloat).filter(function (n) {
        return Number.isFinite(n) && n > 0 && n < 12;
    }).slice(0, 10);
}
function calcAll() {
    const transEl = document.getElementById("trans");
    const customEl = document.getElementById("custom-ratios");
    const typed = parseRatios(customEl.value);
    if (document.activeElement === customEl && typed.length) transEl.value = "custom";
    let rat = ratios[transEl.value] || [2.48, 1.48, 1.00];
    if (transEl.value === "custom") rat = typed.length ? typed : [2.48, 1.48, 1.00];
    let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
    let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
    let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
    let slip = parseFloat(document.getElementById("converter-slip").value);
    if (!Number.isFinite(slip)) slip = 0;
    slip = Math.min(40, Math.max(0, slip)) / 100;
    const drive = 1 - slip;
    let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
    let hp = crankHorsepower(document.getElementById("veh-hp").value || 1100);
    let rollout = tire * Math.PI;
    let estEt = 5.825 * Math.pow(wt / Math.max(hp, 1), 0.333);
    let estTrap = 234 * Math.cbrt(hp / Math.max(wt, 1));
    let firstOverall = rat[0] * gear;
    let firstSpeed = (rpm * drive * tire) / (firstOverall * 336);
    let finishOverall = rat[rat.length - 1] * gear;
    let finishRpm = (estTrap * finishOverall * 336) / (tire * drive);
    publishReadout([
        { label: "Quarter-mile ET", value: estEt, unit: "sec", primary: true },
        { label: "Trap speed", value: estTrap, unit: "mph" },
        { label: "1st gear shift speed", value: firstSpeed, unit: "mph" },
        { label: "Finish RPM", value: Math.round(finishRpm) + " RPM", unit: "text" },
        { label: "Rollout", value: rollout, unit: "in" },
        { label: "1st gear overall", value: firstOverall, unit: "ratio" }
    ]);
    let tbody = document.getElementById("gear-body");
    if (tbody) {
        tbody.innerHTML = "";
        for (let i = 0; i < rat.length; i++) {
            let overall = rat[i] * gear;
            let speed = (rpm * drive * tire) / (overall * 336);
            let trapRpm = Math.round((estTrap * overall * 336) / (tire * drive));
            let drop = i < rat.length - 1
                ? "Drop to " + Math.round(rpm * drive * (rat[i + 1] / rat[i])) + " RPM"
                : "Finish: " + trapRpm + " RPM";
            tbody.innerHTML += "<tr><td>Gear " + (i + 1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + reading(speed, "mph") + "</td><td>" + drop + "</td></tr>";
        }
    }
}
bindCalc(calcAll, ["trans", "custom-ratios", "converter-slip", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp", "dt-loss"]);
""".replace(
    "%%RATIOS%%",
    json.dumps({key: ratios for key, (_label, ratios) in TRANSMISSIONS.items()}),
)


def turbo_html(row):
    fuel = field(row, "fuel", "e85")
    count = field(row, "turbo_count", "1")
    fuel_options = options(TURBO_FUELS, fuel)
    count_options = options([("1", "Single"), ("2", "Twin")], count)
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="tu-hp">Target power</label><input type="number" id="tu-hp" value="{esc(field(row, 'hp', '1000'))}" min="50" step="25"></div>
        <div class="field"><label for="tu-boost">Target boost (PSI)</label><input type="number" id="tu-boost" value="{esc(field(row, 'boost', '22'))}" min="0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div class="field">
            <label for="tu-disp">Displacement</label>
            <input type="number" id="tu-disp" value="364" min="30" step="1">
            <div class="pill-group" role="group" aria-label="Displacement unit">
                <button type="button" class="pill disp-unit active" data-disp="ci">CID</button>
                <button type="button" class="pill disp-unit" data-disp="l">Liters</button>
            </div>
        </div>
        <div class="field"><label for="tu-rpm">Peak power RPM</label><input type="number" id="tu-rpm" value="{esc(field(row, 'rpm', '6500'))}" min="2000" step="100"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="tu-fuel">Fuel</label><select id="tu-fuel">{fuel_options}</select></div>
        <div class="field"><label for="tu-count">Turbo count</label><select id="tu-count">{count_options}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="tu-valve">Valvetrain</label>
            <select id="tu-valve">
                <option value="ohv" selected>OHV / pushrod</option>
                <option value="sohc">SOHC</option>
                <option value="dohc">DOHC</option>
                <option value="race">Race 4-valve</option>
            </select>
        </div>
        <div class="field"><label for="tu-app">Use</label>
            <select id="tu-app">
                <option value="street">Street</option>
                <option value="strip">Street-strip</option>
                <option value="drag" selected>Drag racing</option>
            </select>
        </div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="tu-baro">Barometer (PSI)</label><input type="number" id="tu-baro" value="14.7" min="10" max="15.5" step="0.1"></div>
        <div class="field"><label for="tu-temp">Ambient temp (F)</label><input type="number" id="tu-temp" value="75" min="-20" max="120" step="1"></div>
    </div>
    <div class="field"><label for="tu-bsfc">Custom BSFC</label><input type="number" id="tu-bsfc" placeholder="Auto" min="0.2" max="2" step="0.01"></div>
    <div class="grid-2">
        <div class="field"><label for="tu-ic">Intercooler</label>
            <select id="tu-ic">
                <option value="0">None</option>
                <option value="65">Air-to-air, small</option>
                <option value="75">Air-to-air, standard</option>
                <option value="82" selected>Air-to-air, large</option>
                <option value="90">Water-to-air / ice box</option>
            </select>
        </div>
        <div class="field"><label for="tu-ce">Compressor efficiency (%)</label>
            <select id="tu-ce">
                <option value="65">65, off the island</option>
                <option value="72" selected>72, matched modern turbo</option>
                <option value="76">76, efficient island</option>
                <option value="80">80, peak island</option>
            </select>
        </div>
    </div>
    <p class="field-hint">Volumetric efficiency starts from the valvetrain and the use. Lower the barometer for elevation. Compressor temperature is calculated from the target boost.</p>
    {LOSS_FIELDS}
    """
    results = """
    <div class="duty-card">
        <div class="duty-head"><span>Compressor class</span><strong id="tu-class">—</strong></div>
        <p class="field-hint" id="tu-class-desc"></p>
    </div>
    <p class="assess" id="tu-assess"></p>
    <p class="assess" id="tu-thermal"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Point</th><th>RPM</th><th>NA flow</th><th>At your boost</th></tr></thead>
            <tbody id="tu-rpm-rows"></tbody>
        </table>
        <p class="field-hint">Flow at your boost assumes the same volumetric efficiency from spool to peak. Match the per-turbo number to the compressor map at the pressure ratio.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print turbo match sheet", power_toggle=True, results_extra=results)


TURBO_SCRIPT = r"""
const TURBO_FUEL = {
    gasoline: { bsfc: 0.55, afr: 11.8 },
    e85: { bsfc: 0.78, afr: 8.8 },
    methanol: { bsfc: 1.20, afr: 5.2 },
    race: { bsfc: 0.58, afr: 11.5 },
    diesel: { bsfc: 0.40, afr: 18.0 }
};
const VE_BASE = { ohv: 78, sohc: 85, dohc: 93, race: 100 };
const VE_USE = { street: 0, strip: 4, drag: 8 };
const CID_PER_LITER = 61.024;
let dispUnit = "ci";

function airDensity(baro, ambientF) {
    const rankine = ambientF + 459.67;
    return (baro * 144) / (53.3 * rankine);
}

function sizeBand(flow) {
    if (flow < 13) return ["Micro", "Under 13 lb/min. Small three- and four-cylinder engines."];
    if (flow < 22) return ["Small", "13–22 lb/min. Compact street engines."];
    if (flow < 36) return ["Medium", "22–36 lb/min. A common street turbo class."];
    if (flow < 52) return ["Large", "36–52 lb/min. High-output street and street-strip."];
    if (flow < 72) return ["XL", "52–72 lb/min. Serious power from each compressor."];
    if (flow < 95) return ["XXL", "72–95 lb/min. The top of a catalog compressor."];
    return ["Race", "Over 95 lb/min. Match the wheel on a compressor map. A class label is not enough."];
}

function inducerRange(flow) {
    if (flow < 25) return "40–50 mm";
    if (flow < 40) return "50–60 mm";
    if (flow < 55) return "60–67 mm";
    if (flow < 75) return "70–76 mm";
    if (flow < 100) return "76–83 mm";
    if (flow < 140) return "83–88 mm";
    return "88–94 mm+";
}

function calcTurbo() {
    const hp = crankHorsepower(document.getElementById("tu-hp").value || 1000);
    const boost = Math.max(0, parseFloat(document.getElementById("tu-boost").value) || 0);
    let cid = parseFloat(document.getElementById("tu-disp").value);
    if (!Number.isFinite(cid) || cid <= 0) cid = 364;
    if (dispUnit === "l") cid *= CID_PER_LITER;
    const rpm = Math.max(2000, parseFloat(document.getElementById("tu-rpm").value) || 6500);
    const fuelKey = document.getElementById("tu-fuel").value || "gasoline";
    const fuel = TURBO_FUEL[fuelKey] || TURBO_FUEL.gasoline;
    const customBsfc = parseFloat(document.getElementById("tu-bsfc").value);
    const bsfc = Number.isFinite(customBsfc) && customBsfc > 0 ? customBsfc : fuel.bsfc;
    const count = Math.max(1, parseInt(document.getElementById("tu-count").value, 10) || 1);
    const valve = document.getElementById("tu-valve").value || "ohv";
    const use = document.getElementById("tu-app").value || "drag";
    let baro = parseFloat(document.getElementById("tu-baro").value);
    if (!Number.isFinite(baro) || baro <= 0) baro = 14.7;
    let ambient = parseFloat(document.getElementById("tu-temp").value);
    if (!Number.isFinite(ambient)) ambient = 75;
    const icEff = Math.min(0.95, Math.max(0, (parseFloat(document.getElementById("tu-ic").value) || 0) / 100));
    const compEff = Math.min(0.85, Math.max(0.5, (parseFloat(document.getElementById("tu-ce").value) || 72) / 100));
    const ve = Math.min(1.05, ((VE_BASE[valve] || 78) + (VE_USE[use] || 0)) / 100);
    const density = airDensity(baro, ambient);
    const wNa = (cid / 1728) * (rpm / 2) * ve * density;
    const wReq = (hp * bsfc * fuel.afr) / 60;
    const prReq = wNa > 0 ? wReq / wNa : 1;
    const boostReq = Math.max(0, (prReq - 1) * baro);
    const prTarget = (boost + baro) / baro;
    const flowAtTarget = wNa * prTarget;
    const hpAtTarget = wReq > 0 ? hp * (flowAtTarget / wReq) : 0;
    const perTurbo = wReq / count;
    const band = sizeBand(perTurbo);
    const inletR = ambient + 10 + 459.67;
    const t2 = inletR * (1 + (Math.pow(Math.max(prTarget, 1), 0.286) - 1) / compEff) - 459.67;
    const t3 = icEff > 0 ? t2 - icEff * (t2 - ambient) : t2;
    const cfm = wReq / Math.max(density, 0.02);
    publishReadout([
        { label: "Airflow per turbo", value: perTurbo, unit: "lbmin", primary: true },
        { label: "Total airflow", value: wReq, unit: "lbmin" },
        { label: "Boost this power needs", value: boostReq, unit: "psi" },
        { label: "Pressure ratio needed", value: prReq, unit: "ratio" },
        { label: "PR at your boost", value: prTarget, unit: "ratio" },
        { label: "Power at your boost", value: Math.round(hpAtTarget) + " HP", unit: "text" },
        { label: "Volumetric efficiency", value: ve * 100, unit: "pct" },
        { label: "NA airflow", value: wNa, unit: "lbmin" },
        { label: "Compressor outlet", value: t2, unit: "tempf" },
        { label: "After intercooler", value: t3, unit: "tempf" },
        { label: "Standard flow", value: cfm, unit: "cfm" },
        { label: "BSFC x AFR", value: bsfc.toFixed(2) + " x " + fuel.afr.toFixed(1), unit: "text" }
    ]);
    const className = document.getElementById("tu-class");
    const classDesc = document.getElementById("tu-class-desc");
    if (className) className.textContent = band[0] + " · " + inducerRange(perTurbo);
    if (classDesc) classDesc.textContent = band[1] + " Each turbo needs about " + reading(perTurbo, "lbmin") + ". Shop the inducer, then confirm the island on the map at " + prTarget.toFixed(2) + ":1.";
    const assess = document.getElementById("tu-assess");
    if (assess) {
        const need = "This power target needs about " + reading(boostReq, "psi") + " (" + prReq.toFixed(2) + ":1) on this displacement and volumetric efficiency.";
        let fit;
        if (boost + 0.4 < boostReq) {
            fit = " The boost you entered is short of that, so the engine runs out of air before the power number.";
        } else if (boost > boostReq + 2) {
            fit = " At " + reading(boost, "psi") + " the same engine can feed about " + Math.round(hpAtTarget) + " HP if the turbo and fuel system keep up.";
        } else {
            fit = " The boost you entered is in line with that airflow.";
        }
        const prBuild = Math.max(prReq, prTarget);
        let build;
        if (prBuild < 1.6) build = " That is mild boost for a stock block with fuel and a tune.";
        else if (prBuild < 2.0) build = " Plan on a head gasket, studs, and a fuel system that can keep up.";
        else if (prBuild < 2.5) build = " Forged pistons and rods are the honest short-block plan here.";
        else build = " This is purpose-built short-block territory.";
        assess.textContent = need + fit + build;
    }
    const thermal = document.getElementById("tu-thermal");
    if (thermal) {
        if (icEff === 0) {
            thermal.textContent = "With no intercooler the manifold sees about " + reading(t2, "tempf") + " off the compressor. Add a cooler before treating this as a strip tune.";
        } else if (t3 > 200) {
            thermal.textContent = "Charge temperature is still about " + reading(t3, "tempf") + " after the intercooler. The cooler is undersized for this pressure ratio, or the turbo is off its efficiency island.";
        } else if (t3 > 150) {
            thermal.textContent = "Manifold temperature lands near " + reading(t3, "tempf") + ". A larger air-to-air or a water-to-air cooler gives the tune more room.";
        } else {
            thermal.textContent = "Manifold temperature lands near " + reading(t3, "tempf") + " with this intercooler. That is a usable range at the boost you entered.";
        }
    }
    const body = document.getElementById("tu-rpm-rows");
    if (body) {
        body.replaceChildren();
        const points = [
            ["Spool", 0.35],
            ["Mid", 0.50],
            ["Upper mid", 0.65],
            ["Power", 0.80],
            ["Near peak", 0.90],
            ["Peak", 1]
        ];
        points.forEach(point => {
            const pointRpm = Math.round(rpm * point[1]);
            const na = (cid / 1728) * (pointRpm / 2) * ve * density;
            const boosted = na * prTarget;
            const tr = document.createElement("tr");
            if (point[1] === 1) tr.className = "is-rec";
            const cells = [point[0], pointRpm.toLocaleString("en-US"), reading(na, "lbmin"), reading(boosted, "lbmin")];
            cells.forEach(text => {
                const td = document.createElement("td");
                td.textContent = text;
                tr.appendChild(td);
            });
            body.appendChild(tr);
        });
    }
}
document.querySelectorAll(".disp-unit").forEach(button => {
    button.addEventListener("click", () => {
        const next = button.dataset.disp;
        const el = document.getElementById("tu-disp");
        if (!el || next === dispUnit) return;
        let value = parseFloat(el.value) || 0;
        if (dispUnit === "ci" && next === "l") value = value / CID_PER_LITER;
        if (dispUnit === "l" && next === "ci") value = value * CID_PER_LITER;
        el.value = next === "l" ? value.toFixed(2) : value.toFixed(0);
        el.step = next === "l" ? "0.1" : "1";
        dispUnit = next;
        button.parentElement.querySelectorAll(".disp-unit").forEach(pill => {
            pill.classList.toggle("active", pill === button);
        });
        if (typeof window.refreshCalc === "function") window.refreshCalc();
    });
});
bindCalc(calcTurbo, ["tu-hp", "tu-boost", "tu-disp", "tu-fuel", "tu-count", "tu-valve", "tu-app", "tu-rpm", "tu-bsfc", "tu-baro", "tu-temp", "tu-ic", "tu-ce", "dt-loss"]);
"""



def suspension_html(_row):
    primary = """
    <div class="grid-2">
        <div class="field"><label for="l1">Wheelbase (in)</label><input type="number" id="l1" value="110.0" step="0.5"></div>
        <div class="field"><label for="l2">Crankshaft height (in)</label><input type="number" id="l2" value="24.0" step="0.5"></div>
    </div>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="l3">Axle to rear top hole (in)</label><input type="number" id="l3" value="4.0" step="0.1"></div>
        <div class="field"><label for="l4">Ground to rear top hole (in)</label><input type="number" id="l4" value="18.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="l5">Axle to rear bottom hole (in)</label><input type="number" id="l5" value="4.0" step="0.1"></div>
        <div class="field"><label for="l6">Ground to rear bottom hole (in)</label><input type="number" id="l6" value="10.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="l7">Axle to front top hole (in)</label><input type="number" id="l7" value="32.0" step="0.5"></div>
        <div class="field"><label for="l8">Ground to front top hole (in)</label><input type="number" id="l8" value="20.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="l9">Axle to front bottom hole (in)</label><input type="number" id="l9" value="32.0" step="0.5"></div>
        <div class="field"><label for="l10">Ground to front bottom hole (in)</label><input type="number" id="l10" value="11.0" step="0.5"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print chassis setup sheet")


SUSPENSION_SCRIPT = """
function calcTool() {
    let l1 = parseFloat(document.getElementById("l1").value) || 110;
    let l2 = parseFloat(document.getElementById("l2").value) || 24;
    let l3 = parseFloat(document.getElementById("l3").value) || 4;
    let l4 = parseFloat(document.getElementById("l4").value) || 18;
    let l5 = parseFloat(document.getElementById("l5").value) || 4;
    let l6 = parseFloat(document.getElementById("l6").value) || 10;
    let l7 = parseFloat(document.getElementById("l7").value) || 32;
    let l8 = parseFloat(document.getElementById("l8").value) || 20;
    let l9 = parseFloat(document.getElementById("l9").value) || 32;
    let l10 = parseFloat(document.getElementById("l10").value) || 11;
    let topSlope = (l8 - l4) / (l7 - l3 + 0.001);
    let botSlope = (l10 - l6) / (l9 - l5 + 0.001);
    let icLen = Math.abs((l4 - l6) / (topSlope - botSlope + 0.0001));
    if (isNaN(icLen) || icLen > 250) icLen = 54.5;
    let icHt = l4 + topSlope * icLen;
    if (isNaN(icHt)) icHt = 15.2;
    let antiSquat = Math.round((icHt / l2) * 100);
    publishReadout([
        { label: "Anti-squat", value: antiSquat, unit: "pct", primary: true },
        { label: "Instant center length", value: icLen, unit: "in" },
        { label: "Instant center height", value: icHt, unit: "in" }
    ]);
}
bindCalc(calcTool, ["l1","l2","l3","l4","l5","l6","l7","l8","l9","l10"]);
"""


def exhaust_html(row):
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="ex-cid">Displacement (CID)</label><input type="number" id="ex-cid" value="400" step="5"></div>
        <div class="field"><label for="ex-cyl">Cylinders</label><input type="number" id="ex-cyl" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ex-rpm">Peak RPM</label><input type="number" id="ex-rpm" value="{esc(field(row, 'rpm', '6500'))}" step="100"></div>
        <div class="field"><label for="ex-layout">Layout</label>
            <select id="ex-layout">
                <option value="na">Naturally aspirated headers</option>
                <option value="turbo" selected>Turbo manifold / downpipe</option>
            </select>
        </div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="ex-dur">Exhaust duration (deg)</label><input type="number" id="ex-dur" value="240" step="5"></div>
        <div class="field"><label for="ex-hp">Power for downpipe</label><input type="number" id="ex-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
    </div>
    {LOSS_FIELDS}
    """
    return calculator_shell(primary, advanced, "Print exhaust spec sheet", power_toggle=True)


EXHAUST_SCRIPT = """
function calcExhaust() {
    let cid = parseFloat(document.getElementById("ex-cid").value) || 400;
    let cyl = parseFloat(document.getElementById("ex-cyl").value) || 8;
    let rpm = parseFloat(document.getElementById("ex-rpm").value) || 6500;
    let dur = parseFloat(document.getElementById("ex-dur").value) || 240;
    let layout = document.getElementById("ex-layout").value;
    let hp = crankHorsepower(document.getElementById("ex-hp").value || 1000);
    let primaryId = Math.sqrt((cid / cyl) * rpm / 88200);
    let primaryLen = (dur * 850 / rpm) - 3;
    let collector = layout === "turbo" ? Math.sqrt(hp / 220) : primaryId * 1.75;
    let label = layout === "turbo" ? "Downpipe ID" : "Collector ID";
    publishReadout([
        { label: "Primary ID", value: primaryId, unit: "in", primary: true },
        { label: "Primary length", value: primaryLen, unit: "in" },
        { label: label, value: collector, unit: "in" }
    ]);
}
bindCalc(calcExhaust, ["ex-cid", "ex-cyl", "ex-rpm", "ex-dur", "ex-layout", "ex-hp", "dt-loss"]);
"""


def supercharger_html(row):
    kind = field(row, "blower_type", "twin-screw")
    factor = {key: value for key, value, _label in BLOWER_OPTIONS}[kind]
    blower_options = options([(value, label) for _key, value, label in BLOWER_OPTIONS], factor)
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="sc-crank">Crank pulley (in)</label><input type="number" id="sc-crank" value="{esc(field(row, 'crank_pulley', '8.0'))}" step="0.1"></div>
        <div class="field"><label for="sc-blower">Blower pulley (in)</label><input type="number" id="sc-blower" value="{esc(field(row, 'blower_pulley', '3.0'))}" step="0.1"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="sc-rpm">Max crank RPM</label><input type="number" id="sc-rpm" value="{esc(field(row, 'rpm', '6500'))}" step="100"></div>
        <div class="field"><label for="sc-fac">Blower type</label><select id="sc-fac">{blower_options}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sc-target">Target boost (PSI)</label><input type="number" id="sc-target" value="{esc(cell(row, 'boost'))}" step="0.5"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print pulley spec sheet")


SUPERCHARGER_SCRIPT = """
function calcSupercharger() {
    let crank = parseFloat(document.getElementById("sc-crank").value) || 8.0;
    let blower = parseFloat(document.getElementById("sc-blower").value) || 3.0;
    let rpm = parseFloat(document.getElementById("sc-rpm").value) || 6500;
    let factor = parseFloat(document.getElementById("sc-fac").value) || 1.45;
    let ratio = crank / Math.max(blower, 0.1);
    let impellerRpm = Math.round(rpm * ratio);
    let estBoost = ratio * 5.2 * factor;
    let items = [
        { label: "Estimated boost", value: estBoost, unit: "psi", primary: true },
        { label: "Pulley ratio", value: ratio, unit: "ratio" },
        { label: "Impeller RPM", value: impellerRpm, unit: "rpm" }
    ];
    let targetRaw = document.getElementById("sc-target").value;
    if (targetRaw !== "") {
        let target = parseFloat(targetRaw);
        if (isFinite(target)) items.push({ label: "Boost versus target", value: estBoost - target, unit: "psi" });
    }
    publishReadout(items);
}
bindCalc(calcSupercharger, ["sc-crank", "sc-blower", "sc-rpm", "sc-fac", "sc-target"]);
"""


def rear_gear_html(row):
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="rg-gear">Rear gear</label><input type="number" id="rg-gear" value="{esc(field(row, 'rear_gear', '4.11'))}" step="0.01"></div>
        <div class="field"><label for="rg-tire">Tire diameter (in)</label><input type="number" id="rg-tire" value="{esc(field(row, 'tire_diameter', '32.0'))}" step="0.1"></div>
    </div>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="rg-trap">Target trap speed (MPH)</label><input type="number" id="rg-trap" value="125" step="1"></div>
        <div class="field"><label for="rg-final">Trans final ratio</label><input type="number" id="rg-final" value="1.00" step="0.01"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print rear gear sheet")


REAR_GEAR_SCRIPT = """
function calcRearGear() {
    let trap = parseFloat(document.getElementById("rg-trap").value) || 125;
    let gear = parseFloat(document.getElementById("rg-gear").value) || 4.11;
    let tire = parseFloat(document.getElementById("rg-tire").value) || 32;
    let transFinal = parseFloat(document.getElementById("rg-final").value) || 1.00;
    let overall = gear * transFinal;
    let finishRpm = (trap * overall * 336) / Math.max(tire, 0.1);
    let rollout = tire * Math.PI;
    let mphAt7500 = (7500 * tire) / (overall * 336);
    publishReadout([
        { label: "Finish RPM", value: finishRpm, unit: "rpm", primary: true },
        { label: "Overall ratio", value: overall, unit: "ratio" },
        { label: "Rollout", value: rollout, unit: "in" },
        { label: "Speed at 7,500 RPM", value: mphAt7500, unit: "mph" }
    ]);
}
bindCalc(calcRearGear, ["rg-trap", "rg-gear", "rg-tire", "rg-final"]);
"""


def tire_html(row):
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="tg-dia">Static tire diameter (in)</label><input type="number" id="tg-dia" value="{esc(field(row, 'tire_diameter', '28.0'))}" step="0.1"></div>
        <div class="field"><label for="tg-growth">Growth factor (%)</label><input type="number" id="tg-growth" value="{esc(field(row, 'growth', '4.5'))}" step="0.1"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="tg-trap">Trap speed (MPH)</label><input type="number" id="tg-trap" value="150" step="1"></div>
        <div class="field"><label for="tg-gear">Rear gear</label><input type="number" id="tg-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print tire growth sheet")


TIRE_SCRIPT = """
function calcTireGrowth() {
    let staticDia = parseFloat(document.getElementById("tg-dia").value) || 28;
    let trap = parseFloat(document.getElementById("tg-trap").value) || 150;
    let growth = parseFloat(document.getElementById("tg-growth").value) || 4.5;
    let gear = parseFloat(document.getElementById("tg-gear").value) || 3.42;
    let dynamicDia = staticDia * (1 + (growth / 100));
    let staticRollout = staticDia * Math.PI;
    let dynamicRollout = dynamicDia * Math.PI;
    let estFinishRpm = (trap * gear * 336) / dynamicDia;
    publishReadout([
        { label: "Dynamic diameter", value: dynamicDia, unit: "in", primary: true },
        { label: "Static rollout", value: staticRollout, unit: "in" },
        { label: "Dynamic rollout", value: dynamicRollout, unit: "in" },
        { label: "Finish RPM", value: estFinishRpm, unit: "rpm" }
    ]);
}
bindCalc(calcTireGrowth, ["tg-dia", "tg-trap", "tg-growth", "tg-gear"]);
"""


def wastegate_html(row):
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="wg-hp">Power</label><input type="number" id="wg-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div class="field"><label for="wg-boost">Target boost (PSI)</label><input type="number" id="wg-boost" value="{esc(field(row, 'boost', '22'))}" step="1"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="wg-count">Number of gates</label>
            <select id="wg-count">
                <option value="1" selected>Single gate</option>
                <option value="2">Twin gates</option>
            </select>
        </div>
        <div class="field"><label for="wg-style">Gate style</label>
            <select id="wg-style">
                <option value="1.00">Internal wastegate</option>
                <option value="1.25" selected>External wastegate</option>
            </select>
        </div>
    </div>
    {LOSS_FIELDS}
    """
    return calculator_shell(primary, advanced, "Print wastegate spec sheet", power_toggle=True)


WASTEGATE_SCRIPT = """
function calcWastegate() {
    let hp = crankHorsepower(document.getElementById("wg-hp").value || 1000);
    let boost = parseFloat(document.getElementById("wg-boost").value) || 22;
    let count = parseInt(document.getElementById("wg-count").value, 10) || 1;
    let style = parseFloat(document.getElementById("wg-style").value) || 1.25;
    let bypassFrac = boost / (boost + 14.7);
    let exhaustLbMin = hp * 0.12;
    let wgFlow = (exhaustLbMin * bypassFrac) / count / style;
    let diaMm = 10 * Math.sqrt(Math.max(wgFlow, 1));
    let rec = 38;
    if (diaMm > 42) rec = 44;
    if (diaMm > 48) rec = 50;
    if (diaMm > 56) rec = 60;
    publishReadout([
        { label: "Recommended gate", value: rec, unit: "mm", primary: true },
        { label: "Bypass fraction", value: bypassFrac * 100, unit: "pct" },
        { label: "Flow per gate", value: wgFlow, unit: "lbmin" },
        { label: "Gate count", value: count + " x " + rec + " mm", unit: "text" }
    ]);
}
bindCalc(calcWastegate, ["wg-hp", "wg-boost", "wg-count", "wg-style", "dt-loss"]);
"""


def fuel_html(row):
    fuel = field(row, "fuel", "gasoline")
    fuel_options = options(INJECTOR_FUELS, fuel)
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="fi-hp">Target power</label><input type="number" id="fi-hp" value="{esc(field(row, 'hp', '1000'))}" min="50" step="25"></div>
        <div class="field"><label for="fi-inj">Injector count</label><input type="number" id="fi-inj" value="8" min="1" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="fi-fuel">Fuel</label><select id="fi-fuel">{fuel_options}</select></div>
        <div class="field"><label for="fi-ind">Induction</label>
            <select id="fi-ind">
                <option value="turbo" selected>Turbocharged</option>
                <option value="supercharged">Supercharged</option>
                <option value="na">Naturally aspirated</option>
            </select>
        </div>
    </div>
    <div class="field">
        <label for="fi-dc">Max duty cycle (%)</label>
        <input type="number" id="fi-dc" value="80" min="50" max="95" step="1">
        <input type="range" id="fi-dc-range" value="80" min="50" max="95" step="1" aria-label="Max duty cycle slider">
        <p class="field-hint">80% is the street ceiling. 85% is the redline limit. Count every injector on a staged system.</p>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="fi-bsfc">Custom BSFC</label><input type="number" id="fi-bsfc" placeholder="Auto" min="0.2" max="2" step="0.01"></div>
        <div class="field"><label for="fi-pressure">Base fuel pressure (PSI)</label><input type="number" id="fi-pressure" value="43.5" min="20" max="100" step="0.5"></div>
    </div>
    <p class="field-hint">Leave BSFC blank to use the fuel and induction table. Injectors are rated at 43.5 PSI, so a higher base pressure lets you buy a smaller rated size. A 1:1 boost-referenced regulator holds that differential on boost.</p>
    {LOSS_FIELDS}
    """
    results = """
    <div class="duty-card">
        <div class="duty-head"><span>Duty cycle on recommended size</span><strong id="fi-dc-label">—</strong></div>
        <div class="duty-track"><div class="duty-fill" id="fi-dc-fill"></div></div>
        <div class="duty-scale"><span>0%</span><span>50%</span><span>80%</span><span>85%</span><span>100%</span></div>
    </div>
    <p class="assess" id="fi-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Size</th><th>Duty at target</th><th>Supports</th><th>Status</th></tr></thead>
            <tbody id="fi-sizes"></tbody>
        </table>
        <p class="field-hint">Catalog flow is at 43.5 PSI. Duty cycle and horsepower use flow at your base pressure.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print injector spec sheet", power_toggle=True, results_extra=results)


FUEL_SCRIPT = r"""
const FUEL_BSFC = {
    gasoline: { turbo: 0.65, supercharged: 0.65, na: 0.50 },
    e85: { turbo: 0.95, supercharged: 0.95, na: 0.75 },
    methanol: { turbo: 1.20, supercharged: 1.20, na: 0.95 },
    race: { turbo: 0.70, supercharged: 0.70, na: 0.55 },
    diesel: { turbo: 0.40, supercharged: 0.40, na: 0.37 }
};
const FUEL_DENSITY = { gasoline: 6.17, e85: 6.55, methanol: 6.63, race: 6.20, diesel: 7.05 };
const INJECTOR_SIZES = [275, 310, 365, 440, 550, 650, 750, 850, 1000, 1100, 1200, 1300, 1650, 2200];
const CC_PER_LBHR = 10.5;
const RATED_PSI = 43.5;

function injectorDuty(size, totalLbHr, count, pressureFactor) {
    const actualLb = (size / CC_PER_LBHR) * pressureFactor;
    return (totalLbHr / (count * actualLb)) * 100;
}

function calcInjector() {
    const hp = crankHorsepower(document.getElementById("fi-hp").value || 1000);
    const count = Math.max(1, parseFloat(document.getElementById("fi-inj").value) || 8);
    const fuelKey = document.getElementById("fi-fuel").value || "gasoline";
    const induction = document.getElementById("fi-ind").value || "turbo";
    const custom = parseFloat(document.getElementById("fi-bsfc").value);
    const table = FUEL_BSFC[fuelKey] || FUEL_BSFC.gasoline;
    const bsfc = Number.isFinite(custom) && custom > 0 ? custom : (table[induction] || table.turbo);
    let maxDcPct = parseFloat(document.getElementById("fi-dc").value);
    if (!Number.isFinite(maxDcPct)) maxDcPct = 80;
    maxDcPct = Math.min(95, Math.max(50, maxDcPct));
    const maxDc = maxDcPct / 100;
    let pressure = parseFloat(document.getElementById("fi-pressure").value);
    if (!Number.isFinite(pressure) || pressure < 20) pressure = RATED_PSI;
    const pressureFactor = Math.sqrt(pressure / RATED_PSI);
    const totalLbHr = hp * bsfc;
    const railLbHr = totalLbHr / (count * maxDc);
    const ratedCc = (railLbHr / pressureFactor) * CC_PER_LBHR;
    const recommended = INJECTOR_SIZES.find(size => injectorDuty(size, totalLbHr, count, pressureFactor) <= maxDcPct + 0.05);
    const heroSize = recommended || ratedCc;
    const shownSize = recommended || INJECTOR_SIZES[INJECTOR_SIZES.length - 1];
    const shownDuty = injectorDuty(shownSize, totalLbHr, count, pressureFactor);
    const shownFlow = (shownSize / CC_PER_LBHR) * pressureFactor;
    const supports = (shownFlow * count * maxDc) / bsfc;
    const density = FUEL_DENSITY[fuelKey] || 6.17;
    const pumpGph = (totalLbHr / density) * 1.25;
    publishReadout([
        { label: recommended ? "Recommended size" : "Minimum rated size", value: heroSize, unit: "cc", primary: true },
        { label: "Flow each at cap", value: railLbHr, unit: "lbhr" },
        { label: "Duty on " + shownSize.toLocaleString("en-US") + " cc", value: shownDuty, unit: "pct1" },
        { label: shownSize.toLocaleString("en-US") + " cc supports", value: Math.round(supports) + " HP", unit: "text" },
        { label: "System flow", value: totalLbHr, unit: "lbhr" },
        { label: "BSFC used", value: bsfc.toFixed(2), unit: "text" },
        { label: "Flywheel power", value: Math.round(hp) + " HP", unit: "text" },
        { label: "Fuel pump + 25%", value: pumpGph, unit: "gph" }
    ]);

    const fill = document.getElementById("fi-dc-fill");
    const label = document.getElementById("fi-dc-label");
    const tone = shownDuty <= 80 ? "tone-ok" : (shownDuty <= 85 ? "tone-tight" : "tone-over");
    if (fill) {
        fill.style.width = Math.min(shownDuty, 100) + "%";
        fill.style.background = shownDuty <= 80 ? "#3dd68c" : (shownDuty <= 85 ? "#f5a524" : "#e50914");
    }
    if (label) {
        label.textContent = shownDuty.toFixed(1) + "%";
        label.className = tone;
    }
    const assess = document.getElementById("fi-assess");
    if (assess) {
        const pressureNote = Math.abs(pressure - RATED_PSI) > 0.2
            ? " Catalog sizes are corrected for " + pressure.toFixed(1) + " PSI base pressure."
            : "";
        if (!recommended) {
            assess.textContent = "This target needs more than a 2200 cc injector can deliver with " + count + " injectors. Add injectors or raise base pressure before the top of the gear." + pressureNote;
        } else if (shownDuty <= 80) {
            assess.textContent = "A " + recommended + " cc injector covers this target at " + shownDuty.toFixed(1) + "% duty, under the 80% street ceiling. One size larger is cheap insurance if the power number is still climbing." + pressureNote;
        } else if (shownDuty <= 85) {
            assess.textContent = "A " + recommended + " cc injector is the smallest common size inside your duty-cycle cap, and it still runs " + shownDuty.toFixed(1) + "%. That is the tight side of 85%, so leave pump and regulator headroom." + pressureNote;
        } else {
            assess.textContent = "The closest common injector still runs " + shownDuty.toFixed(1) + "% at this target. Treat anything over 85% as a lean risk at redline." + pressureNote;
        }
    }
    const body = document.getElementById("fi-sizes");
    if (body) {
        body.replaceChildren();
        INJECTOR_SIZES.forEach(size => {
            const duty = injectorDuty(size, totalLbHr, count, pressureFactor);
            const flow = (size / CC_PER_LBHR) * pressureFactor;
            const supportHp = (flow * count * maxDc) / bsfc;
            const tr = document.createElement("tr");
            let status = "Too small";
            let badge = "badge-no";
            if (size === recommended) {
                tr.className = "is-rec";
                status = "Recommended";
                badge = "badge-rec";
            } else if (duty <= 80) {
                status = "Good";
                badge = "badge-ok";
            } else if (duty <= 85) {
                status = "Tight";
                badge = "badge-tight";
            } else {
                tr.className = "is-small";
            }
            const sizeCell = document.createElement("td");
            sizeCell.textContent = size.toLocaleString("en-US") + " cc";
            const sub = document.createElement("div");
            sub.className = "size-sub";
            sub.textContent = reading(size / CC_PER_LBHR, "lbhr") + " rated";
            sizeCell.appendChild(sub);
            const dutyCell = document.createElement("td");
            dutyCell.textContent = duty.toFixed(1) + "%";
            dutyCell.className = duty <= 80 ? "tone-ok" : (duty <= 85 ? "tone-tight" : "tone-over");
            const supportCell = document.createElement("td");
            supportCell.textContent = Math.round(supportHp).toLocaleString("en-US") + " HP";
            const statusCell = document.createElement("td");
            const pill = document.createElement("span");
            pill.className = "badge " + badge;
            pill.textContent = status;
            statusCell.appendChild(pill);
            tr.append(sizeCell, dutyCell, supportCell, statusCell);
            body.appendChild(tr);
        });
    }
}
const dutyNumber = document.getElementById("fi-dc");
const dutyRange = document.getElementById("fi-dc-range");
if (dutyNumber && dutyRange) {
    dutyRange.addEventListener("input", () => { dutyNumber.value = dutyRange.value; });
    dutyNumber.addEventListener("input", () => { dutyRange.value = dutyNumber.value; });
}
bindCalc(calcInjector, ["fi-hp", "fi-inj", "fi-ind", "fi-fuel", "fi-dc", "fi-dc-range", "fi-bsfc", "fi-pressure", "dt-loss"]);
"""



def electrical_html(_row):
    primary = """
    <div class="grid-2">
        <div class="field"><label for="rl-watts">Load power (watts)</label><input type="number" id="rl-watts" value="240" step="10"></div>
        <div class="field"><label for="rl-volts">System voltage</label>
            <select id="rl-volts">
                <option value="12" selected>12V chassis</option>
                <option value="13.8">13.8V running</option>
                <option value="16">16V race</option>
            </select>
        </div>
    </div>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="rl-duty">Duty</label>
            <select id="rl-duty">
                <option value="1.25" selected>Continuous (1.25x)</option>
                <option value="1.10">Intermittent (1.10x)</option>
            </select>
        </div>
        <div class="field"><label for="rl-len">One-way wire length (ft)</label><input type="number" id="rl-len" value="12" step="1"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print wiring spec sheet")


ELECTRICAL_SCRIPT = """
function calcRelay() {
    let watts = parseFloat(document.getElementById("rl-watts").value) || 240;
    let volts = parseFloat(document.getElementById("rl-volts").value) || 12;
    let duty = parseFloat(document.getElementById("rl-duty").value) || 1.25;
    let len = parseFloat(document.getElementById("rl-len").value) || 12;
    let amps = watts / Math.max(volts, 1);
    let designAmps = amps * duty;
    let relaySizes = [20, 30, 40, 70, 80, 100, 120];
    let relay = relaySizes.find(size => size >= designAmps) || 150;
    let fuse = Math.ceil(designAmps / 5) * 5;
    let awg = "16";
    if (designAmps > 15) awg = "14";
    if (designAmps > 24) awg = "12";
    if (designAmps > 32) awg = "10";
    if (designAmps > 45) awg = "8";
    if (designAmps > 65) awg = "6";
    if (designAmps > 95) awg = "4";
    if (len > 15) {
        let n = parseInt(awg, 10);
        if (n >= 8) awg = String(n - 2);
    }
    publishReadout([
        { label: "Design current", value: designAmps, unit: "amp", primary: true },
        { label: "Load current", value: amps, unit: "amp" },
        { label: "Relay", value: relay + " A", unit: "text" },
        { label: "Fuse", value: fuse + " A", unit: "text" },
        { label: "Wire", value: awg, unit: "awg" },
        { label: "One-way length", value: len, unit: "ft" }
    ]);
}
bindCalc(calcRelay, ["rl-watts", "rl-volts", "rl-duty", "rl-len"]);
"""


def cas_html(row):
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="cas-boost">Target boost (PSI)</label><input type="number" id="cas-boost" value="{esc(field(row, 'boost', '20'))}" step="1"></div>
    </div>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="cas-baro">Barometric pressure (PSI)</label><input type="number" id="cas-baro" value="14.7" step="0.1"></div>
    </div>
    """
    return calculator_shell(primary, advanced, "Print boost sheet")


CAS_SCRIPT = """
function calcCas() {
    let boost = parseFloat(document.getElementById("cas-boost").value);
    if (!isFinite(boost) || boost < 0) boost = 0;
    let baro = parseFloat(document.getElementById("cas-baro").value);
    if (!isFinite(baro) || baro <= 0) baro = 14.7;
    let absolute = boost + baro;
    let pr = absolute / baro;
    publishReadout([
        { label: "Gauge boost", value: boost, unit: "psi", primary: true },
        { label: "Absolute pressure", value: absolute, unit: "psi" },
        { label: "Pressure ratio", value: pr, unit: "ratio" }
    ]);
}
bindCalc(calcCas, ["cas-boost", "cas-baro"]);
"""

WIDGETS = {
    "Transmission": (
        "Overall Ratio = Trans Ratio x Rear Gear. Shift Speed (MPH) = (RPM x (1 - Slip) x Tire) / (Overall x 336). Recovery RPM = Shift RPM x (1 - Slip) x (Next Ratio / Current Ratio).",
        transmission_html,
        DRIVETRAIN_SCRIPT,
    ),
    "Turbo": (
        "Air lb/min = (Flywheel HP x BSFC x Power AFR) / 60. Required boost comes from that airflow divided by the engine's naturally aspirated flow at your RPM and volumetric efficiency.",
        turbo_html,
        TURBO_SCRIPT,
    ),
    "Suspension": (
        "Anti-Squat % = (Instant Center Height / Crank Height) x 100, from the 10 chassis coordinates.",
        suspension_html,
        SUSPENSION_SCRIPT,
    ),
    "Exhaust": (
        "Primary ID = sqrt((CID / Cylinders) x RPM / 88200) | Primary Length = (Duration x 850 / RPM) - 3 | Turbo Downpipe ID = sqrt(HP / 220)",
        exhaust_html,
        EXHAUST_SCRIPT,
    ),
    "Supercharger": (
        "Pulley Ratio = Crank Dia / Blower Dia | Impeller RPM = Crank RPM x Ratio | Est. Boost = Ratio x 5.2 x Blower Factor",
        supercharger_html,
        SUPERCHARGER_SCRIPT,
    ),
    "RearGear": (
        "Finish RPM = (Trap MPH x Overall Ratio x 336) / Tire Diameter | Overall Ratio = Rear Gear x Trans Final",
        rear_gear_html,
        REAR_GEAR_SCRIPT,
    ),
    "Tire": (
        "Dynamic Diameter = Static Dia x (1 + Growth% / 100) | Rollout = Diameter x PI | Finish RPM = (Trap x Gear x 336) / Dynamic Dia",
        tire_html,
        TIRE_SCRIPT,
    ),
    "Wastegate": (
        "Bypass Fraction = Boost / (Boost + 14.7) | Gate Flow = (HP x 0.12 x Bypass) / Gate Count",
        wastegate_html,
        WASTEGATE_SCRIPT,
    ),
    "Fuel": (
        "Rated lb/hr = (Flywheel HP x BSFC) / (Injector Count x Max Duty x sqrt(Base PSI / 43.5)). cc/min = lb/hr x 10.5. Buy the smallest common size whose duty cycle stays inside your cap.",
        fuel_html,
        FUEL_SCRIPT,
    ),
    "Electrical": (
        "Load Amps = Watts / Voltage | Design Amps = Load x Duty Factor. Relay, fuse, and wire size sit above that current.",
        electrical_html,
        ELECTRICAL_SCRIPT,
    ),
    "CAS": (
        "Pressure Ratio = (Boost PSI + Barometric PSI) / Barometric PSI",
        cas_html,
        CAS_SCRIPT,
    ),
}


def footer():
    return """
<footer class="site-footer">
    <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved.</p>
    <p><a class="accent" href="contact.html">Contact &amp; Sponsorships</a> &nbsp;|&nbsp; <a href="privacy.html">Privacy Policy &amp; Affiliate Disclosure</a></p>
</footer>
"""


def sidebar(active_slug, hubs):
    parts = ['<nav class="nav-list">']
    master_class = "nav-item active" if active_slug == "index" else "nav-item"
    parts.append(f'<a class="{master_class}" href="index.html">Popular / Master Hub</a>')
    for hub in hubs:
        css = "nav-item active" if hub["slug"] == active_slug else "nav-item"
        parts.append(f'<a class="{css}" href="{esc(hub["slug"])}.html">{esc(hub["nav_label"])}</a>')
    parts.append("</nav>")
    return "".join(parts)


def link_items(pages):
    items = []
    for page in pages:
        items.append(f'<li><a href="{esc(page["slug"])}.html">{esc(page["target_keyword"])}</a></li>')
    if not items:
        return ""
    return '<ul class="variant-list">' + "".join(items) + "</ul>"


def content_box(title, body):
    return f'<section class="content-box"><h2>{esc(title)}</h2>{body}</section>'


def formula_box(text):
    return content_box("Formula", f'<p class="formula">{esc(text)}</p>')


def variants_for(category, pages):
    rows = [page for page in pages if page["category"] == category and page["role"] == "variant"]
    rows.sort(key=lambda page: page["slug"])
    return rows


def neighbor_pages(page, pages):
    ordered = variants_for(page["category"], pages)
    if page["role"] == "hub":
        return ordered
    index = next((i for i, item in enumerate(ordered) if item["slug"] == page["slug"]), None)
    if index is None or len(ordered) < 2:
        return []
    picks = []
    for step in range(1, len(ordered)):
        picks.append(ordered[(index + step) % len(ordered)])
        if len(picks) == 6:
            break
    return picks


TRACKSIDE_NOTES = {
    "Transmission": (
        ("How is shift recovery RPM calculated?", "Recovery RPM is the shift RPM times (1 minus converter slip) times the next gear divided by the gear you are leaving. At 0% slip that is the straight gear drop, and it still needs to land above converter stall."),
        ("What does the 336 constant represent?", "Miles per hour equals RPM times (1 minus converter slip) times tire diameter, divided by overall ratio times 336. Overall ratio is the transmission ratio times the rear gear."),
        ("Why does a taller tire change the chart?", "A taller tire lowers engine RPM at the same trap speed. Use the grown diameter, not the sidewall number, once the tire is at speed."),
    ),
    "Turbo": (
        ("How do you match a turbo?", "Match airflow in pounds per minute and the pressure ratio to a compressor map, then check the island at the boost you will actually run."),
        ("Why can the typed boost miss the power number?", "Naturally aspirated flow at that RPM and volumetric efficiency sets how much boost the horsepower target needs. A short boost number runs out of air first."),
        ("What does compressor outlet temperature tell you?", "Outlet temperature rises with pressure ratio and falls as compressor efficiency improves. The intercooler has to pull that heat out before the intake valve."),
    ),
    "Suspension": (
        ("What is instant center?", "Instant center is where the upper and lower link lines meet. Its height versus the center of gravity sets anti-squat."),
        ("What anti-squat range do drag cars use?", "Many door cars land around 100% to 140% anti-squat so the rear plants without unloading the front too early."),
        ("Why do small hole moves matter?", "Moving a front or rear mount an inch changes the intersection a lot. Measure from the axle center and the ground, then change one hole at a time."),
    ),
    "Exhaust": (
        ("How are primary tubes sized?", "Primary diameter follows horsepower per cylinder and the RPM where you want the torque. Bigger primaries move the peak up and can hurt the bottom."),
        ("What about a turbo downpipe?", "The downpipe has to carry the turbine discharge without becoming the restriction. Area matters more than a huge open collector on a turbo car."),
        ("Why does backpressure hurt a boosted engine?", "Excess backpressure raises turbine drive pressure, adds heat, and makes the same boost harder to control."),
    ),
    "Supercharger": (
        ("How does pulley ratio set boost?", "Pulley ratio is crank pulley diameter divided by blower pulley diameter. A smaller blower pulley raises ratio, rotor speed, and boost."),
        ("Why do roots, screw, and centrifugal blowers differ?", "Roots and twin-screw blowers move a fixed volume per revolution. A centrifugal compressor builds boost with shaft speed, so it comes on later."),
        ("What does the boost factor mean?", "The factor estimates PSI per unit of overdrive for that blower family. It is a planning number. The gauge and the inlet temperature decide the real result."),
    ),
    "RearGear": (
        ("How does gear ratio change finish-line RPM?", "A higher numeric gear raises engine RPM at the same trap speed and tire diameter."),
        ("What is a useful drag gear window?", "The gear should put the engine near peak power at the stripe without forcing an extra shift. A street gear trades that RPM for cruise."),
        ("Why measure the tire at speed?", "Growth makes the tire taller, which drops RPM. Size the gear with the grown diameter."),
    ),
    "Tire": (
        ("Why do drag tires grow?", "Centrifugal force stretches the carcass, so the rolling diameter is larger than the static measurement."),
        ("How does growth change the gear?", "A larger dynamic diameter lowers engine RPM at trap speed. The rollout and the gear chart should use that grown number."),
        ("What growth is typical?", "A radial might grow a few percent. A slick at speed can grow more. The percentage on this page is the estimate to test, not a measured rollout."),
    ),
    "Wastegate": (
        ("What sets wastegate size?", "The gate has to bypass the exhaust the turbine does not swallow at the target boost. Airflow, boost, and drive pressure decide the valve area."),
        ("What causes boost creep?", "The valve or the discharge path is too small, so exhaust still drives the turbine after the gate is open."),
        ("Why do twins use two gates?", "Each scroll or each turbo needs its own bypass path. One undersized gate on a divided housing leaves one side uncontrolled."),
    ),
    "Fuel": (
        ("How is injector size chosen?", "Rated flow is flywheel horsepower times BSFC, divided by injector count, max duty, and the pressure correction. Buy the smallest common size that stays inside the duty cap."),
        ("Why does base pressure change the rating?", "Flow scales with the square root of the pressure ratio versus the 43.5 PSI rating pressure. A higher base lets the same injector support more power."),
        ("What duty cycle is safe?", "A cap around 80% leaves room for the injector to open, close, and stay cool. Living at 90% or more is where lean spikes show up."),
    ),
    "Electrical": (
        ("How is the circuit current found?", "Load amps are watts divided by voltage. Size the wire, fuse, and relay above that, and apply a duty factor for a fan or pump that is not on full time."),
        ("Why size the wire for the run length?", "Voltage drop grows with current and length. A fuel pump at the back of the car needs a larger gauge than the same pump next to the battery."),
        ("What does the relay protect?", "The relay lets a small switch current close a high-current path. The fuse protects the wire, and it belongs at the power source."),
    ),
    "CAS": (
        ("What is a compressed-air supercharger doing?", "A stored-air system raises manifold pressure from a bottle. Pressure ratio is boost plus barometer, divided by barometer."),
        ("How long does the bottle last?", "Flow rate and bottle volume set the pass. A bigger shot or a longer gear uses the supply faster."),
        ("What should the plumbing handle?", "The solenoid, lines, and nozzles have to pass the mass flow at the pressure you dial in. A restriction downstream of the regulator is lost boost."),
    ),
}


def notes_box(page):
    keyword = page["target_keyword"].rstrip(".")
    spec = spec_text(page)
    lead = f"{keyword}. {spec}" if spec else f"{keyword}. The inputs above are the starting point for this combination."
    cheat = (
        '<ul class="cheat-list">'
        "<li>Density altitude: about 3% naturally aspirated power per 1,000 feet.</li>"
        "<li>Converter slip at the finish is often kept around 5% to 8%.</li>"
        "<li>On boost, pull roughly 1 to 2 degrees of timing for every 3 to 4 PSI.</li>"
        "</ul>"
    )
    items = []
    for question, answer in TRACKSIDE_NOTES[page["category"]]:
        items.append(f'<div class="faq-item"><h3>{esc(question)}</h3><p>{esc(answer)}</p></div>')
    return content_box("Trackside notes", f"<p>{esc(lead)}</p>{cheat}{''.join(items)}")


def related_box(page, pages, hubs_by_category):
    links = []
    hub = hubs_by_category.get(page["category"])
    if page["role"] == "hub":
        links.extend(variants_for(page["category"], pages))
        title = "Configurations"
        intro = f'<p class="field-hint">{len(links)} saved combinations for this calculator.</p>' if links else ""
    else:
        if hub:
            links.append(hub)
        links.extend(neighbor_pages(page, pages))
        title = "Related calculators"
        intro = ""
    listing = link_items(links)
    if not listing:
        return ""
    return (
        '<details class="accordion config-drawer">'
        f"<summary>{esc(title)} ({len(links)})</summary>"
        f'<div class="accordion-body">{intro}<div class="config-scroll">{listing}</div></div>'
        "</details>"
    )


def page_tokens(page, pages, hubs, hubs_by_category):
    formula, html_fn, script = WIDGETS[page["category"]]
    active = hubs_by_category.get(page["category"], {}).get("slug", "")
    if page["role"] == "hub":
        active = page["slug"]
    spec = spec_text(page)
    canonical = f"{ORIGIN}/{page['slug']}.html"
    return {
        "TITLE": esc(f"{page['target_keyword']} | DragCalculators.com"),
        "DESCRIPTION": esc(description(page)),
        "CANONICAL": esc(canonical),
        "VERIFICATION": VERIFICATION,
        "ORIGIN": ORIGIN,
        "BACK_ROW": '<div class="back-row"><a href="index.html" class="back-link">&larr; Back to Master Hub</a></div>',
        "SIDEBAR": sidebar(active, hubs),
        "H1": esc(page["target_keyword"]),
        "SPEC": f'<p class="spec">{esc(spec)}</p>' if spec else "",
        "TOOL": html_fn(page),
        "CONTENT": formula_box(formula) + notes_box(page) + related_box(page, pages, hubs_by_category),
        "FOOTER": footer(),
        "SCRIPT": UI_SCRIPT + "\n" + script,
    }


def index_page(pages, hubs):
    transmission = next(page for page in pages if page["slug"] == "transmission-shift-recovery-calculator")
    _formula, html_fn, script = WIDGETS["Transmission"]
    directory = link_items(hubs)
    content = (
        content_box(
            "Track-side notes",
            "<p>Density altitude: about 3% naturally aspirated power per 1,000 feet. "
            "Converter slip at the finish is often kept around 5% to 8%. "
            "On boost, pull roughly 1 to 2 degrees of timing for every 3 to 4 PSI.</p>",
        )
        + content_box(
            "Track sponsorships",
            '<p class="sponsor">Advertising and partnership inquiries go through the '
            '<a href="contact.html">contact form</a>.</p>',
        )
        + content_box("Calculators", directory)
    )
    spec = spec_text(transmission)
    return fill(
        PAGE_TEMPLATE,
        TITLE=esc("Ultimate Drag Racing Master Suite | Drivetrain & Shift Calculator"),
        DESCRIPTION=esc(
            "Drag racing calculators for gear ratios, turbo sizing, fuel injectors, "
            "supercharger pulleys, tire growth, and chassis setup."
        ),
        CANONICAL=esc(f"{ORIGIN}/index.html"),
        VERIFICATION=VERIFICATION,
        ORIGIN=ORIGIN,
        BACK_ROW="",
        SIDEBAR=sidebar("index", hubs),
        H1=esc("Ultimate Drag Racing Master Suite"),
        SPEC=f'<p class="spec">{esc(spec)}</p>' if spec else "",
        TOOL=html_fn(transmission),
        CONTENT=content,
        FOOTER=footer(),
        SCRIPT=UI_SCRIPT + "\n" + script,
    )


def contact_page():
    content = """
<h1>Contact &amp; Track Sponsorships</h1>
<p>Advertising rates, calculator feedback, and partnership inquiries.</p>
<form action="https://formspree.io/f/xqppzgab" method="POST">
    <div><label for="name">Your Name / Shop Name</label><input id="name" type="text" name="name" required placeholder="e.g. Pro Line Racing"></div>
    <div><label for="email">Your Email Address</label><input id="email" type="email" name="email" required placeholder="e.g. yourname@domain.com"></div>
    <div><label for="inquiry_type">Inquiry Type</label>
        <select id="inquiry_type" name="inquiry_type">
            <option value="Sponsorship">Track Sponsor Rates &amp; Advertising</option>
            <option value="Bug / Feedback">Calculator Feedback / Bug Report</option>
            <option value="Other">General Partnership</option>
        </select>
    </div>
    <div><label for="message">Message</label><textarea id="message" name="message" required placeholder="Describe your inquiry or sponsorship request here..."></textarea></div>
    <button type="submit" class="action-btn">Send Message</button>
</form>
"""
    return fill(
        NARROW_TEMPLATE,
        TITLE=esc("Contact & Track Sponsorships | DragCalculators.com"),
        DESCRIPTION=esc("Contact the drag racing calculator suite about sponsorships, feedback, or partnerships."),
        CANONICAL=esc(f"{ORIGIN}/contact.html"),
        VERIFICATION=VERIFICATION,
        ORIGIN=ORIGIN,
        CONTENT=content,
        FOOTER=footer(),
    )


def privacy_page():
    content = """
<h1>Privacy Policy &amp; Affiliate Disclosure</h1>
<p>Last updated: October 2026</p>
<h2>1. FTC Affiliate Disclosure</h2>
<p>In compliance with FTC guidelines, please assume that any links leading to products or services on this website are affiliate links. Ultimate Drag Racing Calculator Suite may receive monetary compensation from merchants (such as Summit Racing, Jegs, or Amazon) when visitors click on these links and complete a qualifying purchase, at no additional cost to the buyer.</p>
<h2>2. Information We Collect</h2>
<p>Our calculators operate entirely client-side in your web browser. Numerical values you enter (such as horsepower, gear ratios, and tire diameters) are processed locally by JavaScript and are never stored or transmitted to our servers.</p>
<h2>3. Cookies &amp; Analytics</h2>
<p>We may use standard analytics tools or hosting providers (such as GitHub Pages) that collect anonymous telemetry data (such as browser type, referral URLs, and visit timestamps) to help us improve site speed and performance.</p>
"""
    return fill(
        NARROW_TEMPLATE,
        TITLE=esc("Privacy Policy & Affiliate Disclosure | DragCalculators.com"),
        DESCRIPTION=esc("Privacy policy and affiliate disclosure for the drag racing calculator suite."),
        CANONICAL=esc(f"{ORIGIN}/privacy.html"),
        VERIFICATION=VERIFICATION,
        ORIGIN=ORIGIN,
        CONTENT=content,
        FOOTER=footer(),
    )


def sitemap(pages):
    entries = [
        ("index.html", "1.0"),
        ("contact.html", "0.5"),
        ("privacy.html", "0.5"),
    ]
    for page in pages:
        priority = "0.8" if page["role"] == "hub" else "0.6"
        entries.append((f"{page['slug']}.html", priority))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for filename, priority in entries:
        loc = esc(f"{ORIGIN}/{filename}")
        lines.append("    <url>")
        lines.append(f"        <loc>{loc}</loc>")
        lines.append("        <changefreq>weekly</changefreq>")
        lines.append(f"        <priority>{priority}</priority>")
        lines.append("    </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def main():
    pages = load_pages(CSV_PATH)
    hubs = [page for page in pages if page["role"] == "hub"]
    hubs_by_category = {page["category"]: page for page in hubs}
    if not any(page["slug"] == "transmission-shift-recovery-calculator" for page in pages):
        raise SystemExit("CSV is missing transmission-shift-recovery-calculator, which the master hub embeds")

    write("styles.css", STYLES)
    write("google9e7c88791a3f2f72.html", "google-site-verification: google9e7c88791a3f2f72.html\n")
    write("contact.html", contact_page())
    write("privacy.html", privacy_page())
    write("index.html", index_page(pages, hubs))
    for page in pages:
        write(f"{page['slug']}.html", fill(PAGE_TEMPLATE, **page_tokens(page, pages, hubs, hubs_by_category)))
    write("sitemap.xml", sitemap(pages))

    counts = {}
    for page in pages:
        counts[page["category"]] = counts.get(page["category"], 0) + 1
    summary = ", ".join(f"{category} {counts[category]}" for category in sorted(counts))
    print(f"Built {len(pages)} calculator pages ({len(hubs)} hubs) from pseo_pages_list.csv")
    print(summary)
    print(f"Sitemap URLs: {len(pages) + 3}")


if __name__ == "__main__":
    main()
