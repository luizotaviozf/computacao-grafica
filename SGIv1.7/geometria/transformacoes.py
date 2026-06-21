import math

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

def aplicar_transformacao(self, obj, matriz):
    novos_pontos = []

    for (x, y) in obj.pontos:
        ponto = [x, y, 1]

        x_novo = matriz[0][0]*ponto[0] + matriz[0][1]*ponto[1] + matriz[0][2]
        y_novo = matriz[1][0]*ponto[0] + matriz[1][1]*ponto[1] + matriz[1][2]

        novos_pontos.append((x_novo, y_novo))

    obj.pontos = novos_pontos