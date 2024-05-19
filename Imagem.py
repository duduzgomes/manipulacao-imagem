import cv2
import pandas as pd
import openpyxl
import numpy as np
from File import File
from collections import deque
from PIL import Image 
import matplotlib.pyplot as plt


class Imagem:
    def __init__(self):
        self.caminho_do_arquivo = None
        self.imagem = None
        self.altura = None
        self.largura = None
        self.corSelecionada = None
        self.fila = []

    def carregarImagem(self):
        self.caminho_do_arquivo = File.abrirArquivo()
        self.img = Image.open(self.caminho_do_arquivo).convert("RGB")
        self.imagem = np.array(self.img)
        self.altura, self.largura, self.canal = self.imagem.shape

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
        m = round(media)
        return (m,m,m)
        
    def calcCinzaMedia(self, r, g, b):
        media = (r*0.33 + g*0.33 + b* 0.33)
        return round(media)

    def calcMinCinza(self, r, g, b):
        m = min(r, g, b)
        return (m,m,m)

    def calcMaxCinza(self, r, g, b):
        m = max(r, g, b)
        return (m,m,m)
    
    def gerarImagemCinza(self):
        img_array = self.imagem
        alt = img_array.shape[0]
        larg = img_array.shape[1]

        img_cinza = np.zeros((img_array.shape[0], img_array.shape[1], 3), np.uint8)
        
        for a in range(alt):
            for l in range(larg):
                b,g,r = img_array[a, l] 
                img_cinza[a,l] = self.calcMaxCinza(r,g,b)


        self.imagem = img_cinza
        
    
    def gerarImagemCmyk(self):
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
    
    def gerar_histrograma(self):
        histograma = {}

        for i in range(255):
            histograma[i] = 0

        for l in range(self.altura):
            for c in range(self.largura):
                intensidade = min(self.imagem[l, c])
                if(intensidade in histograma):
                    histograma[intensidade] += 1
                
        return histograma
    
    def gerar_histrograma_RGB(self):
        hist_b = {}
        hist_g = {}
        hist_r = {}

        for i in range(256):
            hist_b[i] = 0
            hist_g[i] = 0
            hist_r[i] = 0

        for l in range(self.altura):
            for c in range(self.largura):
                r,g,b = self.imagem[l, c]
                hist_b[b] += 1 
                hist_g[g] += 1 
                hist_r[r] += 1 
                
        return [hist_b,hist_g,hist_r]
    
    def equalizar(self):
        hist_b, hist_g,hist_r = self.gerar_histrograma_RGB()


        hist_norm_B = self.normalizar_histograma(hist_b)
        hist_norm_G = self.normalizar_histograma(hist_g)
        hist_norm_R = self.normalizar_histograma(hist_r)
        

        for l in range(self.altura):
            for c in range(self.largura):
                r,g,b = self.imagem[l,c]
                B = hist_norm_B[b]
                G = hist_norm_G[g]
                R = hist_norm_R[r]
                self.imagem[l,c] = (R,G,B)

    def normalizar_histograma(self, hist):
        qtd_pixels = sum(hist.values())

        histograma_normalizado = {}
        intesidade_acumulada = 0
        for i in range(255):
            histograma_normalizado[i] = 0

        for intesidade, valor in hist.items():
            histograma_normalizado[intesidade] = valor / qtd_pixels + intesidade_acumulada
            intesidade_acumulada = histograma_normalizado[intesidade] 
            histograma_normalizado[intesidade] *= 255
            histograma_normalizado[intesidade] = round(histograma_normalizado[intesidade])

        return histograma_normalizado
    
    def min_valor(self,d):
        minimo = 0
        for k , v in d.items():
            if(v > 0):
                minimo = int(k)
                break
        return minimo
    def max_valor(self,d):
        maximo = 0
        for k , v in d.items():
            if(v > 0):
                maximo = int(k)
                
        return maximo

    def contraste(self, taxa):
        b, g ,r = self.gerar_histrograma_RGB()

        min_b = self.min_valor(b)
        min_g = self.min_valor(g)
        min_r = self.min_valor(r)

        max_b = self.max_valor(b)
        max_g = self.max_valor(g)
        max_r = self.max_valor(r)
        
        fd_b = max_b - min_b
        fd_g = max_g - min_g
        fd_r = max_r - min_r

        fator_escala_b = round(taxa * 255 / fd_b)
        fator_escala_g = round(taxa * 255 / fd_g)
        fator_escala_r = round(taxa * 255 / fd_r)
        
        
        for i in range(self.altura):
            for j in range(self.largura):
                R, G, B = self.imagem[i,j]
                b = round((B - min_b) * fator_escala_b)
                g = round((G - min_g) * fator_escala_g)
                r = round((R - min_r) * fator_escala_r)
                self.imagem[i,j] = (min(r,255), min(g,255), min(b, 255))


    def plotarHistograma(self, h1,h2,h3):

        x1 = np.array(list(h1.values()))
        x2 = np.array(list(h2.values()))
        x3 = np.array(list(h3.values()))
        

        plt.plot(range(256), x1, color='blue')
        plt.plot(range(256), x2, color='green')
        plt.plot(range(256), x3, color='red')
        plt.title('RGB')
        plt.xlabel('Valor')
        plt.ylabel('Frequência')
        plt.grid(True)
        plt.show()
    
    def mostrar_canal(self, canal):    
        for i in range(self.altura):
            for j in range(self.largura):
                R, G, B = self.imagem[i,j]
                if(canal == 'b'):
                    self.imagem[i,j] = (B,0,0)
                elif(canal == 'g'):
                    self.imagem[i,j] = (0,G,0)
                elif(canal == 'r'):
                    self.imagem[i,j] = (0,0,R)
                elif(canal == 'bg' or canal == 'gb'):
                    self.imagem[i,j] = (B,G,0)
                elif(canal == 'br' or canal == 'rb'):
                    self.imagem[i,j] = (B,0,R)
                elif(canal == 'gr' or canal == 'rg'):
                    self.imagem[i,j] = (0,G,R)
                elif(canal == 'r'):
                    self.imagem[i,j] = (0,0,R)

        self.mostrarImagem()

    def deteccao_borda(self):
        # m = [-1,0,1,-2,0,2,-1,0,1] # Sobel
        # m = [0,-1,0,-1,4,-1,0,-1,0] # Laplaciano
        m = [-1,-1,-1,-1,8,-1,-1,-1,-1] # Laplaciano melhorado
        # m = [5,5,5,-3,0,-3,-3,-3,-3] #  Kirsch 

        img_saida = np.zeros((self.altura, self.largura,3),np.uint8)

        for a in range(self.altura):
            for l in range(self.largura):
                p = min(self.imagem[a,l])
                if(a == 0 or a == self.altura -1 or l == 0 or l == self.largura-1):
                    continue
                pe = min(self.imagem[a,l-1])
                pec = min(self.imagem[a+1,l-1])
                peb = min(self.imagem[a-1,l-1])
                pd = min(self.imagem[a,l+1])
                pdc = min(self.imagem[a+1,l+1])
                pdb = min(self.imagem[a-1,l+1])
                pc = min(self.imagem[a+1,l])
                pb = min(self.imagem[a-1,l])
            
                media = (pec * m[0] + pc * m[1] + pdc * m[2] + pe * m[3] + p * m[4]
                      + pd * m[5] + peb * m[6] + pb * m[7] + pdb * m[8]) 
                
                r = round(media)

                if(r > 255):
                    r=255
                elif( r < 0):
                    r=0

                img_saida[a,l] = (r,r,r) 
        
        self.imagem = img_saida


    def filtro_blur(self):

        m = [1,1,1,1,1,1,1,1,1]
        img_saida = np.zeros((self.altura, self.largura,3),np.uint8)

        for a in range(self.altura):
            for l in range(self.largura):
                p = min(self.imagem[a,l])
                if(a == 0 or a == self.altura -1 or l == 0 or l == self.largura-1):
                    continue
                pe = min(self.imagem[a,l-1])
                pec = min(self.imagem[a+1,l-1])
                peb = min(self.imagem[a-1,l-1])
                pd = min(self.imagem[a,l+1])
                pdc = min(self.imagem[a+1,l+1])
                pdb = min(self.imagem[a-1,l+1])
                pc = min(self.imagem[a+1,l])
                pb = min(self.imagem[a-1,l])
            
                media = (pec * m[0] + pc * m[1] + pdc * m[2] + pe * m[3] + p * m[4]
                    + pd * m[5] + peb * m[6] + pb * m[7] + pdb * m[8]) / 9
                
                r = round(media)

                if(r > 255):
                    r=255
                elif( r < 0):
                    r=0

                img_saida[a,l] = (r,r,r) 
        
        self.imagem = img_saida



if __name__ == "__main__":
    img = Imagem()
    img.carregarImagem()
    img.deteccao_borda()
    

