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
        .master-container {{
            max-width: 950px;
            margin: 30px auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 35px;
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
        .suite-tabs {{
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
            justify-content: center;
        }}
        .suite-tab-btn {{
            background: var(--input-bg);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 12px 24px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 8px;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
        }}
        .suite-tab-btn.active {{
            background: var(--accent-red);
            color: #fff;
            border-color: var(--accent-red);
            box-shadow: 0 0 15px var(--accent-glow);
        }}
        .suite-content {{
            display: none;
        }}
        .suite-content.active {{
            display: block;
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
    <div style="max-width: 950px; margin: 0 auto;">
        <a href="index.html" class="back-link">&larr; Back to Master Calculators Hub</a>
    </div>

    <div class="master-container">
        <div class="master-header">
            <h1>Ultimate Drag Racing Master Suite</h1>
            <p>{target_keyword} &mdash; Professional Track Tuning Engine</p>
        </div>

        <div class="suite-tabs">
            <button class="suite-tab-btn active" onclick="switchSuiteTab('drivetrain')">&#9881; Drivetrain & Shift RPM</button>
            <button class="suite-tab-btn" onclick="switchSuiteTab('suspension')">&#9874; 4-Link & Suspension</button>
        </div>

        <div id="drivetrain-suite" class="suite-content active">
            <div class="section-title">1. Transmission & Gear Parameters</div>
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans">
                        <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                        <option value="th350" selected>TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
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

            <div class="section-title">2. Vehicle Weight & Power Analytics</div>
            <div class="grid-2">
                <div>
                    <label>Vehicle Weight (lbs with driver)</label>
                    <input type="number" id="weight" value="2390" step="50">
                </div>
                <div>
                    <label>Wheel Horsepower (WHP)</label>
                    <input type="number" id="hp" value="1100" step="25">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Target / Finish Line Trap Speed (MPH)</label>
                    <input type="number" id="target-trap" value="120" step="1">
                </div>
                <div>
                    <label>Torque Converter Slip (%)</label>
                    <input type="number" id="converter-slip" value="0" step="0.5">
                </div>
            </div>

            <div class="results-box" id="drivetrain-results">
                Adjust parameters above to view physics-based ET, trap speed, and rollout analytics.
            </div>

            <table>
                <thead>
                    <tr><th>Gear</th><th>Static Ratio</th><th>Overall Ratio</th><th>Speed at Shift Point</th><th>RPM Drop / Recovery on Shift</th></tr>
                </thead>
                <tbody id="gear-body"></tbody>
            </table>
        </div>

        <div id="suspension-suite" class="suite-content">
            <div class="section-title">1. Vehicle & Weight Distribution Parameters</div>
            <div class="grid-2">
                <div>
                    <label>Total Vehicle Weight (lbs with driver)</label>
                    <input type="number" id="wb-weight" value="2390" step="50">
                </div>
                <div>
                    <label>Wheelbase (inches)</label>
                    <input type="number" id="wb" value="95.4" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Center of Gravity (CG) Height (inches)</label>
                    <input type="number" id="cg-height" value="18.0" step="0.5">
                </div>
                <div>
                    <label>Static Front Weight (%)</label>
                    <input type="number" id="front-weight" value="48.0" step="0.5">
                </div>
            </div>

            <div class="section-title">2. 4-Link Bracket & Bar Geometry</div>
            <div class="grid-2">
                <div>
                    <label>Top Bar Front Hole X (Axle ahead = positive, in)</label>
                    <input type="number" id="top-x1" value="24.0" step="0.5">
                </div>
                <div>
                    <label>Top Bar Front Hole Z (Height above axle, in)</label>
                    <input type="number" id="top-z1" value="6.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Top Bar Rear Hole X (Axle ahead = positive, in)</label>
                    <input type="number" id="top-x2" value="0.0" step="0.5">
                </div>
                <div>
                    <label>Top Bar Rear Hole Z (Height above axle, in)</label>
                    <input type="number" id="top-z2" value="4.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Bottom Bar Front Hole X (in)</label>
                    <input type="number" id="bot-x1" value="26.0" step="0.5">
                </div>
                <div>
                    <label>Bottom Bar Front Hole Z (in)</label>
                    <input type="number" id="bot-z1" value="-2.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Bottom Bar Rear Hole X (in)</label>
                    <input type="number" id="bot-x2" value="0.0" step="0.5">
                </div>
                <div>
                    <label>Bottom Bar Rear Hole Z (in)</label>
                    <input type="number" id="bot-z2" value="-4.0" step="0.5">
                </div>
            </div>

            <div class="results-box" id="susp-results">
                Adjust suspension geometry above to calculate Instant Center and Anti-Squat.
            </div>
        </div>
    </div>

    <script>
        function switchSuiteTab(tabName) {{
            document.querySelectorAll('.suite-tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.suite-content').forEach(content => content.classList.remove('active'));
            
            if(tabName === 'drivetrain') {{
                document.querySelectorAll('.suite-tab-btn')[0].classList.add('active');
                document.getElementById('drivetrain-suite').classList.add('active');
            }} else if(tabName === 'suspension') {{
                document.querySelectorAll('.suite-tab-btn')[1].classList.add('active');
                document.getElementById('suspension-suite').classList.add('active');
            }}
        }}

        const ratios = {{ 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00] 
        }};

        function calcMasterDrivetrain() {{
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.52, 1.52, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let weight = parseFloat(document.getElementById("weight").value) || 2390;
            let hp = parseFloat(document.getElementById("hp").value) || 1100;
            
            let et = DragCalc.quarterMileET(weight, hp);
            let trap = DragCalc.trapSpeed(weight, hp);
            let rollout = (tire * Math.PI).toFixed(1);
            let overall1st = (rat[0] * gear).toFixed(2);

            let resEl = document.getElementById("drivetrain-results");
            if(resEl) {{
                resEl.innerHTML = `
                    <strong>Estimated Performance:</strong><br>
                    &bull; Estimated 1/4 Mile Trap Speed: <strong>${{trap}} MPH</strong><br>
                    &bull; Estimated 1/4 Mile ET: <strong>${{et}} sec</strong><br>
                    &bull; Tire Circumference (Rollout): <strong>${{rollout}} inches</strong><br>
                    &bull; Overall 1st Gear Launch Ratio: <strong>${{overall1st}}:1</strong>
                `;
            }}

            let tbody = document.getElementById("gear-body");
            if(tbody) {{
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {{
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? Math.round(rpm * (rat[i+1] / rat[i])) : "Crossing Line";
                    tbody.innerHTML += `<tr><td>Gear ${{i+1}}</td><td>${{rat[i].toFixed(2)}}</td><td>${{overall.toFixed(2)}}</td><td>${{speed.toFixed(1)}} MPH</td><td>Drop to ${{drop}} RPM</td></tr>`;
                }}
            }}
        }}

        function calcMasterSuspension() {{
            let topX1 = parseFloat(document.getElementById("top-x1").value) || 24;
            let topZ1 = parseFloat(document.getElementById("top-z1").value) || 6;
            let topX2 = parseFloat(document.getElementById("top-x2").value) || 0;
            let topZ2 = parseFloat(document.getElementById("top-z2").value) || 4;
            
            let botX1 = parseFloat(document.getElementById("bot-x1").value) || 26;
            let botZ1 = parseFloat(document.getElementById("bot-z1").value) || -2;
            let botX2 = parseFloat(document.getElementById("bot-x2").value) || 0;
            let botZ2 = parseFloat(document.getElementById("bot-z2").value) || -4;

            let cg = parseFloat(document.getElementById("cg-height").value) || 18;
            let icLength = Math.abs((topZ1 - botZ1) / (((topZ2 - topZ1)/((topX2 - topX1)||0.1)) - ((botZ2 - botZ1)/((botX2 - botX1)||0.1)) || 0.001)).toFixed(1);
            let icHeight = Math.abs(topZ1 + ((topZ2 - topZ1)/((topX2 - topX1)||0.1)) * icLength).toFixed(1);
            let antisquat = Math.round(100 + (icHeight - (cg * 0.5)) * 4.5);

            let resEl = document.getElementById("susp-results");
            if(resEl) {{
                resEl.innerHTML = `
                    <strong>4-Link Geometry Analysis:</strong><br>
                    &bull; Instant Center (IC) Length: <strong>${{icLength}} inches</strong><br>
                    &bull; Instant Center (IC) Height: <strong>${{icHeight}} inches</strong><br>
                    &bull; Anti-Squat Percentage: <strong>${{antisquat}}%</strong>
                `;
            }}
        }}

        ["trans", "max-rpm", "tire-dia", "rear-gear", "weight", "hp", "target-trap", "converter-slip"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcMasterDrivetrain);
        }});
        ["wb-weight", "wb", "cg-height", "front-weight", "top-x1", "top-z1", "top-x2", "top-z2", "bot-x1", "bot-z1", "bot-x2", "bot-z2"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcMasterSuspension);
        }});

        calcMasterDrivetrain();
        calcMasterSuspension();
    </script>
