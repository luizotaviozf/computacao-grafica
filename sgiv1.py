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

        self.window = {
            "xmin": 0,
            "ymin": 0,
            "xmax": 600,
            "ymax": 600
        }

        # Windows/Mac
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        # Linux
        self.canvas.bind("<Button-4>", self.on_zoom)
        self.canvas.bind("<Button-5>", self.on_zoom)

        self.bind("<Left>", lambda e: self.pan(-10, 0))
        self.bind("<Right>", lambda e: self.pan(10, 0))
        self.bind("<Up>", lambda e: self.pan(0, 10))
        self.bind("<Down>", lambda e: self.pan(0, -10))

        frame_lista = tk.Frame(frameMenu)
        frame_lista.pack(pady=5,padx=5)
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox = tk.Listbox(frame_lista, yscrollcommand=scroll.set)
        self.listbox.pack(fill="both")
        scroll.config(command=self.listbox.yview)
        tk.Label(
            frameMenu,
            text="Panning: setas do teclado\nZoom: scroll do mouse",
            bg="lightgray",
            justify="left"
        ).pack(pady=10)
        self.label_window = tk.Label(
            frameMenu,
            text="",
            bg="lightgray",
            justify="left",
            font=("Arial", 9)
        )
        self.label_window.pack(pady=5)
        self.after(100, self.desenhar_objetos)
        self.after(100, self.atualizar_label_window)
        self.focus_set()

    def atualizar_label_window(self):
        w = self.window
        texto = (
            f"Window:\n"
            f"xmin: {w['xmin']:.2f}\n"
            f"ymin: {w['ymin']:.2f}\n"
            f"xmax: {w['xmax']:.2f}\n"
            f"ymax: {w['ymax']:.2f}"
        )
        self.label_window.config(text=texto)

    def pan(self, dx, dy):
        self.window["xmin"] += dx
        self.window["xmax"] += dx
        self.window["ymin"] += dy
        self.window["ymax"] += dy

        self.desenhar_objetos()
        self.atualizar_label_window()

    def zoom(self, fator):
        w = self.window

        cx = (w["xmin"] + w["xmax"]) / 2
        cy = (w["ymin"] + w["ymax"]) / 2

        largura = (w["xmax"] - w["xmin"]) * fator
        altura = (w["ymax"] - w["ymin"]) * fator

        self.window["xmin"] = cx - largura / 2
        self.window["xmax"] = cx + largura / 2
        self.window["ymin"] = cy - altura / 2
        self.window["ymax"] = cy + altura / 2

        self.desenhar_objetos()
        self.atualizar_label_window()

    def on_zoom(self, event):
        # Windows / Mac
        if hasattr(event, "delta") and event.delta != 0:
            if event.delta > 0:
                self.zoom(0.9)
            else:
                self.zoom(1.1)

        # Linux scroll up
        elif event.num == 4:
            self.zoom(0.9)

        # Linux scroll down
        elif event.num == 5:
            self.zoom(1.1)

    def world_to_viewport(self, x, y):
        w = self.window

        self.update_idletasks()  # garante tamanho correto

        vw = self.canvas.winfo_width()
        vh = self.canvas.winfo_height()

        xv = (x - w["xmin"]) / (w["xmax"] - w["xmin"]) * vw
        yv = (y - w["ymin"]) / (w["ymax"] - w["ymin"]) * vh

        yv = vh - yv  # inverte eixo Y

        return xv, yv

    def desenhar_objetos(self):
        self.canvas.delete("all")

        for obj in self.display_file:

            if obj.tipo == "ponto":
                x, y = self.world_to_viewport(*obj.pontos[0])
                r = 3
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

            elif obj.tipo == "reta":
                (x1, y1), (x2, y2) = obj.pontos
                x1, y1 = self.world_to_viewport(x1, y1)
                x2, y2 = self.world_to_viewport(x2, y2)
                self.canvas.create_line(x1, y1, x2, y2, fill="blue")

            elif obj.tipo == "wireframe":
                pontos = [self.world_to_viewport(x, y) for x, y in obj.pontos]
                self.canvas.create_polygon(pontos, outline="green", fill="")

    def add_object(self):
        interfaceAddObj(self, "Adicionar Objeto", 400, 550)

    def remove_object(self):
        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            self.listbox.delete(index)
            self.display_file.pop(index)
        self.atualizar_listbox()
        self.desenhar_objetos()

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
        self.master.desenhar_objetos()
        self.destroy()

class objeto:
    def __init__(self, nome, tipo, pontos):
        self.nome = nome
        self.tipo = tipo
        self.pontos = pontos

app = interfaceMain("sgi", 800, 600)
app.mainloop()
