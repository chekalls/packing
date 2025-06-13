import tkinter as tk
from tkinter import messagebox
import random
from tkinter import ttk
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BinPackingApp:
    def ffdh_2d_packing(self,rectangles, bin_width, bin_height):
        # Trier les rectangles par hauteur décroissante, puis largeur décroissante
            sorted_rects = sorted(rectangles, key=lambda x: (-x[1], -x[0]))

            bins = []  # Chaque bin contient des niveaux (y, height, used_width, rectangles)

            for w, h in sorted_rects:
                if w > bin_width or h > bin_height:
                    print(f"Rectangle {w}x{h} ignoré (trop grand)")
                    continue

                placed = False

                # Chercher dans les bins existants (First-Fit)
                for bin in bins:
                    # Parcourir tous les niveaux dans ce bin
                    for level in bin:
                        y, level_h, used_w, level_rects = level
                        remaining_width = bin_width - used_w

                        # Vérifier si le rectangle rentre dans ce niveau
                        if w <= remaining_width and h <= level_h:
                            # Placer le rectangle
                            level_rects.append((used_w, y, w, h))
                            level[2] += w  # Mettre à jour la largeur utilisée
                            placed = True
                            break
                        
                    if placed:
                        break
                    
                # Si non placé, essayer de créer un nouveau niveau
                if not placed:
                    # Chercher dans les bins existants pour un nouvel espace vertical
                    for bin in bins:
                        if not bin:
                            continue
                        
                        last_level = bin[-1]
                        available_height = bin_height - (last_level[0] + last_level[1])

                        if h <= available_height:
                            new_y = last_level[0] + last_level[1]
                            bin.append([new_y, h, 0, []])  # Nouveau niveau
                            bin[-1][3].append((0, new_y, w, h))  # Premier rectangle
                            bin[-1][2] = w  # Mettre à jour la largeur utilisée
                            placed = True
                            break
                        
                    # Si toujours non placé, créer un nouveau bin
                    if not placed and h <= bin_height:
                        bins.append([[0, h, 0, []]])  # Nouveau bin avec premier niveau
                        bins[-1][-1][3].append((0, 0, w, h))  # Premier rectangle
                        bins[-1][-1][2] = w  # Mettre à jour la largeur utilisée

            # Convertir en format de sortie pour la visualisation
            result_bins = []
            for bin_levels in bins:
                bin_rectangles = []
                for level in bin_levels:
                    bin_rectangles.extend(level[3])
                result_bins.append(bin_rectangles)

            return result_bins

    def nfdh_2d_packing(self,rectangles, bin_width, bin_height):
        # Trier les rectangles par hauteur décroissante
        sorted_rects = sorted(rectangles, key=lambda x: -x[1])

        bins = []          # Liste des bins créés
        current_bin = []    # Rectangle dans le bin courant
        current_level_y = 0 # Position y du niveau courant
        current_level_h = 0 # Hauteur du niveau courant
        current_x = 0       # Position x courante dans le niveau

        for w, h in sorted_rects:
            # Ignorer les rectangles trop larges
            if w > bin_width:
                print(f"Rectangle {w}x{h} ignoré (trop large)")
                continue
            
            # Vérifier si le rectangle est trop haut pour le bin
            if h > bin_height:
                print(f"Rectangle {w}x{h} ignoré (trop haut)")
                continue
            
            # Si nouveau bin nécessaire (premier rectangle ou plus de place verticale)
            if not current_bin or (current_level_y + h > bin_height):
                if current_bin:
                    bins.append(current_bin)
                current_bin = []
                current_level_y = 0
                current_level_h = h
                current_x = 0

            # Si nouveau niveau nécessaire (pas assez de place horizontale)
            if current_x + w > bin_width:
                current_level_y += current_level_h
                current_level_h = h
                current_x = 0

                # Vérifier si le nouveau niveau dépasse la hauteur du bin
                if current_level_y + h > bin_height:
                    bins.append(current_bin)
                    current_bin = []
                    current_level_y = 0
                    current_level_h = h
                    current_x = 0

            # Ajouter le rectangle au bin courant
            current_bin.append((current_x, current_level_y, w, h))
            current_x += w

        # Ajouter le dernier bin s'il contient des rectangles
        if current_bin:
            bins.append(current_bin)

        return bins

    def bfdh_2d_packing(self,rectangles, bin_width, bin_height):
        # Trier par hauteur décroissante, puis largeur décroissante
        sorted_rects = sorted(rectangles, key=lambda x: (-x[1], -x[0]))
        bins = []  # Chaque bin contient des niveaux (y, height, used_width, rectangles)

        for w, h in sorted_rects:
            if w > bin_width or h > bin_height:
                print(f"Rectangle {w}x{h} ignoré (trop grand)")
                continue

            placed = False
            best_bin = None
            best_level = None
            best_remaining = float('inf')

            # Chercher dans les bins existants
            for bin_idx, bin_levels in enumerate(bins):
                for level_idx, level in enumerate(bin_levels):
                    level_y, level_h, used_w, level_rects = level
                    remaining_width = bin_width - used_w
                    if w <= remaining_width and h <= level_h:
                        remaining = remaining_width - w
                        if remaining < best_remaining:
                            best_remaining = remaining
                            best_bin = bin_idx
                            best_level = level_idx

            # Si niveau trouvé
            if best_bin is not None:
                x_pos = bins[best_bin][best_level][2]  # used_width devient position x
                bins[best_bin][best_level][3].append((x_pos, bins[best_bin][best_level][0], w, h))
                bins[best_bin][best_level][2] += w  # Mettre à jour used_width
                placed = True
            else:
                # Chercher où créer un nouveau niveau
                for bin_idx, bin_levels in enumerate(bins):
                    if not bin_levels:
                        continue
                    last_level = bin_levels[-1]
                    available_height = bin_height - (last_level[0] + last_level[1])
                    if h <= available_height:
                        new_y = last_level[0] + last_level[1]
                        bins[bin_idx].append([new_y, h, 0, []])  # Nouveau niveau
                        bins[bin_idx][-1][3].append((0, new_y, w, h))  # Premier rectangle
                        bins[bin_idx][-1][2] = w  # used_width
                        placed = True
                        break
                    
                # Si aucun bin ne convient, créer un nouveau bin
                if not placed and h <= bin_height:
                    bins.append([[0, h, 0, []]])  # Nouveau bin avec premier niveau
                    bins[-1][-1][3].append((0, 0, w, h))  # Premier rectangle
                    bins[-1][-1][2] = w  # used_width

        # Convertir en format de sortie pour la visualisation
        result_bins = []
        for bin_levels in bins:
            bin_rectangles = []
            for level in bin_levels:
                bin_rectangles.extend(level[3])
            result_bins.append(bin_rectangles)

        return result_bins

    def visualize_packing(self,bins, bin_width, bin_height,imageOutput):
        fig, axes = plt.subplots(len(bins), 1, figsize=(10, 5 * len(bins)))
        if len(bins) == 1:
            axes = [axes] 

        for idx, (ax, bin) in enumerate(zip(axes, bins)):
            bin_rect = patches.Rectangle((0, 0), bin_width, bin_height,
                                       linewidth=2, edgecolor='black', 
                                       facecolor='lightgray', alpha=0.2)
            ax.add_patch(bin_rect)

            colors = plt.cm.tab20.colors
            for i, (x, y, w, h) in enumerate(bin):
                rect = patches.Rectangle((x, y), w, h, 
                                       facecolor=colors[i % len(colors)],
                                       edgecolor='black')
                ax.add_patch(rect)
                ax.text(x + w/2, y + h/2, f'{w}x{h}', 
                       ha='center', va='center', color='black')

            ax.set_xlim(0, bin_width)
            ax.set_ylim(0, bin_height)
            ax.set_title(f'Bin {idx+1} - Utilisation: {sum(w*h for _,_,w,h in bin)/(bin_width*bin_height):.1%}')
            ax.grid(True)

        plt.tight_layout()
        plt.savefig(imageOutput, dpi=120, bbox_inches='tight')
        plt.close()

    def __init__(self, root):
        self.root = root
        self.root.title("2D Bin Packing")
        self.bin_width = tk.IntVar(value=300)
        self.bin_height = tk.IntVar(value=300)
        self.rectangles = [] 
        self.listMethod = ["NFDH","BF","FFDH"]
        self.methodeSelector = ttk.Combobox(self.root,values=self.listMethod)
        self.rect_count = 0
        self.problemSolved = False
        self.current_methode = None
        self.bac_width = 0
        self.bac_heigth = 0
        self.setup_ui()

    def selection_change(self,event):
        method = self.methodeSelector.get()

        if method is not None:
            self.current_methode = method
            self.drawSolution()

    def drawSolution(self):
         if not hasattr(self, 'canvas') or self.current_methode is None:
                return
         try:
             if self.current_methode=="NFDH":
                 img = Image.open("2D_NFDH.png")
             elif self.current_methode=="BF":
                 img = Image.open("2D_BF.png")
             elif self.current_methode=="FFDH":
                 img = Image.open("2D_FFDH.png")
             else:
                 return
                 
             img_width, img_height = img.size
             canvas_width = self.canvas.winfo_width() - 20 
             canvas_height = self.canvas.winfo_height() - 20
             
             ratio = min(canvas_width/img_width, canvas_height/img_height)
             new_width = int(img_width * ratio)
             new_height = int(img_height * ratio)
             
             resized = img.resize((new_width, new_height), Image.LANCZOS)
             tk_img = ImageTk.PhotoImage(resized)
             
             x_pos = (canvas_width - new_width) // 2 + 10
             y_pos = (canvas_height - new_height) // 2 + 10
             
             self.canvas.delete("all")
             self.canvas.create_image(x_pos, y_pos, anchor="nw", image=tk_img)
             self.canvas.image = tk_img
             
         except Exception as e:
             print(f"Erreur lors du chargement de l'image: {e}")

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="white", padx=20, pady=20, bd=2, relief="groove")
        left_frame.pack(side="left", padx=10, fill="y")

        tk.Label(left_frame, text="Longueur :", font=("Helvetica", 12), bg="white").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.rect_width_entry = tk.Entry(left_frame, font=("Helvetica", 12))
        self.rect_width_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(left_frame, text="Largeur :", font=("Helvetica", 12), bg="white").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.rect_height_entry = tk.Entry(left_frame, font=("Helvetica", 12))
        self.rect_height_entry.grid(row=1, column=1, pady=5, padx=5)

        add_btn = tk.Button(left_frame, text="Ajouter", bg="#4CAF50", fg="white",font=("Helvetica", 12, "bold"), padx=10, pady=5,command=self.ajouter_rectangle)
        add_btn.grid(row=2, columnspan=2, pady=15)

        self.table = ttk.Treeview(left_frame, columns=("Longueur", "Largeur"), show="headings", height=5)
        self.table.heading("Longueur", text="Longueur")
        self.table.heading("Largeur", text="Largeur")
        self.table.column("Longueur", anchor="center")
        self.table.column("Largeur", anchor="center")
        self.table.grid(row=3, columnspan=2, pady=10)

        reset_btn = tk.Button(left_frame, text="Reset", bg="#B81A1A", fg="white",font=("Helvetica", 12, "bold"), padx=10, pady=5,command=self.reset_data)
        reset_btn.grid(row=4, columnspan=2, pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)

        rigth_frame = tk.Frame(main_frame,bg="white",padx=20,pady=20,bd=2,relief="groove")
        rigth_frame.pack(side="right",padx=10,pady=10, fill="both", expand=True)

        self.methodeSelector = ttk.Combobox(rigth_frame,values=self.listMethod)
        self.methodeSelector.pack(padx=10,pady=10)
        self.methodeSelector.bind("<<ComboboxSelected>>",self.selection_change)

        canvas_container = tk.Frame(rigth_frame)
        canvas_container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(canvas_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(canvas_container, bg="white", yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.canvas.yview)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.bin_width_label = tk.Label(self.root,text="longeur")
        self.double_width_var = tk.DoubleVar(value=0)
        self.bin_width_entry = tk.Entry(self.root,textvariable=self.double_width_var)


        self.bin_heigth_label = tk.Label(self.root,text="largeur")
        self.double_heigth_var = tk.DoubleVar(value=0)
        self.bin_heigth_entry = tk.Entry(self.root,textvariable=self.double_heigth_var)

        self.bin_width_label.pack(padx=30,pady=10)
        self.bin_width_entry.pack(padx=30,pady=10)
        self.bin_heigth_label.pack(padx=30,pady=10)
        self.bin_heigth_entry.pack(padx=30,pady=10)

        solve_btn = tk.Button(self.root, text="résoudre", bg="#4CAF50", fg="white",font=("Helvetica", 12, "bold"), padx=10, pady=5,command=self.solve)
        solve_btn.pack(padx=30,pady=10)

    def reset_data(self):
        self.rectangles = []
        self.table.delete(*self.table.get_children())

    def on_canvas_resize(self, event):
        width = event.width
        height = event.height
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, width, height, outline="black")
        self.drawSolution()

    def ajouter_rectangle(self):
        longueur = 0
        largeur = 0
        try:
            longueur = int(self.rect_width_entry.get())
            largeur = int(self.rect_height_entry.get())
        except ValueError:
            return 
        self.rectangles.append((longueur,largeur))
        self.table.insert("", "end", values=(longueur, largeur))

        x_offset = 10
        y_offset = 10 + self.rect_count * 10
        scale = 2 
        self.canvas.create_rectangle(
            x_offset,
            y_offset,
            x_offset + longueur * scale,
            y_offset + largeur * scale,
            fill="#90caf9", outline="black"
        )

        self.rect_count += 1

        self.rect_width_entry.delete(0, tk.END)
        self.rect_height_entry.delete(0, tk.END)
        print(self.rectangles)

    def solve(self):
        self.bac_width = self.double_width_var.get()
        self.bac_heigth = self.double_heigth_var.get()
        if self.rectangles is not None and self.bac_heigth>0 and self.bac_width>0:
            bins = self.ffdh_2d_packing(self.rectangles,self.bac_width,self.bac_heigth)
            self.visualize_packing(bins,self.bac_width,self.bac_heigth,"2D_FFDH.png")

            bins = self.nfdh_2d_packing(self.rectangles,self.bac_width,self.bac_heigth)
            self.visualize_packing(bins,self.bac_width,self.bac_heigth,"2D_NFDH.png")

            bins = self.bfdh_2d_packing(self.rectangles,self.bac_width,self.bac_heigth)
            self.visualize_packing(bins,self.bac_width,self.bac_heigth,"2D_BF.png")
if __name__ == "__main__":
    root = tk.Tk()
    app = BinPackingApp(root)
    root.mainloop()
