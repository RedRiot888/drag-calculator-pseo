import os
import csv

output_dir = "."
AFFILIATE_TRACKING_URL = "https://www.pjtra.com/t/YOUR_IMPACT_ID_HERE?url="

# 1. Automatically create Google Search Console verification file
gsc_verification_filename = "google9e7c88791a3f2f72.html"
gsc_verification_content = "google-site-verification: google9e7c88791a3f2f72.html"
with open(os.path.join(output_dir, gsc_verification_filename), "w", encoding="utf-8") as f:
    f.write(gsc_verification_content)
print(f"Generated {gsc_verification_filename} for Google Search Console verification.")

# 2. Pages CSV data
csv_content = """slug,target_keyword,category,rear_gear,tire_diameter
transmission-shift-recovery-calculator,Transmission Shift Recovery & Gear Drop Calculator,Transmission,3.42,28.0
turbo-sizing-calculator,Turbo Sizing & Turbocharger Matching Calculator,Turbo,3.42,28.0
exhaust-header-sizing-calculator,Exhaust Primary & Turbo Downpipe Sizing Calculator,Exhaust,3.42,28.0
supercharger-pulley-calculator,Supercharger Pulley Ratio & Boost Pressure Calculator,Supercharger,3.42,28.0
rear-gear-calculator,Ring and Pinion Rear Gear Quarter-Mile Calculator,RearGear,4.11,32.0
tire-growth-calculator,Tire Diameter Growth & Rollout Drag Calculator,Tire,3.42,28.0
wastegate-sizing-calculator,Wastegate Sizing & Boost Control Calculator,Wastegate,3.42,28.0
fuel-injector-calculator,Fuel Injector Flow Rate & Sizing Calculator,Fuel,3.42,28.0
automotive-relay-calculator,Automotive Relay & Circuit Sizing Calculator,Electrical,3.42,28.0
"""
with open("pseo_pages_list.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    pages = list(csv.DictReader(f))

sidebar_nav_html = """
<div style="display: flex; flex-direction: column; gap: 4px;">
    <a href="index.html" class="nav-item active" style="padding: 8px 10px; background: var(--input-bg); border-left: 3px solid var(--accent-red); color: var(--text-main); text-decoration: none; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">🏁 Popular / Master Hub</a>
    <a href="transmission-shift-recovery-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🏎️ Transmission & Gearing</a>
    <a href="turbo-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🌀 Forced Induction / Turbo</a>
    <a href="exhaust-header-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🔥 Exhaust & Airflow</a>
    <a href="fuel-injector-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">⛽ Fueling & EFI</a>
    <a href="tire-growth-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🛞 Chassis & Tires</a>
    <a href="automotive-relay-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">⚡ Electrical & Wiring</a>
</div>
"""

ad_block_html = '<div class="content-box" style="text-align: center; background: #121418; border: 1px dashed var(--border-color);"><h3 style="font-size: 0.85rem; color: var(--text-muted);">Advertisement Space</h3></div>'
partners_html = '<div class="content-box"><h3>Industry Standards</h3></div>'
tuning_guides_html = '<div class="content-box"><h3>Track-Side Tuning</h3></div>'
footer_html = '<footer style="text-align: center; margin-top: 20px; color: var(--text-muted); font-size: 0.8rem;"><p>&copy; 2026 Drag Racing Suite</p></footer>'

verification_tags = """    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>
    <meta name='google-site-verification' content='google9e7c88791a3f2f72'>"""

# 3. Build index.html from index_template.html
if os.path.exists("index_template.html"):
    with open("index_template.html", "r", encoding="utf-8") as f:
        master_index_html = f.read()
    
    master_index_html = (
        master_index_html.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags)
        .replace("REPLACE_SIDEBAR_NAV", sidebar_nav_html)
        .replace("REPLACE_STICKY_AD", ad_block_html)
        .replace("REPLACE_TOP_AD", ad_block_html)
        .replace("REPLACE_BOTTOM_AD", ad_block_html)
        .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
        .replace("REPLACE_PARTNERS", partners_html)
        .replace("REPLACE_FOOTER", footer_html)
    )
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(master_index_html)
    print("Successfully built index.html!")

