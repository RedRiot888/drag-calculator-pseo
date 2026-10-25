import os
import csv

output_dir = "."
AFFILIATE_TRACKING_URL = "https://www.pjtra.com/t/YOUR_IMPACT_ID_HERE?url="

# 1. Automatically create Google Search Console verification file
gsc_verification_filename = "google9e7c88791a3f2f72.html"
gsc_verification_content = "google-site-verification: google9e7c88791a3f2f72.html"
with open(os.path.join(output_dir, gsc_verification_filename), "w", encoding="utf-8") as f:
    f.write(gsc_verification_content)

# 2. Automatically create contact.html submission page with active Formspree endpoint
contact_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact & Track Sponsorships | Ultimate Drag Racing Calculator Suite</title>
    <style>
        :root {
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.5; }
        .container { max-width: 600px; margin: 40px auto; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 30px; }
        h1 { color: var(--accent-red); font-size: 1.4rem; text-transform: uppercase; margin-top: 0; text-align: center; }
        p { color: var(--text-muted); font-size: 0.9rem; text-align: center; margin-bottom: 25px; }
        label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 0.8rem; color: var(--text-muted); }
        input, select, textarea { width: 100%; padding: 10px 12px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; box-sizing: border-box; font-size: 0.9rem; margin-bottom: 15px; }
        textarea { resize: vertical; height: 120px; }
        .action-btn { width: 100%; background: var(--accent-red); color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; font-size: 0.85rem; cursor: pointer; text-transform: uppercase; }
        .action-btn:hover { background: #e0161f; }
        .back-link { display: inline-block; margin-bottom: 20px; color: var(--accent-red); text-decoration: none; font-weight: bold; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto;"><a href="index.html" class="back-link">&larr; Back to Master Hub</a></div>
    <div class="container">
        <h1>Contact & Track Sponsorships</h1>
        <p>Get in touch with our team for advertising rates, technical calculator feedback, or partnership inquiries.</p>
        <form action="https://formspree.io/f/xqppzgab" method="POST">
            <div>
                <label>Your Name / Shop Name</label>
                <input type="text" name="name" required placeholder="e.g. Pro Line Racing">
            </div>
            <div>
                <label>Your Email Address</label>
                <input type="email" name="email" required placeholder="e.g. yourname@domain.com">
            </div>
            <div>
                <label>Inquiry Type</label>
                <select name="inquiry_type">
                    <option value="Sponsorship">Track Sponsor Rates & Advertising</option>
                    <option value="Bug / Feedback">Calculator Feedback / Bug Report</option>
                    <option value="Other">General Partnership</option>
                </select>
            </div>
            <div>
                <label>Message</label>
                <textarea name="message" required placeholder="Describe your inquiry or sponsorship request here..."></textarea>
            </div>
            <button type="submit" class="action-btn">Send Message &rarr;</button>
        </form>
    </div>
</body>
</html>
"""
with open(os.path.join(output_dir, "contact.html"), "w", encoding="utf-8") as f:
    f.write(contact_html_content)
print("Successfully generated contact.html!")

# 3. Pages CSV data
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
    pages = list(csv.DictReader(f))

sidebar_nav_html = """
<div style="display: flex; flex-direction: column; gap: 4px;">
    <a href="index.html" class="nav-item active" style="padding: 8px 10px; background: var(--input-bg); border-left: 3px solid var(--accent-red); color: var(--text-main); text-decoration: none; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">🏁 Popular / Master Hub</a>
    <a href="transmission-shift-recovery-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🏎️ Transmission & Gearing</a>
    <a href="turbo-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🌀 Forced Induction / Turbo</a>
    <a href="exhaust-header-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🔥 Exhaust & Airflow</a>
    <a href="fuel-injector-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">⛽ Fueling & EFI</a>
    <a href="tire-growth-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">🛞 Chassis & Tires</a>
    <a href="automotive-relay-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">⚡ Electrical & Wiring</a>
</div>
"""

ad_block_html = '<div class="content-box" style="text-align: center; background: #121418; border: 1px dashed var(--border-color);"><h3 style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">Advertisement Space</h3><div style="padding: 15px 10px; color: var(--text-muted); font-size: 0.80rem; background: var(--input-bg); border-radius: 6px;">Want your brand here?<br><a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact for Track Sponsor Rates &rarr;</a></div></div>'
partners_html = '<div class="content-box"><h3>Industry Standard References</h3><ul style="list-style: none; padding: 0; margin: 0; font-size: 0.85rem; color: var(--text-muted);"><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Precision Turbo & Engine <span style="float: right; color: #10b981;">Verified Match</span></li><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Strange Engineering <span style="float: right; color: #10b981;">Drivetrain Spec</span></li><li style="padding: 6px 0;">ATI Performance <span style="float: right; color: #10b981;">Transmission Tech</span></li></ul></div>'
tuning_guides_html = '<div class="content-box"><h3>Track-Side Tuning Cheat Sheets</h3><p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">1. Density Altitude (DA): Every 1,000 ft costs NA engines ~3% HP.<br>2. Torque Converter Slip: Target 5% to 8% slip at finish line.<br>3. Boost Management: Pull 1-2° timing per 3-4 PSI boost.</p></div>'

footer_html = """
<footer style="text-align: center; margin: 40px auto 20px auto; color: var(--text-muted); font-size: 0.78rem; border-top: 1px solid var(--border-color); padding-top: 20px;">
    <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved. Professional Track Tuning & Engineering Tools.</p>
    <p style="margin: 6px 0;">
        <a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact & Sponsorships</a> &nbsp;|&nbsp; 
        <a href="contact.html" style="color: var(--text-muted); text-decoration: none;">Privacy Policy & Affiliate Disclosure</a>
    </p>
    <p style="font-size: 0.7rem; color: #6b7280; max-width: 800px; margin: 8px auto 0 auto;">
        Disclosure: We may earn an affiliate commission from qualifying purchases made through links on this site at no extra cost to you.
    </p>
</footer>
"""

verification_tags = """    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>
    <meta name='google-site-verification' content='google9e7c88791a3f2f72'>"""

social_meta_tags = """
    <!-- Open Graph / Social Media Preview Tags -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dragcalculators.com/">
    <meta property="og:title" content="TARGET_KEYWORD | Ultimate Drag Racing Calculator Suite">
    <meta property="og:description" content="Professional drag racing calculators for gear ratios, turbo sizing, shift recovery, and track tuning.">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="TARGET_KEYWORD | Ultimate Drag Racing Master Suite">
    <meta name="twitter:description" content="Professional drag racing calculators for gear ratios, turbo sizing, shift recovery, and track tuning.">
"""

if os.path.exists("index_template.html"):
    with open("index_template.html", "r", encoding="utf-8") as f:
        master_index_html = f.read()
    
    master_index_html = (
        master_index_html.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags + social_meta_tags.replace("TARGET_KEYWORD", "Ultimate Drag Racing Master Suite"))
        .replace("REPLACE_SIDEBAR_NAV", sidebar_nav_html)
        .replace("REPLACE_STICKY_AD", ad_block_html)
        .replace("REPLACE_TOP_AD", ad_block_html)
        .replace("REPLACE_BOTTOM_AD", ad_block_html)
        .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
        .replace("REPLACE_PARTNERS", partners_html)
        .replace("REPLACE_FOOTER", footer_html)
    )
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(master_index_html)

base_html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TARGET_KEYWORD | Ultimate Drag Racing Master Suite</title>
    VERIFICATION_TAGS_PLACEHOLDER
    SOCIAL_TAGS_PLACEHOLDER
    <style>
        :root {
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.5; }
        .layout-grid { max-width: 1350px; margin: 20px auto; display: grid; grid-template-columns: 240px 480px 1fr; gap: 25px; align-items: start; }
        .nexus-sidebar { position: sticky; top: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; }
        .sticky-calculator { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
        .content-column { display: flex; flex-direction: column; gap: 20px; }
        .content-box { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; }
        .content-box h3 { color: var(--accent-red); font-size: 0.95rem; text-transform: uppercase; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        .master-header { text-align: center; margin-bottom: 5px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
        .master-header h1 { color: var(--accent-red); font-size: 1.2rem; text-transform: uppercase; margin: 0 0 3px 0; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }
        label { display: block; margin-bottom: 2px; font-weight: 600; font-size: 0.72rem; color: var(--text-muted); }
        input, select { width: 100%; padding: 7px 9px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; box-sizing: border-box; font-size: 0.82rem; }
        optgroup { color: var(--accent-red); font-weight: bold; }
        option { color: var(--text-main); background: var(--input-bg); }
        .results-box { margin-top: 10px; background: #121418; border: 1px solid var(--border-color); border-left: 4px solid var(--accent-red); padding: 10px; border-radius: 6px; font-size: 0.82rem; }
        .action-btn { width: 100%; margin-top: 10px; background: var(--accent-red); color: white; border: none; padding: 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; cursor: pointer; text-transform: uppercase; }
        .action-btn:hover { background: #e0161f; }
        table { width: 100%; margin-top: 12px; border-collapse: collapse; background: #121418; border-radius: 6px; overflow: hidden; }
        th, td { padding: 5px 4px; border: 1px solid var(--border-color); text-align: center; font-size: 0.72rem; }
        th { background: #1f232b; color: var(--accent-red); text-transform: uppercase; font-size: 0.62rem; }
        .back-link { display: inline-block; margin-bottom: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div style="max-width: 1350px; margin: 0 auto;"><a href="index.html" class="back-link">&larr; Back to Master Hub</a></div>
    <div class="layout-grid">
        <div class="nexus-sidebar">REPLACE_SIDEBAR_NAV</div>
        <div class="sticky-calculator">
            <div>
                <div class="master-header"><h1>PRIMARY_TITLE</h1><p>TARGET_KEYWORD &mdash; Track Tuning Engine</p></div>
                PRIMARY_TOOL_HTML
            </div>
            REPLACE_STICKY_AD
        </div>
        <div class="content-column">
            REPLACE_TOP_AD
            REPLACE_TUNING_GUIDES
            <div class="content-box"><h3>Formula Breakdown</h3><div style="font-family: monospace; color: #10b981; font-size: 0.85rem; background: var(--input-bg); padding: 10px; border-radius: 6px;">FORMULA_TEXT</div></div>
            REPLACE_PARTNERS
            REPLACE_BOTTOM_AD
        </div>
    </div>
    REPLACE_FOOTER
    <script>TOOL_SCRIPT</script>
</body>
</html>
"""

for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]
    gear = row["rear_gear"]
    tire = row["tire_diameter"]

    if category == "Transmission":
        primary_title = "Transmission Shift Recovery Calculator"
        formula_text = "Overall Ratio = Trans Ratio x Rear Gear | Shift Speed = (RPM * Tire) / (Overall * 336)"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Transmission Profile</label>
                    <select id="trans">
                        <optgroup label="GM Automatic">
                            <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                            <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                        </optgroup>
                    </select>
                </div>
                <div><label>Max Shift RPM</label><input type="number" id="max-rpm" value="7500" step="100"></div>
            </div>
            <div class="grid-2">
                <div><label>Tire Diameter (in)</label><input type="number" id="tire-dia" value="28.0" step="0.1"></div>
                <div><label>Rear Gear Ratio</label><input type="number" id="rear-gear" value="3.42" step="0.01"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Track Sheet</button>
            <table>
                <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop / Finish</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        """
        tool_script = """
        const ratios = { powerglide: [1.76, 1.00], th400: [2.48, 1.48, 1.00] };
        function calcTool() {
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey] || [2.48, 1.48, 1.00];
            let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
            let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
            let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
            let rollout = (tire * Math.PI).toFixed(1);
            document.getElementById("results").innerHTML = "Rollout: " + rollout + " in | 1st Gear Overall: " + (rat[0]*gear).toFixed(2) + ":1";
            let tbody = document.getElementById("gear-body");
            if(tbody) {
                tbody.innerHTML = "";
                for(let i=0; i<rat.length; i++) {
                    let overall = rat[i] * gear;
                    let speed = (rpm * tire) / (overall * 336);
                    let trapRpm = Math.round((125 * overall * 336) / tire);
                    let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Finish: " + trapRpm + " RPM";
                    tbody.innerHTML += "<tr><td>Gear " + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
                }
            }
        }
        ["trans", "max-rpm", "tire-dia", "rear-gear"].forEach(id => { let el = document.getElementById(id); if(el) el.addEventListener("input", calcTool); });
        calcTool();
        """
    elif category == "Turbo":
        primary_title = "Turbo Sizing & Turbocharger Matching Calculator"
        formula_text = "Airflow (lb/min) = (HP x BSFC) / 6.0 | Displacement per Cylinder (cc) evaluates Spool Threshold & Turbine A/R Match."
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Engine Displacement (L)</label><input type="number" id="disp" value="5.7" step="0.1"></div>
                <div><label>Cylinder Count</label><select id="cyl"><option value="4">4-Cylinder</option><option value="6">6-Cylinder</option><option value="8" selected>8-Cylinder (V8)</option><option value="10">10-Cylinder</option><option value="12">12-Cylinder</option></select></div>
            </div>
            <div class="grid-2">
                <div><label>Target Flywheel HP</label><input type="number" id="hp" value="1000" step="50"></div>
                <div><label>Target Boost (PSI)</label><input type="number" id="boost" value="25" step="1"></div>
            </div>
            <div class="grid-2">
                <div><label>Fuel Type / BSFC</label><select id="bsfc"><option value="0.50">Pump Gasoline (BSFC 0.50)</option><option value="0.60" selected>Gasoline / Race Gas (BSFC 0.60)</option><option value="0.75">E85 / Alcohol (BSFC 0.75)</option><option value="1.30">Methanol (BSFC 1.30)</option></select></div>
                <div><label>Turbo Count</label><select id="turbos"><option value="1" selected>Single Turbo</option><option value="2">Twin Turbos</option></select></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; margin-top: 10px;">
                <div style="font-size: 0.72rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase;">Displacement & Spool Analysis</div>
                <div id="spool-analysis" style="font-size: 0.78rem; color: var(--text-main); margin-top: 4px;">Calculating...</div>
            </div>
            <div style="background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; margin-top: 10px;">
                <div style="font-size: 0.72rem; color: var(--accent-red); font-weight: bold; text-transform: uppercase;">Engineered Turbo & A/R Match</div>
                <div id="turbo-rec" style="font-size: 0.78rem; color: var(--text-main); margin-top: 4px;">Calculating...</div>
            </div>
            <a href=""" + AFFILIATE_TRACKING_URL + """https://www.summitracing.com" target="_blank" style="text-decoration: none;"><button type="button" class="action-btn" style="background: #e0161f; margin-top: 8px;">🛒 Buy Now at Summit Racing &rarr;</button></a>
            <button type="button" class="action-btn" onclick="window.print()" style="margin-top: 6px;">🖨️ Print / Save Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let disp = parseFloat(document.getElementById("disp").value) || 5.7;
            let cyl = parseInt(document.getElementById("cyl").value) || 8;
            let hp = parseFloat(document.getElementById("hp").value) || 1000;
            let boost = parseFloat(document.getElementById("boost").value) || 25;
            let bsfc = parseFloat(document.getElementById("bsfc").value) || 0.60;
            let count = parseInt(document.getElementById("turbos").value) || 1;
            
            let airflow = (hp * bsfc) / 6.0;
            let perTurbo = airflow / count;
            let pr = (boost + 14.7) / 14.7;
            
            let ccPerCyl = (disp * 1000) / cyl;
            
            document.getElementById("results").innerHTML = "Required Airflow: <strong>" + airflow.toFixed(1) + " lb/min</strong> (" + perTurbo.toFixed(1) + " lb/min per turbo) | Pressure Ratio: <strong>" + pr.toFixed(2) + ":1</strong>";
            
            let spoolText = "";
            if (ccPerCyl < 350 && perTurbo > 70) {
                spoolText = "⚠️ <strong>Extreme Lag Warning:</strong> " + Math.round(ccPerCyl) + " cc/cyl is very low for a " + Math.round(perTurbo) + " lb/min turbo. High RPM threshold; twin turbos or tighter A/R strongly recommended.";
            } else if (ccPerCyl < 500) {
                spoolText = "⚡ <strong>Moderate Spool:</strong> " + Math.round(ccPerCyl) + " cc/cyl. Will require proper converter flashing, anti-lag, or twin-scroll housing to spool quickly.";
            } else {
                spoolText = "🚀 <strong>Optimal Spool Energy:</strong> " + Math.round(ccPerCyl) + " cc/cyl provides heavy exhaust pulse energy for rapid turbine spool.";
            }
            document.getElementById("spool-analysis").innerHTML = spoolText;
            
            let rec = "";
            if (perTurbo <= 45) {
                rec = "Precision 5858 Gen II CEA (~550 HP Cap) | A/R: 0.64 T3 V-Band";
            } else if (perTurbo <= 58) {
                rec = "Precision 6262 Gen II CEA (~700 HP Cap) | A/R: 0.82 T4";
            } else if (perTurbo <= 72) {
                rec = "Precision 6870 Gen II CEA (~900 HP Cap) | A/R: 0.96 T4";
            } else if (perTurbo <= 90) {
                rec = "Precision 7675 Gen II CEA (~1,100 HP Cap) | A/R: 1.15 T4";
            } else if (perTurbo <= 115) {
                rec = "BorgWarner S485 SX-E or Precision 8585 (~1,400 HP Cap) | A/R: 1.25 T6";
            } else if (perTurbo <= 145) {
                rec = "Precision Pro Mod 88mm CEA (Up to 1,850 HP) | A/R: 1.28 T6 V-Band";
            } else if (perTurbo <= 180) {
                rec = "Precision Pro Mod 94mm CEA or Garrett GTX5533R Gen II (Up to 2,300 HP) | A/R: 1.40 T6";
            } else {
                rec = "Garrett GTX5544R Gen II 106mm or Precision Pro Mod 98mm+ (2,500 - 3,200+ HP Monster) | A/R: 1.50+ T6";
            }

            document.getElementById("turbo-rec").innerHTML = "<strong>Engine Spec:</strong> " + cyl + "-Cyl / " + disp + "L (" + Math.round(ccPerCyl) + " cc/cyl)<br><strong>Engineered Match:</strong> " + rec;
        }
        ["disp", "cyl", "hp", "boost", "bsfc", "turbos"].forEach(id => { let el = document.getElementById(id); if(el) { el.addEventListener("input", calcTool); el.addEventListener("change", calcTool); } });
        calcTool();
        """
    elif category == "Exhaust":
        primary_title = "Exhaust Primary & Turbo Downpipe Sizing Calculator"
        formula_text = "NA Header Primary = (Displacement x RPM) / (Cylinder Count x Constant)"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Engine Induction Type</label><select id="ex-type"><option value="na">Naturally Aspirated</option><option value="turbo" selected>Turbocharged</option></select></div>
                <div><label>Target Flywheel HP</label><input type="number" id="ex-hp" value="850" step="50"></div>
            </div>
            <div class="results-box" id="ex-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("ex-hp").value) || 850;
            let type = document.getElementById("ex-type").value;
            let dia = type === "na" ? "1-3/4 to 1-7/8 inches Primary OD" : "3.5 to 4.0 inch Downpipe";
            document.getElementById("ex-results").innerHTML = "Recommended Sizing: <strong>" + dia + "</strong> for " + hp + " HP";
        }
        ["ex-type", "ex-hp"].forEach(id => { let el = document.getElementById(id); if(el) { el.addEventListener("input", calcTool); el.addEventListener("change", calcTool); } });
        calcTool();
        """
    elif category == "Fuel":
        primary_title = "Fuel Injector Flow Rate & Sizing Calculator"
        formula_text = "Required Flow (cc/min) = (Target HP x BSFC) / (# Injectors x Duty Cycle)"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Target Crank HP</label><input type="number" id="inj-hp" value="1200" step="50"></div>
                <div><label>Number of Injectors</label><input type="number" id="inj-count" value="8" step="1"></div>
            </div>
            <div class="results-box" id="inj-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let hp = parseFloat(document.getElementById("inj-hp").value) || 1200;
            let count = parseInt(document.getElementById("inj-count").value) || 8;
            let totalLbHr = (hp * 0.65) / 0.85;
            let perInjCc = (totalLbHr / count) * 10.5;
            document.getElementById("inj-results").innerHTML = "Per-Injector Flow: <strong>" + Math.round(perInjCc) + " cc/min</strong>";
        }
        ["inj-hp", "inj-count"].forEach(id => { let el = document.getElementById(id); if(el) el.addEventListener("input", calcTool); });
        calcTool();
        """
    elif category == "Tire":
        primary_title = "Tire Diameter Growth & Rollout Drag Calculator"
        formula_text = "Dynamic Diameter = Static Diameter x (1 + (Growth % / 100))"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Static Tire Dia (in)</label><input type="number" id="static-dia" value="28.0" step="0.1"></div>
                <div><label>Trap Speed (MPH)</label><input type="number" id="trap-speed" value="150" step="1"></div>
            </div>
            <div class="results-box" id="results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let staticDia = parseFloat(document.getElementById("static-dia").value) || 28;
            let rollout = (staticDia * Math.PI).toFixed(1);
            document.getElementById("results").innerHTML = "Static Rollout: <strong>" + rollout + " inches</strong>";
        }
        let el = document.getElementById("static-dia"); if(el) el.addEventListener("input", calcTool);
        calcTool();
        """
    elif category == "Electrical":
        primary_title = "Automotive Relay & Circuit Sizing Calculator"
        formula_text = "Amps = Watts / Volts | Fuse = Amps x 1.25"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Accessory Draw (Amps)</label><input type="number" id="relay-amps" value="20" step="1"></div>
                <div><label>Wire Length (ft)</label><input type="number" id="relay-ft" value="10" step="1"></div>
            </div>
            <div class="results-box" id="relay-results">Adjust parameters above.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let amps = parseFloat(document.getElementById("relay-amps").value) || 20;
            let fuse = Math.ceil(amps * 1.25 / 5) * 5;
            document.getElementById("relay-results").innerHTML = "Rec. Fuse: <strong>" + fuse + " Amps</strong> | Relay: <strong>Standard 40A Bosch</strong>";
        }
        let el = document.getElementById("relay-amps"); if(el) el.addEventListener("input", calcTool);
        calcTool();
        """
    else:
        primary_title = target_keyword
        formula_text = "Standard Automotive Calculation"
        primary_tool_html = """
            <div class="grid-2">
                <div><label>Parameter Value</label><input type="number" id="val1" value="100" step="1"></div>
            </div>
            <div class="results-box" id="res">Calculated successfully.</div>
            <button type="button" class="action-btn" onclick="window.print()">🖨️ Print Track Sheet</button>
        """
        tool_script = """
        function calcTool() {
            let v = parseFloat(document.getElementById("val1").value) || 100;
            document.getElementById("res").innerHTML = "Calculated Output: <strong>" + (v * 1.5).toFixed(1) + "</strong>";
        }
        let el = document.getElementById("val1"); if(el) el.addEventListener("input", calcTool);
        calcTool();
        """

    page_html = (
        base_html_template.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags)
            .replace("SOCIAL_TAGS_PLACEHOLDER", social_meta_tags.replace("TARGET_KEYWORD", target_keyword))
            .replace("TARGET_KEYWORD", target_keyword)
            .replace("PRIMARY_TITLE", primary_title)
            .replace("PRIMARY_TOOL_HTML", primary_tool_html)
            .replace("FORMULA_TEXT", formula_text)
            .replace("REPLACE_SIDEBAR_NAV", sidebar_nav_html)
            .replace("REPLACE_STICKY_AD", ad_block_html)
            .replace("REPLACE_TOP_AD", ad_block_html)
            .replace("REPLACE_BOTTOM_AD", ad_block_html)
            .replace("REPLACE_TUNING_GUIDES", tuning_guides_html)
            .replace("REPLACE_PARTNERS", partners_html)
            .replace("REPLACE_FOOTER", footer_html)
            .replace("TOOL_SCRIPT", tool_script)
    )

    with open(os.path.join(output_dir, f"{slug}.html"), "w", encoding="utf-8") as out_f:
        out_f.write(page_html)

print("Successfully built all calculator pages with social media preview tags!")

# 4. Automatically generate sitemap.xml for Google Search Console
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://dragcalculators.com/index.html</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://dragcalculators.com/contact.html</loc>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""
for row in pages:
    sitemap_content += f"""    <url>
        <loc>https://dragcalculators.com/{row["slug"]}.html</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""
sitemap_content += "</urlset>"

with open(os.path.join(output_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_content)
print("Successfully generated sitemap.xml with contact.html!")