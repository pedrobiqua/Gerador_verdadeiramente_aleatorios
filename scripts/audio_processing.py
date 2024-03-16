import numpy as np
import pandas as pd
import librosa
import csv
from findpeaks import findpeaks
from scripts.plotting import Plotter

class AudioProcessor:
    """
    Classe responsavel pela processamento dos dados coletados atraves do audio
    """
    def __init__(self):
        self.plotter = Plotter()

    def audio_para_onda_retangular(self, audio_path, multiple=0.1):
        y, sr = librosa.load(audio_path, sr=None)
        # Ao inves de usar limiar utilizar o find peaks do scipy.
        # Para encontrar os picos vamos utilizar esse lib findpeaks
        #================================================
        # o arquivo de som já está em binário!
        #================================================
        del_t = 100
        fp = findpeaks(lookahead=int(del_t))
        results = fp.fit(y)
        # plot = fp.plot() Bug com Gdk, vou ter que testar isso em um caderno

        array_peaks = results['df']['peak'].astype(int).values
        print(array_peaks)
        print("\n")
        
        # limiar = np.mean(np.abs(y)) * multiple
        # onda_retangular = (y > limiar).astype(float)

        # self.plotter.mostrar_grafico(y, sr, limiar)

        return array_peaks

    def salvar_onda_retangular_csv(self, onda_retangular, output_path='onda_retangular.csv'):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amplitude'])
            for amplitude in onda_retangular:
                writer.writerow([amplitude])
