import aiohttp
import base64
import json

class GoogleTranslator:
    def __init__(self, source='auto', target='en'):
        self.source = source
        self.target = target
        self.base_url = "https://translate.googleapis.com/translate_a/single"

    async def translate(self, text):
        params = {
            'client': 'gtx',
            'sl': self.source,
            'tl': self.target,
            'dt': 't',
            'q': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status != 200:
                    raise Exception("Error in translation request")
                data = await response.json()
                translated_text = ''.join([item[0] for item in data[0]])
                return translated_text




# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyCSxLtLUncg6qirOaW4mBt2mjcjLUP5aUM'


async def generate_image_description(image_path, prompt, lang='en'):
    try:
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
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
            api_key = "AIzaSyCSxLtLUncg6qirOaW4mBt2mjcjLUP5aUM"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    response_data = await response.json()

                    candidates = response_data.get("candidates", [])
                    if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        text_result = [part.get("text", "") for part in parts]
                        generated_text = " ".join(text_result)

                        if lang != 'en':
                            translator = await GoogleTranslator(
                                source="en", target=lang).translate(str(generated_text))
                            return translator
                        else:
                            return generated_text
                    else:
                        return response_data

    except Exception as e:
        print(str(e))
        return "An error occurred while generating the description."


with open ('key.txt', 'r') as f:
    API_KEY = f.read()


async def text_to_speech(text):
    url = 'https://mohir.ai/api/v1/tts'
    headers = {
        'Authorization': f"{API_KEY}",  # Replace [API_KEY] with your actual API key
        'Content-Type': 'application/json',
    }
    data = {
        "text": text,
        "model": "davron",
        "mood": "neutral",
        "blocking": "true",
        "webhook_notifaication_url": "https://example.com/webhook",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            response_data = await response.json()
            return response_data