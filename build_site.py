import os
import csv

output_dir = "."

# 1. Google Search Console verification file
with open(os.path.join(output_dir, "google9e7c88791a3f2f72.html"), "w", encoding="utf-8") as f:
    f.write("google-site-verification: google9e7c88791a3f2f72.html")

# 2. Contact page
contact_html = """<!DOCTYPE html>
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
            <div><label>Your Name / Shop Name</label><input type="text" name="name" required placeholder="e.g. Pro Line Racing"></div>
            <div><label>Your Email Address</label><input type="email" name="email" required placeholder="e.g. yourname@domain.com"></div>
            <div><label>Inquiry Type</label>
                <select name="inquiry_type">
                    <option value="Sponsorship">Track Sponsor Rates & Advertising</option>
                    <option value="Bug / Feedback">Calculator Feedback / Bug Report</option>
                    <option value="Other">General Partnership</option>
                </select>
            </div>
            <div><label>Message</label><textarea name="message" required placeholder="Describe your inquiry or sponsorship request here..."></textarea></div>
            <button type="submit" class="action-btn">Send Message &rarr;</button>
        </form>
    </div>
</body>
</html>
"""
with open(os.path.join(output_dir, "contact.html"), "w", encoding="utf-8") as f:
    f.write(contact_html)

# 3. CSV data & Layout components
csv_content = """slug,target_keyword,category,rear_gear,tire_diameter
transmission-shift-recovery-calculator,Transmission Shift Recovery & Gear Drop Calculator,Transmission,3.42,28.0
turbo-sizing-calculator,Turbo Sizing & Turbocharger Matching Calculator,Turbo,3.42,28.0
four-link-suspension-calculator,Four Link Suspension & Instant Center Drag Calculator,Suspension,4.11,32.0
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

sidebar_nav_html = """<div style="display: flex; flex-direction: column; gap: 4px;">
    <a href="index.html" class="nav-item active" style="padding: 8px 10px; background: var(--input-bg); border-left: 3px solid var(--accent-red); color: var(--text-main); text-decoration: none; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">Popular / Master Hub</a>
    <a href="transmission-shift-recovery-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Transmission & Gearing</a>
    <a href="turbo-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Forced Induction / Turbo</a>
    <a href="four-link-suspension-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Suspension & 4-Link</a>
    <a href="exhaust-header-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Exhaust & Airflow</a>
    <a href="fuel-injector-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Fueling & EFI</a>
    <a href="tire-growth-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Chassis & Tires</a>
    <a href="automotive-relay-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Electrical & Wiring</a>
</div>"""

ad_block_html = '<div class="content-box" style="text-align: center; background: #121418; border: 1px dashed var(--border-color);"><h3 style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">Advertisement Space</h3><div style="padding: 15px 10px; color: var(--text-muted); font-size: 0.80rem; background: var(--input-bg); border-radius: 6px;">Want your brand here?<br><a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact for Track Sponsor Rates &rarr;</a></div></div>'
partners_html = '<div class="content-box"><h3>Industry Standard References</h3><ul style="list-style: none; padding: 0; margin: 0; font-size: 0.85rem; color: var(--text-muted);"><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Precision Turbo & Engine <span style="float: right; color: #10b981;">Verified Match</span></li><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Strange Engineering <span style="float: right; color: #10b981;">Drivetrain Spec</span></li><li style="padding: 6px 0;">ATI Performance <span style="float: right; color: #10b981;">Transmission Tech</span></li></ul></div>'
tuning_guides_html = '<div class="content-box"><h3>Track-Side Tuning Cheat Sheets</h3><p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">1. Density Altitude (DA): Every 1,000 ft costs NA engines ~3% HP.<br>2. Torque Converter Slip: Target 5% to 8% slip at finish line.<br>3. Boost Management: Pull 1-2 timing per 3-4 PSI boost.</p></div>'

footer_html = """
<footer style="text-align: center; margin: 40px auto 20px auto; color: var(--text-muted); font-size: 0.78rem; border-top: 1px solid var(--border-color); padding-top: 20px;">
    <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved. Professional Track Tuning & Engineering Tools.</p>
    <p style="margin: 6px 0;"><a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact & Sponsorships</a> &nbsp;|&nbsp; <a href="contact.html" style="color: var(--text-muted); text-decoration: none;">Privacy Policy & Affiliate Disclosure</a></p>
</footer>
"""

verification_tags = """    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>
    <meta name='google-site-verification' content='google9e7c88791a3f2f72'>"""

social_meta_tags = """
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dragcalculators.com/">
    <meta property="og:title" content="Ultimate Drag Racing Master Suite | Ultimate Drag Racing Calculator Suite">
    <meta property="og:description" content="Professional drag racing calculators for gear ratios, turbo sizing, shift recovery, and track tuning.">
    <meta property="og:image" content="https://dragcalculators.com/social-banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Ultimate Drag Racing Master Suite">
    <meta name="twitter:description" content="Professional drag racing calculators for gear ratios, turbo sizing, shift recovery, and track tuning.">
    <meta name="twitter:image" content="https://dragcalculators.com/social-banner.jpg">
