# Fuel Injector tool HTML & Script
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
                <option value="0.55">Methanol (BSFC ~1.50)</option>
            </select>
        </div>
    </div>
    <div class="grid-2">
        <div><label>Max Duty Cycle (%)</label><input type="number" id="fi-dc" value="80" step="5"></div>
        <div><label>Pressure Offset</label><input type="text" value="Standard (43.5 PSI)" disabled style="opacity: 0.7;"></div>
    </div>
    <div class="results-box" id="results" style="background: #121418; border-left: 4px solid var(--accent-red); padding: 12px; border-radius: 6px; margin-top: 10px; text-align: center;">
        <div style="font-size: 0.95rem; font-weight: bold; color: var(--text-main);">Required Flow Rate per Injector:</div>
        <div style="font-size: 1.3rem; font-weight: bold; color: var(--accent-red); margin-top: 4px;"><span id="fi-cc">0.00</span> cc/min</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;"><span id="fi-lbs">0.00</span> lb/hr</div>
    </div>
    <button type="button" class="action-btn" onclick="window.print()">Print Injector Spec Sheet</button>
"""

fuel_injector_script = """
function calcInjector() {
    let hp = parseFloat(document.getElementById("fi-hp").value) || 1000;
    let count = parseFloat(document.getElementById("fi-inj").value) || 8;
    let bsfc = parseFloat(document.getElementById("fi-ind").value) || 0.65;
    let dc = (parseFloat(document.getElementById("fi-dc").value) || 80) / 100;
    
    // Total fuel flow in lbs/hr = (HP * BSFC) / DutyCycle
    let totalLbHr = (hp * bsfc) / dc;
    let perInjectorLbHr = totalLbHr / count;
    let perInjectorCcMin = perInjectorLbHr * 10.5; // conversion factor roughly 1 lb/hr = 10.5 cc/min
    
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