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
        self._debug = False
        self.plotter = Plotter()

    def enable_debug(self):
        self._debug = True

    def disable_debug(self):
        self._debug = False

    def audio_para_onda_retangular(self, audio_path, multiple=0.1):
        y, sr = librosa.load(audio_path, sr=None)
        # Ao inves de usar limiar utilizar o find peaks do scipy.
        # Para encontrar os picos vamos utilizar esse lib findpeaks que já utiliza o scipy

        """
        Perguntas de pesquisa:
            1- Eu não consigo estimar um contante de del_t pois os picos são aleatórios, 
                ou seja não é possivel encontrar um intervalo plausivel para esse problema.
            2- Tenho uma proposta, utilizar o metodo anterior de limiar para remover os 
                ruidos montando um novo conjunto de dados e assim rodar o detector de picos.
        """
        del_t = 10000
        # fp = findpeaks(method='caerus', params={'minperc':5, 'window':50}) # Essa opção não ficou legal
        fp = findpeaks(lookahead=int(del_t))
        results = fp.fit(y)
        plot = fp.plot() #Bug com Gdk, vou ter que testar isso em um caderno

        array_peaks = results['df']['peak'].astype(int).values

        # Variavel para debug do código, para ativar usar a função enable_debug()
        if self._debug:
            print(results)
            print("\n")
            print(array_peaks)
            print("\n")

        #========================================#
        # Metodo anterior
        # limiar = np.mean(np.abs(y)) * multiple
        # onda_retangular = (y > limiar).astype(float)
        #========================================#
        # self.plotter.mostrar_grafico(y, sr, limiar)

        return array_peaks

    def salvar_onda_retangular_csv(self, onda_retangular, output_path='onda_retangular.csv'):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amplitude'])
            for amplitude in onda_retangular:
                writer.writerow([amplitude])
