import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def generate_mel_spectrogram(wav_filepath, output_image_path, sr=22050, n_mels=128, fmax=8000):
    """
    Generate and save a mel spectrogram from a WAV file.
    
    Parameters:
    - wav_filepath (str): Path to the input WAV file.
    - output_image_path (str): Path to save the output image of the spectrogram.
    - sr (int): Sample rate for loading the WAV file.
    - n_mels (int): Number of Mel bands to generate.
    - fmax (float): Maximum frequency for the spectrogram.
    """
    # Load the audio file
    y, sr = librosa.load(wav_filepath, sr=sr)
    
    # Create a Mel spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=fmax)
    S_dB = librosa.power_to_db(S, ref=np.max)  # Convert to decibels
    
    # Plot and save the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=fmax, cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    plt.savefig(output_image_path)
    plt.close()

# Example usage
wav_filepath = 'gen_audio.wav'  # Replace with your WAV file path
output_image_path = 'gen_spectro.png'  # Path to save the output image
generate_mel_spectrogram(wav_filepath, output_image_path)
