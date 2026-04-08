import tkinter as tk
from tkinter import colorchooser

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

        btnTransform = tk.Button(frameMenu, text="Transformar Objeto", command=self.transform_object)
        btnTransform.pack(pady=5)

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

        self.update_idletasks()

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
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=obj.cor)

            elif obj.tipo == "reta":
                (x1, y1), (x2, y2) = obj.pontos
                x1, y1 = self.world_to_viewport(x1, y1)
                x2, y2 = self.world_to_viewport(x2, y2)
                self.canvas.create_line(x1, y1, x2, y2, fill=obj.cor)

            elif obj.tipo == "wireframe":
                pontos = [self.world_to_viewport(x, y) for x, y in obj.pontos]
                for i in range(len(pontos)):
                    x1, y1 = pontos[i]
                    x2, y2 = pontos[(i + 1) % len(pontos)]
                    self.canvas.create_line(x1, y1, x2, y2, fill=obj.cor)

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

    def get_objeto_selecionado(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return self.display_file[sel[0]]
    
    def aplicar_transformacao(self, obj, matriz):
        novos_pontos = []

        for (x, y) in obj.pontos:
            ponto = [x, y, 1]

            x_novo = matriz[0][0]*ponto[0] + matriz[0][1]*ponto[1] + matriz[0][2]
            y_novo = matriz[1][0]*ponto[0] + matriz[1][1]*ponto[1] + matriz[1][2]

            novos_pontos.append((x_novo, y_novo))

        obj.pontos = novos_pontos
    
    def matriz_translacao(self, dx, dy):
        return [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ]
    
    def matriz_escala(self, sx, sy):
        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]

    def matriz_rotacao(self, theta):
        import math
        cos = math.cos(theta)
        sin = math.sin(theta)
        return [
            [cos, -sin, 0],
            [sin, cos, 0],
            [0, 0, 1]
        ]
    
    def multiplica_matrizes(self, A, B):
        resultado = [[0]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    resultado[i][j] += A[i][k] * B[k][j]

        return resultado

    def centro_objeto(self,obj):
        xs = [p[0] for p in obj.pontos]
        ys = [p[1] for p in obj.pontos]
        return sum(xs)/len(xs), sum(ys)/len(ys)

    def transform_object(self):
        if self.get_objeto_selecionado() is None:
            from tkinter import messagebox
            messagebox.showerror("Erro", "Selecione um objeto para transformar")
            return
        interfaceTransformObj(self)
    
    def matriz_escala_centro(self, obj, sx, sy):
        cx, cy = self.centro_objeto(obj)

        T1 = self.matriz_translacao(-cx, -cy)
        S  = self.matriz_escala(sx, sy)
        T2 = self.matriz_translacao(cx, cy)

        return self.multiplica_matrizes(T2, self.multiplica_matrizes(S, T1))
    
    def matriz_rotacao_centro_obj(self, obj, theta):
        cx, cy = self.centro_objeto(obj)

        T1 = self.matriz_translacao(-cx, -cy)
        R  = self.matriz_rotacao(theta)
        T2 = self.matriz_translacao(cx, cy)

        return self.multiplica_matrizes(T2, self.multiplica_matrizes(R, T1))

    def matriz_rotacao_ponto(self, px, py, theta):
        T1 = self.matriz_translacao(-px, -py)
        R  = self.matriz_rotacao(theta)
        T2 = self.matriz_translacao(px, py)

        return self.multiplica_matrizes(T2, self.multiplica_matrizes(R, T1))

class interfaceAddObj(tk.Toplevel):
    def __init__(self, parent, title, largura, altura):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{largura}x{altura}")
        self.pontos = []
        self.cor = "#000000"

        tk.Label(self, text="Nome:").pack(pady=5)

        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)
        
        tk.Button(self, text="Escolher cor", command=self.escolher_cor).pack(pady=5)
        self.label_cor = tk.Label(self, text="Cor atual", bg=self.cor)
        self.label_cor.pack()

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

    def escolher_cor(self):
        cor = colorchooser.askcolor(title="Escolha a cor")

        if cor[1] is not None:
            self.cor = cor[1]
            self.label_cor.config(bg=self.cor)

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
        if (tipo == "wireframe" and len(self.pontos) < 3) or (tipo == "reta" and len(self.pontos) != 2) or (tipo == "ponto" and len(self.pontos) != 1):
            messagebox.showerror("Erro", "O tipo do objeto não corresponde ao número de pontos")
            return
        novo_objeto = objeto(nome, tipo, pontos, self.cor)
        self.master.display_file.append(novo_objeto)
        self.master.atualizar_listbox()
        self.master.desenhar_objetos()
        self.destroy()

