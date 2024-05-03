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
        self.count_1 = 0
        self.count_0 = 0

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
    
    def __is_count1_ok(self, total):
        """
        Valida se a distribuição de 1 está entre 45% e 55%
        """
        return ( ((self.count_1/total)*100) >= 45 and ((self.count_1/total)*100) <= 55 ), ((self.count_1/total)*100)
    
    def __is_count0_ok(self, total):
        """
        Valida se a distribuição de 0 está entre 45% e 55%
        """
        return ( ((self.count_0/total)*100) >= 45 and ((self.count_0/total)*100) <= 55 ), ((self.count_0/total)*100)

    def __separar_em_caixas(self, y, del_t):
        
        conj_dados = [y[i:i+del_t] for i in range(0, len(y), del_t)]
        dados = []
        total = 0
        flag = True
        look_head = int(del_t/2)

        while flag:
            for array in conj_dados:
                fp = findpeaks(lookahead=look_head, verbose=0)
                results = fp.fit(array)
                tem_picos = (results['df']['peak'] == 0).all()
                
                if(tem_picos):
                    dados.append(1)
                    # Conta a quantidade de 1
                    self.count_1 += 1
                
                else:
                    dados.append(0)
                    # Conta a quantidade de 0
                    self.count_0 += 1
                
                total += 1
            
            count_0_validate, percentual_0 = self.__is_count0_ok(total)
            count_1_validate, percentual_1 = self.__is_count1_ok(total)

            if count_0_validate or count_1_validate:
                print(f"Percentuais O: {percentual_0}  1: {percentual_1}\n")
                print("OK!")
                flag = False
            else:
                # Não foi encontrado uma boa distribuição, vamos mudar os parametros
                if look_head == del_t:
                    print("METODO LOOK HEAD NÃO FOI")
                    flag = False
                    break

                if look_head <= 0:
                    print("METODO LOOK HEAD NÃO FOI")
                    flag = False
                    break

                if percentual_1 > percentual_0:
                    look_head -= 5
                else:
                    look_head += 5
                
                print(f"Encontrando um metodo melhor!\npercentual_0: {percentual_0}, percentual_1: {percentual_1}\n")
                print(f"Lookahead: {look_head}")
                dados = []
                total = 0
                self.count_0 = 0
                self.count_1 = 0

            

        return dados
        

    def audio_para_onda_retangular(self, audio_path, multiple=0.1):
        # Carrega os dados do audio.
        y, sr = librosa.load(audio_path, sr=None)

        # Utilizar o limiar para remover os ruidos
        # y = self.__remove_noise(y, multiple)

        # Separa em caixas onde serão detectados os picos
        del_t = 100
        results = self.__separar_em_caixas(y, del_t)

        #===========================
        """
        del_t = len(y)//300
        fp = findpeaks(lookahead=int(del_t))
        results = fp.fit(y)
        plot = fp.plot()
        """
        #===========================

        # array_peaks = results['df']['peak'].astype(int).values

        # Variavel para debug do código, para ativar usar a função enable_debug()
        if self._debug:
            print(results)
            print("\n")
            # print(array_peaks)
            print("\n")

        return results

    def salvar_onda_retangular_csv(self, onda_retangular, output_path='onda_retangular.csv'):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Amplitude'])
            for amplitude in onda_retangular:
                writer.writerow([amplitude])
