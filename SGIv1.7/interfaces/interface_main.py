import tkinter as tk
from tkinter import colorchooser
import math
from objetos.objeto import objeto
from EntradaSaida.carregar_obj import *
from EntradaSaida.descritor_obj import *
from geometria.clipping import *
from geometria.transformacoes import *
from geometria.viewport import *
from geometria.curvas import *
from interfaces.interface_add_obj import interfaceAddObj
from interfaces.interface_transform_obj import interfaceTransformObj
from objetos.objeto3d import Objeto3D
from objetos.ponto3d import Ponto3D
from geometria.projecao import *
from EntradaSaida.salvar_obj import *

class interfaceMain(tk.Tk):

    # definicoes que transformam as funcoes importadas em metodos da classe, assim podem ser chamados usando self.funcao() dentro da classe
    compute_code = compute_code
    clip_cohen_sutherland = clip_cohen_sutherland
    clip_liang_barsky = clip_liang_barsky
    clip_polygon = clip_polygon
    ponto_dentro_window = ponto_dentro_window
    matriz_translacao = matriz_translacao
    matriz_escala = matriz_escala
    matriz_rotacao = matriz_rotacao
    multiplica_matrizes = multiplica_matrizes
    centro_objeto = centro_objeto
    aplicar_transformacao = aplicar_transformacao
    matriz_escala_centro = matriz_escala_centro
    matriz_rotacao_centro_obj = matriz_rotacao_centro_obj
    matriz_rotacao_ponto = matriz_rotacao_ponto
    world_to_window_space = world_to_window_space
    window_to_world_space = window_to_world_space
    world_to_viewport = world_to_viewport
    centro_window = centro_window
    forward_differences = forward_differences
    gerar_bspline_forward = gerar_bspline_forward
    calcular_bezier = calcular_bezier
    projetar_ponto_ortogonal = projetar_ponto_ortogonal
    carregar_obj = carregar_obj
    salvar_obj = salvar_obj
    
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

        self.clipping_var = tk.StringVar(value="cohen")

        tk.Label(frameMenu, text="Clipping de Retas:", bg="lightgray").pack(pady=5)

        tk.Radiobutton(
            frameMenu,
            text="Cohen-Sutherland",
            variable=self.clipping_var,
            value="cohen",
            bg="lightgray"
        ).pack(anchor="w")

        tk.Radiobutton(
            frameMenu,
            text="Liang-Barsky",
            variable=self.clipping_var,
            value="liang",
            bg="lightgray"
        ).pack(anchor="w")

        self.canvas = tk.Canvas(frameCanvas, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.window = {
            "xmin": 0,
            "ymin": 0,
            "xmax": 600,
            "ymax": 600,
            "angulo": 0,
            # posicao da camera
            "vrp": [0, 0, 500],
            # direcao de visualizacao
            "vpn": [0, 0, -1],
            # vetor "up" da camera, usado para calcular a base de visualizacao
            "vup": [0, 1, 0]
        }

        self.viewport = {
            "xmin": 50,
            "ymin": 50,
            "xmax": 550,
            "ymax": 550
        }

        self.INSIDE = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.BOTTOM = 4
        self.TOP = 8

        # Windows/Mac
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        # Linux
        self.canvas.bind("<Button-4>", self.on_zoom)
        self.canvas.bind("<Button-5>", self.on_zoom)

        self.bind("<Left>", lambda e: self.pan(-10, 0))
        self.bind("<Right>", lambda e: self.pan(10, 0))
        self.bind("<Up>", lambda e: self.pan(0, 10))
        self.bind("<Down>", lambda e: self.pan(0, -10))

        self.bind("q", lambda e: self.rotacionar_window(10))
        self.bind("e", lambda e: self.rotacionar_window(-10))
        
        self.bind("a", lambda e: self.yaw(10))
        self.bind("d", lambda e: self.yaw(-10))

        frame_lista = tk.Frame(frameMenu)
        frame_lista.pack(pady=5,padx=5)
        scroll = tk.Scrollbar(frame_lista)
        scroll.pack(side="right", fill="y")
        self.listbox = tk.Listbox(frame_lista, yscrollcommand=scroll.set)
        self.listbox.pack(fill="both")
        scroll.config(command=self.listbox.yview)
        
        tk.Label(
            frameMenu,
            text=(
                "Panning: setas do teclado\n"
                "Zoom: scroll do mouse (ou W/S)\n"
                "Rotação (roll): Q / E\n"
                "Mover VRP (zoom axial): W / S\n"
                "Yaw (girar câmera): A / D"
            ),
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

        tk.Button(frameMenu, text="Salvar .obj", command=self.salvar_obj).pack(pady=5)
        tk.Button(frameMenu, text="Carregar .obj", command=self.carregar_obj).pack(pady=5)

        self.after(100, self.desenhar_objetos)
        self.after(100, self.atualizar_label_window)
        self.focus_set()

    def mult_matriz_vetor(self, M, V):
        resultado = []

        for linha in M:
            soma = 0

            for j in range(4):
                soma += linha[j] * V[j]

            resultado.append(soma)

        return resultado

    def atualizar_label_window(self):
        w = self.window

        ang_graus = math.degrees(w.get("angulo", 0))

        texto = (
            f"Window:\n"
            f"xmin: {w['xmin']:.2f}\n"
            f"ymin: {w['ymin']:.2f}\n"
            f"xmax: {w['xmax']:.2f}\n"
            f"ymax: {w['ymax']:.2f}\n"
            f"ângulo: {ang_graus:.2f}°"
        )
        self.label_window.config(text=texto)

    # -------------------- CÂMERA --------------------
    def camera_basis(self):
        vpn = self.window.get("vpn", [0, 0, -1])
        vup = self.window.get("vup", [0, 1, 0])

        n = normalize(vpn)
        u = normalize(cross(vup, n))
        if u == [0, 0, 0]:
            u = normalize(cross([0, 1, 0], n))
        v = cross(n, u)
        return u, v, n

    def pan(self, dx, dy):
        # move VRP in camera's u/v plane
        u, v, n = self.camera_basis()
        self.window["vrp"][0] += dx * u[0] + dy * v[0]
        self.window["vrp"][1] += dx * u[1] + dy * v[1]
        self.window["vrp"][2] += dx * u[2] + dy * v[2]

        self.desenhar_objetos()
        self.atualizar_label_window()

    def rotacionar_window(self, ang_graus):
        # roll around view axis (n)
        theta = math.radians(ang_graus)
        n = self.camera_basis()[2]
        self.window["vpn"] = rotate_vector_around_axis(self.window["vpn"], n, theta)
        self.window["vup"] = rotate_vector_around_axis(self.window["vup"], n, theta)

        self.desenhar_objetos()
        self.atualizar_label_window()

    def yaw(self, ang_graus):
        # rotate camera left/right around VUP (approximate yaw)
        theta = math.radians(ang_graus)
        vup = self.window.get("vup", [0, 1, 0])
        self.window["vpn"] = rotate_vector_around_axis(self.window["vpn"], vup, theta)

        self.desenhar_objetos()
        self.atualizar_label_window()

    def zoom(self, fator):
        # keep orthographic: scale window extents
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

    def desenhar_objetos(self):
        self.canvas.delete("all")

        vp = self.viewport
        self.canvas.create_rectangle(
            vp["xmin"], vp["ymin"],
            vp["xmax"], vp["ymax"],
            outline="black", width=2
        )

        for obj in self.display_file:
            if obj.tipo == "ponto":
                if obj.tipo == "ponto":
                    x, y = obj.pontos[0]

                    xw, yw = self.world_to_window_space(x, y)

                    if not (self.window["xmin"] <= xw <= self.window["xmax"] and
                            self.window["ymin"] <= yw <= self.window["ymax"]):
                        continue

                    xf, yf = self.window_to_world_space(xw, yw)

                    xv, yv = self.world_to_viewport(xf, yf)
                    r = 3
                    self.canvas.create_oval(xv - r, yv - r, xv + r, yv + r, fill=obj.cor)

            elif obj.tipo == "reta":
                if len(obj.pontos) < 2:
                    continue
                (x1, y1), (x2, y2) = obj.pontos

                x1w, y1w = self.world_to_window_space(x1, y1)
                x2w, y2w = self.world_to_window_space(x2, y2)

                if self.clipping_var.get() == "cohen":
                    resultado = self.clip_cohen_sutherland(x1w, y1w, x2w, y2w)
                else:
                    resultado = self.clip_liang_barsky(x1w, y1w, x2w, y2w)
                if resultado is None:
                    continue

                x1c, y1c, x2c, y2c = resultado

                x1f, y1f = self.window_to_world_space(x1c, y1c)
                x2f, y2f = self.window_to_world_space(x2c, y2c)
                x1v, y1v = self.world_to_viewport(x1f, y1f)
                x2v, y2v = self.world_to_viewport(x2f, y2f)
                self.canvas.create_line(x1v, y1v, x2v, y2v, fill=obj.cor)

            elif obj.tipo == "wireframe":
                n = len(obj.pontos)
                for i in range(n):
                    (x1, y1) = obj.pontos[i]
                    (x2, y2) = obj.pontos[(i + 1) % n]
                    x1w, y1w = self.world_to_window_space(x1, y1)
                    x2w, y2w = self.world_to_window_space(x2, y2)
                    if self.clipping_var.get() == "cohen":
                        resultado = self.clip_cohen_sutherland(x1w, y1w, x2w, y2w)
                    else:
                        resultado = self.clip_liang_barsky(x1w, y1w, x2w, y2w)
                    if resultado is None:
                        continue
                    x1c, y1c, x2c, y2c = resultado
                    x1f, y1f = self.window_to_world_space(x1c, y1c)
                    x2f, y2f = self.window_to_world_space(x2c, y2c)
                    x1v, y1v = self.world_to_viewport(x1f, y1f)
                    x2v, y2v = self.world_to_viewport(x2f, y2f)
                    self.canvas.create_line(x1v, y1v, x2v, y2v, fill=obj.cor)
            elif obj.tipo == "fill":
                pontos_w = [self.world_to_window_space(x, y) for x, y in obj.pontos]
                pontos_clip = self.clip_polygon(pontos_w)

                if len(pontos_clip) < 3:
                    continue
                pontos_mundo = [self.window_to_world_space(x, y) for x, y in pontos_clip]
                pontos_vp = [self.world_to_viewport(x, y) for x, y in pontos_mundo]
                self.canvas.create_polygon(
                    pontos_vp,
                    fill=obj.cor,
                    outline=obj.cor
                )
            elif obj.tipo == "bezier":
                pontos_curva = []

                for i in range(0, len(obj.pontos) - 3, 3):
                    p0 = obj.pontos[i]
                    p1 = obj.pontos[i + 1]
                    p2 = obj.pontos[i + 2]
                    p3 = obj.pontos[i + 3]

                    trecho = self.calcular_bezier(p0, p1, p2, p3)

                    if i != 0:
                        trecho = trecho[1:]

                    pontos_curva.extend(trecho)

                for i in range(len(pontos_curva) - 1):
                    x1, y1 = pontos_curva[i]
                    x2, y2 = pontos_curva[i + 1]

                    x1w, y1w = self.world_to_window_space(x1, y1)
                    x2w, y2w = self.world_to_window_space(x2, y2)

                    if self.clipping_var.get() == "cohen":
                        resultado = self.clip_cohen_sutherland(
                            x1w, y1w, x2w, y2w
                        )
                    else:
                        resultado = self.clip_liang_barsky(
                            x1w, y1w, x2w, y2w
                        )

                    if resultado is None:
                        continue

                    x1c, y1c, x2c, y2c = resultado

                    x1f, y1f = self.window_to_world_space(x1c, y1c)
                    x2f, y2f = self.window_to_world_space(x2c, y2c)

                    x1v, y1v = self.world_to_viewport(x1f, y1f)
                    x2v, y2v = self.world_to_viewport(x2f, y2f)

                    self.canvas.create_line(
                        x1v, y1v,
                        x2v, y2v,
                        fill=obj.cor
                    )
            elif obj.tipo == "bspline":

                pontos_curva = self.gerar_bspline_forward(
                    obj.pontos,
                    delta=0.01
                )

                for i in range(len(pontos_curva) - 1):

                    x1, y1 = pontos_curva[i]
                    x2, y2 = pontos_curva[i + 1]

                    x1w, y1w = self.world_to_window_space(x1, y1)
                    x2w, y2w = self.world_to_window_space(x2, y2)

                    if self.clipping_var.get() == "cohen":
                        resultado = self.clip_cohen_sutherland(
                            x1w, y1w, x2w, y2w
                        )
                    else:
                        resultado = self.clip_liang_barsky(
                            x1w, y1w, x2w, y2w
                        )

                    if resultado is None:
                        continue

                    x1c, y1c, x2c, y2c = resultado

                    x1f, y1f = self.window_to_world_space(x1c, y1c)
                    x2f, y2f = self.window_to_world_space(x2c, y2c)

                    x1v, y1v = self.world_to_viewport(x1f, y1f)
                    x2v, y2v = self.world_to_viewport(x2f, y2f)

                    self.canvas.create_line(
                        x1v, y1v,
                        x2v, y2v,
                        fill=obj.cor
                    )
            elif obj.tipo == "objeto3d":
                for i, j in obj.arestas:
                    p1 = obj.pontos[i]
                    p2 = obj.pontos[j]
                    self.desenhar_linha_3d(p1, p2, obj.cor)

    def desenhar_linha_3d(self, p1, p2, cor):
        x1, y1 = self.projetar_ponto_ortogonal(p1)
        x2, y2 = self.projetar_ponto_ortogonal(p2)

        x1, y1 = self.world_to_window_space(x1, y1)
        x2, y2 = self.world_to_window_space(x2, y2)

        if self.clipping_var.get() == "cohen":
            resultado = self.clip_cohen_sutherland(x1, y1, x2, y2)
        else:
            resultado = self.clip_liang_barsky(x1, y1, x2, y2)

        if resultado is None:
            return

        x1, y1, x2, y2 = resultado

        x1, y1 = self.window_to_world_space(x1, y1)
        x2, y2 = self.window_to_world_space(x2, y2)

        x1, y1 = self.world_to_viewport(x1, y1)
        x2, y2 = self.world_to_viewport(x2, y2)

        self.canvas.create_line(x1, y1, x2, y2, fill=cor)

    def add_object(self):
        interfaceAddObj(self, "Adicionar Objeto", 400, 700)

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
            if isinstance(obj, Objeto3D):
                texto = f"{obj.nome} (3D) [{obj.cor}]"
            else:
                texto = f"{obj.nome} ({obj.tipo}) [{obj.cor}]"
            self.listbox.insert(tk.END, texto)

    def get_objeto_selecionado(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return self.display_file[sel[0]]
    
    def transform_object(self):
        if self.get_objeto_selecionado() is None:
            from tkinter import messagebox
            messagebox.showerror("Erro", "Selecione um objeto para transformar")
            return
        interfaceTransformObj(self)