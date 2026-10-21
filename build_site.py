import os
import csv

output_dir = "."

with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages = list(reader)

pages_created = 0

for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]
    gear = row["rear_gear"]
    tire = row["tire_diameter"]

    if category in ["Transmission", "RearGear"]:
        primary_title = "Transmission Shift Recovery & Gear Drop Calculator"
        formula_text = "Overall Ratio = Transmission Ratio × Rear Gear Ratio<br>Shift Speed = (Shift RPM × Tire Diameter) / (Overall Ratio × 336)"
        faqs = """
            <div class="faq-item">
                <h4>How is shift recovery RPM calculated?</h4>
                <p>Shift recovery is determined by multiplying your shift RPM by the ratio of the upcoming higher gear divided by the current gear.</p>
            </div>
            <div class="faq-item">
                <h4>Why does gear drop matter?</h4>
                <p>Keeping your engine operating inside its peak power band after a shift prevents acceleration lag down the track.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans">
                        <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                        <option value="th350" selected>TH350 (2.52 / 1.52 / 1.00)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                    </select>
                </div>
                <div>
                    <label>Max Shift RPM</label>
                    <input type="number" id="max-rpm" value="7500" step="100">
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
                <thead><tr><th>Gear</th><th>Static Ratio</th><th>Overall Ratio</th><th>Speed at Shift Point</th><th>RPM Drop / Recovery</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        tool_script = """
        const ratios = { powerglide: [1.76, 1.00], th350: [2.52, 1.52, 1.00], th400: [2.48, 1.48, 1.00] };
        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.52, 1.52, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let rollout = (tire * Math.PI).toFixed(1);
            
            let resEl = document.getElementById("results");
            if(resEl) resEl.innerHTML = `<strong>Analysis:</strong> Tire Rollout: ${rollout} in | 1st Gear Ratio: ${(rat[0] * gear).toFixed(2)}:1`;

            let tbody = document.getElementById("gear-body");
            if(tbody) {
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? Math.round(rpm * (rat[i+1] / rat[i])) : "Crossing Line";
                    tbody.innerHTML += `<tr><td>Gear ${i+1}</td><td>${rat[i].toFixed(2)}</td><td>${overall.toFixed(2)}</td><td>${speed.toFixed(1)} MPH</td><td>Drop to ${drop} RPM</td></tr>`;
                }
            }
        }
        ["trans", "max-rpm", "tire-dia", "rear-gear"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbocharger Airflow & Thermodynamic Calculator"
        formula_text = "Reference CFM = (CID × RPM × VE) / 3456<br>Pressure Ratio = Manifold PSIA / Atmospheric PSIA<br>Corrected Airflow (lb/min) = Corrected CFM × 0.0765"
        faqs = """
            <div class="faq-item">
                <h4>Why must manifold pressure be entered as absolute pressure?</h4>
                <p>Pressure ratio compares absolute thermodynamic states; gauge boost omits atmospheric pressure (14.7 PSIA).</p>
            </div>
            <div class="faq-item">
                <h4>How do I estimate volumetric efficiency (VE)?</h4>
                <p>Standard forced-induction race engines typically range from 85% to 95% VE depending on cylinder head flow and camshaft profile.</p>
            </div>
        """
        primary_tool_html = """
            <div class="grid-2">
                <div>
                    <label>Engine Displacement (CID)</label>
                    <input type="number" id="cid" value="355" step="1">
                </div>
                <div>
                    <label>Engine Speed (RPM)</label>
                    <input type="number" id="rpm" value="6500" step="100">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Volumetric Efficiency (%)</label>
                    <input type="number" id="ve" value="90" step="1">
                </div>
                <div>
                    <label>Atmospheric Pressure (PSIA)</label>
                    <input type="number" id="atm" value="14.7" step="0.1">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Manifold Absolute Pressure (PSIA)</label>
                    <input type="number" id="map" value="29.7" step="0.1">
                </div>
                <div>
                    <label>Intake-Air Temperature (°F)</label>
                    <input type="number" id="iat" value="120" step="1">
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to calculate reference CFM and airflow rate.</div>
        """
        tool_script = """
        function calcTool() {
            let cid = parseFloat(document.getElementById("cid").value) || 355;
            let rpm = parseFloat(document.getElementById("rpm").value) || 6500;
            let ve = (parseFloat(document.getElementById("ve").value) || 90) / 100.0;
            let atm = parseFloat(document.getElementById("atm").value) || 14.7;
            let mapVal = parseFloat(document.getElementById("map").value) || 29.7;
            let iat = parseFloat(document.getElementById("iat").value) || 120;

            let refCfm = (cid * rpm * ve) / 3456;
            let pressRatio = mapVal / atm;
            let tempCorr = 518.67 / (iat + 459.67);
            let correctedCfm = refCfm * pressRatio * tempCorr;
            let lbMin = correctedCfm * 0.0765;

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Airflow Results:</strong> Reference CFM: <strong>${Math.round(refCfm)} CFM</strong> | Pressure Ratio: <strong>${pressRatio.toFixed(2)}:1</strong> | Airflow Rate: <strong>${lbMin.toFixed(1)} lb/min</strong>`;
            }
        }
        ["cid", "rpm", "ve", "atm", "map", "iat"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    else:
        primary_title = "Supercharger Pulley Ratio & Boost Pressure Calculator"
        formula_text = "Pulley Ratio = Crank Pulley Diameter / Blower Pulley Diameter<br>Estimated Boost = Pulley Ratio × 5.2 × Boost Factor"
        faqs = """
            <div class="faq-item">
                <h4>How do I increase boost?</h4>
                <p>You can increase boost by installing a smaller blower pulley or a larger crankshaft pulley to overdrive the supercharger speed.</p>
            </div>
        """
        primary_tool_html = """
            <div class="grid-2">
                <div>
                    <label>Crankshaft Pulley Diameter (inches)</label>
                    <input type="number" id="crank-dia" value="8.0" step="0.1">
                </div>
                <div>
                    <label>Blower Pulley Diameter (inches)</label>
                    <input type="number" id="blower-dia" value="3.0" step="0.1">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Max Crank RPM</label>
                    <input type="number" id="crank-rpm" value="6500" step="100">
                </div>
                <div>
                    <label>Base Boost Multiplier Factor</label>
                    <input type="number" id="boost-fac" value="1.45" step="0.05">
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to calculate pulley ratio and estimated boost pressure.</div>
        """
        tool_script = """
        function calcTool() {
            let crank = parseFloat(document.getElementById("crank-dia").value) || 8.0;
            let blower = parseFloat(document.getElementById("blower-dia").value) || 3.0;
            let rpm = parseFloat(document.getElementById("crank-rpm").value) || 6500;
            let factor = parseFloat(document.getElementById("boost-fac").value) || 1.45;
            
            let ratio = crank / blower;
            let estBoost = (ratio * 5.2 * factor).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) resEl.innerHTML = `<strong>Supercharger Results:</strong> Pulley Ratio: <strong>${ratio.toFixed(2)}:1</strong> | Estimated Boost: <strong>${estBoost} PSI</strong>`;
        }
        ["crank-dia", "blower-dia", "crank-rpm", "boost-fac"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{target_keyword} | Ultimate Drag Racing Master Suite</title>
    <script src="calculator-core.js"></script>
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
        .content-box, .sidebar-box {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 25px;
        }}
        .content-box h3, .sidebar-box h3 {{
            color: var(--accent-red);
            font-size: 0.95rem;
            text-transform: uppercase;
            margin-top: 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            letter-spacing: 0.5px;
        }}
        .sponsor-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        .sponsor-list li {{
            padding: 8px 0;
            border-bottom: 1px dashed var(--border-color);
        }}
        .sponsor-list li:last-child {{ border-bottom: none; }}
        .sponsor-list li a {{
            color: var(--text-muted);
            text-decoration: none;
            display: block;
            transition: color 0.2s;
        }}
        .sponsor-list li a:hover {{
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
            font-size: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
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
            gap: 15px;
            margin-bottom: 12px;
        }}
        @media (max-width: 500px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        label {{
            display: block;
            margin-bottom: 4px;
            font-weight: 600;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        input, select {{
            width: 100%;
            padding: 10px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.9rem;
        }}
        input:focus, select:focus {{
            outline: none;
            border-color: var(--accent-red);
            box-shadow: 0 0 5px var(--accent-glow);
        }}
        .results-box {{
            margin-top: 20px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 15px;
            border-radius: 6px;
            font-size: 0.95rem;
        }}
        .formula-content {{
            font-family: monospace;
            color: #10b981;
            font-size: 0.95rem;
            background: var(--input-bg);
            padding: 12px;
            border-radius: 6px;
        }}
        .faq-item {{
            margin-bottom: 15px;
        }}
        .faq-item:last-child {{ margin-bottom: 0; }}
        .faq-item h4 {{
            margin: 0 0 5px 0;
            font-size: 0.9rem;
            color: var(--text-main);
        }}
        .faq-item p {{
            margin: 0;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        table {{
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.85rem;
        }}
        th {{
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: var(--accent-red);
            text-decoration: none;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div style="max-width: 1200px; margin: 0 auto;">
        <a href="index.html" class="back-link">&larr; Back to Master Calculators Hub</a>
    </div>

    <div class="layout-grid">
        <!-- Sticky Left Calculator -->
        <div class="sticky-calculator">
            <div class="master-header">
                <h1>{primary_title}</h1>
                <p>{target_keyword} &mdash; Track Tuning Engine</p>
            </div>

            {primary_tool_html}
        </div>

        <!-- Scrolling Right Column -->
        <div class="content-column">
            <div class="content-box">
                <h3>Formula Breakdown</h3>
                <div class="formula-content">{formula_text}</div>
            </div>

            <div class="content-box">
                <h3>Frequently Asked Questions</h3>
                {faqs}
            </div>

            <div class="sidebar-box">
                <h3>Featured Partners</h3>
                <ul class="sponsor-list">
                    <li><a href="https://www.summitracing.com" target="_blank">Summit Racing Equipment</a></li>
                    <li><a href="https://www.holley.com" target="_blank">Holley Performance</a></li>
                    <li><a href="https://vpracingfuels.com" target="_blank">VP Racing Fuels</a></li>
                    <li><a href="https://www.mickeythompsontires.com" target="_blank">Mickey Thompson Tires</a></li>
                </ul>
            </div>

            <div class="sidebar-box" style="text-align: center;">
                <h3>Advertisement</h3>
                <div style="background: var(--input-bg); height: 250px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 0.85rem; border-radius: 6px;">
                    300 x 250 Ad Slot
                </div>
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

print(f"Successfully generated {pages_created} sticky pages with professional math models!")