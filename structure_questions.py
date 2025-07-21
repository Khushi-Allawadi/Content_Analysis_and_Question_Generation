import json

# Load the extracted content
with open("pdf_content.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

structured_questions = []

for page in raw_data:
    text = page["text"]
    images = page["images"]

    # Basic filtering: only process pages that have both text and at least 2 images
    if text.strip() and len(images) >= 2:
        first_line = text.strip().split("\n")[0]
        
        structured_questions.append({
            "question": first_line,
            "images": images[0],           # First image = question
            "option_images": images[1:]    # Rest = options
        })

# Save to new structured file
with open("structured_questions.json", "w", encoding="utf-8") as f:
    json.dump(structured_questions, f, indent=2)

print("Structured question data saved to structured_questions.json")
