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
# GA4 measurement ID. Empty keeps the tag off every page.
ANALYTICS_ID = "G-VXS2PPLZ20"
# One line on the printed setup sheet. Empty keeps the sheet as a planning printout.
SPONSOR_LINE = ""
# Merchant URLs by category, filled in after an affiliate program approves the site.
# Example: "FuelPump": (("Dual 450 class", "https://example.com/pump"),)
AFFILIATE_LINKS = {}
PRINT_LINE = SPONSOR_LINE or "Setup sheet from dragcalculators.com. These are planning numbers. Confirm the part before you order."
SITE_BANNER = ""
NEXT_STEPS = {
    "Fuel": (("fuel-pump-calculator", "Size the pump for this power"),),
    "FuelPump": (
        ("fuel-injector-calculator", "Size the injectors this pump has to feed"),
        ("carburetor-cfm-calculator", "Size the carburetor when the pump is mechanical"),
        ("automotive-relay-calculator", "Size the relay and the wire for the pump"),
    ),
    "Nitrous": (
        ("fuel-injector-calculator", "Check the injectors when the shot is dry"),
        ("fuel-pump-calculator", "Size the pump for the engine plus the shot"),
    ),
    "Shock": (("four-link-suspension-calculator", "Set the 4-link this shock has to control"),),
    "Suspension": (("drag-shock-calculator", "Choose the shock for this rear suspension"),),
    "Converter": (("transmission-shift-recovery-calculator", "Put this slip into the gear calculator"),),
    "Transmission": (("torque-converter-calculator", "Pick the converter stall, then come back to the slip"),),
    "Turbo": (
        ("fuel-pump-calculator", "Size the pump for this boost"),
        ("wastegate-sizing-calculator", "Size the wastegate for this power"),
    ),
    "Cooling": (
        ("race-car-wiring-calculator", "Add the fan and the water pump to the power budget"),
        ("automotive-relay-calculator", "Size the relay and the wire for the fan"),
    ),
    "Power": (("automotive-relay-calculator", "Size one circuit from this budget"),),
    "Electrical": (("race-car-wiring-calculator", "Add the whole car up before sizing one relay"),),
    "Driveline": (("transmission-shift-recovery-calculator", "The top gear here is the shaft speed"),),
    "Carb": (("fuel-pump-calculator", "Size the mechanical pump for this carburetor"),),
    "Compression": (("ls-engine-builder", "Put this compression on the LS build"),),
    "Cam": (("ls-engine-builder", "Match the head and the RPM on the LS build"),),
}
# Catalog ring-and-pinion sets. The ratio list is what that housing is actually sold in.
# bands are (max ratio, carrier note). deep is an extra note at and above that ratio.
GEAR_HOUSINGS = (
    {
        "id": "ford9",
        "label": "Ford 9-inch",
        "search": "Ford 9 inch",
        "ratios": [3.00, 3.25, 3.40, 3.50, 3.55, 3.70, 3.73, 3.89, 4.00, 4.11, 4.30, 4.56, 4.71, 4.86, 5.00, 5.14, 5.43, 5.67, 5.83, 6.00],
        "bands": [(99, "A Ford 9-inch has no carrier break. The set bolts into the third member. Axle spline does not change the ring and pinion.")],
    },
    {
        "id": "ford88",
        "label": "Ford 8.8",
        "search": "Ford 8.8",
        "ratios": [3.08, 3.31, 3.55, 3.73, 3.90, 4.10, 4.30, 4.56, 4.88, 5.13, 5.71],
        "bands": [(99, "A Ford 8.8 has no carrier break. A 28-spline axle and a 31-spline axle take the same ring and pinion.")],
        "deep": (4.56, "A 4.56 and deeper can hit a stock cover. A deep cover clears the ring gear."),
    },
    {
        "id": "gm12car",
        "label": "GM 12-bolt car",
        "search": "GM 12 bolt car",
        "ratios": [3.08, 3.31, 3.42, 3.55, 3.73, 3.90, 4.10, 4.56, 4.88, 5.14],
        "bands": [
            (3.73, "This set uses the 3.07 to 3.73 carrier."),
            (3.90, "A 3.90 sits on the carrier break. Match the carrier to the set."),
            (99, "This set uses the 4.10-and-up carrier."),
        ],
    },
    {
        "id": "gm12truck",
        "label": "GM 12-bolt truck",
        "search": "GM 12 bolt truck",
        "ratios": [3.08, 3.42, 3.73, 4.10, 4.56],
        "bands": [
            (3.42, "This set uses the 2.76 to 3.42 carrier."),
            (99, "This set uses the 3.73-and-up carrier."),
        ],
    },
    {
        "id": "gm85",
        "label": "GM 8.5-inch 10-bolt",
        "search": "GM 8.5 10 bolt",
        "ratios": [3.08, 3.42, 3.73, 4.10, 4.56, 4.88, 5.13],
        "bands": [(99, "This set uses the 2.73-and-up carrier. A 2.56 carrier will not take it.")],
    },
    {
        "id": "dana60",
        "label": "Dana 60",
        "search": "Dana 60",
        "ratios": [3.54, 3.73, 4.10, 4.56, 4.88, 5.13, 5.38],
        "bands": [
            (4.10, "This set uses the 4.10-and-down carrier."),
            (99, "This set uses the 4.56-and-up carrier."),
        ],
    },
    {
        "id": "dana44",
        "label": "Dana 44",
        "search": "Dana 44",
        "ratios": [3.54, 3.73, 4.09, 4.56, 4.88, 5.13],
        "bands": [
            (3.73, "This set uses the 3.73-and-down carrier."),
            (99, "This set uses the 3.92-and-up carrier."),
        ],
    },
    {
        "id": "mopar875",
        "label": "Mopar 8.75",
        "search": "Mopar 8.75",
        "ratios": [3.55, 3.73, 3.91, 4.10, 4.30, 4.56, 4.86, 5.13],
        "bands": [(99, "Match the set to the case number cast in the center. 489 is the drag case. 741 is the weak case.")],
    },
)
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
    "LS": [],
    "FuelPump": ["hp", "boost", "fuel"],
    "Nitrous": [],
    "Shock": [],
    "Converter": [],
    "Electrical": [],
    "CAS": ["boost"],
    "Cooling": ["hp"],
    "Driveline": [],
    "Power": [],
    "Carb": [],
    "Compression": [],
    "Cam": [],
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
MANUAL_TRANSMISSIONS = set(next(keys for label, keys in TRANSMISSION_GROUPS if label == "Manual"))
AUTO_CONVERTER_SLIP = "6"
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
PUMP_FUELS = [
    ("gasoline", "Gasoline (91/93)"),
    ("e85", "E85"),
    ("e98", "E98"),
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
    --page-pad: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg-dark);
    color: var(--text-main);
    margin: 0;
    padding: 0 var(--page-pad) 20px;
    line-height: 1.5;
}
.site-banner {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 0 calc(var(--page-pad) * -1) 16px;
    padding: 12px var(--page-pad);
    background: #0e0e0e;
    border-bottom: 3px solid var(--accent-red);
    position: sticky;
    top: 0;
    z-index: 40;
}
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
    color: var(--text-main);
    text-decoration: none;
}
.brand-mark {
    width: 38px;
    height: 38px;
    flex: none;
    display: grid;
    place-items: center;
    border-radius: 8px;
    background: var(--accent-red);
    color: #fff;
    font-weight: 800;
    letter-spacing: -0.04em;
}
.brand-copy { display: flex; flex-direction: column; line-height: 1.15; min-width: 0; }
.brand-copy strong { font-size: 1.05rem; letter-spacing: 0.01em; }
.brand-copy em { margin-top: 2px; font-style: normal; color: var(--text-muted); font-size: 0.72rem; }
.site-search { position: relative; flex: 1; min-width: 140px; max-width: 440px; margin-left: auto; }
.search-results {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    background: #1c1c1c;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}
.search-results a {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 10px 12px;
    color: var(--text-main);
    text-decoration: none;
    border-bottom: 1px solid var(--border-color);
}
.search-results a strong { font-size: 0.86rem; font-weight: 650; }
.search-results a span { color: var(--text-muted); font-size: 0.72rem; }
.search-results a:hover, .search-results a.active { background: #242424; }
.search-empty { margin: 0; padding: 12px; color: var(--text-muted); font-size: 0.85rem; }
.banner-cta {
    flex: none;
    color: #fff;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    text-decoration: none;
}
.banner-cta:hover { border-color: var(--accent-red); color: #fff; }
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}
.back-row { max-width: 1350px; margin: 0 auto; }
.back-link { color: var(--accent-red); font-weight: 700; font-size: 0.85rem; text-decoration: none; }
.layout-grid {
    max-width: 1350px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 240px minmax(340px, 520px) 1fr;
    gap: 25px;
    align-items: start;
}
.nexus-sidebar {
    position: sticky;
    top: 78px;
    max-height: 90vh;
    overflow: auto;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px;
}
.nav-list { display: flex; flex-direction: column; gap: 4px; }
.nav-group { margin: 12px 0 2px; }
.nav-group-label {
    margin: 0;
    padding: 4px 12px 2px;
    color: #6f6f6f;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
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
.sticky-calculator { display: flex; flex-direction: column; gap: 15px; min-width: 0; }
.content-column { display: flex; flex-direction: column; gap: 20px; min-width: 0; }
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
.measure-fig { margin: 0 0 14px; }
.measure-fig svg { width: 100%; height: auto; display: block; background: #141414; border: 1px solid var(--border-color); border-radius: 10px; }
.measure-fig figcaption { margin-top: 8px; color: var(--text-muted); font-size: 0.8rem; line-height: 1.45; }
.table-scroll { overflow-x: auto; max-width: 100%; padding: 8px; }
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
.action-row { display: flex; flex-direction: column; gap: 8px; }
.setup-mail { display: flex; flex-direction: column; gap: 8px; }
.setup-mail-row { display: flex; gap: 8px; align-items: center; }
.setup-mail-row input { flex: 1; }
.setup-mail-row .action-btn { width: auto; margin: 0; padding: 0 16px; height: 42px; }
.action-secondary { background: transparent; color: var(--text-main); border: 1px solid var(--border-color); }
.action-secondary:hover { background: #242424; }
.next-steps { display: flex; flex-direction: column; gap: 8px; }
.next-steps a { color: var(--text-main); font-weight: 650; text-decoration: none; }
.next-steps a:hover { color: var(--accent-red); }
.gear-shop { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
.gear-shop p { margin: 0; }
.gear-shop a { color: var(--text-main); font-weight: 650; text-decoration: none; }
.gear-shop a:hover { color: var(--accent-red); }
.shop-note { color: var(--text-muted); font-size: 0.78rem; }
.print-sheet { display: none; }
@media print {
    .site-banner, .nexus-sidebar, .content-column, .back-row, .site-footer, .action-row, .setup-mail, .pill-row, .next-steps, .accordion { display: none !important; }
    .gear-shop, .gear-shop a, .gear-shop .shop-note { color: #111 !important; }
    .print-sheet { display: block; margin-top: 18px; color: #111; font-size: 0.85rem; }
    body, .sticky-calculator, .readout, .table-scroll, .assess, th, td { background: #fff !important; color: #111 !important; }
}
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
.narrow { max-width: 720px; margin: 0 auto 20px; }
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
    body { --page-pad: 12px; padding: 0 var(--page-pad) 12px; }
    .site-banner { flex-wrap: wrap; }
    .site-search { order: 3; flex-basis: 100%; max-width: none; margin-left: 0; }
    .grid-2, .readout-grid, .setup-mail-row { grid-template-columns: 1fr; }
    .setup-mail-row { display: grid; }
    .setup-mail-row .action-btn { width: 100%; }
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
    <meta property="og:image" content="{{ORIGIN}}/share-card.jpg">
    <meta property="og:image:secure_url" content="{{ORIGIN}}/share-card.jpg">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="DragCalculators">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{TITLE}}">
    <meta name="twitter:description" content="{{DESCRIPTION}}">
    <meta name="twitter:image" content="{{ORIGIN}}/share-card.jpg">
    <link rel="stylesheet" href="styles.css">
{{ANALYTICS}}</head>
<body>
    {{BANNER}}
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
    <meta property="og:image" content="{{ORIGIN}}/share-card.jpg">
    <meta property="og:image:secure_url" content="{{ORIGIN}}/share-card.jpg">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="DragCalculators">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{{ORIGIN}}/share-card.jpg">
    <link rel="stylesheet" href="styles.css">
{{ANALYTICS}}</head>
<body>
    {{BANNER}}
    <div class="narrow">
        <a href="index.html" class="back-link">&larr; Start here</a>
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
    if row["category"] == "LS":
        return "Loaded defaults: " + ls_preset(row["slug"])["spec"] + "."
    if row["category"] == "Nitrous":
        return "Loaded defaults: " + n2o_preset(row["slug"])["spec"] + "."
    if row["category"] == "Shock":
        return "Loaded defaults: " + shock_preset(row["slug"])["spec"] + "."
    if row["category"] == "Converter":
        return "Loaded defaults: " + cv_preset(row["slug"])["spec"] + "."
    if row["category"] == "Cooling":
        hp = cell(row, "hp") or "1000"
        return f"Loaded defaults: {hp} HP, water, engine running in the lanes."
    if row["category"] == "Driveline":
        return "Loaded defaults: 48 in center to center, 3.50 x 0.125 aluminum, 7,000 RPM in 1.00."
    if row["category"] == "Power":
        return "Loaded defaults: dual in-tank pump, 16 in fan, 55 GPM water pump, battery in the trunk."
    if row["category"] == "Carb":
        return "Loaded defaults: 383 cubic inches, 6,500 RPM, 90% volumetric efficiency, street/strip."
    if row["category"] == "Compression":
        return "Loaded defaults: 4.030 bore, 3.750 stroke, 64 cc chamber."
    if row["category"] == "Cam":
        return "Loaded defaults: 364 cubic inches, 243 cathedral head, naturally aspirated, street/strip, 6,200 RPM."
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
        case "in3":
            return metric ? { text: (n * 25.4).toFixed(2), suffix: "mm" } : { text: n.toFixed(3), suffix: "in" };
        case "psi":
            return metric ? { text: (n * 0.0689476).toFixed(2), suffix: "bar" } : { text: n.toFixed(1), suffix: "PSI" };
        case "lbmin":
            return metric ? { text: (n * 0.453592).toFixed(2), suffix: "kg/min" } : { text: n.toFixed(1), suffix: "lb/min" };
        case "cfm":
            return metric ? { text: (n * 0.0283168).toFixed(2), suffix: "m3/min" } : { text: Math.round(n).toLocaleString("en-US"), suffix: "CFM" };
        case "tempf":
            return metric ? { text: ((n - 32) * 5 / 9).toFixed(0), suffix: "C" } : { text: Math.round(n).toString(), suffix: "F" };
        case "deltaf":
            return metric ? { text: (n * 5 / 9).toFixed(1), suffix: "C" } : { text: n.toFixed(1), suffix: "F" };
        case "gpm":
            return metric ? { text: (n * 3.78541).toFixed(1), suffix: "L/min" } : { text: n.toFixed(1), suffix: "GPM" };
        case "deg":
            return { text: n.toFixed(1) + "\u00b0", suffix: "" };
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
        case "ci":
            return metric ? { text: (n * 0.0163871).toFixed(2), suffix: "L" } : { text: n.toFixed(1), suffix: "ci" };
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

function applySharedState(ids) {
    const params = new URLSearchParams(location.search);
    if (!params.toString()) return;
    ids.forEach(id => {
        if (!params.has(id)) return;
        const el = document.getElementById(id);
        if (!el) return;
        el.value = params.get(id);
    });
    ["power", "system"].forEach(group => {
        if (!params.has(group)) return;
        unitState[group] = params.get(group);
        document.querySelectorAll('[data-unit-group="' + group + '"]').forEach(pill => {
            pill.classList.toggle("active", pill.dataset.unit === unitState[group]);
        });
    });
}

function setupSearch() {
    const params = new URLSearchParams();
    (window.shareIds || []).forEach(id => {
        const el = document.getElementById(id);
        if (!el || el.value === "") return;
        params.set(id, el.value);
    });
    if (unitState.power !== "bhp") params.set("power", unitState.power);
    if (unitState.system !== "imperial") params.set("system", unitState.system);
    return params.toString();
}

function bindCalc(fn, ids) {
    window.shareIds = ids;
    applySharedState(ids);
    const run = () => fn();
    window.refreshCalc = run;
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener("input", run);
        el.addEventListener("change", run);
    });
    run();
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

function copyText(text) {
    const legacy = () => {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.top = "0";
        area.style.left = "0";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.focus();
        area.select();
        let ok = false;
        try { ok = document.execCommand("copy"); } catch (err) { ok = false; }
        area.remove();
        return ok;
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text).catch(() => (legacy() ? undefined : Promise.reject()));
    }
    return legacy() ? Promise.resolve() : Promise.reject();
}

const copySetup = document.getElementById("copy-setup");
if (copySetup) {
    copySetup.addEventListener("click", () => {
        const search = setupSearch();
        const url = location.origin + location.pathname + (search ? "?" + search : "");
        const done = (label) => {
            copySetup.textContent = label;
            setTimeout(() => { copySetup.textContent = "Copy link to this setup"; }, 1600);
        };
        copyText(url).then(() => done("Link copied")).catch(() => {
            window.prompt("Copy this setup link", url);
            done("Link ready");
        });
    });
}

function setupSummary() {
    const lines = [];
    const title = document.querySelector(".master-header h1");
    if (title) lines.push(title.textContent.trim());
    lastReadout.forEach(item => {
        lines.push(item.label + ": " + reading(item.value, item.unit));
    });
    const search = setupSearch();
    const url = location.origin + location.pathname + (search ? "?" + search : "");
    lines.push(url);
    return { url: url, text: lines.join("\n") };
}

const setupMail = document.getElementById("setup-mail");
if (setupMail) {
    setupMail.addEventListener("submit", (event) => {
        event.preventDefault();
        const email = document.getElementById("setup-email");
        const note = document.getElementById("setup-mail-note");
        const button = setupMail.querySelector("button");
        const summary = setupSummary();
        const address = email ? email.value.trim() : "";
        if (!address || !button) return;
        button.disabled = true;
        fetch("https://formspree.io/f/xqppzgab", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                email: address,
                inquiry_type: "Setup sheet",
                setup_url: summary.url,
                message: summary.text,
                _subject: "Setup sheet from dragcalculators.com"
            })
        }).then(response => {
            if (!response.ok) throw new Error("send failed");
            if (note) note.textContent = "Sent. This setup is in the DragCalculators inbox with your email on it.";
            setupMail.reset();
        }).catch(() => {
            if (note) note.textContent = "That send did not go through. The contact page takes the same setup.";
        }).finally(() => {
            button.disabled = false;
        });
    });
}
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
    <div class="action-row">
        <button type="button" class="action-btn" onclick="window.print()">{esc(print_label)}</button>
        <button type="button" class="action-btn action-secondary" id="copy-setup">Copy link to this setup</button>
    </div>
    <form class="setup-mail" id="setup-mail">
        <label for="setup-email">Email this setup</label>
        <div class="setup-mail-row">
            <input id="setup-email" type="email" name="email" required placeholder="you@example.com" autocomplete="email">
            <button type="submit" class="action-btn">Send</button>
        </div>
        <p class="field-hint" id="setup-mail-note">Sends the numbers on this page, and the address above, to DragCalculators.</p>
    </form>
    <p class="print-sheet">{esc(PRINT_LINE)}</p>
    {extra}
"""


def gear_housing_field(select_id):
    opts = "".join(
        f'<option value="{esc(house["id"])}">{esc(house["label"])}</option>'
        for house in GEAR_HOUSINGS
    )
    return (
        f'<div class="field"><label for="{esc(select_id)}">Rear end</label>'
        f'<select id="{esc(select_id)}">{opts}</select></div>'
    )


def gear_shop_mount(mount_id):
    return f'<div id="{esc(mount_id)}" class="gear-shop"></div>'


GEAR_SHOP_FN = """
const GEAR_HOUSINGS = %%HOUSES%%;
function gearHouse(selectId) {
    const pick = document.getElementById(selectId);
    const key = pick ? pick.value : "";
    for (let i = 0; i < GEAR_HOUSINGS.length; i++) {
        if (GEAR_HOUSINGS[i].id === key) return GEAR_HOUSINGS[i];
    }
    return GEAR_HOUSINGS[0];
}
function nearestGear(ratios, gear) {
    let best = ratios[0];
    let bestDist = Math.abs(gear - best);
    for (let i = 1; i < ratios.length; i++) {
        const dist = Math.abs(gear - ratios[i]);
        if (dist < bestDist) {
            best = ratios[i];
            bestDist = dist;
        }
    }
    return best;
}
function gearNote(house, ratio) {
    let note = "";
    const bands = house.bands || [];
    for (let i = 0; i < bands.length; i++) {
        if (ratio <= bands[i][0] + 0.001) {
            note = bands[i][1];
            break;
        }
    }
    if (house.deep && ratio >= house.deep[0] - 0.001) note += " " + house.deep[1];
    return note;
}
function renderGearShop(mountId, selectId, gear, offer) {
    const mount = document.getElementById(mountId);
    if (!mount) return;
    const house = gearHouse(selectId);
    const set = nearestGear(house.ratios, gear);
    const shown = set.toFixed(2);
    const typed = Number(gear).toFixed(2);
    const lead = Math.abs(set - gear) >= 0.005
        ? typed + " is not a catalog " + house.label + " set. The set to order is the " + shown + "."
        : "The set to order is the " + house.label + " " + shown + " ring and pinion.";
    const q = encodeURIComponent(house.search + " " + shown + " ring and pinion");
    const summit = "https://www.summitracing.com/search?keyword=" + q;
    const jegs = "https://www.jegs.com/search?Ntt=" + q;
    let use = "";
    if (offer && Math.abs(offer.ratio - gear) >= 0.005) {
        use = '<button type="button" class="action-btn action-secondary" id="gear-use">Use the ' + offer.ratio.toFixed(2) + " for this trap</button>";
    }
    mount.innerHTML = "<p>" + lead + " " + gearNote(house, set) + "</p>"
        + use
        + '<a href="' + summit + '" target="_blank" rel="noopener">Summit Racing, ' + house.label + " " + shown + "</a>"
        + '<a href="' + jegs + '" target="_blank" rel="noopener">Jegs, ' + house.label + " " + shown + "</a>"
        + '<p class="shop-note">The link searches that housing and ratio. Confirm the carrier before you order. Bearings and shims are a separate install kit.</p>';
    const button = document.getElementById("gear-use");
    if (button && offer) {
        button.addEventListener("click", function () {
            const input = document.getElementById(offer.inputId);
            if (input) input.value = offer.ratio.toFixed(2);
            if (window.refreshCalc) window.refreshCalc();
        });
    }
}
""".replace(
    "%%HOUSES%%",
    json.dumps([
        {
            "id": house["id"],
            "label": house["label"],
            "search": house["search"],
            "ratios": house["ratios"],
            "bands": [list(band) for band in house["bands"]],
            "deep": list(house["deep"]) if house.get("deep") else None,
        }
        for house in GEAR_HOUSINGS
    ]),
)


def transmission_html(row):
    current = field(row, "transmission", "th400")
    groups = ['<option value="custom">Custom ratios</option>']
    for label, keys in TRANSMISSION_GROUPS:
        opts = options([(key, TRANSMISSIONS[key][0]) for key in keys], current)
        groups.append(f'<optgroup label="{esc(label)}">\n{opts}\n</optgroup>')
    slip_default = "0" if current in MANUAL_TRANSMISSIONS else AUTO_CONVERTER_SLIP
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="trans">Transmission</label><select id="trans">{''.join(groups)}</select></div>
        <div class="field"><label for="rear-gear">Rear gear</label><input type="number" id="rear-gear" value="{esc(field(row, 'rear_gear', '3.42'))}" step="0.01"></div>
    </div>
    {gear_housing_field("rear-end")}
    <p class="field-hint">The ring and pinion is cut for one housing. A 4.11 for a Ford 9-inch does not fit an 8.8 or a 12-bolt.</p>
    <div class="grid-2">
        <div class="field"><label for="custom-ratios">Custom ratios</label><input type="text" id="custom-ratios" placeholder="2.48, 1.48, 1.00" inputmode="decimal" autocomplete="off"></div>
        <div class="field"><label for="converter-slip">Converter slip (%)</label><input type="number" id="converter-slip" value="{slip_default}" min="0" max="40" step="0.5"></div>
    </div>
    <p class="field-hint">An automatic starts at {AUTO_CONVERTER_SLIP}% slip, the usual converter at the shift. A manual or a locked converter starts at 0%. Type any slip you want after the transmission is chosen.</p>
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
    return calculator_shell(
        primary, advanced, "Print track sheet", table, power_toggle=True, results_extra=gear_shop_mount("gear-shop")
    )


DRIVETRAIN_SCRIPT = GEAR_SHOP_FN + """
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
    renderGearShop("gear-shop", "rear-end", gear);
}
const manualTrans = new Set(%%MANUALS%%);
const transPick = document.getElementById("trans");
const slipPick = document.getElementById("converter-slip");
function standardSlip(value) {
    if (value === "custom") return null;
    return manualTrans.has(value) ? "0" : "%%SLIP%%";
}
if (transPick && slipPick) {
    transPick.addEventListener("change", () => {
        const next = standardSlip(transPick.value);
        if (next !== null) slipPick.value = next;
    });
}
bindCalc(calcAll, ["trans", "custom-ratios", "converter-slip", "max-rpm", "tire-dia", "rear-gear", "rear-end", "veh-wt", "veh-hp", "dt-loss"]);
""".replace(
    "%%RATIOS%%",
    json.dumps({key: ratios for key, (_label, ratios) in TRANSMISSIONS.items()}),
).replace(
    "%%MANUALS%%",
    json.dumps(sorted(MANUAL_TRANSMISSIONS)),
).replace("%%SLIP%%", AUTO_CONVERTER_SLIP)


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



FOUR_LINK_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 340" role="img" aria-label="Where to measure a four link">
        <line x1="40" y1="280" x2="690" y2="280" stroke="#3a3a3a" stroke-width="2"/>
        <circle cx="110" cy="230" r="48" fill="none" stroke="#6f6f6f" stroke-width="3"/>
        <circle cx="110" cy="230" r="8" fill="#f5f5f5"/>
        <circle cx="560" cy="210" r="62" fill="none" stroke="#6f6f6f" stroke-width="3"/>
        <circle cx="560" cy="210" r="10" fill="#f5f5f5"/>
        <text x="92" y="168" fill="#a3a3a3" font-size="13">Front</text>
        <text x="536" y="130" fill="#a3a3a3" font-size="13">Rear axle</text>
        <line x1="250" y1="168" x2="430" y2="150" stroke="#e50914" stroke-width="4"/>
        <line x1="250" y1="214" x2="430" y2="196" stroke="#f5f5f5" stroke-width="4"/>
        <circle cx="520" cy="146" r="5" fill="#e50914"/>
        <circle cx="520" cy="198" r="5" fill="#f5f5f5"/>
        <circle cx="250" cy="168" r="5" fill="#e50914"/>
        <circle cx="250" cy="214" r="5" fill="#f5f5f5"/>
        <line x1="560" y1="210" x2="520" y2="146" stroke="#e50914" stroke-width="1"/>
        <line x1="560" y1="210" x2="520" y2="198" stroke="#f5f5f5" stroke-width="1"/>
        <text x="470" y="78" fill="#e50914" font-size="13">Rear top hole</text>
        <text x="470" y="96" fill="#a3a3a3" font-size="12">Forward of the axle, and up from the ground</text>
        <text x="150" y="78" fill="#e50914" font-size="13">Front top hole</text>
        <text x="150" y="96" fill="#a3a3a3" font-size="12">Forward of the axle, and up from the ground</text>
        <text x="150" y="318" fill="#f5f5f5" font-size="13">Front bottom hole is the lower bar. Rear bottom hole is at the axle.</text>
        <line x1="110" y1="292" x2="560" y2="292" stroke="#e50914" stroke-width="1.5"/>
        <text x="280" y="310" fill="#e50914" font-size="13">Wheelbase, spindle to axle</text>
        <line x1="300" y1="280" x2="300" y2="188" stroke="#a3a3a3" stroke-width="1.5" stroke-dasharray="4 3"/>
        <circle cx="300" cy="188" r="4" fill="#a3a3a3"/>
        <text x="308" y="186" fill="#a3a3a3" font-size="13">Crank height, off the ground</text>
    </svg>
    <figcaption>Every hole gets two numbers. One is how far it sits forward of the rear-axle center. The other is how far it sits off the ground. Take both with the car at ride height. The red bar is the top link. The white bar is the bottom link.</figcaption>
</figure>
"""

SHOCK_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 300" role="img" aria-label="How to measure a shock">
        <circle cx="120" cy="42" r="16" fill="none" stroke="#f5f5f5" stroke-width="3"/>
        <line x1="120" y1="58" x2="120" y2="214" stroke="#e50914" stroke-width="8" stroke-linecap="round"/>
        <circle cx="120" cy="232" r="16" fill="none" stroke="#f5f5f5" stroke-width="3"/>
        <text x="156" y="48" fill="#f5f5f5" font-size="16">Extended</text>
        <text x="156" y="130" fill="#a3a3a3" font-size="14">Center of the top eye</text>
        <text x="156" y="150" fill="#a3a3a3" font-size="14">to center of the bottom eye</text>
        <circle cx="430" cy="78" r="16" fill="none" stroke="#f5f5f5" stroke-width="3"/>
        <line x1="430" y1="94" x2="430" y2="176" stroke="#e50914" stroke-width="8" stroke-linecap="round"/>
        <circle cx="430" cy="194" r="16" fill="none" stroke="#f5f5f5" stroke-width="3"/>
        <text x="466" y="84" fill="#f5f5f5" font-size="16">Collapsed</text>
        <text x="466" y="140" fill="#a3a3a3" font-size="14">Same two centers,</text>
        <text x="466" y="160" fill="#a3a3a3" font-size="14">shock fully short</text>
        <text x="40" y="276" fill="#a3a3a3" font-size="14">Ride height is the same measurement with the car at race weight.</text>
    </svg>
    <figcaption>Measure the mounts, not the tire. Full bump is the short length against the bump stop. Full droop is the long length on the strap or at full hang. The shock you order stays 1/2 in short of bump and 1/2 in longer than droop, so the shock is not the travel stop.</figcaption>
</figure>
"""

RELAY_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 340" role="img" aria-label="Four pin and five pin relay wiring">
        <rect x="270" y="70" width="180" height="150" rx="12" fill="#1c1c1c" stroke="#e50914" stroke-width="2"/>
        <text id="rl-fig-relay" x="360" y="108" fill="#f5f5f5" font-size="16" text-anchor="middle">30 A relay</text>
        <text x="300" y="150" fill="#a3a3a3" font-size="13">85 ground</text>
        <text x="300" y="172" fill="#a3a3a3" font-size="13">86 switch</text>
        <text x="390" y="150" fill="#e50914" font-size="13">30 power</text>
        <text x="390" y="172" fill="#f5f5f5" font-size="13">87 load</text>
        <text x="330" y="200" fill="#6f6f6f" font-size="12">87a unused</text>
        <line x1="80" y1="146" x2="270" y2="146" stroke="#e50914" stroke-width="3"/>
        <rect x="150" y="128" width="70" height="36" rx="6" fill="none" stroke="#e50914" stroke-width="2"/>
        <text id="rl-fig-fuse" x="185" y="151" fill="#f5f5f5" font-size="13" text-anchor="middle">30 A</text>
        <text x="40" y="120" fill="#f5f5f5" font-size="14">Battery</text>
        <line x1="450" y1="168" x2="620" y2="168" stroke="#f5f5f5" stroke-width="3"/>
        <text x="560" y="150" fill="#f5f5f5" font-size="14">Pump or fan</text>
        <text id="rl-fig-load" x="560" y="204" fill="#a3a3a3" font-size="13">20 A load</text>
        <line x1="300" y1="220" x2="300" y2="280" stroke="#6f6f6f" stroke-width="2"/>
        <text x="250" y="300" fill="#a3a3a3" font-size="13">Chassis ground</text>
        <line x1="340" y1="220" x2="340" y2="260" stroke="#a3a3a3" stroke-width="2"/>
        <text x="360" y="268" fill="#a3a3a3" font-size="13">Small switch, 18 AWG</text>
        <text id="rl-fig-wire" x="360" y="40" fill="#e50914" font-size="15" text-anchor="middle">12 AWG on pins 30 and 87</text>
    </svg>
    <figcaption>Pin 30 is battery power, and the fuse sits at the source on that wire. Pin 87 feeds the pump or fan with the same gauge. Pin 86 is the switch. Pin 85 is ground. A relay with a diode inside wants 86 on power and 85 on ground. Pin 87a is the normally closed pin and stays empty on a fan or a pump.</figcaption>
</figure>
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
    return calculator_shell(FOUR_LINK_DIAGRAM + primary, advanced, "Print chassis setup sheet")


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
    {gear_housing_field("rg-end")}
    <p class="field-hint">Pick the rear end in the car. The link opens that ring and pinion. The target RPM names the set that hits it.</p>
    <div class="grid-2">
        <div class="field"><label for="rg-gear">Rear gear</label><input type="number" id="rg-gear" value="{esc(field(row, 'rear_gear', '4.11'))}" step="0.01"></div>
        <div class="field"><label for="rg-tire">Tire diameter (in)</label><input type="number" id="rg-tire" value="{esc(field(row, 'tire_diameter', '32.0'))}" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="rg-trap">Target trap speed (MPH)</label><input type="number" id="rg-trap" value="125" step="1"></div>
        <div class="field"><label for="rg-rpm">Target finish RPM</label><input type="number" id="rg-rpm" value="7200" step="100"></div>
    </div>
    """
    advanced = """
    <div class="field"><label for="rg-final">Trans final ratio</label><input type="number" id="rg-final" value="1.00" step="0.01"></div>
    """
    return calculator_shell(primary, advanced, "Print rear gear sheet", results_extra=gear_shop_mount("rg-shop"))


REAR_GEAR_SCRIPT = GEAR_SHOP_FN + """
function calcRearGear() {
    let trap = parseFloat(document.getElementById("rg-trap").value) || 125;
    let gear = parseFloat(document.getElementById("rg-gear").value) || 4.11;
    let tire = parseFloat(document.getElementById("rg-tire").value) || 32;
    let transFinal = parseFloat(document.getElementById("rg-final").value) || 1.00;
    let targetRpm = parseFloat(document.getElementById("rg-rpm").value) || 7200;
    tire = Math.max(tire, 0.1);
    trap = Math.max(trap, 1);
    transFinal = Math.max(transFinal, 0.1);
    let overall = gear * transFinal;
    let finishRpm = (trap * overall * 336) / tire;
    let rollout = tire * Math.PI;
    let mphAt7500 = (7500 * tire) / (overall * 336);
    const house = gearHouse("rg-end");
    const wanted = (targetRpm * tire) / (trap * transFinal * 336);
    const set = nearestGear(house.ratios, wanted);
    const setRpm = (trap * set * transFinal * 336) / tire;
    publishReadout([
        { label: "Finish RPM", value: finishRpm, unit: "rpm", primary: true },
        { label: "Set for the target RPM", value: set.toFixed(2) + " " + house.label, unit: "text" },
        { label: "That set at the trap", value: setRpm, unit: "rpm" },
        { label: "Overall ratio", value: overall, unit: "ratio" },
        { label: "Rollout", value: rollout, unit: "in" },
        { label: "Speed at 7,500 RPM", value: mphAt7500, unit: "mph" }
    ]);
    renderGearShop("rg-shop", "rg-end", gear, { inputId: "rg-gear", ratio: set });
}
bindCalc(calcRearGear, ["rg-trap", "rg-gear", "rg-tire", "rg-final", "rg-end", "rg-rpm"]);
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
    primary = RELAY_DIAGRAM + """
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
    const fuseEl = document.getElementById("rl-fig-fuse");
    if (fuseEl) fuseEl.textContent = fuse + " A";
    const wireEl = document.getElementById("rl-fig-wire");
    if (wireEl) wireEl.textContent = awg + " AWG on pins 30 and 87";
    const loadEl = document.getElementById("rl-fig-load");
    if (loadEl) loadEl.textContent = amps.toFixed(1) + " A load";
    const relayEl = document.getElementById("rl-fig-relay");
    if (relayEl) relayEl.textContent = relay + " A relay";
}
bindCalc(calcRelay, ["rl-watts", "rl-volts", "rl-duty", "rl-len"]);
"""


COOLING_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 280" role="img" aria-label="Cooling air and coolant path on a drag car">
        <rect x="70" y="70" width="150" height="120" rx="8" fill="#1c1c1c" stroke="#f5f5f5" stroke-width="2"/>
        <text x="145" y="124" fill="#f5f5f5" font-size="14" text-anchor="middle">Radiator</text>
        <text x="145" y="146" fill="#a3a3a3" font-size="12" text-anchor="middle">Core face</text>
        <circle cx="40" cy="130" r="18" fill="none" stroke="#e50914" stroke-width="3"/>
        <text x="40" y="168" fill="#e50914" font-size="12" text-anchor="middle">Fan</text>
        <line x1="58" y1="130" x2="70" y2="130" stroke="#e50914" stroke-width="3"/>
        <rect x="300" y="78" width="200" height="104" rx="8" fill="#1c1c1c" stroke="#6f6f6f" stroke-width="2"/>
        <text x="400" y="124" fill="#f5f5f5" font-size="14" text-anchor="middle">Engine</text>
        <text x="400" y="146" fill="#a3a3a3" font-size="12" text-anchor="middle">Block and heads</text>
        <circle cx="560" cy="200" r="28" fill="none" stroke="#e50914" stroke-width="3"/>
        <text x="560" y="204" fill="#e50914" font-size="12" text-anchor="middle">Pump</text>
        <line x1="220" y1="100" x2="300" y2="100" stroke="#e50914" stroke-width="3"/>
        <line x1="500" y1="150" x2="532" y2="186" stroke="#f5f5f5" stroke-width="3"/>
        <line x1="540" y1="176" x2="250" y2="160" stroke="#f5f5f5" stroke-width="3"/>
        <text x="70" y="250" fill="#a3a3a3" font-size="14">The fan pulls only while the car is sitting. Ram air does the return road.</text>
    </svg>
    <figcaption>Air goes through the core, then the fan. Coolant leaves the bottom of the radiator, the pump pushes it through the block, and the hot water comes back to the top of the core. A shroud has to cover the core or the fan pulls air around it instead of through it.</figcaption>
</figure>
"""

DRIVESHAFT_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 300" role="img" aria-label="How to measure driveshaft length and angles">
        <rect x="40" y="78" width="120" height="70" rx="6" fill="#1c1c1c" stroke="#6f6f6f" stroke-width="2"/>
        <text x="100" y="110" fill="#f5f5f5" font-size="13" text-anchor="middle">Transmission</text>
        <text x="100" y="128" fill="#a3a3a3" font-size="12" text-anchor="middle">Tail down</text>
        <line x1="160" y1="130" x2="520" y2="168" stroke="#e50914" stroke-width="6"/>
        <circle cx="175" cy="132" r="8" fill="none" stroke="#f5f5f5" stroke-width="2"/>
        <circle cx="505" cy="166" r="8" fill="none" stroke="#f5f5f5" stroke-width="2"/>
        <rect x="530" y="120" width="140" height="80" rx="6" fill="#1c1c1c" stroke="#6f6f6f" stroke-width="2"/>
        <text x="600" y="156" fill="#f5f5f5" font-size="13" text-anchor="middle">Pinion yoke</text>
        <text x="600" y="176" fill="#a3a3a3" font-size="12" text-anchor="middle">Nose angle</text>
        <line x1="175" y1="200" x2="505" y2="200" stroke="#e50914" stroke-width="1.5"/>
        <line x1="175" y1="190" x2="175" y2="210" stroke="#e50914" stroke-width="1.5"/>
        <line x1="505" y1="190" x2="505" y2="210" stroke="#e50914" stroke-width="1.5"/>
        <text x="250" y="222" fill="#e50914" font-size="13">Center of joint to center of joint</text>
        <text x="40" y="262" fill="#f5f5f5" font-size="14">Angle finder on the tail, the tube, and the pinion yoke.</text>
        <text x="40" y="284" fill="#a3a3a3" font-size="14">Same finder direction. Down toward the rear of the car is negative.</text>
    </svg>
    <figcaption>Measure at ride height with the driver in the car. The length a shop orders is the center of the front U-joint to the center of the rear U-joint. At ride the slip yoke wants about 3/4 in before it bottoms. At full droop about 1 in of the yoke should still be in the transmission.</figcaption>
</figure>
"""

POWER_DIAGRAM = """
<figure class="measure-fig">
    <svg viewBox="0 0 720 280" role="img" aria-label="Trunk battery power distribution">
        <rect x="40" y="90" width="110" height="70" rx="8" fill="#1c1c1c" stroke="#e50914" stroke-width="2"/>
        <text x="95" y="122" fill="#f5f5f5" font-size="14" text-anchor="middle">Battery</text>
        <text x="95" y="142" fill="#a3a3a3" font-size="12" text-anchor="middle">Trunk</text>
        <rect x="190" y="104" width="70" height="42" rx="6" fill="none" stroke="#e50914" stroke-width="2"/>
        <text id="pw-fig-fuse" x="225" y="130" fill="#f5f5f5" font-size="13" text-anchor="middle">100 A</text>
        <line x1="150" y1="125" x2="190" y2="125" stroke="#e50914" stroke-width="3"/>
        <line x1="260" y1="125" x2="360" y2="125" stroke="#e50914" stroke-width="3"/>
        <rect x="360" y="86" width="130" height="78" rx="8" fill="#1c1c1c" stroke="#f5f5f5" stroke-width="2"/>
        <text x="425" y="118" fill="#f5f5f5" font-size="14" text-anchor="middle">Fuse panel</text>
        <text id="pw-fig-panel" x="425" y="140" fill="#a3a3a3" font-size="12" text-anchor="middle">6 AWG</text>
        <line x1="95" y1="160" x2="95" y2="210" stroke="#f5f5f5" stroke-width="3"/>
        <line x1="95" y1="210" x2="560" y2="210" stroke="#f5f5f5" stroke-width="3"/>
        <rect x="560" y="176" width="120" height="68" rx="8" fill="#1c1c1c" stroke="#6f6f6f" stroke-width="2"/>
        <text x="620" y="206" fill="#f5f5f5" font-size="14" text-anchor="middle">Alternator</text>
        <text id="pw-fig-charge" x="620" y="226" fill="#a3a3a3" font-size="12" text-anchor="middle">1/0 charge</text>
        <text x="40" y="260" fill="#a3a3a3" font-size="14">The main fuse is on the battery post. The starter cable is separate.</text>
    </svg>
    <figcaption>A trunk battery feeds the fuse panel on a short run and the alternator on a long run to the front. The fuse belongs at the battery, on the panel feed. The starter cable is a 1/0 or 2/0 for the inrush, and this page sizes the running loads rather than that hit.</figcaption>
</figure>
"""


def cooling_html(row):
    primary = f"""
    {COOLING_DIAGRAM}
    <div class="grid-2">
        <div class="field"><label for="cl-hp">Power</label><input type="number" id="cl-hp" value="{esc(field(row, 'hp', '1000'))}" min="50" step="25"></div>
        <div class="field"><label for="cl-fuel">Fuel</label>
            <select id="cl-fuel">
                <option value="gasoline" selected>Gasoline</option>
                <option value="e85">E85</option>
                <option value="methanol">Methanol</option>
                <option value="race">Race gas</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cl-ind">Induction</label>
            <select id="cl-ind">
                <option value="na">Naturally aspirated</option>
                <option value="boost" selected>Power adder</option>
            </select>
        </div>
        <div class="field"><label for="cl-mix">Coolant</label>
            <select id="cl-mix">
                <option value="water" selected>Water</option>
                <option value="5050">50/50 antifreeze</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cl-gal">Coolant in the system (gal)</label><input type="number" id="cl-gal" value="4" min="1" step="0.5"></div>
        <div class="field"><label for="cl-block">Block</label>
            <select id="cl-block">
                <option value="iron" selected>Iron block, aluminum heads</option>
                <option value="aluminum">Aluminum block and heads</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cl-pass">Pass length (seconds)</label><input type="number" id="cl-pass" value="10" min="4" step="0.5"></div>
        <div class="field"><label for="cl-wait">Wait before the next hit (minutes)</label><input type="number" id="cl-wait" value="8" min="1" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cl-run">Engine in the lanes</label>
            <select id="cl-run">
                <option value="yes" selected>Left running</option>
                <option value="no">Shut off</option>
            </select>
        </div>
        <div class="field"><label for="cl-mode">Water pump</label>
            <select id="cl-mode">
                <option value="both" selected>Mechanical on the hit, electric in the lanes</option>
                <option value="electric">Electric pump only</option>
            </select>
        </div>
    </div>
    <p class="field-hint">A 10-second pass does not put the dyno heat into the water. Most of that energy leaves in the exhaust. The fan's job is the heat that stayed, plus idle heat if the engine keeps running.</p>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="cl-share">Pass heat, share of fuel energy</label><input type="number" id="cl-share" value="0.06" min="0.02" max="0.25" step="0.01"></div>
        <div class="field"><label for="cl-idle-share">Idle heat, share of fuel energy</label><input type="number" id="cl-idle-share" value="0.40" min="0.1" max="0.7" step="0.05"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cl-rise">Coolant rise used to size the pump (°F)</label><input type="number" id="cl-rise" value="20" min="8" step="1"></div>
        <div class="field"><label for="cl-air">Air rise across the core (°F)</label><input type="number" id="cl-air" value="25" min="10" step="1"></div>
    </div>
    <div class="field"><label for="cl-idle">Idle fuel (gal/hr)</label><input type="number" id="cl-idle" placeholder="Auto" min="0.4" step="0.1"></div>
    <p class="field-hint">6% of the fuel energy into the metal and the water matches a car that climbs about 30°F on a 1,000 HP hit. A steady dyno pull is closer to 20%, and that number will oversize a drag radiator.</p>
    """
    assess = '<p class="assess" id="cl-assess"></p>'
    return calculator_shell(primary, advanced, "Print cooling sheet", power_toggle=True, results_extra=assess)


COOLING_SCRIPT = r"""
const CL_FUEL = {
    gasoline: { btu: 18500, dens: 6.17, na: 0.50, boost: 0.65 },
    e85: { btu: 12560, dens: 6.55, na: 0.75, boost: 0.95 },
    methanol: { btu: 8635, dens: 6.63, na: 0.95, boost: 1.20 },
    race: { btu: 18500, dens: 6.20, na: 0.55, boost: 0.70 }
};
const CL_FANS = [
    { cfm: 800, label: "10 in single", amps: 8 },
    { cfm: 1250, label: "12 in single", amps: 11 },
    { cfm: 1700, label: "14 in single", amps: 16 },
    { cfm: 2100, label: "16 in single", amps: 22 },
    { cfm: 3400, label: "Dual 14 in", amps: 32 },
    { cfm: 4200, label: "Dual 16 in", amps: 44 }
];
const CL_PUMPS = [20, 35, 55];
function clPumpClass(gpm) {
    for (let i = 0; i < CL_PUMPS.length; i++) {
        if (CL_PUMPS[i] >= gpm) return { gpm: CL_PUMPS[i], count: 1 };
    }
    if (gpm <= 110) return { gpm: 55, count: 2 };
    return { gpm: 55, count: 3 };
}
function calcCooling() {
    const fuel = CL_FUEL[document.getElementById("cl-fuel").value] || CL_FUEL.gasoline;
    const boost = document.getElementById("cl-ind").value === "boost";
    let hp = crankHorsepower(document.getElementById("cl-hp").value || 1000);
    if (!Number.isFinite(hp) || hp < 50) hp = 1000;
    const bsfc = boost ? fuel.boost : fuel.na;
    let seconds = parseFloat(document.getElementById("cl-pass").value);
    if (!Number.isFinite(seconds) || seconds < 4) seconds = 10;
    let minutes = parseFloat(document.getElementById("cl-wait").value);
    if (!Number.isFinite(minutes) || minutes < 1) minutes = 8;
    let gallons = parseFloat(document.getElementById("cl-gal").value);
    if (!Number.isFinite(gallons) || gallons < 1) gallons = 4;
    let share = parseFloat(document.getElementById("cl-share").value);
    if (!Number.isFinite(share)) share = 0.06;
    share = Math.min(0.25, Math.max(0.02, share));
    let idleShare = parseFloat(document.getElementById("cl-idle-share").value);
    if (!Number.isFinite(idleShare)) idleShare = 0.40;
    idleShare = Math.min(0.7, Math.max(0.1, idleShare));
    let rise = parseFloat(document.getElementById("cl-rise").value);
    if (!Number.isFinite(rise) || rise < 8) rise = 20;
    let air = parseFloat(document.getElementById("cl-air").value);
    if (!Number.isFinite(air) || air < 10) air = 25;
    const water = document.getElementById("cl-mix").value === "water";
    const lbGal = water ? 8.34 : 8.90;
    const cp = water ? 1.00 : 0.85;
    const metal = document.getElementById("cl-block").value === "aluminum" ? 33 : 30.4;
    const running = document.getElementById("cl-run").value === "yes";
    const electricOnly = document.getElementById("cl-mode").value === "electric";
    let idleGph = parseFloat(document.getElementById("cl-idle").value);
    if (!Number.isFinite(idleGph) || idleGph <= 0) idleGph = Math.max(1.2, hp / 800);
    const passBtu = (hp * bsfc * fuel.btu * share * seconds) / 3600;
    const idleLb = running ? idleGph * fuel.dens * (minutes / 60) : 0;
    const idleBtu = idleLb * fuel.btu * idleShare;
    const capacity = gallons * lbGal * cp + metal;
    const delta = passBtu / capacity;
    const btuHr = (passBtu + idleBtu) * (60 / minutes);
    const cfm = btuHr / (1.08 * air);
    let fan = CL_FANS[CL_FANS.length - 1];
    for (let i = 0; i < CL_FANS.length; i++) {
        if (CL_FANS[i].cfm >= cfm) { fan = CL_FANS[i]; break; }
    }
    const heatCap = rise * lbGal * cp;
    const passGpm = (passBtu / (seconds / 60)) / heatCap;
    const laneGpm = (running ? idleBtu / minutes : passBtu / minutes) / heatCap;
    const lanePump = clPumpClass(Math.max(laneGpm, 8));
    const passPump = clPumpClass(passGpm);
    const ordered = electricOnly ? passPump : lanePump;
    const pumpLabel = (ordered.count > 1 ? ordered.count + " x " : "") + ordered.gpm + " GPM electric";
    publishReadout([
        { label: "Coolant rise this pass", value: delta, unit: "deltaf", primary: true },
        { label: "Fan to order", value: fan.label, unit: "text" },
        { label: "Fan airflow", value: cfm, unit: "cfm" },
        { label: "Water pump", value: pumpLabel, unit: "text" },
        { label: "Flow the hit wants", value: passGpm, unit: "gpm" },
        { label: "Flow the lanes want", value: laneGpm, unit: "gpm" }
    ]);
    let heatLine = "The pass puts about " + Math.round(delta) + "\u00b0F into the coolant.";
    if (delta > 70) heatLine += " That is too much for this much water. Add capacity or the car will boil on a back-to-back.";
    else if (delta > 40) heatLine += " That is a hard climb. More water or a longer wait is the fix.";
    else heatLine += " The water and the metal can swallow that hit.";
    let fanLine = " Order a " + fan.label + " fan, about " + fan.amps + " A, to pull " + Math.round(cfm) + " CFM while it sits.";
    if (cfm > 4200) fanLine = " The wait is short for this much heat. Dual 16 in fans are the top of the usual list, and the car still wants more time or the engine shut off.";
    let pumpLine;
    if (electricOnly) {
        pumpLine = passPump.count === 1
            ? " An electric pump has to carry the hit, so order the " + passPump.gpm + " GPM class."
            : " One electric pump does not cover the hit. Order " + passPump.count + " pumps in the 55 GPM class.";
    } else if (passGpm > lanePump.gpm + 5) {
        pumpLine = " The mechanical pump carries the hit at about " + passGpm.toFixed(0) + " GPM. The electric pump is for the lanes: the " + lanePump.gpm + " GPM class.";
    } else {
        pumpLine = " The " + lanePump.gpm + " GPM electric pump also covers the hit, so it can be the only pump.";
    }
    const idleLine = running
        ? " Leaving it running adds the idle heat the fan has to pull."
        : " Shutting it off drops the fan back to the heat from the pass alone.";
    document.getElementById("cl-assess").textContent = heatLine + fanLine + pumpLine + idleLine;
}
bindCalc(calcCooling, ["cl-hp", "cl-fuel", "cl-ind", "cl-mix", "cl-gal", "cl-block", "cl-pass", "cl-wait", "cl-run", "cl-mode", "cl-share", "cl-idle-share", "cl-rise", "cl-air", "cl-idle", "dt-loss"]);
"""


def driveline_html(_row):
    tubes = """
                <option value="2.5|0.083|steel">2.50 x 0.083 steel</option>
                <option value="3|0.083|steel">3.00 x 0.083 steel</option>
                <option value="3|0.065|steel" >3.00 x 0.065 chromoly</option>
                <option value="3.5|0.125|aluminum" selected>3.50 x 0.125 aluminum</option>
                <option value="4|0.125|aluminum">4.00 x 0.125 aluminum</option>
                <option value="custom">Custom tube</option>"""
    primary = f"""
    {DRIVESHAFT_DIAGRAM}
    <div class="grid-2">
        <div class="field"><label for="ds-len">Center-to-center length (in)</label><input type="number" id="ds-len" value="48" min="20" step="0.5"></div>
        <div class="field"><label for="ds-tube">Tube</label><select id="ds-tube">{tubes}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ds-rpm">RPM at the stripe</label><input type="number" id="ds-rpm" value="7000" min="2000" step="100"></div>
        <div class="field"><label for="ds-gear">Top gear ratio</label><input type="number" id="ds-gear" value="1.00" min="0.4" max="2" step="0.01"></div>
    </div>
    <p class="field-hint">Shaft speed is engine RPM divided by the gear it is in at the stripe. A 0.70 overdrive spins the shaft faster than the engine. Rear gear does not change shaft speed.</p>
    <div class="grid-2">
        <div class="field"><label for="ds-trans">Transmission angle (deg)</label><input type="number" id="ds-trans" value="-2" step="0.1"></div>
        <div class="field"><label for="ds-shaft">Driveshaft angle (deg)</label><input type="number" id="ds-shaft" value="-1" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ds-pinion">Pinion angle (deg)</label><input type="number" id="ds-pinion" value="-2" step="0.1"></div>
        <div class="field"><label for="ds-sus">Rear suspension</label>
            <select id="ds-sus">
                <option value="fourlink" selected>4-link or ladder bar</option>
                <option value="leaf">Leaf spring</option>
            </select>
        </div>
    </div>
    <p class="field-hint">Use one angle finder, pointing the same way, on the tailhousing, the tube, and the pinion yoke. A slope down toward the rear of the car is a negative number.</p>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="ds-od">Custom outside diameter (in)</label><input type="number" id="ds-od" value="3.5" min="1.5" step="0.125"></div>
        <div class="field"><label for="ds-wall">Custom wall (in)</label><input type="number" id="ds-wall" value="0.083" min="0.035" step="0.005"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ds-mat">Custom material</label>
            <select id="ds-mat">
                <option value="steel" selected>Steel or chromoly</option>
                <option value="aluminum">Aluminum</option>
            </select>
        </div>
        <div class="field"><label for="ds-street">Also driven on the street</label>
            <select id="ds-street">
                <option value="no" selected>Drag only</option>
                <option value="yes">Street and strip</option>
            </select>
        </div>
    </div>
    """
    assess = '<p class="assess" id="ds-assess"></p>'
    return calculator_shell(primary, advanced, "Print driveshaft sheet", results_extra=assess)


DRIVELINE_SCRIPT = r"""
function dsTube() {
    const pick = document.getElementById("ds-tube").value;
    if (pick === "custom") {
        let od = parseFloat(document.getElementById("ds-od").value);
        let wall = parseFloat(document.getElementById("ds-wall").value);
        if (!Number.isFinite(od) || od < 1.5) od = 3.5;
        if (!Number.isFinite(wall) || wall < 0.035) wall = 0.083;
        wall = Math.min(wall, od / 2 - 0.2);
        return { od: od, wall: wall, mat: document.getElementById("ds-mat").value, label: od.toFixed(2) + " x " + wall.toFixed(3) };
    }
    const parts = pick.split("|");
    return { od: parseFloat(parts[0]), wall: parseFloat(parts[1]), mat: parts[2], label: "" };
}
function dsCritical(od, wall, mat, length) {
    const id = od - 2 * wall;
    const factor = mat === "aluminum" ? 0.981 : 1;
    const k = 4770000 * factor * Math.sqrt(od * od + id * id);
    return { critical: k / (length * length), k: k };
}
function calcDriveline() {
    let length = parseFloat(document.getElementById("ds-len").value);
    if (!Number.isFinite(length) || length < 20) length = 48;
    let rpm = parseFloat(document.getElementById("ds-rpm").value);
    if (!Number.isFinite(rpm) || rpm < 2000) rpm = 7000;
    let gear = parseFloat(document.getElementById("ds-gear").value);
    if (!Number.isFinite(gear) || gear < 0.4) gear = 1;
    const tube = dsTube();
    const speed = dsCritical(tube.od, tube.wall, tube.mat, length);
    const shaftRpm = rpm / gear;
    const safe = speed.critical * 0.75;
    const safeLen = Math.sqrt(speed.k * 0.75 / shaftRpm);
    let trans = parseFloat(document.getElementById("ds-trans").value);
    let shaft = parseFloat(document.getElementById("ds-shaft").value);
    let pinion = parseFloat(document.getElementById("ds-pinion").value);
    if (!Number.isFinite(trans)) trans = -2;
    if (!Number.isFinite(shaft)) shaft = -1;
    if (!Number.isFinite(pinion)) pinion = -2;
    const front = Math.abs(trans - shaft);
    const rear = Math.abs(pinion - shaft);
    const noseDown = pinion - shaft;
    const leaf = document.getElementById("ds-sus").value === "leaf";
    const street = document.getElementById("ds-street").value === "yes";
    let speedLabel = "Under the 75% line";
    if (shaftRpm > speed.critical) speedLabel = "Over critical speed";
    else if (shaftRpm > safe) speedLabel = "Over the 75% line";
    publishReadout([
        { label: "Shaft speed", value: Math.round(shaftRpm), unit: "rpm", primary: true },
        { label: "Critical speed", value: Math.round(speed.critical), unit: "rpm" },
        { label: "75% of critical", value: Math.round(safe), unit: "rpm" },
        { label: "Tube at this RPM", value: speedLabel, unit: "text" },
        { label: "Front working angle", value: front, unit: "deg" },
        { label: "Rear working angle", value: rear, unit: "deg" }
    ]);
    let speedLine;
    if (shaftRpm > speed.critical) {
        speedLine = "This tube is past the first bending speed at " + Math.round(shaftRpm) + " RPM. It is safe out to about " + safeLen.toFixed(1) + " in, or it needs a larger diameter.";
    } else if (shaftRpm > safe) {
        speedLine = "Critical speed is " + Math.round(speed.critical) + " RPM. The planning line is 75% of that, " + Math.round(safe) + " RPM. Shorten it to about " + safeLen.toFixed(1) + " in or go up a tube size.";
    } else {
        speedLine = "Critical speed is " + Math.round(speed.critical) + " RPM. At " + Math.round(shaftRpm) + " the shaft is under the 75% line, and this tube can run out to about " + safeLen.toFixed(1) + " in.";
    }
    let angleLine;
    if (leaf) {
        if (noseDown >= 1.5 && noseDown <= 3.5) {
            angleLine = " The pinion is " + noseDown.toFixed(1) + "\u00b0 nose down from the tube, which is the wrap a leaf spring wants at rest.";
        } else if (noseDown > 0) {
            angleLine = " The pinion is " + noseDown.toFixed(1) + "\u00b0 nose down. A leaf spring wants about 2\u00b0 so the joint straightens when the axle wraps.";
        } else {
            angleLine = " The pinion is nose up from the tube. A leaf spring wants it about 2\u00b0 nose down at rest.";
        }
    } else {
        const cancel = Math.abs(front - rear);
        if (front <= 1.5 && rear <= 1.5 && cancel <= 0.5) {
            angleLine = " The working angles are " + front.toFixed(1) + "\u00b0 and " + rear.toFixed(1) + "\u00b0. A 4-link wants them small and equal.";
        } else if (front > 3 || rear > 3) {
            angleLine = " A working angle over 3\u00b0 will vibrate. Point the pinion at the driveshaft and keep the tail and the pinion parallel.";
        } else {
            angleLine = " The working angles are " + front.toFixed(1) + "\u00b0 and " + rear.toFixed(1) + "\u00b0. A 4-link wants both under 1.5\u00b0 and within half a degree of each other.";
        }
    }
    if (street && Math.min(front, rear) < 0.5) {
        angleLine += " A shaft that also drives on the street wants at least half a degree so the U-joint needles roll.";
    }
    document.getElementById("ds-assess").textContent = speedLine + angleLine;
}
bindCalc(calcDriveline, ["ds-len", "ds-tube", "ds-rpm", "ds-gear", "ds-trans", "ds-shaft", "ds-pinion", "ds-sus", "ds-od", "ds-wall", "ds-mat", "ds-street"]);
"""


def power_html(_row):
    primary = f"""
    {POWER_DIAGRAM}
    <div class="grid-2">
        <div class="field"><label for="pw-pump">Fuel pump</label>
            <select id="pw-pump">
                <option value="0">None, mechanical</option>
                <option value="15">Single in-tank, about 15 A</option>
                <option value="28" selected>Dual in-tank, about 28 A</option>
                <option value="35">Large external, about 35 A</option>
                <option value="60">Dual external, about 60 A</option>
            </select>
        </div>
        <div class="field"><label for="pw-fan">Electric fan</label>
            <select id="pw-fan">
                <option value="0">None</option>
                <option value="11">12 in, about 11 A</option>
                <option value="16">14 in, about 16 A</option>
                <option value="22" selected>16 in, about 22 A</option>
                <option value="32">Dual 14 in, about 32 A</option>
                <option value="44">Dual 16 in, about 44 A</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="pw-wp">Electric water pump</label>
            <select id="pw-wp">
                <option value="0">Mechanical only</option>
                <option value="8">20 GPM class, about 8 A</option>
                <option value="12">35 GPM class, about 12 A</option>
                <option value="16" selected>55 GPM class, about 16 A</option>
            </select>
        </div>
        <div class="field"><label for="pw-ign">Ignition (A)</label><input type="number" id="pw-ign" value="8" min="0" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="pw-ecu">ECU and sensors (A)</label><input type="number" id="pw-ecu" value="5" min="0" step="1"></div>
        <div class="field"><label for="pw-brake">Trans brake solenoid (A)</label><input type="number" id="pw-brake" value="18" min="0" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="pw-charge-len">Alternator wire, one way (ft)</label><input type="number" id="pw-charge-len" value="15" min="1" step="1"></div>
        <div class="field"><label for="pw-panel-len">Battery to fuse panel (ft)</label><input type="number" id="pw-panel-len" value="6" min="1" step="1"></div>
    </div>
    <p class="field-hint">Pump, fan, water pump, and ignition are on the whole time the engine is running. The trans brake, the nitrous, and the line lock are a few seconds on the battery. The alternator has to cover the running loads at idle.</p>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="pw-nitrous">Nitrous solenoids (A)</label><input type="number" id="pw-nitrous" value="0" min="0" step="1"></div>
        <div class="field"><label for="pw-lock">Line lock (A)</label><input type="number" id="pw-lock" value="0" min="0" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="pw-acc">Gauges, delay box, controller (A)</label><input type="number" id="pw-acc" value="3" min="0" step="1"></div>
        <div class="field"><label for="pw-volts">Running voltage</label>
            <select id="pw-volts">
                <option value="13.8" selected>13.8V</option>
                <option value="16">16V</option>
            </select>
        </div>
    </div>
    """
    table = """
    <table>
        <thead><tr><th>Load</th><th>Amps</th><th>When</th></tr></thead>
        <tbody id="pw-body"></tbody>
    </table>
    <p class="assess" id="pw-assess"></p>
    """
    return calculator_shell(primary, advanced, "Print wiring sheet", table)


POWER_SCRIPT = r"""
const PW_ALTS = [60, 90, 120, 150, 200, 250];
const PW_FUSES = [40, 60, 80, 100, 125, 150, 175, 200, 225, 250, 300];
const PW_CABLE = [[2583, "16"], [4107, "14"], [6530, "12"], [10380, "10"], [16510, "8"], [26250, "6"], [41740, "4"], [66360, "2"], [83690, "1"], [105600, "1/0"], [133100, "2/0"], [167800, "3/0"], [211600, "4/0"]];
function pwAmps(id) {
    const n = parseFloat(document.getElementById(id).value);
    return Number.isFinite(n) && n > 0 ? n : 0;
}
function pwCable(amps, length, volts) {
    const drop = Math.max(volts, 12) * 0.03;
    const cm = (10.75 * amps * length * 2) / drop;
    let gauge = "4/0";
    for (let i = 0; i < PW_CABLE.length; i++) {
        if (PW_CABLE[i][0] >= cm) { gauge = PW_CABLE[i][1]; break; }
    }
    return gauge;
}
function pwStep(list, amps) {
    for (let i = 0; i < list.length; i++) {
        if (list[i] >= amps) return list[i];
    }
    return list[list.length - 1];
}
function calcPower() {
    const pump = pwAmps("pw-pump");
    const fan = pwAmps("pw-fan");
    const wp = pwAmps("pw-wp");
    const ign = pwAmps("pw-ign");
    const ecu = pwAmps("pw-ecu");
    const acc = pwAmps("pw-acc");
    const brake = pwAmps("pw-brake");
    const nitrous = pwAmps("pw-nitrous");
    const lock = pwAmps("pw-lock");
    const volts = parseFloat(document.getElementById("pw-volts").value) || 13.8;
    let chargeLen = parseFloat(document.getElementById("pw-charge-len").value);
    let panelLen = parseFloat(document.getElementById("pw-panel-len").value);
    if (!Number.isFinite(chargeLen) || chargeLen < 1) chargeLen = 15;
    if (!Number.isFinite(panelLen) || panelLen < 1) panelLen = 6;
    const continuous = pump + fan + wp + ign + ecu + acc;
    const hit = brake + nitrous + lock;
    const altNeed = continuous * 1.2;
    const alt = pwStep(PW_ALTS, altNeed);
    const fuse = pwStep(PW_FUSES, continuous);
    const panelGauge = pwCable(Math.max(continuous, 1), panelLen, volts);
    const chargeGauge = pwCable(Math.max(alt, 1), chargeLen, volts);
    const altLabel = altNeed > 250 ? "Over 250 A" : alt + " A";
    publishReadout([
        { label: "Running load", value: continuous, unit: "amp", primary: true },
        { label: "Hit load on the battery", value: hit, unit: "amp" },
        { label: "Alternator to order", value: altLabel, unit: "text" },
        { label: "Main fuse at the battery", value: fuse + " A", unit: "text" },
        { label: "Panel feed", value: panelGauge + " AWG", unit: "text" },
        { label: "Alternator charge wire", value: chargeGauge + " AWG", unit: "text" }
    ]);
    const rows = [
        ["Fuel pump", pump, "Running"],
        ["Fan", fan, "Running"],
        ["Water pump", wp, "Running"],
        ["Ignition", ign, "Running"],
        ["ECU", ecu, "Running"],
        ["Gauges and controller", acc, "Running"],
        ["Trans brake", brake, "Hit"],
        ["Nitrous", nitrous, "Hit"],
        ["Line lock", lock, "Hit"]
    ];
    let body = "";
    rows.forEach(function (row) {
        if (row[1] <= 0) return;
        body += "<tr><td>" + row[0] + "</td><td>" + row[1].toFixed(0) + "</td><td>" + row[2] + "</td></tr>";
    });
    document.getElementById("pw-body").innerHTML = body;
    const fuseEl = document.getElementById("pw-fig-fuse");
    if (fuseEl) fuseEl.textContent = fuse + " A";
    const panelEl = document.getElementById("pw-fig-panel");
    if (panelEl) panelEl.textContent = panelGauge + " AWG";
    const chargeEl = document.getElementById("pw-fig-charge");
    if (chargeEl) chargeEl.textContent = chargeGauge + " charge";
    let altLine = altNeed > 250
        ? "The running load wants more than a 250 A alternator. That is two units, or a larger case, and the idle output is the number that matters."
        : "Order an alternator that still makes " + alt + " A at idle. A cruise rating does not keep the fans and the pump alive in the lanes.";
    const wireLine = " The panel feed is " + panelGauge + " AWG for " + panelLen.toFixed(0) + " ft. The charge wire is " + chargeGauge + " AWG for " + chargeLen.toFixed(0) + " ft. Both are high-strand battery cable, sized for a 3% drop. The starter cable stays a 1/0 or 2/0.";
    document.getElementById("pw-assess").textContent = altLine + wireLine;
}
bindCalc(calcPower, ["pw-pump", "pw-fan", "pw-wp", "pw-ign", "pw-ecu", "pw-brake", "pw-charge-len", "pw-panel-len", "pw-nitrous", "pw-lock", "pw-acc", "pw-volts"]);
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

LS_CATALOG = {
    "blocks": {
        "lm7": {"label": "LM7 5.3 iron", "bore": 3.780, "safeBore": 3.810, "maxBore": 4.000, "stockStroke": 3.622, "hp": 850, "boost": 18, "sleeved": False, "note": "Gen III iron 5.3. The small bore leaves more cylinder wall than an aluminum block, and it is the usual budget turbo foundation."},
        "lq4": {"label": "LQ4 6.0 iron", "bore": 4.000, "safeBore": 4.030, "maxBore": 4.070, "stockStroke": 3.622, "hp": 1100, "boost": 24, "sleeved": False, "note": "Gen III iron 6.0. One of the strongest factory LS castings."},
        "lq9": {"label": "LQ9 6.0 iron", "bore": 4.000, "safeBore": 4.030, "maxBore": 4.070, "stockStroke": 3.622, "hp": 1100, "boost": 24, "sleeved": False, "note": "Iron 6.0 HO. Same casting family as the LQ4, with flat-top pistons from the factory."},
        "ls1": {"label": "LS1 aluminum", "bore": 3.898, "safeBore": 3.905, "maxBore": 3.940, "stockStroke": 3.622, "hp": 550, "boost": 8, "sleeved": False, "note": "Aluminum 5.7. Thin cylinder walls and a modest boost ceiling."},
        "ls2": {"label": "LS2 aluminum", "bore": 4.000, "safeBore": 4.010, "maxBore": 4.030, "stockStroke": 3.622, "hp": 650, "boost": 10, "sleeved": False, "note": "Aluminum 6.0. A little stronger than an LS1, and still not an iron 6.0."},
        "ls3": {"label": "LS3 aluminum", "bore": 4.065, "safeBore": 4.070, "maxBore": 4.100, "stockStroke": 3.622, "hp": 700, "boost": 12, "sleeved": False, "note": "Aluminum 6.2. Rectangle-port heads from the factory and a short overbore window."},
        "ls7": {"label": "LS7 aluminum", "bore": 4.125, "safeBore": 4.130, "maxBore": 4.155, "stockStroke": 4.000, "hp": 700, "boost": 8, "sleeved": False, "note": "Aluminum 7.0. The windows in the barrels are the boost limit."},
        "sleeve53": {"label": "5.3 iron, resleeved", "bore": 3.905, "safeBore": 4.000, "maxBore": 4.000, "stockStroke": 3.622, "hp": 1200, "boost": 26, "sleeved": True, "note": "Iron 5.3 with aftermarket sleeves. The bore and the power rating both move up."},
        "sleeve60": {"label": "6.0 iron, resleeved", "bore": 4.030, "safeBore": 4.070, "maxBore": 4.070, "stockStroke": 3.622, "hp": 1500, "boost": 30, "sleeved": True, "note": "Iron 6.0 with aftermarket sleeves for a bigger bore and more boost."},
        "lsx": {"label": "Aftermarket iron (LSX class)", "bore": 4.125, "safeBore": 4.165, "maxBore": 4.185, "stockStroke": 3.622, "hp": 1800, "boost": 35, "sleeved": False, "note": "Aftermarket iron in the LSX class. Priority mains and room for a large bore."},
    },
    "cranks": {
        "s3268": {"label": "4.8 factory 3.268 in", "stroke": 3.268, "hp": 600, "note": "Factory 4.8 cast crank. This is the destroker when it goes into a 6.0."},
        "s3622": {"label": "5.3 / 6.0 / 6.2 factory 3.622 in", "stroke": 3.622, "hp": 750, "note": "Factory cast crank shared by the 5.3, 6.0, and 6.2."},
        "f4000": {"label": "LS7 factory 4.000 in", "stroke": 4.000, "hp": 900, "note": "LS7 forged 4.000 in crank. The mains fit a standard LS block, and the piston has to get shorter."},
        "a4000": {"label": "Aftermarket 4.000 in", "stroke": 4.000, "hp": 1500, "note": "Forged 4.000 in stroker crank."},
        "a4100": {"label": "Aftermarket 4.100 in", "stroke": 4.100, "hp": 1500, "note": "Forged 4.100 in stroker crank."},
        "a4125": {"label": "Aftermarket 4.125 in", "stroke": 4.125, "hp": 1600, "note": "Forged 4.125 in stroker crank."},
        "a4250": {"label": "Aftermarket 4.250 in", "stroke": 4.250, "hp": 1600, "note": "Forged 4.250 in stroker crank. Check the compression height before ordering pistons."},
    },
    "rods": {
        "pm": {"label": "Factory powdered metal", "hp": 550, "rpm": 6800, "pin": "pressed", "note": "Factory powdered-metal rod with a pressed pin."},
        "hbeam": {"label": "Forged H-beam", "hp": 1000, "rpm": 7500, "pin": "floating", "note": "Forged H-beam with a floating pin."},
        "ibeam": {"label": "Forged I-beam", "hp": 1500, "rpm": 8000, "pin": "floating", "note": "Forged I-beam with a floating pin. The usual choice once the power goal passes four figures."},
        "ti": {"label": "LS7 titanium", "hp": 700, "rpm": 7100, "pin": "floating", "note": "LS7 titanium rod. Light, and hard on the big end if RPM or oil is wrong."},
    },
    "heads": {
        "h241": {"label": "241 cathedral (LS6 / LS2)", "cc": 64.5, "cfm": 240, "minBore": 3.70, "direct": True, "note": "Cathedral 241 from the LS6 and LS2. About 64 cc and a direct swap onto a cathedral intake."},
        "h243": {"label": "243 / 799 cathedral", "cc": 64, "cfm": 250, "minBore": 3.70, "direct": True, "note": "Cathedral 243 and 799. The standard performance swap onto a 5.3 or 6.0."},
        "h317": {"label": "317 cathedral (5.3 truck)", "cc": 71, "cfm": 215, "minBore": 3.70, "direct": True, "note": "Cathedral 317 truck head. Larger chamber and less flow."},
        "tfx": {"label": "Trick Flow GenX cathedral", "cc": 62, "cfm": 310, "minBore": 3.78, "direct": True, "note": "Trick Flow GenX cathedral. More port than a factory 243, and it still uses a cathedral intake."},
        "ls3": {"label": "LS3 / L92 rectangular", "cc": 68, "cfm": 320, "minBore": 3.90, "direct": True, "note": "LS3 and L92 rectangle port. Needs a rectangle-port intake, and the chamber wants a 3.900 in bore or larger."},
        "ls7": {"label": "LS7 rectangular", "cc": 70, "cfm": 370, "minBore": 4.10, "direct": False, "note": "LS7 rectangle port. Different valve angle, rockers, and intake."},
        "afr": {"label": "Aftermarket rectangular", "cc": 65, "cfm": 360, "minBore": 3.90, "direct": True, "note": "Aftermarket rectangle port in the AFR or Mast class, matched to a rectangle-port intake."},
    },
    "pistons": {
        "hyper": {"label": "Factory hypereutectic", "dish": 8, "hp": 500, "note": "Hypereutectic piston. Fine for a mild naturally aspirated build, and the first part to give up under boost."},
        "flat": {"label": "Forged flat top", "dish": 4, "hp": 1500, "note": "Forged flat top with valve reliefs."},
        "dish": {"label": "Forged dished", "dish": 16, "hp": 1500, "note": "Forged dished piston for boost. The dish is what keeps the compression in range."},
        "dome": {"label": "Forged dome", "dish": -4, "hp": 1200, "note": "Forged dome for fuel that can support the compression, such as E85 or race gas."},
    },
}
LS_GROUPS = {
    "blocks": (
        ("Factory iron", ("lm7", "lq4", "lq9")),
        ("Factory aluminum", ("ls1", "ls2", "ls3", "ls7")),
        ("Aftermarket / resleeved", ("sleeve53", "sleeve60", "lsx")),
    ),
    "cranks": (
        ("Factory", ("s3268", "s3622", "f4000")),
        ("Aftermarket stroker", ("a4000", "a4100", "a4125", "a4250")),
    ),
    "heads": (
        ("Cathedral port", ("h241", "h243", "h317", "tfx")),
        ("Rectangular port", ("ls3", "ls7", "afr")),
    ),
}
LS_ROD_LENGTHS = (
    ("6.067", "6.067 in (LS7)"),
    ("6.098", "6.098 in (factory)"),
    ("6.125", "6.125 in (stroker)"),
    ("6.200", "6.200 in (long)"),
)
LS_PINS = (("pressed", "Pressed pin"), ("floating", "Floating pin"))
LS_INTENTS = (("na", "Naturally aspirated"), ("turbo", "Turbocharged"), ("super", "Supercharged"), ("nitrous", "Nitrous"))
LS_BUILD_FUELS = (("gasoline", "Gasoline (91/93)"), ("e85", "E85"), ("methanol", "Methanol"), ("race", "Race gas"))
LS_PRESETS = {
    "ls-engine-builder": {"block": "lq4", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "hyper", "head": "h317", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6000", "gasket": "0.051", "deck": "0.005", "spec": "LQ4 iron 6.0, 317 heads, naturally aspirated"},
    "lm7-5-3-iron-engine-build": {"block": "lm7", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "hyper", "head": "h317", "intent": "na", "fuel": "gasoline", "bore": "3.780", "boost": "0", "rpm": "5800", "gasket": "0.051", "deck": "0.005", "spec": "LM7 iron 5.3, 317 heads, naturally aspirated"},
    "lq4-6-0-iron-engine-build": {"block": "lq4", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "hyper", "head": "h317", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6000", "gasket": "0.051", "deck": "0.005", "spec": "LQ4 iron 6.0, 317 heads, naturally aspirated"},
    "lq9-6-0-iron-engine-build": {"block": "lq9", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "flat", "head": "h317", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6200", "gasket": "0.051", "deck": "0.005", "spec": "LQ9 iron 6.0, flat-top pistons, 317 heads"},
    "ls1-aluminum-engine-build": {"block": "ls1", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "flat", "head": "h241", "intent": "na", "fuel": "gasoline", "bore": "3.898", "boost": "0", "rpm": "6200", "gasket": "0.051", "deck": "0.005", "spec": "LS1 aluminum, 241 cathedral heads"},
    "ls2-aluminum-engine-build": {"block": "ls2", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "flat", "head": "h243", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6400", "gasket": "0.051", "deck": "0.005", "spec": "LS2 aluminum, 243 cathedral heads"},
    "ls3-376-engine-build": {"block": "ls3", "crank": "s3622", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "flat", "head": "ls3", "intent": "na", "fuel": "gasoline", "bore": "4.065", "boost": "0", "rpm": "6600", "gasket": "0.051", "deck": "0.005", "spec": "LS3 aluminum, rectangular heads"},
    "ls7-427-engine-build": {"block": "ls7", "crank": "f4000", "rod": "ti", "rodlen": "6.067", "pin": "floating", "piston": "flat", "head": "ls7", "intent": "na", "fuel": "gasoline", "bore": "4.125", "boost": "0", "rpm": "7000", "gasket": "0.051", "deck": "0.005", "spec": "LS7, 4.000 in stroke, titanium rods, LS7 heads"},
    "iron-5-3-4-inch-stroker": {"block": "lm7", "crank": "f4000", "rod": "hbeam", "rodlen": "6.125", "pin": "floating", "piston": "flat", "head": "h243", "intent": "na", "fuel": "gasoline", "bore": "3.780", "boost": "0", "rpm": "6500", "gasket": "0.051", "deck": "0.005", "spec": "iron 5.3, 4.000 in crank, 6.125 in rods, 243 heads"},
    "iron-6-0-402-stroker": {"block": "lq4", "crank": "a4000", "rod": "hbeam", "rodlen": "6.125", "pin": "floating", "piston": "flat", "head": "ls3", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6500", "gasket": "0.051", "deck": "0.005", "spec": "iron 6.0, 4.000 in crank, LS3 heads"},
    "iron-6-0-4-125-stroker": {"block": "lq4", "crank": "a4125", "rod": "ibeam", "rodlen": "6.125", "pin": "floating", "piston": "flat", "head": "ls3", "intent": "na", "fuel": "e85", "bore": "4.000", "boost": "0", "rpm": "6800", "gasket": "0.051", "deck": "0.005", "spec": "iron 6.0, 4.125 in crank, E85"},
    "iron-6-0-4-8-destroker": {"block": "lq4", "crank": "s3268", "rod": "pm", "rodlen": "6.098", "pin": "pressed", "piston": "hyper", "head": "h317", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "7000", "gasket": "0.051", "deck": "0.005", "spec": "iron 6.0 with a 4.8 crank"},
    "turbo-5-3-iron-build": {"block": "lm7", "crank": "s3622", "rod": "hbeam", "rodlen": "6.098", "pin": "floating", "piston": "dome", "head": "h243", "intent": "turbo", "fuel": "e85", "bore": "3.780", "boost": "12", "rpm": "6400", "gasket": "0.051", "deck": "0.005", "spec": "iron 5.3, 243 heads, E85, 12 PSI turbo"},
    "supercharged-ls3-build": {"block": "ls3", "crank": "s3622", "rod": "hbeam", "rodlen": "6.098", "pin": "floating", "piston": "dish", "head": "ls3", "intent": "super", "fuel": "gasoline", "bore": "4.065", "boost": "8", "rpm": "6400", "gasket": "0.051", "deck": "0.005", "spec": "LS3, forged dished pistons, 8 PSI supercharged"},
    "lq4-ls3-head-swap": {"block": "lq4", "crank": "s3622", "rod": "hbeam", "rodlen": "6.098", "pin": "floating", "piston": "flat", "head": "ls3", "intent": "na", "fuel": "gasoline", "bore": "4.000", "boost": "0", "rpm": "6500", "gasket": "0.051", "deck": "0.005", "spec": "iron 6.0 with LS3 rectangular heads"},
    "aftermarket-lsx-engine-build": {"block": "lsx", "crank": "a4125", "rod": "ibeam", "rodlen": "6.125", "pin": "floating", "piston": "dish", "head": "afr", "intent": "turbo", "fuel": "e85", "bore": "4.125", "boost": "18", "rpm": "7000", "gasket": "0.051", "deck": "0.005", "spec": "aftermarket iron, 4.125 in crank, E85, 18 PSI"},
}


def ls_preset(slug):
    return LS_PRESETS.get(slug, LS_PRESETS["ls-engine-builder"])


def ls_group_options(kind, current):
    parts = []
    for label, keys in LS_GROUPS[kind]:
        opts = options([(key, LS_CATALOG[kind][key]["label"]) for key in keys], current)
        parts.append(f'<optgroup label="{esc(label)}">\n{opts}\n</optgroup>')
    return "".join(parts)


def ls_html(row):
    preset = ls_preset(row["slug"])
    dish = LS_CATALOG["pistons"][preset["piston"]]["dish"]
    boost_disabled = " disabled" if preset["intent"] == "na" else ""
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="ls-block">Block</label><select id="ls-block">{ls_group_options("blocks", preset["block"])}</select></div>
        <div class="field"><label for="ls-bore">Bore (in)</label><input type="number" id="ls-bore" value="{esc(f'{float(preset["bore"]):.3f}')}" min="3.4" max="4.3" step="0.001"></div>
    </div>
    <p class="field-hint" id="ls-block-note"></p>
    <div class="grid-2">
        <div class="field"><label for="ls-crank">Crankshaft</label><select id="ls-crank">{ls_group_options("cranks", preset["crank"])}</select></div>
        <div class="field"><label for="ls-rod">Rods</label><select id="ls-rod">{options([(key, item["label"]) for key, item in LS_CATALOG["rods"].items()], preset["rod"])}</select></div>
    </div>
    <p class="field-hint" id="ls-crank-note"></p>
    <div class="grid-2">
        <div class="field"><label for="ls-rodlen">Rod length</label><select id="ls-rodlen">{options(LS_ROD_LENGTHS, preset["rodlen"])}</select></div>
        <div class="field"><label for="ls-pin">Wrist pin</label><select id="ls-pin">{options(LS_PINS, preset["pin"])}</select></div>
    </div>
    <p class="field-hint" id="ls-rod-note"></p>
    <div class="grid-2">
        <div class="field"><label for="ls-head">Cylinder heads</label><select id="ls-head">{ls_group_options("heads", preset["head"])}</select></div>
        <div class="field"><label for="ls-piston">Pistons</label><select id="ls-piston">{options([(key, item["label"]) for key, item in LS_CATALOG["pistons"].items()], preset["piston"])}</select></div>
    </div>
    <p class="field-hint" id="ls-head-note"></p>
    <p class="field-hint" id="ls-piston-note"></p>
    <div class="grid-2">
        <div class="field"><label for="ls-intent">Power adder</label><select id="ls-intent">{options(LS_INTENTS, preset["intent"])}</select></div>
        <div class="field"><label for="ls-fuel">Fuel</label><select id="ls-fuel">{options(LS_BUILD_FUELS, preset["fuel"])}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ls-boost" id="ls-boost-label">Target boost (PSI)</label><input type="number" id="ls-boost" value="{esc(preset["boost"])}" min="0" max="600" step="0.5"{boost_disabled}></div>
        <div class="field"><label for="ls-rpm">Peak RPM</label><input type="number" id="ls-rpm" value="{esc(preset["rpm"])}" min="4000" max="8500" step="100"></div>
    </div>
    <p class="field-hint">A 4.000 in crank in an iron 5.3 or 6.0 is the budget stroker. A 3.268 in crank in a 6.0 is the destroker. Power figures are planning limits for a tuned engine, not a guarantee.</p>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="ls-gasket">Head gasket (in)</label><input type="number" id="ls-gasket" value="{esc(preset["gasket"])}" min="0.020" max="0.120" step="0.001"></div>
        <div class="field"><label for="ls-deck">Deck clearance (in)</label><input type="number" id="ls-deck" value="{esc(preset["deck"])}" min="-0.020" max="0.040" step="0.001"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ls-deck-height">Deck height (in)</label><input type="number" id="ls-deck-height" value="9.240" min="9.000" max="10.000" step="0.001"></div>
        <div class="field"><label for="ls-dish">Piston dish (cc)</label><input type="number" id="ls-dish" value="{dish:g}" min="-20" max="40" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="ls-chamber">Chamber volume (cc)</label><input type="number" id="ls-chamber" placeholder="Auto" min="40" max="120" step="0.5"></div>
        <div class="field"><label for="ls-ivc">Intake close (deg ABDC)</label><input type="number" id="ls-ivc" placeholder="Auto" min="20" max="70" step="1"></div>
    </div>
    <p class="field-hint">Positive dish adds volume and lowers compression. A dome is a negative number. Leave chamber and intake closing blank to use the selected head and the cam profile.</p>
    {LOSS_FIELDS}
    """
    results = """
    <p class="assess" id="ls-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Check</th><th>Detail</th><th>Result</th><th>Status</th></tr></thead>
            <tbody id="ls-matrix"></tbody>
        </table>
        <p class="field-hint">Horsepower is the airflow estimate, plus the nitrous shot when that adder is selected. The power row flags a part rated below that number. The cam row is a starting profile.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print build sheet", power_toggle=True, results_extra=results)


LS_SCRIPT = r"""
const LS = %%LS%%;
const CC_PER_CI = 16.387064;

function lsNum(id, fallback) {
    const el = document.getElementById(id);
    const value = el ? parseFloat(el.value) : NaN;
    return Number.isFinite(value) ? value : fallback;
}

function lsText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function cidOf(bore, stroke) {
    return bore * bore * stroke * Math.PI / 4 * 8;
}

function volCc(bore, inches) {
    return bore * bore * Math.PI / 4 * inches * CC_PER_CI;
}

function clamp(value, lo, hi) {
    return Math.min(hi, Math.max(lo, value));
}

function pistonFromTdc(stroke, rod, theta) {
    const half = stroke / 2;
    const s = Math.sin(theta);
    const inside = 1 - Math.pow((half / rod) * s, 2);
    if (inside <= 0 || rod <= 0) return stroke;
    return half * (1 - Math.cos(theta)) + rod * (1 - Math.sqrt(inside));
}

function camPlan(intent, cid) {
    if (intent === "turbo") {
        return { duration: clamp(Math.round(214 + (cid - 346) * 0.04), 212, 228), lsa: 115, lift: 0.595, ivc: 34 };
    }
    if (intent === "super") {
        return { duration: clamp(Math.round(216 + (cid - 346) * 0.04), 214, 230), lsa: 114, lift: 0.585, ivc: 36 };
    }
    if (intent === "nitrous") {
        return { duration: clamp(Math.round(212 + (cid - 346) * 0.035), 210, 226), lsa: 113, lift: 0.570, ivc: 40 };
    }
    const duration = clamp(Math.round(208 + (cid - 330) * 0.07), 206, 238);
    const lift = Math.min(0.65, 0.54 + Math.max(0, cid - 330) * 0.00045);
    return {
        duration: duration,
        lsa: cid >= 400 ? 112 : 113,
        lift: Math.round(lift * 1000) / 1000,
        ivc: clamp(Math.round(36 + (duration - 214) * 0.45), 34, 52)
    };
}

function compressionBand(intent, fuel) {
    const boosted = intent !== "na";
    if (fuel === "methanol") return boosted ? { scrLo: 11, scrHi: 14, dcrLo: 8.5, dcrHi: 10 } : { scrLo: 12, scrHi: 15, dcrLo: 9, dcrHi: 11 };
    if (fuel === "e85") return boosted ? { scrLo: 10, scrHi: 12, dcrLo: 8, dcrHi: 9.2 } : { scrLo: 11, scrHi: 13.2, dcrLo: 8.4, dcrHi: 9.6 };
    if (fuel === "race") return boosted ? { scrLo: 10, scrHi: 11.5, dcrLo: 8, dcrHi: 9 } : { scrLo: 11, scrHi: 13, dcrLo: 8.5, dcrHi: 9.4 };
    return boosted ? { scrLo: 8.8, scrHi: 10.3, dcrLo: 7.5, dcrHi: 8.4 } : { scrLo: 10, scrHi: 11.5, dcrLo: 8, dcrHi: 8.7 };
}

function compressionStatus(value, lo, hi) {
    if (value >= lo && value <= hi) return "Good";
    if (value > hi && value <= hi + 0.4) return "Watch";
    if (value > hi) return "No";
    if (value >= lo - 0.8) return "Watch";
    return "No";
}

function wheelScale() {
    if (unitState.power !== "whp") return 1;
    const loss = Math.min(0.4, Math.max(0, lsNum("dt-loss", 15) / 100));
    return 1 - loss;
}

function matrixRow(name, detail, result, status) {
    const tr = document.createElement("tr");
    if (status === "No") tr.className = "is-small";
    const badge = status === "Good" ? "badge-ok" : (status === "Watch" ? "badge-tight" : "badge-no");
    [name, detail, result].forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
    });
    const statusCell = document.createElement("td");
    const pill = document.createElement("span");
    pill.className = "badge " + badge;
    pill.textContent = status;
    statusCell.appendChild(pill);
    tr.appendChild(statusCell);
    return tr;
}

function calcLs() {
    const block = LS.blocks[document.getElementById("ls-block").value] || LS.blocks.lq4;
    const crank = LS.cranks[document.getElementById("ls-crank").value] || LS.cranks.s3622;
    const rod = LS.rods[document.getElementById("ls-rod").value] || LS.rods.pm;
    const head = LS.heads[document.getElementById("ls-head").value] || LS.heads.h317;
    const piston = LS.pistons[document.getElementById("ls-piston").value] || LS.pistons.hyper;
    const rodLen = Math.max(5.5, lsNum("ls-rodlen", 6.098));
    const pin = document.getElementById("ls-pin").value || "pressed";
    const intent = document.getElementById("ls-intent").value || "na";
    const fuel = document.getElementById("ls-fuel").value || "gasoline";
    const bore = clamp(lsNum("ls-bore", block.bore), 3.4, 4.3);
    const stroke = crank.stroke;
    const deckHeight = lsNum("ls-deck-height", 9.24);
    const gasket = Math.max(0.02, lsNum("ls-gasket", 0.051));
    const deckClear = lsNum("ls-deck", 0.005);
    const dish = lsNum("ls-dish", piston.dish);
    const chamberEl = document.getElementById("ls-chamber");
    const chamberRaw = chamberEl && chamberEl.value.trim();
    const chamber = chamberRaw ? Math.max(20, parseFloat(chamberRaw) || head.cc) : head.cc;
    const rpm = clamp(lsNum("ls-rpm", 6400), 4000, 8500);
    const boostEl = document.getElementById("ls-boost");
    const boostLabel = document.getElementById("ls-boost-label");
    const nitrous = intent === "nitrous";
    const boosted = intent === "turbo" || intent === "super";
    if (boostEl) boostEl.disabled = intent === "na";
    if (boostLabel) boostLabel.textContent = nitrous ? "Nitrous shot (HP)" : "Target boost (PSI)";
    const adderValue = Math.max(0, lsNum("ls-boost", 0));
    const shot = nitrous ? Math.min(600, adderValue) : 0;
    const boost = boosted ? Math.min(40, adderValue) : 0;
    const cid = cidOf(bore, stroke);
    const delta = cid - cidOf(bore, block.stockStroke);
    const swept = volCc(bore, stroke);
    const clearance = chamber + volCc(bore, gasket) + volCc(bore, deckClear) + dish;
    const realClearance = clearance > 1;
    const scr = realClearance ? (swept + clearance) / clearance : 0;
    const ch = deckHeight - stroke / 2 - rodLen - deckClear;
    const rodRatio = rodLen / stroke;
    const cam = camPlan(intent, cid);
    const ivcEl = document.getElementById("ls-ivc");
    const ivcRaw = ivcEl && ivcEl.value.trim();
    const ivc = ivcRaw ? clamp(parseFloat(ivcRaw) || cam.ivc, 20, 70) : cam.ivc;
    const effective = pistonFromTdc(stroke, rodLen, (180 + ivc) * Math.PI / 180);
    const dcr = realClearance ? (volCc(bore, effective) + clearance) / clearance : 0;
    const ve = head.cfm >= 300 ? 0.93 : (head.cfm >= 240 ? 0.88 : 0.84);
    const naHp = Math.max(1, Math.min(cid * rpm * ve / 3456 * 0.85, head.cfm * 2.05));
    const adder = intent === "super" ? 0.88 : 0.9;
    let airHp = naHp;
    if (boosted) airHp = naHp * ((14.7 + boost) / 14.7) * adder;
    if (nitrous) airHp = naHp + shot;
    let hardware = { phrase: "The block is", hp: block.hp };
    [
        { phrase: "The crank is", hp: crank.hp },
        { phrase: "The rods are", hp: rod.hp },
        { phrase: "The pistons are", hp: piston.hp }
    ].forEach(item => { if (item.hp < hardware.hp) hardware = item; });
    const shown = airHp * wheelScale();
    let strokeLabel = "Stock stroke";
    if (delta >= 1.5) strokeLabel = "Stroker, +" + delta.toFixed(0) + " ci";
    else if (delta <= -1.5) strokeLabel = "Destroker, " + Math.abs(delta).toFixed(0) + " ci down";
    const band = compressionBand(intent, fuel);
    const scrStatus = realClearance ? compressionStatus(scr, band.scrLo, band.scrHi) : "No";
    const dcrStatus = realClearance ? compressionStatus(dcr, band.dcrLo, band.dcrHi) : "No";
    let boreStatus = "Good";
    let boreResult = Math.abs(bore - block.bore) > 0.002 ? "Overbore is inside the safe wall." : "Stock bore.";
    if (bore > block.maxBore + 0.001) {
        boreStatus = "No";
        boreResult = "Past " + block.maxBore.toFixed(3) + " in, the sleeve limit for this casting.";
    } else if (bore > block.safeBore + 0.001) {
        boreStatus = "Watch";
        boreResult = block.sleeved
            ? "On the large side of what this sleeve likes."
            : "Past the bare-casting overbore of " + block.safeBore.toFixed(3) + " in. This bore wants a sleeve.";
    }
    let chStatus = "Good";
    let chResult = ch.toFixed(3) + " in is a normal compression height.";
    if (ch < 0.98) {
        chStatus = "No";
        chResult = ch.toFixed(3) + " in puts the pin through the ring pack. Use less stroke or a shorter rod.";
    } else if (ch < 1.12) {
        chStatus = "Watch";
        chResult = ch.toFixed(3) + " in needs a custom piston, and the ring pack is close to the pin.";
    } else if (ch > 1.65) {
        chStatus = "Watch";
        chResult = ch.toFixed(3) + " in is a tall, heavy piston, and it still fits.";
    }
    let pinStatus = "Good";
    let pinResult = pin === "floating" ? "Floating pin." : "Pressed pin.";
    if (rod.pin === "pressed" && pin === "floating") {
        pinStatus = "No";
        pinResult = "These rods are pressed-pin. A floating pin needs a bushed rod.";
    } else if (rod.pin === "floating" && pin === "pressed") {
        pinStatus = "Watch";
        pinResult = "These rods are bushed for a floating pin.";
    }
    let headStatus = "Good";
    let headResult = "Clears a " + bore.toFixed(3) + " in bore.";
    if (!head.direct) {
        headStatus = "Watch";
        headResult = "Needs the matching rockers and intake. Not a simple cathedral swap.";
    }
    if (bore + 0.002 < head.minBore) {
        headStatus = "No";
        headResult = "The chamber wants a " + head.minBore.toFixed(3) + " in bore or larger.";
    }
    const rrStatus = rodRatio < 1.5 ? "Watch" : "Good";
    const rrResult = rodRatio.toFixed(2) + ":1. " + (rodRatio < 1.5 ? "Low rod ratio and more skirt load." : (rodRatio > 1.8 ? "High rod ratio, happier at RPM." : "Healthy rod ratio."));
    const rpmStatus = rpm <= rod.rpm ? "Good" : "Watch";
    let powerStatus = "Good";
    let powerResult = "About " + Math.round(airHp) + " HP at the crank.";
    if (nitrous) powerResult += " The " + Math.round(shot) + " HP shot is added to the naturally aspirated estimate.";
    if (!realClearance) {
        powerStatus = "No";
        powerResult = "Compression volume is not real until the piston clears the head.";
    } else if (boosted && boost > block.boost + 0.4) {
        powerStatus = "No";
        powerResult = "About " + Math.round(airHp) + " HP at the crank. This block's planning limit is " + block.boost + " PSI, and the request is " + boost.toFixed(1) + " PSI.";
    } else if (airHp > hardware.hp + 20) {
        powerStatus = "Watch";
        powerResult += " " + hardware.phrase + " the planning limit at " + hardware.hp + " HP.";
    }
    const scrResult = realClearance
        ? scr.toFixed(2) + ":1. Target " + band.scrLo.toFixed(1) + " to " + band.scrHi.toFixed(1) + " for this fuel and power adder."
        : "The piston is into the head. Add dish, gasket, or deck clearance.";
    const dcrResult = realClearance
        ? dcr.toFixed(2) + ":1 at " + ivc + " deg ABDC. Target " + band.dcrLo.toFixed(1) + " to " + band.dcrHi.toFixed(1) + "."
        : "No intake-closing compression until the piston clears the head.";
    const camResult = cam.duration + " deg at 0.050, " + cam.lift.toFixed(3) + " in lift, " + cam.lsa + " LSA, intake closes " + (ivcRaw ? ivc + " deg ABDC typed" : cam.ivc + " deg ABDC") + ".";
    publishReadout([
        { label: "Displacement", value: cid, unit: "ci", primary: true },
        { label: "Stroke class", value: strokeLabel, unit: "text" },
        { label: "Static compression", value: realClearance ? scr : 0, unit: "ratio" },
        { label: "Dynamic compression", value: realClearance ? dcr : 0, unit: "ratio" },
        { label: unitState.power === "whp" ? "Power at the wheels" : "Power at the crank", value: Math.round(shown).toLocaleString("en-US") + (unitState.power === "whp" ? " WHP" : " HP"), unit: "text" },
        { label: "Piston height", value: ch, unit: "in3" },
        { label: "Rod ratio", value: rodRatio, unit: "ratio" },
        { label: "Bore", value: bore, unit: "in3" },
        { label: "Stroke", value: stroke, unit: "in3" }
    ]);
    lsText("ls-block-note", block.note + " Stock bore " + block.bore.toFixed(3) + " in, safe overbore " + block.safeBore.toFixed(3) + " in, sleeve limit " + block.maxBore.toFixed(3) + " in. Planning rating " + block.hp + " HP and " + block.boost + " PSI.");
    lsText("ls-crank-note", crank.note + " Planning limit " + crank.hp + " HP.");
    lsText("ls-rod-note", rod.note + " Planning limit " + rod.hp + " HP and " + rod.rpm.toLocaleString("en-US") + " RPM.");
    lsText("ls-head-note", head.note);
    lsText("ls-piston-note", piston.note);
    const assess = document.getElementById("ls-assess");
    if (assess) {
        const intentName = intent === "turbo" ? "turbo" : (intent === "super" ? "supercharged" : (nitrous ? "nitrous" : "naturally aspirated"));
        const sentences = [cid.toFixed(0) + " ci " + intentName + " combination. " + strokeLabel + "."];
        if (!realClearance) sentences.push("The piston is into the head. Add dish, gasket thickness, or deck clearance before the compression number means anything.");
        else if (scrStatus === "Good" && dcrStatus === "Good") sentences.push("Static compression is " + scr.toFixed(2) + ":1 and dynamic is " + dcr.toFixed(2) + ":1. Both sit in the usual window for this fuel.");
        else sentences.push("Static compression is " + scr.toFixed(2) + ":1 and dynamic is " + dcr.toFixed(2) + ":1. One of them sits outside the usual window for this fuel.");
        sentences.push(chResult);
        if (headStatus !== "Good") sentences.push(headResult);
        sentences.push(powerResult);
        sentences.push("Starting cam: " + cam.duration + " degrees at 0.050, " + cam.lift.toFixed(3) + " in lift, " + cam.lsa + " LSA, intake closing " + ivc + " degrees ABDC.");
        assess.textContent = sentences.join(" ");
    }
    const body = document.getElementById("ls-matrix");
    if (body) {
        body.replaceChildren(
            matrixRow("Bore", block.label, bore.toFixed(3) + " in. " + boreResult, boreStatus),
            matrixRow("Stroke", crank.label, stroke.toFixed(3) + " in. " + strokeLabel + " versus the factory " + block.stockStroke.toFixed(3) + " in stroke.", "Good"),
            matrixRow("Piston height", rodLen.toFixed(3) + " in rod", chResult, chStatus),
            matrixRow("Rod ratio", rod.label, rrResult, rrStatus),
            matrixRow("Wrist pin", pin === "floating" ? "Floating" : "Pressed", pinResult, pinStatus),
            matrixRow("Heads", head.label, headResult, headStatus),
            matrixRow("Static compression", chamber.toFixed(1) + " cc chamber", scrResult, scrStatus),
            matrixRow("Dynamic compression", ivc + " deg ABDC", dcrResult, dcrStatus),
            matrixRow("RPM", rod.label, Math.round(rpm).toLocaleString("en-US") + " RPM. Rod planning limit is " + rod.rpm.toLocaleString("en-US") + ".", rpmStatus),
            matrixRow("Power", nitrous ? (Math.round(shot) + " HP shot") : (boosted ? (boost.toFixed(1) + " PSI") : "Naturally aspirated"), powerResult, powerStatus),
            matrixRow("Cam profile", nitrous ? "Nitrous" : (intent === "turbo" ? "Turbo" : (intent === "super" ? "Supercharged" : "Naturally aspirated")), camResult, "Good")
        );
    }
}
const lsBlock = document.getElementById("ls-block");
if (lsBlock) {
    lsBlock.addEventListener("change", () => {
        const next = LS.blocks[lsBlock.value];
        if (next) document.getElementById("ls-bore").value = next.bore.toFixed(3);
    });
}
const lsPiston = document.getElementById("ls-piston");
if (lsPiston) {
    lsPiston.addEventListener("change", () => {
        const next = LS.pistons[lsPiston.value];
        if (next) document.getElementById("ls-dish").value = next.dish;
    });
}
const lsIntent = document.getElementById("ls-intent");
if (lsIntent) {
    lsIntent.addEventListener("change", () => {
        const field = document.getElementById("ls-boost");
        if (!field) return;
        const current = parseFloat(field.value);
        if (lsIntent.value === "nitrous") {
            field.step = "25";
            if (!Number.isFinite(current) || current < 50) field.value = "150";
        } else if (lsIntent.value === "turbo" || lsIntent.value === "super") {
            field.step = "0.5";
            if (Number.isFinite(current) && current > 45) field.value = "10";
        }
    });
}
bindCalc(calcLs, ["ls-block", "ls-bore", "ls-crank", "ls-rod", "ls-rodlen", "ls-pin", "ls-piston", "ls-head", "ls-intent", "ls-fuel", "ls-boost", "ls-rpm", "ls-gasket", "ls-deck", "ls-deck-height", "ls-dish", "ls-chamber", "ls-ivc", "dt-loss"]);
"""
LS_PAGE_SCRIPT = LS_SCRIPT.replace("%%LS%%", json.dumps(LS_CATALOG, separators=(",", ":")))

def fuel_pump_html(row):
    fuel = field(row, "fuel", "gasoline")
    if fuel not in {key for key, _label in PUMP_FUELS}:
        fuel = "gasoline"
    boost = field(row, "boost", "20")
    try:
        boosted = float(boost) > 0
    except ValueError:
        boosted = True
        boost = "20"
    turbo_selected = " selected" if boosted else ""
    na_selected = "" if boosted else " selected"
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="fp-hp">Target power</label><input type="number" id="fp-hp" value="{esc(field(row, 'hp', '1000'))}" min="50" step="25"></div>
        <div class="field"><label for="fp-ind">Induction</label>
            <select id="fp-ind">
                <option value="na"{na_selected}>Naturally aspirated</option>
                <option value="turbo"{turbo_selected}>Turbocharged</option>
                <option value="supercharged">Supercharged</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="fp-fuel">Fuel</label><select id="fp-fuel">{options(PUMP_FUELS, fuel)}</select></div>
        <div class="field"><label for="fp-system">Fuel system</label>
            <select id="fp-system">
                <option value="return" selected>Return, 1:1 regulator</option>
                <option value="returnless">Returnless, fixed pressure</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="fp-base">Base fuel pressure (PSI)</label><input type="number" id="fp-base" value="43.5" min="4" max="120" step="0.5"></div>
        <div class="field"><label for="fp-boost">Boost (PSI)</label><input type="number" id="fp-boost" value="{esc(boost)}" min="0" max="80" step="0.5"></div>
    </div>
    <p class="field-hint">A return system with a 1:1 regulator makes the pump hold base pressure plus boost. A returnless system holds the base pressure unless the controller raises it with boost. A carburetor is usually about 6 to 8 PSI with the induction set to naturally aspirated.</p>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="fp-bsfc">Custom BSFC</label><input type="number" id="fp-bsfc" placeholder="Auto" min="0.2" max="2" step="0.01"></div>
        <div class="field"><label for="fp-margin">Pump margin (%)</label><input type="number" id="fp-margin" value="25" min="0" max="60" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="fp-rated-lph">Your pump, catalog flow (L/h)</label><input type="number" id="fp-rated-lph" placeholder="e.g. 450" min="0" step="5"></div>
        <div class="field"><label for="fp-rated-psi">That flow is rated at (PSI)</label><input type="number" id="fp-rated-psi" value="40" min="0" max="150" step="1"></div>
    </div>
    <div class="field"><label for="fp-deadhead">Deadhead pressure (PSI)</label><input type="number" id="fp-deadhead" value="120" min="60" max="200" step="5"></div>
    <p class="field-hint">Leave the pump flow blank to size from horsepower only. Catalog flows are usually taken near 40 PSI. Above that, flow is estimated on a straight line from the rating down to the deadhead.</p>
    """ + LOSS_FIELDS
    results = """
    <p class="assess" id="fp-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Pump class</th><th>At your pressure</th><th>Vs target</th><th>Status</th></tr></thead>
            <tbody id="fp-pumps"></tbody>
        </table>
        <p class="field-hint">Classes are common catalog ratings at 40 PSI, not a brand chart. Multiple-pump rows assume the pumps share the rail and the voltage stays up. The 1400 L/h rows are large external electric pumps.</p>
    </div>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Mechanical pump</th><th>Rating</th><th>On this job</th><th>Status</th></tr></thead>
            <tbody id="fp-mech"></tbody>
        </table>
        <p class="field-hint">Cam rows are diaphragm pumps. The GPH number is free flow, and the shutoff is the pressure where they stop. Belt rows are gear or gerotor pumps: 6 and 12 GPM follow the Aeromotive belt-drive classes, and 6.8 and 12.5 GPM follow Weldon 34706 and 34712, which publish a boosted EFI rating at 80 PSI. A belt pump's flow follows its rpm. The Weldon gear pumps are rated near 4,000 pump rpm.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print pump spec sheet", power_toggle=True, results_extra=results)


FUEL_PUMP_SCRIPT = r"""
const PUMP_BSFC = {
    gasoline: { turbo: 0.65, supercharged: 0.65, na: 0.50 },
    e85: { turbo: 0.95, supercharged: 0.95, na: 0.75 },
    e98: { turbo: 1.02, supercharged: 1.02, na: 0.82 },
    methanol: { turbo: 1.20, supercharged: 1.20, na: 0.95 },
    race: { turbo: 0.70, supercharged: 0.70, na: 0.55 },
    diesel: { turbo: 0.40, supercharged: 0.40, na: 0.37 }
};
const PUMP_DENSITY = { gasoline: 6.17, e85: 6.55, e98: 6.59, methanol: 6.63, race: 6.20, diesel: 7.05 };
const PUMP_SHELF = [
    { label: "255 L/h", lph: 255 },
    { label: "340 L/h", lph: 340 },
    { label: "450 L/h", lph: 450 },
    { label: "525 L/h", lph: 525 },
    { label: "Dual 340", lph: 680 },
    { label: "Dual 450", lph: 900 },
    { label: "Dual 525", lph: 1050 },
    { label: "Triple 450", lph: 1350 },
    { label: "Triple 525", lph: 1575 },
    { label: "Quad 450", lph: 1800 },
    { label: "Quad 525", lph: 2100 },
    { label: "Dual 1400 external", lph: 2800 },
    { label: "Triple 1400 external", lph: 4200 }
];
const LITER_PER_GALLON = 3.78541;
const SHELF_RATED_PSI = 40;
const MECH_PUMPS = [
    { label: "Cam 80 GPH", detail: "Street diaphragm", gph: 80, shutoff: 7.5, kind: "cam" },
    { label: "Cam 110 GPH", detail: "Performance diaphragm", gph: 110, shutoff: 8, kind: "cam" },
    { label: "Cam 130 GPH", detail: "Race diaphragm", gph: 130, shutoff: 9, kind: "cam" },
    { label: "Cam 170 GPH", detail: "HP billet diaphragm", gph: 170, shutoff: 11, kind: "cam" },
    { label: "Cam 225 GPH", detail: "Alcohol diaphragm", gph: 225, shutoff: 17, kind: "cam" },
    { label: "Belt 6 GPM", detail: "Gerotor, Aeromotive 6 GPM class", gph: 360, shutoff: 80, kind: "belt" },
    { label: "Belt 6.8 GPM", detail: "Gear, Weldon 34706 class", gph: 408, shutoff: 80, kind: "belt" },
    { label: "Belt 12 GPM", detail: "Gerotor, Aeromotive 12 GPM class", gph: 720, shutoff: 80, kind: "belt" },
    { label: "Belt 12.5 GPM", detail: "Gear, Weldon 34712 class", gph: 750, shutoff: 80, kind: "belt" }
];

function flowAtPressure(catalogLph, ratedPsi, workPsi, deadhead) {
    if (!(catalogLph > 0)) return 0;
    if (workPsi <= ratedPsi) return catalogLph;
    if (deadhead <= workPsi || deadhead <= ratedPsi) return 0;
    return catalogLph * (deadhead - workPsi) / (deadhead - ratedPsi);
}

function fpVolume(gph) {
    if (unitState.system === "metric") return Math.round(gph * LITER_PER_GALLON).toLocaleString("en-US") + " L/h";
    return Math.round(gph).toLocaleString("en-US") + " GPH";
}

function mechJob(pump, workPsi, shopGph) {
    if (pump.kind === "cam" && workPsi >= pump.shutoff - 0.2) {
        return {
            flow: 0,
            status: "No",
            result: "Shutoff is " + pump.shutoff + " PSI, so it cannot hold this pressure."
        };
    }
    if (pump.kind === "belt" && workPsi > pump.shutoff) {
        return {
            flow: 0,
            status: "No",
            result: "The published boosted window stops at " + pump.shutoff + " PSI."
        };
    }
    const covers = pump.gph + 0.5 >= shopGph;
    if (pump.kind === "cam") {
        if (!covers) {
            return { flow: pump.gph, status: "Short", result: "Free flow is short of the shopping target." };
        }
        if (workPsi > 12) {
            return {
                flow: pump.gph,
                status: "Watch",
                result: "Free flow covers the volume, and the shutoff is only " + pump.shutoff + " PSI."
            };
        }
        return {
            flow: pump.gph,
            status: "Good",
            result: "Free flow covers a carb at this pressure. Regulated flow is below the free-flow number."
        };
    }
    if (!covers) return { flow: pump.gph, status: "Short", result: "Rated flow is short of the shopping target." };
    return {
        flow: pump.gph,
        status: "Good",
        result: "Rated flow covers this job through " + pump.shutoff + " PSI. Pulley ratio sets the pump rpm."
    };
}

function calcFuelPump() {
    const hp = crankHorsepower(document.getElementById("fp-hp").value || 1000);
    const induction = document.getElementById("fp-ind").value || "turbo";
    const fuelKey = document.getElementById("fp-fuel").value || "gasoline";
    const system = document.getElementById("fp-system").value || "return";
    const custom = parseFloat(document.getElementById("fp-bsfc").value);
    const table = PUMP_BSFC[fuelKey] || PUMP_BSFC.gasoline;
    const bsfc = Number.isFinite(custom) && custom > 0 ? custom : (table[induction] || table.turbo);
    const density = PUMP_DENSITY[fuelKey] || 6.17;
    let base = parseFloat(document.getElementById("fp-base").value);
    if (!Number.isFinite(base) || base < 4) base = 43.5;
    base = Math.min(120, base);
    let boost = parseFloat(document.getElementById("fp-boost").value);
    if (!Number.isFinite(boost) || boost < 0) boost = 0;
    const boostInput = document.getElementById("fp-boost");
    if (boostInput) boostInput.disabled = induction === "na";
    const addedBoost = induction === "na" || system === "returnless" ? 0 : boost;
    const workPsi = base + addedBoost;
    let marginPct = parseFloat(document.getElementById("fp-margin").value);
    if (!Number.isFinite(marginPct)) marginPct = 25;
    marginPct = Math.min(60, Math.max(0, marginPct));
    let deadhead = parseFloat(document.getElementById("fp-deadhead").value);
    if (!Number.isFinite(deadhead) || deadhead < 60) deadhead = 120;
    const demandLbHr = hp * bsfc;
    const demandGph = demandLbHr / density;
    const shopGph = demandGph * (1 + marginPct / 100);
    const shopLph = shopGph * LITER_PER_GALLON;
    let ratedLph = parseFloat(document.getElementById("fp-rated-lph").value);
    let ratedPsi = parseFloat(document.getElementById("fp-rated-psi").value);
    if (!Number.isFinite(ratedPsi) || ratedPsi < 0) ratedPsi = SHELF_RATED_PSI;
    const hasPump = Number.isFinite(ratedLph) && ratedLph > 0;
    const pumpLph = hasPump ? flowAtPressure(ratedLph, ratedPsi, workPsi, deadhead) : 0;
    const pumpGph = pumpLph / LITER_PER_GALLON;
    const rows = [
        { label: "Pump to buy", value: shopGph, unit: "gph", primary: true },
        { label: "Engine demand", value: demandGph, unit: "gph" },
        { label: "Working pressure", value: workPsi, unit: "psi" },
        { label: "Fuel mass", value: demandLbHr, unit: "lbhr" },
        { label: "BSFC used", value: bsfc.toFixed(2), unit: "text" },
        { label: "Margin", value: marginPct, unit: "pct" }
    ];
    if (hasPump) {
        rows.push({ label: "Your pump at pressure", value: pumpGph, unit: "gph" });
        rows.push({ label: "Pump vs target", value: shopLph > 0 ? (pumpLph / shopLph) * 100 : 0, unit: "pct" });
    }
    publishReadout(rows);

    const assess = document.getElementById("fp-assess");
    if (assess) {
        const pressureNote = system === "returnless"
            ? "Returnless holds " + base.toFixed(1) + " PSI, so boost is not added to the pump."
            : (induction === "na"
                ? "Naturally aspirated, so the pump only has to hold the " + base.toFixed(1) + " PSI base."
                : "The 1:1 regulator puts the pump at " + base.toFixed(1) + " + " + boost.toFixed(1) + " = " + workPsi.toFixed(1) + " PSI.");
        let pumpNote = "";
        if (hasPump) {
            if (workPsi > deadhead) {
                pumpNote = " Working pressure is past the deadhead, so this estimate says the pump is stalled.";
            } else if (pumpLph + 0.5 >= shopLph) {
                pumpNote = " The entered pump still has about " + Math.round(pumpLph) + " L/h at that pressure, which covers the shopping target.";
            } else {
                pumpNote = " The entered pump estimates about " + Math.round(pumpLph) + " L/h at that pressure, short of the " + Math.round(shopLph) + " L/h shopping target.";
            }
        }
        assess.textContent = "The engine wants " + demandLbHr.toFixed(0) + " lb/hr. Buy a pump that still moves about " + Math.round(shopLph) + " L/h at " + workPsi.toFixed(1) + " PSI after the " + Math.round(marginPct) + "% margin. " + pressureNote + pumpNote;
    }

    const mechBody = document.getElementById("fp-mech");
    let mechPick = null;
    const mechRows = MECH_PUMPS.map(pump => {
        const job = mechJob(pump, workPsi, shopGph);
        return { pump: pump, job: job };
    });
    mechRows.forEach(row => {
        if (mechPick === null && row.job.status === "Good") mechPick = row.pump.label;
    });
    if (assess && mechPick) {
        assess.textContent += " The smallest mechanical pump that covers it is the " + mechPick + ".";
    } else if (assess) {
        assess.textContent += " None of the mechanical pumps cover this pressure and volume together.";
    }

    const body = document.getElementById("fp-pumps");
    if (body) {
        body.replaceChildren();
        let recommended = null;
        PUMP_SHELF.forEach(pump => {
            const atPressure = flowAtPressure(pump.lph, SHELF_RATED_PSI, workPsi, deadhead);
            if (recommended === null && atPressure + 0.5 >= shopLph) recommended = pump.label;
        });
        PUMP_SHELF.forEach(pump => {
            const atPressure = flowAtPressure(pump.lph, SHELF_RATED_PSI, workPsi, deadhead);
            const covers = atPressure + 0.5 >= shopLph;
            const tr = document.createElement("tr");
            let status = "Short";
            let badge = "badge-no";
            if (pump.label === recommended) {
                tr.className = "is-rec";
                status = "Recommended";
                badge = "badge-rec";
            } else if (covers) {
                status = "Covers";
                badge = "badge-ok";
            } else {
                tr.className = "is-small";
            }
            const nameCell = document.createElement("td");
            nameCell.textContent = pump.label;
            const sub = document.createElement("div");
            sub.className = "size-sub";
            sub.textContent = pump.lph + " L/h at " + SHELF_RATED_PSI + " PSI";
            nameCell.appendChild(sub);
            const flowCell = document.createElement("td");
            flowCell.textContent = Math.round(atPressure).toLocaleString("en-US") + " L/h";
            const versus = shopLph > 0 ? (atPressure / shopLph) * 100 : 0;
            const versusCell = document.createElement("td");
            versusCell.textContent = Math.round(versus) + "%";
            versusCell.className = covers ? "tone-ok" : "tone-over";
            const statusCell = document.createElement("td");
            const pill = document.createElement("span");
            pill.className = "badge " + badge;
            pill.textContent = status;
            statusCell.appendChild(pill);
            tr.append(nameCell, flowCell, versusCell, statusCell);
            body.appendChild(tr);
        });
    }
    if (mechBody) {
        mechBody.replaceChildren();
        mechRows.forEach(row => {
            const job = row.job;
            const pump = row.pump;
            const tr = document.createElement("tr");
            let status = job.status === "Short" ? "Short" : job.status;
            let badge = "badge-no";
            if (pump.label === mechPick) {
                tr.className = "is-rec";
                status = "Recommended";
                badge = "badge-rec";
            } else if (job.status === "Good") {
                status = "Covers";
                badge = "badge-ok";
            } else if (job.status === "Watch") {
                badge = "badge-tight";
            } else {
                tr.className = "is-small";
            }
            const nameCell = document.createElement("td");
            nameCell.textContent = pump.label;
            const sub = document.createElement("div");
            sub.className = "size-sub";
            sub.textContent = pump.detail;
            nameCell.appendChild(sub);
            const ratingCell = document.createElement("td");
            ratingCell.textContent = pump.kind === "cam"
                ? fpVolume(pump.gph) + " free, " + pump.shutoff + " PSI shutoff"
                : fpVolume(pump.gph) + " through " + pump.shutoff + " PSI";
            const resultCell = document.createElement("td");
            resultCell.textContent = job.result;
            const statusCell = document.createElement("td");
            const pill = document.createElement("span");
            pill.className = "badge " + badge;
            pill.textContent = status;
            statusCell.appendChild(pill);
            tr.append(nameCell, ratingCell, resultCell, statusCell);
            mechBody.appendChild(tr);
        });
    }
}
bindCalc(calcFuelPump, ["fp-hp", "fp-ind", "fp-fuel", "fp-system", "fp-base", "fp-boost", "fp-bsfc", "fp-margin", "fp-rated-lph", "fp-rated-psi", "fp-deadhead", "dt-loss"]);
"""

N2O_SYSTEMS = (("plate", "Wet plate"), ("fogger", "Wet fogger"), ("direct", "Direct port"), ("dry", "Dry EFI"))
N2O_FUELS = (("gasoline", "Gasoline (91/93)"), ("e85", "E85"), ("methanol", "Methanol"), ("race", "Race gas"))
N2O_STAGES = (("1", "Single stage"), ("2", "Two stage"))
N2O_DELIVERY = (("full", "Full hit"), ("progressive", "Progressive"))


def _n2o(**overrides):
    preset = {
        "base": "500",
        "shot": "150",
        "shot2": "100",
        "system": "plate",
        "stages": "1",
        "fuel": "gasoline",
        "bottle": "950",
        "fuelpsi": "6",
        "cylinders": "8",
        "timing": "34",
        "inj": "60",
        "injcount": "8",
        "delivery": "full",
        "start": "40",
        "end": "100",
        "ramp": "2.0",
        "ontime": "6",
        "delay": "1.2",
        "bottlelb": "10",
        "spec": "150 HP gasoline plate at 950 PSI",
    }
    preset.update(overrides)
    return preset


N2O_PRESETS = {
    "nitrous-shot-calculator": _n2o(),
    "100-shot-gasoline-nitrous-calculator": _n2o(shot="100", spec="100 HP gasoline plate at 950 PSI"),
    "150-shot-gasoline-nitrous-calculator": _n2o(shot="150", spec="150 HP gasoline plate at 950 PSI"),
    "200-shot-gasoline-nitrous-calculator": _n2o(shot="200", spec="200 HP gasoline plate at 950 PSI"),
    "250-shot-gasoline-nitrous-calculator": _n2o(shot="250", spec="250 HP gasoline plate at 950 PSI"),
    "e85-nitrous-jet-calculator": _n2o(fuel="e85", spec="150 HP E85 plate at 950 PSI"),
    "methanol-nitrous-jet-calculator": _n2o(fuel="methanol", shot="200", spec="200 HP methanol plate at 950 PSI"),
    "direct-port-nitrous-calculator": _n2o(system="direct", shot="250", spec="250 HP direct port, eight nozzles"),
    "two-stage-nitrous-calculator": _n2o(stages="2", shot="150", shot2="100", spec="150 HP first stage, 100 HP second stage"),
    "dry-nitrous-efi-calculator": _n2o(system="dry", fuelpsi="43.5", spec="150 HP dry EFI shot, 60 lb/hr injectors"),
    "progressive-nitrous-calculator": _n2o(delivery="progressive", shot="200", spec="200 HP progressive shot, 40% to 100%"),
    "fogger-nitrous-calculator": _n2o(system="fogger", shot="175", spec="175 HP fogger, two nozzles"),
}


def n2o_preset(slug):
    return N2O_PRESETS.get(slug, N2O_PRESETS["nitrous-shot-calculator"])


def n2o_html(row):
    preset = n2o_preset(row["slug"])
    shot2_disabled = " disabled" if preset["stages"] != "2" else ""
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="nx-base">Base engine power</label><input type="number" id="nx-base" value="{esc(preset["base"])}" min="50" step="10"></div>
        <div class="field"><label for="nx-shot">Stage 1 shot (HP)</label><input type="number" id="nx-shot" value="{esc(preset["shot"])}" min="25" max="800" step="25"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-system">System</label><select id="nx-system">{options(N2O_SYSTEMS, preset["system"])}</select></div>
        <div class="field"><label for="nx-fuel">Fuel</label><select id="nx-fuel">{options(N2O_FUELS, preset["fuel"])}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-stages">Stages</label><select id="nx-stages">{options(N2O_STAGES, preset["stages"])}</select></div>
        <div class="field"><label for="nx-shot2">Stage 2 shot (HP)</label><input type="number" id="nx-shot2" value="{esc(preset["shot2"])}" min="0" max="600" step="25"{shot2_disabled}></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-bottle">Bottle pressure (PSI)</label><input type="number" id="nx-bottle" value="{esc(preset["bottle"])}" min="300" max="1200" step="10"></div>
        <div class="field"><label for="nx-fuelpsi">Fuel pressure (PSI)</label><input type="number" id="nx-fuelpsi" value="{esc(preset["fuelpsi"])}" min="1" max="120" step="0.5"></div>
    </div>
    <p class="field-hint">Jets are starting orifices for this shot at the bottle pressure on the gauge. A 900 to 950 PSI bottle is the usual tune window. Wet fuel pressure is often about 6 PSI at the fuel solenoid. Dry EFI uses rail pressure.</p>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="nx-cylinders">Cylinders</label><input type="number" id="nx-cylinders" value="{esc(preset["cylinders"])}" min="4" max="16" step="1"></div>
        <div class="field"><label for="nx-timing">Base timing (deg)</label><input type="number" id="nx-timing" value="{esc(preset["timing"])}" min="10" max="50" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-delivery">Controller</label><select id="nx-delivery">{options(N2O_DELIVERY, preset["delivery"])}</select></div>
        <div class="field"><label for="nx-ontime">Time on the button (sec)</label><input type="number" id="nx-ontime" value="{esc(preset["ontime"])}" min="0.5" max="20" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-start">Progressive start (%)</label><input type="number" id="nx-start" value="{esc(preset["start"])}" min="0" max="100" step="5"></div>
        <div class="field"><label for="nx-end">Progressive end (%)</label><input type="number" id="nx-end" value="{esc(preset["end"])}" min="0" max="100" step="5"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-ramp">Ramp time (sec)</label><input type="number" id="nx-ramp" value="{esc(preset["ramp"])}" min="0.2" max="8" step="0.1"></div>
        <div class="field"><label for="nx-delay">Stage 2 delay (sec)</label><input type="number" id="nx-delay" value="{esc(preset["delay"])}" min="0" max="8" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="nx-inj">Injector size (lb/hr)</label><input type="number" id="nx-inj" value="{esc(preset["inj"])}" min="10" max="500" step="1"></div>
        <div class="field"><label for="nx-injcount">Injector count</label><input type="number" id="nx-injcount" value="{esc(preset["injcount"])}" min="1" max="16" step="1"></div>
    </div>
    <div class="field"><label for="nx-bottlelb">Bottle size (lb)</label><input type="number" id="nx-bottlelb" value="{esc(preset["bottlelb"])}" min="5" max="30" step="1"></div>
    <p class="field-hint">A fogger here is two nozzles. Direct port uses one nozzle per cylinder. Leave the controller on Full hit unless a progressive box is ramping the solenoid.</p>
    {LOSS_FIELDS}
    """
    results = """
    <p class="assess" id="nx-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Check</th><th>Detail</th><th>Result</th><th>Status</th></tr></thead>
            <tbody id="nx-matrix"></tbody>
        </table>
        <p class="field-hint">Hit horsepower is the base engine plus the full shot. Average horsepower is the button with a progressive ramp or a second-stage delay. Weigh the bottle after a timed hit before trusting the flow.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print nitrous sheet", power_toggle=True, results_extra=results)


N2O_SCRIPT = r"""
const N2O_FUEL = {
    gasoline: { ratio: 5.8, density: 6.17, bsfc: 0.50, degPer50: 2.0, rho: 740 },
    e85: { ratio: 3.85, density: 6.55, bsfc: 0.68, degPer50: 1.5, rho: 785 },
    methanol: { ratio: 2.54, density: 6.63, bsfc: 0.95, degPer50: 1.0, rho: 795 },
    race: { ratio: 5.8, density: 6.20, bsfc: 0.55, degPer50: 1.5, rho: 745 }
};
const BOTTLE_CHART = [[0, 283], [10, 335], [20, 387], [32, 460], [40, 520], [50, 590], [60, 675], [70, 760], [80, 865], [85, 950], [97, 1069]];

function nxNum(id, fallback) {
    const el = document.getElementById(id);
    const value = el ? parseFloat(el.value) : NaN;
    return Number.isFinite(value) ? value : fallback;
}

function nxClamp(value, lo, hi) {
    return Math.min(hi, Math.max(lo, value));
}

function bottleTemp(psi) {
    if (psi <= BOTTLE_CHART[0][1]) return BOTTLE_CHART[0][0];
    for (let i = 1; i < BOTTLE_CHART.length; i++) {
        if (psi <= BOTTLE_CHART[i][1]) {
            const span = BOTTLE_CHART[i][1] - BOTTLE_CHART[i - 1][1];
            const mix = span > 0 ? (psi - BOTTLE_CHART[i - 1][1]) / span : 0;
            return BOTTLE_CHART[i - 1][0] + mix * (BOTTLE_CHART[i][0] - BOTTLE_CHART[i - 1][0]);
        }
    }
    return BOTTLE_CHART[BOTTLE_CHART.length - 1][0];
}

function nozzleCount(system, cylinders) {
    if (system === "direct") return Math.max(1, Math.round(cylinders));
    if (system === "fogger") return 2;
    return 1;
}

function nitrousJetInches(hp, nozzles, bottlePsi) {
    const each = hp / Math.max(1, nozzles);
    const factor = Math.sqrt(Math.max(300, bottlePsi) / 900);
    if (!(each > 0) || !(factor > 0)) return 0;
    return Math.sqrt(each / (70 * factor)) / 25.4;
}

function fuelJetInches(lbPerHr, psi, rho) {
    if (!(lbPerHr > 0) || !(psi > 0) || !(rho > 0)) return 0;
    const mass = lbPerHr * 0.45359237 / 3600;
    const drop = psi * 6894.757;
    const areaM2 = mass / (0.75 * Math.sqrt(2 * rho * drop));
    const areaIn2 = areaM2 / 0.00064516;
    return Math.sqrt(areaIn2 / 0.785398163);
}

function jetLabel(inches) {
    if (!(inches > 0) || !Number.isFinite(inches)) return "—";
    const thou = Math.max(10, Math.round(inches * 1000));
    return "0." + String(thou).padStart(3, "0") + " in (" + thou + ")";
}

function averageFraction(delivery, start, end, ramp, onTime) {
    if (delivery !== "progressive") return 1;
    const time = Math.max(0.1, onTime);
    const span = Math.max(0.1, ramp);
    const open = nxClamp(start, 0, 100) / 100;
    const close = nxClamp(end, 0, 100) / 100;
    if (time <= span) {
        const reached = open + (close - open) * (time / span);
        return (open + reached) / 2;
    }
    return (span * (open + close) / 2 + (time - span) * close) / time;
}

function nxWheelScale() {
    if (unitState.power !== "whp") return 1;
    const loss = nxClamp(nxNum("dt-loss", 15) / 100, 0, 0.4);
    return 1 - loss;
}

function nxRow(name, detail, result, status) {
    const tr = document.createElement("tr");
    if (status === "No") tr.className = "is-small";
    const badge = status === "Good" ? "badge-ok" : (status === "Watch" ? "badge-tight" : "badge-no");
    [name, detail, result].forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
    });
    const statusCell = document.createElement("td");
    const pill = document.createElement("span");
    pill.className = "badge " + badge;
    pill.textContent = status;
    statusCell.appendChild(pill);
    tr.appendChild(statusCell);
    return tr;
}

function calcNitrous() {
    const fuelKey = document.getElementById("nx-fuel").value || "gasoline";
    const fuel = N2O_FUEL[fuelKey] || N2O_FUEL.gasoline;
    const system = document.getElementById("nx-system").value || "plate";
    const stages = document.getElementById("nx-stages").value || "1";
    const delivery = document.getElementById("nx-delivery").value || "full";
    const dry = system === "dry";
    const shot2El = document.getElementById("nx-shot2");
    if (shot2El) shot2El.disabled = stages !== "2";
    const base = Math.max(1, crankHorsepower(document.getElementById("nx-base").value || 500));
    const shot = nxClamp(nxNum("nx-shot", 150), 0, 800);
    const shot2 = stages === "2" ? nxClamp(nxNum("nx-shot2", 0), 0, 600) : 0;
    const totalShot = shot + shot2;
    const bottle = nxClamp(nxNum("nx-bottle", 950), 300, 1200);
    const fuelPsi = nxClamp(nxNum("nx-fuelpsi", dry ? 43.5 : 6), 1, 120);
    const cylinders = nxClamp(nxNum("nx-cylinders", 8), 1, 16);
    const nozzles = nozzleCount(system, cylinders);
    const timing = nxClamp(nxNum("nx-timing", 34), 0, 60);
    const onTime = nxClamp(nxNum("nx-ontime", 6), 0.2, 20);
    const delay = nxClamp(nxNum("nx-delay", 0), 0, onTime);
    const fraction = averageFraction(delivery, nxNum("nx-start", 40), nxNum("nx-end", 100), nxNum("nx-ramp", 2), onTime);
    const stagedTime = stages === "2" ? Math.max(0, onTime - delay) : onTime;
    const averageShot = stages === "2"
        ? (delay * shot * fraction + stagedTime * totalShot * fraction) / Math.max(0.1, onTime)
        : totalShot * fraction;
    const hit = base + totalShot;
    const average = base + averageShot;
    const scale = nxWheelScale();
    const n2oLbHr = totalShot * 3.6;
    const fuelLbHr = n2oLbHr / fuel.ratio;
    const jet1 = nitrousJetInches(shot, nozzles, bottle);
    const jet2 = shot2 > 0 ? nitrousJetInches(shot2, nozzles, bottle) : 0;
    const stageFuel = shot > 0 ? fuelJetInches((shot * 3.6 / fuel.ratio) / nozzles, fuelPsi, fuel.rho) : 0;
    const stage2Fuel = shot2 > 0 ? fuelJetInches((shot2 * 3.6 / fuel.ratio) / nozzles, fuelPsi, fuel.rho) : 0;
    const pull = totalShot / 50 * fuel.degPer50;
    const suggested = timing - pull;
    const firstHit = suggested - (fuelKey === "gasoline" ? 2 : 0);
    const temp = bottleTemp(bottle);
    const flowLbMin = n2oLbHr / 60;
    const used = flowLbMin * (onTime / 60) * (averageShot / Math.max(1, totalShot));
    const usable = Math.max(0, nxNum("nx-bottlelb", 10)) * 0.8;
    const passes = used > 0 ? usable / used : 0;
    const injCount = Math.max(1, nxNum("nx-injcount", 8));
    const injRated = Math.max(1, nxNum("nx-inj", 60)) * Math.sqrt(fuelPsi / 43.5);
    const baseFuel = base * fuel.bsfc;
    const duty = dry ? ((baseFuel + fuelLbHr) / injCount) / injRated * 100 : 0;
    const thou = Math.round(jet1 * 1000);
    let bottleStatus = "Good";
    let bottleResult = Math.round(temp) + " F bottle temperature sits on this pressure. The tune window is 900 to 950 PSI.";
    if (bottle < 850 || bottle > 1050) {
        bottleStatus = "No";
        bottleResult = Math.round(bottle) + " PSI is outside the tune window. Flow, the fuel ratio, and the hit all move with pressure.";
    } else if (bottle < 900 || bottle > 1000) {
        bottleStatus = "Watch";
        bottleResult = Math.round(temp) + " F is close. Hold 900 to 950 PSI if this jet is the one you want.";
    }
    let jetStatus = "Good";
    let jetResult = jetLabel(jet1) + " nitrous, shared across " + nozzles + (nozzles === 1 ? " nozzle." : " nozzles.");
    if (shot2 > 0) jetResult += " Stage 2 is " + jetLabel(jet2) + ".";
    const sameAt900 = shot * Math.sqrt(900 / bottle);
    jetResult += " This stage 1 jet is about a " + Math.round(sameAt900) + " HP shot if the bottle falls to 900 PSI.";
    if (thou > 100 && nozzles < 4) {
        jetStatus = "No";
        jetResult = jetLabel(jet1) + " is past a normal single orifice. Split it across more nozzles or a second stage.";
    } else if (thou > 80 && nozzles < 4) {
        jetStatus = "Watch";
        jetResult += " That orifice is getting large for one solenoid.";
    }
    let fuelStatus = "Good";
    let fuelResult = "";
    if (dry) {
        fuelResult = "Dry system. The injectors add " + fuelLbHr.toFixed(0) + " lb/hr on top of the engine. Duty is about " + duty.toFixed(0) + "% at this rail pressure.";
        if (duty > 95) {
            fuelStatus = "No";
            fuelResult += " The injectors are out of room.";
        } else if (duty > 80) {
            fuelStatus = "Watch";
            fuelResult += " That is past an 80% duty ceiling.";
        }
    } else {
        const each = nozzles > 1 ? " on each nozzle" : "";
        fuelResult = jetLabel(stageFuel) + " fuel" + each + ".";
        if (shot2 > 0) fuelResult += " Stage 2 fuel jet is " + jetLabel(stage2Fuel) + each + ".";
        fuelResult += " The shot wants " + fuelLbHr.toFixed(0) + " lb/hr (" + (fuelLbHr / fuel.density).toFixed(1) + " gal/hr) from the fuel solenoid.";
        if (fuelPsi < 4) {
            fuelStatus = "No";
            fuelResult += " Under about 5 PSI a carb-style fuel solenoid goes short on fuel.";
        } else if (fuelPsi < 5.5 || (fuelPsi > 8 && fuelPsi < 30)) {
            fuelStatus = "Watch";
            fuelResult += " Confirm this is the pressure at the solenoid while it is open.";
        }
    }
    let timeStatus = suggested >= 18 ? "Good" : "Watch";
    let timeResult = "Pull " + pull.toFixed(1) + " degrees. " + suggested.toFixed(1) + " degrees on a tuned hit.";
    if (fuelKey === "gasoline") timeResult += " A first hit at " + firstHit.toFixed(1) + " degrees leaves two degrees in reserve.";
    if (shot2 > 0) {
        const pull1 = shot / 50 * fuel.degPer50;
        timeResult += " Stage 1 alone pulls " + pull1.toFixed(1) + " degrees.";
    }
    if (suggested < 16) {
        timeStatus = "No";
        timeResult += " That pull lands very low. The shot or the base timing needs another look.";
    }
    const colder = totalShot >= 50 ? Math.max(1, Math.round(totalShot / 100)) : 0;
    const plugStatus = "Good";
    const plugResult = colder > 0
        ? colder + (colder === 1 ? " heat range colder" : " heat ranges colder") + ", gapped near 0.032 in, with a thick ground strap."
        : "A small shot can stay on the current heat range. Keep the gap near 0.035 in.";
    let feedStatus = "Good";
    let feedResult = "One nitrous solenoid and a -4 feed cover this shot.";
    if (nozzles >= 4) feedResult = "Direct port splits the shot across " + nozzles + " nozzles.";
    else if (totalShot > 300) {
        feedStatus = "No";
        feedResult = "One plate solenoid is past this shot. Use two stages, two solenoids, or a direct port.";
    } else if (totalShot > 175) {
        feedStatus = "Watch";
        feedResult = "A -6 feed or a second nitrous solenoid keeps the hit from leaning out as the solenoid runs out of flow.";
    }
    const passStatus = passes >= 4 ? "Good" : "Watch";
    const passResult = used.toFixed(2) + " lb per button. About " + passes.toFixed(1) + " hits from " + Math.round(usable) + " usable pounds in the bottle.";
    const powerLabel = unitState.power === "whp" ? "Power at the wheels" : "Power on the hit";
    const powerValue = Math.round(hit * scale).toLocaleString("en-US") + (unitState.power === "whp" ? " WHP" : " HP");
    publishReadout([
        { label: powerLabel, value: powerValue, unit: "text", primary: true },
        { label: "Average on the button", value: Math.round(average * scale).toLocaleString("en-US") + (unitState.power === "whp" ? " WHP" : " HP"), unit: "text" },
        { label: "Nitrous flow", value: flowLbMin, unit: "lbmin" },
        { label: "Stage 1 nitrous jet", value: jetLabel(jet1), unit: "text" },
        { label: dry ? "Injector duty" : "Stage 1 fuel jet", value: dry ? duty.toFixed(0) + "%" : jetLabel(stageFuel), unit: "text" },
        { label: "Timing on the hit", value: suggested.toFixed(1) + " deg", unit: "text" },
        { label: "Bottle temperature", value: temp, unit: "tempf" },
        { label: "Hits in the bottle", value: passes.toFixed(1), unit: "text" }
    ]);
    const assess = document.getElementById("nx-assess");
    if (assess) {
        const systemName = system === "direct" ? "direct-port" : (system === "fogger" ? "fogger" : (dry ? "dry EFI" : "plate"));
        const sentences = [
            Math.round(hit) + " HP on the hit from a " + Math.round(base) + " HP engine and a " + Math.round(totalShot) + " HP " + systemName + " shot."
        ];
        if (delivery === "progressive" || stages === "2") {
            sentences.push("The button averages about " + Math.round(average) + " HP because the solenoid is not at the full shot the whole time.");
        }
        sentences.push(jetResult);
        sentences.push(timeResult);
        sentences.push(passResult);
        assess.textContent = sentences.join(" ");
    }
    const body = document.getElementById("nx-matrix");
    if (body) {
        body.replaceChildren(
            nxRow("Bottle", Math.round(bottle) + " PSI", bottleResult, bottleStatus),
            nxRow("Nitrous jet", nozzles + (nozzles === 1 ? " nozzle" : " nozzles"), jetResult, jetStatus),
            nxRow(dry ? "Injectors" : "Fuel jet", dry ? injCount + " injectors" : fuelPsi.toFixed(1) + " PSI", fuelResult, fuelStatus),
            nxRow("Timing", Math.round(timing) + " deg base", timeResult, timeStatus),
            nxRow("Spark plugs", Math.round(totalShot) + " HP shot", plugResult, plugStatus),
            nxRow("Feed", system === "direct" ? "Direct port" : "Single feed", feedResult, feedStatus),
            nxRow("Bottle", nxNum("nx-bottlelb", 10).toFixed(0) + " lb", passResult, passStatus)
        );
    }
}
bindCalc(calcNitrous, ["nx-base", "nx-shot", "nx-shot2", "nx-system", "nx-fuel", "nx-stages", "nx-bottle", "nx-fuelpsi", "nx-cylinders", "nx-timing", "nx-delivery", "nx-ontime", "nx-start", "nx-end", "nx-ramp", "nx-delay", "nx-inj", "nx-injcount", "nx-bottlelb", "dt-loss"]);
"""

SHOCK_USES = (("strip", "Street-strip"), ("drag", "Drag car"), ("street", "Street car"))
SHOCK_SURFACES = (("radial", "Radial prep"), ("prepped", "Prepped"), ("noprep", "No prep"))
SHOCK_TIRES = (("radial", "Drag radial"), ("slick", "Bias slick"), ("street", "Street tire"))
SHOCK_STYLES = (("double", "Double adjustable"), ("single", "Single adjustable"))
SHOCK_BRANDS = (
    ("qa1", "QA1 (0-18, higher is firmer)"),
    ("strange", "Strange (0-16, higher is firmer)"),
    ("viking", "Viking (0-24, higher is firmer)"),
    ("afco", "Afco (0-12, higher is firmer)"),
    ("generic", "Generic (0-18, higher is firmer)"),
)
SHOCK_HITS = (
    ("power", "Power adder comes in"),
    ("na", "Naturally aspirated"),
    ("brake", "On the brake or transbrake"),
)
SHOCK_REARS = (
    ("fourlink", "4-link"),
    ("ladder", "Ladder bar"),
    ("torquearm", "Torque arm"),
    ("coilover", "Coilover"),
    ("stock", "Stock arms or leaf"),
)
SHOCK_SYMPTOMS = (
    ("baseline", "Baseline"),
    ("spin", "Spins on the hit"),
    ("dead", "No bite"),
    ("wheelie", "Wheelstands"),
    ("unload", "Unloads on the shift"),
    ("shake", "Shakes the tire"),
)


def _shock(**overrides):
    preset = {
        "use": "strip",
        "surface": "radial",
        "tire": "radial",
        "style": "double",
        "brand": "qa1",
        "hp": "650",
        "weight": "3400",
        "hit": "power",
        "rear": "fourlink",
        "symptom": "baseline",
        "spec": "street-strip, radial prep, drag radial, double-adjustable QA1",
    }
    preset.update(overrides)
    return preset


SHOCK_PRESETS = {
    "drag-shock-calculator": _shock(),
    "prepped-slick-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", hp="1000", weight="3200", hit="brake",
        spec="prepped slick, on the brake, double-adjustable QA1",
    ),
    "radial-prep-shock-calculator": _shock(
        hp="700", spec="radial prep, 700 HP drag radial, double-adjustable QA1",
    ),
    "no-prep-shock-calculator": _shock(
        surface="noprep", hp="700", weight="3300",
        spec="no prep, 700 HP drag radial, double-adjustable QA1",
    ),
    "street-car-shock-calculator": _shock(
        use="street", surface="noprep", tire="street", style="single", hp="400", weight="3600", hit="na", rear="stock",
        spec="street car, street tire, single-adjustable QA1",
    ),
    "street-strip-shock-calculator": _shock(
        hp="600", weight="3500", rear="coilover",
        spec="street-strip coilover, radial prep, double-adjustable QA1",
    ),
    "single-adjustable-drag-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", style="single", brand="strange", hp="800", weight="3200",
        spec="prepped slick, single-adjustable Strange",
    ),
    "double-adjustable-drag-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", brand="viking", hp="1000", weight="3100", hit="brake",
        spec="prepped slick, on the brake, double-adjustable Viking",
    ),
    "qa1-drag-shock-calculator": _shock(spec="radial prep, double-adjustable QA1, 0 to 18"),
    "strange-drag-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", brand="strange", hp="900", weight="3200",
        spec="prepped slick, double-adjustable Strange, 0 to 16",
    ),
    "viking-drag-shock-calculator": _shock(
        surface="noprep", brand="viking", hp="750", weight="3300",
        spec="no prep, double-adjustable Viking, 0 to 24",
    ),
    "afco-drag-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", brand="afco", hp="850", weight="3150",
        spec="prepped slick, double-adjustable Afco, 0 to 12",
    ),
    "four-link-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", hp="900", weight="3000",
        spec="4-link, prepped slick, double-adjustable QA1",
    ),
    "ladder-bar-shock-calculator": _shock(
        use="drag", surface="prepped", tire="slick", hp="800", weight="2800", rear="ladder",
        spec="ladder bar, prepped slick, double-adjustable QA1",
    ),
    "torque-arm-shock-calculator": _shock(
        hp="700", weight="3600", rear="torquearm",
        spec="torque arm, radial prep, double-adjustable QA1",
    ),
    "wheelstand-shock-adjustment": _shock(
        use="drag", surface="prepped", tire="slick", hp="1100", weight="3000", hit="brake", symptom="wheelie",
        spec="wheelstand correction, prepped slick, on the brake",
    ),
    "spin-on-hit-shock-adjustment": _shock(
        surface="noprep", hp="800", weight="3300", hit="brake", symptom="spin",
        spec="spin-on-the-hit correction, no prep, on the brake",
    ),
    "shift-unload-shock-adjustment": _shock(
        use="drag", surface="prepped", hp="900", weight="3200", symptom="unload",
        spec="shift-unload correction, prepped drag radial",
    ),
}


