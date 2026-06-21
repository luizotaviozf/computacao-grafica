class DescritorOBJ:
    def __init__(self):
        self.vertex_offset = 0
    
    def descrever_objeto(self, obj):
        from objetos.objeto3d import Objeto3D
        
        linhas = []

        linhas.append(f"# tipo: {obj.tipo}")
        linhas.append(f"# cor: {obj.cor}")
        linhas.append(f"o {obj.nome}")

        indices = []

        if isinstance(obj, Objeto3D):
            # Objetos 3D
            for ponto in obj.pontos:
                linhas.append(f"v {ponto.x} {ponto.y} {ponto.z}")
                self.vertex_offset += 1
                indices.append(self.vertex_offset)
            
            # Arestas 3D
            for i, j in obj.arestas:
                linhas.append(f"l {i + 1} {j + 1}")
        else:
            # Objetos 2D
            for (x, y) in obj.pontos:
                linhas.append(f"v {x} {y} 0")
                self.vertex_offset += 1
                indices.append(self.vertex_offset)

            # arestas 2D
            if obj.tipo == "reta":
                linhas.append(f"l {indices[0]} {indices[1]}")

            elif obj.tipo == "wireframe":
                n = len(indices)
                for i in range(n):
                    a = indices[i]
                    b = indices[(i + 1) % n]
                    linhas.append(f"l {a} {b}")

            elif obj.tipo == "ponto":
                linhas.append(f"l {indices[0]} {indices[0]}")
            
            elif obj.tipo == "fill":
                n = len(indices)
                for i in range(n):
                    a = indices[i]
                    b = indices[(i + 1) % n]
                    linhas.append(f"l {a} {b}")

        return "\n".join(linhas)