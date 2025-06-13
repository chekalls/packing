# import math
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import numpy as np
# from typing import List, Tuple, Dict

# class Shape:
#     def __init__(self, shape_type: str, dim1: float, dim2: float = None):
#         self.type = shape_type
#         self.dim1 = dim1  # Pour cercle: rayon, rectangle: largeur, triangle: côté
#         self.dim2 = dim2  # Pour rectangle: hauteur, triangle: None
        
#     def area(self) -> float:
#         if self.type == "Rectangle":
#             return self.dim1 * self.dim2
#         elif self.type == "Circle":
#             return math.pi * (self.dim1 ** 2)
#         elif self.type == "Triangle":
#             return (math.sqrt(3) / 4) * (self.dim1 ** 2)
#         return 0
    
#     def get_bounding_box(self, rotated: bool = False) -> Tuple[float, float]:
#         if self.type == "Rectangle":
#             if rotated:
#                 return (self.dim2, self.dim1)
#             return (self.dim1, self.dim2)
#         elif self.type == "Circle":
#             return (2 * self.dim1, 2 * self.dim1)
#         elif self.type == "Triangle":
#             # Triangle rectangle (plus facile à voir la rotation)
#             if rotated:
#                 return (self.dim1, self.dim1)  # Rotaté 90 degrés
#             return (self.dim1, self.dim1)  # Même boîte englobante mais orientation différente
#         return (0, 0)

# class BinPacker2D:
#     def __init__(self, bin_width: float, bin_height: float):
#         self.bin_width = bin_width
#         self.bin_height = bin_height
#         self.bins = []  # Liste de bins, chaque bin est une liste d'items placés
        
#     def pack(self, shapes: List[Shape], rotation_types: List[str] = ["none", "pi/2", "pi"]) -> List[List[Tuple]]:
#         # Trier les formes par aire décroissante
#         sorted_shapes = sorted(shapes, key=lambda s: s.area(), reverse=True)
        
#         for shape in sorted_shapes:
#             placed = False
            
#             # Essayer de placer la forme dans un bin existant
#             for bin_idx, bin in enumerate(self.bins):
#                 # Essayer différentes rotations
#                 for rotation in rotation_types:
#                     if rotation == "none":
#                         rotated = False
#                         w, h = shape.get_bounding_box()
#                     elif rotation == "pi/2" and shape.type == "Rectangle":
#                         rotated = True
#                         w, h = shape.get_bounding_box(rotated=True)
#                     elif rotation == "pi" and shape.type in ["Triangle"]:
#                         rotated = True
#                         w, h = shape.get_bounding_box()
#                     else:
#                         continue
                    
#                     # Trouver une position valide
#                     position = self.find_position(bin, w, h)
#                     if position:
#                         x, y = position
#                         bin.append((x, y, w, h, {"type": shape.type, "dim1": shape.dim1, "dim2": shape.dim2}, rotated))
#                         placed = True
#                         break
                
#                 if placed:
#                     break
            
#             # Si non placé, créer un nouveau bin
#             if not placed:
#                 new_bin = []
#                 for rotation in rotation_types:
#                     if rotation == "none":
#                         rotated = False
#                         w, h = shape.get_bounding_box()
#                     elif rotation == "pi/2" and shape.type == "Rectangle":
#                         rotated = True
#                         w, h = shape.get_bounding_box(rotated=True)
#                     elif rotation == "pi" and shape.type in ["Triangle"]:
#                         rotated = True
#                         w, h = shape.get_bounding_box()
#                     else:
#                         continue
                    
#                     if w <= self.bin_width and h <= self.bin_height:
#                         new_bin.append((0, 0, w, h, {"type": shape.type, "dim1": shape.dim1, "dim2": shape.dim2}, rotated))
#                         self.bins.append(new_bin)
#                         placed = True
#                         break
                
#                 if not placed:
#                     print(f"Warning: Shape {shape.type} of size {shape.dim1}x{shape.dim2} is too large for the bin.")
        
#         return self.bins
    
#     def find_position(self, bin: List[Tuple], w: float, h: float) -> Tuple[float, float]:
#         # Implémentation simple: cherche la première position disponible (stratégie first-fit)
#         # On pourrait améliorer avec des algorithmes plus sophistiqués comme Guillotine ou Shelf
        
