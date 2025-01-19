import deepl
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")  # Replace with your key
translator = deepl.Translator(auth_key)

result = translator.translate_text("I love coding!", target_lang="FR")
print(result.text)  # "Bonjour, le monde !"
