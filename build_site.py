import os
import csv

output_dir = "."

# 1. Read pSEO pages list
with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages = list(reader)

# Build HTML links for "Other Utilities" box
utilities_links_html = ""
for row in pages:
    utilities_links_html += f'<li><a href="{row["slug"]}.html">{row["target_keyword"]}</a></li>\n'

# 2. Generate Master Index Hub (index.html) with Sticky Layout
index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Master Suite | Professional Track Calculators</title>
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
        .tab-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .tab-btn {{
            flex: 1;
            padding: 10px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.8rem;
            text-transform: uppercase;
        }}
        .tab-btn.active {{
            background: var(--accent-red);
            color: white;
            border-color: var(--accent-red);
        }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 12px;
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
    </style>
</head>
<body>
    <div class="layout-grid">
        <!-- Sticky Left Calculator Hub -->
        <div class="sticky-calculator">
            <div class="master-header">
                <h1>Ultimate Drag Racing Suite</h1>
                <p>Professional Track Tuning Engine</p>
            </div>

            <div class="tab-buttons">
                <button class="tab-btn active" onclick="switchTab('drivetrain', event)">Drivetrain & Shift</button>
                <button class="tab-btn" onclick="switchTab('suspension', event)">4-Link Suspension</button>
            </div>

            <!-- Drivetrain Tab -->
            <div id="tab-drivetrain" class="tab-content active">
                <div class="grid-2">
                    <div>
                        <label>Transmission Profile</label>
                        <select id="trans" onchange="calcDrivetrain()">
                            <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                            <option value="th350" selected>TH350 (2.52 / 1.52 / 1.00)</option>
                            <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                        </select>
                    </div>
                    <div>
                        <label>Max Shift RPM</label>
                        <input type="number" id="max-rpm" value="7500" step="100" oninput="calcDrivetrain()">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>Tire Diameter (inches)</label>
                        <input type="number" id="tire-dia" value="28.0" step="0.1" oninput="calcDrivetrain()">
                    </div>
                    <div>
                        <label>Rear Gear Ratio</label>
                        <input type="number" id="rear-gear" value="3.42" step="0.01" oninput="calcDrivetrain()">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>Vehicle Weight (lbs)</label>
                        <input type="number" id="veh-weight" value="3200" step="50" oninput="calcDrivetrain()">
                    </div>
                    <div>
                        <label>Flywheel Horsepower</label>
                        <input type="number" id="veh-hp" value="600" step="25" oninput="calcDrivetrain()">
                    </div>
                </div>
                <div class="results-box" id="dt-results">Adjust parameters above to view performance analysis.</div>
                <table>
                    <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
                    <tbody id="gear-body"></tbody>
                </table>
            </div>

            <!-- Suspension Tab -->
            <div id="tab-suspension" class="tab-content">
                <div class="grid-2">
                    <div>
                        <label>Total Vehicle Weight (lbs)</label>
                        <input type="number" id="susp-weight" value="3200" step="50" oninput="calcSuspension()">
                    </div>
                    <div>
                        <label>Wheelbase (inches)</label>
                        <input type="number" id="susp-wb" value="105.0" step="0.5" oninput="calcSuspension()">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>CG Height (inches)</label>
                        <input type="number" id="susp-cg" value="20.0" step="0.5" oninput="calcSuspension()">
                    </div>
                    <div>
                        <label>Static Front Weight (%)</label>
                        <input type="number" id="susp-fwt" value="52.0" step="0.5" oninput="calcSuspension()">
                    </div>
                </div>
                <div class="results-box" id="susp-results">Adjust suspension parameters to view instantaneous center and anti-squat.</div>
            </div>
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
                <h3>Featured Partners</h3>
                <ul class="sponsor-list">
                    <li><a href="https://www.summitracing.com" target="_blank">Summit Racing Equipment</a></li>
                    <li><a href="https://www.holley.com" target="_blank">Holley Performance</a></li>
                    <li><a href="https://vpracingfuels.com" target="_blank">VP Racing Fuels</a></li>
                    <li><a href="https://www.mickeythompsontires.com" target="_blank">Mickey Thompson Tires</a></li>
                </ul>
            </div>

            <div class="content-box" style="text-align: center;">
                <h3>Advertisement</h3>
                <div style="background: var(--input-bg); height: 250px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 0.85rem; border-radius: 6px;">
                    300 x 250 Ad Slot
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName, event) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            event.currentTarget.classList.add('active');
        }}

        const ratios = {{ powerglide: [1.76, 1.00], th350: [2.52, 1.52, 1.00], th400: [2.48, 1.48, 1.00] }};
        function calcDrivetrain() {{
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.52, 1.52, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let weight = parseFloat(document.getElementById("veh-weight").value) || 3200;
            let hp = parseFloat(document.getElementById("veh-hp").value) || 600;
            
            let et = (5.825 * Math.cbrt(weight / (hp > 0 ? hp : 1))).toFixed(2);
            let rollout = (tire * Math.PI).toFixed(1);
            
            let resEl = document.getElementById("dt-results");
            if(resEl) {{
                resEl.innerHTML = `<strong>Performance Estimate:</strong> Est. 1/4 Mile ET: <strong>${{et}} sec</strong> | Rollout: ${{rollout}} in | 1st Gear Overall: ${{(rat[0] * gear).toFixed(2)}}:1`;
            }}

            let tbody = document.getElementById("gear-body");
            if(tbody) {{
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {{
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? Math.round(rpm * (rat[i+1] / rat[i])) : "Finish Line";
                    tbody.innerHTML += `<tr><td>Gear ${{i+1}}</td><td>${{rat[i].toFixed(2)}}</td><td>${{overall.toFixed(2)}}</td><td>${{speed.toFixed(1)}} MPH</td><td>Drop to ${{drop}}</td></tr>`;
                }}
            }}
        }}

        function calcSuspension() {{
            let weight = parseFloat(document.getElementById("susp-weight").value) || 3200;
            let wb = parseFloat(document.getElementById("susp-wb").value) || 105;
            let cg = parseFloat(document.getElementById("susp-cg").value) || 20;
            let fwt = parseFloat(document.getElementById("susp-fwt").value) || 52;

            let rearWeight = weight * (1 - (fwt / 100));
            let resEl = document.getElementById("susp-results");
            if(resEl) {{
                resEl.innerHTML = `<strong>Suspension Geometry:</strong> Rear Static Weight: <strong>${{Math.round(rearWeight)}} lbs</strong> | Estimated Instant Center Length: <strong>${{(wb * 0.45).toFixed(1)}} inches</strong> (Optimal for 60ft launch traction).`;
            }}
        }}

        calcDrivetrain();
        calcSuspension();
    </script>
</body>
</html>
"""

with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("Successfully updated index.html with fully escaped JavaScript templates!")