class interfaceTransformObj(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Transformar Objeto")
        self.geometry("400x650")
        self.transformacoes = []
        self.rotacao_tipo = tk.StringVar(value="mundo")

        frame_translacao = tk.LabelFrame(self, text="Translação")
        frame_translacao.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_translacao, text="dx").grid(row=0, column=0)
        self.entry_dx = tk.Entry(frame_translacao)
        self.entry_dx.grid(row=0, column=1)
        tk.Label(frame_translacao, text="dy").grid(row=1, column=0)
        self.entry_dy = tk.Entry(frame_translacao)
        self.entry_dy.grid(row=1, column=1)
        tk.Button(frame_translacao, text="Adicionar", command=self.add_translacao).grid(row=2, columnspan=2)

        frame_escala = tk.LabelFrame(self, text="Escala")
        frame_escala.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_escala, text="sx").grid(row=0, column=0)
        self.entry_sx = tk.Entry(frame_escala)
        self.entry_sx.grid(row=0, column=1)
        tk.Label(frame_escala, text="sy").grid(row=1, column=0)
        self.entry_sy = tk.Entry(frame_escala)
        self.entry_sy.grid(row=1, column=1)
        tk.Button(frame_escala, text="Adicionar", command=self.add_escala).grid(row=2, columnspan=2)

        frame_rotacao = tk.LabelFrame(self, text="Rotação")
        frame_rotacao.pack(fill="x", padx=10, pady=5)
        self.entry_px = tk.Entry(frame_rotacao)
        self.entry_py = tk.Entry(frame_rotacao)
        tk.Radiobutton(frame_rotacao, text="Centro do mundo", variable=self.rotacao_tipo, value="mundo", command=self.atualizar_campos_rotacao).pack()
        tk.Radiobutton(frame_rotacao, text="Centro do objeto", variable=self.rotacao_tipo, value="objeto", command=self.atualizar_campos_rotacao).pack()
        tk.Radiobutton(frame_rotacao, text="Ponto arbitrário", variable=self.rotacao_tipo, value="ponto", command=self.atualizar_campos_rotacao).pack()
        self.atualizar_campos_rotacao()
        tk.Label(frame_rotacao, text="Ângulo (°)").pack()
        self.entry_ang = tk.Entry(frame_rotacao)
        self.entry_ang.pack()
        tk.Label(frame_rotacao, text="px").pack()
        self.entry_px.pack()
        tk.Label(frame_rotacao, text="py").pack()
        self.entry_py.pack()
        tk.Button(frame_rotacao, text="Adicionar", command=self.add_rotacao).pack()

        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=10)
        tk.Label(frame_lista, text="Transformações a aplicar:").pack()
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox = tk.Listbox(frame_lista, height=5, yscrollcommand=scroll.set)
        self.listbox.pack(side="left")
        scroll.config(command=self.listbox.yview)

        tk.Button(self, text="Remover transformação", command=self.remover_transformacao).pack(pady=5)

        tk.Button(self, text="Aplicar", command=self.aplicar_transformacoes).pack()

    def add_translacao(self):
        from tkinter import messagebox

        try:
            dx = float(self.entry_dx.get())
            dy = float(self.entry_dy.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos para dx ou dy")
            return
        matriz = self.master.matriz_translacao(dx, dy)

        self.transformacoes.append(matriz)
        self.listbox.insert(tk.END, f"T({dx}, {dy})")

    def add_escala(self):
        from tkinter import messagebox

        try:
            sx = float(self.entry_sx.get())
            sy = float(self.entry_sy.get())
        except:
            messagebox.showerror("Erro", "Valores inválidos para sx ou sy")
            return

        obj = self.master.get_objeto_selecionado()
        if obj is None:
            messagebox.showerror("Erro", "Selecione um objeto para escalar")
            return
        matriz = self.master.matriz_escala_centro(obj, sx, sy)

        self.transformacoes.append(matriz)
        self.listbox.insert(tk.END, f"S({sx}, {sy})")

    def add_rotacao(self):
        from tkinter import messagebox
        import math

        try:
            ang = float(self.entry_ang.get())
        except:
            messagebox.showerror("Erro", "Valor inválido para ângulo")
            return

        theta = math.radians(ang)

        tipo = self.rotacao_tipo.get()
        obj = self.master.get_objeto_selecionado()
        if obj is None:
            messagebox.showerror("Erro", "Selecione um objeto para rotacionar")
            return
        if tipo == "mundo":
            matriz = self.master.matriz_rotacao(theta)

        elif tipo == "objeto":
            matriz = self.master.matriz_rotacao_centro_obj(obj, theta)

        elif tipo == "ponto":
            try:
                px = float(self.entry_px.get())
                py = float(self.entry_py.get())
            except:
                messagebox.showerror("Erro", "Valores inválidos para px ou py")
                return

            matriz = self.master.matriz_rotacao_ponto(px, py, theta)

        self.transformacoes.append(matriz)
        self.listbox.insert(tk.END, f"R({ang}°)")

    def aplicar_transformacoes(self):
        from tkinter import messagebox

        obj = self.master.get_objeto_selecionado()
        if obj is None:
            messagebox.showerror("Erro", "Selecione um objeto para transformar")
            return
        if not self.transformacoes:
            messagebox.showerror("Erro", "Nenhuma transformação a ser aplicada")
            return
        if obj is None:
            messagebox.showerror("Erro", "Selecione um objeto para transformar")
            return

        matriz_final = self.transformacoes[0]

        for m in self.transformacoes[1:]:
            matriz_final = self.master.multiplica_matrizes(m, matriz_final)

        self.master.aplicar_transformacao(obj, matriz_final)
        self.master.desenhar_objetos()

        self.destroy()
    
    def atualizar_campos_rotacao(self):
        tipo = self.rotacao_tipo.get()

        if tipo == "ponto":
            self.entry_px.config(state="normal")
            self.entry_py.config(state="normal")
        else:
            self.entry_px.delete(0, tk.END)
            self.entry_py.delete(0, tk.END)
            self.entry_px.config(state="disabled")
            self.entry_py.config(state="disabled")

    def remover_transformacao(self):
        sel = self.listbox.curselection()
        if not sel:
            return

        index = sel[0]

        self.listbox.delete(index)
        self.transformacoes.pop(index)

class objeto:
    def __init__(self, nome, tipo, pontos, cor):
        self.nome = nome
        self.tipo = tipo
        self.pontos = pontos
        self.cor = cor

app = interfaceMain("sgi", 800, 600)
app.mainloop()
