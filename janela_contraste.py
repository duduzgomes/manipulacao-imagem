import tkinter as tk
from tkinter import ttk, Scale, Label, Button

class Contraste(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Contraste")
        self.configure(background='#202124')
        self.geometry("400x300")
        self.valor= 1

        texto = Label(self, 
                      text='Ajustar Contraste', 
                      font=("Arial",18,'bold'), 
                      background='#202124',
                      anchor='w',
                      fg='white',
                      relief='sunken')
        texto.pack(fill='x',pady=10, padx=10)

        scale_horizontal = Scale(self, 
                                 from_=0, 
                                 to= 5, 
                                 orient="horizontal", 
                                 command=self.mudar_valor, 
                                 variable=self.valor,
                                 resolution=0.1,
                                 label='contraste')
        
        scale_horizontal.set(1)
        
        scale_horizontal.pack(padx=20, fill='x', expand=True)

        butao_ok = Button(self, text='Ok', command=self.fechar_janela)
        butao_ok.pack(pady=20,padx=20, side='right')

    def fechar_janela(self):
        self.destroy()

    def mudar_valor(self, valor):
        self.valor = float(valor)
    

# if __name__ == '__main__':
#     t= tk.Tk()
#     root = Contraste(t)
#     root.mainloop()
#     print(root.valor)