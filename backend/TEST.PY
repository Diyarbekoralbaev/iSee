import requests
import base64


# Prepare the JSON payload
with open("image.jpg", "rb") as img_file:
    image_data = base64.b64encode(img_file.read()).decode("utf-8")

payload = {
    "contents": [
        {
            "parts": [
                {"text": "What is this picture?"},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_data,
                    }
                },
            ]
        }
    ]
}

# Make the API request
api_key = "AIzaSyCSxLtLUncg6qirOaW4mBt2mjcjLUP5aUM"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=payload)

# Check the response for the "text" field
response_data = response.json()
candidates = response_data.get("candidates", [])
if candidates:
    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    text_result = [part.get("text", "") for part in parts]
    generated_text = " ".join(text_result)
