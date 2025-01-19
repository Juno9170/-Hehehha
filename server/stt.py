import whisper_timestamped as whisper
from allosaurus.app import read_recognizer
from pydub import AudioSegment

from objects.phoneme import Phoneme
from objects.word import Word


class Lango:
    def __init__(self, whisper_model, allosaurus_model):
        self.whisper_model = whisper_model
        self.allosaurus_model = allosaurus_model

    def get_results(self, audio_file):
        res = self.recognize(audio_file)
        words = self.timestamp_transcription(audio_file)
        phonemes = self.audio_to_phonemes(audio_file)
        word_phoneme_map = self.map_phonemes_to_words(words, phonemes)

        print(' '.join([w.text for w, ps in word_phoneme_map]))
        print(''.join([''.join([p.phoneme for p in ps])
              for w, ps in word_phoneme_map]))
        for w, ps in res:
            print(w)

        return res, word_phoneme_map

    def recognize(self, audio_file):
        res = self.allosaurus_model.recognize(
            audio_file, topk=5, timestamp=True)
        return res

    def timestamp_transcription(self, bytes):
        words = []

        audio = whisper.load_audio(bytes)
        result = whisper.transcribe(self.whisper_model, audio, language="en")

        for w in result["segments"][0]["words"]:
            word = Word(w["text"], w["start"], w["end"], w["confidence"])
            words.append(word)

        return words

    def process_words_in_audio(self, audio_file, word_timestamps):
        out = []
        audio = AudioSegment.from_file(audio_file)

        for i, (start_time, end_time) in enumerate(word_timestamps):

            # need to convert s -> ms
            start_ms = start_time * 1000
            end_ms = end_time * 1000

            word_audio = audio[start_ms:end_ms]

            # process audio
            res = self.model.recognize(word_audio)
            out.append(res.replace(" ", ""))

        return out

    def speech_to_text(self, ipa_transcription, word_timestamps):
        out = []

        for i, (start_time, end_time) in enumerate(word_timestamps):
            word = ipa_transcription[i]
            out.append(word)

        return out

    def audio_to_phonemes(self, audio_file):
        phonemes = []
        # get model's IPA output
        ipa_transcription = self.allosaurus_model.recognize(
            audio_file, timestamp=True)

        print("ipa_transcription:", ipa_transcription.split("\n"))

        for t in ipa_transcription.split("\n"):
            # print("ipa:", repr(t))
            # if len(t) != 3:  # Ensure the line has exactly 3 parts
            #     print(f"Skipping invalid line...")  # Optional debug statement
            #     continue
            start, duration, phoneme = t.split(" ")
            start = float(start)
            duration = float(duration)
            end = start + duration
            # add phoneme to table
            phonemes.append(Phoneme(start, end, phoneme))

        return phonemes

    def map_phonemes_to_words(self, words, phonemes):

        out = []

        p = 0

        for w in words:
            mapped_phonemes = []

            # stop when start of phoneme is after end of word
            while (p < len(phonemes)) and (phonemes[p].start) <= w.end:

                # if phoneme times are within word times, append to out
                if (phonemes[p].start >= w.start) and (phonemes[p].end <= w.end):
                    mapped_phonemes.append(phonemes[p])
                p += 1

            out.append((w, mapped_phonemes))

        return out


if __name__ == "__main__":

    whisper_model = whisper.load_model("tiny", device="cpu")
    allosaurus_model = read_recognizer("eng2102")

    lango = Lango(whisper_model, allosaurus_model)

    audio_file = "testingNOW.wav"
    # audio_file = "test_audio_files/quickbrownfox.wav"
    # audio_file = f"audio_files/{audio_file}.wav"

    # res, word_phoneme_map = lango.get_results(audio_file)

    phonemes = lango.audio_to_phonemes(audio_file)
    words = lango.timestamp_transcription(audio_file)
    res = lango.map_phonemes_to_words(words, phonemes)

    print(' '.join([w.text for w, ps in res]))

    print(''.join([''.join([p.phoneme for p in ps]) for w, ps in res]))

    for w, ps in res:
        print(w)
