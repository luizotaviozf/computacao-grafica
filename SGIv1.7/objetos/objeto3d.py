from objetos.ponto3d import Ponto3D
from geometria.transformacoes3d import aplicar_matriz_3d

class Objeto3D:
    def __init__(self, nome, pontos, arestas, cor, faces=None):
        self.nome = nome
        self.pontos = pontos
        self.arestas = arestas
        self.faces = faces if faces else []
        self.cor = cor
        self.tipo = "objeto3d"

    def aplicar_transformacao(self, matriz):
        novos_pontos = []

        for ponto in self.pontos:
            novos_pontos.append(aplicar_matriz_3d(ponto, matriz))

        self.pontos = novos_pontos

