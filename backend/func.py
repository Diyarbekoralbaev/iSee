import google.generativeai as genai
import PIL.Image
from translatorr import GoogleTranslator


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
