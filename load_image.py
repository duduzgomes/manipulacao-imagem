
import cv2
import openpyxl
import numpy as np
import tkinter as tk
from tkinter import filedialog


def hex_para_RGB(linha):
    linhaRGB = []
    for cores in linha:
        cores = cores.replace("#", "")
        sublistas = [cores[i : i + 2] for i in range(0, len(cores), 2)]
        R = int(sublistas[0], 16)
        G = int(sublistas[1], 16)
        B = int(sublistas[2], 16)
        linhaRGB.append([B, G, R])
    return linhaRGB


def selecionar_imagem():
    root = tk.Tk()
    root.withdraw()
    caminho_do_arquivo = tk.filedialog.askopenfilename()
    return caminho_do_arquivo


def selecionar_caminho_de_salvamento():
    root = tk.Tk()
    root.withdraw()
    caminho_de_salvamento = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("Imagem JPG", "*.jpg"), ("Todos os arquivos", "*.*")],
    )
    return caminho_de_salvamento


caminho_imagem = selecionar_imagem()

workbook = openpyxl.load_workbook(caminho_imagem)
sheet = workbook.active

matriz_imagem = []
for linha in sheet.iter_rows(values_only=True):
    linha = hex_para_RGB(linha)
    if list(linha) == None:
        print("entrei")
    matriz_imagem.append(list(linha))

matriz_imagem = np.array(matriz_imagem, dtype=np.uint8)

caminho_salvo = selecionar_caminho_de_salvamento()
cv2.imwrite(caminho_salvo, matriz_imagem)