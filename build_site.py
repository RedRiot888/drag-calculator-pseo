import os
import csv

output_dir = "."

AFFILIATE_TRACKING_URL = "https://www.pjtra.com/t/YOUR_IMPACT_ID_HERE?url="

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
    reader = csv.DictReader(f)
    pages = list(reader)

utilities_grid_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">\n'
for row in pages:
    slug = row["slug"]
    keyword = row["target_keyword"]
    cat = row["category"]
    
    icon = "⚙️"
    if "Turbo" in cat: icon = "🌀"
    elif "Exhaust" in cat: icon = "🔥"
    elif "Supercharger" in cat: icon = "⚡"
    elif "Rear" in cat: icon = "🔧"
    elif "Tire" in cat: icon = "🛞"
    elif "Transmission" in cat: icon = "🏎️"
    elif "Wastegate" in cat: icon = "🎛️"
    elif "Fuel" in cat: icon = "⛽"
    elif "Electrical" in cat: icon = "⚡"
    
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
                <div style="padding: 20px 10px; color: var(--text-muted); font-size: 0.80rem; background: var(--input-bg); border-radius: 6px;">
                    Want your brand here?<br><a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact for Track Sponsor Rates &rarr;</a>
                </div>
            </div>
"""

partners_html = """
            <div class="content-box">
                <h3 style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Industry Standard References</span>
                    <span style="font-size: 0.7rem; font-weight: normal; color: var(--text-muted); text-transform: none;">Gold-Standard Tech</span>
                </h3>
                <ul class="sponsor-list" style="list-style: none; padding: 0; margin: 0 0 15px 0; font-size: 0.85rem; color: var(--text-muted);">
                    <li style="padding: 8px 0; border-bottom: 1px dashed var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--text-main); font-weight: 600;">Precision Turbo & Engine</span>
                        <span style="font-size: 0.75rem; color: #10b981;">Verified Match</span>
                    </li>
                    <li style="padding: 8px 0; border-bottom: 1px dashed var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--text-main); font-weight: 600;">Strange Engineering</span>
                        <span style="font-size: 0.75rem; color: #10b981;">Drivetrain Spec</span>
                    </li>
                    <li style="padding: 8px 0; border-bottom: 1px dashed var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--text-main); font-weight: 600;">ATI Performance Products</span>
                        <span style="font-size: 0.75rem; color: #10b981;">Transmission Tech</span>
                    </li>
                    <li style="padding: 8px 0; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--text-main); font-weight: 600;">Mickey Thompson Tires</span>
                        <span style="font-size: 0.75rem; color: #10b981;">Rollout Standard</span>
                    </li>
                </ul>
                <div style="background: var(--input-bg); border: 1px solid var(--border-color); padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.78rem; font-weight: bold; color: var(--text-main); margin-bottom: 4px;">Are you a performance manufacturer?</div>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0 0 8px 0;">Put your parts and banner in front of thousands of active racers daily.</p>
                    <a href="contact.html" style="display: inline-block; background: var(--accent-red); color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.72rem; text-transform: uppercase;">Claim Sponsor Space &rarr;</a>
                </div>
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
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">Read spark plug ground straps for heat mark placement. Back off timing 1 to 2 degrees per additional 3-4 PSI of boost or when stepping up nitrous jetting.</p>
                </div>

                <div>
                    <strong style="color: var(--text-main); font-size: 0.85rem;">4. 4-Link Anti-Squat & Launch</strong>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">If the car bounces or unloads the tires immediately on launch, lower the instantaneous center (IC) or soften rear shock extension.</p>
                </div>
            </div>