"""

# Drivetrain Hub Tool HTML & Script for index.html
drivetrain_tool_html = """
    <div class="grid-2">
        <div><label>Transmission Profile</label>
            <select id="trans">
                <optgroup label="GM Automatic">
                    <option value="th400" selected>TH400 / 4L80e (2.48 / 1.48 / 1.00)</option>
                    <option value="powerglide">Powerglide (1.76 / 1.00)</option>
                    <option value="th350">TH350 (2.52 / 1.52 / 1.00)</option>
                    <option value="4l60e">4L60e (3.06 / 1.62 / 1.00 / 0.70)</option>
                </optgroup>
                <optgroup label="Ford Automatic">
                    <option value="c4_c6">Ford C4 / C6 (2.46 / 1.46 / 1.00)</option>
                    <option value="aod">AOD (2.40 / 1.47 / 1.00 / 0.67)</option>
                </optgroup>
            </select>
        </div>
        <div><label>Max Shift RPM</label><input type="number" id="max-rpm" value="7500" step="100"></div>
    </div>
    <div class="grid-2">
        <div><label>Tire Diameter (in)</label><input type="number" id="tire-dia" value="28.0" step="0.1"></div>
        <div><label>Rear Gear Ratio</label><input type="number" id="rear-gear" value="3.42" step="0.01"></div>
    </div>
    <div class="grid-2">
        <div><label>Vehicle Weight (lbs)</label><input type="number" id="veh-wt" value="3200" step="50"></div>
        <div><label>Flywheel HP</label><input type="number" id="veh-hp" value="1100" step="25"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Track Sheet</button>
    <table>
        <thead><tr><th>Gear</th><th>Ratio</th><th>Overall</th><th>Shift Speed</th><th>RPM Drop</th></tr></thead>
        <tbody id="gear-body"></tbody>
    </table>
