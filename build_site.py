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
    "4l60e": ("4L60E (3.06 / 1.62 / 1.00 / 0.70)", [3.06, 1.62, 1.00, 0.70]),
    "c4_c6": ("Ford C4 / C6 (2.46 / 1.46 / 1.00)", [2.46, 1.46, 1.00]),
    "aod": ("AOD (2.40 / 1.47 / 1.00 / 0.67)", [2.40, 1.47, 1.00, 0.67]),
    "t56": ("T56 (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50)", [2.66, 1.78, 1.30, 1.00, 0.74, 0.50]),
    "zf8hp": (
        "ZF 8HP70 (4.71 / 3.14 / 2.11 / 1.67 / 1.29 / 1.00 / 0.84 / 0.67)",
        [4.714, 3.143, 2.106, 1.667, 1.285, 1.000, 0.839, 0.667],
    ),
}
TRANSMISSION_GROUPS = [
    ("GM Automatic", ["th400", "powerglide", "th350", "4l60e"]),
    ("Ford Automatic", ["c4_c6", "aod"]),
    ("Manual", ["t56"]),
    ("ZF Automatic", ["zf8hp"]),
]
TRANS_SHORT = {
    "powerglide": "Powerglide (2-Speed)",
    "th400": "TH400",
    "th350": "TH350",
    "4l60e": "4L60E",
    "c4_c6": "Ford C4 / C6",
    "aod": "AOD",
    "t56": "T56 Manual (6-Speed)",
    "zf8hp": "ZF8HP",
}
FUEL_LABEL = {"gasoline": "gasoline", "e85": "E85", "methanol": "methanol"}
BLOWER_LABEL = {
    "roots": "roots blower",
    "twin-screw": "twin-screw blower",
    "centrifugal": "centrifugal blower",
}
TURBO_FUELS = [
    ("gasoline", "0.60", "Gasoline (0.60)"),
    ("e85", "0.85", "E85 (0.85)"),
    ("methanol", "1.50", "Methanol (1.50)"),
]
INJECTOR_FUELS = [
    ("gasoline", "0.65", "Gasoline (BSFC ~0.65)"),
    ("e85", "1.10", "E85 Ethanol (BSFC ~1.10)"),
    ("methanol", "1.50", "Methanol (BSFC ~1.50)"),
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
.variant-list { list-style: none; padding: 0; margin: 0; max-height: 420px; overflow: auto; }
.variant-list a {
    display: block;
    padding: 6px 0;
    border-bottom: 1px dashed var(--border-color);
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.82rem;
}
.variant-list a:hover { color: var(--text-main); }
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
        case "cc":
            return { text: n.toFixed(1), suffix: "cc/min" };
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


def calculator_shell(primary, advanced, print_label, extra="", power_toggle=False):
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
    <button type="button" class="action-btn" onclick="window.print()">{esc(print_label)}</button>
    {extra}
"""


def transmission_html(row):
    current = field(row, "transmission", "th400")
    groups = []
    for label, keys in TRANSMISSION_GROUPS:
        opts = options([(key, TRANSMISSIONS[key][0]) for key in keys], current)
        groups.append(f'<optgroup label="{esc(label)}">\n{opts}\n</optgroup>')
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="trans">Transmission</label><select id="trans">{''.join(groups)}</select></div>
        <div class="field"><label for="rear-gear">Rear gear</label><input type="number" id="rear-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
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
function calcAll() {
    let tKey = document.getElementById("trans").value;
    let rat = ratios[tKey] || [2.48, 1.48, 1.00];
    let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
    let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
    let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
    let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
    let hp = crankHorsepower(document.getElementById("veh-hp").value || 1100);
    let rollout = tire * Math.PI;
    let estEt = 5.825 * Math.pow(wt / Math.max(hp, 1), 0.333);
    let estTrap = 234 * Math.cbrt(hp / Math.max(wt, 1));
    publishReadout([
        { label: "Quarter-mile ET", value: estEt, unit: "sec", primary: true },
        { label: "Trap speed", value: estTrap, unit: "mph" },
        { label: "Rollout", value: rollout, unit: "in" },
        { label: "1st gear overall", value: rat[0] * gear, unit: "ratio" }
    ]);
    let tbody = document.getElementById("gear-body");
    if (tbody) {
        tbody.innerHTML = "";
        for (let i = 0; i < rat.length; i++) {
            let overall = rat[i] * gear;
            let speed = (rpm * tire) / (overall * 336);
            let trapRpm = Math.round((estTrap * overall * 336) / tire);
            let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i + 1] / rat[i])) + " RPM" : "Finish: " + trapRpm + " RPM";
            tbody.innerHTML += "<tr><td>Gear " + (i + 1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + reading(speed, "mph") + "</td><td>" + drop + "</td></tr>";
        }
    }
}
bindCalc(calcAll, ["trans", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp", "dt-loss"]);
""".replace(
    "%%RATIOS%%",
    json.dumps({key: ratios for key, (_label, ratios) in TRANSMISSIONS.items()}),
)


def turbo_html(row):
    fuel = field(row, "fuel", "e85")
    count = field(row, "turbo_count", "1")
    fuel_options = options([(value, label) for _key, value, label in TURBO_FUELS], dict((key, value) for key, value, _label in TURBO_FUELS)[fuel])
    count_options = options([("1", "Single"), ("2", "Twin")], count)
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="tu-hp">Power</label><input type="number" id="tu-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div class="field"><label for="tu-boost">Target boost (PSI)</label><input type="number" id="tu-boost" value="{esc(field(row, 'boost', '22'))}" step="1"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="tu-bsfc">Fuel BSFC</label><select id="tu-bsfc">{fuel_options}</select></div>
        <div class="field"><label for="tu-count">Turbo count</label><select id="tu-count">{count_options}</select></div>
    </div>
    {LOSS_FIELDS}
    """
    return calculator_shell(primary, advanced, "Print turbo match sheet", power_toggle=True)


TURBO_SCRIPT = """
function calcTurbo() {
    let hp = crankHorsepower(document.getElementById("tu-hp").value || 1000);
    let boost = parseFloat(document.getElementById("tu-boost").value) || 22;
    let bsfc = parseFloat(document.getElementById("tu-bsfc").value) || 0.85;
    let count = parseInt(document.getElementById("tu-count").value, 10) || 1;
    let totalAirflow = (hp * bsfc) / 6.0;
    let perTurbo = totalAirflow / count;
    let pr = (boost + 14.7) / 14.7;
    let rec = perTurbo < 45 ? "T4 62-67mm class" : (perTurbo < 75 ? "T4 76-83mm class" : "T6 88-94mm+ class");
    publishReadout([
        { label: "Airflow per turbo", value: perTurbo, unit: "lbmin", primary: true },
        { label: "Total airflow", value: totalAirflow, unit: "lbmin" },
        { label: "Pressure ratio", value: pr, unit: "ratio" },
        { label: "Compressor class", value: rec, unit: "text" }
    ]);
}
bindCalc(calcTurbo, ["tu-hp", "tu-boost", "tu-bsfc", "tu-count", "dt-loss"]);
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
    fuel_value = {key: value for key, value, _label in INJECTOR_FUELS}[fuel]
    fuel_options = options([(value, label) for _key, value, label in INJECTOR_FUELS], fuel_value)
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="fi-hp">Power</label><input type="number" id="fi-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div class="field"><label for="fi-inj">Injector count</label><input type="number" id="fi-inj" value="8" step="1"></div>
    </div>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="fi-ind">Induction</label>
            <select id="fi-ind">
                <option value="0.50">Naturally aspirated</option>
                <option value="0.65" selected>Turbocharged / supercharged</option>
            </select>
        </div>
        <div class="field"><label for="fi-fuel">Fuel</label><select id="fi-fuel">{fuel_options}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="fi-dc">Max duty cycle (%)</label><input type="number" id="fi-dc" value="80" step="5"></div>
        <div class="field"><label for="fi-pressure">Pressure offset</label><input id="fi-pressure" type="text" value="Standard (43.5 PSI)" disabled></div>
    </div>
    {LOSS_FIELDS}
    """
    return calculator_shell(primary, advanced, "Print injector spec sheet", power_toggle=True)


FUEL_SCRIPT = """
function calcInjector() {
    let hp = crankHorsepower(document.getElementById("fi-hp").value || 1000);
    let count = parseFloat(document.getElementById("fi-inj").value) || 8;
    let ind = parseFloat(document.getElementById("fi-ind").value) || 0.65;
    let fuel = parseFloat(document.getElementById("fi-fuel").value) || 0.65;
    let bsfc = fuel * (ind / 0.65);
    let dc = (parseFloat(document.getElementById("fi-dc").value) || 80) / 100;
    let totalLbHr = (hp * bsfc) / dc;
    let perInjectorLbHr = totalLbHr / count;
    let perInjectorCcMin = perInjectorLbHr * 10.5;
    publishReadout([
        { label: "Flow per injector", value: perInjectorCcMin, unit: "cc", primary: true },
        { label: "Mass flow", value: perInjectorLbHr, unit: "lbhr" },
        { label: "Total flow", value: totalLbHr, unit: "lbhr" }
    ]);
}
bindCalc(calcInjector, ["fi-hp", "fi-inj", "fi-ind", "fi-fuel", "fi-dc", "dt-loss"]);
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
        "Overall Ratio = Trans Ratio x Rear Gear | Shift Speed (MPH) = (RPM x Tire) / (Overall x 336)",
        transmission_html,
        DRIVETRAIN_SCRIPT,
    ),
    "Turbo": (
        "Airflow (lb/min) = (HP x BSFC) / 6 | Pressure Ratio = (Boost PSI + 14.7) / 14.7",
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
        "Injector lb/hr = (Flywheel HP x BSFC) / (Max Duty Cycle x Injector Count). cc/min = lb/hr x 10.5.",
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


def related_box(page, pages, hubs_by_category):
    links = []
    hub = hubs_by_category.get(page["category"])
    if page["role"] == "hub":
        links.extend(variants_for(page["category"], pages))
        title = "Configurations"
        intro = f"<p>{len(links)} saved combinations for this calculator.</p>" if links else ""
    else:
        if hub:
            links.append(hub)
        links.extend(neighbor_pages(page, pages))
        title = "Related calculators"
        intro = ""
    listing = link_items(links)
    if not listing:
        return ""
    return content_box(title, intro + listing)


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
        "CONTENT": formula_box(formula) + related_box(page, pages, hubs_by_category),
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