"""

footer_html = """
    <footer style="max-width: 1200px; margin: 40px auto 20px auto; text-align: center; border-top: 1px solid var(--border-color); padding-top: 20px; font-size: 0.8rem; color: var(--text-muted);">
        <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved. Professional Track Tuning & Engineering Tools.</p>
        <p style="margin-top: 5px;">
            <a href="contact.html" style="color: var(--text-muted); text-decoration: none; margin: 0 10px;">Contact & Sponsorships</a> | 
            <a href="privacy.html" style="color: var(--text-muted); text-decoration: none; margin: 0 10px;">Privacy Policy & Affiliate Disclosure</a>
        </p>
        <p style="font-size: 0.72rem; color: #6b7280; margin-top: 8px;">Disclosure: We may earn an affiliate commission from qualifying purchases made through links on this site at no extra cost to you.</p>
    </footer>
"""

impact_meta_tag = "    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>"

master_index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Drivetrain & Shift RPM Calculator Suite</title>
    IMPACT_META_PLACEHOLDER
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
        @media (max-width: 900px) {
            .layout-grid { grid-template-columns: 1fr; }
            .sticky-calculator { position: static; top: auto; box-shadow: none; }
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
            .content-column, .tab-buttons, .action-btn, footer { display: none; }
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

    REPLACE_FOOTER

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
    master_index_html.replace("IMPACT_META_PLACEHOLDER", impact_meta_tag)
    .replace("REPLACE_UTILITIES_GRID", utilities_grid_html)
    .replace("REPLACE_STICKY_AD", ad_block_html)
    .replace("REPLACE_TOP_AD", ad_block_html)
    .replace("REPLACE_BOTTOM_AD", ad_block_html)
    .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
    .replace("REPLACE_PARTNERS", partners_html)
    .replace("REPLACE_FOOTER", footer_html)
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
    IMPACT_META_PLACEHOLDER
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
        @media (max-width: 900px) {
            .layout-grid { grid-template-columns: 1fr; }
            .sticky-calculator { position: static; top: auto; box-shadow: none; }
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
            .content-column, .back-link, .action-btn, footer { display: none; }
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

    REPLACE_FOOTER

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
        formula_text = "Overall Ratio = Transmission Ratio x Rear Gear Ratio<br>Shift Speed = (Shift RPM x Tire Diameter) / (Overall Ratio x 336)<br>RPM Drop = Shift RPM x (Next Gear Ratio / Current Gear Ratio)"
        faqs = """
            <div class="faq-item">
                <h4>How is shift recovery RPM calculated?</h4>
                <p>Shift recovery is determined by multiplying your shift RPM by the ratio of the upcoming higher gear divided by the current gear.</p>
            </div>
            <div class="faq-item" style="margin-top: 10px;">
                <h4>Why is gear drop critical in drag racing?</h4>
                <p>Keeping your engine operating inside its peak power band during shifts prevents RPM from falling below torque converter stall or power peak, maximizing acceleration.</p>
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
    elif category == "Exhaust":
        primary_title = "Exhaust Primary & Turbo Downpipe Sizing Calculator"
        formula_text = "NA Header Primary = (Displacement x RPM) / (Cylinder Count x Constant)<br>Turbo Downpipe = Sized directly by total horsepower and turbine exhaust gas volume."
        faqs = """
            <div class="faq-item">
                <h4>What size header primary is best for a Naturally Aspirated drag car?</h4>
                <p>Too large of a primary tube loses exhaust velocity and scavenging at launch; too small chokes high-RPM horsepower. This calculator determines the optimal primary outer diameter based on cubic inches and peak RPM.</p>
            </div>
            <div class="faq-item" style="margin-top: 10px;">
                <h4>Why is turbo downpipe sizing critical?</h4>
                <p>In a turbo setup, the downpipe is the primary restriction after the turbine wheel. Restrictive downpipes increase backpressure, raising EGTs and robbing top-end boost efficiency.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div><label>Engine Induction Type</label>
                    <select id="ex-type" onchange="toggleExhaustMode()">
                        <option value="na" selected>Naturally Aspirated (Header Primaries)</option>
                        <option value="turbo">Turbocharged (Downpipe & Exhaust)</option>
                    </select>
                </div>
                <div><label>Target Flywheel HP</label><input type="number" id="ex-hp" value="850" step="50"></div>
            </div>
            <div class="grid-2" id="na-fields">
                <div><label>Displacement (Cubic Inches)</label><input type="number" id="ex-ci" value="427" step="1"></div>
                <div><label>Peak Horsepower RPM</label><input type="number" id="ex-rpm" value="7200" step="100"></div>
            </div>
            <div class="grid-2" id="turbo-fields" style="display: none;">
                <div><label>Target Boost (PSI)</label><input type="number" id="ex-boost" value="20" step="1"></div>
                <div><label>Exhaust Exit Routing</label>
                    <select id="ex-routing">
                        <option value="full">Full 3.5\" / 4\" Exhaust to Bumper</option>
                        <option value="fender" selected>Fender Exit / Short Downpipe</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="ex-results">Adjust parameters above.</div>
            
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-top: 12px;" id="ex-affiliate-box">
                <div style="font-size: 0.75rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Recommended Fabrication & Tubing Kit</div>
                <div id="ex-part-details" style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 8px;">Loading fabrication specifications...</div>
                <a href="{AFFILIATE_TRACKING_URL}https%3A%2F%2Fwww.performanceparts.com" id="ex-buy-btn" target="_blank" style="display: block; text-align: center; background: var(--accent-red); color: white; padding: 7px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.75rem; text-transform: uppercase;">Explore Tubing & TIG Weld Supplies &rarr;</a>
            </div>

            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function toggleExhaustMode() {
            let mode = document.getElementById("ex-type").value;
            let naFields = document.getElementById("na-fields");
            let turboFields = document.getElementById("turbo-fields");
            if(naFields) naFields.style.display = (mode === "na") ? "grid" : "none";
            if(turboFields) turboFields.style.display = (mode === "turbo") ? "grid" : "none";
            calcTool();
        }

        function calcTool() {
            let type = document.getElementById("ex-type").value;
            let hp = parseFloat(document.getElementById("ex-hp").value) || 850;
            
            if(type === "na") {
                let ci = parseFloat(document.getElementById("ex-ci").value) || 427;
                let rpm = parseFloat(document.getElementById("ex-rpm").value) || 7200;
                
                let primaryDia = "1-3/4 inches";
                let collectorDia = "3.0 inches";
                let tubingSpec = "304 Stainless Steel Mandrel Bends (16-gauge)";
                let weldingReq = "ER308L TIG Filler Rod, Back-Purging Kit";
                
                let cfmEst = (ci * rpm * 0.5 * 0.85) / 1728;
                if(cfmEst > 650 || hp > 700) {
                    primaryDia = "1-7/8 to 2-0 inches";
                    collectorDia = "3.5 to 4.0 inches";
                } else if(cfmEst > 500) {
                    primaryDia = "1-3/4 inches";
                    collectorDia = "3.5 inches";
                } else {
                    primaryDia = "1-5/8 inches";
                    collectorDia = "3.0 inches";
                }
                
                let resEl = document.getElementById("ex-results");
                if(resEl) {
                    resEl.innerHTML = "Rec. Header Primary OD: <strong>" + primaryDia + "</strong> | Collector Diameter: <strong>" + collectorDia + "</strong><br>Est. Airflow Demand: <strong>" + Math.round(cfmEst) + " CFM</strong>";
                }
                
                let partEl = document.getElementById("ex-part-details");
                if(partEl) {
                    partEl.innerHTML = "<strong>Material Spec:</strong> " + tubingSpec + "<br><strong>Flange & Collector:</strong> Heavy-Duty Laser Cut Flanges & Merge Collector<br><strong>Fabrication Tools:</strong> " + weldingReq + "<br><span style='color: var(--text-muted); font-size: 0.75rem;'><strong>Tuning Note:</strong> Maintain constant primary length (+/- 0.5 in) for even scavenging.</span>";
                }
            } else {
                let boost = parseFloat(document.getElementById("ex-boost").value) || 20;
                let routing = document.getElementById("ex-routing").value;
                
                let downpipeDia = "3.5 inches";
                let material = "304 Stainless Steel Tubing";
                let flangeSpec = "V-Band Flange Assembly & Clamp";
                let weldSupplies = "Back-Purging Argon Setup, 1/16\" ER308L Rod";
                
                if(hp > 1200 || boost > 25) {
                    downpipeDia = "4.5 to 5.0 inches";
                } else if(hp > 800 || boost > 15) {
                    downpipeDia = "4.0 inches";
                } else {
                    downpipeDia = "3.5 inches";
                }
                
                if(routing === "fender") {
                    downpipeDia += " (Short Fender Exit)";
                }
                
                let resEl = document.getElementById("ex-results");
                if(resEl) {
                    resEl.innerHTML = "Rec. Turbo Downpipe OD: <strong>" + downpipeDia + "</strong> (Target: " + hp + " HP @ " + boost + " PSI)";
                }
                
                let partEl = document.getElementById("ex-part-details");
                if(partEl) {
                    partEl.innerHTML = "<strong>Downpipe Material:</strong> " + material + " (" + downpipeDia + ")<br><strong>Hardware:</strong> " + flangeSpec + " & Thermal Blanket<br><strong>Welding Gear:</strong> " + weldSupplies + "<br><span style='color: var(--text-muted); font-size: 0.75rem;'><strong>Backpressure Warning:</strong> Ensure smooth radius bends within 12 inches of turbine exit.</span>";
                }
            }
        }

        ["ex-type", "ex-hp", "ex-ci", "ex-rpm", "ex-boost", "ex-routing"].forEach(id => {
            let el = document.getElementById(id);
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
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
                <div><label>Axle Housing / Differential</label>
                    <select id="housing">
                        <option value="ford88">Ford 8.8\" Rear Axle</option>
                        <option value="ford9">Ford 9\" Pinion Carrier</option>
                        <option value="gm10">GM 10-Bolt (8.5\")</option>
                        <option value="gm12">GM 12-Bolt Passenger</option>
                        <option value="dana60">Dana 60 Heavy Duty</option>
                    </select>
                </div>
                <div><label>Tire Diameter (in)</label><input type="number" id="tire" value="{tire}" step="0.1"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-top: 12px;" id="affiliate-box">
                <div style="font-size: 0.75rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Recommended Match & Parts</div>
                <div id="part-details" style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 8px;">Loading matching ring & pinion...</div>
                <a href="{AFFILIATE_TRACKING_URL}https%3A%2F%2Fwww.performanceparts.com" id="buy-btn" target="_blank" style="display: block; text-align: center; background: var(--accent-red); color: white; padding: 7px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.75rem; text-transform: uppercase;">Explore Hardware & Parts &rarr;</a>
            </div>

            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let trap = parseFloat(document.getElementById("trap").value) || 125;
            let gear = parseFloat(document.getElementById("gear").value) || 4.11;
            let tire = parseFloat(document.getElementById("tire").value) || 32;
            let housing = document.getElementById("housing").value;
            
            let finishRpm = (trap * gear * 336) / tire;
            let rollout = (tire * Math.PI).toFixed(1);
            document.getElementById("results").innerHTML = "Gear Ratio: <strong>" + gear.toFixed(2) + ":1</strong> | Rollout: <strong>" + rollout + " in</strong> | Finish RPM: <strong>" + Math.round(finishRpm) + " RPM</strong>";
            
            let brand = "Heavy Duty Performance Series";
            let housingName = "Ford 8.8\" Rear Axle";
            let price = "$249.99";
            let toolsNeeded = "Master Bearing Kit, Gear Marking Compound, 80W-90 Gear Oil";
            
            if(housing === "ford9") {
                housingName = "Ford 9\" Drop-Out Carrier";
                brand = "Pro Series Heavy Duty";
                price = "$319.99";
                toolsNeeded = "Daytona Pinion Support, Solid Spacer Shim Kit, Gear Lube";
            } else if(housing === "gm10") {
                housingName = "GM 10-Bolt 8.5\" Axle";
                brand = "Performance Ring & Pinion";
                price = "$239.99";
                toolsNeeded = "Master Install Kit, Crush Sleeve, Gear Paint";
            } else if(housing === "gm12") {
                housingName = "GM 12-Bolt Passenger Car";
                brand = "Heavy Duty Series";
                price = "$289.99";
                toolsNeeded = "Master Bearing Kit, Heavy Duty Shim Pack";
            } else if(housing === "dana60") {
                housingName = "Dana 60 Heavy Duty Axle";
                brand = "Hardcore Pro Series";
                price = "$389.99";
                toolsNeeded = "Install Kit with Timken Bearings, Gear Oil";
            }

            document.getElementById("part-details").innerHTML = 
                "<strong>Target:</strong> " + gear.toFixed(2) + " Ratio (" + housingName + ")<br>" +
                "<strong>Kit:</strong> " + brand + " Ring & Pinion<br>" +
                "<strong>Price:</strong> " + price + "<br>" +
                "<span style='color: var(--text-muted); font-size: 0.75rem;'><strong>Required Setup Supplies:</strong> " + toolsNeeded + "</span>";
        }
        ["trap", "gear", "tire", "housing"].forEach(id => {
            let el = document.getElementById(id);
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
        });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbo Sizing & Turbocharger Matching Calculator"
        formula_text = "Required Airflow (lb/min) = (Target Flywheel HP x BSFC) / 6.0<br>Pressure Ratio = (Target Boost + 14.7) / 14.7<br>Application Factor = Adjusts turbine A/R & wheel trim for spool vs top-end."
        faqs = """
            <div class="faq-item">
                <h4>How does vehicle application affect turbo choice?</h4>
                <p>Street cars and drag-and-drive builds require faster spool and broader torque curves (smaller turbine A/R), while full race cars prioritize maximum top-end airflow and lower backpressure (larger turbine A/R).</p>
            </div>
            <div class="faq-item" style="margin-top: 10px;">
                <h4>How do I choose the correct turbocharger size?</h4>
                <p>Match your total required airflow in lb/min and compressor pressure ratio to manufacturer compressor maps, ensuring surge lines and choke limits are respected.</p>
            </div>
        """
        primary_tool_html = f"""
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
            <div class="grid-2">
                <div style="grid-column: span 2;">
                    <label>Vehicle Application & Purpose</label>
                    <select id="app-type">
                        <option value="street">Street / Weekend Cruiser (Fast Spool & Low-End Response)</option>
                        <option value="dragndrive" selected>Drag-and-Drive / Street-Strip (Balanced Spool & Top-End)</option>
                        <option value="race">Full Blown Race Car (Maximum Top-End & Low Backpressure)</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-top: 12px;" id="affiliate-box">
                <div style="font-size: 0.75rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Recommended Specific Turbo Match</div>
                <div id="turbo-part-details" style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 8px;">Loading precise turbo recommendation...</div>
                <a href="{AFFILIATE_TRACKING_URL}https%3A%2F%2Fwww.performanceparts.com" id="turbo-buy-btn" target="_blank" style="display: block; text-align: center; background: var(--accent-red); color: white; padding: 7px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.75rem; text-transform: uppercase;">Explore Turbochargers & Parts &rarr;</a>
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
            let app = document.getElementById("app-type").value;
            
            let totalAirflow = (hp * bsfc) / 6.0;
            let perTurbo = totalAirflow / count;
            let pr = (boost + 14.7) / 14.7;
            
            document.getElementById("results").innerHTML = "Required Airflow: <strong>" + totalAirflow.toFixed(1) + " lb/min</strong> (" + perTurbo.toFixed(1) + " per turbo) | Pressure Ratio: <strong>" + pr.toFixed(2) + ":1</strong>";
            
            let brand = "Heavy Duty Performance Turbo";
            let model = "76mm Turbine V-Band";
            let ar = "1.10 A/R T4 Divided";
            let price = "$1,099.99";
            
            if(app === "street") {
                if(perTurbo > 75) {
                    brand = "Ball Bearing Pro Turbo";
                    model = "7675 Gen II Ball Bearing";
                    ar = "0.81 A/R T4 (Quick Spool)";
                    price = "$2,399.99";
                } else {
                    brand = "Performance Series";
                    model = "67mm High Flow";
                    ar = "0.72 A/R V-Band";
                    price = "$2,199.99";
                }
            } else if(app === "dragndrive") {
                if(perTurbo > 90) {
                    brand = "Pro Mod Series";
                    model = "85mm Turbine";
                    ar = "1.15 A/R T4 Divided";
                    price = "$2,699.99";
                } else if(perTurbo > 60) {
                    brand = "AirWerks Series";
                    model = "80mm Extended Tip";
                    ar = "1.25 A/R T4 Divided";
                    price = "$1,249.99";
                } else {
                    brand = "Performance Series";
                    model = "69mm Turbine";
                    ar = "0.91 A/R T4";
                    price = "$899.99";
                }
            } else {
                if(perTurbo > 90) {
                    brand = "Pro Mod Competition Series";
                    model = "91mm Pro Mod";
                    ar = "1.39 A/R T6 Housing";
                    price = "$3,199.99";
                } else if(perTurbo > 70) {
                    brand = "Elite Race Series";
                    model = "88mm Stainless";
                    ar = "1.40 A/R T6";
                    price = "$3,499.99";
                } else {
                    brand = "Race Spec Series";
                    model = "76R Race Unit";
                    ar = "1.32 A/R T4 Divided";
                    price = "$1,499.99";
                }
            }

            let setupType = (count === 2) ? "Twin Turbo Setup (Dual Units)" : "Single Turbo Setup";
            let appName = (app === "street") ? "Street / Weekend Cruiser" : (app === "dragndrive" ? "Drag-and-Drive / Street-Strip" : "Full Blown Race Car");

            document.getElementById("turbo-part-details").innerHTML = 
                "<strong>Application:</strong> " + appName + " (" + setupType + ")<br>" +
                "<strong>Model:</strong> " + brand + " &mdash; " + model + "<br>" +
                "<strong>A/R Ratio:</strong> " + ar + " | <strong>Est. Price:</strong> " + price + "<br>" +
                "<span style='color: var(--text-muted); font-size: 0.75rem;'><strong>Match Quality:</strong> Tuned for " + Math.round(totalAirflow) + " lb/min airflow at " + pr.toFixed(1) + " PR.</span>";
        }
        ["disp", "hp", "rpm", "boost", "bsfc", "turbos", "app-type"].forEach(id => {
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
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
        });
        calcTool();
        """
    elif category == "Fuel":
        primary_title = "Fuel Injector Flow Rate & Sizing Calculator"
        formula_text = "Required Flow (cc/min) = (Target HP x BSFC) / (# of Injectors x Max Duty Cycle) x 10.5"
        faqs = '<div class="faq-item"><h4>What is safe maximum injector duty cycle?</h4><p>80% to 85% duty cycle is standard practice to prevent injector overheating and lean spikes.</p></div>'
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Target Crank HP</label><input type="number" id="inj-hp" value="1200" step="50"></div>
                <div><label>Number of Injectors</label><input type="number" id="inj-count" value="8" step="1"></div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Fuel Type / BSFC</label>
                    <select id="inj-fuel" onchange="updateBsfc()">
                        <option value="0.50">Gasoline (BSFC 0.50)</option>
                        <option value="0.65" selected>E85 / Ethanol (BSFC 0.65)</option>
                        <option value="1.10">Methanol (BSFC 1.10)</option>
                    </select>
                </div>
                <div><label>Max Duty Cycle (%)</label><input type="number" id="inj-duty" value="85" step="1"></div>
            </div>
            <div class="results-box" id="inj-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("inj-hp").value) || 1200;
            let count = parseInt(document.getElementById("inj-count").value) || 8;
            let bsfc = parseFloat(document.getElementById("inj-fuel").value) || 0.65;
            let duty = (parseFloat(document.getElementById("inj-duty").value) || 85) / 100.0;
            
            let totalLbHr = (hp * bsfc) / duty;
            let perInjectorLbHr = totalLbHr / count;
            let perInjectorCcMin = perInjectorLbHr * 10.5;
            
            document.getElementById("inj-results").innerHTML = "Required Per-Injector Flow: <strong>" + Math.round(perInjectorCcMin) + " cc/min</strong> (" + perInjectorLbHr.toFixed(1) + " lb/hr) | Total System: <strong>" + Math.round(totalLbHr * 10.5) + " cc/min</strong>";
        }
        ["inj-hp", "inj-count", "inj-fuel", "inj-duty"].forEach(id => {
            let el = document.getElementById(id);
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
        });
        calcTool();
        """
    elif category == "Electrical":
        primary_title = "Automotive Relay & Circuit Sizing Calculator"
        formula_text = "Current (Amps) = Watts / Volts<br>Recommended Fuse = Current Draw x 1.25 (25% safety margin)<br>Trigger Coil Power = ~1.6W (approx 135mA at 12V)"
        faqs = """
            <div class="faq-item">
                <h4>Why use an automotive relay for high-draw accessories?</h4>
                <p>Relays allow a low-current switch or ECU output (trigger) to safely control high-current components (like fuel pumps or fans) through heavy-gauge wire, preventing switch meltdowns and voltage drop.</p>
            </div>
            <div class="faq-item" style="margin-top: 10px;">
                <h4>What do relay pins 30, 85, 86, and 87 mean?</h4>
                <p>Pin 30 = Battery Power In (Fused), Pin 85 = Ground (Trigger Switch), Pin 86 = 12V Trigger In (Switch/ECU), Pin 87 = Switched Power Out to Accessory.</p>
            </div>
        """
        primary_tool_html = f"""
            <div class="grid-2">
                <div><label>Accessory Power Draw (Amps)</label><input type="number" id="relay-amps" value="20" step="1"></div>
                <div><label>System Voltage</label><select id="relay-volts"><option value="12" selected>12V Standard</option><option value="16">16V Race Battery</option></select></div>
            </div>
            <div class="grid-2">
                <div><label>Wire Run Length (One Way, Ft)</label><input type="number" id="relay-ft" value="10" step="1"></div>
                <div><label>Accessory Type (Auto-Preset Amps)</label>
                    <select id="relay-type" onchange="applyAccessoryPreset()">
                        <option value="custom">Custom Amperage</option>
                        <option value="fuel_single">Single Electric Fuel Pump (~15A)</option>
                        <option value="fuel_dual">Dual Fuel Pumps / Aeromotive (~30A)</option>
                        <option value="fan_single">Radiator / Intercooler Fan (~25A)</option>
                        <option value="fan_dual">Dual High-Output Fans (~45A)</option>
                        <option value="water_pump">Electric Water Pump (~12A)</option>
                        <option value="nitros">Nitrous Solenoids (~20A)</option>
                        <option value="headlights">Headlights / Aux Lighting (~10A)</option>
                    </select>
                </div>
            </div>
            <div class="results-box" id="relay-results">Adjust parameters above.</div>
            
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-top: 12px;" id="relay-affiliate-box">
                <div style="font-size: 0.75rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Recommended Relay & Wiring Kit</div>
                <div id="relay-part-details" style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 8px;">Loading relay kit specs...</div>
                <a href="{AFFILIATE_TRACKING_URL}https%3A%2F%2Fwww.performanceparts.com" id="relay-buy-btn" target="_blank" style="display: block; text-align: center; background: var(--accent-red); color: white; padding: 7px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.75rem; text-transform: uppercase;">Explore Wiring Kits &rarr;</a>
            </div>

            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        const accessoryAmps = {
            fuel_single: 15,
            fuel_dual: 30,
            fan_single: 25,
            fan_dual: 45,
            water_pump: 12,
            nitros: 20,
            headlights: 10
        };

        function applyAccessoryPreset() {
            let val = document.getElementById("relay-type").value;
            if(val !== "custom" && accessoryAmps[val] !== undefined) {
                document.getElementById("relay-amps").value = accessoryAmps[val];
            }
            calcTool();
        }

        function calcTool() {
            let amps = parseFloat(document.getElementById("relay-amps").value) || 20;
            let volts = parseFloat(document.getElementById("relay-volts").value) || 12;
            let ft = parseFloat(document.getElementById("relay-ft").value) || 10;
            
            let fuseAmps = Math.ceil(amps * 1.25 / 5) * 5; 
            if(fuseAmps < 10) fuseAmps = 10;
            
            let wireGauge = "14 AWG";
            let wireDesc = "Standard GXL Automotive Wire";
            if(amps > 50) { wireGauge = "6 AWG"; wireDesc = "Heavy Duty Battery Cable"; }
            else if(amps > 35) { wireGauge = "8 AWG"; wireDesc = "Heavy Duty Power Cable"; }
            else if(amps > 20) { wireGauge = "10 AWG"; wireDesc = "Primary Power Wire"; }
            else if(amps > 12) { wireGauge = "12 AWG"; wireDesc = "Standard Power Wire"; }
            
            let relayType = "Standard Bosch 40A Weatherproof Relay";
            let kitPrice = "$24.99";
            
            if(amps > 50) {
                relayType = "Dual 40A Relays in Parallel (or 100A High-Amp Solenoid)";
                kitPrice = "$54.99";
            } else if(amps > 30) {
                relayType = "Heavy Duty 70/80A SPDT Relay";
                kitPrice = "$39.99";
            }
            
            document.getElementById("relay-results").innerHTML = 
                "Rec. Fuse Size: <strong>" + fuseAmps + " Amps</strong> | Rec. Wire Gauge: <strong>" + wireGauge + "</strong><br>" +
                "Pinout: Pin 30 (Bat+), Pin 85 (Gnd), Pin 86 (Trigger), Pin 87 (Out)";
                
            document.getElementById("relay-part-details").innerHTML = 
                "<strong>Relay Needed:</strong> " + relayType + "<br>" +
                "<strong>Wire & Fuse Kit:</strong> " + wireGauge + " " + wireDesc + " with inline waterproof holder<br>" +
                "<strong>Kit Price:</strong> " + kitPrice + "<br>" +
                "<span style='color: var(--text-muted); font-size: 0.75rem;'><strong>Wiring Note:</strong> Calculated with 25% safety margin for surge current.</span>";
        }
        ["relay-amps", "relay-volts", "relay-ft", "relay-type"].forEach(id => {
            let el = document.getElementById(id);
            if(el) {
                el.addEventListener("input", calcTool);
                el.addEventListener("change", calcTool);
            }
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
        base_html_template.replace("IMPACT_META_PLACEHOLDER", impact_meta_tag)
            .replace("TARGET_KEYWORD", target_keyword)
            .replace("PRIMARY_TITLE", primary_title)
            .replace("PRIMARY_TOOL_HTML", primary_tool_html)
            .replace("FORMULA_TEXT", formula_text)
            .replace("FAQS_HTML", faqs)
            .replace("REPLACE_UTILITIES_GRID", utilities_grid_html)
            .replace("REPLACE_STICKY_AD", ad_block_html)
            .replace("REPLACE_TOP_AD", ad_block_html)
            .replace("REPLACE_BOTTOM_AD", ad_block_html)
            .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
            .replace("REPLACE_PARTNERS", partners_html)
            .replace("REPLACE_FOOTER", footer_html)
            .replace("TOOL_SCRIPT", tool_script)
    )

    file_path = os.path.join(output_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(page_html)
    pages_created += 1

print(f"Successfully updated build script and generated {pages_created} pages with polished industry authority partners!")