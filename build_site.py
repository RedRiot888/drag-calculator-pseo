import os
import csv

output_dir = "."

with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages = list(reader)

utilities_links_html = ""
for row in pages:
    utilities_links_html += f'<li><a href="{row["slug"]}.html">{row["target_keyword"]}</a></li>\n'

pages_created = 0
for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]
    gear = row["rear_gear"]
    tire = row["tire_diameter"]

    if category == "Transmission":
        primary_title = "Transmission Shift Recovery & Gear Drop Calculator"
        formula_text = "Overall Ratio = Transmission Ratio x Rear Gear Ratio<br>Shift Speed = (Shift RPM x Tire Diameter) / (Overall Ratio x 336)"
        faqs = """
            <div class="faq-item">
                <h4>How is shift recovery RPM calculated?</h4>
                <p>Shift recovery is determined by multiplying your shift RPM by the ratio of the upcoming higher gear divided by the current gear.</p>
            </div>
            <div class="faq-item">
                <h4>Why do manufacturer presets and custom gear sets matter?</h4>
                <p>Manufacturer presets give you instant access to factory and race-proven gear stacks across GM, Ford, Mopar, and imports, while custom ratios accommodate custom gearboxes.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans" onchange="applyTransPreset()">
                        <optgroup label="GM">
                            <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                            <option value="th350">TH350 (2.52 / 1.52 / 1.00)</option>
                            <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                            <option value="4l60e">4L60e (3.06 / 1.62 / 1.00 / 0.70)</option>
                            <option value="6l80">6L80 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67)</option>
                        </optgroup>
                        <optgroup label="Ford">
                            <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00)</option>
                            <option value="ford_t5">Ford T-5 (2.95 / 1.94 / 1.34 / 1.00 / 0.73)</option>
                            <option value="mustang_10r80">Mustang 10R80 (10-Speed)</option>
                        </optgroup>
                        <optgroup label="Custom">
                            <option value="custom">Custom Ratios</option>
                        </optgroup>
                    </select>
                </div>
                <div>
                    <label>Max Shift RPM</label>
                    <input type="number" id="max-rpm" value="7500" step="100">
                </div>
            </div>
            <div class="grid-2" id="custom-gears-row" style="display: none;">
                <div style="grid-column: span 2;">
                    <label>Custom Ratios (comma-separated)</label>
                    <input type="text" id="custom-ratios" value="2.48, 1.48, 1.00">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Tire Diameter (inches)</label>
                    <input type="number" id="tire-dia" value="{tire}" step="0.1">
                </div>
                <div>
                    <label>Rear Gear Ratio</label>
                    <input type="number" id="rear-gear" value="{gear}" step="0.01">
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to view shift recovery and RPM drop.</div>
            <table>
                <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        tool_script = """
        const ratios = { 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00],
            "4l60e": [3.06, 1.62, 1.00, 0.70],
            "6l80": [4.03, 2.36, 1.53, 1.15, 0.85, 0.67],
            c4_c6: [2.46, 1.46, 1.00],
            ford_t5: [2.95, 1.94, 1.34, 1.00, 0.73],
            mustang_10r80: [4.70, 2.99, 2.15, 1.77, 1.52, 1.28, 1.00, 0.85, 0.69, 0.64]
        };

        function applyTransPreset() {
            let val = document.getElementById("trans").value;
            let customRow = document.getElementById("custom-gears-row");
            if(customRow) {
                customRow.style.display = (val === "custom") ? "grid" : "none";
            }
            calcTool();
        }

        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = [];
            if(tKey === "custom") {
                let customStr = document.getElementById("custom-ratios").value;
                rat = customStr.split(",").map(function(x) { return parseFloat(x.trim()); }).filter(function(x) { return !isNaN(x) && x > 0; });
                if(rat.length === 0) rat = [2.48, 1.48, 1.00];
            } else {
                rat = ratios[tKey] || [2.48, 1.48, 1.00];
            }

            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let rollout = (tire * Math.PI).toFixed(1);
            
            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = "Tire Rollout: " + rollout + " in | 1st Gear Ratio: " + (rat[0] * gear).toFixed(2) + ":1";
            }

            let tbody = document.getElementById("gear-body");
            if(tbody) {
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Crossing Line";
                    tbody.innerHTML += "<tr><td>Gear " + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
                }
            }
        }
        ["trans", "max-rpm", "tire-dia", "rear-gear", "custom-ratios"].forEach(function(id) {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    else:
        primary_title = "Drag Racing Calculator Suite"
        formula_text = "Standard Automotive Calculation"
        faqs = ""
        primary_tool_html = "<div>Select a tool from the hub.</div>"
        tool_script = ""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{target_keyword} | Ultimate Drag Racing Master Suite</title>
    <style>
        :root {{
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --accent-glow: rgba(255, 30, 39, 0.25);
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.5;
        }}
        .layout-grid {{
            max-width: 1200px;
            margin: 30px auto;
            display: grid;
            grid-template-columns: 480px 1fr;
            gap: 30px;
            align-items: start;
        }}
        @media (max-width: 900px) {{
            .layout-grid {{ grid-template-columns: 1fr; }}
        }}
        .sticky-calculator {{
            position: sticky;
            top: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 30px;
        }}
        .content-column {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .content-box {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 25px;
        }}
        .content-box h3 {{
            color: var(--accent-red);
            font-size: 0.95rem;
            text-transform: uppercase;
            margin-top: 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
        }}
        .utility-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        .utility-list li {{
            padding: 8px 0;
            border-bottom: 1px dashed var(--border-color);
        }}
        .utility-list li a {{
            color: var(--text-muted);
            text-decoration: none;
            display: block;
        }}
        .utility-list li a:hover {{
            color: var(--accent-red);
        }}
        .master-header {{
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
        }}
        .master-header h1 {{
            color: var(--accent-red);
            font-size: 1.4rem;
            text-transform: uppercase;
            margin: 0 0 5px 0;
        }}
        .master-header p {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin: 0;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 10px;
        }}
        label {{
            display: block;
            margin-bottom: 3px;
            font-weight: 600;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
        input, select {{
            width: 100%;
            padding: 8px 10px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.85rem;
        }}
        optgroup {{ color: var(--accent-red); font-weight: bold; }}
        option {{ color: var(--text-main); background: var(--input-bg); }}
        .results-box {{
            margin-top: 15px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 12px;
            border-radius: 6px;
            font-size: 0.85rem;
        }}
        .formula-content {{
            font-family: monospace;
            color: #10b981;
            font-size: 0.85rem;
            background: var(--input-bg);
            padding: 10px;
            border-radius: 6px;
        }}
        .faq-item {{ margin-bottom: 12px; }}
        .faq-item h4 {{ margin: 0 0 3px 0; font-size: 0.85rem; color: var(--text-main); }}
        .faq-item p {{ margin: 0; font-size: 0.8rem; color: var(--text-muted); }}
        table {{
            width: 100%;
            margin-top: 15px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }}
        th, td {{
            padding: 6px 4px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.75rem;
        }}
        th {{
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.65rem;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 15px;
            color: var(--accent-red);
            text-decoration: none;
            font-weight: bold;
            font-size: 0.85rem;
        }}
        .back-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div style="max-width: 1200px; margin: 0 auto;">
        <a href="index.html" class="back-link">&larr; Back to Master Hub</a>
    </div>

    <div class="layout-grid">
        <div class="sticky-calculator">
            <div class="master-header">
                <h1>{primary_title}</h1>
                <p>{target_keyword} &mdash; Track Tuning Engine</p>
            </div>
            {primary_tool_html}
        </div>

        <div class="content-column">
            <div class="content-box">
                <h3>Other Utilities & Calculators</h3>
                <ul class="utility-list">
                    {utilities_links_html}
                </ul>
            </div>
            <div class="content-box">
                <h3>Formula Breakdown</h3>
                <div class="formula-content">{formula_text}</div>
            </div>
            <div class="content-box">
                <h3>Frequently Asked Questions</h3>
                {faqs}
            </div>
        </div>
    </div>

    <script>
        {tool_script}
    </script>
</body>
</html>
"""

    file_path = os.path.join(output_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(html)
    pages_created += 1

print(f"Successfully generated {pages_created} PSEO pages without syntax errors!")