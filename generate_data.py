import csv

rows = [
    # Transmission & Gear Drop
    {"slug": "powerglide-3.08-gear-26.0-tire", "target_keyword": "Powerglide (2-Speed) 3.08 gear 26.0 inch tire drag calculator", "transmission": "Powerglide (2-Speed)", "rear_gear": "3.08", "tire_diameter": "26.0"},
    {"slug": "th400-3.73-gear-28.0-tire", "target_keyword": "TH400 (3-Speed) 3.73 gear 28.0 inch tire drag calculator", "transmission": "TH400 (3-Speed)", "rear_gear": "3.73", "tire_diameter": "28.0"},
    
    # Turbo Sizing & Boost Matrix
    {"slug": "turbo-sizing-800hp-gasoline", "target_keyword": "800 HP Gasoline Turbo Sizing & Compressor Map Calculator", "transmission": "Turbo Setup (Single)", "rear_gear": "3.55", "tire_diameter": "28.0"},
    {"slug": "turbo-sizing-1200hp-e85", "target_keyword": "1200 HP E85 Twin Turbo Airflow & Boost Calculator", "transmission": "Turbo Setup (Twin)", "rear_gear": "3.73", "tire_diameter": "31.0"},

    # Supercharger Pulley & Boost
    {"slug": "supercharger-pulley-15psi-roots", "target_keyword": "Roots Supercharger 15 PSI Boost Pulley Ratio Calculator", "transmission": "Roots Blower", "rear_gear": "3.42", "tire_diameter": "28.0"},
    {"slug": "supercharger-pulley-20psi-screws", "target_keyword": "Twin-Screw Supercharger 20 PSI Pulley Calculator", "transmission": "Twin-Screw Blower", "rear_gear": "3.89", "tire_diameter": "29.5"},

    # Rear Gear Ratio Math
    {"slug": "rear-gear-ratio-4.56-drag-racing", "target_keyword": "4.56 Ring and Pinion Rear Gear Quarter-Mile Calculator", "transmission": "Powerglide (2-Speed)", "rear_gear": "4.56", "tire_diameter": "32.0"},
    {"slug": "rear-gear-ratio-3.89-street-strip", "target_keyword": "3.89 Rear End Gear Ratio RPM & Trap Speed Calculator", "transmission": "TH400 (3-Speed)", "rear_gear": "3.89", "tire_diameter": "30.0"},

    # Tire Diameter & Growth
    {"slug": "tire-diameter-growth-33-slick", "target_keyword": "33 Inch Slick Tire Growth & Rollout Drag Calculator", "transmission": "Powerglide (2-Speed)", "rear_gear": "4.10", "tire_diameter": "33.0"},
    {"slug": "tire-diameter-growth-28-radial", "target_keyword": "28 Inch Drag Radial Effective Circumference Calculator", "transmission": "4L80e (Overdrive)", "rear_gear": "3.50", "tire_diameter": "28.0"}
]

with open("pseo_pages_list.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["slug", "target_keyword", "transmission", "rear_gear", "tire_diameter"])
    writer.writeheader()
    writer.writerows(rows)

print("Successfully generated diverse pseo_pages_list.csv data!")