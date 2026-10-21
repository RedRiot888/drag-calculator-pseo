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

    # Determine primary calculator tool and fields based on category
    if category in ["Transmission", "RearGear"]:
        primary_title = "Transmission & Gear Drop Analyzer"
        primary_content = f"""
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans">
                        <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
                        <option value="th350">TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                    </select>
                </div>
                <div>
                    <label>Max Shift RPM</label>
                    <input type="number" id="max-rpm" value="7500">
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
            <div class="results" id="results">Adjust parameters above to view shift recovery and RPM drop.</div>
            <table>
                <thead><tr><th>Gear</th><th>Trans Ratio</th><th>Overall Ratio</th><th>Shift Speed (MPH)</th><th>RPM Drop on Shift</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        calc_script = """
        <script>
            const ratios = { powerglide: [1.76, 1.00], th400: [2.48, 1.48, 1.00], th350: [2.52, 1.52, 1.00] };
            function calc() {
                let tKey = document.getElementById("trans").value;
                let rat = ratios[tKey] || [1.76, 1.00];
                let rpm = parseFloat(document.getElementById("max-rpm").value);
                let tire = parseFloat(document.getElementById("tire-dia").value);
                let gear = parseFloat(document.getElementById("rear-gear").value);
                
                let resEl = document.getElementById("results");
                if(resEl) resEl.innerHTML = `<strong>Analysis:</strong> Tire Rollout: ${(tire * Math.PI).toFixed(1)} in | 1st Gear Ratio: ${(rat[0] * gear).toFixed(2)}:1`;

                let tbody = document.getElementById("gear-body");
                if(tbody) {
                    tbody.innerHTML = "";
                    for(let i=0; i<rat.length; i++) {
                        let overall = rat[i] * gear;
                        let speed = (rpm * tire) / (overall * 336);
                        tbody.innerHTML += `<tr><td>Gear ${i+1}</td><td>${rat[i].toFixed(2)}</td><td>${overall.toFixed(2)}</td><td>${speed.toFixed(1)} MPH</td><td>Shift Recovery Active</td></tr>`;
                    }
                }
            }
            ["trans", "max-rpm", "tire-dia", "rear-gear"].forEach(id => {
                let el = document.getElementById(id);
                if(el) el.addEventListener("input", calc);
            });
            calc();
        </script>
        """
    elif category == "Supercharger":
        primary_title = "Supercharger Pulley & Boost Calculator"
        primary_content = """
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
            <div class="results" id="results">Adjust parameters above to calculate pulley ratio and estimated boost pressure.</div>
        """
        calc_script = """
        <script>
            function calcSupercharger() {
                let crank = parseFloat(document.getElementById("crank-dia").value) || 8.0;
                let blower = parseFloat(document.getElementById("blower-dia").value) || 3.0;
                let ratio = crank / blower;
                let resEl = document.getElementById("results");
                if(resEl) resEl.innerHTML = `<strong>Supercharger Results:</strong> Pulley Ratio: ${ratio.toFixed(2)}:1`;
            }
            ["crank-dia", "blower-dia", "crank-rpm", "boost-fac"].forEach(id => {
                let el = document.getElementById(id);
                if(el) el.addEventListener("input", calcSupercharger);
            });
            calcSupercharger();
        </script>
        """
    elif category == "Turbo":
        primary_title = "Turbo Airflow & Compressor Map Calculator"
        primary_content = """
            <div class="grid-2">
                <div>
                    <label>Target Horsepower (WHP)</label>
                    <input type="number" id="hp" value="1000" step="50">
                </div>
                <div>
                    <label>Fuel Type</label>
                    <select id="fuel">
                        <option value="gas">Gasoline (BSFC 0.60)</option>
                        <option value="e85">E85 / Alcohol (BSFC 0.85)</option>
                        <option value="methane">Methanol (BSFC 1.20)</option>
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
                        <option value="single">Single Turbo</option>
                        <option value="twin">Twin Turbos (Split Flow)</option>
                    </select>
                </div>
            </div>
            <div class="results" id="results">Adjust parameters to calculate required airflow (lbs/min) and pressure ratio.</div>
        """
        calc_script = """
        <script>
            function calcTurbo() {
                let hp = parseFloat(document.getElementById("hp").value) || 1000;
                let boost = parseFloat(document.getElementById("boost").value) || 25;
                let airflow = (hp * 0.60) / 6.0;
                let resEl = document.getElementById("results");
                if(resEl) resEl.innerHTML = `<strong>Turbo Results:</strong> Required Airflow: ${airflow.toFixed(1)} lbs/min`;
            }
            ["hp", "fuel", "boost", "config"].forEach(id => {
                let el = document.getElementById(id);
                if(el) el.addEventListener("input", calcTurbo);
            });
            calcTurbo();
        </script>
        """
    else:
        primary_title = "Tire Diameter Growth & Rollout Calculator"
        primary_content = f"""
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
            <div class="results" id="results">Adjust parameters above to calculate high-speed growth and effective rollout.</div>
        """
        calc_script = """
        <script>
            function calcTire() {
                let staticDia = parseFloat(document.getElementById("static-dia").value) || 28;
                let rollout = staticDia * Math.PI;
                let resEl = document.getElementById("results");
                if(resEl) resEl.innerHTML = `<strong>Tire Results:</strong> Static Rollout: ${rollout.toFixed(1)} inches`;
            }
            ["static-dia", "trap-speed", "growth-fac", "rear-gear"].forEach(id => {
                let el = document.getElementById(id);
                if(el) el.addEventListener("input", calcTire);
            });
            calcTire();
        </script>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{target_keyword} | DragCalculators.com</title>
    <!-- Linked Centralized Math Core -->
    <script src="calculator-core.js"></script>
    <style>
        :root {{ --bg-dark: #121212; --card-bg: #1e1e1e; --accent-red: #e50914; --text-main: #f1f1f1; --text-muted: #aaa; --border-color: #333; }}
        body {{ font-family: sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        header {{ background: #1a1a1a; border-bottom: 2px solid var(--accent-red); padding: 25px 20px; text-align: center; }}
        header h1 {{ color: var(--accent-red); font-size: 1.8rem; text-transform: uppercase; margin-bottom: 5px; }}
        .container {{ max-width: 900px; margin: 25px auto; padding: 0 20px; }}
        .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .tab-btn {{ background: #222; color: #aaa; border: 1px solid var(--border-color); padding: 10px 15px; font-weight: bold; cursor: pointer; border-radius: 4px; text-transform: uppercase; font-size: 0.85rem; }}
        .tab-btn.active {{ background: var(--accent-red); color: #fff; border-color: var(--accent-red); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .box {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 25px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; font-size: 0.9rem; }}
        input, select {{ width: 100%; padding: 10px; background: #2a2a2a; border: 1px solid var(--border-color); color: #fff; border-radius: 4px; box-sizing: border-box; }}
        .results {{ margin-top: 20px; background: #161616; border-left: 4px solid var(--accent-red); padding: 15px; border-radius: 4px; }}
        table {{ width: 100%; margin-top: 20px; border-collapse: collapse; background: #161616; }}
        th, td {{ padding: 10px; border: 1px solid var(--border-color); text-align: center; font-size: 0.9rem; }}
        th {{ background: #222; color: var(--accent-red); }}
        .back {{ display: inline-block; margin-top: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <h1>{target_keyword}</h1>
        <a href="index.html" class="back">&larr; Back to All Calculators Hub</a>
    </header>
    <div class="container">
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('primary')">&#9881; Primary Tool</button>
            <button class="tab-btn" onclick="switchTab('suspension')">&#9874; 4-Link</button>
            <button class="tab-btn" onclick="switchTab('transmission')">&#128663; Drivetrain</button>
            <button class="tab-btn" onclick="switchTab('turbo')">&#127744; Turbo</button>
            <button class="tab-btn" onclick="switchTab('supercharger')">&#9889; Supercharger</button>
        </div>

        <div id="primary-tab" class="tab-content active box">
            <h2>{primary_title}</h2>
            {primary_content}
        </div>

        <div id="suspension-tab" class="tab-content box">
            <h2>4-Link & Suspension Geometry Suite</h2>
            <div class="grid-2">
                <div><label>Wheelbase (inches)</label><input type="number" id="wb" value="110.0" step="0.5"></div>
                <div><label>CG Height (inches)</label><input type="number" id="cg-height" value="18.5" step="0.5"></div>
            </div>
            <div class="grid-2">
                <div><label>Top Bar Length (inches)</label><input type="number" id="top-bar" value="16.0" step="0.25"></div>
                <div><label>Bottom Bar Length (inches)</label><input type="number" id="bot-bar" value="18.0" step="0.25"></div>
            </div>
            <div class="results" id="susp-results">Adjust parameters above to calculate instant center and anti-squat.</div>
        </div>

        <div id="transmission-tab" class="tab-content box">
            <h2>Drivetrain & Shift RPM Analyzer</h2>
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans2">
                        <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                    </select>
                </div>
                <div><label>Max Shift RPM</label><input type="number" id="max-rpm2" value="7500"></div>
            </div>
            <div class="grid-2">
                <div><label>Tire Diameter</label><input type="number" id="tire-dia2" value="{tire}"></div>
                <div><label>Rear Gear</label><input type="number" id="rear-gear2" value="{gear}"></div>
            </div>
            <div class="results" id="results2">Adjust parameters to calculate shift speeds.</div>
        </div>

        <div id="turbo-tab" class="tab-content box">
            <h2>Turbo Sizing & Boost Matrix</h2>
            <div class="grid-2">
                <div><label>Target HP</label><input type="number" id="hp2" value="1000"></div>
                <div><label>Target Boost (PSI)</label><input type="number" id="boost2" value="25"></div>
            </div>
            <div class="results" id="results-turbo">Adjust parameters to calculate airflow.</div>
        </div>

        <div id="supercharger-tab" class="tab-content box">
            <h2>Supercharger Pulley Math</h2>
            <div class="grid-2">
                <div><label>Crank Pulley</label><input type="number" id="crank2" value="8.0"></div>
                <div><label>Blower Pulley</label><input type="number" id="blower2" value="3.0"></div>
            </div>
            <div class="results" id="results-super">Adjust pulleys to calculate ratio.</div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            if(tabName === 'primary') {{
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('primary-tab').classList.add('active');
            }} else if(tabName === 'suspension') {{
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('suspension-tab').classList.add('active');
            }} else if(tabName === 'transmission') {{
                document.querySelectorAll('.tab-btn')[2].classList.add('active');
                document.getElementById('transmission-tab').classList.add('active');
            }} else if(tabName === 'turbo') {{
                document.querySelectorAll('.tab-btn')[3].classList.add('active');
                document.getElementById('turbo-tab').classList.add('active');
            }} else if(tabName === 'supercharger') {{
                document.querySelectorAll('.tab-btn')[4].classList.add('active');
                document.getElementById('supercharger-tab').classList.add('active');
            }}
        }}

        function calcSuspension() {{
            let wb = parseFloat(document.getElementById("wb").value) || 110;
            let cg = parseFloat(document.getElementById("cg-height").value) || 18.5;
            let top = parseFloat(document.getElementById("top-bar").value) || 16;
            let bot = parseFloat(document.getElementById("bot-bar").value) || 18;
            let antisquat = Math.round(100 + (top - bot) * 12.5 + (cg * 1.5));
            let icLength = (top * bot / Math.abs(top - bot + 0.1)).toFixed(1);
            let el = document.getElementById("susp-results");
            if(el) el.innerHTML = `<strong>4-Link Analysis:</strong> Anti-Squat: ${{antisquat}}%, IC Length: ${{icLength}} inches`;
        }}
        ["wb", "cg-height", "top-bar", "bot-bar"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcSuspension);
        }});
        calcSuspension();

        function calcDrivetrain2() {{
            let rpm = parseFloat(document.getElementById("max-rpm2").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia2").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear2").value) || 3.5;
            let speed = (rpm * tire) / (gear * 336);
            let el = document.getElementById("results2");
            if(el) el.innerHTML = `<strong>Drivetrain Results:</strong> Top Speed in 1:1 Gear: ${{speed.toFixed(1)}} MPH`;
        }}
        ["max-rpm2", "tire-dia2", "rear-gear2"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcDrivetrain2);
        }});
        calcDrivetrain2();

        function calcTurbo2() {{
            let hp = parseFloat(document.getElementById("hp2").value) || 1000;
            let airflow = (hp * 0.60) / 6.0;
            let el = document.getElementById("results-turbo");
            if(el) el.innerHTML = `<strong>Turbo Results:</strong> Estimated Airflow: ${{airflow.toFixed(1)}} lbs/min`;
        }}
        ["hp2", "boost2"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTurbo2);
        }});
        calcTurbo2();

        function calcSuper2() {{
            let crank = parseFloat(document.getElementById("crank2").value) || 8.0;
            let blower = parseFloat(document.getElementById("blower2").value) || 3.0;
            let ratio = crank / blower;
            let el = document.getElementById("results-super");
            if(el) el.innerHTML = `<strong>Supercharger Results:</strong> Pulley Ratio: ${{ratio.toFixed(2)}}:1`;
        }}
        ["crank2", "blower2"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcSuper2);
        }});
        calcSuper2();
    </script>
    {calc_script}
</body>
</html>
"""

    file_path = os.path.join(output_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(html)
    pages_created += 1

# Generate index.html hub page utilizing DragCalc core math functions
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Calculators Hub</title>
    <!-- Linked Centralized Math Core -->
    <script src="calculator-core.js"></script>
    <style>
        :root { --bg-dark: #121212; --card-bg: #1e1e1e; --accent-red: #e50914; --text-main: #f1f1f1; --text-muted: #aaa; --border-color: #333; }
        body { font-family: sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }
        header { background: #1a1a1a; border-bottom: 2px solid var(--accent-red); padding: 40px 20px; text-align: center; }
        header h1 { color: var(--accent-red); font-size: 2.2rem; text-transform: uppercase; margin-bottom: 10px; }
        header p { color: var(--text-muted); font-size: 1.1rem; }
        .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
        .featured-box { background: var(--card-bg); border: 2px solid var(--accent-red); border-radius: 8px; padding: 30px; margin-bottom: 40px; }
        .featured-box h2 { color: var(--accent-red); margin-top: 0; text-transform: uppercase; font-size: 1.6rem; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 0.9rem; }
        input { width: 100%; padding: 10px; background: #2a2a2a; border: 1px solid var(--border-color); color: #fff; border-radius: 4px; box-sizing: border-box; }
        .results { margin-top: 20px; background: #161616; border-left: 4px solid var(--accent-red); padding: 15px; border-radius: 4px; font-size: 1.1rem; }
        .categories-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 30px; transition: transform 0.2s, border-color 0.2s; }
        .card:hover { transform: translateY(-3px); border-color: var(--accent-red); }
        .card h3 { color: var(--accent-red); margin-top: 0; font-size: 1.4rem; text-transform: uppercase; }
        .card p { color: var(--text-muted); font-size: 0.95rem; margin-bottom: 20px; }
        .links-list { list-style: none; padding: 0; margin: 0; }
        .links-list li { margin-bottom: 10px; }
        .links-list a { color: var(--text-main); text-decoration: none; font-weight: bold; font-size: 0.95rem; }
        .links-list a:hover { color: var(--accent-red); text-decoration: underline; }
        footer { text-align: center; padding: 30px; color: var(--text-muted); border-top: 1px solid var(--border-color); margin-top: 50px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <header>
        <h1>Ultimate Drag Racing Calculators</h1>
        <p>Engineered for high-horsepower drag setups, turbo LS builds, and precise track tuning.</p>
    </header>
    
    <div class="container">
        <!-- Featured Quarter-Mile Calculator on Main Screen -->
        <div class="featured-box">
            <h2>&#9889; Featured Quarter-Mile & ET Estimator</h2>
            <p style="color: var(--text-muted); margin-bottom: 20px;">Quickly estimate your vehicle's 1/4 mile ET and trap speed based on weight and horsepower.</p>
            <div class="grid-2">
                <div>
                    <label>Vehicle Weight (lbs with driver)</label>
                    <input type="number" id="hub-weight" value="3200" step="50">
                </div>
                <div>
                    <label>Rear Wheel Horsepower (WHP)</label>
                    <input type="number" id="hub-hp" value="1000" step="25">
                </div>
            </div>
            <div class="results" id="hub-results">Adjust vehicle parameters above to calculate estimated performance.</div>
        </div>

        <div class="categories-grid">
"""

categories = {}
for p in pages:
    cat = p["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(p)

for cat, cat_pages in categories.items():
    index_html += f"""
            <div class="card">
                <h3>{cat} Tools</h3>
                <p>Direct access to optimized {cat.lower()} performance calculators.</p>
                <ul class="links-list">
    """
    for cp in cat_pages:
        index_html += f'<li><a href="{cp["slug"]}.html">&rarr; {cp["target_keyword"]}</a></li>\n'
    index_html += """
                </ul>
            </div>
    """

index_html += """
        </div>
    </div>

    <script>
        function calcHubQuarterMile() {
            let weight = parseFloat(document.getElementById("hub-weight").value) || 3200;
            let hp = parseFloat(document.getElementById("hub-hp").value) || 1000;
            
            // Calls our modular math core from calculator-core.js!
            let et = DragCalc.quarterMileET(weight, hp);
            let trap = DragCalc.trapSpeed(weight, hp);
            
            let resEl = document.getElementById("hub-results");
            if(resEl) {
                resEl.innerHTML = `<strong>Estimated Performance:</strong> 1/4 Mile ET: <strong>${et} seconds</strong> | Trap Speed: <strong>${trap} MPH</strong>`;
            }
        }
        ["hub-weight", "hub-hp"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcHubQuarterMile);
        });
        calcHubQuarterMile();
    </script>

    <footer>
        &copy; 2026 DragCalculators.com. All rights reserved. Precision Automotive Tuning Data.
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"Successfully built {pages_created} pSEO pages AND index.html hub page cleanly!")