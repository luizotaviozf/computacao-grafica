def compute_code(self, x, y):
        w = self.window
        code = self.INSIDE

        if x < w["xmin"]:
            code |= self.LEFT
        elif x > w["xmax"]:
            code |= self.RIGHT
        if y < w["ymin"]:
            code |= self.BOTTOM
        elif y > w["ymax"]:
            code |= self.TOP

        return code

def clip_cohen_sutherland(self, x1, y1, x2, y2):
    w = self.window

    code1 = self.compute_code(x1, y1)
    code2 = self.compute_code(x2, y2)

    while True:
        if code1 == 0 and code2 == 0:
            return x1, y1, x2, y2

        if code1 & code2:
            return None

        code_out = code1 if code1 != 0 else code2

        if code_out & self.TOP:
            x = x1 + (x2 - x1) * (w["ymax"] - y1) / (y2 - y1)
            y = w["ymax"]
        elif code_out & self.BOTTOM:
            x = x1 + (x2 - x1) * (w["ymin"] - y1) / (y2 - y1)
            y = w["ymin"]
        elif code_out & self.RIGHT:
            y = y1 + (y2 - y1) * (w["xmax"] - x1) / (x2 - x1)
            x = w["xmax"]
        elif code_out & self.LEFT:
            y = y1 + (y2 - y1) * (w["xmin"] - x1) / (x2 - x1)
            x = w["xmin"]

        if code_out == code1:
            x1, y1 = x, y
            code1 = self.compute_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = self.compute_code(x2, y2)

def clip_liang_barsky(self, x1, y1, x2, y2):
    w = self.window
    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - w["xmin"], w["xmax"] - x1,
            y1 - w["ymin"], w["ymax"] - y1]

    u1, u2 = 0, 1

    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return None
        else:
            t = qi / pi
            if pi < 0:
                u1 = max(u1, t)
            else:
                u2 = min(u2, t)

    if u1 > u2:
        return None

    return (
        x1 + u1 * dx,
        y1 + u1 * dy,
        x1 + u2 * dx,
        y1 + u2 * dy
    )

def clip_polygon(self, pontos):
    w = self.window

    def inside(p, edge):
        x, y = p
        if edge == "left":
            return x >= w["xmin"]
        elif edge == "right":
            return x <= w["xmax"]
        elif edge == "bottom":
            return y >= w["ymin"]
        elif edge == "top":
            return y <= w["ymax"]

    def intersect(p1, p2, edge):
        x1, y1 = p1
        x2, y2 = p2

        if edge == "left":
            x = w["xmin"]
            y = y1 + (y2 - y1) * (w["xmin"] - x1) / (x2 - x1)

        elif edge == "right":
            x = w["xmax"]
            y = y1 + (y2 - y1) * (w["xmax"] - x1) / (x2 - x1)

        elif edge == "bottom":
            y = w["ymin"]
            x = x1 + (x2 - x1) * (w["ymin"] - y1) / (y2 - y1)

        elif edge == "top":
            y = w["ymax"]
            x = x1 + (x2 - x1) * (w["ymax"] - y1) / (y2 - y1)

        return (x, y)

    def clip_edge(pontos, edge):
        novos = []

        for i in range(len(pontos)):
            P = pontos[i]
            Q = pontos[(i + 1) % len(pontos)]

            if inside(Q, edge):
                if not inside(P, edge):
                    novos.append(intersect(P, Q, edge))
                novos.append(Q)
            elif inside(P, edge):
                novos.append(intersect(P, Q, edge))

        return novos

    # aplica nos 4 lados
    pontos = clip_edge(pontos, "left")
    pontos = clip_edge(pontos, "right")
    pontos = clip_edge(pontos, "bottom")
    pontos = clip_edge(pontos, "top")

    return pontos

def ponto_dentro_window(self, x, y):
        w = self.window
        return (w["xmin"] <= x <= w["xmax"] and
                w["ymin"] <= y <= w["ymax"])