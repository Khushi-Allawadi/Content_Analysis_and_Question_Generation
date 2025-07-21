import openai
import json
import base64
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

with open("structured_questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ai_questions = []

for item in data:
    question_img_path = item["images"]
    base64_image = encode_image(question_img_path)

    prompt = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Generate a multiple choice question based on this image:"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ]
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[prompt],
            max_tokens=300
        )
        generated_q = response["choices"][0]["message"]["content"]
    except Exception as e:
        generated_q = f"Error: {e}"

    ai_questions.append({
        "original_image": question_img_path,
        "ai_generated_question": generated_q
    })

with open("ai_generated_questions.json", "w", encoding="utf-8") as f:
    json.dump(ai_questions, f, indent=2)

print("AI-generated questions saved to ai_generated_questions.json")