def shock_preset(slug):
    return SHOCK_PRESETS.get(slug, SHOCK_PRESETS["drag-shock-calculator"])


def shock_html(row):
    preset = shock_preset(row["slug"])
    primary = SHOCK_DIAGRAM + f"""
    <div class="grid-2">
        <div class="field"><label for="sk-fr">Front, ride height (in)</label><input type="number" id="sk-fr" value="14.0" min="4" max="30" step="0.05"></div>
        <div class="field"><label for="sk-fb">Front, full bump (in)</label><input type="number" id="sk-fb" value="12.5" min="4" max="30" step="0.05"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sk-fd">Front, full droop (in)</label><input type="number" id="sk-fd" value="17.0" min="4" max="36" step="0.05"></div>
        <div class="field"><label for="sk-measure">How it was measured</label>
            <select id="sk-measure">
                <option value="eye" selected>Eye center to eye center</option>
                <option value="pad">Pad face to pad face</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sk-rr">Rear, ride height (in)</label><input type="number" id="sk-rr" value="14.5" min="4" max="30" step="0.05"></div>
        <div class="field"><label for="sk-rb">Rear, full bump (in)</label><input type="number" id="sk-rb" value="12.0" min="4" max="30" step="0.05"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sk-rd">Rear, full droop (in)</label><input type="number" id="sk-rd" value="16.0" min="4" max="36" step="0.05"></div>
        <div class="field"><label for="sk-use">Car</label><select id="sk-use">{options(SHOCK_USES, preset["use"])}</select></div>
    </div>
    <p class="field-hint">Full bump is the short center-to-center length. Full droop is the long one. Ride height is the car at race weight. Pad face to pad face takes 5/8 in off each end before the shock is chosen.</p>
    <div class="grid-2">
        <div class="field"><label for="sk-surface">Surface</label><select id="sk-surface">{options(SHOCK_SURFACES, preset["surface"])}</select></div>
        <div class="field"><label for="sk-tire">Tire</label><select id="sk-tire">{options(SHOCK_TIRES, preset["tire"])}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sk-style">Shock</label><select id="sk-style">{options(SHOCK_STYLES, preset["style"])}</select></div>
    </div>
    <div class="field"><label for="sk-brand">Adjuster scale</label><select id="sk-brand">{options(SHOCK_BRANDS, preset["brand"])}</select></div>
    <p class="field-hint">Prepped can take a fast hit. Radial prep is the middle. No prep spins if the hit is sharp. A single adjustable moves rebound only. A double adjustable adds a compression knob, which is the rear hit and the front return.</p>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="sk-hp">Power</label><input type="number" id="sk-hp" value="{esc(preset["hp"])}" min="100" max="4000" step="25"></div>
        <div class="field"><label for="sk-weight">Race weight (lb)</label><input type="number" id="sk-weight" value="{esc(preset["weight"])}" min="1400" max="7000" step="50"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="sk-hit">How it hits</label><select id="sk-hit">{options(SHOCK_HITS, preset["hit"])}</select></div>
        <div class="field"><label for="sk-rear">Rear suspension</label><select id="sk-rear">{options(SHOCK_REARS, preset["rear"])}</select></div>
    </div>
    <div class="field"><label for="sk-symptom">What it is doing</label><select id="sk-symptom">{options(SHOCK_SYMPTOMS, preset["symptom"])}</select></div>
    <p class="field-hint">Count clicks from the soft stop toward firm. Set both fronts the same and both rears the same. Change two clicks on one end, make one pass, and write down the 60-foot.</p>
    {LOSS_FIELDS}
    """
    results = """
    <p class="assess" id="sk-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>End</th><th>Order</th><th>Lengths</th><th>Status</th></tr></thead>
            <tbody id="sk-order"></tbody>
        </table>
        <p class="field-hint">Collapsed is the longest shock body that still has 1/2 in before the bump measurement. Extended is the shortest open length that still has 1/2 in past full droop. Drag wants more of that stroke in front extension and in rear compression at ride height.</p>
    </div>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Knob</th><th>Start</th><th>What it does</th><th>Status</th></tr></thead>
            <tbody id="sk-matrix"></tbody>
        </table>
    </div>
    <div class="table-scroll">
        <table>
            <thead><tr><th>If the next pass</th><th>Front extension</th><th>Front compression</th><th>Rear compression</th><th>Rear extension</th></tr></thead>
            <tbody id="sk-moves"></tbody>
        </table>
        <p class="field-hint">The pass table is the next change from the clicks above, not a second setup. Turn one row. A cell that says Valve is built into a single-adjustable shock and does not have its own knob. Leave extension travel in the front shaft at ride height, and compression travel in the rear. A shock that is already at the end of its stroke will not do what the click says.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print shock sheet", power_toggle=True, results_extra=results)


SHOCK_SCRIPT = r"""
const SK_BRAND = {
    qa1: { name: "QA1", max: 18 },
    strange: { name: "Strange", max: 16 },
    viking: { name: "Viking", max: 24 },
    afco: { name: "Afco", max: 12 },
    generic: { name: "Generic", max: 18 }
};
const SK_BITE = { prepped: 1, radial: 0.72, noprep: 0.38 };
const SK_TIRE = { slick: 1, radial: 0.74, street: 0.42 };
const SK_PLANT = { drag: 1, strip: 0.72, street: 0.35 };
const SK_SEP = { fourlink: 1, ladder: 0.88, torquearm: 0.55, coilover: 0.48, stock: 0.4 };
const SK_HIT = { na: 0.85, power: 1, brake: 1.22 };
const SK_SHIFT = {
    baseline: [0, 0, 0, 0],
    spin: [12, 0, 12, 0],
    dead: [-12, 0, -12, 0],
    wheelie: [14, -12, 6, 0],
    unload: [0, -10, 0, -14],
    shake: [6, 0, 14, 0]
};

