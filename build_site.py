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
    --bg-dark: #0f1015;
    --card-bg: #181a20;
    --accent-red: #ff1e27;
    --text-main: #f8f9fa;
    --text-muted: #9ca3af;
    --border-color: #2d3139;
    --input-bg: #21242c;
    --ok: #10b981;
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
    grid-template-columns: 240px minmax(320px, 480px) 1fr;
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
    border-radius: 12px;
    padding: 15px;
}
.nav-list { display: flex; flex-direction: column; gap: 4px; }
.nav-item {
    display: block;
    padding: 8px 10px;
    color: var(--text-muted);
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.78rem;
    border-left: 3px solid transparent;
}
.nav-item.active {
    background: var(--input-bg);
    border-left-color: var(--accent-red);
    color: var(--text-main);
    font-weight: 600;
}
.nav-item:hover { background: var(--input-bg); color: var(--text-main); }
.sticky-calculator, .content-box, .narrow-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 25px;
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
    color: var(--accent-red);
    font-size: 1.15rem;
    text-transform: uppercase;
    margin: 0 0 6px;
}
.spec, .content-box p, .narrow-card p { color: var(--text-muted); font-size: 0.9rem; }
.spec { font-size: 0.82rem; margin: 0; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }
label { display: block; margin-bottom: 2px; font-weight: 600; font-size: 0.72rem; color: var(--text-muted); }
input, select, textarea {
    width: 100%;
    padding: 7px 9px;
    background: var(--input-bg);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    border-radius: 6px;
    font-size: 0.82rem;
    font-family: inherit;
}
textarea { min-height: 120px; resize: vertical; }
.results-box {
    margin-top: 10px;
    background: #121418;
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--accent-red);
    padding: 10px;
    border-radius: 6px;
    font-size: 0.82rem;
}
.action-btn {
    width: 100%;
    margin-top: 10px;
    background: var(--accent-red);
    color: white;
    border: none;
    padding: 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.75rem;
    cursor: pointer;
    text-transform: uppercase;
}
.action-btn:hover { background: #e0161f; }
table { width: 100%; margin-top: 12px; border-collapse: collapse; background: #121418; }
th, td { padding: 5px 4px; border: 1px solid var(--border-color); text-align: center; font-size: 0.72rem; }
th { background: #1f232b; color: var(--accent-red); text-transform: uppercase; font-size: 0.62rem; }
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
.narrow-card h1 { color: var(--accent-red); font-size: 1.3rem; text-transform: uppercase; margin-top: 0; }
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
    .grid-2 { grid-template-columns: 1fr; }
    .sticky-calculator, .content-box, .narrow-card { padding: 16px; }
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


def transmission_html(row):
    current = field(row, "transmission", "th400")
    groups = []
    for label, keys in TRANSMISSION_GROUPS:
        opts = options([(key, TRANSMISSIONS[key][0]) for key in keys], current)
        groups.append(f'<optgroup label="{esc(label)}">\n{opts}\n</optgroup>')
    return f"""
    <div class="grid-2">
        <div><label for="trans">Transmission Profile</label>
            <select id="trans">
                {''.join(groups)}
            </select>
        </div>
        <div><label for="max-rpm">Max Shift RPM</label><input type="number" id="max-rpm" value="{esc(field(row, 'rpm', '7500'))}" step="100"></div>
    </div>
    <div class="grid-2">
        <div><label for="tire-dia">Tire Diameter (in)</label><input type="number" id="tire-dia" value="{esc(field(row, 'tire_diameter', '28.0'))}" step="0.1"></div>
        <div><label for="rear-gear">Rear Gear Ratio</label><input type="number" id="rear-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
    <div class="grid-2">
        <div><label for="veh-wt">Vehicle Weight (lbs)</label><input type="number" id="veh-wt" value="3200" step="50"></div>
        <div><label for="veh-hp">Flywheel HP</label><input type="number" id="veh-hp" value="{esc(field(row, 'hp', '1100'))}" step="25"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Track Sheet</button>
    <table>
        <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
        <tbody id="gear-body"></tbody>
    </table>
"""


DRIVETRAIN_SCRIPT = """
const ratios = %%RATIOS%%;
function calcAll() {
    let tKey = document.getElementById("trans").value;
    let rat = ratios[tKey] || [2.48, 1.48, 1.00];
    let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
    let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
    let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
    let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
    let hp = parseFloat(document.getElementById("veh-hp").value) || 1100;
    let rollout = (tire * Math.PI).toFixed(1);
    let estEt = (5.825 * Math.pow(wt / hp, 0.333)).toFixed(2);
    let estTrap = (234 * Math.cbrt(hp / wt)).toFixed(1);
    document.getElementById("results").innerHTML = "Est. 1/4 Mile ET: " + estEt + "s @ " + estTrap + " MPH | Rollout: " + rollout + " in | 1st Gear: " + (rat[0] * gear).toFixed(2) + ":1";
    let tbody = document.getElementById("gear-body");
    if (tbody) {
        tbody.innerHTML = "";
        for (let i = 0; i < rat.length; i++) {
            let overall = rat[i] * gear;
            let speed = (rpm * tire) / (overall * 336);
            let trapRpm = Math.round((parseFloat(estTrap) * overall * 336) / tire);
            let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i + 1] / rat[i])) + " RPM" : "Finish: " + trapRpm + " RPM";
            tbody.innerHTML += "<tr><td>Gear " + (i + 1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
        }
    }
}
["trans", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp"].forEach(id => {
    let el = document.getElementById(id);
    if (el) el.addEventListener("input", calcAll);
});
calcAll();
""".replace(
    "%%RATIOS%%",
    json.dumps({key: ratios for key, (_label, ratios) in TRANSMISSIONS.items()}),
)


def turbo_html(row):
    fuel = field(row, "fuel", "e85")
    count = field(row, "turbo_count", "1")
    fuel_options = options([(value, label) for _key, value, label in TURBO_FUELS], dict((key, value) for key, value, _label in TURBO_FUELS)[fuel])
    count_options = options([("1", "Single"), ("2", "Twin")], count)
    return f"""
    <p class="tool-note">Turbocharger airflow and pressure-ratio matching</p>
    <div class="grid-2">
        <div><label for="tu-hp">Target Flywheel HP</label><input type="number" id="tu-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div><label for="tu-boost">Target Boost (PSI)</label><input type="number" id="tu-boost" value="{esc(field(row, 'boost', '22'))}" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label for="tu-bsfc">Fuel BSFC</label><select id="tu-bsfc">{fuel_options}</select></div>
        <div><label for="tu-count">Turbo Count</label><select id="tu-count">{count_options}</select></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Turbo Match Sheet</button>
"""


TURBO_SCRIPT = """
function calcTurbo() {
    let hp = parseFloat(document.getElementById("tu-hp").value) || 1000;
    let boost = parseFloat(document.getElementById("tu-boost").value) || 22;
    let bsfc = parseFloat(document.getElementById("tu-bsfc").value) || 0.85;
    let count = parseInt(document.getElementById("tu-count").value, 10) || 1;
    let totalAirflow = (hp * bsfc) / 6.0;
    let perTurbo = totalAirflow / count;
    let pr = (boost + 14.7) / 14.7;
    let rec = perTurbo < 45 ? "T4 62-67mm class" : (perTurbo < 75 ? "T4 76-83mm class" : "T6 88-94mm+ class");
    document.getElementById("results").innerHTML = "Total Airflow: <strong>" + totalAirflow.toFixed(1) + " lb/min</strong> (" + perTurbo.toFixed(1) + " per turbo)<br>Pressure Ratio: <strong>" + pr.toFixed(2) + ":1</strong> | Match: <strong>" + rec + "</strong>";
}
["tu-hp", "tu-boost", "tu-bsfc", "tu-count"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcTurbo); el.addEventListener("change", calcTurbo); }
});
calcTurbo();
"""


def suspension_html(_row):
    return """
    <p class="tool-note">10-point chassis geometry</p>
    <div class="grid-2">
        <div><label for="l1">1. Vehicle Wheelbase (in)</label><input type="number" id="l1" value="110.0" step="0.5"></div>
        <div><label for="l2">2. Crankshaft Height (in)</label><input type="number" id="l2" value="24.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div><label for="l3">3. Axle Centerline to Rear Top Hole (in)</label><input type="number" id="l3" value="4.0" step="0.1"></div>
        <div><label for="l4">4. Ground to Rear Top Hole Center (in)</label><input type="number" id="l4" value="18.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label for="l5">5. Axle Centerline to Rear Bottom Hole (in)</label><input type="number" id="l5" value="4.0" step="0.1"></div>
        <div><label for="l6">6. Ground to Rear Bottom Hole Center (in)</label><input type="number" id="l6" value="10.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label for="l7">7. Axle Centerline to Front Top Hole (in)</label><input type="number" id="l7" value="32.0" step="0.5"></div>
        <div><label for="l8">8. Ground to Front Top Hole Center (in)</label><input type="number" id="l8" value="20.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div><label for="l9">9. Axle Centerline to Front Bottom Hole (in)</label><input type="number" id="l9" value="32.0" step="0.5"></div>
        <div><label for="l10">10. Ground to Front Bottom Hole Center (in)</label><input type="number" id="l10" value="11.0" step="0.5"></div>
    </div>
    <div class="results-box" id="results">
        <div>Instant Center Length: <span id="ic-len">0"</span></div>
        <div>Instant Center Height: <span id="ic-ht">0"</span></div>
        <div>Anti-Squat: <span id="as-pct">0%</span></div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Chassis Setup Sheet</button>
"""


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
    let icLenEl = document.getElementById("ic-len");
    let icHtEl = document.getElementById("ic-ht");
    let asPctEl = document.getElementById("as-pct");
    if (icLenEl) icLenEl.textContent = icLen.toFixed(1) + '"';
    if (icHtEl) icHtEl.textContent = icHt.toFixed(1) + '"';
    if (asPctEl) asPctEl.textContent = antiSquat + "%";
}
["l1","l2","l3","l4","l5","l6","l7","l8","l9","l10"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcTool); el.addEventListener("change", calcTool); }
});
calcTool();
"""


def exhaust_html(row):
    return f"""
    <p class="tool-note">Header primary tube and turbo downpipe sizing</p>
    <div class="grid-2">
        <div><label for="ex-cid">Engine Displacement (CID)</label><input type="number" id="ex-cid" value="400" step="5"></div>
        <div><label for="ex-cyl">Cylinders</label><input type="number" id="ex-cyl" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label for="ex-rpm">Peak RPM</label><input type="number" id="ex-rpm" value="{esc(field(row, 'rpm', '6500'))}" step="100"></div>
        <div><label for="ex-dur">Exhaust Duration (deg)</label><input type="number" id="ex-dur" value="240" step="5"></div>
    </div>
    <div class="grid-2">
        <div><label for="ex-layout">Layout</label>
            <select id="ex-layout">
                <option value="na">Naturally Aspirated Headers</option>
                <option value="turbo" selected>Turbo Manifold / Downpipe</option>
            </select>
        </div>
        <div><label for="ex-hp">Target HP (turbo pipe)</label><input type="number" id="ex-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Exhaust Spec Sheet</button>
