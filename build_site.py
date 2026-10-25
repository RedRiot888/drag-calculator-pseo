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

sidebar_nav_html = """
<div style="display: flex; flex-direction: column; gap: 4px;">
    <a href="index.html" class="nav-item active" style="padding: 8px 10px; background: var(--input-bg); border-left: 3px solid var(--accent-red); color: var(--text-main); text-decoration: none; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">Popular / Master Hub</a>
    <a href="transmission-shift-recovery-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Transmission & Gearing</a>
    <a href="turbo-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Forced Induction / Turbo</a>
    <a href="four-link-suspension-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Suspension & 4-Link</a>
    <a href="exhaust-header-sizing-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Exhaust & Airflow</a>
    <a href="fuel-injector-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Fueling & EFI</a>
    <a href="tire-growth-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Chassis & Tires</a>
    <a href="automotive-relay-calculator.html" class="nav-item" style="padding: 8px 10px; color: var(--text-muted); text-decoration: none; font-size: 0.78rem;">Electrical & Wiring</a>
</div>
"""

ad_block_html = '<div class="content-box" style="text-align: center; background: #121418; border: 1px dashed var(--border-color);"><h3 style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">Advertisement Space</h3><div style="padding: 15px 10px; color: var(--text-muted); font-size: 0.80rem; background: var(--input-bg); border-radius: 6px;">Want your brand here?<br><a href="contact.html" style="color: var(--accent-red); text-decoration: none; font-weight: bold;">Contact for Track Sponsor Rates &rarr;</a></div></div>'
partners_html = '<div class="content-box"><h3>Industry Standard References</h3><ul style="list-style: none; padding: 0; margin: 0; font-size: 0.85rem; color: var(--text-muted);"><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Precision Turbo & Engine <span style="float: right; color: #10b981;">Verified Match</span></li><li style="padding: 6px 0; border-bottom: 1px dashed var(--border-color);">Strange Engineering <span style="float: right; color: #10b981;">Drivetrain Spec</span></li><li style="padding: 6px 0;">ATI Performance <span style="float: right; color: #10b981;">Transmission Tech</span></li></ul></div>'
tuning_guides_html = '<div class="content-box"><h3>Track-Side Tuning Cheat Sheets</h3><p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">1. Density Altitude (DA): Every 1,000 ft costs NA engines ~3% HP.<br>2. Torque Converter Slip: Target 5% to 8% slip at finish line.<br>