function skClamp(value, lo, hi) {
    return Math.min(hi, Math.max(lo, value));
}

function skNum(id, fallback) {
    const el = document.getElementById(id);
    const value = el ? parseFloat(el.value) : NaN;
    return Number.isFinite(value) ? value : fallback;
}

function skClicks(percent, max) {
    return Math.round(skClamp(percent, 0, 100) / 100 * max);
}

function skPlan() {
    const use = document.getElementById("sk-use").value || "strip";
    const surface = document.getElementById("sk-surface").value || "radial";
    const tire = document.getElementById("sk-tire").value || "radial";
    const style = document.getElementById("sk-style").value || "double";
    const brandKey = document.getElementById("sk-brand").value || "qa1";
    const brand = SK_BRAND[brandKey] || SK_BRAND.qa1;
    const hit = document.getElementById("sk-hit").value || "power";
    const rear = document.getElementById("sk-rear").value || "fourlink";
    const symptom = document.getElementById("sk-symptom").value || "baseline";
    const hp = Math.max(100, crankHorsepower(skNum("sk-hp", 650)));
    const weight = skClamp(skNum("sk-weight", 3400), 1400, 7000);
    const ptw = hp / weight * 1000;
    const bite = (SK_BITE[surface] || 0.7) * (SK_TIRE[tire] || 0.7);
    const plant = SK_PLANT[use] || 0.7;
    const demand = skClamp(ptw / 200, 0.35, 1.85) * (SK_HIT[hit] || 1);
    let smooth = skClamp((demand - bite * 1.15) / 1.1, 0, 1);
    if (use === "street") smooth = Math.max(smooth, 0.72);
    else if (use === "strip") smooth = Math.max(smooth, 0.28);
    let frontExt = 26 + smooth * 48 - Math.max(0, bite - 0.55) * 18;
    let frontComp = 18 + plant * 22 + bite * 10 - (use === "street" ? 12 : 0);
    let rearComp = 18 + smooth * 46 - bite * 8 + (rear === "torquearm" ? 8 : 0);
    let rearExt = 16 + (1 - bite) * 28 + (1 - (SK_SEP[rear] || 0.5)) * 14 - plant * 6;
    const shift = SK_SHIFT[symptom] || SK_SHIFT.baseline;
    frontExt += shift[0];
    frontComp += shift[1];
    rearComp += shift[2];
    rearExt += shift[3];
    return {
        use: use,
        surface: surface,
        tire: tire,
        style: style,
        brandKey: brandKey,
        brand: brand,
        hit: hit,
        rear: rear,
        symptom: symptom,
        hp: hp,
        weight: weight,
        ptw: ptw,
        bite: bite,
        smooth: smooth,
        double: style === "double",
        frontExt: skClamp(frontExt, 6, 90),
        frontComp: skClamp(frontComp, 6, 80),
        rearComp: skClamp(rearComp, 6, 88),
        rearExt: skClamp(rearExt, 6, 80)
    };
}

