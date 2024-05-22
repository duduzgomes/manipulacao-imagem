import tkinter as tk
from tkinter import Entry, Label, Frame, Button

class Borda(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Detecção de Bordas")
        self.configure(background='#202124')
        self.geometry("400x300")

        self.mascara = []
        self.array = []

        texto = Label(self, 
                      text='Defina uma Máscara', 
                      font=("Arial",18,'bold'), 
                      background='#202124',
                      anchor='w',
                      fg='white',
                      relief='sunken')
        texto.pack(fill='x',pady=10, padx=10)

        frame = Frame(self, height=500)
        frame.pack(expand=True)


        botao = Button(self, text='Aplicar', command=self.aplicar)
        botao.pack()

        for i in range(3):
            for j in range(3):
                entry = Entry(frame, width=10, font=18,  justify='center')
                entry.grid(row=i, column=j, padx=3, pady=3)
                self.array.append(entry)



        # self.l1 = Entry(frame, width=10, font=18,  justify='center').grid(row=0, column=0, padx=3, pady=3)
        # self.l2 = Entry(frame, width=10, font=18, justify='center').grid(row=0, column=1, padx=3, pady=3)
        # self.l3 = Entry(frame, width=10, font=18, justify='center').grid(row=0, column=2, padx=3, pady=3)

        # self.l4 = Entry(frame, width=10, font=18,  justify='center').grid(row=1, column=0, padx=3, pady=3)
        # self.l5 = Entry(frame, width=10, font=18,  justify='center').grid(row=1, column=1, padx=3, pady=3)
        # self.l6 = Entry(frame, width=10, font=18,  justify='center').grid(row=1, column=2, padx=3, pady=3)

        # self.l7 = Entry(frame, width=10, font=18, justify='center').grid(row=2, column=0, padx=3, pady=3)
        # self.l8 = Entry(frame, width=10, font=18, justify='center').grid(row=2, column=1, padx=3, pady=3)
        # self.l9 = Entry(frame, width=10, font=18, justify='center').grid(row=2, column=2, padx=3, pady=3)

    def aplicar(self):
        for entry in self.array:
            valor = int(entry.get())
            self.mascara.append(valor)
        
        print(self.mascara)
        
        self.destroy()


    

if __name__ == '__main__':
    t= tk.Tk()
    root = Borda(t)
    t.wait_window(root)
    root.mainloop()