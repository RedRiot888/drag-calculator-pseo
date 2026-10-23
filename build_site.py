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

# Option 1: Clean category filter + search bar + elegant card grid
utilities_grid_html = '''
<div style="display: flex; gap: 8px; margin-bottom: 12px;">
    <input type="text" id="util-search" placeholder="🔍 Search tools..." onkeyup="filterUtils()" style="flex: 1; padding: 8px 10px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; font-size: 0.8rem; outline: none; transition: border-color 0.2s;" onfocus="this.style.borderColor='var(--accent-red)'" onblur="this.style.borderColor='var(--border-color)'">
    <select id="util-cat-filter" onchange="filterUtils()" style="width: 140px; padding: 8px; background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-main); border-radius: 6px; font-size: 0.8rem; outline: none;">
        <option value="all">All Systems</option>
        <option value="transmission">Transmission</option>
        <option value="forced-induction">Forced Induction</option>
        <option value="exhaust">Exhaust</option>
        <option value="fuel">Fuel & EFI</option>
        <option value="chassis">Chassis & Tires</option>
        <option value="electrical">Electrical</option>
    </select>
</div>
<div id="utilities-container" style="display: grid; grid-template-columns: 1fr; gap: 8px; max-height: 440px; overflow-y: auto; padding-right: 4px;">
'''

for row in pages:
    slug = row["slug"]
    keyword = row["target_keyword"]
    cat = row["category"]
    
    # Map category group slug for filtering
    filter_group = "transmission"
    if cat in ["Turbo", "Supercharger", "Wastegate"]: filter_group = "forced-induction"
    elif cat == "Exhaust": filter_group = "exhaust"
    elif cat == "Fuel": filter_group = "fuel"
    elif cat in ["RearGear", "Tire"]: filter_group = "chassis"
    elif cat == "Electrical": filter_group = "electrical"
    
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
    <a href="{slug}.html" class="util-card" data-keyword="{keyword.lower()}" data-group="{filter_group}" style="background: linear-gradient(135deg, var(--input-bg) 0%, var(--card-bg) 100%); border: 1px solid var(--border-color); border-left: 3px solid var(--accent-red); padding: 10px 12px; border-radius: 6px; text-decoration: none; display: flex; align-items: center; gap: 10px; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
        <span style="font-size: 1.1rem; flex-shrink: 0;">{icon}</span>
        <div style="display: flex; flex-direction: column;">
            <span style="font-size: 0.78rem; font-weight: 600; color: var(--text-main); line-height: 1.2;">{keyword}</span>
            <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; margin-top: 2px;">{cat}</span>
        </div>
    </a>
    '''

utilities_grid_html += '</div>\n'

search_script = """
<script>
    function filterUtils() {
        let input = document.getElementById('util-search').value.toLowerCase();
        let selectedCat = document.getElementById('util-cat-filter').value;
        let cards = document.querySelectorAll('.util-card');
        
        cards.forEach(card => {
            let kw = card.getAttribute('data-keyword');
            let group = card.getAttribute('data-group');
            let matchesSearch = kw.includes(input);
            let matchesCat = (selectedCat === 'all' || group === selectedCat);
            
            if(matchesSearch && matchesCat) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }
</script>
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
                    <div style="font-size: 0.78rem; font-weight: bold; color: var(--text-main