</body>
</html>
"""

    file_path = os.path.join(output_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(html)
    pages_created += 1

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Master Suite Hub</title>
    <script src="calculator-core.js"></script>
    <style>
        :root {
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --accent-glow: rgba(255, 30, 39, 0.25);
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.5;
        }
        .master-container {
            max-width: 950px;
            margin: 30px auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 35px;
        }
        .master-header {
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }
        .master-header h1 {
            color: var(--accent-red);
            font-size: 2.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 0 0 5px 0;
        }
        .master-header p {
            color: var(--text-muted);
            font-size: 1rem;
            margin: 0;
        }
        .suite-tabs {
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
            justify-content: center;
        }
        .suite-tab-btn {
            background: var(--input-bg);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 12px 24px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 8px;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
        }
        .suite-tab-btn.active {
            background: var(--accent-red);
            color: #fff;
            border-color: var(--accent-red);
            box-shadow: 0 0 15px var(--accent-glow);
        }
        .suite-content {
            display: none;
        }
        .suite-content.active {
            display: block;
        }
        .section-title {
            color: var(--accent-red);
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 25px 0 15px 0;
            border-left: 3px solid var(--accent-red);
            padding-left: 10px;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
        }
        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
        input, select {
            width: 100%;
            padding: 12px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.95rem;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--accent-red);
            box-shadow: 0 0 5px var(--accent-glow);
        }
        .results-box {
            margin-top: 25px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 20px;
            border-radius: 6px;
            font-size: 1rem;
        }
        table {
            width: 100%;
            margin-top: 25px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 12px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.9rem;
        }
        th {
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }
        .pseo-directory {
            max-width: 950px;
            margin: 40px auto;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 30px;
        }
        .pseo-directory h3 {
            color: var(--accent-red);
            text-transform: uppercase;
            margin-top: 0;
            font-size: 1.2rem;
        }
        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 15px;
            list-style: none;
            padding: 0;
            margin: 15px 0 0 0;
        }
        .links-grid li a {
            color: var(--text-main);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        .links-grid li a:hover {
            color: var(--accent-red);
            text-decoration: underline;
        }
        footer {
            text-align: center;
            padding: 30px;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            margin-top: 50px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="master-container">
        <div class="master-header">
            <h1>Ultimate Drag Racing Master Suite</h1>
            <p>Drivetrain Shift RPM & 4-Link Suspension Geometry Calculator</p>
        </div>

        <div class="suite-tabs">
            <button class="suite-tab-btn active" onclick="switchSuiteTab('drivetrain')">&#9881; Drivetrain & Shift RPM</button>
            <button class="suite-tab-btn" onclick="switchSuiteTab('suspension')">&#9874; 4-Link & Suspension</button>
        </div>

        <div id="drivetrain-suite" class="suite-content active">
            <div class="section-title">1. Transmission & Gear Parameters</div>
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans">
                        <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                        <option value="th350" selected>TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
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
                    <input type="number" id="tire-dia" value="28.0" step="0.1">
                </div>
                <div>
                    <label>Rear Gear Ratio</label>
                    <input type="number" id="rear-gear" value="3.42" step="0.01">
                </div>
            </div>

            <div class="section-title">2. Vehicle Weight & Power Analytics</div>
            <div class="grid-2">
                <div>
                    <label>Vehicle Weight (lbs with driver)</label>
                    <input type="number" id="weight" value="2390" step="50">
                </div>
                <div>
                    <label>Wheel Horsepower (WHP)</label>
                    <input type="number" id="hp" value="1100" step="25">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Target / Finish Line Trap Speed (MPH)</label>
                    <input type="number" id="target-trap" value="120" step="1">
                </div>
                <div>
                    <label>Torque Converter Slip (%)</label>
                    <input type="number" id="converter-slip" value="0" step="0.5">
                </div>
            </div>

            <div class="results-box" id="drivetrain-results">
                Adjust parameters above to view physics-based ET, trap speed, and rollout analytics.
            </div>

            <table>
                <thead>
                    <tr><th>Gear</th><th>Static Ratio</th><th>Overall Ratio</th><th>Speed at Shift Point</th><th>RPM Drop / Recovery on Shift</th></tr>
                </thead>
                <tbody id="gear-body"></tbody>
            </table>
        </div>

        <div id="suspension-suite" class="suite-content">
            <div class="section-title">1. Vehicle & Weight Distribution Parameters</div>
            <div class="grid-2">
                <div>
                    <label>Total Vehicle Weight (lbs with driver)</label>
                    <input type="number" id="wb-weight" value="2390" step="50">
                </div>
                <div>
                    <label>Wheelbase (inches)</label>
                    <input type="number" id="wb" value="95.4" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Center of Gravity (CG) Height (inches)</label>
                    <input type="number" id="cg-height" value="18.0" step="0.5">
                </div>
                <div>
                    <label>Static Front Weight (%)</label>
                    <input type="number" id="front-weight" value="48.0" step="0.5">
                </div>
            </div>

            <div class="section-title">2. 4-Link Bracket & Bar Geometry</div>
            <div class="grid-2">
                <div>
                    <label>Top Bar Front Hole X (Axle ahead = positive, in)</label>
                    <input type="number" id="top-x1" value="24.0" step="0.5">
                </div>
                <div>
                    <label>Top Bar Front Hole Z (Height above axle, in)</label>
                    <input type="number" id="top-z1" value="6.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Top Bar Rear Hole X (Axle ahead = positive, in)</label>
                    <input type="number" id="top-x2" value="0.0" step="0.5">
                </div>
                <div>
                    <label>Top Bar Rear Hole Z (Height above axle, in)</label>
                    <input type="number" id="top-z2" value="4.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Bottom Bar Front Hole X (in)</label>
                    <input type="number" id="bot-x1" value="26.0" step="0.5">
                </div>
                <div>
                    <label>Bottom Bar Front Hole Z (in)</label>
                    <input type="number" id="bot-z1" value="-2.0" step="0.5">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Bottom Bar Rear Hole X (in)</label>
                    <input type="number" id="bot-x2" value="0.0" step="0.5">
                </div>
                <div>
                    <label>Bottom Bar Rear Hole Z (in)</label>
                    <input type="number" id="bot-z2" value="-4.0" step="0.5">
                </div>
            </div>

            <div class="results-box" id="susp-results">
                Adjust suspension geometry above to calculate Instant Center and Anti-Squat.
            </div>
        </div>
    </div>

    <div class="pseo-directory">
        <h3>Targeted Performance Calculators</h3>
        <ul class="links-grid">
"""

