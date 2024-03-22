from scripts.audio_processing import AudioProcessor
from scripts.gui import GUI
from scripts.plotting import Plotter
from pathlib import Path

class Main:
    def __init__(self):
        """
        Inicializa os modulos de gui, plot e processamento de audio
        """
        self.audio_processor = AudioProcessor()
        self.gui = GUI()
        self.plotter = Plotter()

    def run(self):
        # Obtém o diretório atual do script
        arquivo_audio = self.gui.escolher_arquivo()
        # current_dir = Path(__file__).resolve().parent
        # arquivo_audio = current_dir/"data"/"Audio-teste-07-12-23-B.mp4"

        if arquivo_audio:
            destino_csv = self.gui.escolher_destino()
            # destino_csv = current_dir/"results"/"results_teste.csv"
            if destino_csv:
                onda_retangular = self.audio_processor.audio_para_onda_retangular(arquivo_audio, multiple=0.5)
                self.audio_processor.salvar_onda_retangular_csv(onda_retangular, output_path=destino_csv)
                print(f"Arquivo CSV salvo em: {destino_csv}")
            else:
                print("Nenhum destino selecionado. Operação cancelada.")
        else:
            print("Nenhum arquivo de áudio selecionado. Operação cancelada.")

if __name__ == "__main__":
    main_app = Main()
    main_app.run()