"""

drivetrain_script = """
const ratios = { 
    powerglide: [1.76, 1.00], 
    th350: [2.52, 1.52, 1.00], 
    th400: [2.48, 1.48, 1.00],
    "4l60e": [3.06, 1.62, 1.00, 0.70],
    c4_c6: [2.46, 1.46, 1.00],
    aod: [2.40, 1.47, 1.00, 0.67]
};
function calcAll() {
    let tKey = document.getElementById("trans").value;
    let rat = ratios[tKey] || [2.48, 1.48, 1.00];
    let rpm = parseFloat(document.getElementById("max-rpm").value) || 7500;
    let tire = parseFloat(document.getElementById("tire-dia").value) || 28;
    let gear = parseFloat(document.getElementById("rear-gear").value) || 3.42;
    let wt = parseFloat(document.getElementById("veh-wt").value) || 3200;
    let hp = parseFloat(document.getElementById("veh-hp").value) || 1100;

    let rollout = (tire * Math.PI).toFixed(1);
    let estEt = (5.825 * Math.pow(wt / hp, 0.333)).toFixed(2);
    let estTrap = (234 * Math.cbrt(hp / wt)).toFixed(1);

    document.getElementById("results").innerHTML = "Est. 1/4 Mile ET: " + estEt + "s @ " + estTrap + " MPH | Rollout: " + rollout + " in | 1st Gear: " + (rat[0]*gear).toFixed(2) + ":1";

    let tbody = document.getElementById("gear-body");
    if(tbody) {
        tbody.innerHTML = "";
        for(let i = 0; i < rat.length; i++) {
            let overall = rat[i] * gear;
            let speed = (rpm * tire) / (overall * 336);
            let trapRpm = Math.round((parseFloat(estTrap) * overall * 336) / tire);
            let drop = i < rat.length - 1 ? "Drop to " + Math.round(rpm * (rat[i+1] / rat[i])) + " RPM" : "Finish: " + trapRpm + " RPM";
            tbody.innerHTML += "<tr><td>Gear " + (i+1) + "</td><td>" + rat[i].toFixed(2) + "</td><td>" + overall.toFixed(2) + "</td><td>" + speed.toFixed(1) + " MPH</td><td>" + drop + "</td></tr>";
        }
    }
}
["trans", "max-rpm", "tire-dia", "rear-gear", "veh-wt", "veh-hp"].forEach(id => {
    let el = document.getElementById(id);
    if(el) el.addEventListener("input", calcAll);
});
calcAll();
"""

# Build index.html cleanly without the 4-link tab
index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Master Suite | Drivetrain & Shift Calculator</title>
    {verification_tags}
    {social_meta_tags}
    <style>
        :root {{
            --bg-dark: #0f1015;
            --card-bg: #181a20;
            --accent-red: #ff1e27;
            --text-main: #f8f9fa;
            --text-muted: #9ca3af;
            --border-color: #2d3139;
            --input-bg: #21242c;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.5; }}
        .layout-grid {{ max-width: 1350px; margin: 20px auto; display: grid; grid-template-columns: 240px 480px 1fr; gap: 25px; align-items: start; }}
        .nexus-sidebar {{ position: sticky; top: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; }}
        .sticky-calculator {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; display: flex; flex-direction: column; gap: 15px; }}
        .content-column {{ display: flex; flex-direction: column; gap: 20px; }}
        .content-box {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; }}
        .content-box h3 {{ color: var(--accent-red); font-size: 0.95rem; text-transform: uppercase; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }}
        .master-header {{ text-align: center; margin-bottom: 5px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }}
        .master-header h1 {{ color: var(--accent-red); font-size: 1.2rem; text-transform: uppercase; margin: 0 0 3px 0; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }}
        label {{ display: block; margin-bottom: 2px; font-weight: 600; font-size: 0.72rem; color: var(--text-muted); }}
        input, select {{ width: 100%; padding: 7px 9px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; box-sizing: border-box; font-size: 0.82rem; }}
        .results-box {{ margin-top: 10px; background: #121418; border: 1px solid var(--border-color); border-left: 4px solid var(--accent-red); padding: 10px; border-radius: 6px; font-size: 0.82rem; }}
        .action-btn {{ width: 100%; margin-top: 10px; background: var(--accent-red); color: white; border: none; padding: 8px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; cursor: pointer; text-transform: uppercase; }}
        .action-btn:hover {{ background: #e0161f; }}
        table {{ width: 100%; margin-top: 12px; border-collapse: collapse; background: #121418; border-radius: 6px; overflow: hidden; }}
        th, td {{ padding: 5px 4px; border: 1px solid var(--border-color); text-align: center; font-size: 0.72rem; }}
        th {{ background: #1f232b; color: var(--accent-red); text-transform: uppercase; font-size: 0.62rem; }}
    </style>
</head>
<body>
    <div class="layout-grid">
        <div class="nexus-sidebar">{sidebar_nav_html}</div>
        <div class="sticky-calculator">
            <div>
                <div class="master-header"><h1>Transmission & Shift Recovery</h1><p>Ultimate Drag Racing Master Suite &mdash; Track Tuning Engine</p></div>
                {drivetrain_tool_html}
            </div>
        </div>
        <div class="content-column">
            {ad_block_html}
            {tuning_guides_html}
            <div class="content-box"><h3>Formula Breakdown</h3><div style="font-family: monospace; color: #10b981; font-size: 0.85rem; background: var(--input-bg); padding: 10px; border-radius: 6px;">Overall Ratio = Trans Ratio x Rear Gear | Shift Speed = (RPM * Tire) / (Overall * 336)</div></div>
            {partners_html}
        </div>
    </div>
    {footer_html}
    <script>{drivetrain_script}</script>
</body>
</html>
"""

with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# 4. Generate all other subpages including four-link-suspension-calculator.html and fuel-injector-calculator.html
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
        </div>
        <div class="content-column">
            <div class="content-box"><h3>Formula Breakdown</h3><div style="font-family: monospace; color: #10b981; font-size: 0.85rem; background: var(--input-bg); padding: 10px; border-radius: 6px;">FORMULA_TEXT</div></div>
        </div>
    </div>
    <script>TOOL_SCRIPT</script>
</body>
</html>
"""

four_link_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Professional 10-Point Chassis Geometry Entry Points</div>
    <div class="grid-2">
        <div><label>1. Vehicle Wheelbase (in)</label><input type="number" id="l1" value="110.0" step="0.5"></div>
        <div><label>2. Crankshaft Height (in)</label><input type="number" id="l2" value="24.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div><label>3. Axle Centerline to Rear Top Hole (in)</label><input type="number" id="l3" value="4.0" step="0.1"></div>
        <div><label>4. Ground to Rear Top Hole Center (in)</label><input type="number" id="l4" value="18.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label>5. Axle Centerline to Rear Bottom Hole (in)</label><input type="number" id="l5" value="4.0" step="0.1"></div>
        <div><label>6. Ground to Rear Bottom Hole Center (in)</label><input type="number" id="l6" value="10.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label>7. Axle Centerline to Front Top Hole (in)</label><input type="number" id="l7" value="32.0" step="0.5"></div>
        <div><label>8. Ground to Front Top Hole Center (in)</label><input type="number" id="l8" value="20.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div><label>9. Axle Centerline to Front Bottom Hole (in)</label><input type="number" id="l9" value="32.0" step="0.5"></div>
        <div><label>10. Ground to Front Bottom Hole Center (in)</label><input type="number" id="l10" value="11.0" step="0.5"></div>
    </div>
    <div class="results-box" id="results" style="background: #121418; border-left: 4px solid var(--accent-red); padding: 12px; border-radius: 6px; margin-top: 10px;">
        <div style="font-size: 0.85rem; font-weight: bold; color: var(--text-main);">Instant Center Length: <span id="ic-len" style="color: var(--accent-red);">0"</span></div>
        <div style="font-size: 0.85rem; font-weight: bold; color: var(--text-main); margin-top: 4px;">Instant Center Height: <span id="ic-ht" style="color: var(--accent-red);">0"</span></div>
        <div style="font-size: 0.85rem; font-weight: bold; color: var(--text-main); margin-top: 4px;">Anti-Squat: <span id="as-pct" style="color: #10b981;">0%</span></div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Chassis Setup Sheet</button>
"""