#         # Essayer en haut à droite des formes existantes
#         for item in bin:
#             x, y, iw, ih, _, _ = item
#             # Essayer à droite
#             new_x = x + iw
#             new_y = y
#             if new_x + w <= self.bin_width and new_y + h <= self.bin_height:
#                 if not self.overlaps(bin, new_x, new_y, w, h):
#                     return (new_x, new_y)
#             # Essayer en haut
#             new_x = x
#             new_y = y + ih
#             if new_x + w <= self.bin_width and new_y + h <= self.bin_height:
#                 if not self.overlaps(bin, new_x, new_y, w, h):
#                     return (new_x, new_y)
        
#         # Essayer dans les coins vides
#         for x in [0, self.bin_width - w]:
#             for y in [0, self.bin_height - h]:
#                 if x >= 0 and y >= 0 and not self.overlaps(bin, x, y, w, h):
#                     return (x, y)
        
#         return None
    
#     def overlaps(self, bin: List[Tuple], x: float, y: float, w: float, h: float) -> bool:
#         # Vérifie si le nouvel item chevauche un item existant
#         for item in bin:
#             ix, iy, iw, ih, shape, _ = item
#             if self.rect_overlap(x, y, x+w, y+h, ix, iy, ix+iw, iy+ih):
#                 return True
#         return False
    
#     @staticmethod
#     def rect_overlap(x1: float, y1: float, x2: float, y2: float, 
#                     x3: float, y3: float, x4: float, y4: float) -> bool:
#         # Vérifie si deux rectangles se chevauchent
#         return not (x2 <= x3 or x4 <= x1 or y2 <= y3 or y4 <= y1)
    
#     def visualize_packing(self, image_output: str):
#         fig, axes = plt.subplots(len(self.bins), 1, figsize=(10, 5 * len(self.bins)))
#         if len(self.bins) == 1:
#             axes = [axes] 

#         for idx, (ax, bin) in enumerate(zip(axes, self.bins)):
#             # Dessiner le bin
#             bin_rect = patches.Rectangle((0, 0), self.bin_width, self.bin_height,
#                                        linewidth=2, edgecolor='black', 
#                                        facecolor='lightgray', alpha=0.2)
#             ax.add_patch(bin_rect)

#             colors = plt.cm.tab20.colors

#             for i, (x, y, w, h, original_shape, rotated) in enumerate(bin):
#                 color = colors[i % len(colors)]

#                 if original_shape["type"] == "Rectangle":
#                     # Dessiner le rectangle (rotaté ou non)
#                     rect = patches.Rectangle((x, y), w, h, 
#                                            facecolor=color, edgecolor='black')
#                     ax.add_patch(rect)

#                     # Ajouter un indicateur de rotation
#                     if rotated:
#                         center_x, center_y = x + w/2, y + h/2
#                         ax.plot(center_x, center_y, 'ro', markersize=3)

#                     ax.text(x + w/2, y + h/2, 
#                            f'{original_shape["dim1"]}x{original_shape["dim2"]}' + (' (R)' if rotated else ''), 
#                            ha='center', va='center', color='black', fontsize=8)
#                 elif original_shape["type"] == "Triangle":
#                     # Dessiner un triangle rectangle avec orientation différente si rotaté
#                     if rotated:
#                         points = np.array([
#                             [x, y],
#                             [x, y + h],
#                             [x + w, y]
#                         ])
#                     else:
#                         points = np.array([
#                             [x, y],
#                             [x + w, y],
#                             [x, y + h]
#                         ])
#                     triangle = patches.Polygon(points, facecolor=color, edgecolor='black')
#                     ax.add_patch(triangle)
#                     ax.text(x + w/2, y + h/2, f'{original_shape["dim1"]}' + (' (R)' if rotated else ''), 
#                            ha='center', va='center', color='black', fontsize=8)
#                 elif original_shape["type"] == "Circle":
#                     # Dessiner un cercle
#                     circle = patches.Circle((x + w/2, y + w/2), w/2,
#                                           facecolor=color, edgecolor='black')
#                     ax.add_patch(circle)
#                     ax.text(x + w/2, y + w/2, f'{original_shape["dim1"]}', 
#                            ha='center', va='center', color='black', fontsize=8)
#             ax.set_xlim(0, self.bin_width)
#             ax.set_ylim(0, self.bin_height)
#             ax.set_title(f'Bin {idx+1} - Utilization: {sum(w*h for x,y,w,h,_,_ in bin)/(self.bin_width*self.bin_height):.1%}')
#             ax.grid(True)
#             ax.set_aspect('equal')

