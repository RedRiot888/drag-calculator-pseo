import os
import csv

output_dir = "."

csv_content = """slug,target_keyword,category,rear_gear,tire_diameter
transmission-shift-recovery-calculator,Transmission Shift Recovery & Gear Drop Calculator,Transmission,3.42,28.0
turbo-sizing-calculator,Turbo Sizing & Turbocharger Matching Calculator,Turbo,3.42,28.0
supercharger-pulley-calculator,Supercharger Pulley Ratio & Boost Pressure Calculator,Supercharger,3.42,28.0
rear-gear-calculator,Ring and Pinion Rear Gear Quarter-Mile Calculator,RearGear,4.11,32.0
tire-growth-calculator,Tire Diameter Growth & Rollout Drag Calculator,Tire,3.42,28.0
wastegate-sizing-calculator,Wastegate Sizing & Boost Control Calculator,Wastegate,3.42,28.0
"""
with open("pseo_pages_list.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages = list(reader)

utilities_grid_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">\n'
for row in pages:
    slug = row["slug"]
    keyword = row["target_keyword"]
    cat = row["category"]
    
    icon = "⚙️"
    if "Turbo" in cat: icon = "🌀"
    elif "Supercharger" in cat: icon = "⚡"
    elif "Rear" in cat: icon = "🔧"
    elif "Tire" in cat: icon = "🛞"
    elif "Transmission" in cat: icon = "🏎️"
    elif "Wastegate" in cat: icon = "🎛️"
    
    utilities_grid_html += f'''
    <a href="{slug}.html" style="background: var(--input-bg); border: 1px solid var(--border-color); padding: 12px 10px; border-radius: 8px; text-decoration: none; display: flex; flex-direction: column; gap: 4px; transition: all 0.2s ease;">
        <span style="font-size: 1.1rem;">{icon}</span>
        <span style="font-size: 0.78rem; font-weight: bold; color: var(--text-main); line-height: 1.2;">{keyword}</span>
    </a>
'''
utilities_grid_html += '</div>\n'

ad_block_html = """
            <div class="content-box" style="text-align: center; background: #121418; border: 1px dashed var(--border-color);">
                <h3 style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">Advertisement Space</h3>
                <div style="padding: 20px 10px; color: var(--text-muted); font-size: 0.8rem; background: var(--input-bg); border-radius: 6px;">
                    Your Ad Here<br>Contact for Track Sponsor Rates
                </div>
            </div>
"""

partners_html = """
            <div class="content-box">
                <h3>Featured Partners</h3>
                <ul class="sponsor-list" style="list-style: none; padding: 0; margin: 0; font-size: 0.9rem; color: var(--text-muted);">
                    <li style="padding: 8px 0; border-bottom: 1px dashed var(--border-color);"><a href="#" style="color: var(--text-muted); text-decoration: none;">Pro-Comp Race Transmissions</a></li>
                    <li style="padding: 8px 0; border-bottom: 1px dashed var(--border-color);"><a href="#" style="color: var(--text-muted); text-decoration: none;">Precision Turbo & Engine</a></li>
                    <li style="padding: 8px 0;"><a href="#" style="color: var(--text-muted); text-decoration: none;">DragStrip Tire & Compound Tech</a></li>
                </ul>
            </div>
"""

tuning_guides_html = """
            <div class="content-box">
                <h3>Track-Side Tuning Cheat Sheets</h3>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Essential round-by-round reference guides for the trailer:</p>
                
                <div style="margin-bottom: 12px; border-bottom: 1px dashed var(--border-color); padding-bottom: 10px;">
                    <strong style="color: var(--text-main); font-size: 0.85rem;">1. Density Altitude (DA) & Weather</strong>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">Every 1,000 ft increase in DA costs naturally aspirated engines ~3% horsepower. Forced induction setups compensate better via wastegate control, but watch inlet air temps.</p>
                </div>

                <div style="margin-bottom: 12px; border-bottom: 1px dashed var(--border-color); padding-bottom: 10px;">
                    <strong style="color: var(--text-main); font-size: 0.85rem;">2. Torque Converter Slip</strong>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">Target 5% to 8% slip at the finish line for max efficiency. Excessive slip generates transmission heat and kills trap speed; too tight kills 60-foot times.</p>
                </div>

                <div style="margin-bottom: 12px; border-bottom: 1px dashed var(--border-color); padding-bottom: 10px;">
                    <strong style="color: var(--text-main); font-size: 0.85rem;">3. Boost & Nitro Management</strong>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">Read spark plug ground straps for heat mark placement. Back off timing 1 to 2 degrees per additional 3–4 PSI of boost or when stepping up nitrous jetting.</p>
                </div>

                <div>
                    <strong style="color: var(--text-main); font-size: 0.85rem;">4. 4-Link Anti-Squat & Launch</strong>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">If the car bounces or unloads the tires immediately on launch, lower the instantaneous center (IC) or soften rear shock extension.</p>
                </div>
            </div>
"""

# 1. MASTER index.html HUB
master_index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Drivetrain & Shift RPM Calculator Suite</title>
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
        .layout-grid {
            max-width: 1200px;
            margin: 30px auto;
            display: grid;
            grid-template-columns: 500px 1fr;
            gap: 30px;
            align-items: start;
        }
        @media (max-width: 900px) {
            .layout-grid { grid-template-columns: 1fr; }
        }
        .sticky-calculator {
            position: sticky;
            top: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .content-column {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .content-box {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 25px;
        }
        .content-box h3 {
            color: var(--accent-red);
            font-size: 0.95rem;
            text-transform: uppercase;
            margin-top: 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
        }
        .master-header {
            text-align: center;
            margin-bottom: 5px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }
        .master-header h1 {
            color: var(--accent-red);
            font-size: 1.3rem;
            text-transform: uppercase;
            margin: 0 0 3px 0;
        }
        .master-header p {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin: 0;
        }
        .tab-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }
        .tab-btn {
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 10px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.75rem;
            cursor: pointer;
            text-transform: uppercase;
            text-align: center;
        }
        .tab-btn.active {
            background: var(--accent-red);
            color: white;
            border-color: var(--accent-red);
        }
        .tab-pane {
            display: none;
        }
        .tab-pane.active {
            display: block;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 8px;
        }
        label {
            display: block;
            margin-bottom: 2px;
            font-weight: 600;
            font-size: 0.72rem;
            color: var(--text-muted);
        }
        input, select {
            width: 100%;
            padding: 7px 9px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.82rem;
        }
        optgroup { color: var(--accent-red); font-weight: bold; }
        option { color: var(--text-main); background: var(--input-bg); }
        .results-box {
            margin-top: 10px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 10px;
            border-radius: 6px;
            font-size: 0.82rem;
        }
        .action-btn {
            width: 100%;
            margin-top: 10px;
            background: var(--accent-red);
            color: white;
            border: none;
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.75rem;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .action-btn:hover { background: #e0161f; }
        table {
            width: 100%;
            margin-top: 12px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 5px 4px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.72rem;
        }
        th {
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.62rem;
        }
        .section-title {
            color: var(--accent-red);
            font-size: 0.78rem;
            text-transform: uppercase;
            border-bottom: 1px dashed var(--border-color);
            margin: 12px 0 6px 0;
            padding-bottom: 3px;
        }
        @media print {
            body { background: white; color: black; padding: 0; }
            .sticky-calculator { border: none; box-shadow: none; background: white; padding: 0; position: static; }
            .content-column, .tab-buttons, .action-btn { display: none; }
            input, select { border: 1px solid #ccc; background: white; color: black; }
        }
    </style>
</head>
<body>
    <div class="layout-grid">
        <div class="sticky-calculator">
            <div>
                <div class="master-header">
                    <h1>Ultimate Drag Racing Suite</h1>
                    <p>Professional Track Tuning Engine</p>
                </div>

                <div class="tab-buttons">
                    <button type="button" class="tab-btn active" id="btn-drivetrain">Drivetrain & Shift</button>
                    <button type="button" class="tab-btn" id="btn-suspension">4-Link Suspension</button>
                </div>

                <div id="pane-drivetrain" class="tab-pane active">
                    <div class="grid-2">
                        <div>
                            <label>Transmission Profile</label>
                            <select id="trans" onchange="applyTransPreset()">
                                <optgroup label="Custom">
                                    <option value="custom">Custom Ratios</option>
                                </optgroup>
                                <optgroup label="GM Automatic">
                                    <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                                    <option value="th350">TH350 (2.52 / 1.52 / 1.00)</option>
                                    <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                                    <option value="4l60e">4L60e (3.06 / 1.62 / 1.00 / 0.70)</option>
                                    <option value="6l80">6L80 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67)</option>
                                    <option value="8l90">8L90 (4.56 / 2.97 / 2.08 / 1.69 / 1.27 / 1.00 / 0.85 / 0.65)</option>
                                    <option value="10l90">10L90 (4.70 / 2.98 / 2.14 / 1.77 / 1.52 / 1.27 / 1.00 / 0.85 / 0.69 / 0.64)</option>
                                </optgroup>
                                <optgroup label="Ford Automatic">
                                    <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00)</option>
                                    <option value="aod">AOD (2.40 / 1.47 / 1.00 / 0.67)</option>
                                    <option value="4r70w">4R70W (2.84 / 1.55 / 1.00 / 0.70)</option>
                                    <option value="mustang_10r80">Mustang 10R80 (4.70 / 2.99 / 2.15 / 1.77 / 1.52 / 1.28 / 1.00 / 0.85 / 0.69 / 0.64)</option>
                                </optgroup>
                                <optgroup label="Mopar Automatic">
                                    <option value="torque_727">Torqueflite 727 (2.45 / 1.45 / 1.00)</option>
                                </optgroup>
                                <optgroup label="Manuals">
                                    <option value="ford_t5">Ford T-5 (2.95 / 1.94 / 1.34 / 1.00 / 0.73)</option>
                                    <option value="t56">T56 / TR-6060 (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50)</option>
                                    <option value="tremec_tkx">Tremec TKX (2.87 / 1.89 / 1.28 / 1.00 / 0.68)</option>
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
                            <label>Tire Diameter (in)</label>
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
                            <label>Flywheel HP</label>
                            <input type="number" id="veh-hp" value="1100" step="25">
                        </div>
                    </div>
                    <div class="results-box" id="results">Adjust parameters above to view performance.</div>
                    <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
                    <table>
                        <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
                        <tbody id="gear-body"></tbody>
                    </table>
                </div>

                <div id="pane-suspension" class="tab-pane">
                    <div class="section-title">1. Vehicle Weight & Distribution</div>
                    <div class="grid-2">
                        <div>
                            <label>Total Weight (lbs)</label>
                            <input type="number" id="susp-wt" value="3200" step="50">
                        </div>
                        <div>
                            <label>Wheelbase (in)</label>
                            <input type="number" id="susp-wb" value="105.0" step="0.5">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label>CG Height (in)</label>
                            <input type="number" id="susp-cg" value="20.0" step="0.5">
                        </div>
                        <div>
                            <label>Static Front Weight (%)</label>
                            <input type="number" id="susp-front-wt" value="52.0" step="0.5">
                        </div>
                    </div>

                    <div class="section-title">2. 4-Link Bar Geometry</div>
                    <div class="grid-2">
                        <div>
                            <label>Top Bar Front X (in)</label>
                            <input type="number" id="tb-fx" value="26.0" step="0.5">
                        </div>
                        <div>
                            <label>Top Bar Front Z (in)</label>
                            <input type="number" id="tb-fz" value="16.0" step="0.5">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label>Top Bar Rear X (in)</label>
                            <input type="number" id="tb-rx" value="0.0" step="0.5">
                        </div>
                        <div>
                            <label>Top Bar Rear Z (in)</label>
                            <input type="number" id="tb-rz" value="12.0" step="0.5">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label>Bottom Bar Front X (in)</label>
                            <input type="number" id="bb-fx" value="32.0" step="0.5">
                        </div>
                        <div>
                            <label>Bottom Bar Front Z (in)</label>
                            <input type="number" id="bb-fz" value="8.0" step="0.5">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div>
                            <label>Bottom Bar Rear X (in)</label>
                            <input type="number" id="bb-rx" value="0.0" step="0.5">
                        </div>
                        <div>
                            <label>Bottom Bar Rear Z (in)</label>
                            <input type="number" id="bb-rz" value="4.0" step="0.5">
                        </div>
                    </div>

                    <div class="results-box" id="susp-results">Adjust suspension geometry above.</div>
                    <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Suspension Sheet</button>
                </div>
            </div>

            REPLACE_STICKY_AD
        </div>

        <div class="content-column">
            REPLACE_TOP_AD
            <div class="content-box">
                <h3>Other Utilities & Calculators</h3>
                REPLACE_UTILITIES_GRID
            </div>
            REPLACE_TUNING_GUIDES
            REPLACE_PARTNERS
            REPLACE_BOTTOM_AD
        </div>
    </div>

    <script>
        document.getElementById('btn-drivetrain').addEventListener('click', function() {
            document.getElementById('pane-drivetrain').classList.add('active');
            document.getElementById('pane-suspension').classList.remove('active');
            document.getElementById('btn-drivetrain').classList.add('active');
            document.getElementById('btn-suspension').classList.remove('active');
        });

        document.getElementById('btn-suspension').addEventListener('click', function() {
            document.getElementById('pane-suspension').classList.add('active');
            document.getElementById('pane-drivetrain').classList.remove('active');
            document.getElementById('btn-suspension').classList.add('active');
            document.getElementById('btn-drivetrain').classList.remove('active');
        });

        const ratios = { 
            powerglide: [1.76, 1.00], 
            th350: [2.52, 1.52, 1.00], 
            th400: [2.48, 1.48, 1.00],
            "4l60e": [3.06, 1.62, 1.00, 0.70],
            "6l80": [4.03, 2.36, 1.53, 1.15, 0.85, 0.67],
            "8l90": [4.56, 2.97, 2.08, 1.69, 1.27, 1.00, 0.85, 0.65],
            "10l90": [4.70, 2.98, 2.14, 1.77, 1.52, 1.27, 1.00, 0.85, 0.69, 0.64],
            c4_c6: [2.46, 1.46, 1.00],
            aod: [2.40, 1.47, 1.00, 0.67],
            "4r70w": [2.84, 1.55, 1.00, 0.70],
            mustang_10r80: [4.70, 2.99, 2.15, 1.77, 1.52, 1.28, 1.00, 0.85, 0.69, 0.64],
            torque_727: [2.45, 1.45, 1.00],
            ford_t5: [2.95, 1.94, 1.34, 1.00, 0.73],
            t56: [2.66, 1.78, 1.30, 1.00, 0.74, 0.50],
            tremec_tkx: [2.87, 1.89, 1.28, 1.00, 0.68]
        };

        function applyTransPreset() {
            let val = document.getElementById("trans").value;
            let customRow = document.getElementById("custom-gears-row");
            if(customRow) {
                customRow.style.display = (val === "custom") ? "grid" : "none";
            }
            calcAll();
        }

        function calcAll() {
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
            let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
            let hp = parseFloat(document.getElementById("veh-hp").value) || 1100;

            let rollout = (tire * Math.PI).toFixed(1);
            let estEt = (5.825 * Math.pow(wt / hp, 0.333)).toFixed(2);
            let estTrap = (234 * Math.cbrt(hp / wt)).toFixed(1);

            let resEl = document.getElementById("results");
            if(resEl) {
                resEl.innerHTML = "Est. 1/4 Mile ET: " + estEt + "s @ " + estTrap + " MPH | Rollout: " + rollout + " in";
            }

            let tbody = document.getElementById("gear-body");
            if(tbody) {
                tbody.innerHTML = "";
                for(let i = 0; i < rat.length; i++) {
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Finish";
                    tbody.innerHTML += "<tr><td>" + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
                }
            }

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
            if(sRes) {
                sRes.innerHTML = "Rear Static Weight: " + rearWt + " lbs | IC Length: " + icLength + " in";
            }
        }

        ["trans", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp", "custom-ratios", "susp-wt", "susp-wb", "susp-cg", "susp-front-wt", "tb-fx", "tb-fz", "tb-rx", "tb-rz", "bb-fx", "bb-fz", "bb-rx", "bb-rz"].forEach(function(id) {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcAll);
        });

        calcAll();
    </script>
</body>
</html>
"""

master_index_html = (
    master_index_html.replace("REPLACE_UTILITIES_GRID", utilities_grid_html)
    .replace("REPLACE_STICKY_AD", ad_block_html)
    .replace("REPLACE_TOP_AD", ad_block_html)
    .replace("REPLACE_BOTTOM_AD", ad_block_html)
    .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
    .replace("REPLACE_PARTNERS", partners_html)
)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(master_index_html)

# 2. PSEO SUB-PAGES TEMPLATE
base_html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TARGET_KEYWORD | Ultimate Drag Racing Master Suite</title>
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
        .layout-grid {
            max-width: 1200px;
            margin: 30px auto;
            display: grid;
            grid-template-columns: 480px 1fr;
            gap: 30px;
            align-items: start;
        }
        @media (max-width: 900px) {
            .layout-grid { grid-template-columns: 1fr; }
        }
        .sticky-calculator {
            position: sticky;
            top: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .content-column {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .content-box {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 25px;
        }
        .content-box h3 {
            color: var(--accent-red);
            font-size: 0.95rem;
            text-transform: uppercase;
            margin-top: 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
        }
        .master-header {
            text-align: center;
            margin-bottom: 5px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }
        .master-header h1 {
            color: var(--accent-red);
            font-size: 1.3rem;
            text-transform: uppercase;
            margin: 0 0 3px 0;
        }
        .master-header p {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin: 0;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 8px;
        }
        label {
            display: block;
            margin-bottom: 2px;
            font-weight: 600;
            font-size: 0.72rem;
            color: var(--text-muted);
        }
        input, select {
            width: 100%;
            padding: 7px 9px;
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.82rem;
        }
        optgroup { color: var(--accent-red); font-weight: bold; }
        option { color: var(--text-main); background: var(--input-bg); }
        .results-box {
            margin-top: 10px;
            background: #121418;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-red);
            padding: 10px;
            border-radius: 6px;
            font-size: 0.82rem;
        }
        .action-btn {
            width: 100%;
            margin-top: 10px;
            background: var(--accent-red);
            color: white;
            border: none;
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.75rem;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .action-btn:hover { background: #e0161f; }
        .formula-content {
            font-family: monospace;
            color: #10b981;
            font-size: 0.85rem;
            background: var(--input-bg);
            padding: 10px;
            border-radius: 6px;
        }
        .faq-item { margin-bottom: 12px; }
        .faq-item h4 { margin: 0 0 3px 0; font-size: 0.85rem; color: var(--text-main); }
        .faq-item p { margin: 0; font-size: 0.8rem; color: var(--text-muted); }
        table {
            width: 100%;
            margin-top: 12px;
            border-collapse: collapse;
            background: #121418;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 5px 4px;
            border: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.72rem;
        }
        th {
            background: #1f232b;
            color: var(--accent-red);
            text-transform: uppercase;
            font-size: 0.62rem;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 15px;
            color: var(--accent-red);
            text-decoration: none;
            font-weight: bold;
            font-size: 0.85rem;
        }
        .back-link:hover { text-decoration: underline; }
        @media print {
            body { background: white; color: black; padding: 0; }
            .sticky-calculator { border: none; box-shadow: none; background: white; padding: 0; position: static; }
            .content-column, .back-link, .action-btn { display: none; }
            input, select { border: 1px solid #ccc; background: white; color: black; }
        }
    </style>
</head>
<body>
    <div style="max-width: 1200px; margin: 0 auto;">
        <a href="index.html" class="back-link">&larr; Back to Master Hub</a>
    </div>

    <div class="layout-grid">
        <div class="sticky-calculator">
            <div>
                <div class="master-header">
                    <h1>PRIMARY_TITLE</h1>
                    <p>TARGET_KEYWORD &mdash; Track Tuning Engine</p>
                </div>
                PRIMARY_TOOL_HTML
            </div>
            REPLACE_STICKY_AD
        </div>

        <div class="content-column">
            REPLACE_TOP_AD
            <div class="content-box">
                <h3>Other Utilities & Calculators</h3>
                REPLACE_UTILITIES_GRID
            </div>
            REPLACE_TUNING_GUIDES
            <div class="content-box">
                <h3>Formula Breakdown</h3>
                <div class="formula-content">FORMULA_TEXT</div>
            </div>
            <div class="content-box">
                <h3>Frequently Asked Questions</h3>
                FAQS_HTML
            </div>
            REPLACE_PARTNERS
            REPLACE_BOTTOM_AD
        </div>
    </div>

    <script>
        TOOL_SCRIPT
    </script>
</body>
</html>
"""

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
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans" onchange="applyTransPreset()">
                        <optgroup label="Custom">
                            <option value="custom">Custom Ratios</option>
                        </optgroup>
                        <optgroup label="GM Automatic">
                            <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                            <option value="th350">TH350 (2.52 / 1.52 / 1.00)</option>
                            <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                            <option value="4l60e">4L60e (3.06 / 1.62 / 1.00 / 0.70)</option>
                            <option value="6l80">6L80 (4.03 / 2.36 / 1.53 / 1.15 / 0.85 / 0.67)</option>
                            <option value="8l90">8L90 (4.56 / 2.97 / 2.08 / 1.69 / 1.27 / 1.00 / 0.85 / 0.65)</option>
                            <option value="10l90">10L90 (4.70 / 2.98 / 2.14 / 1.77 / 1.52 / 1.27 / 1.00 / 0.85 / 0.69 / 0.64)</option>
                        </optgroup>
                        <optgroup label="Ford Automatic">
                            <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00)</option>
                            <option value="aod">AOD (2.40 / 1.47 / 1.00 / 0.67)</option>
                            <option value="4r70w">4R70W (2.84 / 1.55 / 1.00 / 0.70)</option>
                            <option value="mustang_10r80">Mustang 10R80 (4.70 / 2.99 / 2.15 / 1.77 / 1.52 / 1.28 / 1.00 / 0.85 / 0.69 / 0.64)</option>
                        </optgroup>
                        <optgroup label="Mopar Automatic">
                            <option value="torque_727">Torqueflite 727 (2.45 / 1.45 / 1.00)</option>
                        </optgroup>
                        <optgroup label="Manuals">
                            <option value="ford_t5">Ford T-5 (2.95 / 1.94 / 1.34 / 1.00 / 0.73)</option>
                            <option value="t56">T56 / TR-6060 (2.66 / 1.78 / 1.30 / 1.00 / 0.74 / 0.50)</option>
                            <option value="tremec_tkx">Tremec TKX (2.87 / 1.89 / 1.28 / 1.00 / 0.68)</option>
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
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
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
            "8l90": [4.56, 2.97, 2.08, 1.69, 1.27, 1.00, 0.85, 0.65],
            "10l90": [4.70, 2.98, 2.14, 1.77, 1.52, 1.27, 1.00, 0.85, 0.69, 0.64],
            c4_c6: [2.46, 1.46, 1.00],
            aod: [2.40, 1.47, 1.00, 0.67],
            "4r70w": [2.84, 1.55, 1.00, 0.70],
            mustang_10r80: [4.70, 2.99, 2.15, 1.77, 1.52, 1.28, 1.00, 0.85, 0.69, 0.64],
            torque_727: [2.45, 1.45, 1.00],
            ford_t5: [2.95, 1.94, 1.34, 1.00, 0.73],
            t56: [2.66, 1.78, 1.30, 1.00, 0.74, 0.50],
            tremec_tkx: [2.87, 1.89, 1.28, 1.00, 0.68]
        };
        function applyTransPreset() {
            let val = document.getElementById("trans").value;
            let customRow = document.getElementById("custom-gears-row");
            if(customRow) { customRow.style.display = (val === "custom") ? "grid" : "none"; }
            calcTool();
        }
        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = tKey === "custom" ? (document.getElementById("custom-ratios").value.split(",").map(x => parseFloat(x.trim())).filter(x => !isNaN(x) && x > 0) || [2.48, 1.48, 1.00]) : (ratios[tKey] || [2.48, 1.48, 1.00]);
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let rollout = (tire * Math.PI).toFixed(1);
            let resEl = document.getElementById("results");
            if(resEl) resEl.innerHTML = "Tire Rollout: " + rollout + " in | 1st Gear Ratio: " + (rat[0] * gear).toFixed(2) + ":1";
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
        ["trans", "max-rpm", "tire-dia", "rear-gear", "custom-ratios"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "RearGear":
        primary_title = "Ring and Pinion Rear Gear Quarter-Mile Calculator"
        formula_text = "Finish Line RPM = (Trap Speed x Rear Gear x 336) / Tire Diameter"
        faqs = '<div class="faq-item"><h4>How does gear ratio affect finish line RPM?</h4><p>Higher numeric gears increase finish line RPM.</p></div>'
        primary_tool_html = f"""
            <div class="grid-2">
                <div><label>Target Trap Speed (MPH)</label><input type="number" id="trap" value="125" step="1"></div>
                <div><label>Rear Gear Ratio</label><input type="number" id="gear" value="{gear}" step="0.01"></div>
            </div>
            <div class="grid-2">
                <div><label>Tire Diameter (in)</label><input type="number" id="tire" value="{tire}" step="0.1"></div>
                <div><label>Trans Final Ratio</label><input type="number" id="trans-final" value="1.00" step="0.01"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
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
            document.getElementById("results").innerHTML = "Overall Ratio: <strong>" + overall.toFixed(2) + ":1</strong> | Rollout: <strong>" + rollout + " in</strong> | Finish RPM: <strong>" + Math.round(finishRpm) + " RPM</strong>";
        }
        ["trap", "gear", "tire", "trans-final"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbo Sizing & Turbocharger Matching Calculator"
        formula_text = "Required Airflow (lb/min) = (Target Flywheel HP x BSFC) / 6.0<br>Pressure Ratio = (Target Boost + 14.7) / 14.7"
        faqs = '<div class="faq-item"><h4>How do I choose turbo size?</h4><p>Match total required airflow in lb/min and pressure ratio to compressor maps.</p></div>'
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Engine Displacement (L)</label><input type="number" id="disp" value="5.3" step="0.1"></div>
                <div><label>Target Flywheel HP</label><input type="number" id="hp" value="1000" step="50"></div>
            </div>
            <div class="grid-2">
                <div><label>Max Boost RPM</label><input type="number" id="rpm" value="7000" step="100"></div>
                <div><label>Target Boost (PSI)</label><input type="number" id="boost" value="22" step="1"></div>
            </div>
            <div class="grid-2">
                <div><label>Fuel BSFC</label><select id="bsfc"><option value="0.60">Gasoline (0.60)</option><option value="0.85" selected>E85 (0.85)</option></select></div>
                <div><label>Turbo Count</label><select id="turbos"><option value="1" selected>Single</option><option value="2">Twin</option></select></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; margin-top: 10px; font-size: 0.78rem;" id="turbo-rec">
                <strong>Turbo Recommendation:</strong> Loading...
            </div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let disp = parseFloat(document.getElementById("disp").value) || 5.3;
            let hp = parseFloat(document.getElementById("hp").value) || 1000;
            let rpm = parseFloat(document.getElementById("rpm").value) || 7000;
            let boost = parseFloat(document.getElementById("boost").value) || 22;
            let bsfc = parseFloat(document.getElementById("bsfc").value) || 0.85;
            let count = parseInt(document.getElementById("turbos").value) || 1;
            
            let totalAirflow = (hp * bsfc) / 6.0;
            let perTurbo = totalAirflow / count;
            let pr = (boost + 14.7) / 14.7;
            
            let rec = "Small Frame (T3 / 55-61mm)";
            let ar = "0.63 - 0.82 A/R";
            if(perTurbo > 85) {
                rec = "Large Frame (T6 / Pro Mod 80mm+)";
                ar = "1.10 - 1.41 A/R";
            } else if(perTurbo > 50) {
                rec = "Medium Frame (T4 / 62-76mm)";
                ar = "0.82 - 1.00 A/R";
            }
            
            document.getElementById("results").innerHTML = "Required Airflow: <strong>" + totalAirflow.toFixed(1) + " lb/min</strong> (" + perTurbo.toFixed(1) + " per turbo) | Pressure Ratio: <strong>" + pr.toFixed(2) + ":1</strong>";
            document.getElementById("turbo-rec").innerHTML = "<strong>Turbo Recommendation:</strong> " + rec + "<br><span style='color: var(--text-muted);'>Suggested Turbine A/R: <strong>" + ar + "</strong></span>";
        }
        ["disp", "hp", "rpm", "boost", "bsfc", "turbos"].forEach(id => {
            let el = document.getElementById(id);
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
        });
        calcTool();
        """
    elif category == "Supercharger":
        primary_title = "Supercharger Pulley Ratio & Boost Pressure Calculator"
        formula_text = "Pulley Ratio = Crank Pulley Diameter / Blower Pulley Diameter"
        faqs = '<div class="faq-item"><h4>How to increase boost?</h4><p>Install a smaller blower pulley.</p></div>'
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Crank Pulley Dia (in)</label><input type="number" id="crank-dia" value="8.0" step="0.1"></div>
                <div><label>Blower Pulley Dia (in)</label><input type="number" id="blower-dia" value="3.0" step="0.1"></div>
            </div>
            <div class="grid-2">
                <div><label>Max Crank RPM</label><input type="number" id="crank-rpm" value="6500" step="100"></div>
                <div><label>Boost Factor</label><input type="number" id="boost-fac" value="1.45" step="0.05"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let crank = parseFloat(document.getElementById("crank-dia").value) || 8.0;
            let blower = parseFloat(document.getElementById("blower-dia").value) || 3.0;
            let rpm = parseFloat(document.getElementById("crank-rpm").value) || 6500;
            let factor = parseFloat(document.getElementById("boost-fac").value) || 1.45;
            let ratio = crank / blower;
            let estBoost = (ratio * 5.2 * factor).toFixed(1);
            document.getElementById("results").innerHTML = "Pulley Ratio: <strong>" + ratio.toFixed(2) + ":1</strong> | Est. Boost: <strong>" + estBoost + " PSI</strong>";
        }
        ["crank-dia", "blower-dia", "crank-rpm", "boost-fac"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Tire":
        primary_title = "Tire Diameter Growth & Rollout Drag Calculator"
        formula_text = "Dynamic Diameter = Static Diameter x (1 + (Growth % / 100))"
        faqs = '<div class="faq-item"><h4>Why do tires grow?</h4><p>Centrifugal force expands the tire at speed.</p></div>'
        primary_tool_html = f"""
            <div class="grid-2">
                <div><label>Static Tire Dia (in)</label><input type="number" id="static-dia" value="{tire}" step="0.1"></div>
                <div><label>Trap Speed (MPH)</label><input type="number" id="trap-speed" value="150" step="1"></div>
            </div>
            <div class="grid-2">
                <div><label>Growth Factor (%)</label><input type="number" id="growth-fac" value="4.5" step="0.1"></div>
                <div><label>Rear Gear Ratio</label><input type="number" id="rear-gear" value="{gear}" step="0.01"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let staticDia = parseFloat(document.getElementById("static-dia").value) || 28;
            let trap = parseFloat(document.getElementById("trap-speed").value) || 150;
            let growth = parseFloat(document.getElementById("growth-fac").value) || 4.5;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let dynamicDia = staticDia * (1 + (growth / 100));
            let staticRollout = (staticDia * Math.PI).toFixed(1);
            let dynamicRollout = (dynamicDia * Math.PI).toFixed(1);
            let estFinishRpm = Math.round((trap * gear * 336) / dynamicDia);
            document.getElementById("results").innerHTML = "Static Rollout: <strong>" + staticRollout + " in</strong> | Dynamic Rollout: <strong>" + dynamicRollout + " in</strong> | Est. Finish RPM: <strong>" + estFinishRpm + " RPM</strong>";
        }
        ["static-dia", "trap-speed", "growth-fac", "rear-gear"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
        });
        calcTool();
        """
    elif category == "Wastegate":
        primary_title = "Wastegate Sizing & Boost Control Calculator"
        formula_text = "Valve Sizing = Determined by Total Airflow (lb/min), Target Boost, and Exhaust Backpressure."
        faqs = '<div class="faq-item"><h4>What causes boost creep?</h4><p>Wastegate valve is too small to bypass excess exhaust gas at high RPM.</p></div>'
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Target Flywheel HP</label><input type="number" id="wg-hp" value="1000" step="50"></div>
                <div><label>Target Boost (PSI)</label><input type="number" id="wg-boost" value="22" step="1"></div>
            </div>
            <div class="grid-2">
                <div style="grid-column: span 2;">
                    <label>Turbo Frame Size / Exhaust Flow</label>
                    <select id="wg-turbo">
                        <option value="small">Small Frame (T3, 50-60mm, 400-700 HP)</option>
                        <option value="medium" selected>Medium Frame (T4, 62-76mm, 700-1200 HP)</option>
                        <option value="large">Large Frame (T6 / Pro Mod, 80mm+, 1200+ HP)</option>
                        <option value="twin">Twin Turbo Setup (Divided / Dual Gates)</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="wg-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("wg-hp").value) || 1000;
            let boost = parseFloat(document.getElementById("wg-boost").value) || 22;
            let frame = document.getElementById("wg-turbo").value;
            let rec = "38mm";
            if(hp > 1200 || frame === "large") {
                rec = "60mm+ (or Dual 44mm Gates)";
            } else if(hp > 800 || boost > 20 || frame === "medium") {
                rec = "44mm - 50mm";
            } else if(hp > 500) {
                rec = "40mm - 44mm";
            } else {
                rec = "38mm";
            }
            document.getElementById("wg-results").innerHTML = "Recommended Wastegate: <strong>" + rec + "</strong> (Target: " + hp + " HP @ " + boost + " PSI)";
        }
        ["wg-hp", "wg-boost", "wg-turbo"].forEach(id => {
            let el = document.getElementById(id);
            if(el) el.addEventListener("input", calcTool);
            if(el) el.addEventListener("change", calcTool);
        });
        calcTool();
        """
    else:
        primary_title = "Drag Racing Calculator Suite"
        formula_text = "Standard Automotive Calculation"
        faqs = ""
        primary_tool_html = "<div>Select a tool from the hub.</div>"
        tool_script = ""

    page_html = (
        base_html_template.replace("TARGET_KEYWORD", target_keyword)
            .replace("PRIMARY_TITLE", primary_title)
            .replace("PRIMARY_TOOL_HTML", primary_tool_html)
            .replace("REPLACE_UTILITIES_GRID", utilities_grid_html)
            .replace("REPLACE_STICKY_AD", ad_block_html)
            .replace("REPLACE_TOP_AD", ad_block_html)
            .replace("REPLACE_BOTTOM_AD", ad_block_html)
            .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
            .replace("REPLACE_PARTNERS", partners_html)
            .replace("TOOL_SCRIPT", tool_script)
    )

    file_path = os.path.join(output_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(page_html)
    pages_created += 1

print(f"Successfully updated all pages with the advanced Turbo Sizing & Matching Calculator!")