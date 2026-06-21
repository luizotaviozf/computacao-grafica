import math
from objetos.ponto3d import Ponto3D

def matriz_translacao_3d(dx, dy, dz):
    return [
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ]

def matriz_escala_3d(sx, sy, sz):
    return [
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ]

def matriz_rotacao_x(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    return [
        [1, 0, 0, 0],
        [0, cos, -sin, 0],
        [0, sin, cos, 0],
        [0, 0, 0, 1]
    ]

def matriz_rotacao_y(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    return [
        [cos, 0, sin, 0],
        [0, 1, 0, 0],
        [-sin, 0, cos, 0],
        [0, 0, 0, 1]
    ]

def matriz_rotacao_z(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    return [
        [cos, -sin, 0, 0],
        [sin, cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def multiplica_matrizes_3d(A, B):
    resultado = [[0]*4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                resultado[i][j] += A[i][k] * B[k][j]

    return resultado

def aplicar_matriz_3d(ponto, matriz):
    vetor = [ponto.x, ponto.y, ponto.z, 1]
    resultado = [0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            resultado[i] += matriz[i][j] * vetor[j]

    return Ponto3D(resultado[0], resultado[1], resultado[2])