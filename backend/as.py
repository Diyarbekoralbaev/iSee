import langid
import re

def detect_and_store_language(text):
    sentences = re.split(r'[.!?]', text)

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            detected_language, _ = langid.classify(sentence)

            if detected_language == 'ru':
                print("Detected Russian Sentence:", sentence)
                # Handle Russian text accordingly
            elif detected_language == 'en':
                print("Detected English Sentence:", sentence)
                # Handle English text accordingly
            elif detected_language == 'uz':
                print("Detected Uzbek Sentence:", sentence)
                # Handle Uzbek text accordingly
            else:
                # Default to a specific language or consider it as mixed-language
                print("Uncertain language or mixed-language sentence:", sentence)

# Example usage:
mixed_text = "Привет! This is a mixed text. Salom! Как дела? What's up?"
detect_and_store_language(mixed_text)
