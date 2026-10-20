import os
import csv

output_dir = "."

# Templates for different categories so calculators make sense!
transmission_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{ --bg-dark: #121212; --card-bg: #1e1e1e; --accent-red: #e50914; --text-main: #f1f1f1; --text-muted: #aaa; --border-color: #333; }}
        body {{ font-family: sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        header {{ background: #1a1a1a; border-bottom: 2px solid var(--accent-red); padding: 30px 20px; text-align: center; }}
        header h1 {{ color: var(--accent-red); font-size: 2rem; text-transform: uppercase; margin-bottom: 5px; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        .box {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 30px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, select {{ width: 100%; padding: 10px; background: #2a2a2a; border: 1px solid var(--border-color); color: #fff; border-radius: 4px; box-sizing: border-box; }}
        .results {{ margin-top: 20px; background: #161616; border-left: 4px solid var(--accent-red); padding: 15px; border-radius: 4px; }}
        table {{ width: 100%; margin-top: 20px; border-collapse: collapse; background: #161616; }}
        th, td {{ padding: 10px; border: 1px solid var(--border-color); text-align: center; }}
        th {{ background: #222; color: var(--accent-red); }}
        .back {{ display: inline-block; margin-top: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <h1>{target_keyword}</h1>
        <a href="index.html" class="back">&larr; Back to All Calculators Hub</a>
    </header>
    <div class="container">
        <div class="box">
            <h2>Transmission & Gear Drop Analyzer</h2>
            <div class="grid-2">
                <div>
                    <label>Transmission Profile</label>
                    <select id="trans">
                        <option value="powerglide">Powerglide (1.76 / 1.00 - 2-Speed)</option>
                        <option value="th400">TH400 / 4L80e (2.48 / 1.48 / 1.00 - 3-Speed)</option>
                        <option value="th350">TH350 (2.52 / 1.52 / 1.00 - 3-Speed)</option>
                    </select>
                </div>
                <div>
                    <label>Max Shift RPM</label>
                    <input type="number" id="max-rpm" value="7500">
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Tire Diameter (inches)</label>
                    <input type="number" id="tire-dia" value="{tire_diameter}" step="0.1">
                </div>
                <div>
                    <label>Rear Gear Ratio</label>
                    <input type="number" id="rear-gear" value="{rear_gear}" step="0.01">
                </div>
            </div>
            <div class="results" id="results">Adjust parameters above to view shift recovery and RPM drop.</div>
            <table>
                <thead><tr><th>Gear</th><th>Trans Ratio</th><th>Overall Ratio</th><th>Shift Speed (MPH)</th><th>RPM Drop on Shift</th></tr></thead>
                <tbody id="gear-body"></tbody>
            </table>
        </div>
    </div>
    <script>
        const ratios = {{ powerglide: [1.76, 1.00], th400: [2.48, 1.48, 1.00], th350: [2.52, 1.52, 1.00] }};
        function calc() {{
            let tKey = document.getElementById("trans").value;
            let rat = ratios[tKey];
            let rpm = parseFloat(document.getElementById("max-rpm").value);
            let tire = parseFloat(document.getElementById("tire-dia").value);
            let gear = parseFloat(document.getElementById("rear-gear").value);
            
            let html = `<strong>Analysis:</strong><br>• Tire Rollout: ${(tire * Math.PI).toFixed(1)} inches<br>• 1st Gear Overall Ratio: ${(rat[0] * gear).toFixed(2)}:1`;
            document.getElementById("results").innerHTML = html;

            let tbody = document.getElementById("gear-body");
            tbody.innerHTML = "";
            for(let i=0; i<rat.length; i++) {{
                let overall = rat[i] * gear;
                let speed = (rpm * tire) / (overall * 336);
                let drop = i < rat.length - 1 ? `${Math.round(rpm * (rat[i+1]/rat[i]))} RPM recovery` : "Finish Line";
                tbody.innerHTML += `<tr><td>Gear ${i+1}</td><td>${rat[i].toFixed(2)}</td><td>${overall.toFixed(2)}</td><td>${speed.toFixed(1)} MPH</td><td>${drop}</td></tr>`;
            }}
        }}
        ["trans", "max-rpm", "tire-dia", "rear-gear"].forEach(id => document.getElementById(id).addEventListener("input", calc));
        calc();
    </script>
</body>
</html>
"""

supercharger_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{ --bg-dark: #121212; --card-bg: #1e1e1e; --accent-red: #e50914; --text-main: #f1f1f1; --text-muted: #aaa; --border-color: #333; }}
        body {{ font-family: sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        header {{ background: #1a1a1a; border-bottom: 2px solid var(--accent-red); padding: 30px 20px; text-align: center; }}
        header h1 {{ color: var(--accent-red); font-size: 2rem; text-transform: uppercase; margin-bottom: 5px; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        .box {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 30px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, select {{ width: 100%; padding: 10px; background: #2a2a2a; border: 1px solid var(--border-color); color: #fff; border-radius: 4px; box-sizing: border-box; }}
        .results {{ margin-top: 20px; background: #161616; border-left: 4px solid var(--accent-red); padding: 15px; border-radius: 4px; }}
        .back {{ display: inline-block; margin-top: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <h1>{target_keyword}</h1>
        <a href="index.html" class="back">&larr; Back to All Calculators Hub</a>
    </header>
    <div class="container">
        <div class="box">
            <h2>Supercharger Pulley & Boost Calculator</h2>
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
            <div class="results" id="results">Adjust parameters above to calculate pulley ratio and estimated boost pressure.</div>
        </div>
    </div>
    <script>
        function calc() {{
            let crank = parseFloat(document.getElementById("crank-dia").value) || 8.0;
            let blower = parseFloat(document.getElementById("blower-dia").value) || 3.0;
            let rpm = parseFloat(document.getElementById("crank-rpm").value) || 6500;
            let fac = parseFloat(document.getElementById("boost-fac").value) || 1.45;

            let ratio = crank / blower;
            let blowerRpm = rpm * ratio;
            let estBoost = (ratio - 1) * 7.5 * fac;

            document.getElementById("results").innerHTML = `
                <strong>Supercharger Calculation Results:</strong><br><br>
                • Pulley Ratio: <strong>${ratio.toFixed(2)}:1</strong><br>
                • Blower Impeller/Rotor RPM at Max Crank: <strong>${Math.round(blowerRpm).toLocaleString()} RPM</strong><br>
                • Estimated Boost Pressure: <strong>${estBoost.toFixed(1)} PSI</strong>
            `;
        }
        ["crank-dia", "blower-dia", "crank-rpm", "boost-fac"].forEach(id => document.getElementById(id).addEventListener("input", calc));
        calc();
    </script>
</body>
</html>
"""

turbo_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{ --bg-dark: #121212; --card-bg: #1e1e1e; --accent-red: #e50914; --text-main: #f1f1f1; --text-muted: #aaa; --border-color: #333; }}
        body {{ font-family: sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; line-height: 1.6; }}
        header {{ background: #1a1a1a; border-bottom: 2px solid var(--accent-red); padding: 30px 20px; text-align: center; }}
        header h1 {{ color: var(--accent-red); font-size: 2rem; text-transform: uppercase; margin-bottom: 5px; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        .box {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 30px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, select {{ width: 100%; padding: 10px; background: #2a2a2a; border: 1px solid var(--border-color); color: #fff; border-radius: 4px; box-sizing: border-box; }}
        .results {{ margin-top: 20px; background: #161616; border-left: 4px solid var(--accent-red); padding: 15px; border-radius: 4px; }}
        .back {{ display: inline-block; margin-top: 15px; color: var(--accent-red); text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <h1>{target_keyword}</h1>
        <a href="index.html" class="back">&larr; Back to All Calculators Hub</a>
    </header>
    <div class="container">
        <div class="box">
            <h2>Turbo Airflow & Compressor Map Calculator</h2>
            <div class="grid-2">
                <div>
                    <label>Target Horsepower (WHP)</label>
                    <input type="number" id="hp" value="1000" step="50">
                </div>
                <div>
                    <label>Fuel Type</label>
                    <select id="fuel">
                        <option value="gas">Gasoline (BSFC 0.60)</option>
                        <option value="e85">E85 / Alcohol (BSFC 0.85)</option>
                        <option value="methane">Methanol (BSFC 1.20)</option>
                    </select>
                </div>
            </div>
            <div class="grid-2">
                <div>
                    <label>Target Boost Pressure (PSI)</label>
                    <input type="number" id="boost" value="25" step="1">
                </div>
                <div>
                    <label>Turbo Configuration</label>
                    <select id="config">
                        <option value="single">Single Turbo</option>
                        <option value="twin">Twin Turbos (Split Flow)</option>
                    </select>
                </div>
            </div>
            <div class="results" id="results">Adjust parameters to calculate required airflow (lbs/min) and pressure ratio.</div>
        </div>
    </div>
    <script>
        function calc() {{
            let hp = parseFloat(document.getElementById("hp").value) || 1000;
            let fuel = document.getElementById("fuel").value;
            let boost = parseFloat(document.getElementById("boost").value) || 25;
            let config = document.getElementById("config").value;

            let bsfc = fuel === 'e85' ? 0.85 : (fuel === 'methane' ? 1.20 : 0.60);
            let airflow = (hp * bsfc) / 6.0; // lbs/min roughly
            let pr = (boost + 14.7) / 14.7;

            if(config === 'twin') airflow /= 2;

            document.getElementById("results").innerHTML = `
                <strong>Turbo Sizing Results:</strong><br><br>
                • Required Airflow per Turbo: <strong>${airflow.toFixed(1)} lbs/min</strong><br>
                • Compressor Pressure Ratio (PR): <strong>${pr.toFixed(2)}:1</strong><br>
                • Recommended Inducer Size Range: <strong>${Math.round(Math.sqrt(hp) * 2.1)}mm+</strong>
            `;
        }
        ["hp", "fuel", "boost", "config"].forEach(id => document.getElementById(id).addEventListener("input", calc));
        calc();
    </script>
</body>
</html>
"""

pages_created = 0
csv_file = "pseo_pages_list.csv"

if os.path.exists(csv_file):
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row["slug"]
            target_keyword = row["target_keyword"]
            category = row["category"]
            gear = row["rear_gear"]
            tire = row["tire_diameter"]

            # Select correct template based on category
            if category == "Transmission" or category == "RearGear":
                template = transmission_template
            elif category == "Supercharger":
                template = supercharger_template
            else:
                template = turbo_template

            page_content = template.format(
                title=f"{target_keyword} | DragCalculators.com",
                target_keyword=target_keyword,
                rear_gear=gear,
                tire_diameter=tire
            )

            file_path = os.path.join(output_dir, f"{slug}.html")
            with open(file_path, "w", encoding="utf-8") as out_f:
                out_f.write(page_content)
            pages_created += 1

print(f"Successfully compiled {pages_created} category-tailored pSEO calculators!")