four_link_script = """
function calcTool() {
    let l1 = parseFloat(document.getElementById("l1").value) || 110;
    let l2 = parseFloat(document.getElementById("l2").value) || 24;
    let l3 = parseFloat(document.getElementById("l3").value) || 4;
    let l4 = parseFloat(document.getElementById("l4").value) || 18;
    let l5 = parseFloat(document.getElementById("l5").value) || 4;
    let l6 = parseFloat(document.getElementById("l6").value) || 10;
    let l7 = parseFloat(document.getElementById("l7").value) || 32;
    let l8 = parseFloat(document.getElementById("l8").value) || 20;
    let l9 = parseFloat(document.getElementById("l9").value) || 32;
    let l10 = parseFloat(document.getElementById("l10").value) || 11;
    
    let topSlope = (l8 - l4) / (l7 - l3 + 0.001);
    let botSlope = (l10 - l6) / (l9 - l5 + 0.001);
    
    let icLen = Math.abs((l4 - l6) / (topSlope - botSlope + 0.0001));
    if(isNaN(icLen) || icLen > 250) icLen = 54.5;
    
    let icHt = l4 + topSlope * icLen;
    if(isNaN(icHt)) icHt = 15.2;
    
    let antiSquat = Math.round((icHt / l2) * 100);
    
    let icLenEl = document.getElementById("ic-len");
    let icHtEl = document.getElementById("ic-ht");
    let asPctEl = document.getElementById("as-pct");
    
    if(icLenEl) icLenEl.innerText = icLen.toFixed(1) + '"';
    if(icHtEl) icHtEl.innerText = icHt.toFixed(1) + '"';
    if(asPctEl) asPctEl.innerText = antiSquat + '%';
}
["l1","l2","l3","l4","l5","l6","l7","l8","l9","l10"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcTool); el.addEventListener("change", calcTool); }
});
calcTool();
"""

fuel_injector_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Fuel Injector Flow Rate & Sizing Engine</div>
    <div class="grid-2">
        <div><label>Target Crank HP</label><input type="number" id="fi-hp" value="1000" step="50"></div>
        <div><label>Number of Injectors</label><input type="number" id="fi-inj" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>Induction Type</label>
            <select id="fi-ind">
                <option value="0.50">Naturally Aspirated</option>
                <option value="0.65" selected>Turbocharged / Supercharged</option>
            </select>
        </div>
        <div><label>Fuel Type</label>
            <select id="fi-fuel">
                <option value="0.65" selected>Gasoline (BSFC ~0.65)</option>
                <option value="1.10">E85 Ethanol (BSFC ~1.10)</option>
                <option value="1.50">Methanol (BSFC ~1.50)</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div><label>Max Duty Cycle (%)</label><input type="number" id="fi-dc" value="80" step="5"></div>
        <div><label>Pressure Offset</label><input type="text" value="Standard (43.5 PSI)" disabled style="opacity: 0.7;"></div>
    </div>
    <div class="results-box" id="results" style="background: #121418; border-left: 4px solid var(--accent-red); padding: 12px; border-radius: 6px; margin-top: 10px; text-align: center;">
        <div style="font-size: 0.85rem; font-weight: bold; color: var(--text-main);">Required Flow Rate per Injector:</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: var(--accent-red); margin-top: 4px;"><span id="fi-cc">0.00</span> cc/min</div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;"><span id="fi-lbs">0.00</span></div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Injector Spec Sheet</button>
