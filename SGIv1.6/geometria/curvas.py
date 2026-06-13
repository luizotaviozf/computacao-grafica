def forward_differences(self, Cx, Cy, delta):
    pontos = []

    ax, bx, cx, dx = Cx
    ay, by, cy, dy = Cy

    x = dx
    y = dy

    dx1 = ax * delta ** 3 + bx * delta ** 2 + cx * delta
    dy1 = ay * delta ** 3 + by * delta ** 2 + cy * delta

    dx2 = 6 * ax * delta ** 3 + 2 * bx * delta ** 2
    dy2 = 6 * ay * delta ** 3 + 2 * by * delta ** 2

    dx3 = 6 * ax * delta ** 3
    dy3 = 6 * ay * delta ** 3

    passos = int(1 / delta)

    for _ in range(passos + 1):
        pontos.append((x, y))

        x += dx1
        y += dy1

        dx1 += dx2
        dy1 += dy2

        dx2 += dx3
        dy2 += dy3

    return pontos

def gerar_bspline_forward(self, pontos_controle, delta=0.01):

    pontos_curva = []

    n = len(pontos_controle)

    Mbs = [
        [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
        [3 / 6, -6 / 6, 3 / 6, 0],
        [-3 / 6, 0, 3 / 6, 0],
        [1 / 6, 4 / 6, 1 / 6, 0]
    ]

    for i in range(n - 3):

        Gx = [
            pontos_controle[i][0],
            pontos_controle[i + 1][0],
            pontos_controle[i + 2][0],
            pontos_controle[i + 3][0]
        ]

        Gy = [
            pontos_controle[i][1],
            pontos_controle[i + 1][1],
            pontos_controle[i + 2][1],
            pontos_controle[i + 3][1]
        ]

        Cx = self.mult_matriz_vetor(Mbs, Gx)
        Cy = self.mult_matriz_vetor(Mbs, Gy)

        trecho = self.forward_differences(
            Cx,
            Cy,
            delta
        )

        if i != 0:
            trecho = trecho[1:]

        pontos_curva.extend(trecho)

    return pontos_curva

def calcular_bezier(self, p0, p1, p2, p3, passos=100):
    pontos = []

    for i in range(passos + 1):
        t = i / passos

        x = (
            (1 - t) ** 3 * p0[0] +
            3 * (1 - t) ** 2 * t * p1[0] +
            3 * (1 - t) * t ** 2 * p2[0] +
            t ** 3 * p3[0]
        )

        y = (
            (1 - t) ** 3 * p0[1] +
            3 * (1 - t) ** 2 * t * p1[1] +
            3 * (1 - t) * t ** 2 * p2[1] +
            t ** 3 * p3[1]
        )

        pontos.append((x, y))

    return pontos