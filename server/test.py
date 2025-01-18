from allosaurus.app import read_recognizer

# load your model
model = read_recognizer()

# run inference -> æ l u s ɔ ɹ s
print(model.recognize('Cat.wav'))