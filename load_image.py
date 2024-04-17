import cv2
import openpyxl
import numpy as np
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
    caminho_de_salvamento = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Imagem JPG", "*.jpg"), ("Todos os arquivos", "*.*")])
    return caminho_de_salvamento

caminho_imagem = selecionar_imagem()

workbook = openpyxl.load_workbook(caminho_imagem)
sheet = workbook.active

matriz_imagem = []
for linha in sheet.iter_rows(values_only=True):
    matriz_imagem.append(list(linha))

matriz_imagem = np.array(matriz_imagem, dtype=np.uint8)

caminho_salvo = selecionar_caminho_de_salvamento()
cv2.imwrite(caminho_salvo, matriz_imagem)