#         plt.tight_layout()
#         plt.savefig(image_output, dpi=120, bbox_inches='tight')
#         plt.close()

#     # def visualize_packing(self, image_output: str):
#     #     fig, axes = plt.subplots(len(self.bins), 1, figsize=(10, 5 * len(self.bins)))
#     #     if len(self.bins) == 1:
#     #         axes = [axes] 

#     #     for idx, (ax, bin) in enumerate(zip(axes, self.bins)):
#     #         # Dessiner le bin
#     #         bin_rect = patches.Rectangle((0, 0), self.bin_width, self.bin_height,
#     #                                    linewidth=2, edgecolor='black', 
#     #                                    facecolor='lightgray', alpha=0.2)
#     #         ax.add_patch(bin_rect)

#     #         colors = plt.cm.tab20.colors

#     #         for i, (x, y, w, h, original_shape, rotated) in enumerate(bin):
#     #             color = colors[i % len(colors)]

#     #             if original_shape["type"] == "Rectangle":
#     #                 # Dessiner le rectangle (rotaté ou non)
#     #                 rect = patches.Rectangle((x, y), w, h, 
#     #                                        facecolor=color, edgecolor='black')
#     #                 ax.add_patch(rect)

#     #                 # Ajouter un indicateur de rotation
#     #                 if rotated:
#     #                     center_x, center_y = x + w/2, y + h/2
#     #                     ax.plot(center_x, center_y, 'ro', markersize=3)

#     #                 ax.text(x + w/2, y + h/2, 
#     #                        f'{original_shape["dim1"]}x{original_shape["dim2"]}' + (' (R)' if rotated else ''), 
#     #                        ha='center', va='center', color='black', fontsize=8)

#     #             elif original_shape["type"] == "Triangle":
#     #                 # Dessiner un triangle équilatéral
#     #                 points = np.array([
#     #                     [x, y],
#     #                     [x + w, y],
#     #                     [x + w/2, y + h]
#     #                 ])
#     #                 triangle = patches.Polygon(points, facecolor=color, edgecolor='black')
#     #                 ax.add_patch(triangle)
#     #                 ax.text(x + w/2, y + h/2, f'{original_shape["dim1"]}', 
#     #                        ha='center', va='center', color='black', fontsize=8)

#     #             elif original_shape["type"] == "Circle":
#     #                 # Dessiner un cercle
#     #                 circle = patches.Circle((x + w/2, y + w/2), w/2,
#     #                                       facecolor=color, edgecolor='black')
#     #                 ax.add_patch(circle)
#     #                 ax.text(x + w/2, y + w/2, f'{original_shape["dim1"]}', 
#     #                        ha='center', va='center', color='black', fontsize=8)

#     #         ax.set_xlim(0, self.bin_width)
#     #         ax.set_ylim(0, self.bin_height)
#     #         ax.set_title(f'Bin {idx+1} - Utilization: {sum(w*h for x,y,w,h,_,_ in bin)/(self.bin_width*self.bin_height):.1%}')
#     #         ax.grid(True)
#     #         ax.set_aspect('equal')

#     #     plt.tight_layout()
#     #     plt.savefig(image_output, dpi=120, bbox_inches='tight')
#     #     plt.close()


# # Création d'un packer avec des bins de 10x10
# packer = BinPacker2D(10, 10)

# # Création des formes à packer
# shapes = [
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 2),
#     Shape("Triangle", 3),
#     Shape("Triangle", 3),
#     Shape("Triangle", 3),
#     Shape("Triangle", 3)
# ]

# # Packing avec rotations possibles (pi/2 pour rectangles, pi pour triangles)
# bins = packer.pack(shapes, rotation_types=["none", "pi"])
# # Visualisation
# packer.visualize_packing("packing_result.png")