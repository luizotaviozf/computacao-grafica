import tkinter as tk
from tkinter import colorchooser
from objetos.objeto import objeto

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

        tk.Radiobutton(self, text="Ponto", variable=self.tipo_var, value="ponto", command=self.atualizar_interface_tipo).pack()
        tk.Radiobutton(self, text="Reta", variable=self.tipo_var, value="reta", command=self.atualizar_interface_tipo).pack()
        tk.Radiobutton(self, text="Wireframe", variable=self.tipo_var, value="wireframe", command=self.atualizar_interface_tipo).pack()
        tk.Radiobutton(self, text="Preenchido",variable=self.tipo_var, value="fill", command=self.atualizar_interface_tipo).pack()
        tk.Radiobutton(self, text="Bezier", variable=self.tipo_var, value="bezier", command=self.atualizar_interface_tipo).pack()
        tk.Radiobutton(self,text="B-Spline",variable=self.tipo_var,value="bspline",command=self.atualizar_interface_tipo).pack()

        tk.Label(self, text="Bezier e B-Spline (formato):").pack(pady=5)
        self.entry_bezier = tk.Entry(self, width=40)
        self.entry_bezier.pack()
        tk.Label(self, text="Ex: (10,20),(50,80),(100,30),(150,90)", font=("Arial", 8)).pack()

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

        self.atualizar_interface_tipo()

    def atualizar_interface_tipo(self):
        tipo = self.tipo_var.get()

        if tipo in ["bezier", "bspline"]:
            self.entry_x.config(state="disabled")
            self.entry_y.config(state="disabled")
            self.listbox_pontos.config(state="disabled")
            self.entry_bezier.config(state="normal")
        else:
            self.entry_x.config(state="normal")
            self.entry_y.config(state="normal")
            self.listbox_pontos.config(state="normal")
            self.entry_bezier.config(state="disabled")

    def parse_bezier_points(self, texto):
        import re

        padrao = r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
        matches = re.findall(padrao, texto)

        pontos = []

        for x, y in matches:
            pontos.append((float(x), float(y)))

        return pontos

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
        if not nome:
            messagebox.showerror("Erro", "O nome do objeto não pode ser vazio")
            return
        tipo = self.tipo_var.get()
        
        if tipo in ["bezier", "bspline"]:
            texto = self.entry_bezier.get().strip()
            pontos = self.parse_bezier_points(texto)
        else:
            pontos = self.pontos

        if (tipo == "wireframe" and len(pontos) < 3) or (tipo == "reta" and len(pontos) != 2) or (tipo == "ponto" and len(pontos) != 1) or (tipo == "fill" and len(pontos) < 3):
            messagebox.showerror("Erro", "O tipo do objeto não corresponde ao número de pontos")
            return
        elif tipo == "bezier":
            if len(pontos) < 4 or (len(pontos) - 4) % 3 != 0:
                messagebox.showerror("Erro", "Bezier precisa de 4 + 3n pontos\nEx: 4, 7, 10, 13...")
                return
        elif tipo == "bspline":
            if len(pontos) < 4:
                messagebox.showerror(
                    "Erro",
                    "B-Spline precisa de no mínimo 4 pontos"
                )
                return

        novo_objeto = objeto(nome, tipo, pontos, self.cor)
        self.master.display_file.append(novo_objeto)
        self.master.atualizar_listbox()
        self.master.desenhar_objetos()
        self.destroy()