function skStart(percent, brand, enabled) {
    const pct = Math.round(percent) + "% from full soft";
    if (!enabled) return "In the valve · " + pct;
    return skClicks(percent, brand.max) + " of " + brand.max + " · " + pct;
}

function skNext(percent, delta, brand, enabled) {
    if (!enabled) return "Valve";
    const base = skClicks(percent, brand.max);
    if (!delta) return "leave";
    const next = skClamp(base + delta, 0, brand.max);
    if (next === base) return base + " (at the stop)";
    return String(next);
}

function skRow(name, detail, result, status) {
    const tr = document.createElement("tr");
    if (status === "No") tr.className = "is-small";
    const badge = status === "Good" ? "badge-ok" : (status === "Watch" ? "badge-tight" : "badge-no");
    [name, detail, result].forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
    });
    const statusCell = document.createElement("td");
    const pill = document.createElement("span");
    pill.className = "badge " + badge;
    pill.textContent = status;
    statusCell.appendChild(pill);
    tr.appendChild(statusCell);
    return tr;
}

function skMoveRow(cells) {
    const tr = document.createElement("tr");
    cells.forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
    });
    return tr;
}

function skInches(value) {
    if (unitState.system === "metric") return (value * 25.4).toFixed(1) + " mm";
    return value.toFixed(2) + " in";
}

