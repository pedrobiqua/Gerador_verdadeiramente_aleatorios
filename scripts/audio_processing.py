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
#============================================================
    def __remove_noise(self, y, multiple):
        limiar = np.mean(np.abs(y)) * multiple
        print(f"Limiar{limiar}")
        indices = np.where(y < limiar)[0]
        y = np.delete(y, indices)
        print(len(y))
        return y

    def __separar_em_caixas(self, y, del_t):
        
        conj_dados = [y[i:i+del_t] for i in range(0, len(i), del_t)]
        dados = []
        for array in conj_dados:
            fp = findpeaks(lookahead=1)
            results = fp.fit(y)
            tem_picos = (results['peak'] == 0).all()
            if(tem_picos):
                dados.append(0)
            else:
                dados.append(1)

        return dados
        

    def audio_para_onda_retangular(self, audio_path, multiple=0.1):
        # Carrega os dados do audio.
        y, sr = librosa.load(audio_path, sr=None)

        # Utilizar o limiar para remover os ruidos
        y = self.__remove_noise(y, multiple)

        # Separa em caixas onde serão detectados os picos
        del_t = 100
        __separar_em_caixas(y, del_t)

        #===========================
        """
        del_t = len(y)//300
        fp = findpeaks(lookahead=int(del_t))
        results = fp.fit(y)
        plot = fp.plot()
        """
        #===========================

        array_peaks = results['df']['peak'].astype(int).values

        # Variavel para debug do código, para ativar usar a função enable_debug()
        if self._debug:
            print(results)
            print("\n")
            print(array_peaks)
            print("\n")

        return array_peaks

    def salvar_onda_retangular_csv(self, onda_retangular, output_path='onda_retangular.csv'):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amplitude'])
            for amplitude in onda_retangular:
                writer.writerow([amplitude])
