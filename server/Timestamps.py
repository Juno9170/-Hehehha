from datetime import datetime
from flask_socketio import SocketIO, emit
from flask import send_from_directory
import os
import whisper_timestamped as whisper
import base64
from allosaurus.app import read_recognizer
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import deepl
from flask_cors import CORS
from io import BytesIO
from openai import OpenAI
import wave
import subprocess
from pydub import AudioSegment
from time import sleep
import eng_to_ipa as ipa

from utils import utils
from stt import Lango


load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
whisper_model = whisper.load_model("tiny", device="cpu")
allosaurus_model = read_recognizer("eng2102")
lango = Lango(whisper_model, allosaurus_model)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4321")


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


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

@socketio.on("translated_text")
def handle_translated_text(data):
    print("Received translated text")
    print(data)
    phonemes = ipa.convert(data)
    synthesize_audio(data, "gen_audio.wav")

    emit("translated_text", data, broadcast=True)


@socketio.on("audio_data")
def handle_audio(data):
    # audio_file = data["audio"]
    try:
        audio_bytes_io = BytesIO(data['arrayBuffer'])
        file_tuple = ("audio.wav", audio_bytes_io, "audio/wav")
        #
        # with open("testing.webm", "wb") as f:
        #    f.write(audio_bytes_io.getvalue())
        webm_audio = AudioSegment.from_file(
            BytesIO(audio_bytes_io.getvalue()), format="webm")
        wav_io = BytesIO()
        webm_audio.export(wav_io, format="wav")
        wav_bitstring = wav_io.getvalue()

        target = data['additionalString']

        output_file = 'test_audio_files/' + f'{target}.wav'

        print("target:", target)
        # with open(output_file, 'wb') as file:
        #     file.write(wav_bitstring)

        phonemes = lango.audio_to_phonemes(output_file)
        print(phonemes)
        words = lango.timestamp_transcription(output_file)
        print(words)
        res = lango.map_phonemes_to_words(words, phonemes)

        print(' '.join([w.text for w, ps in res]))
        print(' '.join([ipa.convert(w.text) for w, _ in res]))
        print(' '.join([''.join([p.phoneme for p in ps]) for w, ps in res]))

        diffs = [utils.levenshtein_operations(
            ''.join([p.phoneme for p in ps]), ipa.convert(w.text)) for w, ps in res]

        for d in diffs:
            print(d)

        for w, ps in res:
            print(w)

        gen_text = ' '.join([w.text for w, ps in res])
        gen_phoneme = ' '.join([''.join([p.phoneme for p in ps]) for w, ps in res])
        emit("audio_processed", {"text": gen_text, "phoneme": gen_phoneme})
    except Exception as e:
        print("An error occurred: ", str(e))


def get_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Be extremely concise.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    response = completion.choices[0].message.content
    print(response)

    return response


def synthesize_audio(text, audio_filename):
    audio = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    audio_url = os.path.join("static", "audio", audio_filename)
    audio.stream_to_file(audio_url)
    print(type(audio), audio)

    return audio_url


@socketio.on("connect")
def test_connect():
    print("Client connected.")


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected.")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
