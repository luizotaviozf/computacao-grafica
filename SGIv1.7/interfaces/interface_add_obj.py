import tkinter as tk
from tkinter import colorchooser
from objetos import objeto3d
from objetos.objeto import objeto
from objetos.ponto3d import Ponto3D
from objetos.objeto3d import Objeto3D

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
        tk.Radiobutton(self, text="Objeto3D", variable=self.tipo_var, value="objeto3d", command=self.atualizar_interface_tipo).pack()

        self.label_bezier = tk.Label(self, text="Bezier e B-Spline (formato):")
        self.label_bezier.pack(pady=5)
        self.entry_bezier = tk.Entry(self, width=40)
        self.entry_bezier.pack()
        self.label_exemplo_bezier = tk.Label(self, text="Ex: (10,20),(50,80),(100,30),(150,90)", font=("Arial", 8))
        self.label_exemplo_bezier.pack()

        # pontos 2d
        self.frame_pontos = tk.Frame(self)
        tk.Label(self.frame_pontos, text="Pontos:").pack(pady=5)
        tk.Label(self.frame_pontos, text="X:").pack()
        self.entry_x = tk.Entry(self.frame_pontos)
        self.entry_x.pack()
        tk.Label(self.frame_pontos, text="Y:").pack()
        self.entry_y = tk.Entry(self.frame_pontos)
        self.entry_y.pack()

        # pontos 3d
        self.frame_pontos3d = tk.Frame(self)
        tk.Label(self.frame_pontos3d, text="Pontos:").pack(pady=5)
        tk.Label(self.frame_pontos3d, text="X:").pack()
        self.entry_x3d = tk.Entry(self.frame_pontos3d)
        self.entry_x3d.pack()
        tk.Label(self.frame_pontos3d, text="Y:").pack()
        self.entry_y3d = tk.Entry(self.frame_pontos3d)
        self.entry_y3d.pack()
        tk.Label(self.frame_pontos3d, text="Z:").pack()
        self.entry_z3d = tk.Entry(self.frame_pontos3d)
        self.entry_z3d.pack()

        # botões adicionar ponto
        self.btn_add_ponto3d = tk.Button(self.frame_pontos3d, text="Adicionar ponto", command=self.add_ponto3d)
        self.btn_add_ponto3d.pack(pady=5)
        self.btn_add_ponto = tk.Button(self, text="Adicionar ponto", command=self.add_ponto)
        self.btn_add_ponto.pack(pady=5)

        # lista pontos 2d
        frame_lista = tk.Frame(self)
        self.frame_lista = frame_lista
        frame_lista.pack(pady=10)
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox_pontos = tk.Listbox(frame_lista, height=5, yscrollcommand=scroll.set)
        self.listbox_pontos.pack(side="left")
        scroll.config(command=self.listbox_pontos.yview)

        # lista pontos 3d
        frame_lista3d = tk.Frame(self)
        self.frame_lista3d = frame_lista3d
        frame_lista3d.pack(pady=10)
        scroll3d = tk.Scrollbar(frame_lista3d)
        scroll3d.pack(side="right", fill="y")
        self.listbox_pontos3d = tk.Listbox(frame_lista3d, height=5, yscrollcommand=scroll3d.set)
        self.listbox_pontos3d.pack(side="left")
        scroll.config(command=self.listbox_pontos3d.yview)

        # botões remover ponto
        self.btn_remover_ponto3d = tk.Button(self, text="Remover ponto", command=self.remover_ponto3d)
        self.btn_remover_ponto3d.pack(pady=5)
        self.btn_remover_ponto = tk.Button(self, text="Remover ponto", command=self.remover_ponto)
        self.btn_remover_ponto.pack(pady=5)

        self.btn_salvar = tk.Button(self, text="Salvar", command=self.save_object)
        self.btn_salvar.pack(pady=10)

        self.atualizar_interface_tipo()

    def atualizar_interface_tipo(self):
        tipo = self.tipo_var.get()

        # esconde tudo primeiro
        self.frame_pontos.pack_forget()
        self.frame_pontos3d.pack_forget()
        self.label_bezier.pack_forget()
        self.entry_bezier.pack_forget()
        self.label_exemplo_bezier.pack_forget()
        self.btn_add_ponto.pack_forget()
        self.btn_remover_ponto.pack_forget()
        self.frame_lista.pack_forget()
        self.frame_lista3d.pack_forget()
        self.btn_add_ponto3d.pack_forget()
        self.btn_remover_ponto3d.pack_forget()

        # mostra o necessário
        if tipo == "objeto3d":
            self.frame_pontos3d.pack(fill="x",padx=10,pady=5)
            self.btn_add_ponto3d.pack(pady=5)
            self.frame_lista3d.pack(pady=10)
            self.btn_remover_ponto3d.pack(pady=5)
        elif tipo in ["bezier", "bspline"]:
            self.label_bezier.pack(pady=5)
            self.entry_bezier.pack()
            self.label_exemplo_bezier.pack()
        else:
            self.frame_pontos.pack(fill="x",padx=10,pady=5)
            self.btn_add_ponto.pack(pady=5)
            self.frame_lista.pack(pady=10)
            self.btn_remover_ponto.pack(pady=5)

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

    def add_ponto3d(self):
        from tkinter import messagebox

        tipo = self.tipo_var.get()
        if tipo == "objeto3d" and len(self.pontos) >= 1000:
            messagebox.showerror("Erro", "Limite de pontos para objeto3d é 1000")
            return

        try:
            x = float(self.entry_x3d.get())
            y = float(self.entry_y3d.get())
            z = float(self.entry_z3d.get())

            self.pontos.append(Ponto3D(x, y, z))
            self.listbox_pontos3d.insert(tk.END, f"({x}, {y}, {z})")

            self.entry_x3d.delete(0, tk.END)
            self.entry_y3d.delete(0, tk.END)
            self.entry_z3d.delete(0, tk.END)
        except:
            messagebox.showerror("Erro", "Coordenadas inválidas")

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
    
    def remover_ponto3d(self):
        sel = self.listbox_pontos3d.curselection()
        if sel:
            index = sel[0]
            self.listbox_pontos3d.delete(index)
            self.pontos.pop(index)

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
        
        if tipo == "objeto3d":
            if len(self.pontos) < 4:
                messagebox.showerror("Erro", "Objeto3D precisa de no mínimo 4 pontos")
                return
            
            arestas = [(i, i+1) for i in range(len(self.pontos)-1)]
            novo_objeto = Objeto3D(nome, self.pontos, arestas, self.cor)
            self.master.display_file.append(novo_objeto)
            self.master.atualizar_listbox()
            self.master.desenhar_objetos()
            self.destroy()
            return

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