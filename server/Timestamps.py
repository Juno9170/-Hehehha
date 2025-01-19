import os
import whisper_timestamped as whisper
from allosaurus.app import read_recognizer
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import deepl
from flask_cors import CORS
from io import BytesIO
from stt import Lango

from word import Word

load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
whisper_model = whisper.load_model("tiny", device="cpu")
allosaurus_model = read_recognizer("eng2102")
lango = Lango(whisper_model, allosaurus_model)

app = Flask(__name__)

CORS(app, origins="*")


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Timestamps API"


@app.route('/transcribe', methods=['POST'])
def timestamp_transcription():
    words = []
    temp = BytesIO(request.files['audio'].read())
    words = lango.timestamp_transcription(temp)

    return words


@app.route('/translate', methods=['POST'])
def translateText():
    data = request.get_json()
    body = data.get('body', '')
    print(body)
    print(f"Received text: {body['prompt']}")
    print(f"Received text: {body['language']}")
    result = translator.translate_text(
        body["prompt"], target_lang=body['language'].upper())

    return jsonify({"translatedText": result.text})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
