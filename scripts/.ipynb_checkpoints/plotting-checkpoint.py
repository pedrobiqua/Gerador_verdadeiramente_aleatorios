import matplotlib.pyplot as plt
# import seaborn as sns
import librosa
import os

class Plotter:
    """
    Classe responsavel pela plotagem de graficos
    """
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

        # Diretório para salvar a imagem
        diretorio_imagens = os.path.join(os.path.dirname(__file__), "..", "imgs", "image_results")

        # Verifica se o diretório existe e, se não existir, cria
        if not os.path.exists(diretorio_imagens):
            os.makedirs(diretorio_imagens)
        
        nome_arquivo = nome_arquivo + "_" + str(limiar) + ".png"
        caminho_arquivo = os.path.join(diretorio_imagens, nome_arquivo)

        plt.savefig(caminho_arquivo)
