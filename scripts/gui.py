import tkinter as tk
from tkinter import filedialog

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def escolher_arquivo(self):
        arquivo = filedialog.askopenfilename(title="Escolha o arquivo de áudio", filetypes=[("Arquivos de áudio", "*.mp4")])
        return arquivo

    def escolher_destino(self):
        destino = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")], title="Escolha o destino para salvar o arquivo CSV")
        return destino