function skMeasured(id, fallback) {
    let value = skNum(id, fallback);
    const how = document.getElementById("sk-measure");
    if (how && how.value === "pad") value -= 1.25;
    return value;
}

function skFit(ride, bump, droop) {
    if (!(droop > ride + 0.2 && ride > bump + 0.2)) {
        return {
            ok: false,
            status: "No",
            lengths: "Measure again",
            detail: "Bump, ride, and droop are out of order. Bump is the short length and droop is the long length."
        };
    }
    const collapsed = bump - 0.5;
    const extended = droop + 0.5;
    return {
        ok: true,
        status: "Good",
        collapsed: collapsed,
        extended: extended,
        stroke: extended - collapsed,
        compression: ride - collapsed,
        extension: extended - ride,
        lengths: skInches(collapsed) + " collapsed, " + skInches(extended) + " extended",
        detail: ""
    };
}

function calcShock() {
    const plan = skPlan();
    const brand = plan.brand;
    const step = Math.max(1, Math.round(brand.max / 9));
    const frontValve = (plan.use === "street" || plan.tire === "street") ? "50/50" : (plan.surface === "noprep" ? "80/20" : "90/10");
    const rearWantsDouble = plan.tire !== "street" && plan.use !== "street" && (plan.rearComp >= 40 || plan.ptw >= 160 || plan.smooth >= 0.55);
    const frontCompOn = plan.double;
    const rearCompOn = plan.double;
    const travel = plan.use === "drag" ? 2 : (plan.use === "strip" ? 1.5 : 1);
    const rearTravel = plan.use === "street" ? 1 : 1.5;
    const fe = skClicks(plan.frontExt, brand.max);
    const fc = skClicks(plan.frontComp, brand.max);
    const rc = skClicks(plan.rearComp, brand.max);
    const re = skClicks(plan.rearExt, brand.max);
    const feLabel = fe + " of " + brand.max;
    const fcLabel = frontCompOn ? fc + " of " + brand.max : frontValve + " valve";
    const rcLabel = rearCompOn ? rc + " of " + brand.max : "50/50 valve";
    const reLabel = re + " of " + brand.max;
    let frontCompStatus = "Good";
    let frontCompResult = "Holds the nose up. Less of it lets a wheelstand come back down.";
    if (!frontCompOn && plan.symptom === "wheelie") {
        frontCompStatus = "Watch";
        frontCompResult = "A single front is already light on compression. Slow the rise with extension. If it still stands up, the shaft is out of travel or the power is ahead of the shock.";
    } else if (!frontCompOn) {
        frontCompResult = "Built into the " + frontValve + " valve. The knob on this shock is extension.";
    }
    let rearCompStatus = "Good";
    let rearCompResult = "Softens the hit. More of it keeps the tire from getting shocked.";
    if (!rearCompOn && rearWantsDouble) {
        rearCompStatus = "Watch";
        rearCompResult = "This hit wants a compression knob. A single rear only moves rebound, so it cannot soften the hit.";
    } else if (!rearCompOn) {
        rearCompResult = "The 50/50 valve is the compression. The knob only changes how the rear recovers.";
    }
    let frontPartStatus = "Good";
    let frontPart = frontValve + " front. Use a double if you need the nose to come down on its own knob.";
    if (plan.use === "street") {
        frontPart = "50/50 street front. A drag 90/10 will float on the street.";
    } else if (plan.double) {
        frontPart = "Double adjustable front, or a " + frontValve + " single if extension is the only knob you need.";
    }
    if (!plan.double && plan.symptom === "wheelie") frontPartStatus = "Watch";
    let rearPartStatus = "Good";
    let rearPart = "Double adjustable rear. Compression is the hit. Extension is the recovery and the gear change.";
    if (!plan.double && rearWantsDouble) {
        rearPartStatus = "Watch";
        rearPart = "Plan on a double adjustable rear. Leave the single at the rebound click until that shock is on the car.";
    } else if (!plan.double) {
        rearPart = "50/50 single is enough here. The knob is rebound, not the hit.";
    }
    const directionStatus = plan.brandKey === "afco" ? "Watch" : "Good";
    const directionResult = plan.brandKey === "afco"
        ? "This scale counts 0 soft to " + brand.max + " firm. If the arrow on the Afco body points the other way, count back from the firm stop."
        : "0 is full soft and " + brand.max + " is full firm on this " + brand.name + " scale. Higher slows that circuit.";
    const rearNote = {
        fourlink: "Rear extension stays loose so the 4-link can separate.",
        ladder: "A ladder bar hits quickly, so the rear starts a little tighter than a 4-link.",
        torquearm: "A torque arm hits harder than a 4-link, so rear compression starts firmer.",
        coilover: "A coilover shaft moves less than the wheel, so leave extra travel in the shock.",
        stock: "Stock arms and leaf springs do not separate like a 4-link, so rear rebound starts closer to the middle."
    }[plan.rear] || "";
    let surfaceNote = "The surface can take a hit.";
    if (plan.use === "street") {
        surfaceNote = "A street tire wants the 50/50 valve and a controlled nose, not a drag 90/10.";
    } else if (plan.surface === "noprep") {
        surfaceNote = "The power is ahead of this surface. Firmer front extension and rear compression make the spin smoother. They do not add grip the track does not have.";
    } else if (plan.smooth >= 0.35) {
        surfaceNote = "The hit is slowed so the tire is planted instead of shocked.";
    }
    const symptomNote = {
        baseline: "",
        spin: " The starting clicks are already firmer on front extension and rear compression for a car that spins on the hit.",
        dead: " The starting clicks are already softer on front extension and rear compression for a car that will not transfer.",
        wheelie: " The starting clicks already slow the rise and let the nose come back down.",
        unload: " The starting clicks already let the nose down and loosen rear extension for a car that unloads on the shift.",
        shake: " The starting clicks already add rear compression for a tire that shakes."
    }[plan.symptom] || "";
    publishReadout([
        { label: "Front extension", value: feLabel, unit: "text", primary: true },
        { label: "Front compression", value: fcLabel, unit: "text" },
        { label: "Rear compression", value: rcLabel, unit: "text" },
        { label: "Rear extension", value: reLabel, unit: "text" },
        { label: "Front valve", value: frontValve, unit: "text" },
        { label: "Front travel left", value: travel, unit: "in" },
        { label: "Power to weight", value: Math.round(plan.ptw) + " HP / 1,000 lb", unit: "text" }
    ]);
    const assess = document.getElementById("sk-assess");
    if (assess) {
        const rearGap = (!plan.double && rearWantsDouble)
            ? " The rear hit wants a compression knob, and a single adjustable does not have one."
            : "";
        assess.textContent = "Start the " + brand.name + " fronts at " + feLabel + " extension and " + fcLabel + " compression. Start the rears at " + rcLabel + " compression and " + reLabel + " extension. Higher is firmer. Front extension slows the rise. Rear compression softens the hit. " + surfaceNote + " " + rearNote + symptomNote + rearGap + " Leave about " + travel.toFixed(1) + " in of front extension and " + rearTravel.toFixed(1) + " in of rear compression in the shafts at ride height.";
    }
    const body = document.getElementById("sk-matrix");
    if (body) {
        body.replaceChildren(
            skRow("Front extension", skStart(plan.frontExt, brand, true), "Slows the rise. More is a softer hit. Less plants the tire harder.", "Good"),
            skRow("Front compression", skStart(plan.frontComp, brand, frontCompOn), frontCompResult, frontCompStatus),
            skRow("Rear compression", skStart(plan.rearComp, brand, rearCompOn), rearCompResult, rearCompStatus),
            skRow("Rear extension", skStart(plan.rearExt, brand, true), "Loose lets the housing separate. Tight keeps the tire loaded when the surface goes away.", "Good"),
            skRow("Front shock", frontValve, frontPart, frontPartStatus),
            skRow("Rear shock", plan.double ? "Double" : "Single", rearPart, rearPartStatus),
            skRow("Scale", brand.name, directionResult, directionStatus)
        );
    }
    const moves = document.getElementById("sk-moves");
    if (moves) {
        const rows = [
            ["Spins on the hit", step, 0, step, 0],
            ["No bite, nose barely rises", -step, 0, -step, 0],
            ["Wheelstands", step, -step, 0, 0],
            ["Unloads on the shift", 0, -step, 0, -step],
            ["Shakes the tire", 0, 0, step, 0],
            ["Greasy or cold track", step, 0, step, 0]
        ];
        moves.replaceChildren(...rows.map(row => skMoveRow([
            row[0],
            skNext(plan.frontExt, row[1], brand, true),
            skNext(plan.frontComp, row[2], brand, frontCompOn),
            skNext(plan.rearComp, row[3], brand, rearCompOn),
            skNext(plan.rearExt, row[4], brand, true)
        ])));
    }
    const frontFit = skFit(skMeasured("sk-fr", 14), skMeasured("sk-fb", 12.5), skMeasured("sk-fd", 17));
    const rearFit = skFit(skMeasured("sk-rr", 14.5), skMeasured("sk-rb", 12), skMeasured("sk-rd", 16));
    const frontBuy = (plan.double || plan.symptom === "wheelie") ? "Double adjustable" : ("Single, " + frontValve + " valve");
    const rearBuy = (plan.double || rearWantsDouble) ? "Double adjustable" : "Single, 50/50 valve";
    function skLengthNote(fit, end) {
        if (!fit.ok) return fit;
        const drag = plan.use !== "street";
        let status = "Good";
        let detail = "At ride, " + skInches(fit.compression) + " of compression and " + skInches(fit.extension) + " of extension are left. Stroke is " + skInches(fit.stroke) + ".";
        if (end === "front" && drag && fit.extension + 0.05 < fit.compression) {
            status = "Watch";
            detail += " The front has more compression than extension. Drag wants the extra travel in extension so the nose can rise.";
        }
        if (end === "rear" && drag && fit.compression + 0.05 < fit.extension) {
            status = "Watch";
            detail += " The rear has more extension than compression. The hit needs the compression travel.";
        }
        if (fit.compression < 0.75 || fit.extension < 0.75) {
            status = "Watch";
            detail += " One end of the shaft is inside 3/4 in at ride height.";
        }
        return { ok: true, status: status, lengths: fit.lengths, detail: detail };
    }
    const frontOrder = skLengthNote(frontFit, "front");
    const rearOrder = skLengthNote(rearFit, "rear");
    if (!plan.double && rearWantsDouble && rearOrder.ok && rearOrder.status === "Good") rearOrder.status = "Watch";
    if (assess && frontOrder.ok && rearOrder.ok) {
        assess.textContent += " Order the front " + frontBuy.toLowerCase() + ", collapsed at or under " + skInches(frontFit.collapsed) + " and extended at or over " + skInches(frontFit.extended) + ". Order the rear " + rearBuy.toLowerCase() + ", collapsed at or under " + skInches(rearFit.collapsed) + " and extended at or over " + skInches(rearFit.extended) + ".";
    }
    const order = document.getElementById("sk-order");
    if (order) {
        const frontDetail = frontOrder.detail + (frontBuy.indexOf("Single") === 0 && plan.symptom === "wheelie" ? " A wheelstand is easier to bring down with a compression knob." : "");
        const rearDetail = rearOrder.detail + (!plan.double && rearWantsDouble ? " This hit wants a compression knob, so order a double even if the clicks above are for a single." : "");
        order.replaceChildren(
            skRow("Front", frontBuy, frontOrder.ok ? frontOrder.lengths + ". " + frontDetail : frontOrder.detail, frontOrder.status),
            skRow("Rear", rearBuy, rearOrder.ok ? rearOrder.lengths + ". " + rearDetail : rearOrder.detail, rearOrder.status)
        );
    }
}
bindCalc(calcShock, ["sk-use", "sk-surface", "sk-tire", "sk-style", "sk-brand", "sk-hp", "sk-weight", "sk-hit", "sk-rear", "sk-symptom", "sk-fr", "sk-fb", "sk-fd", "sk-rr", "sk-rb", "sk-rd", "sk-measure", "dt-loss"]);
"""

CV_TRANSMISSIONS = (
    ("powerglide", "Powerglide (1.76 / 1.00)"),
    ("th350", "TH350 (2.52 / 1.52 / 1.00)"),
    ("th400", "TH400 (2.48 / 1.48 / 1.00)"),
    ("4l60e", "4L60E / 4L70E (3.06, lockup 0.70)"),
    ("4l80e", "4L80E (2.48, lockup 0.75)"),
    ("6l80", "6L80 (4.03, lockup 0.67)"),
    ("8l90", "8L90 (4.56, lockup 0.65)"),
    ("10r80", "10R80 (4.70, lockup 0.64)"),
    ("c4", "C4 (2.46 / 1.46 / 1.00)"),
    ("c6", "C6 (2.46 / 1.46 / 1.00)"),
    ("727", "Torqueflite 727 (2.45 / 1.45 / 1.00)"),
    ("904", "Torqueflite 904 (2.74 / 1.54 / 1.00)"),
    ("zf8hp", "8HP70 / 8HP90 (4.71, lockup 0.67)"),
)
CV_USES = (("street", "Street"), ("strip", "Street-strip"), ("drag", "Drag"))
CV_TRACKS = (("street", "Street tire"), ("radial", "Radial prep"), ("prepped", "Prepped slick"), ("noprep", "No prep"))
CV_HOLDS = (("foot", "Foot brake"), ("transbrake", "Trans brake"))


def _cv(**overrides):
    preset = {
        "use": "drag",
        "track": "prepped",
        "trans": "th400",
        "hold": "transbrake",
        "tq": "500",
        "tqrpm": "4800",
        "hp": "750",
        "hprpm": "6800",
        "rear": "3.73",
        "tire": "28.0",
        "shift": "7000",
        "mph": "70",
        "spec": "TH400, 500 lb-ft at 4,800 RPM, prepped slick, trans brake",
    }
    preset.update(overrides)
    return preset


CV_PRESETS = {
    "torque-converter-calculator": _cv(),
    "street-lockup-converter-calculator": _cv(
        use="street", track="street", trans="4l80e", hold="foot",
        tq="400", tqrpm="3600", hp="420", hprpm="5400", rear="3.55", tire="28.0", shift="5600",
        spec="4L80E lockup, 400 lb-ft at 3,600 RPM, street",
    ),
    "powerglide-converter-calculator": _cv(
        trans="powerglide", tq="620", tqrpm="5600", hp="900", hprpm="7400", rear="4.10", tire="28.0", shift="7600",
        spec="Powerglide, 620 lb-ft at 5,600 RPM, prepped slick, trans brake",
    ),
    "th400-converter-calculator": _cv(
        spec="TH400, 500 lb-ft at 4,800 RPM, prepped slick, trans brake",
    ),
    "no-prep-converter-calculator": _cv(
        track="noprep", hold="foot", tq="700", tqrpm="5200", hp="1100", hprpm="7000", rear="3.50", tire="29.0", shift="7200",
        spec="no prep, 700 lb-ft at 5,200 RPM, foot brake",
    ),
    "radial-converter-calculator": _cv(
        use="strip", track="radial", hold="foot", tq="550", tqrpm="4600", hp="800", hprpm="6400", rear="3.73", tire="28.0", shift="6800",
        spec="radial prep, 550 lb-ft at 4,600 RPM, foot brake",
    ),
    "trans-brake-converter-calculator": _cv(
        tq="640", tqrpm="6000", hp="1000", hprpm="7600", rear="4.10", tire="28.0", shift="7800",
        spec="trans brake, 640 lb-ft at 6,000 RPM, prepped slick",
    ),
    "footbrake-converter-calculator": _cv(
        hold="foot", tq="450", tqrpm="6400", hp="900", hprpm="7800", rear="4.10", tire="28.0", shift="8000",
        spec="foot brake, 450 lb-ft at 6,400 RPM, small-core stall",
    ),
    "street-strip-converter-calculator": _cv(
        use="strip", track="radial", trans="4l60e", hold="foot",
        tq="450", tqrpm="4200", hp="550", hprpm="6000", rear="3.73", tire="28.0", shift="6200",
        spec="4L60E lockup, street-strip, 450 lb-ft at 4,200 RPM",
    ),
}


def cv_preset(slug):
    return CV_PRESETS.get(slug, CV_PRESETS["torque-converter-calculator"])


def converter_html(row):
    preset = cv_preset(row["slug"])
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="cv-use">Car</label><select id="cv-use">{options(CV_USES, preset["use"])}</select></div>
        <div class="field"><label for="cv-track">Surface</label><select id="cv-track">{options(CV_TRACKS, preset["track"])}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cv-trans">Transmission</label><select id="cv-trans">{options(CV_TRANSMISSIONS, preset["trans"])}</select></div>
        <div class="field"><label for="cv-hold">How it is held</label><select id="cv-hold">{options(CV_HOLDS, preset["hold"])}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cv-tq">Peak torque (lb-ft)</label><input type="number" id="cv-tq" value="{esc(preset["tq"])}" min="100" max="2500" step="10"></div>
        <div class="field"><label for="cv-tqrpm">Torque peak (RPM)</label><input type="number" id="cv-tqrpm" value="{esc(preset["tqrpm"])}" min="1500" max="9000" step="50"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cv-hp">Peak power</label><input type="number" id="cv-hp" value="{esc(preset["hp"])}" min="100" max="4000" step="10"></div>
        <div class="field"><label for="cv-hprpm">Power peak (RPM)</label><input type="number" id="cv-hprpm" value="{esc(preset["hprpm"])}" min="2000" max="10000" step="50"></div>
    </div>
    <p class="field-hint">Brake stall is the RPM with the turbine held. It follows the torque at that RPM and the converter's K-factor. Weight does not change it. The tire and the gear decide whether that stall hooks.</p>
    """
    advanced = f"""
    <div class="grid-2">
        <div class="field"><label for="cv-rear">Rear gear</label><input type="number" id="cv-rear" value="{esc(preset["rear"])}" min="2" max="6.5" step="0.01"></div>
        <div class="field"><label for="cv-tire">Tire diameter (in)</label><input type="number" id="cv-tire" value="{esc(preset["tire"])}" min="18" max="40" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cv-shift">Shift RPM</label><input type="number" id="cv-shift" value="{esc(preset["shift"])}" min="2000" max="11000" step="50"></div>
        <div class="field"><label for="cv-mph">Cruise (MPH)</label><input type="number" id="cv-mph" value="{esc(preset["mph"])}" min="30" max="100" step="1"></div>
    </div>
    {LOSS_FIELDS}
    """
    results = """
    <p class="assess" id="cv-assess"></p>
    <div class="table-scroll">
        <table>
            <thead><tr><th>Check</th><th>Number</th><th>What to order</th><th>Status</th></tr></thead>
            <tbody id="cv-matrix"></tbody>
        </table>
        <p class="field-hint">K-factor is brake stall divided by the square root of the torque at that RPM. Give the shop the stall, the torque, the K, and the stall torque ratio. The core diameter is the usual can for that stall. The stator and the vane angle are what set it.</p>
    </div>
    """
    return calculator_shell(primary, advanced, "Print converter sheet", power_toggle=True, results_extra=results)


