import tkinter as tk
from tkinter import ttk, Frame, Button, Menu
from PIL import Image, ImageTk
from Imagem import Imagem
from janela_contraste import Contraste
from janela_canal import Canal
from janela_bordas import Borda


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Photoshop da Shoppe')
        self.configure(background='#202124')
        self.img = Imagem()
        self.carregar_e_mostrar_imagem()

        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()
        largura = 1200
        altura =  800
        posx = largura_screen / 2 - largura / 2
        posy = altura_screen / 2 - altura / 2
        self.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_img = Frame(self, padx=40, pady=40)
        frame_img.grid(row=0, column=0)
        frame_img.config(background='#212121')

        frama_imagem_saida = Frame(self, padx=40, pady=40)
        frama_imagem_saida.grid(row=0, column=2)
        frama_imagem_saida.config(background='#212121')

        self.label_imagem_entrada = ttk.Label(frame_img, image=self.python_image_entrada)
        self.label_imagem_entrada.pack(side='left')

        self.label_imagem_saida = ttk.Label(frame_img, image=self.python_image_saida)
        self.label_imagem_saida.pack(side='right')


        menu_principal = Menu(self)

        menu_arquivo = Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label='Abrir', command=self.abrir_imagem)
        menu_arquivo.add_command(label='Salvar Imagem', command=self.salvar_imagem)
        menu_arquivo.add_command(label='Salvar em Excel', command=self.excel)

        menu_cinza = Menu(menu_principal, tearoff=0)
        menu_cinza.add_command(label='Minimo', command=self.imagem_cinza_min)
        menu_cinza.add_command(label='Maximo', command=self.imagem_cinza_max)
        menu_cinza.add_command(label='Média', command=self.imagem_cinza_media)
        menu_cinza.add_command(label='Ponderada', command=self.imagem_cinza_ponderada)
        
        menu_histograma = Menu(menu_principal, tearoff=0)
        menu_histograma.add_command(label='Imagem de Entrada', command=self.histograma_entrada)
        menu_histograma.add_command(label='Imagem de Saída', command=self.histograma_saida)

        menu_imagem = Menu(menu_principal, tearoff=0)
        menu_imagem.add_command(label='Converter para CMYK', command=self.imagem_cmyk)
        
        menu_cores = Menu(menu_principal, tearoff=0)
        menu_cores.add_command(label='Contraste e Brilho', command=self.contraste_brilho)
        menu_cores.add_command(label='Equalizar', command=self.equalizar)
        menu_cores.add_command(label='Canais de cores', command=self.escolher_canal)

        menu_filtro = Menu(menu_principal, tearoff=0)
        menu_filtro.add_command(label='Detectar Bordas', command=self.detectar_bordas)
        menu_filtro.add_command(label='Desfoque (blur)', command=self.fitro_blur)

        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_principal.add_cascade(label="Imagem", menu=menu_imagem)
        menu_principal.add_cascade(label="Cores", menu=menu_cores)
        menu_principal.add_cascade(label="Filtros", menu=menu_filtro)
        menu_imagem.add_cascade(label='Converter para Cinza', menu=menu_cinza);
        menu_imagem.add_cascade(label='Plotar Histograma', menu=menu_histograma);

        self.config(menu=menu_principal)
    
    def carregar_e_mostrar_imagem(self):
        self.img.carregarImagem()
        self.image_entrada = Image.fromarray(self.img.imagem)
        self.image_saida = Image.fromarray(self.img.imagem_saida)
        self.python_image_entrada = ImageTk.PhotoImage(self.image_entrada)
        self.python_image_saida = ImageTk.PhotoImage(self.image_saida)
    
    def carregar_imagem_saida(self):
        self.image_saida = Image.fromarray(self.img.imagem_saida)
        self.python_image_saida = ImageTk.PhotoImage(self.image_saida)
        self.label_imagem_saida.configure(image=self.python_image_saida)
        self.label_imagem_saida.image = self.python_image_saida

    def abrir_imagem(self):
        self.carregar_e_mostrar_imagem()
        self.label_imagem_entrada.configure(image=self.python_image_entrada)
        self.label_imagem_entrada.image = self.python_image_entrada
        self.carregar_imagem_saida()
    
    def imagem_cmyk(self):
        self.img.gerarImagemCmyk()

    def excel(self):
        self.img.salvarEmExcel()
    
    def equalizar(self):
        self.img.equalizar()
        self.carregar_imagem_saida()
    
    def imagem_cinza_min(self):
        self.img.gerarImagemCinza('min')
        self.carregar_imagem_saida()
    
    def imagem_cinza_max(self):
        self.img.gerarImagemCinza('max')
        self.carregar_imagem_saida()
    
    def imagem_cinza_media(self):
        self.img.gerarImagemCinza('media')
        self.carregar_imagem_saida()
    
    def imagem_cinza_ponderada(self):
        self.img.gerarImagemCinza('ponderada')
        self.carregar_imagem_saida()
    
    def contraste_brilho(self):
        root = Contraste(self)
        self.wait_window(root)
        print(root.contraste)
        print(root.brilho)
        self.img.contraste_brilho(root.contraste, root.brilho)
        self.carregar_imagem_saida()
    
    def detectar_bordas(self):
        root = Borda(self)
        self.wait_window(root)
        self.img.deteccao_borda(root.mascara)
        self.carregar_imagem_saida()
    
    def fitro_blur(self):
        self.img.filtro_blur()
        self.carregar_imagem_saida()
    
    def escolher_canal(self):
        root = Canal(self)
        self.wait_window(root)
        self.img.mostrar_canal(root.resultado)
        self.carregar_imagem_saida()
    
    def histograma_entrada(self):
        self.img.plotarHistograma_img_entrada()

    def histograma_saida(self):
        self.img.plotarHistograma_img_saida()

    def salvar_imagem(self):
        self.img.salvar_imagem()



if __name__ == '__main__':
    app = App()
    app.mainloop()