"""


EXHAUST_SCRIPT = """
function calcExhaust() {
    let cid = parseFloat(document.getElementById("ex-cid").value) || 400;
    let cyl = parseFloat(document.getElementById("ex-cyl").value) || 8;
    let rpm = parseFloat(document.getElementById("ex-rpm").value) || 6500;
    let dur = parseFloat(document.getElementById("ex-dur").value) || 240;
    let layout = document.getElementById("ex-layout").value;
    let hp = parseFloat(document.getElementById("ex-hp").value) || 1000;
    let primaryId = Math.sqrt((cid / cyl) * rpm / 88200);
    let primaryLen = (dur * 850 / rpm) - 3;
    let collector = layout === "turbo" ? Math.sqrt(hp / 220) : primaryId * 1.75;
    let label = layout === "turbo" ? "Turbo Downpipe ID" : "Collector ID";
    document.getElementById("results").innerHTML = "Primary ID: <strong>" + primaryId.toFixed(2) + " in</strong> | Primary Length: <strong>" + primaryLen.toFixed(1) + " in</strong><br>" + label + ": <strong>" + collector.toFixed(2) + " in</strong>";
}
["ex-cid", "ex-cyl", "ex-rpm", "ex-dur", "ex-layout", "ex-hp"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcExhaust); el.addEventListener("change", calcExhaust); }
});
calcExhaust();
"""


def supercharger_html(row):
    kind = field(row, "blower_type", "twin-screw")
    factor = {key: value for key, value, _label in BLOWER_OPTIONS}[kind]
    blower_options = options([(value, label) for _key, value, label in BLOWER_OPTIONS], factor)
    return f"""
    <p class="tool-note">Pulley ratio and estimated boost</p>
    <div class="grid-2">
        <div><label for="sc-crank">Crank Pulley Dia (in)</label><input type="number" id="sc-crank" value="{esc(field(row, 'crank_pulley', '8.0'))}" step="0.1"></div>
        <div><label for="sc-blower">Blower Pulley Dia (in)</label><input type="number" id="sc-blower" value="{esc(field(row, 'blower_pulley', '3.0'))}" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label for="sc-rpm">Max Crank RPM</label><input type="number" id="sc-rpm" value="{esc(field(row, 'rpm', '6500'))}" step="100"></div>
        <div><label for="sc-fac">Blower Type Factor</label><select id="sc-fac">{blower_options}</select></div>
    </div>
    <div class="grid-2">
        <div><label for="sc-target">Target Boost (PSI, optional)</label><input type="number" id="sc-target" value="{esc(cell(row, 'boost'))}" step="0.5"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Pulley Spec Sheet</button>
