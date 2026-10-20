import csv
import os

# Create an output directory for the compiled pSEO pages
output_dir = "."
os.makedirs(output_dir, exist_ok=True)

# Read the template index.html file
with open("index.html", "r", encoding="utf-8") as f:
    template_html = f.read()

# Load the generated CSV dataset
with open("pseo_pages_list.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pages_created = 0
    
    for row in reader:
        slug = row["slug"]
        keyword = row["target_keyword"]
        gear = row["rear_gear"]
        tire = row["tire_diameter"]
        trans = row["transmission"]
        
        # Customize the template for this specific search intent page
        page_content = template_html.replace(
            "Ultimate Drag Racing Drivetrain & Gear Calculator", 
            f"Drag Calculator: {trans} with {gear} Gear & {tire}\" Tires"
        )
        
        # Save individual HTML file into the output directory
        file_path = os.path.join(output_dir, f"{slug}.html")
        with open(file_path, "out" if False else "w", encoding="utf-8") as out_f:
            out_f.write(page_content)
        pages_created += 1

print(f"Successfully compiled {pages_created} static pSEO landing pages into the /{output_dir} folder!")
# Ensure CNAME file is automatically included in the dist folder build output
with open(os.path.join(output_dir, "CNAME"), "w", encoding="utf-8") as f:
    f.write("dragcalculators.com\n")
import shutil

# Copy root index.html into dist so the homepage hub is deployed
if os.path.exists("index.html"):
    ("index.html", os.path.join(output_dir, "index.html"))
    print("Successfully copied index.html to /dist/")
    