for p in pages:
    index_html += f'            <li><a href="{p["slug"]}.html">&rarr; {p["target_keyword"]}</a></li>\n'

index_html += """
        </ul>
    </div>

    <script>
        function switchSuiteTab(tabName) {
            document.querySelectorAll('.suite-tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.suite-content').forEach(content => content.classList.remove('active'));
            
            if(tabName === 'drivetrain') {
                document.querySelectorAll('.suite-tab-btn')[0].classList.add('active');
                document.getElementById('drivetrain-suite').classList.add('active');
            } else if(tabName === 'suspension') {
                document.querySelectorAll('.suite-tab-btn')[1].classList.add('active');
                document.getElementById('suspension-suite').classList.add('active');
            }
        }

        const ratios = { 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00] 
        };

        function calcMasterDrivetrain() {
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.52, 1.52, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let weight = parseFloat(document.getElementById("weight").value) || 2390;
            let hp = parseFloat(document.getElementById("hp").value) || 1100;
            
            let et = DragCalc.quarterMileET(weight, hp);
            let trap = DragCalc.trapSpeed(weight, hp);
            let rollout = (tire * Math.PI).toFixed(1);
            let overall1st = (rat[0] * gear).toFixed(2);

            let resEl = document.getElementById("drivetrain-results");
            if(resEl) {
                resEl.innerHTML = `
                    <strong>Estimated Performance:</strong><br>
                    &bull; Estimated 1/4 Mile Trap Speed: <strong>${trap} MPH</strong><br>
                    &bull; Estimated 1/4 Mile ET: <strong>${et} sec</strong><br>
                    &bull; Tire Circumference (Rollout): <strong>${rollout} inches</strong><br>
                    &bull; Overall 1st Gear Launch Ratio: <strong>${overall1st}:1</strong>
                `;
            }

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

        function calcMasterSuspension() {
            let topX1 = parseFloat(document.getElementById("top-x1").value) || 24;
            let topZ1 = parseFloat(document.getElementById("top-z1").value) || 6;
            let topX2 = parseFloat(document.getElementById("top-x2").value) || 0;
            let topZ2 = parseFloat(document.getElementById("top-z2").value) || 4;
            
            let botX1 = parseFloat(document.getElementById("bot-x1").value) || 26;
            let botZ1 = parseFloat(document.getElementById("bot-z1").value) || -2;
            let botX2 = parseFloat(document.getElementById("bot-x2").value) || 0;
            let botZ2 = parseFloat(document.getElementById("bot-z2").value) || -4;

            let cg = parseFloat(document.getElementById("cg-height").value) || 18;
            let icLength = Math.abs((topZ1 - botZ1) / (((topZ2 - topZ1)/((topX2 - topX1)||0.1)) - ((botZ2 - botZ1)/((botX2 - botX1)||0.1)) || 0.001)).toFixed(1);
            let icHeight = Math.abs(topZ1 + ((topZ2 - topZ1)/((topX2 - topX1)||0.1)) * icLength).toFixed(1);
            let antisquat = Math.round(100 + (icHeight - (cg * 0.5)) * 4.5);

            let resEl = document.getElementById("susp-results");
            if(resEl) {
                resEl.innerHTML = `
                    <strong>4-Link Geometry Analysis:</strong><br>
                    &bull; Instant Center (IC) Length: <strong>${icLength} inches</strong><br>
                    &bull; Instant Center (IC) Height: <strong>${icHeight} inches</strong><br>
                    &bull; Anti-Squat Percentage: <strong>${antisquat}%</strong>
                `;
            }
        }

        ["trans", "max-rpm", "tire-dia", "rear-gear", "weight", "hp", "target-trap", "converter-slip"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcMasterDrivetrain);
        });
        ["wb-weight", "wb", "cg-height", "front-weight", "top-x1", "top-z1", "top-x2", "top-z2", "bot-x1", "bot-z1", "bot-x2", "bot-z2"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcMasterSuspension);
        });

        calcMasterDrivetrain();
        calcMasterSuspension();
    </script>

    <footer>
        &copy; 2026 DragCalculators.com. All rights reserved. Professional Automotive Tuning Data.
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"Successfully built {pages_created} Master Suite pSEO pages AND index.html hub page cleanly!")