"""


SUPERCHARGER_SCRIPT = """
function calcSupercharger() {
    let crank = parseFloat(document.getElementById("sc-crank").value) || 8.0;
    let blower = parseFloat(document.getElementById("sc-blower").value) || 3.0;
    let rpm = parseFloat(document.getElementById("sc-rpm").value) || 6500;
    let factor = parseFloat(document.getElementById("sc-fac").value) || 1.45;
    let ratio = crank / Math.max(blower, 0.1);
    let impellerRpm = Math.round(rpm * ratio);
    let estBoost = ratio * 5.2 * factor;
    let targetRaw = document.getElementById("sc-target").value;
    let targetLine = "";
    if (targetRaw !== "") {
        let target = parseFloat(targetRaw);
        if (isFinite(target)) {
            targetLine = "<br>Target boost: <strong>" + target.toFixed(1) + " PSI</strong> | Difference: <strong>" + (estBoost - target).toFixed(1) + " PSI</strong>";
        }
    }
    document.getElementById("results").innerHTML = "Pulley Ratio: <strong>" + ratio.toFixed(2) + ":1</strong> | Impeller RPM: <strong>" + impellerRpm.toLocaleString() + "</strong><br>Est. Boost: <strong>" + estBoost.toFixed(1) + " PSI</strong>" + targetLine;
}
["sc-crank", "sc-blower", "sc-rpm", "sc-fac", "sc-target"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcSupercharger); el.addEventListener("change", calcSupercharger); }
});
calcSupercharger();
"""


def rear_gear_html(row):
    return f"""
    <p class="tool-note">Finish RPM and trap speed from ring and pinion</p>
    <div class="grid-2">
        <div><label for="rg-trap">Target Trap Speed (MPH)</label><input type="number" id="rg-trap" value="125" step="1"></div>
        <div><label for="rg-gear">Rear Gear Ratio</label><input type="number" id="rg-gear" value="{esc(field(row, 'rear_gear', '4.11'))}" step="0.01"></div>
    </div>
    <div class="grid-2">
        <div><label for="rg-tire">Tire Diameter (in)</label><input type="number" id="rg-tire" value="{esc(field(row, 'tire_diameter', '32.0'))}" step="0.1"></div>
        <div><label for="rg-final">Trans Final Ratio</label><input type="number" id="rg-final" value="1.00" step="0.01"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Rear Gear Sheet</button>
