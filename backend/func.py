import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyCSxLtLUncg6qirOaW4mBt2mjcjLUP5aUM'

genai.configure(api_key=GOOGLE_API_KEY)


def generate_image_description(image_path, prompt="describe this image in 15 words"):
    img = PIL.Image.open(image_path)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    return response.text
