import tkinter as tk
from tkinter import ttk, Scale, Label, Button, Checkbutton

class Canal(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Escolher canal")
        self.configure(background='#202124')
        self.geometry("400x300")
        self.resultado = ''
        self.b = tk.IntVar()
        self.g = tk.IntVar()
        self.r = tk.IntVar()

        texto = Label(self, 
                      text='Escolher canal de cor', 
                      font=("Arial",18,'bold'), 
                      background='#202124',
                      anchor='w',
                      fg='white',
                      relief='sunken')
        texto.pack(fill='x',pady=10, padx=10)

        check_azul = Checkbutton(self, text='Azul', variable=self.b)
        check_verde = Checkbutton(self, text='Verde', variable=self.g)
        check_vermelho = Checkbutton(self, text='Vermelho', variable=self.r)

        botao_ok = Button(self, text='Aplicar', command=self.aplicar)

        check_azul.pack()
        check_verde.pack()
        check_vermelho.pack()
        botao_ok.pack()

    def aplicar(self):
        if(self.b.get() == 1):
            self.resultado += 'b'
        if(self.g.get() == 1):
            self.resultado += 'g'
        if(self.r.get() == 1):
            self.resultado += 'r'
        
        print(self.resultado)
        self.destroy()

    

# if __name__ == '__main__':
#     t= tk.Tk()
#     root = Canal(t)
#     t.wait_window()
#     print(root.resultado)
#     root.mainloop()