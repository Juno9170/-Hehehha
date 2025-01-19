import whisper_timestamped as whisper
import json

audio = whisper.load_audio("quickbrownfox.wav")

model = whisper.load_model("tiny", device="cpu")

result = whisper.transcribe(model, audio, language="en")

print(json.dumps(result, indent=2, ensure_ascii=False))
