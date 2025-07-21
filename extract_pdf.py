import fitz
import os
import json

# === Setup ===
pdf_path = "IMO Grade 1 - 1-2.pdf"
output_folder = "extracted_images"
os.makedirs(output_folder, exist_ok=True)

# === Open PDF ===
doc = fitz.open(pdf_path)
extracted_data = []

# === Loop through each page ===
for page_num, page in enumerate(doc, start=1):
    print(f"Processing page {page_num}")
    
    page_text = page.get_text()
    page_images = []

    # Extract images
    images = page.get_images(full=True)
    for img_index, img in enumerate(images, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"page{page_num}_image{img_index}.{image_ext}"
        image_path = os.path.join(output_folder, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        page_images.append(image_path)

    # Save text + image paths
    extracted_data.append({
        "page": page_num,
        "text": page_text.strip(),
        "images": page_images
    })

# === Save to JSON ===
with open("pdf_content.json", "w", encoding="utf-8") as json_file:
    json.dump(extracted_data, json_file, indent=2, ensure_ascii=False)

print("Done! Extracted data saved to pdf_content.json")
