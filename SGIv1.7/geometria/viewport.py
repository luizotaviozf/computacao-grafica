import math

def world_to_window_space(self, x, y):
    w = self.window

    cx, cy = self.centro_window()

    xt = x - cx
    yt = y - cy

    ang = -w["angulo"]

    xr = xt * math.cos(ang) - yt * math.sin(ang)
    yr = xt * math.sin(ang) + yt * math.cos(ang)

    # volta
    xr += cx
    yr += cy

    return xr, yr

def window_to_world_space(self, x, y):
    w = self.window

    cx, cy = self.centro_window()

    xt = x - cx
    yt = y - cy

    ang = w["angulo"]  # agora positivo

    xr = xt * math.cos(ang) - yt * math.sin(ang)
    yr = xt * math.sin(ang) + yt * math.cos(ang)

    xr += cx
    yr += cy

    return xr, yr

def world_to_viewport(self, x, y):

    w = self.window
    vp = self.viewport

    self.update_idletasks()
    vw = self.canvas.winfo_width()
    vh = self.canvas.winfo_height()

    cx, cy = self.centro_window()

    xt = x - cx
    yt = y - cy

    ang = -w["angulo"]
    xr = xt * math.cos(ang) - yt * math.sin(ang)
    yr = xt * math.sin(ang) + yt * math.cos(ang)

    xr += cx
    yr += cy

    xn = (xr - w["xmin"]) / (w["xmax"] - w["xmin"])
    yn = (yr - w["ymin"]) / (w["ymax"] - w["ymin"])

    xv = vp["xmin"] + xn * (vp["xmax"] - vp["xmin"])
    yv = vp["ymax"] - yn * (vp["ymax"] - vp["ymin"])

    return xv, yv

def centro_window(self):
    w = self.window
    cx = (w["xmin"] + w["xmax"]) / 2
    cy = (w["ymin"] + w["ymax"]) / 2
    return cx, cy