CONVERTER_SCRIPT = r"""
const CV_TRANS = {
    powerglide: { name: "Powerglide", first: 1.76, top: 1.00, lock: false },
    th350: { name: "TH350", first: 2.52, top: 1.00, lock: false },
    th400: { name: "TH400", first: 2.48, top: 1.00, lock: false },
    "4l60e": { name: "4L60E", first: 3.06, top: 0.70, lock: true },
    "4l80e": { name: "4L80E", first: 2.48, top: 0.75, lock: true },
    "6l80": { name: "6L80", first: 4.027, top: 0.667, lock: true },
    "8l90": { name: "8L90", first: 4.56, top: 0.65, lock: true },
    "10r80": { name: "10R80", first: 4.696, top: 0.636, lock: true },
    c4: { name: "C4", first: 2.46, top: 1.00, lock: false },
    c6: { name: "C6", first: 2.46, top: 1.00, lock: false },
    "727": { name: "727", first: 2.45, top: 1.00, lock: false },
    "904": { name: "904", first: 2.74, top: 1.00, lock: false },
    zf8hp: { name: "8HP", first: 4.714, top: 0.667, lock: true }
};

function cvNum(id, fallback) {
    const el = document.getElementById(id);
    const value = el ? parseFloat(el.value) : NaN;
    return Number.isFinite(value) ? value : fallback;
}

function cvCore(stall) {
    if (stall < 2600) return "12 in";
    if (stall < 3400) return "11 in";
    if (stall < 4300) return "10 in";
    if (stall < 5000) return "9.5 in";
    if (stall < 5600) return "9 in";
    return "8 in";
}

function cvRow(name, detail, result, status) {
    const tr = document.createElement("tr");
    if (status === "No") tr.className = "is-small";
    const badge = status === "Good" ? "badge-ok" : (status === "Watch" ? "badge-tight" : "badge-no");
    [name, detail, result].forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
    });
    const statusCell = document.createElement("td");
    const pill = document.createElement("span");
    pill.className = "badge " + badge;
    pill.textContent = status;
    statusCell.appendChild(pill);
    tr.appendChild(statusCell);
    return tr;
}

function cvTorqueAt(stall, tq, tqRpm, hpTorque, hpRpm) {
    if (stall >= hpRpm) return hpTorque;
    if (stall >= tqRpm) {
        const span = Math.max(1, hpRpm - tqRpm);
        return tq + (hpTorque - tq) * ((stall - tqRpm) / span);
    }
    return tq * Math.pow(Math.max(0.35, stall / tqRpm), 0.4);
}

function calcConverter() {
    const use = document.getElementById("cv-use").value || "drag";
    const track = document.getElementById("cv-track").value || "prepped";
    const trans = CV_TRANS[document.getElementById("cv-trans").value] || CV_TRANS.th400;
    const hold = document.getElementById("cv-hold").value || "transbrake";
    const hpTyped = cvNum("cv-hp", 750);
    const hp = Math.max(50, crankHorsepower(hpTyped));
    const scale = hp / Math.max(50, hpTyped);
    const tq = Math.max(80, cvNum("cv-tq", 500) * scale);
    let tqRpm = Math.max(1500, cvNum("cv-tqrpm", 4800));
    let hpRpm = Math.max(2000, cvNum("cv-hprpm", 6800));
    if (hpRpm <= tqRpm + 100) hpRpm = tqRpm + 800;
    const rear = Math.max(2, cvNum("cv-rear", 3.73));
    const tire = Math.max(18, cvNum("cv-tire", 28));
    const shift = Math.max(2000, cvNum("cv-shift", 7000));
    const mph = Math.max(30, cvNum("cv-mph", 70));
    const hpTorque = hp * 5252 / hpRpm;
    let offset = 600;
    if (use === "street") offset = 400;
    else if (use === "strip") offset = 450;
    if (track === "noprep") offset = Math.max(offset, 900);
    let stall = Math.max(1400, tqRpm - offset);
    const cruise = (mph * trans.top * rear * 336) / tire;
    let cruiseStatus = "Good";
    let cruiseDetail = "Cruise in top gear is " + Math.round(cruise).toLocaleString("en-US") + " RPM. The stall sits under it.";
    if (use === "drag" && stall > cruise - 200) {
        cruiseStatus = "Watch";
        cruiseDetail = "At " + Math.round(mph) + " MPH in high gear the engine is at " + Math.round(cruise).toLocaleString("en-US") + " RPM. This stall is for the track, and it will slip if the car is driven there unlocked.";
    } else if (!trans.lock && stall > cruise - 500) {
        stall = Math.max(1400, cruise - 500);
        cruiseStatus = "Watch";
        cruiseDetail = "Unlocked cruise is " + Math.round(cruise).toLocaleString("en-US") + " RPM, so the stall is held about 500 RPM under it. A later cam needs a lockup gear or a shorter top gear.";
    } else if (trans.lock && stall > cruise - 200) {
        cruiseStatus = "Watch";
        cruiseDetail = "Cruise is " + Math.round(cruise).toLocaleString("en-US") + " RPM. Lock the converter there. Unlocked, this stall slips on the highway.";
    }
    const torque = Math.max(40, cvTorqueAt(stall, tq, tqRpm, hpTorque, hpRpm));
    const kFactor = stall / Math.sqrt(torque);
    let str = 2.15;
    if (use === "street" || track === "street") str = 1.9;
    else if (track === "noprep") str = 1.85;
    else if (use === "drag" && track === "prepped") str = 2.35;
    else if (use === "strip") str = 2.05;
    const core = cvCore(stall);
    const coreIn = parseFloat(core);
    let holdStatus = "Good";
    let holdDetail = hold === "transbrake"
        ? "A trans brake holds the turbine, so the engine can reach this brake stall."
        : "The foot brake has to hold the torque this converter multiplies. If the car pushes through it, the stall you see is short of this number.";
    if (hold === "foot" && coreIn <= 9 && str >= 2.2) {
        holdStatus = "Watch";
        holdDetail = "A small core with a high stall torque ratio can push through the foot brake before the engine reaches this stall. A trans brake holds the turbine so it can.";
    }
    let shiftStatus = "Good";
    let shiftDetail = "The shift is " + (shift / stall).toFixed(2) + " times the stall, so the converter is coupling before the gear change.";
    if (shift < stall) {
        shiftStatus = "No";
        shiftDetail = "The shift is under the stall, so the converter is still at stall when the gear changes.";
    } else if (shift < stall * 1.15) {
        shiftStatus = "Watch";
        shiftDetail = "The shift is barely above the stall. Raise the shift or tighten the converter so it couples first.";
    }
    let slip = 6;
    if (use === "street") slip = 5;
    if (use === "drag" && track === "prepped") slip = 7;
    if (shift < stall * 1.15) slip = 9;
    const axle = torque * str * trans.first * rear;
    const underPeak = tqRpm - stall;
    publishReadout([
        { label: "Brake stall", value: Math.round(stall), unit: "rpm", primary: true },
        { label: "K-factor", value: kFactor.toFixed(0), unit: "text" },
        { label: "Stall torque ratio", value: str.toFixed(2), unit: "text" },
        { label: "Core", value: core, unit: "text" },
        { label: "Torque at stall", value: Math.round(torque) + " lb-ft", unit: "text" },
        { label: "Axle torque at stall", value: Math.round(axle).toLocaleString("en-US") + " lb-ft", unit: "text" }
    ]);
    const assess = document.getElementById("cv-assess");
    if (assess) {
        const lockNote = trans.lock ? " This transmission can lock the converter in top gear." : " This transmission does not lock the converter.";
        assess.textContent = "Order a " + trans.name + " converter with a brake stall of " + Math.round(stall).toLocaleString("en-US") + " RPM at " + Math.round(torque) + " lb-ft. That is a K-factor of " + kFactor.toFixed(0) + " and a stall torque ratio near " + str.toFixed(2) + ". The stall is " + Math.round(underPeak).toLocaleString("en-US") + " RPM under the torque peak so the engine can accelerate through it. The usual core is " + core + ". The stator and the vane angle set the stall." + lockNote + " At the shift, type about " + slip + "% slip into the gear calculator. A locked gear is 0%.";
    }
    const body = document.getElementById("cv-matrix");
    if (body) {
        body.replaceChildren(
            cvRow("Brake stall", Math.round(stall).toLocaleString("en-US") + " RPM", Math.round(tqRpm - stall).toLocaleString("en-US") + " RPM under the torque peak. An unlocked street converter is also held under cruise.", "Good"),
            cvRow("K-factor", kFactor.toFixed(0), "Stall RPM divided by the square root of " + Math.round(torque) + " lb-ft. This is the number the shop builds to.", "Good"),
            cvRow("Stall torque ratio", str.toFixed(2), track === "noprep" || track === "street" ? "Kept down so the hit does not shock the tire." : "As high as this surface can take. More multiplies the hit and makes the car harder to hold.", "Good"),
            cvRow("Core", core, "A smaller can can stall higher, and it can also foot-brake lower when the torque ratio pushes the car. Order the K-factor, not the can by itself.", "Good"),
            cvRow("Cruise", Math.round(cruise).toLocaleString("en-US") + " RPM", cruiseDetail, cruiseStatus),
            cvRow("Shift", Math.round(shift).toLocaleString("en-US") + " RPM", shiftDetail, shiftStatus),
            cvRow(hold === "transbrake" ? "Trans brake" : "Foot brake", trans.first.toFixed(2) + " first gear", holdDetail, holdStatus),
            cvRow("Gear calculator", slip + "% at the shift", "That is the slip to type into the transmission calculator. Lockup in top gear is 0% once it is locked.", "Good")
        );
    }
}
bindCalc(calcConverter, ["cv-use", "cv-track", "cv-trans", "cv-hold", "cv-tq", "cv-tqrpm", "cv-hp", "cv-hprpm", "cv-rear", "cv-tire", "cv-shift", "cv-mph", "dt-loss"]);
"""

