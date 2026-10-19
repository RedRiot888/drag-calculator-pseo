import csv

# Define our parameter lists for high-value drag racing search terms
transmissions = [
    {"code": "powerglide", "name": "Powerglide (2-Speed)", "gear1": 1.76},
    {"code": "th400", "name": "TH400 (3-Speed)", "gear1": 2.48},
    {"code": "t56", "name": "T56 Manual (6-Speed)", "gear1": 2.66},
    {"code": "zf8hp", "name": "ZF 8HP (8-Speed)", "gear1": 4.71}
]

gear_ratios = [3.08, 3.23, 3.42, 3.55, 3.73, 3.90, 4.10, 4.30, 4.56, 4.88, 5.13]
tire_diameters = [26.0, 28.0, 29.5, 31.0, 33.0]

# Generate all pSEO combinations
rows = []
for trans in transmissions:
    for gear in gear_ratios:
        for tire in tire_diameters:
            slug = f"{trans['code']}-{gear}-gear-{tire}-tire"
            keyword = f"{trans['name']} {gear} gear {tire} inch tire drag calculator"
            url = f"/?trans={trans['code']}&gear={gear}&tire={tire}"
            rows.append({
                "slug": slug,
                "target_keyword": keyword,
                "transmission": trans['name'],
                "rear_gear": gear,
                "tire_diameter": tire,
                "page_url": url
            })

# Save to a CSV file
filename = "pseo_pages_list.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["slug", "target_keyword", "transmission", "rear_gear", "tire_diameter", "page_url"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {len(rows)} target pages in {filename}!")