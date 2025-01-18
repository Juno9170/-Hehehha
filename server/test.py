from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
import torch

# Load the processor and model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-robust-ft-swbd-300h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-robust-ft-swbd-300h")

# Load your WAV file
file_path = "Cat.wav"  # Replace with your WAV file path
waveform, sample_rate = torchaudio.load(file_path)

# Resample if the sample rate is not 16kHz
if sample_rate != 16000:
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
    waveform = resampler(waveform)
    sample_rate = 16000

# Ensure waveform is mono
if waveform.shape[0] > 1:
    waveform = torch.mean(waveform, dim=0).unsqueeze(0)

# Process audio and get logits
inputs = processor(waveform, sampling_rate=sample_rate, return_tensors="pt", padding=True)
logits = model(**inputs).logits

# Decode the logits to get phonemes
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)

# Print the phoneme transcription
print("Phoneme Transcription:", transcription[0])
