import numpy as np
import librosa
import csv

class AudioProcessor:
    def __init__(self):
        pass

    def audio_para_onda_retangular(self, audio_path, multiple=0.1):
        y, sr = librosa.load(audio_path, sr=None)
        # Ao inves de usar limiar utilizar o find peaks do scipy.
        limiar = np.mean(np.abs(y)) * multiple
        onda_retangular = (y > limiar).astype(float)
        return onda_retangular

    def salvar_onda_retangular_csv(self, onda_retangular, output_path='onda_retangular.csv'):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amplitude'])
            for amplitude in onda_retangular:
                writer.writerow([amplitude])
