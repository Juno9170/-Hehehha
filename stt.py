import os
from groq import Groq
from dotenv import load_dotenv
import eng_to_ipa as ipa

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

filename = "quickbrownfox"

filepath = os.path.dirname(__file__) + f"/audio_files/{filename}.wav"

with open(filepath, "rb") as file:
    # create transcription
    transcription = client.audio.transcriptions.create(
        file=(filepath, file.read()),
        model="whisper-large-v3",
        prompt="Return timestamps of words",
        response_format="json",
        temperature=0.0
    )

    text = transcription.text.strip()

    print(ipa.convert(text))

# can we use STT on the user's input to get the timestamps we need to split the audio at?
