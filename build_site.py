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

    # Customize content based on category
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
    elif category == "Supercharger":
        primary_title = "Supercharger Pulley Ratio & Boost Pressure Calculator"
        formula_text = "Pulley Ratio = Crank Pulley Diameter / Blower Pulley Diameter<br>Estimated Boost = Pulley Ratio × 5.2 × Boost Factor"
        faqs = """
            <div class="faq-item">
                <h4>How do I increase boost?</h4>
                <p>You can increase boost by installing a smaller blower pulley or a larger crankshaft pulley to overdrive the supercharger speed.</p>
            </div>
            <div class="faq-item">
                <h4>Does belt slip affect boost?</h4>
                <p>Yes, belt slip under high load reduces effective blower RPM and causes a drop in peak boost pressure.</p>
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
            let blowerRpm = rpm * ratio;
            let estBoost = (ratio * 5.2 * factor).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) resEl.innerHTML = `<strong>Supercharger Results:</strong> Pulley Ratio: <strong>${ratio.toFixed(2)}:1</strong> | Blower Speed: <strong>${Math.round(blowerRpm)} RPM</strong> | Estimated Boost: <strong>${estBoost} PSI</strong>`;
        }
        ["crank-dia", "blower-dia", "crank-rpm", "boost-fac"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbo Sizing, Compressor Map & Boost Calculator"
        formula_text = "Airflow (lbs/min) = (Horsepower × BSFC) / 6.0<br>Pressure Ratio = (Boost PSI + 14.7) / 14.7"
        faqs = """
            <div class="faq-item">
                <h4>What BSFC value should I use?</h4>
                <p>Standard gasoline engines typically use 0.60, while E85 setups use ~0.85 and methanol setups use ~1.20.</p>
            </div>
            <div class="faq-item">
                <h4>How do I read a compressor map?</h4>
                <p>Match your required airflow (lbs/min) on the vertical axis and pressure ratio on the horizontal axis to see if the turbo operates in peak efficiency.</p>
            </div>
        """
        primary_tool_html = """
            <div class="grid-2">
                <div>
                    <label>Target Horsepower (WHP)</label>
                    <input type="number" id="hp" value="1000" step="50">
                </div>
                <div>
                    <label>Fuel Type / BSFC</label>
                    <select id="fuel">
                        <option value="0.60">Gasoline (BSFC 0.60)</option>
                        <option value="0.85">E85 / Alcohol (BSFC 0.85)</option>
                        <option value="1.20">Methanol (BSFC 1.20)</option>
                    </select>
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Target Boost Pressure (PSI)</label>
                    <input type="number" id="boost" value="25" step="1">
                </div>
                <div>
                    <label>Turbo Configuration</label>
                    <select id="config">
                        <option value="1">Single Turbo</option>
                        <option value="2">Twin Turbos (Split Flow)</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters to calculate required airflow (lbs/min) and pressure ratio.</div>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("hp").value) || 1000;
            let bsfc = parseFloat(document.getElementById("fuel").value) || 0.60;
            let boost = parseFloat(document.getElementById("boost").value) || 25;
            let config = parseInt(document.getElementById("config").value) || 1;

            let airflow = (hp * bsfc) / 6.0;
            let perTurbo = airflow / config;
            let pressureRatio = ((boost + 14.7) / 14.7).toFixed(2);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Turbo Results:</strong> Total Airflow: <strong>${airflow.toFixed(1)} lbs/min</strong> (${perTurbo.toFixed(1)} lbs/min per turbo) | Pressure Ratio: <strong>${pressureRatio}:1</strong>`;
            }
        }
        ["hp", "fuel", "boost", "config"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    else:
        primary_title = "Tire Diameter Growth & Rollout Drag Calculator"
        formula_text = "Dynamic Diameter = Static Diameter × (1 + (Growth % / 100))<br>Rollout = Diameter × π"
        faqs = """
            <div class="faq-item">
                <h4>Why do drag tires grow at high speed?</h4>
                <p>Centrifugal force at 150+ MPH causes bias-ply and radial slick treads to expand outward, increasing effective rollout and altering finish line RPM.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Static Tire Diameter (inches)</label>
                    <input type="number" id="static-dia" value="{tire}" step="0.1">
                </div>
                <div>
                    <label>Trap Speed (MPH)</label>
                    <input type="number" id="trap-speed" value="150" step="1">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Estimated Growth Factor (%)</label>
                    <input type="number" id="growth-fac" value="4.5" step="0.1">
                </div>
                <div>
                    <label>Rear Gear Ratio</label>
                    <input type="number" id="rear-gear" value="{gear}" step="0.01">
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to calculate high-speed growth and effective rollout.</div>
        """
        tool_script = """
        function calcTool() {
            let staticDia = parseFloat(document.getElementById("static-dia").value) || 28;
            let trap = parseFloat(document.getElementById("trap-speed").value) || 150;
            let growth = parseFloat(document.getElementById("growth-fac").value) || 4.5;

            let dynamicDia = staticDia * (1 + (growth / 100));
            let staticRollout = (staticDia * Math.PI).toFixed(1);
            let dynamicRollout = (dynamicDia * Math.PI).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Tire Results:</strong> Static Rollout: <strong>${staticRollout} in</strong> | High-Speed Growth Diameter: <strong>${dynamicDia.toFixed(2)} in</strong> | Dynamic Rollout: <strong>${dynamicRollout} in</strong>`;
            }
        }
        ["static-dia", "trap-speed", "growth-fac", "rear-gear"].forEach(id => {
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
            grid-template-columns: 1fr 300px;
            gap: 30px;
        }}
        @media (max-width: 900px) {{
            .layout-grid {{ grid-template-columns: 1fr; }}
        }}
        .master-container {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 35px;
        }}
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .sidebar-box {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }}
        .sidebar-box h3 {{
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
            padding: 6px 0;
            border-bottom: 1px dashed var(--border-color);
        }}
        .sponsor-list li:last-child {{ border-bottom: none; }}
        .sponsor-list li::before {{
            content: "\\2022";
            color: var(--accent-red);
            font-weight: bold;
            display: inline-block;
            width: 1em;
        }}
        .master-header {{
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }}
        .master-header h1 {{
            color: var(--accent-red);
            font-size: 1.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 0 0 5px 0;
        }}
        .master-header p {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin: 0;
        }}
        .section-title {{
            color: var(--accent-red);
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 25px 0 15px 0;
            border-left: 3px solid var(--accent-red);
            padding-left: 10px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
        }}
        @media (max-width: 768px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        label {{
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        input, select {{
            width: 100%;
            padding: 12px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.95rem;
        }}
        input:focus, select:focus {{
            outline: none;
            border-color: var(--accent-red);
            box-shadow: 0 0 5px var(--accent-glow);
        }}
        .results-box {{
            margin-top: 25px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 20px;
            border-radius: 6px;
            font-size: 1rem;
        }}
        .formula-box, .faq-box {{
            margin-top: 25px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
        }}
        .formula-box h3, .faq-box h3 {{
            color: var(--accent-red);
            font-size: 0.95rem;
            text-transform: uppercase;
            margin-top: 0;
            letter-spacing: 0.5px;
        }}
        .formula-content {{
            font-family: monospace;
            color: #10b981;
            font-size: 1rem;
            background: var(--input-bg);
            padding: 12px;
            border-radius: 6px;
        }}
        .faq-item {{
            margin-bottom: 15px;
        }}
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
            margin-top: 25px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.9rem;
        }}
        th {{
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.8rem;
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
        <div class="master-container">
            <div class="master-header">
                <h1>{primary_title}</h1>
                <p>{target_keyword} &mdash; Professional Track Tuning Engine</p>
            </div>

            {primary_tool_html}

            <div class="formula-box">
                <h3>Formula Used</h3>
                <div class="formula-content">{formula_text}</div>
            </div>

            <div class="faq-box">
                <h3>Frequently Asked Questions</h3>
                {faqs}
            </div>
        </div>

        <div class="sidebar">
            <div class="sidebar-box">
                <h3>Sponsored By</h3>
                <ul class="sponsor-list">
                    <li>Holley</li>
                    <li>VP Racing Fuels</li>
                    <li>Summit Racing</li>
                    <li>Racepak</li>
                    <li>Mickey Thompson</li>
                    <li>FuelTech</li>
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

print(f"Successfully built {pages_created} high-end pSEO pages with Formula and Sponsor sidebars!")