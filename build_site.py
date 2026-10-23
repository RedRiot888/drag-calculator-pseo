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

sidebar_nav_html = """
<div style="display: flex; flex-direction: column; gap: 4px;">
    <a href="index.html" class="nav-item active" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: var(--input-bg); border-left: 3px solid var(--accent-red); color: var(--text-main); text-decoration: none; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">
        <span>🏁 Popular / Master Hub</span>
        <span style="font-size: 0.65rem; color: var(--text-muted);">ALL</span>
    </a>
    <a href="transmission-shift-recovery-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>🏎️ Transmission & Gearing</span>
    </a>
    <a href="turbo-sizing-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>🌀 Forced Induction / Turbo</span>
    </a>
    <a href="exhaust-header-sizing-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>🔥 Exhaust & Airflow</span>
    </a>
    <a href="fuel-injector-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>⛽ Fueling & EFI</span>
    </a>
    <a href="tire-growth-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>🛞 Chassis & Tires</span>
    </a>
    <a href="automotive-relay-calculator.html" class="nav-item" style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; background: transparent; border-left: 3px solid transparent; color: var(--text-muted); text-decoration: none; border-radius: 4px; font-size: 0.78rem; transition: all 0.2s;">
        <span>⚡ Electrical & Wiring</span>
    </a>
</div>
"""

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
    <footer style="max-width: 1400px; margin: 40px auto 20px auto; text-align: center; border-top: 1px solid var(--border-color); padding-top: 20px; font-size: 0.8rem; color: var(--text-muted);">
        <p>&copy; 2026 Ultimate Drag Racing Calculator Suite. All rights reserved. Professional Track Tuning & Engineering Tools.</p>
        <p style="margin-top: 5px;">
            <a href="contact.html" style="color: var(--text-muted); text-decoration: none; margin: 0 10px;">Contact & Sponsorships</a> | 
            <a href="privacy.html" style="color: var(--text-muted); text-decoration: none; margin: 0 10px;">Privacy Policy & Affiliate Disclosure</a>
        </p>
        <p style="font-size: 0.72rem; color: #6b7280; margin-top: 8px;">Disclosure: We may earn an affiliate commission from qualifying purchases made through links on this site at no extra cost to you.</p>
    </footer>
"""

# Verification Meta Tags (Impact + Google Search Console)
verification_tags = """    <meta name='impact-site-verification' value='b2bb3042-cfc7-4ed4-b783-57a9b5a6451f'>
    <meta name='google-site-verification' content='google9e7c88791a3f2f72'>"""

master_index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Drag Racing Drivetrain & Shift RPM Calculator Suite</title>
    VERIFICATION_TAGS_PLACEHOLDER
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
            max-width: 1350px;
            margin: 20px auto;
            display: grid;
            grid-template-columns: 240px 480px 1fr;
            gap: 25px;
            align-items: start;
        }
        .nexus-sidebar {
            position: sticky;
            top: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            max-height: 90vh;
            overflow-y: auto;
        }
        .sticky-calculator {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        @media (max-width: 1100px) {
            .layout-grid { grid-template-columns: 1fr; }
            .nexus-sidebar { position: static; max-height: none; }
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
            background: var