"""


REAR_GEAR_SCRIPT = """
function calcRearGear() {
    let trap = parseFloat(document.getElementById("rg-trap").value) || 125;
    let gear = parseFloat(document.getElementById("rg-gear").value) || 4.11;
    let tire = parseFloat(document.getElementById("rg-tire").value) || 32;
    let transFinal = parseFloat(document.getElementById("rg-final").value) || 1.00;
    let overall = gear * transFinal;
    let finishRpm = (trap * overall * 336) / Math.max(tire, 0.1);
    let rollout = (tire * Math.PI).toFixed(1);
    let mphAt7500 = (7500 * tire) / (overall * 336);
    document.getElementById("results").innerHTML = "Overall Ratio: <strong>" + overall.toFixed(2) + ":1</strong> | Rollout: <strong>" + rollout + " in</strong><br>Finish RPM: <strong>" + Math.round(finishRpm) + " RPM</strong> | 7500 RPM Trap: <strong>" + mphAt7500.toFixed(1) + " MPH</strong>";
}
["rg-trap", "rg-gear", "rg-tire", "rg-final"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcRearGear); el.addEventListener("change", calcRearGear); }
});
calcRearGear();
"""


def tire_html(row):
    return f"""
    <p class="tool-note">Slick growth, dynamic diameter, and finish RPM</p>
    <div class="grid-2">
        <div><label for="tg-dia">Static Tire Dia (in)</label><input type="number" id="tg-dia" value="{esc(field(row, 'tire_diameter', '28.0'))}" step="0.1"></div>
        <div><label for="tg-trap">Trap Speed (MPH)</label><input type="number" id="tg-trap" value="150" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label for="tg-growth">Growth Factor (%)</label><input type="number" id="tg-growth" value="{esc(field(row, 'growth', '4.5'))}" step="0.1"></div>
        <div><label for="tg-gear">Rear Gear Ratio</label><input type="number" id="tg-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Tire Growth Sheet</button>
