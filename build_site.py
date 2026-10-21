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
    elif category == "RearGear":
        primary_title = "Ring and Pinion Rear Gear Quarter-Mile Calculator"
        formula_text = "Finish Line RPM = (Trap Speed × Rear Gear × 336) / Tire Diameter<br>Overall Drive Ratio = Transmission Final × Ring & Pinion"
        faqs = """
            <div class="faq-item">
                <h4>How does changing rear gear affect finish line RPM?</h4>
                <p>Going from a 3.42 to a 4.11 gear increases your finish line RPM significantly, ensuring you cross the stripe right at your peak horsepower band.</p>
            </div>
            <div class="faq-item">
                <h4>What gear is best for quarter-mile drag racing?</h4>
                <p>The optimal rear gear matches your tire height and engine redline so that you cross the 1320-foot finish line at or slightly above peak horsepower RPM in your final 1:1 gear.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Target Trap Speed (MPH)</label>
                    <input type="number" id="trap" value="125" step="1">
                </div>
                <div>
                    <label>Rear Gear Ratio (Ring & Pinion)</label>
                    <input type="number" id="gear" value="{gear}" step="0.01">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Tire Diameter (inches)</label>
                    <input type="number" id="tire" value="{tire}" step="0.1">
                </div>
                <div>
                    <label>Transmission Final Gear Ratio</label>
                    <input type="number" id="trans-final" value="1.00" step="0.01">
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to calculate finish line engine RPM.</div>
        """
        tool_script = """
        function calcTool() {
            let trap = parseFloat(document.getElementById("trap").value) || 125;
            let gear = parseFloat(document.getElementById("gear").value) || 4.11;
            let tire = parseFloat(document.getElementById("tire").value) || 32;
            let transFinal = parseFloat(document.getElementById("trans-final").value) || 1.00;

            let overall = gear * transFinal;
            let finishRpm = (trap * overall * 336) / tire;
            let rollout = (tire * Math.PI).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Rear Gear Analysis:</strong> Overall Drive Ratio: <strong>${overall.toFixed(2)}:1</strong> | Tire Rollout: <strong>${rollout} in</strong> | Finish Line RPM: <strong>${Math.round(finishRpm)} RPM</strong>`;
            }
        }
        ["trap", "gear", "tire", "trans-final"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbo Sizing & Turbocharger Matching Calculator"
        formula_text = "Required Airflow (lb/min) = (Target Flywheel HP × BSFC) / 6.0<br>Pressure Ratio = (Boost PSI + 14.7) / 14.7<br>Approx. Compressor Inducer A/R = Airflow / 18.5"
        faqs = """
            <div class="faq-item">
                <h4>How do I choose the right turbocharger size?</h4>
                <p>Calculate your target flywheel horsepower and required airflow in lb/min. Match your airflow to a compressor map where efficiency islands exceed 70%.</p>
            </div>
            <div class="faq-item">
                <h4>What BSFC factor should I select?</h4>
                <p>Use 0.60 for gasoline intercooled setups, 0.70 for non-intercooled gasoline, 0.85 for E85, and 1.20 for methanol fuel systems.</p>
            </div>
        """
        primary_tool_html = """
            <div class="grid-2">
                <div>
                    <label>Target Flywheel Horsepower (HP)</label>
                    <input type="number" id="hp" value="1000" step="50">
                </div>
                <div>
                    <label>Target Boost Pressure (PSI)</label>
                    <input type="number" id="boost" value="22" step="1">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Fuel BSFC Factor</label>
                    <select id="bsfc">
                        <option value="0.60">Gasoline Intercooled (0.60)</option>
                        <option value="0.70">Gasoline Non-Intercooled (0.70)</option>
                        <option value="0.85" selected>E85 / Ethanol (0.85)</option>
                        <option value="1.20">Methanol (1.20)</option>
                    </select>
                </div>
                <div>
                    <label>Turbo Setup</label>
                    <select id="turbos">
                        <option value="1" selected>Single Turbocharger</option>
                        <option value="2">Twin Turbochargers (Split)</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="results">Adjust target horsepower and boost to determine turbo sizing specs.</div>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("hp").value) || 1000;
            let boost = parseFloat(document.getElementById("boost").value) || 22;
            let bsfc = parseFloat(document.getElementById("bsfc").value) || 0.85;
            let count = parseInt(document.getElementById("turbos").value) || 1;

            let totalAirflow = (hp * bsfc) / 6.0;
            let perTurbo = totalAirflow / count;
            let pr = (boost + 14.7) / 14.7;
            let recInducer = (Math.sqrt(perTurbo * 14.2)).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Turbo Sizing Match:</strong> Total Airflow: <strong>${totalAirflow.toFixed(1)} lb/min</strong> (${perTurbo.toFixed(1)} lb/min per turbo) | Pressure Ratio: <strong>${pr.toFixed(2)}:1</strong> | Rec. Inducer: <strong>${recInducer} mm</strong>`;
            }
        }
        ["hp", "boost", "bsfc", "turbos"].forEach(id => {
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
    elif category == "Tire":
        primary_title = "Tire Diameter Growth & Rollout Drag Calculator"
        formula_text = "Dynamic Diameter = Static Diameter × (1 + (Growth % / 100))<br>Rollout = Diameter × π<br>Finish Line RPM = (Trap Speed × Rear Gear × 336) / Dynamic Diameter"
        faqs = """
            <div class="faq-item">
                <h4>Why do drag tires grow at high speed?</h4>
                <p>Centrifugal force at 150+ MPH causes bias-ply and radial slick treads to expand outward, increasing effective rollout and altering finish line RPM.</p>
            </div>
            <div class="faq-item">
                <h4>How do tire construction types affect growth?</h4>
                <p>Traditional bias-ply slicks expand significantly more (6-8%) due to flexible sidewalls, whereas stiff-sidewall slicks and radial drag tires maintain much tighter dimensional stability (2-4%).</p>
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
                    <label>Tire Construction Preset</label>
                    <select id="tire-preset" onchange="applyPreset()">
                        <option value="custom">Custom Growth Factor</option>
                        <option value="7.0">Bias-Ply Drag Slick (7.0%)</option>
                        <option value="4.5" selected>Stiff Sidewall Slick (4.5%)</option>
                        <option value="2.5">Radial Drag Slick (2.5%)</option>
                        <option value="1.0">Street Radial / DOT Tire (1.0%)</option>
                    </select>
                </div>
                <div>
                    <label>Growth Factor (%)</label>
                    <input type="number" id="growth-fac" value="4.5" step="0.1">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Rear Gear Ratio</label>
                    <input type="number" id="rear-gear" value="{gear}" step="0.01">
                </div>
                <div>
                    <label style="opacity:0">Spacer</label>
                    <div style="font-size:0.80rem; color: var(--text-muted); padding-top:8px;">Select preset above for beginner guidance</div>
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above to calculate high-speed growth and effective rollout.</div>
        """
        tool_script = """
        function applyPreset() {
            let pVal = document.getElementById("tire-preset").value;
            if(pVal !== "custom") {
                document.getElementById("growth-fac").value = pVal;
                calcTool();
            }
        }
        function calcTool() {
            let staticDia = parseFloat(document.getElementById("static-dia").value) || 28;
            let trap = parseFloat(document.getElementById("trap-speed").value) || 150;
            let growth = parseFloat(document.getElementById("growth-fac").value) || 4.5;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;

            let dynamicDia = staticDia * (1 + (growth / 100));
            let staticRollout = (staticDia * Math.PI).toFixed(1);
            let dynamicRollout = (dynamicDia * Math.PI).toFixed(1);
            let estFinishRpm = Math.round((trap * gear * 336) / dynamicDia);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = `<strong>Tire Results:</strong> Static Rollout: <strong>${staticRollout} in</strong> | Dynamic Dia: <strong>${dynamicDia.toFixed(2)} in</strong> | Dynamic Rollout: <strong>${dynamicRollout} in</strong><br>Est. Finish Line RPM: <strong>${estFinishRpm} RPM</strong>`;
            }
        }
        ["static-dia", "trap-speed", "growth-fac", "rear-gear"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", () => {
                document.getElementById("tire-preset").value = "custom";
                calcTool();
            });
        });
        calcTool();
        """
    else:
        primary_title = "Drag Racing Calculator Suite"
        formula_text = "Standard Automotive Calculation"
        faqs = ""
        primary_tool_html = "<div>Select a tool from the hub.</div>"
        tool_script = ""

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
        .utility-list, .sponsor-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        .utility-list li, .sponsor-list li {{
            padding: 8px 0;
            border-bottom: 1px dashed var(--border-color);
        }}
        .utility-list li:last-child, .sponsor-list li:last-child {{ border-bottom: none; }}
        .utility-list li a, .sponsor-list li a {{
            color: var(--text-muted);
            text-decoration: none;
            display: block;
            transition: color 0.2s;
        }}
        .utility-list li a:hover, .sponsor-list li a:hover {{
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
            .layout-grid {{ grid-template-columns: 1fr; }}
        }}
        label {{
            display: block;
            margin-bottom: 4px;
            font-weight: 600;
            font-size: 0.80rem;
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

print(f"Successfully generated {pages_created} unique clean pages with preset updates.")