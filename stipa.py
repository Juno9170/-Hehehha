from allosaurus.app import read_recognizer

model = read_recognizer()
# model = read_recognizer("eng2102")

audio_file = "quickbrownfox"
audio_file = f"audio_files/{audio_file}.wav"

res = model.recognize(audio_file, topk=5, timestamp=True)
# res = model.recognize(audio_file)
print(res)

# with open('test.txt', 'w', encoding='utf-8') as output_file:
#     output_file.write(res)

# TODO: take .wav file as input and output STT
