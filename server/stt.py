import whisper_timestamped as whisper
import os
from dotenv import load_dotenv
import eng_to_ipa as ipa
from allosaurus.app import read_recognizer
from pydub import AudioSegment

from phoneme import Phoneme
from word import Word


class Lango:
    def __init__(self, whisper_model, allosaurus_model, time_shift=0.0):
        self.whisper_model = whisper_model
        self.allosaurus_model = allosaurus_model
        self.time_shift = time_shift

    def recognize(self, audio_file):
        res = self.allosaurus_model.recognize(
            audio_file, topk=5, timestamp=True)
        return res

    def timestamp_transcription(self, filepath):
        words = []

        audio = whisper.load_audio(filepath)
        result = whisper.transcribe(self.whisper_model, audio, language="en")

        for i, w in enumerate(result["segments"][0]["words"]):
            word = Word(w["text"], w["start"], w["end"], w["confidence"])
            # shift the start time up by the time_shift except for the first word
            word.start += self.time_shift  # if i > 0 else 0
            # shift the end time down by the time_shift except for the last word
            word.end += self.time_shift if i < len(
                result["segments"][0]["words"]) - 1 else 0
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

        for t in ipa_transcription.split("\n"):
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
                # if the phoneme is on the boundary, assign it to the word that starts first
                # so really we just check if p starts before w ends
                if (phonemes[p].start >= w.start):
                    mapped_phonemes.append(phonemes[p])
                p += 1

            out.append((w, mapped_phonemes))

        return out

    def to_ipa(self, text):
        return ipa.convert(text)


if __name__ == "__main__":

    whisper_model = whisper.load_model("tiny", device="cpu")
    allosaurus_model = read_recognizer("eng2102")

    lango = Lango(whisper_model, allosaurus_model, time_shift=0.0)

    audio_file = "quickbrownfoxSLOW"
    audio_file = f"audio_files/{audio_file}.wav"

    phonemes = lango.audio_to_phonemes(audio_file)
    words = lango.timestamp_transcription(audio_file)
    res = lango.map_phonemes_to_words(words, phonemes)

    # print(' '.join([w.text for w, ps in res]))

    # print(' '.join([''.join([p.phoneme for p in ps]) for _, ps in res]))

    for w, ps in res:
        # print(f"{w} | {[p for p in ps]}")
        print(f"{w.text:10} | {''.join([p.phoneme for p in ps])}")