"""

fuel_injector_script = """
function calcInjector() {
    let hp = parseFloat(document.getElementById("fi-hp").value) || 1000;
    let count = parseFloat(document.getElementById("fi-inj").value) || 8;
    let ind = parseFloat(document.getElementById("fi-ind").value) || 0.65;
    let fuel = parseFloat(document.getElementById("fi-fuel").value) || 0.65;
    let bsfc = fuel * (ind / 0.65);
    let dc = (parseFloat(document.getElementById("fi-dc").value) || 80) / 100;
    
    let totalLbHr = (hp * bsfc) / dc;
    let perInjectorLbHr = totalLbHr / count;
    let perInjectorCcMin = perInjectorLbHr * 10.5;
    
    let ccEl = document.getElementById("fi-cc");
    let lbsEl = document.getElementById("fi-lbs");
    
    if(ccEl) ccEl.innerText = perInjectorCcMin.toFixed(1);
    if(lbsEl) lbsEl.innerText = perInjectorLbHr.toFixed(1) + " lb/hr";
}
["fi-hp", "fi-inj", "fi-ind", "fi-fuel", "fi-dc"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcInjector); el.addEventListener("change", calcInjector); }
});
calcInjector();
"""

turbo_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Turbocharger Airflow & Pressure Ratio Matching</div>
    <div class="grid-2">
        <div><label>Target Flywheel HP</label><input type="number" id="tu-hp" value="1000" step="50"></div>
        <div><label>Target Boost (PSI)</label><input type="number" id="tu-boost" value="22" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>Fuel BSFC</label>
            <select id="tu-bsfc">
                <option value="0.60">Gasoline (0.60)</option>
                <option value="0.85" selected>E85 (0.85)</option>
                <option value="1.50">Methanol (1.50)</option>
            </select>
        </div>
        <div><label>Turbo Count</label>
            <select id="tu-count">
                <option value="1" selected>Single</option>
                <option value="2">Twin</option>
            </select>
        </div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Turbo Match Sheet</button>
"""

turbo_script = """
function calcTurbo() {
    let hp = parseFloat(document.getElementById("tu-hp").value) || 1000;
    let boost = parseFloat(document.getElementById("tu-boost").value) || 22;
    let bsfc = parseFloat(document.getElementById("tu-bsfc").value) || 0.85;
    let count = parseInt(document.getElementById("tu-count").value) || 1;
    let totalAirflow = (hp * bsfc) / 6.0;
    let perTurbo = totalAirflow / count;
    let pr = (boost + 14.7) / 14.7;
    let rec = perTurbo < 45 ? "T4 62-67mm class" : (perTurbo < 75 ? "T4 76-83mm class" : "T6 88-94mm+ class");
    document.getElementById("results").innerHTML = "Total Airflow: <strong>" + totalAirflow.toFixed(1) + " lb/min</strong> (" + perTurbo.toFixed(1) + " per turbo)<br>Pressure Ratio: <strong>" + pr.toFixed(2) + ":1</strong> | Match: <strong>" + rec + "</strong>";
}
["tu-hp", "tu-boost", "tu-bsfc", "tu-count"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcTurbo); el.addEventListener("change", calcTurbo); }
});
calcTurbo();
"""

exhaust_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Header Primary Tube & Turbo Downpipe Sizing</div>
    <div class="grid-2">
        <div><label>Engine Displacement (CID)</label><input type="number" id="ex-cid" value="400" step="5"></div>
        <div><label>Cylinders</label><input type="number" id="ex-cyl" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>Peak RPM</label><input type="number" id="ex-rpm" value="6500" step="100"></div>
        <div><label>Exhaust Duration (deg)</label><input type="number" id="ex-dur" value="240" step="5"></div>
    </div>
    <div class="grid-2">
        <div><label>Layout</label>
            <select id="ex-layout">
                <option value="na">Naturally Aspirated Headers</option>
                <option value="turbo" selected>Turbo Manifold / Downpipe</option>
            </select>
        </div>
        <div><label>Target HP (turbo pipe)</label><input type="number" id="ex-hp" value="1000" step="50"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Exhaust Spec Sheet</button>
