class Phoneme:

    def __init__(self, start, end, phoneme):
        self.start = start
        self.end = end
        self.phoneme = phoneme

    def __repr__(self):
        return f"PHON | {self.phoneme} | {self.start:.4f} -> {self.end:.4f}"
