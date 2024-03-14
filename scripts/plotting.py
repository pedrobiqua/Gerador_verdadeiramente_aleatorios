import matplotlib.pyplot as plt
import seaborn as sns
import librosa

class Plotter:
    def __init__(self):
        pass

    def mostrar_grafico(self, y, sr, limiar, nome_arquivo="plot"):
        tempo = librosa.times_like(y, sr=sr)
        plt.figure(figsize=(12, 6))
        plt.plot(tempo, y, color='b')
        plt.title('Coleta dos dados decaimento')
        plt.axhline(y=limiar, color='g', linestyle='--', label=f'Limiar = {limiar:.3f}')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        nome_arquivo = nome_arquivo + "_" + str(limiar) + ".png"
        plt.savefig(nome_arquivo)
