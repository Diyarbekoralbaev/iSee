import google.generativeai as genai
import PIL.Image
import aiohttp

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

genai.configure(api_key=GOOGLE_API_KEY)


async def generate_image_description(image_path, prompt, lang='en'):
    try:
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([prompt, img], stream=True)
        response.resolve()
        if lang != 'en':
            translator = await GoogleTranslator(
                    source="en", target=lang).translate(str(response.text))
            return translator
        else:
            return response.text    

    except Exception as e:
        print(str(e))
        return "An error occurred while generating the description."
    

async def chat_with_image(image_path, prompt, lang='en'):
    try:
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([prompt, img], stream=True)
        response.resolve()
        if lang != 'en':
            translator = await GoogleTranslator(
                    source="en", target=lang).translate(str(response.text))
            return translator
        else:
            return response.text    

    except Exception as e:
        print(str(e))
        return "An error occurred while generating the description."

        
