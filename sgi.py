import tkinter as tk

class interfaceMain(tk.Tk):
    def __init__(self, title, largura, altura):
        super().__init__()
        self.title(title)
        self.largura = largura
        self.altura = altura
        self.geometry(f'{largura}x{altura}+{int((self.winfo_screenwidth() - largura) / 2)}+{int((self.winfo_screenheight() - altura) / 2)}')
        self.display_file = []

        frameMenu = tk.Frame(self, bg="lightgray", width=200)
        frameMenu .pack(side="left", fill="y")

        frameCanvas = tk.Frame(self, bg="white")
        frameCanvas.pack(side="right", fill="both", expand=True)

        btnAddObj = tk.Button(frameMenu, text="Adicionar Objeto", command=self.add_object)
        btnAddObj.pack(pady=10)

        btnRemoveObj = tk.Button(frameMenu, text="Remover Objeto", command=self.remove_object)
        btnRemoveObj.pack()

        self.canvas = tk.Canvas(frameCanvas, bg="white")
        self.canvas.pack(fill="both", expand=True)

        frame_lista = tk.Frame(frameMenu)
        frame_lista.pack(pady=5,padx=5)
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox = tk.Listbox(frame_lista, yscrollcommand=scroll.set)
        self.listbox.pack(fill="both")
        scroll.config(command=self.listbox.yview)

    def add_object(self):
        interfaceAddObj(self, "Adicionar Objeto", 400, 550)

    def remove_object(self):
        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            self.listbox.delete(index)
            self.display_file.pop(index)
        self.atualizar_listbox()

    def atualizar_listbox(self):
        self.listbox.delete(0, tk.END)
        for obj in self.display_file:
            texto = f"{obj.nome} ({obj.tipo})"
            self.listbox.insert(tk.END, texto)

class interfaceAddObj(tk.Toplevel):
    def __init__(self, parent, title, largura, altura):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{largura}x{altura}")
        self.pontos = []

        tk.Label(self, text="Nome:").pack(pady=5)

        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)
        
        tk.Label(self, text="Tipo:").pack(pady=5)

        self.tipo_var = tk.StringVar(value="ponto")

        tk.Radiobutton(self, text="Pt", variable=self.tipo_var, value="ponto").pack()
        tk.Radiobutton(self, text="Rt", variable=self.tipo_var, value="reta").pack()
        tk.Radiobutton(self, text="Wf", variable=self.tipo_var, value="wireframe").pack()

        tk.Label(self, text="Pontos:").pack(pady=5)

        tk.Label(self, text="X:").pack()
        self.entry_x = tk.Entry(self)
        self.entry_x.pack()

        tk.Label(self, text="Y:").pack()
        self.entry_y = tk.Entry(self)
        self.entry_y.pack()

        tk.Button(self, text="Adicionar ponto", command=self.add_ponto).pack(pady=5)

        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=10)
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox_pontos = tk.Listbox(frame_lista, height=5, yscrollcommand=scroll.set)
        self.listbox_pontos.pack(side="left")
        scroll.config(command=self.listbox_pontos.yview)

        tk.Button(self, text="Remover ponto", command=self.remover_ponto).pack(pady=5)

        tk.Button(self, text="Salvar", command=self.save_object).pack(pady=10)

    def add_ponto(self):
        from tkinter import messagebox

        tipo = self.tipo_var.get()
        if tipo == "ponto" and len(self.pontos) >= 1:
            messagebox.showerror("Erro", "Objeto do tipo ponto aceita apenas 1 ponto")
            return
        if tipo == "reta" and len(self.pontos) >= 2:
            messagebox.showerror("Erro", "Reta aceita no máximo 2 pontos")
            return

        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())

            self.pontos.append((x, y))
            self.listbox_pontos.insert(tk.END, f"({x}, {y})")

            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
        except:
            messagebox.showerror("Erro", "Coordenadas inválidas")
        
    def remover_ponto(self):
        sel = self.listbox_pontos.curselection()
        if sel:
            index = sel[0]
            self.listbox_pontos.delete(index)
            self.pontos.pop(index)

    def save_object(self):
        from tkinter import messagebox

        nome = self.entry_nome.get()
        tipo = self.tipo_var.get()
        pontos = self.pontos
        if tipo == "wireframe" and len(self.pontos) < 3 or (tipo == "reta" and len(self.pontos) != 2) or (tipo == "ponto" and len(self.pontos) != 1):
            messagebox.showerror("Erro", "O tipo do objeto não corresponde ao número de pontos")
            return
        novo_objeto = objeto(nome, tipo, pontos)
        self.master.display_file.append(novo_objeto)
        self.master.atualizar_listbox()
        self.destroy()

class objeto:
    def __init__(self, nome, tipo, pontos):
        self.nome = nome
        self.tipo = tipo
        self.pontos = pontos

app = interfaceMain("sgi", 800, 600)
app.mainloop()