def carb_html(row):
    del row
    uses = (
        ("na", "Naturally aspirated"),
        ("blow", "Blow-through turbo"),
        ("draw", "Draw-through blower"),
    )
    jobs = (
        ("street", "Street"),
        ("strip", "Street/strip"),
        ("drag", "Drag"),
    )
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="cb-cid">Cubic inches</label><input type="number" id="cb-cid" value="383" min="200" max="800" step="1"></div>
        <div class="field"><label for="cb-rpm">Peak RPM</label><input type="number" id="cb-rpm" value="6500" min="4000" max="9000" step="100"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cb-use">Induction</label><select id="cb-use">{options(uses, "na")}</select></div>
        <div class="field"><label for="cb-job">Use</label><select id="cb-job">{options(jobs, "strip")}</select></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cb-ve">Volumetric efficiency (%)</label><input type="number" id="cb-ve" value="90" min="50" max="120" step="1"></div>
        <div class="field" id="cb-boost-field"><label for="cb-boost">Boost (PSI)</label><input type="number" id="cb-boost" value="10" min="0" max="40" step="1"></div>
    </div>
    <p class="field-hint">Street is often 80 to 85 percent volumetric efficiency. Street/strip is about 90. Drag on a race head can be 95 to 100. A blow-through carb sits in the hat, so boost does not raise the CFM. A draw-through carb sits ahead of the blower, so the pressure ratio does.</p>
    """
    return calculator_shell(primary, "", "Print carb sheet", results_extra='<div id="cb-shop" class="gear-shop"></div>')


CARB_SCRIPT = r"""
const CARB_SIZES = [600, 650, 750, 850, 950, 1050, 1150];

function carbCeiling(cfm) {
    for (let i = 0; i < CARB_SIZES.length; i++) {
        if (CARB_SIZES[i] >= cfm) return CARB_SIZES[i];
    }
    return null;
}

function carbFloor(cfm) {
    let floor = null;
    for (let i = 0; i < CARB_SIZES.length; i++) {
        if (CARB_SIZES[i] <= cfm) floor = CARB_SIZES[i];
    }
    return floor;
}

function pickCarb(cfm, job) {
    const above = carbCeiling(cfm);
    const below = carbFloor(cfm);
    if (job === "street" && below && above && (above - cfm) > 40 && ((cfm - below) / cfm) <= 0.12) {
        return { size: below, covered: true };
    }
    if (above) return { size: above, covered: true };
    return { size: CARB_SIZES[CARB_SIZES.length - 1], covered: false };
}

function calcCarb() {
    const cid = parseFloat(document.getElementById("cb-cid").value);
    const rpm = parseFloat(document.getElementById("cb-rpm").value);
    const vePct = parseFloat(document.getElementById("cb-ve").value);
    const boost = parseFloat(document.getElementById("cb-boost").value);
    const use = document.getElementById("cb-use").value;
    const job = document.getElementById("cb-job").value;
    const cidOk = Number.isFinite(cid) ? cid : 0;
    const rpmOk = Number.isFinite(rpm) ? rpm : 0;
    const boostOk = Math.max(0, Number.isFinite(boost) ? boost : 0);
    const ve = Math.min(1.2, Math.max(0.5, (Number.isFinite(vePct) ? vePct : 0) / 100));
    const volume = (cidOk * rpmOk * ve) / 3456;
    const ratio = (boostOk + 14.7) / 14.7;
    const boosted = use === "na" ? volume : volume * ratio;
    const sizing = use === "draw" ? boosted : volume;
    const pair = use === "draw" && sizing > 900;
    const each = pair ? sizing / 2 : sizing;
    const picked = pickCarb(each, use === "na" ? job : "strip");
    const mechanical = use !== "na" || job !== "street";
    const secondary = mechanical ? "Mechanical secondary" : "Vacuum secondary";
    const boostField = document.getElementById("cb-boost-field");
    if (boostField) boostField.style.display = use === "na" ? "none" : "";
    let order = picked.covered ? (picked.size + " CFM") : "Two carbs or a custom";
    if (use === "blow") order = picked.covered ? (picked.size + " CFM blow-through") : "Two blow-through carbs or a custom";
    if (pair && picked.covered) order = "Two " + picked.size + " CFM";
    const rows = [
        { label: "Carburetor to order", value: order, unit: "text", primary: true },
        { label: "Secondary", value: secondary, unit: "text" },
        { label: use === "draw" ? "Draw-through flow" : "Engine flow", value: sizing, unit: "cfm" }
    ];
    if (use === "blow") rows.push({ label: "Density ratio", value: ratio.toFixed(2) + " x", unit: "text" });
    publishReadout(rows);
    const mount = document.getElementById("cb-shop");
    if (!mount) return;
    const words = use === "blow" ? " CFM blow through carburetor" : (use === "draw" ? " CFM blower carburetor" : " CFM carburetor");
    const query = picked.size + words;
    const q = encodeURIComponent(query);
    let note = "The link searches that carburetor. Confirm the flange before you order.";
    if (!picked.covered) note = "That flow is past a single 1,150 CFM carburetor. Two carburetors or a larger custom is the next step.";
    else if (use === "blow") note = "Blow-through uses the same cubic feet as the engine. Boost makes the air denser, so this CFM can feed more power than it would on a naturally aspirated engine. The carb needs a solid float, a sealed bowl, mechanical secondaries, and a boost-referenced fuel-pressure regulator.";
    else if (pair) note = "A draw-through carb sits in atmospheric air ahead of the blower, so the flow is the engine CFM times the pressure ratio. The Blower Shop publishes that formula. This split is two carbs.";
    else if (job === "street") note = "Holley sizes a street carb at the flow, or slightly under it, and uses a vacuum secondary so the primaries can drive the car.";
    else note = "A street/strip or drag carb on this page is a mechanical-secondary double pumper. The converter or the clutch has to pull the main circuit open.";
    mount.innerHTML = '<a href="https://www.summitracing.com/search?keyword=' + q + '" rel="noopener">Summit Racing, ' + query + '</a>'
        + '<a href="https://www.jegs.com/search?Ntt=' + q + '" rel="noopener">Jegs, ' + query + '</a>'
        + '<p class="shop-note">' + note + '</p>';
}
bindCalc(calcCarb, ["cb-cid", "cb-rpm", "cb-ve", "cb-boost", "cb-use", "cb-job"]);
"""


def compression_html(row):
    del row
    primary = """
    <div class="grid-2">
        <div class="field"><label for="cr-bore">Bore (in)</label><input type="number" id="cr-bore" value="4.030" min="3.000" max="5.000" step="0.001"></div>
        <div class="field"><label for="cr-stroke">Stroke (in)</label><input type="number" id="cr-stroke" value="3.750" min="2.000" max="5.000" step="0.001"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cr-chamber">Chamber (cc)</label><input type="number" id="cr-chamber" value="64" min="20" max="120" step="0.1"></div>
        <div class="field"><label for="cr-dish">Piston dish (cc)</label><input type="number" id="cr-dish" value="6" min="-30" max="50" step="0.1"></div>
    </div>
    <p class="field-hint">A dish is a positive cc. A dome is a negative number. Valve reliefs on a flat top are a small positive dish.</p>
    """
    advanced = """
    <div class="grid-2">
        <div class="field"><label for="cr-gasket-bore">Gasket bore (in)</label><input type="number" id="cr-gasket-bore" value="4.100" min="3.000" max="5.200" step="0.001"></div>
        <div class="field"><label for="cr-gasket">Gasket thickness (in)</label><input type="number" id="cr-gasket" value="0.039" min="0.015" max="0.120" step="0.001"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cr-deck">Deck clearance (in)</label><input type="number" id="cr-deck" value="0.000" min="-0.030" max="0.050" step="0.001"></div>
        <div class="field"><label for="cr-target">Target ratio</label><input type="number" id="cr-target" value="10.5" min="7" max="16" step="0.1"></div>
    </div>
    <p class="field-hint">Deck clearance is how far the piston sits down in the hole at top dead center. A piston above the deck is a negative number.</p>
    """
    return calculator_shell(primary, advanced, "Print compression sheet")


COMPRESSION_SCRIPT = r"""
function crCc(bore, depth) {
    return bore * bore * depth * 0.785398163 * 16.387064;
}

function calcCompression() {
    const bore = parseFloat(document.getElementById("cr-bore").value);
    const stroke = parseFloat(document.getElementById("cr-stroke").value);
    const chamber = parseFloat(document.getElementById("cr-chamber").value);
    const dish = parseFloat(document.getElementById("cr-dish").value);
    const gasketBore = parseFloat(document.getElementById("cr-gasket-bore").value);
    const gasket = parseFloat(document.getElementById("cr-gasket").value);
    const deck = parseFloat(document.getElementById("cr-deck").value);
    const target = parseFloat(document.getElementById("cr-target").value);
    const boreOk = Number.isFinite(bore) ? bore : 0;
    const strokeOk = Number.isFinite(stroke) ? stroke : 0;
    const chamberOk = Number.isFinite(chamber) ? chamber : 0;
    const dishOk = Number.isFinite(dish) ? dish : 0;
    const gasketBoreOk = Number.isFinite(gasketBore) ? gasketBore : boreOk;
    const gasketOk = Number.isFinite(gasket) ? gasket : 0;
    const deckOk = Number.isFinite(deck) ? deck : 0;
    const targetOk = Number.isFinite(target) ? target : 10.5;
    const swept = crCc(boreOk, strokeOk);
    const gasketCc = crCc(gasketBoreOk, gasketOk);
    const deckCc = crCc(boreOk, deckOk);
    const clearance = chamberOk + gasketCc + deckCc + dishOk;
    const ratio = clearance > 0.5 ? (swept + clearance) / clearance : 0;
    const dishTarget = targetOk > 1 ? (swept / (targetOk - 1)) - chamberOk - gasketCc - deckCc : 0;
    const dishText = Math.abs(dishTarget).toFixed(1) + (dishTarget >= 0 ? " cc dish" : " cc dome");
    const rows = [
        { label: "Swept volume", value: swept.toFixed(1) + " cc", unit: "text" },
        { label: "Clearance volume", value: clearance.toFixed(1) + " cc", unit: "text" },
        { label: "Piston for " + targetOk.toFixed(1) + ":1", value: dishText, unit: "text" }
    ];
    if (ratio > 0) rows.unshift({ label: "Static compression", value: ratio, unit: "ratio", primary: true });
    else rows.unshift({ label: "Static compression", value: "Clearance is gone", unit: "text", primary: true });
    publishReadout(rows);
}
bindCalc(calcCompression, ["cr-bore", "cr-stroke", "cr-chamber", "cr-dish", "cr-gasket-bore", "cr-gasket", "cr-deck", "cr-target"]);
"""


def cam_html(row):
    del row
    heads = (
        ("h317", "317 cathedral"),
        ("h241", "241 cathedral"),
        ("h243", "243 / 799 cathedral"),
        ("tfx", "Trick Flow GenX cathedral"),
        ("ls3", "LS3 / L92 rectangle"),
        ("ls7", "LS7 rectangle"),
        ("afr", "Aftermarket rectangle"),
    )
    adders = (
        ("na", "Naturally aspirated"),
        ("turbo-low", "Turbo, large or twin"),
        ("turbo-high", "Turbo, single small"),
        ("super", "Supercharger"),
        ("nitrous", "Nitrous"),
    )
    jobs = (
        ("street", "Street"),
        ("strip", "Street/strip"),
        ("drag", "Drag"),
    )
    primary = f"""
    <div class="grid-2">
        <div class="field"><label for="cm-head">Cylinder head</label><select id="cm-head">{options(heads, "h243")}</select></div>
        <div class="field"><label for="cm-cid">Cubic inches</label><input type="number" id="cm-cid" value="364" min="280" max="500" step="1"></div>
    </div>
    <div class="grid-2">
        <div class="field"><label for="cm-rpm">Peak RPM</label><input type="number" id="cm-rpm" value="6200" min="4500" max="8500" step="100"></div>
        <div class="field"><label for="cm-adder">Power adder</label><select id="cm-adder">{options(adders, "na")}</select></div>
    </div>
    <div class="field"><label for="cm-job">Use</label><select id="cm-job">{options(jobs, "strip")}</select></div>
    <p class="field-hint">A 5.3 is about 325 cubic inches, a 6.0 is 364, a 6.2 is 376, and a 408 is the stroker. Street stays on the shortest card that still covers the RPM. Drag uses the longest published card aimed at that RPM. A large turbo or a pair keeps turbine pressure down. Every result is a published card. The page does not grind a lobe.</p>
    """
    return calculator_shell(primary, "", "Print cam card", results_extra='<div id="cm-shop" class="gear-shop"></div>')


CAM_SCRIPT = r"""
const CAM_HEADS = {
    h317: "cathedral",
    h241: "cathedral",
    h243: "cathedral",
    tfx: "cathedral",
    ls3: "rectangle",
    ls7: "rectangle",
    afr: "rectangle"
};
const CAMS = [
    { part: "GM 12561721", port: "cathedral", uses: ["na"], stock: true, durIn: 196, durEx: 207, liftIn: 0.467, liftEx: 0.479, lsa: 116, rpmMin: 4000, rpmMax: 5400, card: "Factory 2001 LS1 and 6.0 truck card, 196/207 at 0.050. Stock springs fit this lobe. It is the mild end of the list." },
    { part: "GM 12560950", port: "cathedral", uses: ["na"], stock: true, durIn: 204, durEx: 211, liftIn: 0.525, liftEx: 0.525, lsa: 116, rpmMin: 4800, rpmMax: 5800, card: "Factory 2001 LS6 card, 204/211 at 0.050. Stock springs fit this lobe." },
    { part: "GM 12565308", port: "cathedral", uses: ["na"], stock: true, durIn: 204, durEx: 218, liftIn: 0.551, liftEx: 0.548, lsa: 117.5, rpmMin: 5200, rpmMax: 6200, card: "Factory 2002-2004 LS6 card, 204/218 at 0.050. Stock springs fit this lobe." },
    { part: "GM 12623063", port: "rectangle", uses: ["na"], stock: true, durIn: 204, durEx: 211, liftIn: 0.551, liftEx: 0.522, lsa: 117, rpmMin: 4800, rpmMax: 5800, card: "Factory LS3 card, 204/211 at 0.050, single-bolt, no AFM and no VVT. Stock springs fit this lobe." },
    { part: "GM 12638426", port: "rectangle", heads: ["ls7"], uses: ["na"], durIn: 211, durEx: 230, liftIn: 0.558, liftEx: 0.558, lsa: 121, rpmMin: 5600, rpmMax: 6600, card: "Factory LS7 card, 211/230 at 0.050 and 121 LSA. GM lists 0.558 lift with a 1.7 rocker and 0.593/0.588 with the LS7 1.8 rocker. Operating range 6,500 RPM. It does not fit a Gen III block." },
    { part: "Comp Cams 54-455-11", port: "cathedral", uses: ["na"], cidMax: 359, durIn: 215, durEx: 223, liftIn: 0.604, liftEx: 0.610, lsa: 112, rpmMin: 1300, rpmMax: 6500, card: "Comp LSR cathedral card for a 4.8 to 5.7 that wants torque. Published 1,300 to 6,500 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-456-11", port: "cathedral", uses: ["na"], cidMax: 359, durIn: 219, durEx: 227, liftIn: 0.607, liftEx: 0.614, lsa: 112, rpmMin: 1500, rpmMax: 6700, card: "Comp LSR cathedral card for a broad 4.8 to 5.7 power band. Published 1,500 to 6,700 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-457-11", port: "cathedral", uses: ["na"], cidMax: 359, durIn: 223, durEx: 231, liftIn: 0.610, liftEx: 0.617, lsa: 112, rpmMin: 1700, rpmMax: 6800, card: "Comp LSR cathedral card once the intake and the exhaust can feed it. Published 1,700 to 6,800 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-458-11", port: "cathedral", uses: ["na"], cidMax: 359, durIn: 227, durEx: 235, liftIn: 0.614, liftEx: 0.621, lsa: 113, rpmMin: 1900, rpmMax: 7000, card: "Comp LSR cathedral street/strip card for a 4.8 to 5.7 with real airflow. Published 1,900 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-459-11", port: "cathedral", uses: ["na"], cidMin: 360, cidMax: 399, durIn: 231, durEx: 239, liftIn: 0.617, liftEx: 0.624, lsa: 113, rpmMin: 2000, rpmMax: 7000, card: "Comp LSR cathedral card for all-out 5.7 to 6.2 power. Published 2,000 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-460-11", port: "cathedral", uses: ["na"], cidMin: 360, cidMax: 399, durIn: 235, durEx: 243, liftIn: 0.621, liftEx: 0.624, lsa: 113, rpmMin: 2200, rpmMax: 7200, card: "Comp LSR cathedral card for mid-range through the top of a 5.7 to 6.2. Published 2,200 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-461-11", port: "cathedral", uses: ["na"], cidMin: 360, cidMax: 399, durIn: 239, durEx: 247, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2400, rpmMax: 7200, card: "Comp LSR race card for aftermarket cathedral heads and higher compression. Published 2,400 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-462-11", port: "cathedral", uses: ["na"], cidMin: 360, cidMax: 399, durIn: 243, durEx: 251, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2600, rpmMax: 7200, card: "Comp's longest 5.7 to 6.2 cathedral race card. Published 2,600 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-463-11", port: "cathedral", uses: ["na"], cidMin: 400, cidMax: 419, durIn: 247, durEx: 255, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2400, rpmMax: 7000, card: "Comp LSR cathedral card for 400 cubic inches and up. Published 2,400 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-464-11", port: "cathedral", uses: ["na"], cidMin: 420, cidMax: 439, durIn: 251, durEx: 259, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 2600, rpmMax: 7000, card: "Comp LSR cathedral card for a 420-cube race head. Published 2,600 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-465-11", port: "cathedral", uses: ["na"], cidMin: 440, durIn: 255, durEx: 263, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 2800, rpmMax: 7200, card: "Comp LSR cathedral card for power above 6,000 RPM on 440 cubic inches and up. Published 2,800 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-466-11", port: "cathedral", uses: ["na"], cidMin: 440, durIn: 259, durEx: 267, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 3000, rpmMax: 7200, card: "Comp's longest cathedral LSR card, for an extreme-displacement race engine. Published 3,000 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-453-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 219, durEx: 235, liftIn: 0.607, liftEx: 0.621, lsa: 113, rpmMin: 1500, rpmMax: 6700, card: "Comp LSR rectangle card for torque and a broad street band. Published 1,500 to 6,700 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-454-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 227, durEx: 243, liftIn: 0.614, liftEx: 0.624, lsa: 113, rpmMin: 1900, rpmMax: 7000, card: "Comp LSR rectangle street/strip card. Published 1,900 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-469-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 231, durEx: 247, liftIn: 0.617, liftEx: 0.624, lsa: 113, rpmMin: 2000, rpmMax: 7000, card: "Comp LSR rectangle card for a wide 5.7 to 6.2 power band. Published 2,000 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-470-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 235, durEx: 251, liftIn: 0.621, liftEx: 0.624, lsa: 113, rpmMin: 2200, rpmMax: 7200, card: "Comp LSR rectangle card for mid-range through the top. Published 2,200 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-471-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 239, durEx: 255, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2400, rpmMax: 7200, card: "Comp LSR race card for aftermarket rectangle heads and higher compression. Published 2,400 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-472-11", port: "rectangle", uses: ["na"], cidMax: 399, durIn: 243, durEx: 259, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2600, rpmMax: 7200, card: "Comp's longest 5.7 to 6.2 rectangle race card. Published 2,600 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-473-11", port: "rectangle", uses: ["na"], cidMin: 400, cidMax: 419, durIn: 247, durEx: 263, liftIn: 0.624, liftEx: 0.624, lsa: 114, rpmMin: 2400, rpmMax: 7000, card: "Comp LSR rectangle card for 400 cubic inches and up. Published 2,400 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-474-11", port: "rectangle", uses: ["na"], cidMin: 420, cidMax: 439, durIn: 251, durEx: 267, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 2600, rpmMax: 7000, card: "Comp LSR rectangle card for a 420-cube race head. Published 2,600 to 7,000 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-475-11", port: "rectangle", uses: ["na"], cidMin: 440, durIn: 255, durEx: 271, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 2800, rpmMax: 7200, card: "Comp LSR rectangle card for power above 6,000 RPM on 440 cubic inches and up. Published 2,800 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-476-11", port: "rectangle", uses: ["na"], cidMin: 440, durIn: 259, durEx: 275, liftIn: 0.624, liftEx: 0.624, lsa: 115, rpmMin: 3000, rpmMax: 7200, card: "Comp's longest rectangle LSR card, for an extreme-displacement race engine. Published 3,000 to 7,200 RPM. Stock springs cannot be used." },
    { part: "Comp Cams 54-330-11", port: "both", uses: ["turbo-low", "super"], cidMax: 346, durIn: 223, durEx: 225, liftIn: 0.598, liftEx: 0.600, lsa: 115, rpmMin: 2300, rpmMax: 7400, card: "Comp LST Stage 1, published for a 4.8 or 5.3 turbo when the turbine pressure is unknown. 2,300 to 7,400 RPM, 115 LSA. Stock springs cannot be used." },
    { part: "Comp Cams 54-332-11", port: "both", uses: ["turbo-low"], cidMax: 346, durIn: 231, durEx: 237, liftIn: 0.605, liftEx: 0.610, lsa: 115, rpmMin: 2500, rpmMax: 7400, card: "Comp LST Stage 2, published for a 5.3 with a lower-backpressure turbo. 2,500 to 7,400 RPM, 115 LSA. Stock springs cannot be used." },
    { part: "Summit SUM-8715", port: "both", uses: ["turbo-high", "super", "nitrous"], durIn: 222, durEx: 233, liftIn: 0.600, liftEx: 0.575, lsa: 115, overlap: -3, ivc: 43, rpmMin: 2800, rpmMax: 6800, card: "Summit Stage 1. Published overlap at 0.050 is -3 degrees, intake closes 43 degrees after bottom dead center, 2,800 to 6,800 RPM. Summit says this card works with a turbo, nitrous, or a supercharger, and it is the largest of their stages that works with a stock converter. Order the cathedral or rectangle core that matches the head." },
    { part: "Summit SUM-8706", port: "both", uses: ["turbo-high", "super"], durIn: 226, durEx: 230, liftIn: 0.600, liftEx: 0.575, lsa: 113, overlap: 2, ivc: 42, rpmMin: 3000, rpmMax: 7000, card: "Summit Stage 2 turbo card. Summit published it to keep overlap at 2 degrees when turbine pressure is high. Intake closes 42 degrees after bottom dead center, 3,000 to 7,000 RPM. Order the core that matches the head." },
    { part: "Summit SUM-8716", port: "both", uses: ["turbo-high", "super"], durIn: 231, durEx: 234, liftIn: 0.600, liftEx: 0.575, lsa: 115, overlap: 2, ivc: 46, rpmMin: 3000, rpmMax: 7000, card: "Summit Stage 3 turbo card for a single turbo with higher turbine pressure. Published overlap is 2 degrees, 3,000 to 7,000 RPM. Order the core that matches the head." },
    { part: "Summit SUM-8717", port: "both", uses: ["turbo-high", "super"], durIn: 237, durEx: 234, liftIn: 0.625, liftEx: 0.600, lsa: 117, overlap: 2, ivc: 50, rpmMin: 3500, rpmMax: 7200, card: "Summit Stage 4 turbo card. Reverse split, 237/234 at 0.050, 117 LSA, published for a single turbo with a T4 hot side. Overlap is 2 degrees. 3,500 to 7,200 RPM. Order the core that matches the head." },
    { part: "BTR-TURBOSTG4", port: "both", uses: ["turbo-low"], durIn: 227, durEx: null, liftIn: 0.618, liftEx: 0.618, lsa: 115, rpmMin: 6400, rpmMax: 8200, card: "Brian Tooley Stage 4 V2 turbo card, 227 intake duration at 0.050 and 115 LSA. Exhaust duration is printed 24X, so overlap is not calculated. Published for a stock-stroke engine over 8,000 RPM with the matching valvetrain, and for about 408 cubic inches at 6,400 to 6,800 RPM." },
    { part: "BTR-53NITROUS", port: "both", uses: ["nitrous"], cidMax: 346, durIn: 233, durEx: 250, liftIn: 0.631, liftEx: 0.617, lsa: 113, ivc: 44.5, rpmMin: 5200, rpmMax: 7500, band: "Higher RPM, high stall", card: "Brian Tooley 5.3 nitrous cam. The cam card prints 233/250 at 0.050, 113 LSA, and 0.631/0.617 net lift with a 1.7 rocker. Intake closes 44.5 degrees after bottom dead center. BTR describes a rough idle, a high stall, and power in the higher RPM range. They do not print a closed RPM band on that card." },
    { part: "BTR-400+NITROUS", port: "both", uses: ["nitrous"], cidMin: 400, durIn: 247, durEx: null, liftIn: 0.618, liftEx: 0.618, lsa: 112, rpmMin: 6800, rpmMax: 8000, band: "7,500 to 8,000 with the springs they name", card: "Brian Tooley 400-plus nitrous cam, 247 intake duration at 0.050 and 112 LSA. Exhaust duration is printed 27X, so overlap is not calculated. BTR says 7,500 RPM with SP010 springs and valves under 105 grams, and 8,000 RPM with SK703 springs shimmed to 1.700 and lightweight valves. Check piston to valve. A 1-bolt engine needs the 3-bolt conversion." }
];

function camOverlap(cam) {
    if (Number.isFinite(cam.overlap)) return cam.overlap;
    if (!Number.isFinite(cam.durEx)) return null;
    return (cam.durIn + cam.durEx) / 2 - (2 * cam.lsa);
}

function camCandidates(head, port, cid, adder) {
    return CAMS.filter(cam => {
        if (cam.port !== "both" && cam.port !== port) return false;
        if (cam.heads && cam.heads.indexOf(head) < 0) return false;
        if (cam.uses.indexOf(adder) < 0) return false;
        if (cam.stock && adder !== "na") return false;
        if (Number.isFinite(cam.cidMin) && cid < cam.cidMin) return false;
        if (Number.isFinite(cam.cidMax) && cid > cam.cidMax) return false;
        return true;
    });
}

const RACE_CAMS = {
    "Comp Cams 54-461-11": true,
    "Comp Cams 54-462-11": true,
    "Comp Cams 54-465-11": true,
    "Comp Cams 54-466-11": true,
    "Comp Cams 54-471-11": true,
    "Comp Cams 54-472-11": true,
    "Comp Cams 54-475-11": true,
    "Comp Cams 54-476-11": true,
    "BTR-TURBOSTG4": true,
    "BTR-53NITROUS": true,
    "BTR-400+NITROUS": true
};

function pickCam(list, rpm, job) {
    const eligible = list.filter(cam => !(cam.stock && rpm > 5600));
    if (!eligible.length) return null;
    const inside = eligible.filter(cam => rpm >= cam.rpmMin && rpm <= cam.rpmMax);
    if (inside.length) {
        if (job === "street") {
            const tame = inside.filter(cam => !RACE_CAMS[cam.part]);
            const pool = tame.length ? tame : inside;
            pool.sort((a, b) => a.durIn - b.durIn);
            return pool[0];
        }
        if (job === "drag") {
            const near = inside.filter(cam => (cam.rpmMax - rpm) <= 800);
            const pool = near.length ? near : inside;
            pool.sort((a, b) => b.durIn - a.durIn);
            return pool[0];
        }
        inside.sort((a, b) => {
            const gap = (a.rpmMax - rpm) - (b.rpmMax - rpm);
            if (gap) return gap;
            const nearTop = (a.rpmMax - rpm) <= 400;
            return nearTop ? b.durIn - a.durIn : a.durIn - b.durIn;
        });
        return inside[0];
    }
    const above = eligible.filter(cam => cam.rpmMax < rpm);
    const pool = above.length ? above : eligible.filter(cam => cam.rpmMin > rpm);
    if (!pool.length) return eligible[0];
    if (above.length) {
        const bestMax = Math.max.apply(null, pool.map(cam => cam.rpmMax));
        const close = pool.filter(cam => bestMax - cam.rpmMax <= 400);
        close.sort((a, b) => b.durIn - a.durIn);
        return close[0];
    }
    pool.sort((a, b) => a.rpmMin - b.rpmMin || a.durIn - b.durIn);
    return pool[0];
}

function overlapLine(overlap, adder, cam) {
    if (adder === "nitrous" && cam && cam.durEx != null && cam.durEx > cam.durIn) return " The exhaust duration is longer than the intake. That is the published nitrous split, so the extra exhaust from the shot has time to leave.";
    if (overlap == null) return "";
    if (overlap <= -5) return " Overlap at 0.050 is negative. That is the wide factory lobe separation, and it gives up the intake pull a longer published card uses.";
    if (overlap < 4) return " Overlap at 0.050 stays near zero, so boost is not pushed out the exhaust. That is the published turbo and supercharger pattern on this list.";
    return " Overlap at 0.050 is positive, so the exhaust can pull the next intake charge. That is the naturally aspirated pattern on this list.";
}

function calcCam() {
    const head = document.getElementById("cm-head").value;
    const cid = parseFloat(document.getElementById("cm-cid").value);
    const rpm = parseFloat(document.getElementById("cm-rpm").value);
    const adder = document.getElementById("cm-adder").value;
    const job = document.getElementById("cm-job").value;
    const port = CAM_HEADS[head] || "cathedral";
    const cidOk = Number.isFinite(cid) ? cid : 0;
    const rpmOk = Number.isFinite(rpm) ? rpm : 0;
    const cam = pickCam(camCandidates(head, port, cidOk, adder), rpmOk, job);
    const mount = document.getElementById("cm-shop");
    if (!cam) {
        publishReadout([{ label: "Cam to order", value: "No published card", unit: "text", primary: true }]);
        if (mount) mount.innerHTML = "";
        return;
    }
    const overlap = camOverlap(cam);
    const duration = Number.isFinite(cam.durEx) ? (cam.durIn + "/" + cam.durEx) : (cam.durIn + " / not published");
    const rows = [
        { label: "Cam to order", value: cam.part, unit: "text", primary: true },
        { label: "Duration at 0.050", value: duration, unit: "text" },
        { label: "Valve lift", value: cam.liftIn.toFixed(3) + "/" + cam.liftEx.toFixed(3), unit: "text" },
        { label: "Lobe separation", value: cam.lsa, unit: "deg" },
        { label: "Published range", value: cam.band || (cam.rpmMin.toLocaleString("en-US") + "-" + cam.rpmMax.toLocaleString("en-US")), unit: "text" }
    ];
    if (overlap == null) rows.push({ label: "Overlap at 0.050", value: "Not published", unit: "text" });
    else rows.push({ label: "Overlap at 0.050", value: overlap, unit: "deg" });
    if (Number.isFinite(cam.ivc)) rows.push({ label: "Intake close at 0.050", value: cam.ivc + " ABDC", unit: "text" });
    publishReadout(rows);
    let limit = "";
    if (cam.band) {
        limit = "";
    } else if (rpmOk > cam.rpmMax) {
        limit = " This card is published to " + cam.rpmMax.toLocaleString("en-US") + " RPM. No card on this list is published to " + rpmOk.toLocaleString("en-US") + " RPM.";
    } else if (rpmOk < cam.rpmMin) {
        limit = " This card is published from " + cam.rpmMin.toLocaleString("en-US") + " RPM. No card on this list starts as low as " + rpmOk.toLocaleString("en-US") + " RPM.";
    }
    if (mount) {
        const q = encodeURIComponent(cam.part);
        const useLine = job === "street"
            ? " Street uses the shortest published card that still covers this RPM."
            : (job === "drag" ? " Drag uses the longest published card aimed at this RPM." : "");
        mount.innerHTML = "<p>" + cam.card + overlapLine(overlap, adder, cam) + useLine + limit + "</p>"
            + '<a href="https://www.summitracing.com/search?keyword=' + q + '" rel="noopener">Summit Racing, ' + cam.part + "</a>"
            + '<a href="https://www.jegs.com/search?Ntt=' + q + '" rel="noopener">Jegs, ' + cam.part + "</a>"
            + '<p class="shop-note">The link searches that part number. Check piston-to-valve clearance and the valve springs before you order.</p>';
    }
}
bindCalc(calcCam, ["cm-head", "cm-cid", "cm-rpm", "cm-adder", "cm-job"]);
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
        "Gear = (Target RPM x Tire Diameter) / (Trap MPH x Trans Final x 336). The set to order is the closest catalog ratio for that rear end. Finish RPM = (Trap MPH x Overall Ratio x 336) / Tire Diameter.",
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
    "LS": (
        "CID = Bore x Bore x Stroke x 0.7854 x 8. SCR = (Swept volume + clearance volume) / clearance volume. Clearance volume is the chamber, the gasket, the deck, and the piston dish. DCR uses the piston position at intake-valve closing instead of the full stroke.",
        ls_html,
        LS_PAGE_SCRIPT,
    ),
    "FuelPump": (
        "Engine gal/hr = (Flywheel HP x BSFC) / Fuel density. A 1:1 return regulator makes the pump hold base pressure plus boost. Shop the flow that remains at that pressure after the margin.",
        fuel_pump_html,
        FUEL_PUMP_SCRIPT,
    ),
    "Nitrous": (
        "Nitrous lb/hr = Shot HP x 3.6 once the jet is sized for that shot. Jet diameter follows the shot per nozzle and the square root of bottle pressure over 900 PSI. The fuel jet feeds that nitrous at the fuel's nitrous-to-fuel ratio. Gasoline timing pull is 2 degrees per 50 HP.",
        n2o_html,
        N2O_SCRIPT,
    ),
    "Shock": (
        "Front extension slows the rise. Rear compression softens the hit. A single adjustable moves rebound only. A double adjustable adds compression, which is the rear hit and the speed the nose comes back down. Clicks count from full soft toward firm. Order the shock 1/2 in short of the bump measurement and 1/2 in longer than full droop.",
        shock_html,
        SHOCK_SCRIPT,
    ),
    "Converter": (
        "K = Brake stall RPM / sqrt(torque at that RPM). Brake stall is set under the torque peak so the engine can accelerate through it. Stall torque ratio is as high as the tire can take. Cruise RPM = (MPH x top gear x rear gear x 336) / tire diameter, and an unlocked converter has to stall under that.",
        converter_html,
        CONVERTER_SCRIPT,
    ),
    "Electrical": (
        "Load Amps = Watts / Voltage | Design Amps = Load x Duty Factor. Relay, fuse, and wire size sit above that current. Pin 30 is the fused battery feed, pin 87 feeds the load, pin 86 is the switch, and pin 85 is ground.",
        electrical_html,
        ELECTRICAL_SCRIPT,
    ),
    "Cooling": (
        "Pass heat = HP x BSFC x fuel BTU/lb x 0.06 x seconds / 3600. That 6% is the share that stays in the metal and the water on a short pass. Fan CFM = BTU/hr / (1.08 x air rise). Pump GPM = BTU/min / (coolant rise x lb/gal x specific heat).",
        cooling_html,
        COOLING_SCRIPT,
    ),
    "Driveline": (
        "Critical RPM = 4,770,000 x material x square root(OD^2 + ID^2) / length^2, for a steel tube. Aluminum uses 0.981 of that, from the modulus and the density. The planning limit is 75% of critical. Shaft RPM = engine RPM / top gear. Working angle is the difference between the tube and the transmission, and between the tube and the pinion.",
        driveline_html,
        DRIVELINE_SCRIPT,
    ),
    "Power": (
        "Running amps are the pump, fan, water pump, ignition, and ECU. Alternator idle output wants 1.2 times that. Cable circular mils = 10.75 x amps x one-way feet x 2 / (voltage x 0.03). The trans brake and the nitrous sit on the battery for the hit.",
        power_html,
        POWER_SCRIPT,
    ),
    "Carb": (
        "Engine CFM = (Cubic inches x RPM x Volumetric efficiency) / 3456. A blow-through carb uses that CFM. A draw-through carb multiplies it by (boost + 14.7) / 14.7. Street orders the catalog size at the flow, or one step under. Street/strip and drag order the next size up.",
        carb_html,
        CARB_SCRIPT,
    ),
    "Compression": (
        "Static compression = (Swept volume + clearance volume) / clearance volume. Clearance volume is the chamber, the gasket, the deck, and the piston dish. A dome is a negative dish.",
        compression_html,
        COMPRESSION_SCRIPT,
    ),
    "Cam": (
        "The page orders the published cam card whose RPM range covers this cubic inch, head port, power adder, and use. Street takes the shortest card that still covers the RPM. Drag takes the longest card aimed at that RPM. Overlap at 0.050 = (intake duration + exhaust duration) / 2 - (2 x lobe separation). Nitrous, turbo, and supercharger cards are separate lists.",
        cam_html,
        CAM_SCRIPT,
    ),
    "CAS": (
        "Pressure Ratio = (Boost PSI + Barometric PSI) / Barometric PSI",
        cas_html,
        CAS_SCRIPT,
    ),
}