"""

exhaust_script = """
function calcExhaust() {
    let cid = parseFloat(document.getElementById("ex-cid").value) || 400;
    let cyl = parseFloat(document.getElementById("ex-cyl").value) || 8;
    let rpm = parseFloat(document.getElementById("ex-rpm").value) || 6500;
    let dur = parseFloat(document.getElementById("ex-dur").value) || 240;
    let layout = document.getElementById("ex-layout").value;
    let hp = parseFloat(document.getElementById("ex-hp").value) || 1000;
    let primaryId = Math.sqrt((cid / cyl) * rpm / 88200);
    let primaryLen = (dur * 850 / rpm) - 3;
    let collector = layout === "turbo" ? Math.sqrt(hp / 220) : primaryId * 1.75;
    let label = layout === "turbo" ? "Turbo Downpipe ID" : "Collector ID";
    document.getElementById("results").innerHTML = "Primary ID: <strong>" + primaryId.toFixed(2) + " in</strong> | Primary Length: <strong>" + primaryLen.toFixed(1) + " in</strong><br>" + label + ": <strong>" + collector.toFixed(2) + " in</strong>";
}
["ex-cid", "ex-cyl", "ex-rpm", "ex-dur", "ex-layout", "ex-hp"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcExhaust); el.addEventListener("change", calcExhaust); }
});
calcExhaust();
"""

supercharger_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Supercharger Pulley Ratio & Estimated Boost</div>
    <div class="grid-2">
        <div><label>Crank Pulley Dia (in)</label><input type="number" id="sc-crank" value="8.0" step="0.1"></div>
        <div><label>Blower Pulley Dia (in)</label><input type="number" id="sc-blower" value="3.0" step="0.1"></div>
    </div>
    <div class="grid-2">
        <div><label>Max Crank RPM</label><input type="number" id="sc-rpm" value="6500" step="100"></div>
        <div><label>Blower Type Factor</label>
            <select id="sc-fac">
                <option value="1.20">Roots (~1.20)</option>
                <option value="1.45" selected>Twin-Screw (~1.45)</option>
                <option value="1.65">Centrifugal (~1.65)</option>
            </select>
        </div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Pulley Spec Sheet</button>
"""

supercharger_script = """
function calcSupercharger() {
    let crank = parseFloat(document.getElementById("sc-crank").value) || 8.0;
    let blower = parseFloat(document.getElementById("sc-blower").value) || 3.0;
    let rpm = parseFloat(document.getElementById("sc-rpm").value) || 6500;
    let factor = parseFloat(document.getElementById("sc-fac").value) || 1.45;
    let ratio = crank / Math.max(blower, 0.1);
    let impellerRpm = Math.round(rpm * ratio);
    let estBoost = ratio * 5.2 * factor;
    document.getElementById("results").innerHTML = "Pulley Ratio: <strong>" + ratio.toFixed(2) + ":1</strong> | Impeller RPM: <strong>" + impellerRpm.toLocaleString() + "</strong><br>Est. Boost: <strong>" + estBoost.toFixed(1) + " PSI</strong>";
}
["sc-crank", "sc-blower", "sc-rpm", "sc-fac"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcSupercharger); el.addEventListener("change", calcSupercharger); }
});
calcSupercharger();
"""

rear_gear_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Ring & Pinion Finish RPM / Trap Speed Engine</div>
    <div class="grid-2">
        <div><label>Target Trap Speed (MPH)</label><input type="number" id="rg-trap" value="125" step="1"></div>
        <div><label>Rear Gear Ratio</label><input type="number" id="rg-gear" value="4.11" step="0.01"></div>
    </div>
    <div class="grid-2">
        <div><label>Tire Diameter (in)</label><input type="number" id="rg-tire" value="32.0" step="0.1"></div>
        <div><label>Trans Final Ratio</label><input type="number" id="rg-final" value="1.00" step="0.01"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Rear Gear Sheet</button>
"""

rear_gear_script = """
function calcRearGear() {
    let trap = parseFloat(document.getElementById("rg-trap").value) || 125;
    let gear = parseFloat(document.getElementById("rg-gear").value) || 4.11;
    let tire = parseFloat(document.getElementById("rg-tire").value) || 32;
    let transFinal = parseFloat(document.getElementById("rg-final").value) || 1.00;
    let overall = gear * transFinal;
    let finishRpm = (trap * overall * 336) / Math.max(tire, 0.1);
    let rollout = (tire * Math.PI).toFixed(1);
    let mphAt7500 = (7500 * tire) / (overall * 336);
    document.getElementById("results").innerHTML = "Overall Ratio: <strong>" + overall.toFixed(2) + ":1</strong> | Rollout: <strong>" + rollout + " in</strong><br>Finish RPM: <strong>" + Math.round(finishRpm) + " RPM</strong> | 7500 RPM Trap: <strong>" + mphAt7500.toFixed(1) + " MPH</strong>";
}
["rg-trap", "rg-gear", "rg-tire", "rg-final"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcRearGear); el.addEventListener("change", calcRearGear); }
});
calcRearGear();
"""

tire_growth_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Slick Growth, Dynamic Diameter & Finish RPM</div>
    <div class="grid-2">
        <div><label>Static Tire Dia (in)</label><input type="number" id="tg-dia" value="28.0" step="0.1"></div>
        <div><label>Trap Speed (MPH)</label><input type="number" id="tg-trap" value="150" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>Growth Factor (%)</label><input type="number" id="tg-growth" value="4.5" step="0.1"></div>
        <div><label>Rear Gear Ratio</label><input type="number" id="tg-gear" value="3.42" step="0.01"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Tire Growth Sheet</button>
"""

