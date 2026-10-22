import os
import csv

output_dir = "."

with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages = list(reader)

utilities_links_html = ""
for row in pages:
    utilities_links_html += f'<li><a href="{row["slug"]}.html">{row["target_keyword"]}</a></li>\n'

# 1. GENERATE THE MASTER HUB (index.html)
master_index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Drivetrain & Shift RPM Calculator Suite</title>
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
            grid-template-columns: 500px 1fr;
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
            font-size: 1.4rem;
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
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .tab-btn {{
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 12px 8px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.75rem;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: var(--accent-red);
            color: white;
            border-color: var(--accent-red);
            box-shadow: 0 0 10px var(--accent-glow);
        }}
        .tab-pane {{
            display: none;
        }}
        .tab-pane.active {{
            display: block;
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
        optgroup {{
            color: var(--accent-red);
            font-weight: bold;
        }}
        option {{
            color: var(--text-main);
            background: var(--input-bg);
        }}
        input:focus, select:focus {{
            outline: none;
            border-color: var(--accent-red);
            box-shadow: 0 0 5px var(--accent-glow);
        }}
        .results-box {{
            margin-top: 15px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            word-break: break-word;
        }}
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
            letter-spacing: 0.5px;
        }}
        .section-title {{
            color: var(--accent-red);
            font-size: 0.80rem;
            text-transform: uppercase;
            border-bottom: 1px dashed var(--border-color);
            margin: 15px 0 8px 0;
            padding-bottom: 4px;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
    <div class="layout-grid">
        <!-- Sticky Left Calculator -->
        <div class="sticky-calculator">
            <div class="master-header">
                <h1>Ultimate Drag Racing Suite</h1>
                <p>Professional Track Tuning Engine</p>
            </div>

            <!-- Tabs -->
            <div class="tab-buttons">
                <button type="button" class="tab-btn active" id="btn-drivetrain">Drivetrain & Shift</button>
                <button type="button" class="tab-btn" id="btn-suspension">4-Link Suspension</button>
            </div>

            <!-- Tab 1: Drivetrain & Shift -->
            <div id="pane-drivetrain" class="tab-pane active">
                <div class="grid-2">
                    <div>
                        <label>Transmission Profile</label>
                        <select id="trans" onchange="applyTransPreset()">
                            <optgroup label="GM (Chevrolet / GMC)">
                                <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                                <option value="th350">TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                                <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
                                <option value="4l60e">4L60e / 4L65E / 4L70E (3.06 / 1.62 / 1.00 / 0.70 - 4-Speed)</option>
                                <option value="4l80e_overdrive">4L80E w/ Overdrive (2.48 / 1.48 / 1.00 / 0.75 - 4-Speed)</option>
                                <option value="6l80">6L80 / 6L90 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67 - 6-Speed)</option>
                                <option value="gm_8l90">GM 8L90 / ZL1 Auto (4.56 / 2.97 / 2.08 / 1.69 / 1.27 / 1.00 / 0.85 / 0.65 - 8-Speed)</option>
                                <option value="muncie_m22">Muncie M22 'Rock Crusher' (2.20 / 1.64 / 1.28 / 1.00 - 4-Speed)</option>
                                <option value="borg_warner">Borg-Warner Super T-10 (2.43 / 1.61 / 1.23 / 1.00 - 4-Speed)</option>
                                <option value="tr6060">1LE / ZL1 Camaro TR-6060 (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50 - 6-Speed)</option>
                            </optgroup>
                            <optgroup label="Ford">
                                <option value="toploader_close">Ford Toploader - Close Ratio (2.32 / 1.69 / 1.29 / 1.00 - 4-Speed)</option>
                                <option value="toploader_wide">Ford Toploader - Wide Ratio (2.78 / 1.93 / 1.35 / 1.00 - 4-Speed)</option>
                                <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00 - 3-Speed)</option>
                                <option value="ford_t5">Ford T-5 Manual (2.95 / 1.94 / 1.34 / 1.00 / 0.73 - 5-Speed)</option>
                                <option value="mustang_mt82">Mustang GT MT82 (3.66 / 2.43 / 1.69 / 1.32 / 1.00 / 0.65 - 6-Speed)</option>
                                <option value="shelby_gt500">Shelby GT500 TR-9070 DCT (2.26 / 1.58 / 1.19 / 1.00 / 0.83 / 0.64 / 0.53 - 7-Speed)</option>
                                <option value="mustang_10r80">Mustang 10R80 Auto (4.70 / 2.99 / 2.15 / 1.77 / 1.52 / 1.28 / 1.00 / 0.85 / 0.69 / 0.64 - 10-Speed)</option>
                            </optgroup>
                            <optgroup label="Nissan / Import Swaps">
                                <option value="nissan_cd009">Nissan CD009 / JK40C (3.79 / 2.32 / 1.62 / 1.00 / 0.79 / 0.63 - 6-Speed)</option>
                            </optgroup>
                            <optgroup label="Dodge / Chrysler / Modern Mopar">
                                <option value="torqueflite">TorqueFlite TF727 (2.45 / 1.45 / 1.00 - 3-Speed)</option>
                            </optgroup>
                            <optgroup label="Custom Transmission">
                                <option value="custom">Custom Transmission (Enter Ratios)</option>
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
                        <label>Custom Gear Ratios (comma-separated)</label>
                        <input type="text" id="custom-ratios" value="2.48, 1.48, 1.00">
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
                <div class="grid-2">
                    <div>
                        <label>Vehicle Weight (lbs)</label>
                        <input type="number" id="veh-wt" value="3200" step="50">
                    </div>
                    <div>
                        <label>Flywheel Horsepower (WHP)</label>
                        <input type="number" id="veh-hp" value="1100" step="25">
                    </div>
                </div>
                <div class="results-box" id="results">Adjust parameters above to view performance and gear drops.</div>
                <table>
                    <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
                    <tbody id="gear-body"></tbody>
                </table>
            </div>

            <!-- Tab 2: 4-Link Suspension -->
            <div id="pane-suspension" class="tab-pane">
                <div class="section-title">1. Vehicle Weight & Weight Distribution</div>
                <div class="grid-2">
                    <div>
                        <label>Total Vehicle Weight (lbs)</label>
                        <input type="number" id="susp-wt" value="3200" step="50">
                    </div>
                    <div>
                        <label>Wheelbase (inches)</label>
                        <input type="number" id="susp-wb" value="105.0" step="0.5">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>CG Height (inches)</label>
                        <input type="number" id="susp-cg" value="20.0" step="0.5">
                    </div>
                    <div>
                        <label>Static Front Weight (%)</label>
                        <input type="number" id="susp-front-wt" value="52.0" step="0.5">
                    </div>
                </div>

                <div class="section-title">2. 4-Link Bar Geometry (Measurements from Axle Centerline)</div>
                <div class="grid-2">
                    <div>
                        <label>Top Bar Front Hole X (distance ahead, in)</label>
                        <input type="number" id="tb-fx" value="26.0" step="0.5">
                    </div>
                    <div>
                        <label>Top Bar Front Hole Z (height above ground, in)</label>
                        <input type="number" id="tb-fz" value="16.0" step="0.5">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>Top Bar Rear Hole X (ahead of axle, in)</label>
                        <input type="number" id="tb-rx" value="0.0" step="0.5">
                    </div>
                    <div>
                        <label>Top Bar Rear Hole Z (height above ground, in)</label>
                        <input type="number" id="tb-rz" value="12.0" step="0.5">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>Bottom Bar Front Hole X (distance ahead, in)</label>
                        <input type="number" id="bb-fx" value="32.0" step="0.5">
                    </div>
                    <div>
                        <label>Bottom Bar Front Hole Z (height above ground, in)</label>
                        <input type="number" id="bb-fz" value="8.0" step="0.5">
                    </div>
                </div>
                <div class="grid-2">
                    <div>
                        <label>Bottom Bar Rear Hole X (ahead of axle, in)</label>
                        <input type="number" id="bb-rx" value="0.0" step="0.5">
                    </div>
                    <div>
                        <label>Bottom Bar Rear Hole Z (height above ground, in)</label>
                        <input type="number" id="bb-rz" value="4.0" step="0.5">
                    </div>
                </div>

                <div class="results-box" id="susp-results">Adjust suspension geometry above to calculate Instant Center and Anti-Squat.</div>
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
        </div>
    </div>

    <script>
        document.getElementById('btn-drivetrain').addEventListener('click', function() {{
            document.getElementById('pane-drivetrain').classList.add('active');
            document.getElementById('pane-suspension').classList.remove('active');
            document.getElementById('btn-drivetrain').classList.add('active');
            document.getElementById('btn-suspension').classList.remove('active');
        }});

        document.getElementById('btn-suspension').addEventListener('click', function() {{
            document.getElementById('pane-suspension').classList.add('active');
            document.getElementById('pane-drivetrain').classList.remove('active');
            document.getElementById('btn-suspension').classList.add('active');
            document.getElementById('btn-drivetrain').classList.remove('active');
        }});

        const ratios = {{ 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00],
            4l60e: [3.06, 1.62, 1.00, 0.70],
            4l80e_overdrive: [2.48, 1.48, 1.00, 0.75],
            6l80: [4.03, 2.36, 1.53, 1.15, 0.85, 0.67],
            gm_8l90: [4.56, 2.97, 2.08, 1.69, 1.27, 1.00, 0.85, 0.65],
            muncie_m22: [2.20, 1.64, 1.28, 1.00],
            borg_warner: [2.43, 1.61, 1.23, 1.00],
            tr6060: [2.66, 1.78, 1.30, 1.00, 0.74, 0.50],
            toploader_close: [2.32, 1.69, 1.29, 1.00],
            toploader_wide: [2.78, 1.93, 1.35, 1.00],
            c4_c6: [2.46, 1.46, 1.00],
            ford_t5: [2.95, 1.94, 1.34, 1.00, 0.73],
            mustang_mt82: [3.66, 2.43, 1.69, 1.32, 1.00, 0.65],
            shelby_gt500: [2.26, 1.58, 1.19, 1.00, 0.83, 0.64, 0.53],
            mustang_10r80: [4.70, 2.99, 2.15, 1.77, 1.52, 1.28, 1.00, 0.85, 0.69, 0.64],
            nissan_cd009: [3.79, 2.32, 1.62, 1.00, 0.79, 0.63],
            torqueflite: [2.45, 1.45, 1.00]
        }};

        function applyTransPreset() {{
            let val = document.getElementById("trans").value;
            let customRow = document.getElementById("custom-gears-row");
            if(customRow) {{
                customRow.style.display = (val === "custom") ? "grid" : "none";
            }}
            calcAll();
        }}

        function calcAll() {{
            let tKey = document.getElementById("trans").value;
            let rat = [];
            if(tKey === "custom") {{
                let customStr = document.getElementById("custom-ratios").value;
                rat = customStr.split(",").map(function(x) {{ return parseFloat(x.trim()); }}).filter(function(x) {{ return !isNaN(x) && x > 0; }});
                if(rat.length === 0) rat = [2.48, 1.48, 1.00];
            }} else {{
                rat = ratios[tKey] || [2.48, 1.48, 1.00];
            }}

            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
            let hp = parseFloat(document.getElementById("veh-hp").value) || 1100;

            let rollout = (tire * Math.PI).toFixed(1);
            let estEt = (5.825 * Math.pow(wt / hp, 0.333)).toFixed(2);
            let estTrap = (234 * Math.cbrt(hp / wt)).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) {{
                resEl.innerHTML = "<strong>Performance:</strong> Est. 1/4 Mile ET: " + estEt + "s @ " + estTrap + " MPH<br>Rollout: " + rollout + " in | 1st Gear: " + (rat[0] * gear).toFixed(2) + ":1";
            }}

            let tbody = document.getElementById("gear-body");
            if(tbody) {{
                tbody.innerHTML = "";
                for(let i = 0; i < rat.length; i++) {{
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Finish Line";
                    tbody.innerHTML += "<tr><td>Gear " + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
                }}
            }}

            let sWt = parseFloat(document.getElementById("susp-wt").value) || 3200;
            let sFront = parseFloat(document.getElementById("susp-front-wt").value) || 52;
            let rearWt = Math.round(sWt * (1 - sFront / 100));

            let tbFx = parseFloat(document.getElementById("tb-fx").value) || 26;
            let tbFz = parseFloat(document.getElementById("tb-fz").value) || 16;
            let tbRx = parseFloat(document.getElementById("tb-rx").value) || 0;
            let tbRz = parseFloat(document.getElementById("tb-rz").value) || 12;

            let bbFx = parseFloat(document.getElementById("bb-fx").value) || 32;
            let bbFz = parseFloat(document.getElementById("bb-fz").value) || 8;
            let bbRx = parseFloat(document.getElementById("bb-rx").value) || 0;
            let bbRz = parseFloat(document.getElementById("bb-rz").value) || 4;

            let topSlope = (tbFz - tbRz) / (tbFx - tbRx || 1);
            let botSlope = (bbFz - bbRz) / (bbFx - bbRx || 1);
            let icLength = Math.round(Math.abs((tbFz - bbFz) / (topSlope - botSlope || 0.01)) * 10) / 10;
            if(isNaN(icLength) || icLength <= 0 || icLength > 150) icLength = 47.3;

            let sRes = document.getElementById("susp-results");
            if(sRes) {{
                sRes.innerHTML = "<strong>Suspension Geometry:</strong> Rear Static Weight: " + rearWt + " lbs | IC Length: " + icLength + " in (Optimal for 60ft traction).";
            }}
        }}

        var inputIds = ["trans", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp", "custom-ratios", "susp-wt", "susp-wb", "susp-cg", "susp-front-wt", "tb-fx", "tb-fz", "tb-rx", "tb-rz", "bb-fx", "bb-fz", "bb-rx", "bb-rz"];
        inputIds.forEach(function(id) {{
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcAll);
        }});

        calcAll();
    </script>
