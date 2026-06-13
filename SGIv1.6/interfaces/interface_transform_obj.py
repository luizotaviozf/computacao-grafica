import tkinter as tk
import math

class interfaceTransformObj(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Transformar Objeto")
        self.geometry("400x650")
        self.transformacoes = []
        self.rotacao_tipo = tk.StringVar(value="mundo")
        self.objeto = self.master.get_objeto_selecionado()

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

        matriz = self.master.matriz_escala_centro(self.objeto, sx, sy)

        self.transformacoes.append(matriz)
        self.listbox.insert(tk.END, f"S({sx}, {sy})")

    def add_rotacao(self):
        from tkinter import messagebox

        try:
            ang = float(self.entry_ang.get())
        except:
            messagebox.showerror("Erro", "Valor inválido para ângulo")
            return

        theta = math.radians(ang)

        tipo = self.rotacao_tipo.get()
        
        if tipo == "mundo":
            matriz = self.master.matriz_rotacao(theta)

        elif tipo == "objeto":
            matriz = self.master.matriz_rotacao_centro_obj(self.objeto, theta)

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

        if not self.transformacoes:
            messagebox.showerror("Erro", "Nenhuma transformação a ser aplicada")
            return

        matriz_final = self.transformacoes[0]

        for m in self.transformacoes[1:]:
            matriz_final = self.master.multiplica_matrizes(m, matriz_final)

        self.master.aplicar_transformacao(self.objeto, matriz_final)
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