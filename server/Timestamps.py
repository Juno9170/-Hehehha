from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import deepl
from flask_cors import CORS
from io import BytesIO

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
auth_key = os.getenv("DEEPL_API_KEY")  # Replace with your key
translator = deepl.Translator(auth_key)
app = Flask(__name__)

CORS(app, origins="*")


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Timestamps API"


@app.route('/transcribe', methods=['POST'])
def speechTimestamps():

    # 'file' should match the field name in FormData
    file = request.files['file']
    print(file.content_type)
    file_bytes = BytesIO(file.read())

    print(file.filename)

    transcription = client.audio.transcriptions.create(
        file=file_bytes,  # Pass the binary content of the MP3 file
        model="whisper-1",
        response_format="verbose_json",
    )

    print(transcription.words)
    output = []
    for word in transcription.words:
        temp = {}
        temp["word"] = word.word
        temp["start"] = word.start
        temp["end"] = word.end
        output.append(temp)

    return output  # Return transcription words


@app.route('/translate', methods=['POST'])
def translateText():
    # Get the incoming JSON data
    data = request.get_json()
    # Extract the 'body' key value (the text to translate)
    body = data.get('body', '')
    print(body)
    print(f"Received text: {body['prompt']}")
    print(f"Received text: {body['language']}")
    # Translate the text (example: to French)
    result = translator.translate_text(
        body["prompt"], target_lang=body['language'].upper())

    # Return the translated text as a JSON response
    return jsonify({"translatedText": result.text})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
