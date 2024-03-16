from scripts.audio_processing import AudioProcessor
from scripts.gui import GUI
from scripts.plotting import Plotter

class Main:
    def __init__(self):
        """
        Inicializa os modulos de gui, plot e processamento de audio
        """
        self.audio_processor = AudioProcessor()
        self.gui = GUI()
        self.plotter = Plotter()

    def run(self):
        arquivo_audio = self.gui.escolher_arquivo()

        if arquivo_audio:
            destino_csv = self.gui.escolher_destino()
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
