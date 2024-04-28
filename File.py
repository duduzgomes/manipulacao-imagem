import tkinter as tk
from tkinter import filedialog

class File:
    def __init__(self):
        pass

    def abrirArquivo():
        root = tk.Tk()
        root.withdraw()
        caminho_do_arquivo = filedialog.askopenfilename()
        return caminho_do_arquivo

    def salvarArquivo():
        root = tk.Tk()
        root.withdraw()
        caminho_de_salvamento = filedialog.asksaveasfilename(defaultextension=".xlsx", 
            filetypes=[("Arquivo xlsx", "*.xlsx"), ("Imagem JPG", "*.jpg"), ("Todos os arquivos", "*.*")])
        return caminho_de_salvamento
    