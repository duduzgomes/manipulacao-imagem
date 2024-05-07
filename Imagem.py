import cv2
import pandas as pd
import openpyxl
import numpy as np
from File import File
from collections import deque
from PIL import Image 


class Imagem:
    def __init__(self):
        self.caminho_do_arquivo = None
        self.imagem = None
        self.linhas = None
        self.colunas = None
        self.corSelecionada = None
        self.fila = []

    def carregarImagem(self):
        self.caminho_do_arquivo = File.abrirArquivo()
        self.imagem = cv2.imread(self.caminho_do_arquivo, 1)
        self.altura = self.imagem.shape[0]
        self.largura = self.imagem.shape[1]
        self.canal = self.imagem.shape[2]

    def selecionarCor(self):
        print("Digite uma com cor:")
        r = int(input("R:"))
        g = int(input("G:"))
        b = int(input("B:"))
        return [b, g, r]

    def rgbParaCmyk(self, r, g, b):
        c = 1 - (r / 255)
        m = 1 - (g / 255)
        y = 1 - (b / 255)

        k = min(c, m, y)

        if(k < 1):
            c = (c - k) / (1 - k )
            m = (m - k) / (1 - k )
            y = (y - k) / (1 - k )
            k = k
        return [c*255, m*255, y*255, k*255]
    
    def calcPonderadaCinza(self, r, g, b):
        media = r*0.2989 + g*0.5870 + b*0.1140 
        return round(media)
    
    def calcCinzaMedia(self, r, g, b):
        media = (r*0.33 + g*0.33 + b* 0.33)
        return round(media)
    
    def calcMinCinza(self, r, g, b):
        m = min(r, g, b)
        return m
    
    def calcMaxCinza(self, r, g, b):
        m = max(r, g, b)
        return m
    
    def calTonCinza(self):
        img = Image.open(self.caminho_do_arquivo)
        img_array = np.array(self.imagem)
        alt = img_array.shape[0]
        larg = img_array.shape[1]

        img_cinza = np.zeros((img_array.shape[0], img_array.shape[1]), np.uint8)
        
        for a in range(alt):
            for l in range(larg):
                b,g,r = img_array[a, l] 
                img_cinza[a,l] = self.calcPonderadaCinza(r,g,b)

        img_c = Image.fromarray(img_cinza, mode='L')
        img_c.save('images/imagem-cinza.jpg')
        img_c.show()

        img.show()
    
    def gerarImagemCmyk(self):
        img = Image.open(self.caminho_do_arquivo)
        img_array = np.array(self.imagem)
        alt = img_array.shape[0]
        larg = img_array.shape[1]

        imagem_cmyk = np.zeros((img_array.shape[0], img_array.shape[1], 4), np.uint8)
        
        for a in range(alt):
            for l in range(larg):
                b,g,r = img_array[a, l] 
                imagem_cmyk[a,l] = self.rgbParaCmyk(r,g,b)
        
        new = Image.fromarray(imagem_cmyk, mode='CMYK')
        new.save('images/new.jpg')

        teste = img.convert('CMYK')
        r = np.array(teste)
        w = Image.fromarray(r, mode='CMYK')

        print(img.mode)
        print(img_array.shape)

        print(new.mode)
        print(imagem_cmyk.shape)

        print(img_array[1,1])
        print(imagem_cmyk[1,1])
        print(r[1,1])

        w.show()
        new.show()
        # img.show()

    def pegarPixel(self, event, larg, alt, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            r, g, b = self.imagem[alt, larg]
            self.corSelecionada = [r, g, b]
            cor = self.selecionarCor()
            self.mudarCor(alt, larg, cor)
            self.mostrarImagem()

    def mudarCor(self, alt, larg, cor):
        if alt < 0 or alt >= self.altura or larg < 0 or larg >= self.largura:
            return

        self.imagem[alt, larg] = cor

        fila = deque(
            [(alt + 1, larg), (alt - 1, larg), (alt, larg + 1), (alt, larg - 1)]
        )

        while fila:
            a, l = fila.popleft()
            if (
                0 <= a < self.altura
                and 0 <= l < self.largura
                and (self.imagem[a, l] == self.corSelecionada).all()
            ):
                self.imagem[a, l] = cor
                fila.extend([(a + 1, l), (a - 1, l), (a, l + 1), (a, l - 1)])

    def mostrarImagem(self):
        cv2.namedWindow("janela")
        cv2.setMouseCallback("janela", self.pegarPixel)
        cv2.imshow("janela", self.imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def salvarEmExcel(self):
        imagem_hex = [
            [
                "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2])
                for pixel in linha
            ]
            for linha in self.imagem
        ]
        df = pd.DataFrame(imagem_hex)
        arquivo = File.salvarArquivo()
        df.to_excel(arquivo, index=False)

    def hex_para_RGB(self, linha):
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
        cv2.imwrite(caminho_salvo, matriz_imagem)
        self.imagem = cv2.imread(caminho_salvo, 1)
        self.caminho_do_arquivo = caminho_salvo
        self.altura = self.imagem.shape[0]
        self.largura = self.imagem.shape[1]
        self.canal = self.imagem.shape[2]


if __name__ == "__main__":
    img = Imagem()
    img.carregarImagem()
    img.calTonCinza()
    # img.mostrarImagem()