"""


TIRE_SCRIPT = """
function calcTireGrowth() {
    let staticDia = parseFloat(document.getElementById("tg-dia").value) || 28;
    let trap = parseFloat(document.getElementById("tg-trap").value) || 150;
    let growth = parseFloat(document.getElementById("tg-growth").value) || 4.5;
    let gear = parseFloat(document.getElementById("tg-gear").value) || 3.42;
    let dynamicDia = staticDia * (1 + (growth / 100));
    let staticRollout = (staticDia * Math.PI).toFixed(1);
    let dynamicRollout = (dynamicDia * Math.PI).toFixed(1);
    let estFinishRpm = Math.round((trap * gear * 336) / dynamicDia);
    document.getElementById("results").innerHTML = "Static Rollout: <strong>" + staticRollout + " in</strong> | Dynamic Dia: <strong>" + dynamicDia.toFixed(2) + " in</strong><br>Dynamic Rollout: <strong>" + dynamicRollout + " in</strong> | Est. Finish RPM: <strong>" + estFinishRpm + " RPM</strong>";
}
["tg-dia", "tg-trap", "tg-growth", "tg-gear"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcTireGrowth); el.addEventListener("change", calcTireGrowth); }
});
calcTireGrowth();
"""


def wastegate_html(row):
    return f"""
    <p class="tool-note">External wastegate diameter and bypass flow</p>
    <div class="grid-2">
        <div><label for="wg-hp">Target Flywheel HP</label><input type="number" id="wg-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div><label for="wg-boost">Target Boost (PSI)</label><input type="number" id="wg-boost" value="{esc(field(row, 'boost', '22'))}" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label for="wg-count">Number of Gates</label>
            <select id="wg-count">
                <option value="1" selected>Single Gate</option>
                <option value="2">Twin Gates</option>
            </select>
        </div>
        <div><label for="wg-style">Gate Style</label>
            <select id="wg-style">
                <option value="1.00">Internal WG (restricted)</option>
                <option value="1.25" selected>External WG</option>
            </select>
        </div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Wastegate Spec Sheet</button>
"""


WASTEGATE_SCRIPT = """
function calcWastegate() {
    let hp = parseFloat(document.getElementById("wg-hp").value) || 1000;
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
    document.getElementById("results").innerHTML = "Bypass Fraction: <strong>" + (bypassFrac * 100).toFixed(0) + "%</strong> | Flow per Gate: <strong>" + wgFlow.toFixed(1) + " lb/min</strong><br>Recommended Gate: <strong>" + rec + " mm</strong> (" + count + " x " + rec + " mm)";
}
["wg-hp", "wg-boost", "wg-count", "wg-style"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcWastegate); el.addEventListener("change", calcWastegate); }
});
calcWastegate();
"""


def fuel_html(row):
    fuel = field(row, "fuel", "gasoline")
    fuel_value = {key: value for key, value, _label in INJECTOR_FUELS}[fuel]
    fuel_options = options([(value, label) for _key, value, label in INJECTOR_FUELS], fuel_value)
    return f"""
    <p class="tool-note">Injector flow rate at the target horsepower</p>
    <div class="grid-2">
        <div><label for="fi-hp">Target Crank HP</label><input type="number" id="fi-hp" value="{esc(field(row, 'hp', '1000'))}" step="50"></div>
        <div><label for="fi-inj">Number of Injectors</label><input type="number" id="fi-inj" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label for="fi-ind">Induction Type</label>
            <select id="fi-ind">
                <option value="0.50">Naturally Aspirated</option>
                <option value="0.65" selected>Turbocharged / Supercharged</option>
            </select>
        </div>
        <div><label for="fi-fuel">Fuel Type</label><select id="fi-fuel">{fuel_options}</select></div>
    </div>
    <div class="grid-2">
        <div><label for="fi-dc">Max Duty Cycle (%)</label><input type="number" id="fi-dc" value="80" step="5"></div>
        <div><label for="fi-pressure">Pressure Offset</label><input id="fi-pressure" type="text" value="Standard (43.5 PSI)" disabled></div>
    </div>
    <div class="results-box" id="results">
        <div>Required flow rate per injector</div>
        <div><span id="fi-cc">0.0</span> cc/min</div>
        <div><span id="fi-lbs">0.0 lb/hr</span></div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Injector Spec Sheet</button>
