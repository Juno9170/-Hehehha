from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
)

def speechTimestamps(filepath):
    """
    This function takes the file path of an audio file, transcribes it using Whisper,
    and returns the word-level timestamps in JSON format.

    Args:
        filepath (str): Path to the audio file (e.g., .mp3, .wav)

    Returns:
        dict: A JSON object containing the word-level timestamps
    """
    # Open the audio file
    with open(filepath, "rb") as audio_file:
        # Create the transcription request
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )

    # Return transcription's word-level timestamps as JSON
    return transcription.words

# Example usage
if __name__ == "__main__":
    audio_file = "quickbrownfox.wav"
    timestamps = speechTimestamps(audio_file)
    print(timestamps)