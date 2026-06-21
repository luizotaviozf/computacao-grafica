from objetos.objeto import objeto
from objetos.objeto3d import Objeto3D
from objetos.ponto3d import Ponto3D

def carregar_obj(self):
        from tkinter import filedialog

        caminho = filedialog.askopenfilename(filetypes=[("OBJ", "*.obj")])
        if not caminho:
            return

        self.display_file.clear()

        with open(caminho, "r") as f:
            linhas = f.readlines()

        nome = None
        pontos = []
        pontos3d = []
        arestas = []
        tipo = "wireframe"
        cor = "black"

        tipo_atual = "wireframe"
        cor_atual = "black"
        vertex_count = 0

        for linha in linhas:
            partes = linha.strip().split()
            if not partes:
                continue

            # ---------------- COMENTÁRIOS ----------------
            if partes[0] == "#":
                linha_str = linha.strip()

                if "tipo:" in linha_str:
                    tipo_atual = linha_str.split("tipo:")[1].strip()

                elif "cor:" in linha_str:
                    cor_atual = linha_str.split("cor:")[1].strip()

            # ---------------- NOVO OBJETO ----------------
            elif partes[0] == "o":

                # salva anterior
                if nome:
                    if tipo_atual == "objeto3d":
                        if len(pontos3d) >= 4:
                            novo_obj = Objeto3D(nome, pontos3d, arestas, cor)
                            self.display_file.append(novo_obj)
                    else:
                        pontos_validos = pontos.copy()

                        if tipo == "ponto":
                            pontos_validos = pontos_validos[:1]

                        elif tipo == "reta":
                            if len(pontos_validos) >= 2:
                                pontos_validos = pontos_validos[:2]
                            else:
                                pontos_validos = []

                        elif tipo == "wireframe" or tipo == "fill":
                            if len(pontos_validos) < 3:
                                pontos_validos = []
                        
                        elif tipo == "bezier":
                            if len(pontos_validos) < 4:
                                pontos_validos = []

                        elif tipo == "bspline":
                            if len(pontos_validos) < 4:
                                pontos_validos = []

                        if pontos_validos:
                            self.display_file.append(objeto(nome, tipo, pontos_validos, cor))

                # inicia novo
                nome = partes[1]
                pontos = []
                pontos3d = []
                arestas = []
                tipo = tipo_atual
                cor = cor_atual
                vertex_count = 0

            # ---------------- VÉRTICES ----------------
            elif partes[0] == "v":
                if tipo_atual == "objeto3d":
                    x = float(partes[1])
                    y = float(partes[2])
                    z = float(partes[3]) if len(partes) > 3 else 0
                    pontos3d.append(Ponto3D(x, y, z))
                else:
                    x = float(partes[1])
                    y = float(partes[2])
                    pontos.append((x, y))
                vertex_count += 1

            # ---------------- ARESTAS ----------------
            elif partes[0] == "l":
                if tipo_atual == "objeto3d" and len(partes) >= 3:
                    i = int(partes[1]) - 1
                    j = int(partes[2]) - 1
                    arestas.append((i, j))

        # ---------------- ÚLTIMO OBJETO ----------------
        if nome:
            if tipo_atual == "objeto3d":
                if len(pontos3d) >= 4:
                    novo_obj = Objeto3D(nome, pontos3d, arestas, cor)
                    self.display_file.append(novo_obj)
            else:
                pontos_validos = pontos.copy()

                if tipo == "ponto":
                    pontos_validos = pontos_validos[:1]

                elif tipo == "reta":
                    if len(pontos_validos) >= 2:
                        pontos_validos = pontos_validos[:2]
                    else:
                        pontos_validos = []

                elif tipo == "wireframe" or tipo == "fill":
                    if len(pontos_validos) < 3:
                        pontos_validos = []

                if pontos_validos:
                    self.display_file.append(objeto(nome, tipo, pontos_validos, cor))

        self.atualizar_listbox()
        self.desenhar_objetos()