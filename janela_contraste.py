import tkinter as tk
from tkinter import ttk, Scale, Label, Button

class Contraste(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Contraste")
        self.configure(background='#202124')
        self.geometry("400x300")

        self.taxa_contraste= tk.DoubleVar()
        self.taxa_brilho= tk.DoubleVar()

        texto = Label(self, 
                      text='Ajustar Contraste', 
                      font=("Arial",18,'bold'), 
                      background='#202124',
                      anchor='w',
                      fg='white',
                      relief='sunken')
        texto.pack(fill='x',pady=10, padx=10)

        scale_contraste = Scale(self, 
                                 from_=0, 
                                 to= 2, 
                                 orient="horizontal", 
                                 command=self.mudar_contraste, 
                                 variable=self.taxa_contraste,
                                 resolution=0.1,
                                 label='contraste')
        
        scale_brilho = Scale(self, 
                                 from_= -1, 
                                 to= 1, 
                                 orient="horizontal", 
                                 command=self.mudar_brilho, 
                                 variable=self.taxa_brilho,
                                 resolution=0.1,
                                 label='brilho')
        
        scale_contraste.set(1)
        scale_brilho.set(0)
        
        scale_contraste.pack(padx=20, fill='x', expand=True)
        scale_brilho.pack(padx=20, fill='x', expand=True)

        butao_ok = Button(self, text='Ok', command=self.fechar_janela)
        butao_ok.pack(pady=20,padx=20, side='right')

    def fechar_janela(self):
        self.brilho = self.taxa_brilho.get()
        self.contraste = self.taxa_contraste.get()
        self.destroy()

    def mudar_contraste(self, valor):
        self.taxa_contraste.set(valor)

    def mudar_brilho(self, valor):
        self.taxa_brilho.set(valor)
    

if __name__ == '__main__':
    t= tk.Tk()
    root = Contraste(t)
    root.mainloop()
    print(root.valor)