def follow_on(category):
    steps = []
    for slug, label in NEXT_STEPS.get(category, ()):
        steps.append(f'<a href="{esc(slug)}.html">{esc(label)}</a>')
    shops = []
    for label, url in AFFILIATE_LINKS.get(category, ()):
        shops.append(f'<a href="{esc(url)}" rel="sponsored noopener">{esc(label)}</a>')
    parts = []
    if steps:
        parts.append('<div class="next-steps"><p class="field-hint">Next in the build</p>' + "".join(steps) + "</div>")
    if shops:
        parts.append(
            '<div class="next-steps"><p class="field-hint">Shop this spec</p>'
            + "".join(shops)
            + '<p class="shop-note">Some of these are affiliate links. DragCalculators may earn a commission if you buy through them, at no extra cost to you.</p></div>'
        )
    return "".join(parts)


def analytics_tag():
    if not ANALYTICS_ID:
        return ""
    tag = esc(ANALYTICS_ID)
    return (
        f'    <script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script>\n'
        "    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        f"gtag('js',new Date());gtag('config','{tag}');</script>\n"
    )


def footer():
    return """
<footer class="site-footer">
    <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved.</p>
    <p><a class="accent" href="contact.html">Contact &amp; Sponsorships</a> &nbsp;|&nbsp; <a href="privacy.html">Privacy Policy &amp; Affiliate Disclosure</a></p>
</footer>
"""


SEARCH_SCRIPT = r"""
(function () {
    const input = document.getElementById("site-search");
    const list = document.getElementById("site-search-results");
    const raw = document.getElementById("site-search-data");
    if (!input || !list || !raw) return;
    let records = [];
    try { records = JSON.parse(raw.textContent); } catch (err) { records = []; }
    let active = -1;

    function escapeHtml(value) {
        return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function rank(record, query) {
        const title = record.title.toLowerCase();
        const group = record.group.toLowerCase();
        const slug = record.slug.replace(/-/g, " ");
        if ((title + " " + group + " " + slug).indexOf(query) === -1) return 99;
        let score = record.hub ? 0 : 5;
        if (title.indexOf(query) === 0) score -= 2;
        else if (group.indexOf(query) === 0) score -= 1;
        return score;
    }

    function hits() {
        const query = input.value.trim().toLowerCase();
        if (!query) return [];
        return records.map(record => ({ record: record, score: rank(record, query) }))
            .filter(item => item.score < 99)
            .sort((a, b) => a.score - b.score || a.record.title.localeCompare(b.record.title))
            .slice(0, 8);
    }

    function render() {
        const found = hits();
        active = -1;
        if (!input.value.trim()) {
            list.hidden = true;
            list.innerHTML = "";
            return;
        }
        list.hidden = false;
        if (!found.length) {
            list.innerHTML = '<p class="search-empty">No calculator matches that.</p>';
            return;
        }
        list.innerHTML = found.map(item => {
            const record = item.record;
            return '<a href="' + record.slug + '.html"><strong>' + escapeHtml(record.title) + '</strong><span>' + escapeHtml(record.group) + '</span></a>';
        }).join("");
    }

    function move(step) {
        const links = list.querySelectorAll("a");
        if (!links.length) return;
        active = Math.max(0, Math.min(links.length - 1, active + step));
        links.forEach((link, index) => link.classList.toggle("active", index === active));
        links[active].scrollIntoView({ block: "nearest" });
    }

    input.addEventListener("input", render);
    input.addEventListener("keydown", (event) => {
        if (event.key === "ArrowDown") {
            event.preventDefault();
            move(1);
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            move(-1);
        } else if (event.key === "Enter") {
            const links = list.querySelectorAll("a");
            const pick = links[active] || links[0];
            if (pick) {
                event.preventDefault();
                location.href = pick.getAttribute("href");
            }
        } else if (event.key === "Escape") {
            list.hidden = true;
        }
    });
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".site-search")) list.hidden = true;
    });
    input.form.addEventListener("submit", (event) => event.preventDefault());
})();
"""


def search_records(pages, hubs_by_category):
    records = []
    for page in pages:
        hub = hubs_by_category.get(page["category"], {})
        records.append({
            "slug": page["slug"],
            "title": page["target_keyword"],
            "group": section_for(hub.get("slug", "")) or hub.get("nav_label") or page["category"],
            "hub": page["role"] == "hub",
        })
    return records


def site_banner(records):
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f"""<header class="site-banner">
    <a class="brand" href="index.html">
        <span class="brand-mark">DC</span>
        <span class="brand-copy"><strong>DragCalculators</strong><em>Setup sheets for the pass</em></span>
    </a>
    <form class="site-search" role="search">
        <label class="sr-only" for="site-search">Search calculators</label>
        <input id="site-search" type="search" placeholder="Search calculators" autocomplete="off" enterkeyhint="search">
        <div id="site-search-results" class="search-results" hidden></div>
    </form>
    <a class="banner-cta" href="contact.html">Advertise</a>
</header>
<script type="application/json" id="site-search-data">{payload}</script>
<script>
{SEARCH_SCRIPT}
</script>
"""


NAV_SECTIONS = (
    ("Fuel", ("fuel-injector-calculator", "fuel-pump-calculator", "carburetor-cfm-calculator")),
    ("Power", (
        "turbo-sizing-calculator",
        "wastegate-sizing-calculator",
        "supercharger-pulley-calculator",
        "nitrous-shot-calculator",
    )),
    ("Engine", ("ls-engine-builder", "compression-ratio-calculator", "ls-camshaft-calculator", "exhaust-header-sizing-calculator")),
    ("Drivetrain", (
        "transmission-shift-recovery-calculator",
        "torque-converter-calculator",
        "rear-gear-calculator",
        "driveshaft-calculator",
    )),
    ("Chassis", (
        "four-link-suspension-calculator",
        "drag-shock-calculator",
        "tire-growth-calculator",
    )),
    ("Cooling and wiring", (
        "drag-cooling-system-calculator",
        "automotive-relay-calculator",
        "race-car-wiring-calculator",
    )),
)


def section_for(slug):
    for title, slugs in NAV_SECTIONS:
        if slug in slugs:
            return title
    return ""


def sidebar(active_slug, hubs):
    by_slug = {hub["slug"]: hub for hub in hubs}
    parts = ['<nav class="nav-list">']
    master_class = "nav-item active" if active_slug == "index" else "nav-item"
    parts.append(f'<a class="{master_class}" href="index.html">Start here</a>')
    used = set()
    for title, slugs in NAV_SECTIONS:
        rows = []
        for slug in slugs:
            hub = by_slug.get(slug)
            if not hub:
                continue
            used.add(slug)
            css = "nav-item active" if hub["slug"] == active_slug else "nav-item"
            rows.append(f'<a class="{css}" href="{esc(hub["slug"])}.html">{esc(hub["nav_label"])}</a>')
        if rows:
            parts.append(f'<div class="nav-group"><p class="nav-group-label">{esc(title)}</p>{"".join(rows)}</div>')
    leftover = []
    for hub in hubs:
        if hub["slug"] in used:
            continue
        css = "nav-item active" if hub["slug"] == active_slug else "nav-item"
        leftover.append(f'<a class="{css}" href="{esc(hub["slug"])}.html">{esc(hub["nav_label"])}</a>')
    if leftover:
        parts.append(f'<div class="nav-group"><p class="nav-group-label">More</p>{"".join(leftover)}</div>')
    parts.append("</nav>")
    return "".join(parts)


def grouped_directory(hubs):
    by_slug = {hub["slug"]: hub for hub in hubs}
    parts = []
    used = set()
    for title, slugs in NAV_SECTIONS:
        items = []
        for slug in slugs:
            hub = by_slug.get(slug)
            if not hub:
                continue
            used.add(slug)
            items.append(f'<li><a href="{esc(slug)}.html">{esc(hub["nav_label"])}</a></li>')
        if items:
            parts.append(f'<p class="field-hint">{esc(title)}</p><ul class="variant-list">{"".join(items)}</ul>')
    leftover = [hub for hub in hubs if hub["slug"] not in used]
    if leftover:
        items = "".join(
            f'<li><a href="{esc(hub["slug"])}.html">{esc(hub["nav_label"])}</a></li>' for hub in leftover
        )
        parts.append(f'<p class="field-hint">More</p><ul class="variant-list">{items}</ul>')
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
        ("Why pick the rear end to buy a gear?", "The ratio alone is not a part. A 3.73 Ford 9-inch set does not fit an 8.8, a 12-bolt, or a Dana 60. The housing sets the ring, the pinion, and the carrier."),
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
        ("Why does the same ratio need a different gear?", "Each housing has its own ring diameter and its own catalog ratios. A Ford 9-inch 4.10 is the 4.11 set. A Dana 60 4.56 also needs the 4.56-and-up carrier."),
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
    "LS": (
        ("How does a stroker change the inches?", "Displacement is bore times bore times stroke times 0.7854 times 8. A 4.000 inch crank in an iron 5.3 or 6.0 adds cubes without changing the bore, as long as the piston compression height still clears the rings."),
        ("What is the difference between static and dynamic compression?", "Static compression uses the full stroke. Dynamic compression uses the piston position when the intake valve closes, so a later-closing cam bleeds some of that compression off."),
        ("Why can a part fit the block and still be the wrong part?", "An LS7 crank shares the main journal, and an LS3 head bolts to a 6.0, but the piston height, the chamber versus the bore, and the power limit still have to match the combination."),
    ),
    "FuelPump": (
        ("Why does boost change the pump and not just the injector?", "A 1:1 regulator raises rail pressure with manifold pressure, so the pump outlet is base pressure plus boost. The injector differential stays near the base, which is why injector size uses base pressure and the pump uses the higher number."),
        ("Why is the shopping flow bigger than engine demand?", "Voltage drop, a dirty filter, and hot fuel all steal flow. The margin, 25% unless you change it, is the flow the pump still needs to make at the working pressure."),
        ("Why does a 40 PSI catalog number shrink?", "Most in-tank pumps are rated near 40 PSI and fall off toward their deadhead. The table draws a straight line between those two points. Raise the deadhead if the pump's own curve holds pressure longer."),
        ("When does a mechanical pump belong on the car?", "A cam-driven diaphragm pump feeds a carburetor and shuts off around 7 to 17 PSI. A belt-driven gear or gerotor pump is the mechanical pump that holds EFI pressure. Its flow follows pump rpm, so the pulley ratio is part of the setup."),
    ),
    "Nitrous": (
        ("Why does bottle pressure change the jet?", "A nitrous jet is a liquid orifice. More bottle pressure pushes more nitrous through the same hole, so the hit gets richer on nitrous and the fuel jet is suddenly small. Hold the bottle near 900 to 950 PSI."),
        ("How much timing does a shot want?", "Gasoline starts at about 2 degrees pulled for every 50 HP of nitrous. E85 and race gas want less, and methanol wants less again. The first hit on gasoline can stand another 2 degrees of reserve."),
        ("What is the difference between a wet plate and a dry shot?", "A wet system brings its own fuel through a fuel jet and a fuel solenoid. A dry system sprays only nitrous, and the injectors have to add the fuel. The duty cycle is the check on a dry car."),
    ),
    "Shock": (
        ("What does the front extension knob do?", "On the launch the front shock gets longer. That circuit is extension. More extension slows the rise and softens the hit. Less extension lets the nose come up faster and plants the tire harder."),
        ("Why is rear compression the hit knob?", "The rear shock gets shorter as the car squats. More compression keeps the tire from getting shocked. Rear extension is the recovery and the gear change, not the first hit. A single adjustable cannot move compression."),
        ("How do prepped, radial prep, and no prep differ?", "A prepped slick can take a faster hit, so front extension and rear compression stay softer. Radial prep is the middle. No prep breaks loose if the hit is sharp, so those two knobs go firmer. The shock cannot invent grip the track does not have."),
        ("Which shock do I order?", "Measure center to center at ride, at full bump, and at full droop. Order a collapsed length at least 1/2 in shorter than the bump measurement and an extended length at least 1/2 in longer than droop. The front wants more of that stroke in extension. The rear wants more of it in compression."),
    ),
    "Electrical": (
        ("How is the circuit current found?", "Load amps are watts divided by voltage. Size the wire, fuse, and relay above that, and apply a duty factor for a fan or pump that is not on full time."),
        ("Why size the wire for the run length?", "Voltage drop grows with current and length. A fuel pump at the back of the car needs a larger gauge than the same pump next to the battery."),
        ("What does the relay protect?", "The relay lets a small switch current close a high-current path. The fuse protects the wire, and it belongs at the power source."),
        ("Which pin is which?", "Pin 30 is battery power through the fuse. Pin 87 goes to the pump or fan on the same gauge. Pin 86 is the switch, on 18 AWG. Pin 85 is ground. A diode inside the relay wants 86 on power and 85 on ground."),
    ),
    "Cooling": (
        ("Why is a drag radiator not sized like a dyno?", "A dyno pull holds the power. A pass is about 10 seconds, and most of the fuel energy leaves in the exhaust before it ever reaches the water. The temperature climb on one hit is the check."),
        ("When does the fan actually work?", "Ram air does the return road. The fan works in the lanes, and only if a shroud makes it pull through the core. Leaving the engine running is a bigger load than the pass itself."),
        ("Why an electric water pump if the car already has one?", "A mechanical pump moves the most water at RPM, which is the hit. It moves little at idle. The electric pump is there so the fans still have flow while the car sits."),
    ),
    "Driveline": (
        ("Where is the driveshaft measured?", "At ride height, center of the front U-joint to center of the rear U-joint. The slip yoke wants about 3/4 in before it bottoms at ride, and about 1 in still engaged at full droop."),
        ("What is critical speed?", "It is the RPM where the tube's first bending mode lines up with the shaft speed. The constant 4,770,000 is the steel modulus and density in that formula. Stay under 75% of it. A bigger diameter raises it. A longer tube lowers it by the length squared."),
        ("Why can the pinion angle look wrong at rest?", "A 4-link barely wraps, so the pinion should already point along the tube. A leaf spring wraps on the launch, so it wants about 2 degrees nose down at rest and straight once the axle winds up."),
    ),
    "Power": (
        ("Which amps does the alternator have to cover?", "The loads that stay on while the engine idles in the lanes: pump, fan, water pump, ignition, ECU. The trans brake and the nitrous are a few seconds, and the battery covers that hit."),
        ("Why size the wire from voltage drop?", "Circular mils equal 10.75 times the amps times the round-trip length, divided by a 3% voltage drop. A trunk battery makes the alternator wire the long one. High-strand battery cable is what carries it, not primary wire in a loom."),
        ("Where does the fuse go?", "On the battery post, ahead of the panel feed. The starter cable is its own 1/0 or 2/0 and is not fused like a running load."),
    ),
    "Carb": (
        ("How is carburetor CFM calculated?", "Cubic inches times peak RPM times volumetric efficiency, divided by 3456. A 383 at 6,500 RPM and 90 percent is about 648 CFM, so the carburetor to order is a 650."),
        ("Why does street sometimes order the smaller carb?", "Holley sizes a street carb at the calculated flow, or slightly under it, with a vacuum secondary. Street/strip and drag stay at or above the flow and use a mechanical secondary."),
        ("Why is a blow-through carb not a bigger CFM?", "The carb sits in the hat, after the turbo. It still passes the engine's cubic feet. Boost raises the density, not the volume, so a 650 or 750 can feed a lot more power than it would on a naturally aspirated engine. It needs a solid float, sealed bowls, mechanical secondaries, and a boost-referenced regulator."),
        ("What changes on a draw-through blower?", "The carb sits in atmospheric air ahead of the blower. The Blower Shop multiplies the engine CFM by (boost + 14.7) / 14.7. This page also keeps the volumetric efficiency you enter. Past 900 CFM the result is two carbs, each carrying half."),
    ),
    "Compression": (
        ("How is static compression calculated?", "Swept volume plus clearance volume, divided by clearance volume. Clearance is the chamber, the head gasket, the deck, and the piston dish. A dome is entered as a negative dish."),
        ("What dish hits a target ratio?", "The page solves the dish that lands on the target once the bore, stroke, chamber, gasket, and deck are fixed. It does not pick a piston part number."),
        ("Why does a thicker gasket drop the ratio?", "A thicker gasket, or a larger gasket bore, adds clearance volume. The same piston in a bigger chamber does the same thing."),
    ),
    "Cam": (
        ("Why is there no custom duration?", "Every result is a published cam card with a part number. Intake duration, exhaust duration, lift, and lobe separation come from that card. The page does not grind a lobe."),
        ("Why does a turbo engine not get the factory cam?", "A factory LS3 or LS6 card is about 204 degrees at 0.050 and it is not published as a turbo cam. A large turbo at high RPM uses the Brian Tooley Stage 4 card, which is published past 8,000 RPM on a stock-stroke engine. A single small turbo uses the Summit turbo cards, which keep overlap near zero so exhaust pressure does not blow back into the intake."),
        ("What does cubic inches change?", "Comp splits the naturally aspirated LSR cards into under 360 cubic inches, 360 to 399, and 400 and up. The Comp turbo cards are published for a 4.8 or 5.3. A bigger turbo engine moves to the Summit or Brian Tooley card."),
        ("What does street or drag change?", "Street orders the shortest published card that still covers the RPM, and it skips the race cards when a milder one covers. Drag orders the longest card whose published range is aimed at that RPM. Street/strip keeps the tightest ceiling."),
        ("Where are the nitrous cams?", "A mild nitrous build uses Summit Stage 1, which Summit says works with nitrous and a stock converter. A 5.3 at higher RPM uses the Brian Tooley 5.3 nitrous card, 233/250 at 0.050. A 400-cube nitrous engine uses the Brian Tooley 400-plus card. Exhaust duration printed as 27X is left unpublished."),
        ("What happens past the published RPM?", "Hydraulic-roller cards on this list stop where the maker printed the range, about 7,200 RPM for the naturally aspirated LSR cams and 7,200 to 7,400 for the Comp and Summit turbo cams. Above that, the page says so instead of stretching a shorter card."),
    ),
    "Converter": (
        ("What is K-factor?", "K-factor is brake stall RPM divided by the square root of engine torque at that RPM. The same converter stalls higher behind an engine with more torque. Give the shop the K, the stall, and the torque, not a stall number with no engine attached."),
        ("Where should the stall sit?", "Brake stall wants to land about 500 to 700 RPM under the torque peak so the engine accelerates through the converter instead of starting above it. A no-prep tire wants it lower. An unlocked street converter also has to stall under cruise RPM."),
        ("Why is the car weight not in the stall?", "Brake stall is engine torque against the converter with the turbine held. Weight, the tire, and the gear decide whether that stall hooks. They do not change the RPM."),
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
        "ANALYTICS": analytics_tag(),
        "BANNER": SITE_BANNER,
        "BACK_ROW": '<div class="back-row"><a href="index.html" class="back-link">&larr; Start here</a></div>',
        "SIDEBAR": sidebar(active, hubs),
        "H1": esc(page["target_keyword"]),
        "SPEC": f'<p class="spec">{esc(spec)}</p>' if spec else "",
        "TOOL": html_fn(page) + follow_on(page["category"]),
        "CONTENT": formula_box(formula) + notes_box(page) + related_box(page, pages, hubs_by_category),
        "FOOTER": footer(),
        "SCRIPT": UI_SCRIPT + "\n" + script,
    }


def index_page(pages, hubs):
    transmission = next(page for page in pages if page["slug"] == "transmission-shift-recovery-calculator")
    _formula, html_fn, script = WIDGETS["Transmission"]
    directory = grouped_directory(hubs)
    start = link_items([
        {"slug": "fuel-injector-calculator", "target_keyword": "Fuel injectors"},
        {"slug": "fuel-pump-calculator", "target_keyword": "Fuel pump"},
        {"slug": "carburetor-cfm-calculator", "target_keyword": "Carburetor"},
        {"slug": "compression-ratio-calculator", "target_keyword": "Compression ratio"},
        {"slug": "ls-camshaft-calculator", "target_keyword": "LS camshaft"},
        {"slug": "nitrous-shot-calculator", "target_keyword": "Nitrous jet and timing"},
        {"slug": "drag-shock-calculator", "target_keyword": "Shock to order"},
        {"slug": "torque-converter-calculator", "target_keyword": "Torque converter stall"},
        {"slug": "drag-cooling-system-calculator", "target_keyword": "Cooling, fan, and water pump"},
        {"slug": "driveshaft-calculator", "target_keyword": "Driveshaft length and angles"},
        {"slug": "race-car-wiring-calculator", "target_keyword": "Alternator and wire size"},
    ])
    content = (
        content_box(
            "Start a build",
            "<p>These end in a part. The menu is grouped the way a car is built: fuel together, power together, then the gear, the chassis, and the wiring.</p>"
            + start,
        )
        + content_box("Calculators", directory)
        + content_box(
            "Track sponsorships",
            '<p class="sponsor">A shop can take the banner across the top, the line on the printed setup sheet, '
            'or the part links under one calculator. Tell us which tool your customer is already using. '
            'Inquiries go through the <a href="contact.html">contact form</a>.</p>',
        )
        + content_box(
            "Track-side notes",
            "<p>Density altitude: about 3% naturally aspirated power per 1,000 feet. "
            "Converter slip at the finish is often kept around 5% to 8%. "
            "On boost, pull roughly 1 to 2 degrees of timing for every 3 to 4 PSI.</p>",
        )
    )
    spec = spec_text(transmission)
    return fill(
        PAGE_TEMPLATE,
        TITLE=esc("Ultimate Drag Racing Master Suite | Drivetrain & Shift Calculator"),
        DESCRIPTION=esc(
            "Drag racing calculators for gear ratios, turbo sizing, LS engine builds, "
            "nitrous jetting, shock selection, torque converter stall, fuel injectors, fuel pumps, supercharger pulleys, tire growth, and chassis setup."
        ),
        CANONICAL=esc(f"{ORIGIN}/"),
        VERIFICATION=VERIFICATION,
        ORIGIN=ORIGIN,
        ANALYTICS=analytics_tag(),
        BANNER=SITE_BANNER,
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
<p>A shop can buy the banner across the top, the line on every printed setup sheet, or the part links under one calculator: converter, shocks, fuel system, or rear gear. Rates follow the visits on that page.</p>
<p>Calculator feedback and other partnership inquiries use the same form.</p>
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
        ANALYTICS=analytics_tag(),
        BANNER=SITE_BANNER,
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
<p>The calculators run in your browser. Horsepower, gear ratios, tire diameters, and the rest of the inputs stay on the page unless you choose Email this setup or the contact form. Those forms send the address you enter, and the setup or message you submit, to DragCalculators through Formspree.</p>
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
        ANALYTICS=analytics_tag(),
        BANNER=SITE_BANNER,
        CONTENT=content,
        FOOTER=footer(),
    )


def not_found_page():
    content = """
<h1>That setup page moved</h1>
<p>The gear-and-tire grid and the pulley grid now live inside the calculators. Open the tool, set the combination, and copy a link to that setup.</p>
<ul class="variant-list">
    <li><a href="transmission-shift-recovery-calculator.html">Transmission and gearing</a></li>
    <li><a href="supercharger-pulley-calculator.html">Supercharger pulleys</a></li>
    <li><a href="index.html">All calculators</a></li>
</ul>
"""
    return fill(
        NARROW_TEMPLATE,
        TITLE=esc("Page not found | DragCalculators.com"),
        DESCRIPTION=esc("That calculator page moved into the main tool."),
        CANONICAL=esc(f"{ORIGIN}/404.html"),
        VERIFICATION=VERIFICATION,
        ORIGIN=ORIGIN,
        ANALYTICS=analytics_tag(),
        BANNER=SITE_BANNER,
        CONTENT=content,
        FOOTER=footer(),
    )


KEEP_HTML = {
    "index.html",
    "contact.html",
    "privacy.html",
    "404.html",
    "google9e7c88791a3f2f72.html",
}


def remove_stale_pages(pages):
    keep = set(KEEP_HTML)
    keep.update(f"{page['slug']}.html" for page in pages)
    removed = []
    for name in os.listdir(ROOT):
        if name.endswith(".html") and name not in keep:
            os.remove(os.path.join(ROOT, name))
            removed.append(name)
    return removed


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
        path = "/" if filename == "index.html" else f"/{filename}"
        loc = esc(f"{ORIGIN}{path}")
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
    missing_ls = [page["slug"] for page in pages if page["category"] == "LS" and page["slug"] not in LS_PRESETS]
    if missing_ls:
        raise SystemExit("LS pages missing presets: " + ", ".join(missing_ls))
    missing_n2o = [page["slug"] for page in pages if page["category"] == "Nitrous" and page["slug"] not in N2O_PRESETS]
    if missing_n2o:
        raise SystemExit("Nitrous pages missing presets: " + ", ".join(missing_n2o))
    missing_shock = [page["slug"] for page in pages if page["category"] == "Shock" and page["slug"] not in SHOCK_PRESETS]
    if missing_shock:
        raise SystemExit("Shock pages missing presets: " + ", ".join(missing_shock))
    missing_cv = [page["slug"] for page in pages if page["category"] == "Converter" and page["slug"] not in CV_PRESETS]
    if missing_cv:
        raise SystemExit("Converter pages missing presets: " + ", ".join(missing_cv))
    hubs = [page for page in pages if page["role"] == "hub"]
    hubs_by_category = {page["category"]: page for page in hubs}
    global SITE_BANNER
    SITE_BANNER = site_banner(search_records(pages, hubs_by_category))
    if not any(page["slug"] == "transmission-shift-recovery-calculator" for page in pages):
        raise SystemExit("CSV is missing transmission-shift-recovery-calculator, which the master hub embeds")

    write("styles.css", STYLES)
    write("google9e7c88791a3f2f72.html", "google-site-verification: google9e7c88791a3f2f72.html\n")
    write("contact.html", contact_page())
    write("privacy.html", privacy_page())
    write("404.html", not_found_page())
    write("index.html", index_page(pages, hubs))
    for page in pages:
        write(f"{page['slug']}.html", fill(PAGE_TEMPLATE, **page_tokens(page, pages, hubs, hubs_by_category)))
    write("sitemap.xml", sitemap(pages))
    removed = remove_stale_pages(pages)

    counts = {}
    for page in pages:
        counts[page["category"]] = counts.get(page["category"], 0) + 1
    summary = ", ".join(f"{category} {counts[category]}" for category in sorted(counts))
    print(f"Built {len(pages)} calculator pages ({len(hubs)} hubs) from pseo_pages_list.csv")
    print(summary)
    print(f"Sitemap URLs: {len(pages) + 3}")
    if removed:
        print(f"Removed {len(removed)} stale calculator pages")


if __name__ == "__main__":
    main()
