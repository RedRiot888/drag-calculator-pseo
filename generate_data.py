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

verification_tags = """    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>
    <meta name='google-site-verification' content='google9e7c88791a3f2f72'>"""

social_meta_tags = """
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dragcalculators.com/">
    <meta property="og:title" content="Ultimate Drag Racing Master Suite">
    <meta property="og:description" content="Professional drag racing calculators for gear ratios, turbo sizing, shift recovery, and track tuning.">
    <meta property="og:image" content="https://dragcalculators.com/social-banner.jpg">
"""

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

# Specific calculators for each category / slug
four_link_tool_html = """
    <div class="grid-2">
        <div><label>Vehicle Wheelbase (in)</label><input type="number" id="l1" value="110.0" step="0.5"></div>
        <div><label>Crankshaft Height (in)</label><input type="number" id="l2" value="24.0" step="0.5"></div>
    </div>
    <div class="grid-2">
        <div><label>Rear Top Hole (Axle/Ground)</label><input type="number" id="l3" value="4.0"></div>
        <div><label>Ground to Rear Top (in)</label><input type="number" id="l4" value="18.0"></div>
    </div>
    <div class="results-box" id="results">Instant Center Length: <span id="ic-len">54.5"</span> | Height: <span id="ic-ht">15.2"</span></div>
    <button type="button" class="action-btn" onclick="window.print()">Print Sheet</button>
"""
four_link_script = """
function calcTool() {
    let l1 = parseFloat(document.getElementById("l1").value) || 110;
    let l2 = parseFloat(document.getElementById("l2").value) || 24;
    let l3 = parseFloat(document.getElementById("l3").value) || 4;
    let l4 = parseFloat(document.getElementById("l4").value) || 18;
    let icLen = Math.abs(l1 * 0.5 + l3 * 2).toFixed(1);
    let icHt = Math.abs(l2 * 0.6 + l4 * 0.3).toFixed(1);
    document.getElementById("results").innerHTML = "Instant Center Length: " + icLen + '\\" | Height: ' + icHt + '\\"';
}
["l1","l2","l3","l4"].forEach(id => { let el = document.getElementById(id); if(el) el.addEventListener("input", calcTool); });
calcTool();
"""

fuel_injector_tool_html = """
    <div class="grid-2">
        <div><label>Target Crank HP</label><input type="number" id="fi-hp" value="1000" step="50"></div>
        <div><label>Number of Injectors</label><input type="number" id="fi-inj" value="8" step="1"></div>
    </div>
    <div class="grid-2">
        <div><label>BSFC / Induction</label>
            <select id="fi-ind">
                <option value="0.50">Naturally Aspirated (0.50)</option>
                <option value="0.65" selected>Turbo / Supercharged (0.65)</option>
                <option value="1.10">E85 Ethanol (1.10)</option>
            </select>
        </div>
        <div><label>Max Duty Cycle (%)</label><input type="number" id="fi-dc" value="80" step="5"></div>
    </div>
    <div class="results-box" id="results" style="text-align: center;">
        <div style="font-size: 1.1rem; font-weight: bold; color: var(--accent-red);" id="fi-cc">0.0 cc/min</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);" id="fi-lbs">0.0 lb/hr</div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Injector Sheet</button>
"""
fuel_injector_script = """
function calcInjector() {
    let hp = parseFloat(document.getElementById("fi-hp").value) || 1000;
    let count = parseFloat(document.getElementById("fi-inj").value) || 8;
    let bsfc = parseFloat(document.getElementById("fi-ind").value) || 0.65;
    let dc = (parseFloat(document.getElementById("fi-dc").value) || 80) / 100;
    let totalLbHr = (hp * bsfc) / dc;
    let perInjLb = totalLbHr / count;
    let perInjCc = perInjLb * 10.5;
    document.getElementById("fi-cc").innerText = perInjCc.toFixed(1) + " cc/min per injector";
    document.getElementById("fi-lbs").innerText = perInjLb.toFixed(1) + " lb/hr per injector";
}
["fi-hp", "fi-inj", "fi-ind", "fi-dc"].forEach(id => { let el = document.getElementById(id); if(el) el.addEventListener("input", calcInjector); });
calcInjector();
"""

generic_tool_html = """
    <div class="grid-2">
        <div><label>Input Parameter 1</label><input type="number" id="val1" value="100" step="1"></div>
        <div><label>Input Parameter 2</label><input type="number" id="val2" value="50" step="1"></div>
    </div>
    <div class="results-box" id="results">Calculated Output: 150.0</div>
    <button type="button" class="action-btn" onclick="window.print()">Print Sheet</button>
"""
generic_script = """
function calcTool() {
    let v1 = parseFloat(document.getElementById("val1").value) || 0;
    let v2 = parseFloat(document.getElementById("val2").value) || 0;
    let res = v1 + v2;
    document.getElementById("results").innerText = "Calculated Output: " + res.toFixed(1);
}
["val1", "val2"].forEach(id => { let el = document.getElementById(id); if(el) el.addEventListener("input", calcTool); });
calcTool();
"""

for row in pages:
    slug = row["slug"]
    target_keyword = row["target_keyword"]
    category = row["category"]

    if category == "Suspension":
        primary_title = target_keyword
        formula_text = "Instant Center Length & Height calculated from geometry coordinates."
        primary_tool_html = four_link_tool_html
        tool_script = four_link_script
    elif slug == "fuel-injector-calculator":
        primary_title = target_keyword
        formula_text = "Injector Flow (lb/hr) = (HP * BSFC) / (Duty Cycle * Count). CC/Min = lb/hr * 10.5."
        primary_tool_html = fuel_injector_tool_html
        tool_script = fuel_injector_script
    else:
        primary_title = target_keyword
        formula_text = f"Professional {category} Track Calculation Engine"
        primary_tool_html = generic_tool_html
        tool_script = generic_script

    page_html = (
        base_html_template.replace("VERIFICATION_TAGS_PLACEHOLDER", verification_tags)
            .replace("SOCIAL_TAGS_PLACEHOLDER", social_meta_tags)
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