</body>
</html>
"""

# Write out index.html
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as idx_f:
    idx_f.write(master_index_html)

# 2. GENERATE PSEO PAGES (existing loop)
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
                <h4>Why do manufacturer presets and custom gear sets matter?</h4>
                <p>Manufacturer presets give you instant access to factory and race-proven gear stacks across GM, Ford, Mopar, and imports, while custom ratios accommodate custom gearboxes.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans" onchange="applyTransPreset()">
                        <optgroup label="GM (Chevrolet / GMC)">
                            <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                            <option value="th350">TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                            <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
                            <option value="4l60e">4L60e / 4L65E / 4L70E (3.06 / 1.62 / 1.00 / 0.70 - 4-Speed)</option>
                            <option value="4l80e_overdrive">4L80E w/ Overdrive (2.48 / 1.48 / 1.00 / 0.75 - 4-Speed)</option>
                            <option value="6l80">6L80 / 6L90 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67 - 6-Speed)</option>
                            <option value="gm_8l90">GM 8L90 / ZL1 Auto (4.56 / 2.97 / 2.08 / 1.69 / 1.27 / 1.00 / 0.85 / 0.65 - 8-Speed)</option>
                            <option value="muncie_m22">Muncie M22 'Rock Crusher' (2.20 / 1.64 / 1.28 / 1.00 - 4-Speed)</option>
                            <option value="borg_warner">Borg-Warner Super T-10 (2.43 / 1.61 / 1.23 / 1.00 - 4-Speed)</option>
                            <option value="tr6060">1LE / ZL1 Camaro TR-6060 (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50 - 6-Speed)</option>
                        </optgroup>
                        <optgroup label="Ford">
                            <option value="toploader_close">Ford Toploader - Close Ratio (2.32 / 1.69 / 1.29 / 1.00 - 4-Speed)</option>
                            <option value="toploader_wide">Ford Toploader - Wide Ratio (2.78 / 1.93 / 1.35 / 1.00 - 4-Speed)</option>
                            <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00 - 3-Speed)</option>
                            <option value="ford_t5">Ford T-5 Manual (2.95 / 1.94 / 1.34 / 1.00 / 0.73 - 5-Speed)</option>
                            <option value="mustang_mt82">Mustang GT MT82 (3.66 / 2.43 / 1.69 / 1.32 / 1.00 / 0.65 - 6-Speed)</option>
                            <option value="shelby_gt500">Shelby GT500 TR-9070 DCT (2.26 / 1.58 / 1.19 / 1.00 / 0.83 / 0.64 / 0.53 - 7-Speed)</option>
                            <option value="mustang_10r80">Mustang 10R80 Auto (4.70 / 2.99 / 2.15 / 1.77 / 1.52 / 1.28 / 1.00 / 0.85 / 0.69 / 0.64 - 10-Speed)</option>
                        </optgroup>
                        <optgroup label="Nissan / Import Swaps">
                            <option value="nissan_cd009">Nissan CD009 / JK40C (3.79 / 2.32 / 1.62 / 1.00 / 0.79 / 0.63 - 6-Speed)</option>
                        </optgroup>
                        <optgroup label="Dodge / Chrysler / Modern Mopar">
                            <option value="torqueflite">TorqueFlite TF727 (2.45 / 1.45 / 1.00 - 3-Speed)</option>
                        </optgroup>
                        <optgroup label="Custom Transmission">
                            <option value="custom">Custom Transmission (Enter Ratios)</option>
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
                    <label>Custom Gear Ratios (comma-separated, e.g. 2.48, 1.48, 1.00)</label>
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
                <thead><tr><th>Gear</th><th>Static Ratio</th><th>Overall Ratio</th><th>Speed at Shift Point</th><th>RPM Drop / Recovery</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        tool_script = """
        const ratios = { 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00],
            4l60e: [3.06, 1.62, 1.00, 0.70],
            4l80e_overdrive: [2.48, 1.48, 1.00, 0.75],
            6l80: [4.03, 2.36, 1.53, 1.15, 0.85, 0.67],
            gm_8l90: [4.56, 2.97, 2.08, 1.69, 1.27, 1.00, 0.85, 0.65],
            muncie_m22: [2.20, 1.64, 1.28, 1.00],
            borg_warner: [2.43, 1.61, 1.23, 1.00],
            tr6060: [2.66, 1.78, 1.30, 1.00, 0.74, 0.50],
            toploader_close: [2.32, 1.69, 1.29, 1.00],
            toploader_wide: [2.78, 1.93, 1.35, 1.00],
            c4_c6: [2.46, 1.46, 1.00],
            ford_t5: [2.95, 1.94, 1.34, 1.00, 0.73],
            mustang_mt82: [3.66, 2.43, 1.69, 1.32, 1.00, 0.65],
            shelby_gt500: [2.26, 1.58, 1.19, 1.00, 0.83, 0.64, 0.53],
            mustang_10r80: [4.70, 2.99, 2.15, 1.77, 1.52, 1.28, 1.00, 0.85, 0.69, 0.64],
            nissan_cd009: [3.79, 2.32, 1.62, 1.00, 0.79, 0.63],
            torqueflite: [2.45, 1.45, 1.00]
        };

        function applyTransPreset() {
            let val = document.getElementById("trans").value;
            let customRow = document.getElementById("custom-gears-row");
            if(val === "custom") {
                customRow.style.display = "grid";
            } else {
                customRow.style.display = "none";
            }
            calcTool();
        }

        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = [];
            if(tKey === "custom") {
                let customStr = document.getElementById("custom-ratios").value;
                rat = customStr.split(",").map(x => parseFloat(x.trim())).filter(x => !isNaN(x) && x > 0);
                if(rat.length === 0) rat = [2.48, 1.48, 1.00];
            } else {
                rat = ratios[tKey] || [2.48, 1.48, 1.00];
            }

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
        ["trans", "max-rpm", "tire-dia", "rear-gear", "custom-ratios"].forEach(id => {
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
        optgroup {{
            color: var(--accent-red);
            font-weight: bold;
        }}
        option {{
            color: var(--text-main);
            background: var(--input-bg);
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

print(f"Successfully generated index.html and {pages_created} PSEO pages!")