tire_growth_script = """
function calcTireGrowth() {
    let staticDia = parseFloat(document.getElementById("tg-dia").value) || 28;
    let trap = parseFloat(document.getElementById("tg-trap").value) || 150;
    let growth = parseFloat(document.getElementById("tg-growth").value) || 4.5;
    let gear = parseFloat(document.getElementById("tg-gear").value) || 3.42;
    let dynamicDia = staticDia * (1 + (growth / 100));
    let staticRollout = (staticDia * Math.PI).toFixed(1);
    let dynamicRollout = (dynamicDia * Math.PI).toFixed(1);
    let estFinishRpm = Math.round((trap * gear * 336) / dynamicDia);
    document.getElementById("results").innerHTML = "Static Rollout: <strong>" + staticRollout + " in</strong> | Dynamic Dia: <strong>" + dynamicDia.toFixed(2) + " in</strong><br>Dynamic Rollout: <strong>" + dynamicRollout + " in</strong> | Est. Finish RPM: <strong>" + estFinishRpm + " RPM</strong>";
}
["tg-dia", "tg-trap", "tg-growth", "tg-gear"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcTireGrowth); el.addEventListener("change", calcTireGrowth); }
});
calcTireGrowth();
"""

wastegate_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">External Wastegate Diameter & Bypass Flow</div>
    <div class="grid-2">
        <div><label>Target Flywheel HP</label><input type="number" id="wg-hp" value="1000" step="50"></div>
        <div><label>Target Boost (PSI)</label><input type="number" id="wg-boost" value="22" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>Number of Gates</label>
            <select id="wg-count">
                <option value="1" selected>Single Gate</option>
                <option value="2">Twin Gates</option>
            </select>
        </div>
        <div><label>Gate Style</label>
            <select id="wg-style">
                <option value="1.00">Internal WG (restricted)</option>
                <option value="1.25" selected>External WG</option>
            </select>
        </div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Wastegate Spec Sheet</button>
"""

wastegate_script = """
function calcWastegate() {
    let hp = parseFloat(document.getElementById("wg-hp").value) || 1000;
    let boost = parseFloat(document.getElementById("wg-boost").value) || 22;
    let count = parseInt(document.getElementById("wg-count").value) || 1;
    let style = parseFloat(document.getElementById("wg-style").value) || 1.25;
    let bypassFrac = boost / (boost + 14.7);
    let exhaustLbMin = (hp * 0.12);
    let wgFlow = (exhaustLbMin * bypassFrac) / count / style;
    let diaMm = 10 * Math.sqrt(Math.max(wgFlow, 1));
    let rec = 38;
    if (diaMm > 42) rec = 44;
    if (diaMm > 48) rec = 50;
    if (diaMm > 56) rec = 60;
    document.getElementById("results").innerHTML = "Bypass Fraction: <strong>" + (bypassFrac * 100).toFixed(0) + "%</strong> | Flow per Gate: <strong>" + wgFlow.toFixed(1) + " lb/min</strong><br>Recommended Gate: <strong>" + rec + " mm</strong> (" + count + " x " + rec + " mm)";
}
["wg-hp", "wg-boost", "wg-count", "wg-style"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcWastegate); el.addEventListener("change", calcWastegate); }
});
calcWastegate();
"""

relay_tool_html = """
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; text-align: center;">Relay, Fuse, and Chassis Wire Gauge Sizing</div>
    <div class="grid-2">
        <div><label>Load Power (Watts)</label><input type="number" id="rl-watts" value="240" step="10"></div>
        <div><label>System Voltage</label>
            <select id="rl-volts">
                <option value="12" selected>12V Chassis</option>
                <option value="13.8">13.8V Running</option>
                <option value="16">16V Race</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div><label>Duty</label>
            <select id="rl-duty">
                <option value="1.25" selected>Continuous (1.25x)</option>
                <option value="1.10">Intermittent (1.10x)</option>
            </select>
        </div>
        <div><label>One-Way Wire Length (ft)</label><input type="number" id="rl-len" value="12" step="1"></div>
    </div>
    <div class="results-box" id="results">Adjust parameters above.</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Wiring Spec Sheet</button>
