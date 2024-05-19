import tkinter as tk
from tkinter import ttk, Frame, Button, Menu
from PIL import Image, ImageTk
from Imagem import Imagem


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter PhotoImage Demo')
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

        frame_menu = Frame(self, padx=40, pady=40)
        frame_menu.grid(row=0, column=2, sticky='ns')
        frame_menu.config(background='#171717')

        self.label_imagem = ttk.Label(frame_img, image=self.python_image)
        self.label_imagem.pack()

        menu_principal = Menu(self)

        menu_arquivo = Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label='Abrir', command=self.abrir_imagem)
        menu_arquivo.add_command(label='Salvar Imagem', command=self.excel)

        menu_imagem = Menu(menu_principal, tearoff=0)
        menu_imagem.add_command(label='Converter para CMYK', command=self.imagem_cmyk)
        menu_imagem.add_command(label='Converter para Cinza', command=self.imagem_cinza)
        
        menu_cores = Menu(menu_principal, tearoff=0)
        menu_cores.add_command(label='Contraste', command=self.contraste)
        menu_cores.add_command(label='Equalizar', command=self.equalizar)

        menu_filtro = Menu(menu_principal, tearoff=0)
        menu_filtro.add_command(label='Detectar Bordas', command=self.detectar_bordas)
        menu_filtro.add_command(label='Desfoque (blur)', command=self.fitro_blur)

        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_principal.add_cascade(label="Imagem", menu=menu_imagem)
        menu_principal.add_cascade(label="Cores", menu=menu_cores)
        menu_principal.add_cascade(label="Filtros", menu=menu_filtro)

        self.config(menu=menu_principal)
    
    def carregar_e_mostrar_imagem(self):
        self.img.carregarImagem()
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)

    def abrir_imagem(self):
        self.carregar_e_mostrar_imagem()
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image
    
    def imagem_cmyk(self):
        self.img.gerarImagemCmyk()

    def excel(self):
        self.img.salvarEmExcel()
    
    def equalizar(self):
        self.img.equalizar()
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image
    
    def imagem_cinza(self):
        self.img.gerarImagemCinza()
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image

    def contraste(self):
        self.img.contraste(1)
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image
    
    def detectar_bordas(self):
        self.img.deteccao_borda()
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image
    
    def fitro_blur(self):
        self.img.filtro_blur()
        self.image = Image.fromarray(self.img.imagem)
        self.python_image = ImageTk.PhotoImage(self.image)
        self.label_imagem.configure(image=self.python_image)
        self.label_imagem.image = self.python_image



if __name__ == '__main__':
    app = App()
    app.mainloop()