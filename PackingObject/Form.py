import tkinter as tk
import math

class Form:
    def __init__(self):
        self.rotation = 0.0  # en radians
        self.x, self.y = 0.0, 0.0
        self.form = "T"
        self.size = {"w": 100, "h": 100}  # taille par défaut

    def setType(self, formName: str):
        self.form = formName

    def getType(self):
        return self.form

    def setSizing(self, size: dict):
        self.size = size

    def getSize(self):
        return self.size

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def getPosition(self):
        return self.x, self.y

    def setRotation(self, value):  # en radians
        self.rotation = value

    def _rotate_point(self, px, py, cx, cy, angle_rad):
        dx = px - cx
        dy = py - cy
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rx = cx + cos_a * dx - sin_a * dy
        ry = cy + sin_a * dx + cos_a * dy
        return rx, ry

    def draw(self, canvas: tk.Canvas):
        if self.form == "T":
            self._draw_triangle(canvas)
        elif self.form == "R":
            self._draw_rectangle(canvas)
        elif self.form == "C":
            self._draw_circle(canvas)

 
    def _draw_triangle(self, canvas):
        w = self.size.get("w", 100)
        h = self.size.get("h", 100)
    
        # Centre du rectangle
        cx = self.x + w / 2
        cy = self.y + h / 2
    
        # Triangle isocèle centré sur (cx, cy)
        p1 = (cx, cy - h / 2)      # sommet haut
        p2 = (cx - w / 2, cy + h / 2)  # bas gauche
        p3 = (cx + w / 2, cy + h / 2)  # bas droit
    
        points = [p1, p2, p3]
        rotated = [self._rotate_point(px, py, cx, cy, self.rotation) for px, py in points]
        flat = [coord for pt in rotated for coord in pt]
    
        canvas.create_polygon(flat, fill="lightblue", outline="black", width=2)

    def _draw_rectangle(self, canvas):
        w = self.size.get("w", 100)
        h = self.size.get("h", 100)

        # Points non-rotés du rectangle (sens horaire)
        p1 = (self.x - w / 2, self.y - h / 2)
        p2 = (self.x + w / 2, self.y - h / 2)
        p3 = (self.x + w / 2, self.y + h / 2)
        p4 = (self.x - w / 2, self.y + h / 2)

        cx, cy = self.x, self.y

        points = [p1, p2, p3, p4]
        rotated = [self._rotate_point(px, py, cx, cy, self.rotation) for px, py in points]
        flat = [coord for pt in rotated for coord in pt]

        canvas.create_polygon(flat, fill="lightgreen", outline="black", width=2)

    def _draw_circle(self, canvas):
        d = self.size.get("d", 100)
        r = d / 2

        # Comme on ne peut pas dessiner un cercle tourné (il reste un cercle),
        # on ignore la rotation ici
        x0 = self.x - r
        y0 = self.y - r
        x1 = self.x + r
        y1 = self.y + r

        canvas.create_oval(x0, y0, x1, y1, fill="salmon", outline="black", width=2)
