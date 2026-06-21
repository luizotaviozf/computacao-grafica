import math

# Calcula o produto escalar de dois vetores, usado para calcular as coordenadas do ponto projetado em projeção 3D
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

# Calcula o produto vetorial de dois vetores, usado para calcular a base de visualização em projeção 3D
def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]

# Calcula a magnitude de um vetor, usado para normalização em projeção 3D
def norm(v):
    return math.sqrt(dot(v, v))

# Normaliza um vetor para ter magnitude 1
def normalize(v):
    m = norm(v)
    if m == 0:
        return [0, 0, 0]
    return [v[0] / m, v[1] / m, v[2] / m]

# Rotaciona um vetor v em torno de um eixo definido por 'axis' por um ângulo 'theta' (em radianos), usado para rotação de câmera em projeção 3D
def rotate_vector_around_axis(v, axis, theta):
    # Rodrigues' rotation formula
    axis_n = normalize(axis)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    dot_va = dot(v, axis_n)

    term1 = [v[i] * cos_t for i in range(3)]
    term2 = [axis_n[i] * dot_va * (1 - cos_t) for i in range(3)]
    cross_v_axis = cross(axis_n, v)

    return [
        term1[i] + term2[i] + cross_v_axis[i] * sin_t
        for i in range(3)
    ]

# Projeta um ponto 3D para coordenadas de tela usando projeção ortogonal, levando em conta a posição da câmera (vrp), a direção de visualização (vpn) e o vetor "up" da câmera (vup)
def projetar_ponto_ortogonal(self, ponto):
    vrp = self.window.get("vrp", [0, 0, 0])
    vpn = self.window.get("vpn", [0, 0, -1])
    vup = self.window.get("vup", [0, 1, 0])

    n = normalize(vpn)
    u = normalize(cross(vup, n))
    if u == [0, 0, 0]:
        u = normalize(cross([0, 1, 0], n))
    v = cross(n, u)

    dx = ponto.x - vrp[0]
    dy = ponto.y - vrp[1]
    dz = ponto.z - vrp[2]
    d = [dx, dy, dz]

    x_cam = dot(d, u)
    y_cam = dot(d, v)
    z_cam = dot(d, n)

    return x_cam, y_cam