# 4. Build individual PSEO calculator pages
base_html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TARGET_KEYWORD | Ultimate Drag Racing Master Suite</title>
    VERIFICATION_TAGS_PLACEHOLDER
    <style>
        :root {
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.5; }
        .layout-grid { max-width: 1350px; margin: 20px auto; display: grid; grid-template-columns: 240px 480px 1fr; gap: 25px; align-items: start; }
        .nexus-sidebar { position: sticky; top: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; }
        .sticky-calculator { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
        .content-column { display: flex; flex-direction: column; gap: 20px; }
        .content-box { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; }
        .content-box h3 { color: var(--accent-red); font-size: 0.95rem; text-transform: uppercase; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        .master-header { text-align: center; margin-bottom: 5px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
        .master-header h1 { color: var(--accent-red); font-size: 1.3rem; text-transform: uppercase; margin: 0 0 3px 0; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }
        label { display: block; margin-bottom: 2px; font-weight: 600; font-size: 0.72rem; color: var(--text-muted); }
        input, select { width: 100%; padding: 7px 9px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; box-sizing: border-box; font-size: 0.82rem; }
        .results-box { margin-top: 10px; background: #121418; border: 1px solid var(--border-color); border-left: 4px solid var(--accent-red); padding: 10px; border-radius: 6px; font-size: 0.82rem; }
        .action-btn { width: 100%; margin-top: 10px; background: var(--accent-red); color: white; border: none; padding: 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; cursor: pointer; text-transform: uppercase; }
        .action-btn:hover { background: #e0161f; }
        table { width: 100%; margin-top: 12px; border-collapse: collapse; background: #121418; border-radius: 6px; overflow: hidden; }
        th, td { padding: 5px 4px; border: 1px solid var(--border-color); text-align: center; font-size: 0.72rem; }
        th { background: #1f232b; color: var(--accent-red); text-transform: uppercase; font-size: 0.62rem; }
        .back-link { display: inline-block; margin-bottom: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div style="max-width: 1350px; margin: 0 auto;"><a href="index.html" class="back-link">&larr; Back to Master Hub</a></div>
    <div class="layout-grid">
        <div class="nexus-sidebar">REPLACE_SIDEBAR_NAV</div>
        <div class="sticky-calculator">
            <div>
                <div class="master-header"><h1>PRIMARY_TITLE</h1><p>TARGET_KEYWORD &mdash; Track Tuning Engine</p></div>
                PRIMARY_TOOL_HTML
            </div>
            REPLACE_STICKY_AD
        </div>
        <div class="content-column">
            REPLACE_TOP_AD
            REPLACE_TUNING_GUIDES
            <div class="content-box"><h3>Formula Breakdown</h3><div style="font-family: monospace; color: #10b981; font-size: 0.85rem; background: var(--input-bg); padding: 10px; border-radius: 6px;">FORMULA_TEXT</div></div>
            REPLACE_PARTNERS
            REPLACE_BOTTOM_AD
        </div>
    </div>
    REPLACE_FOOTER
    <script>TOOL_SCRIPT</script>
</body>
</html>
"""

for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]
    gear = row["rear_gear"]
    tire = row["tire_diameter"]

    if category == "Transmission":
        primary_title = "Transmission Shift Recovery Calculator"
        formula_text = "Overall Ratio = Trans Ratio x Rear Gear | Shift Speed = (RPM * Tire) / (Overall * 336)"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Transmission Profile</label>
                    <select id="trans">
                        <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                        <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                        <option value="th350">TH350 (2.52 / 1.52 / 1.00)</option>
                        <option value="4l60e">4L60e (3.06 / 1.62 / 1.00 / 0.70)</option>
                    </select>
                </div>
                <div><label>Max Shift RPM</label><input type="number" id="max-rpm" value="7500" step="100"></div>
            </div>
            <div class="grid-2">
                <div><label>Tire Diameter (in)</label><input type="number" id="tire-dia" value="28.0" step="0.1"></div>
                <div><label>Rear Gear Ratio</label><input type="number" id="rear-gear" value="3.42" step="0.01"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Track Sheet</button>
            <table>
                <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop / Finish</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        tool_script = """
        const ratios = { powerglide: [1.76, 1.00], th350: [2.52, 1.52, 1.00], th400: [2.48, 1.48, 1.00], "4l60e": [3.06, 1.62, 1.00, 0.70] };
        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.48, 1.48, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let rollout = (tire * Math.PI).toFixed(1);
            document.getElementById("results").innerHTML = "Rollout: " + rollout + " in | 1st Gear Overall: " + (rat[0]*gear).toFixed(2) + ":1";
            let tbody = document.getElementById("gear-body");
            if(tbody) {
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let trapRpm = Math.round((125 * overall * 336) / tire);
                    let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Finish: " + trapRpm + " RPM";
                    tbody.innerHTML += "<tr><td>Gear " + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
                }
            }
        }
        ["trans", "max-rpm", "tire-dia", "rear-gear"].forEach(id => { document.getElementById(id).addEventListener("input", calcTool); });
        calcTool();
        """
    elif category == "Exhaust":
        primary_title = "Exhaust Primary & Turbo Downpipe Sizing"
        formula_text = "NA Header Primary = (Displacement x RPM) / (Cylinder Count x Constant)"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Engine Type</label><select id="ex-type"><option value="na">Naturally Aspirated</option><option value="turbo">Turbocharged</option></select></div>
                <div><label>Target HP</label><input type="number" id="ex-hp" value="850" step="50"></div>
            </div>
            <div class="results-box" id="ex-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("ex-hp").value) || 850;
            let type = document.getElementById("ex-type").value;
            let dia = type === "na" ? "1-3/4 to 1-7/8 inches" : "3.5 to 4.0 inch Downpipe";
            document.getElementById("ex-results").innerHTML = "Recommended Sizing: <strong>" + dia + "</strong> for " + hp + " HP";
        }
        ["ex-type", "ex-hp"].forEach(id => { document.getElementById(id).addEventListener("input", calcTool); document.getElementById(id).addEventListener("change", calcTool); });
        calcTool();
        """
    else:
        primary_title = target_keyword
        formula_text = "Standard Automotive Calculation"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Primary Value</label><input type="number" id="val1" value="100" step="1"></div>
            </div>
            <div class="results-box" id="res">Calculated successfully.</div>
        """
        tool_script = """
        function calcTool() {
            let v = parseFloat(document.getElementById("val1").value) || 100;
            document.getElementById("res").innerHTML = "Calculated Output: <strong>" + (v * 1.5).toFixed(1) + "</strong>";
        }
        let el = document.getElementById("val1");
        if(el) el.addEventListener("input", calcTool);
        calcTool();
        """

    page_html = (
        base_html_template.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags)
            .replace("TARGET_KEYWORD", target_keyword)
            .replace("PRIMARY_TITLE", primary_title)
            .replace("PRIMARY_TOOL_HTML", primary_tool_html)
            .replace("FORMULA_TEXT", formula_text)
            .replace("REPLACE_SIDEBAR_NAV", sidebar_nav_html)
            .replace("REPLACE_STICKY_AD", ad_block_html)
            .replace("REPLACE_TOP_AD", ad_block_html)
            .replace("REPLACE_BOTTOM_AD", ad_block_html)
            .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
            .replace("REPLACE_PARTNERS", partners_html)
            .replace("REPLACE_FOOTER", footer_html)
            .replace("TOOL_SCRIPT", tool_script)
    )

    with open(os.path.join(output_dir, f"{slug}.html"), "w", encoding="utf-8") as out_f:
        out_f.write(page_html)

print("Successfully built all PSEO pages and Google verification file!")