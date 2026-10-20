import csv

def generate_all_pages():
    rows = []

    # 1. Standard Drag Calculators (Transmission, Gear, Tire)
    transmissions = [
        {"code": "powerglide", "name": "Powerglide (2-Speed)", "gear1": 1.76},
        {"code": "th400", "name": "TH400 (3-Speed)", "gear1": 2.48},
        {"code": "t56", "name": "T56 Manual (6-Speed)", "gear1": 2.66},
        {"code": "zf8hp", "name": "ZF 8HP (8-Speed)", "gear1": 4.71}
    ]
    gear_ratios = [3.08, 3.23, 3.42, 3.55, 3.73, 3.90, 4.10, 4.30, 4.56, 4.88, 5.13]
    tire_diameters = [26.0, 28.0, 29.5, 31.0, 33.0]

    for trans in transmissions:
        for gear in gear_ratios:
            for tire in tire_diameters:
                slug = f"{trans['code']}-{gear}-gear-{tire}-tire"
                keyword = f"{trans['name']} {gear} gear {tire} inch tire drag calculator"
                rows.append({
                    "slug": slug,
                    "target_keyword": keyword,
                    "transmission": trans['name'],
                    "rear_gear": str(gear),
                    "tire_diameter": str(tire),
                    "page_url": f"https://dragcalculators.co/{slug}"
                })

    # 2. Fuel System Calculators
    hp_targets = range(400, 1601, 100)
    fuel_types = ["gasoline", "e85"]
    for hp in hp_targets:
        for fuel in fuel_types:
            slug = f"fuel-calculator-{hp}hp-{fuel}"
            keyword = f"{hp} hp {fuel} fuel injector size and pump calculator"
            rows.append({
                "slug": slug,
                "target_keyword": keyword,
                "transmission": f"Fuel System ({hp}HP {fuel.upper()})",
                "rear_gear": "0.0",
                "tire_diameter": "0.0",
                "page_url": f"https://dragcalculators.co/{slug}"
            })

    # 3. CAS (Compressed Air Supercharging) / Boost Calculators
    boost_levels = [15, 20, 25, 30, 35, 40]
    for boost in boost_levels:
        slug = f"cas-compressed-air-supercharger-{boost}psi-boost"
        keyword = f"compressed air supercharger {boost} psi boost calculator"
        rows.append({
            "slug": slug,
            "target_keyword": keyword,
            "transmission": f"CAS Supercharger ({boost} PSI)",
            "rear_gear": "0.0",
            "tire_diameter": "0.0",
            "page_url": f"https://dragcalculators.co/{slug}"
        })

    # 4. Turbo Sizing Calculators
    turbo_hp_targets = [500, 600, 750, 900, 1000, 1250, 1500, 2000]
    turbo_setups = ["single", "twin"]
    for hp in turbo_hp_targets:
        for setup in turbo_setups:
            slug = f"turbo-sizing-{setup}-{hp}hp-calculator"
            keyword = f"{setup} turbocharger sizing calculator for {hp} hp engine"
            rows.append({
                "slug": slug,
                "target_keyword": keyword,
                "transmission": f"Turbo Sizing ({setup.upper()} - {hp}HP)",
                "rear_gear": "0.0",
                "tire_diameter": "0.0",
                "page_url": f"https://dragcalculators.co/{slug}"
            })

    # 5. Supercharger Pulley & Boost Calculators
    crank_pulleys = [7.5, 8.0, 8.5]
    blower_pulleys = [2.75, 3.0, 3.25, 3.5, 3.75, 4.0]
    blower_types = ["roots", "centrifugal", "twin-screw"]

    for crank in crank_pulleys:
        for blower in blower_pulleys:
            for b_type in blower_types:
                slug = f"supercharger-pulley-{b_type}-{crank}in-crank-{blower}in-blower"
                keyword = f"{b_type} supercharger pulley ratio calculator {crank} inch crank {blower} inch blower"
                rows.append({
                    "slug": slug,
                    "target_keyword": keyword,
                    "transmission": f"Supercharger Pulley ({b_type.title()} - {crank}in / {blower}in)",
                    "rear_gear": "0.0",
                    "tire_diameter": "0.0",
                    "page_url": f"https://dragcalculators.co/{slug}"
                })

    # Save everything to CSV
    with open("pseo_pages_list.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "target_keyword", "transmission", "rear_gear", "tire_diameter", "page_url"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Successfully generated {len(rows)} total programmatic pages in CSV!")

if __name__ == "__main__":
    generate_all_pages()
    