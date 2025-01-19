from vosk import Model, KaldiRecognizer
import wave
import json


def transcribe_audio(file_path):
    wf = wave.open(file_path, "rb")
    # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    #     raise ValueError("Audio file must be WAV format mono PCM.")

    model = Model(lang="en-us")
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            results.append(result)

    final_result = json.loads(rec.FinalResult())
    results.append(final_result)

    return results


# Example usage
file_path = "audio_files/quickbrownfox.wav"
transcription_results = transcribe_audio(file_path)
for result in transcription_results:
    print(result)
