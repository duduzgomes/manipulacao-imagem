import cv2 
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def selecionar_imagem():
    root = tk.Tk()
    root.withdraw()
    caminho_do_arquivo = tk.filedialog.askopenfilename()
    return caminho_do_arquivo

def selecionar_caminho_de_salvamento():
    root = tk.Tk()
    root.withdraw()
    caminho_de_salvamento = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivo xlsx", "*.xlsx"), ("Todos os arquivos", "*.*")])
    return caminho_de_salvamento

caminho_imagem = selecionar_imagem()

imagem = cv2.imread(caminho_imagem)

if imagem is None:
    print("Não foi possivel  carregar a imagem")

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

df = pd.DataFrame(imagem_cinza)

caminho_arquivo = selecionar_caminho_de_salvamento()

df.to_excel(caminho_arquivo, index=False)