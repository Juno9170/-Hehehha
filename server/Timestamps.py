from datetime import datetime
from flask_socketio import SocketIO, emit
from flask import send_from_directory
import os
import whisper_timestamped as whisper
from allosaurus.app import read_recognizer
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import deepl
from flask_cors import CORS
from io import BytesIO
from openai import OpenAI

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
socketio = SocketIO(app, cors_allowed_origins="*")


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


@socketio.on("audio_data")
def handle_audio(data):
    # audio_file = data["audio"]
    try:
        print(type(data))
        # Wrap the file content in a BytesIO object
        audio_bytes_io = BytesIO(data)
        print(type(audio_bytes_io))

        # Prepare the tuple (filename, file-like object, content_type)
        file_tuple = ("audio.wav", audio_bytes_io, "audio/wav")

        # Pass the tuple to the transcription API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=file_tuple, response_format="verbose_json",
        )

        print(f"Text: {transcription.text}")
        emit("transcription", {"text": transcription.text})

        response = get_response(transcription.text)
        emit("response", {"text": response})

        audio_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        audio_url = synthesize_audio(response, audio_filename)
        emit("audio_url", {"url": audio_url})

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
