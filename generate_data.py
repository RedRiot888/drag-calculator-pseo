import csv

pages = [
    {
        "slug": "transmission-gear-drop-calculator",
        "target_keyword": "Transmission Shift Recovery & Gear Drop Calculator",
        "category": "Transmission",
        "trans": "Powerglide (2-Speed)",
        "gear": "3.73",
        "tire": "28.0"
    },
    {
        "slug": "turbo-sizing-boost-matrix",
        "target_keyword": "Turbo Sizing, Compressor Map & Boost Calculator",
        "category": "Turbo",
        "trans": "TH400 (3-Speed)",
        "gear": "3.55",
        "tire": "28.0"
    },
    {
        "slug": "supercharger-pulley-boost-calculator",
        "target_keyword": "Supercharger Pulley Ratio & Boost Pressure Calculator",
        "category": "Supercharger",
        "trans": "TH400 (3-Speed)",
        "gear": "3.42",
        "tire": "28.0"
    },
    {
        "slug": "rear-gear-ratio-calculator",
        "target_keyword": "Ring and Pinion Rear Gear Quarter-Mile Calculator",
        "category": "RearGear",
        "trans": "Powerglide (2-Speed)",
        "gear": "4.56",
        "tire": "32.0"
    },
    {
        "slug": "tire-diameter-growth-calculator",
        "target_keyword": "Tire Diameter Growth & Rollout Drag Calculator",
        "category": "Tire",
        "trans": "4L80e (Overdrive)",
        "gear": "4.10",
        "tire": "33.0"
    }
]

with open("pseo_pages_list.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["slug", "target_keyword", "category", "transmission", "rear_gear", "tire_diameter"])
    writer.writeheader()
    for p in pages:
        writer.writerow({
            "slug": p["slug"],
            "target_keyword": p["target_keyword"],
            "category": p["category"],
            "transmission": p["trans"],
            "rear_gear": p["gear"],
            "tire_diameter": p["tire"]
        })

print("Successfully updated pseo_pages_list.csv with clean category mapping!")