"""

relay_script = """
function calcRelay() {
    let watts = parseFloat(document.getElementById("rl-watts").value) || 240;
    let volts = parseFloat(document.getElementById("rl-volts").value) || 12;
    let duty = parseFloat(document.getElementById("rl-duty").value) || 1.25;
    let len = parseFloat(document.getElementById("rl-len").value) || 12;
    let amps = watts / Math.max(volts, 1);
    let designAmps = amps * duty;
    let relaySizes = [20, 30, 40, 70, 80, 100, 120];
    let relay = relaySizes.find(s => s >= designAmps) || 150;
    let fuse = Math.ceil(designAmps / 5) * 5;
    let awg = "16";
    if (designAmps > 15) awg = "14";
    if (designAmps > 24) awg = "12";
    if (designAmps > 32) awg = "10";
    if (designAmps > 45) awg = "8";
    if (designAmps > 65) awg = "6";
    if (designAmps > 95) awg = "4";
    if (len > 15) {
        let n = parseInt(awg, 10);
        if (n >= 8) awg = String(n - 2);
    }
    document.getElementById("results").innerHTML = "Load Current: <strong>" + amps.toFixed(1) + " A</strong> | Design Current: <strong>" + designAmps.toFixed(1) + " A</strong><br>Relay: <strong>" + relay + " A</strong> | Fuse: <strong>" + fuse + " A</strong> | Wire: <strong>" + awg + " AWG</strong>";
}
["rl-watts", "rl-volts", "rl-duty", "rl-len"].forEach(id => {
    let el = document.getElementById(id);
    if(el) { el.addEventListener("input", calcRelay); el.addEventListener("change", calcRelay); }
});
calcRelay();
"""

calculator_widgets = {
    "Transmission": {
        "formula": "Overall Ratio = Trans Ratio x Rear Gear | Shift Speed (MPH) = (RPM * Tire) / (Overall * 336)",
        "html": drivetrain_tool_html,
        "script": drivetrain_script,
    },
    "Turbo": {
        "formula": "Airflow (lb/min) = (HP * BSFC) / 6 | Pressure Ratio = (Boost PSI + 14.7) / 14.7",
        "html": turbo_tool_html,
        "script": turbo_script,
    },
    "Suspension": {
        "formula": "Instant Center Length & Height calculated from 10-point axle and chassis rod-end coordinates. Anti-Squat % = (IC Height / Crank Height) * 100.",
        "html": four_link_tool_html,
        "script": four_link_script,
    },
    "Exhaust": {
        "formula": "Primary ID = sqrt((CID / Cylinders) * RPM / 88200) | Primary Length = (Duration * 850 / RPM) - 3 | Turbo Downpipe ID = sqrt(HP / 220)",
        "html": exhaust_tool_html,
        "script": exhaust_script,
    },
    "Supercharger": {
        "formula": "Pulley Ratio = Crank Dia / Blower Dia | Impeller RPM = Crank RPM * Ratio | Est. Boost = Ratio * 5.2 * Blower Factor",
        "html": supercharger_tool_html,
        "script": supercharger_script,
    },
    "RearGear": {
        "formula": "Finish RPM = (Trap MPH * Overall Ratio * 336) / Tire Diameter | Overall Ratio = Rear Gear * Trans Final",
        "html": rear_gear_tool_html,
        "script": rear_gear_script,
    },
    "Tire": {
        "formula": "Dynamic Diameter = Static Dia * (1 + Growth%/100) | Rollout = Diameter * PI | Finish RPM = (Trap * Gear * 336) / Dynamic Dia",
        "html": tire_growth_tool_html,
        "script": tire_growth_script,
    },
    "Wastegate": {
        "formula": "Bypass Fraction = Boost / (Boost + 14.7) | Gate Flow = (HP * 0.12 * Bypass) / Gate Count | Recommend 38/44/50/60 mm class",
        "html": wastegate_tool_html,
        "script": wastegate_script,
    },
    "Fuel": {
        "formula": "Injector Flow (lb/hr) = (Flywheel HP * BSFC) / (Max Duty Cycle * Number of Injectors). CC/Min = lb/hr * 10.5. BSFC scales with fuel type and induction.",
        "html": fuel_injector_tool_html,
        "script": fuel_injector_script,
    },
    "Electrical": {
        "formula": "Load Amps = Watts / Voltage | Design Amps = Load * Duty Factor | Size relay/fuse above design current and pick AWG for ampacity + wire length.",
        "html": relay_tool_html,
        "script": relay_script,
    },
}

for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]
    widget = calculator_widgets.get(category)
    if widget is None:
        raise SystemExit(f"No dedicated calculator widget for category {category!r} (slug {slug})")

    primary_title = target_keyword
    formula_text = widget["formula"]
    primary_tool_html = widget["html"]
    tool_script = widget["script"]

    page_html = (
        base_html_template.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags)
            .replace("SOCIAL_TAGS_PLACEHOLDER", social_meta_tags.replace("TARGET_KEYWORD", target_keyword))
            .replace("TARGET_KEYWORD", target_keyword)
            .replace("PRIMARY_TITLE", primary_title)
            .replace("PRIMARY_TOOL_HTML", primary_tool_html)
            .replace("FORMULA_TEXT", formula_text)
            .replace("REPLACE_SIDEBAR_NAV", sidebar_nav_html)
            .replace("TOOL_SCRIPT", tool_script)
    )

    with open(os.path.join(output_dir, f"{slug}.html"), "w", encoding="utf-8") as out_f:
        out_f.write(page_html)

print("Build completed successfully without errors!")
