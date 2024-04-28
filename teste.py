import cv2 
import pandas as pd
import openpyxl
import numpy as np
from File import File
from collections import deque

class Imagem:
    def __init__(self):
        self.imagem = None
        self.linhas = None
        self.colunas = None
        self.corSelecionada = None
        self.fila = []

    def carregarImagem(self):
        caminho_do_arquivo = File.abrirArquivo()
        self.imagem = cv2.imread(caminho_do_arquivo, 1)
        self.altura = self.imagem.shape[0]
        self.largura = self.imagem.shape[1]
        self.canal = self.imagem.shape[2]

    def selecionarCor(self):
        print("Digite uma com cor:")
        r = int(input("R:"))

        g = int(input("G:"))
        b = int(input("B:"))
        return [r,g,b]

    def pegarPixel(self, event, larg, alt, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            r,g,b = self.imagem[alt, larg]
            self.corSelecionada = [r,g,b]
            cor = self.selecionarCor()
            self.mudarCor(alt,larg, cor)
            self.mostrarImagem()

    def mudarCor(self, alt, larg, cor):
        if alt < 0 or alt >= self.altura or larg < 0 or larg >= self.largura:
            return

        if not (self.imagem[alt, larg] == self.corSelecionada).all():
            return

        self.imagem[alt, larg] = cor


        fila = deque([(alt + 1, larg), (alt - 1, larg), (alt, larg + 1), (alt, larg - 1)])

        while fila:
            a, l = fila.popleft()
            if 0 <= a < self.altura and 0 <= l < self.largura and (self.imagem[a, l] == self.corSelecionada).all():
                self.imagem[a, l] = cor
                fila.extend([(a + 1, l), (a - 1, l), (a, l + 1), (a, l - 1)])

        

    def mostrarImagem(self):
        cv2.namedWindow('janela')
        cv2.setMouseCallback('janela', self.pegarPixel) 
        cv2.imshow('janela',self.imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def salvarEmExcel(self): 
        imagem_hex = [['#{:02X}{:02X}{:02X}'.format(pixel[0], pixel[1], pixel[2]) for pixel in linha] for linha in self.imagem]
        df = pd.DataFrame(imagem_hex)
        arquivo = File.salvarArquivo()
        df.to_excel(arquivo, index=False)
    
    def hex_para_RGB(self,linha):
        linhaRGB = []
        for cores in linha:
            cores = cores.replace("#", "")
            sublistas = [cores[i : i + 2] for i in range(0, len(cores), 2)]
            R = int(sublistas[0], 16)
            G = int(sublistas[1], 16)
            B = int(sublistas[2], 16)
            linhaRGB.append([B, G, R])
        return linhaRGB
        
    def carregarImagemExcel(self):
        caminho_imagem = File.abrirArquivo()
        workbook = openpyxl.load_workbook(caminho_imagem)
        sheet = workbook.active

        matriz_imagem = []
        for linha in sheet.iter_rows(values_only=True):
            linha = self.hex_para_RGB(linha)
            matriz_imagem.append(list(linha))

        matriz_imagem = np.array(matriz_imagem, dtype=np.uint8)

        caminho_salvo = File.salvarArquivo()
        self.imagem =  cv2.imwrite(caminho_salvo, matriz_imagem)
        self.linhas = self.imagem.shape[0]
        self.colunas = self.imagem.shape[1]

if __name__ == "__main__":
    img = Imagem()
    img.carregarImagem()
    img.mostrarImagem()