"""


FUEL_SCRIPT = """
function calcInjector() {
    let hp = parseFloat(document.getElementById("fi-hp").value) || 1000;
    let count = parseFloat(document.getElementById("fi-inj").value) || 8;
    let ind = parseFloat(document.getElementById("fi-ind").value) || 0.65;
    let fuel = parseFloat(document.getElementById("fi-fuel").value) || 0.65;
    let bsfc = fuel * (ind / 0.65);
    let dc = (parseFloat(document.getElementById("fi-dc").value) || 80) / 100;
    let totalLbHr = (hp * bsfc) / dc;
    let perInjectorLbHr = totalLbHr / count;
    let perInjectorCcMin = perInjectorLbHr * 10.5;
    let ccEl = document.getElementById("fi-cc");
    let lbsEl = document.getElementById("fi-lbs");
    if (ccEl) ccEl.textContent = perInjectorCcMin.toFixed(1);
    if (lbsEl) lbsEl.textContent = perInjectorLbHr.toFixed(1) + " lb/hr";
}
["fi-hp", "fi-inj", "fi-ind", "fi-fuel", "fi-dc"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcInjector); el.addEventListener("change", calcInjector); }
});
calcInjector();
"""


def electrical_html(_row):
    return """
    <p class="tool-note">Relay, fuse, and chassis wire gauge</p>
    <div class="grid-2">
        <div><label for="rl-watts">Load Power (Watts)</label><input type="number" id="rl-watts" value="240" step="10"></div>
        <div><label for="rl-volts">System Voltage</label>
            <select id="rl-volts">
                <option value="12" selected>12V Chassis</option>
                <option value="13.8">13.8V Running</option>
                <option value="16">16V Race</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div><label for="rl-duty">Duty</label>
            <select id="rl-duty">
                <option value="1.25" selected>Continuous (1.25x)</option>
                <option value="1.10">Intermittent (1.10x)</option>
            </select>
        </div>
        <div><label for="rl-len">One-Way Wire Length (ft)</label><input type="number" id="rl-len" value="12" step="1"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Wiring Spec Sheet</button>
"""


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
    document.getElementById("results").innerHTML = "Load Current: <strong>" + amps.toFixed(1) + " A</strong> | Design Current: <strong>" + designAmps.toFixed(1) + " A</strong><br>Relay: <strong>" + relay + " A</strong> | Fuse: <strong>" + fuse + " A</strong> | Wire: <strong>" + awg + " AWG</strong>";
}
["rl-watts", "rl-volts", "rl-duty", "rl-len"].forEach(id => {
    let el = document.getElementById(id);
    if (el) { el.addEventListener("input", calcRelay); el.addEventListener("change", calcRelay); }
});
calcRelay();
"""


def cas_html(row):
    return f"""
    <p class="tool-note">Gauge boost, absolute pressure, and pressure ratio</p>
    <div class="grid-2">
        <div><label for="cas-boost">Target Boost (PSI)</label><input type="number" id="cas-boost" value="{esc(field(row, 'boost', '20'))}" step="1"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Boost Sheet</button>
"""


CAS_SCRIPT = """
function calcCas() {
    let boost = parseFloat(document.getElementById("cas-boost").value);
    if (!isFinite(boost) || boost < 0) boost = 0;
    let absolute = boost + 14.7;
    let pr = absolute / 14.7;
    document.getElementById("results").innerHTML = "Gauge boost: <strong>" + boost.toFixed(1) + " PSI</strong><br>Absolute pressure: <strong>" + absolute.toFixed(1) + " PSI</strong> | Pressure ratio: <strong>" + pr.toFixed(2) + ":1</strong>";
}
let casBoost = document.getElementById("cas-boost");
if (casBoost) {
    casBoost.addEventListener("input", calcCas);
    casBoost.addEventListener("change", calcCas);
}
calcCas();
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
        "Pressure Ratio = (Boost PSI + 14.7) / 14.7",
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
        "SCRIPT": script,
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
        SCRIPT=script,
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
