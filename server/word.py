class Word:

    def __init__(self, text, start, end, confidence):
        self.text = text
        self.start = start
        self.end = end
        self.confidence = confidence

    def __repr__(self):
        return f"WORD | {self.text} | {self.start} -> {self.end} | confidence={self.confidence:.4f}"
