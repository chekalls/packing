import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import math
import random
import itertools


class BinPackingApp:

    def has_overlap(self, bin, x, y, w, h):
        for rect in bin:
            rx, ry = rect["pos"]
            rw, rh = rect["dims"]

            if not (x + w <= rx or rx + rw <= x or y + h <= ry or ry + rh <= y):
                return True
        return False

    def generate_valid_positions(self, bin, bin_width, bin_height, w, h):
        positions = set()

        positions.add((0, 0))

        for rect in bin:
            rx, ry = rect["pos"]
            rw, rh = rect["dims"]

            if rx + rw + w <= bin_width:
                positions.add((rx + rw, ry))

            if ry + rh + h <= bin_height:
                positions.add((rx, ry + rh))

        positions.add((bin_width - w, 0))
        positions.add((0, bin_height - h))

        return sorted(positions, key=lambda pos: (pos[1], pos[0])) 

    def overlaps(self, bin, x, y, w, h):
        for rect in bin:
            rx, ry = rect["pos"]
            rw, rh = rect["dims"]
            if not (x + w <= rx or rx + rw <= x or y + h <= ry or ry + rh <= y):
                return True
        return False
    def generate_positions(self, bin, bin_width, bin_height, w, h):
        positions = set()

        for rect in bin:
            x, y = rect["pos"]
            rw, rh = rect["dims"]
            positions.add((x + rw, y))      
            positions.add((x, y + rh))      

        positions.add((0, 0))
        positions.add((bin_width - w, 0))
        positions.add((0, bin_height - h))

        return positions

    def can_place_in_bin(self, bin, w, h, bin_width, bin_height):
        total_area = sum(rect["dims"][0] * rect["dims"][1] for rect in bin)
        new_area = w * h
        return (total_area + new_area) <= (bin_width * bin_height)

    def brute_force_packing(self, shapes, bin_width, bin_height):
        rectangles = []
        for shape in shapes:
            if shape["type"] == "Rectangle" and shape["rotation"]:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })
                rectangles.append({
                    "dims": (shape["dim2"], shape["dim1"]),
                    "original": shape,
                    "rotated": True
                })
            else:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })

        best_solution = None
        min_bins = float('inf')

        for ordering in itertools.permutations(rectangles):
            bins = []

            for rect in ordering:
                placed = False
                w, h = rect["dims"]

                if w > bin_width or h > bin_height:
                    continue

                for bin in bins:
                    for x, y in self.generate_valid_positions(bin, bin_width, bin_height, w, h):
                        if not self.has_overlap(bin, x, y, w, h):
                            bin.append({
                                "pos": (x, y),
                                "dims": (w, h),
                                "original": rect["original"],
                                "rotated": rect["rotated"]
                            })
                            placed = True
                            break
                    if placed:
                        break
                    
                if not placed and w <= bin_width and h <= bin_height:
                    bins.append([{
                        "pos": (0, 0),
                        "dims": (w, h),
                        "original": rect["original"],
                        "rotated": rect["rotated"]
                    }])

            if bins and len(bins) < min_bins:
                min_bins = len(bins)
                best_solution = bins

        result_bins = []
        for bin in best_solution:
            bin_rectangles = []
            for rect in bin:
                bin_rectangles.append((
                    rect["pos"][0],
                    rect["pos"][1],
                    rect["dims"][0],
                    rect["dims"][1],
                    rect["original"],
                    rect["rotated"]
                ))
            result_bins.append(bin_rectangles)

        return result_bins if best_solution else []

    def ffdh_2d_packing(self, shapes, bin_width, bin_height):
        rectangles = []
        for shape in shapes:
            if shape["type"] == "Rectangle" and shape["rotation"]:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })
                rectangles.append({
                    "dims": (shape["dim2"], shape["dim1"]),
                    "original": shape,
                    "rotated": True
                })
            else:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })

        sorted_rects = sorted(rectangles, key=lambda x: (-x["dims"][1], -x["dims"][0]))

        bins = []
        placed_indices = set()

        for idx, rect in enumerate(sorted_rects):
            if idx in placed_indices:
                continue

            w, h = rect["dims"]
            if w > bin_width or h > bin_height:
                continue

            placed = False

            for bin in bins:
                for level in bin:
                    y, level_h, used_w, level_rects = level
                    remaining_width = bin_width - used_w

                    if w <= remaining_width and h <= level_h:
                        level_rects.append({
                            "pos": (used_w, y),
                            "dims": (w, h),
                            "original": rect["original"],
                            "rotated": rect["rotated"]
                        })
                        level[2] += w
                        placed = True
                        placed_indices.add(idx)
                        break
                
                if placed:
                    break

            if not placed and idx not in placed_indices:
                for bin in bins:
                    if not bin:
                        continue
                    
                    last_level = bin[-1]
                    available_height = bin_height - (last_level[0] + last_level[1])

                    if h <= available_height:
                        new_y = last_level[0] + last_level[1]
                        bin.append([new_y, h, 0, []])
                        bin[-1][3].append({
                            "pos": (0, new_y),
                            "dims": (w, h),
                            "original": rect["original"],
                            "rotated": rect["rotated"]
                        })
                        bin[-1][2] = w
                        placed = True
                        placed_indices.add(idx)
                        break

                if not placed and h <= bin_height:
                    bins.append([[0, h, 0, []]])
                    bins[-1][-1][3].append({
                        "pos": (0, 0),
                        "dims": (w, h),
                        "original": rect["original"],
                        "rotated": rect["rotated"]
                    })
                    bins[-1][-1][2] = w
                    placed_indices.add(idx)

        result_bins = []
        for bin_levels in bins:
            bin_rectangles = []
            for level in bin_levels:
                for rect in level[3]:
                    bin_rectangles.append((
                        rect["pos"][0], 
                        rect["pos"][1], 
                        rect["dims"][0], 
                        rect["dims"][1],
                        rect["original"],
                        rect["rotated"]
                    ))
            result_bins.append(bin_rectangles)

        return result_bins

    def nfdh_2d_packing(self, shapes, bin_width, bin_height):
        rectangles = []
        for shape in shapes:
            if shape["type"] == "Rectangle" and shape["rotation"]:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })
                rectangles.append({
                    "dims": (shape["dim2"], shape["dim1"]),
                    "original": shape,
                    "rotated": True
                })
            else:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })

        sorted_rects = sorted(rectangles, key=lambda x: -x["dims"][1])

        bins = []
        current_bin = []
        current_level_y = 0
        current_level_h = 0
        current_x = 0
        placed_indices = set()

        for idx, rect in enumerate(sorted_rects):
            if idx in placed_indices:
                continue

            w, h = rect["dims"]
            if w > bin_width or h > bin_height:
                continue

            if not current_bin or (current_level_y + h > bin_height):
                if current_bin:
                    bins.append(current_bin)
                current_bin = []
                current_level_y = 0
                current_level_h = h
                current_x = 0

            if current_x + w > bin_width:
                current_level_y += current_level_h
                current_level_h = h
                current_x = 0

                if current_level_y + h > bin_height:
                    bins.append(current_bin)
                    current_bin = []
                    current_level_y = 0
                    current_level_h = h
                    current_x = 0

            current_bin.append((
                current_x, 
                current_level_y, 
                w, 
                h,
                rect["original"],
                rect["rotated"]
            ))
            current_x += w
            placed_indices.add(idx)

        if current_bin:
            bins.append(current_bin)

        return bins

    def bfdh_2d_packing(self, shapes, bin_width, bin_height):
        rectangles = []
        for shape in shapes:
            if shape["type"] == "Rectangle" and shape["rotation"]:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })
                rectangles.append({
                    "dims": (shape["dim2"], shape["dim1"]),
                    "original": shape,
                    "rotated": True
                })
            else:
                rectangles.append({
                    "dims": (shape["dim1"], shape["dim2"]),
                    "original": shape,
                    "rotated": False
                })

        sorted_rects = sorted(rectangles, key=lambda x: (-x["dims"][1], -x["dims"][0]))

        bins = []
        placed_indices = set()

        for idx, rect in enumerate(sorted_rects):
            if idx in placed_indices:
                continue

            w, h = rect["dims"]
            if w > bin_width or h > bin_height:
                continue

            placed = False
            best_bin = None
            best_level = None
            best_remaining = float('inf')

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

            if best_bin is not None:
                x_pos = bins[best_bin][best_level][2]
                bins[best_bin][best_level][3].append({
                    "pos": (x_pos, bins[best_bin][best_level][0]),
                    "dims": (w, h),
                    "original": rect["original"],
                    "rotated": rect["rotated"]
                })
                bins[best_bin][best_level][2] += w
                placed = True
                placed_indices.add(idx)

            if not placed:
                for bin_idx, bin_levels in enumerate(bins):
                    if not bin_levels:
                        continue
                    last_level = bin_levels[-1]
                    available_height = bin_height - (last_level[0] + last_level[1])
                    if h <= available_height:
                        new_y = last_level[0] + last_level[1]
                        bins[bin_idx].append([new_y, h, 0, []])
                        bins[bin_idx][-1][3].append({
                            "pos": (0, new_y),
                            "dims": (w, h),
                            "original": rect["original"],
                            "rotated": rect["rotated"]
                        })
                        bins[bin_idx][-1][2] = w
                        placed = True
                        placed_indices.add(idx)
                        break

                if not placed and h <= bin_height:
                    bins.append([[0, h, 0, []]])
                    bins[-1][-1][3].append({
                        "pos": (0, 0),
                        "dims": (w, h),
                        "original": rect["original"],
                        "rotated": rect["rotated"]
                    })
                    bins[-1][-1][2] = w
                    placed_indices.add(idx)

        result_bins = []
        for bin_levels in bins:
            bin_rectangles = []
            for level in bin_levels:
                for rect in level[3]:
                    bin_rectangles.append((
                        rect["pos"][0],
                        rect["pos"][1],
                        rect["dims"][0],
                        rect["dims"][1],
                        rect["original"],
                        rect["rotated"]
                    ))
            result_bins.append(bin_rectangles)

        return result_bins

    def __init__(self, root):
        self.root = root
        self.root.title("2D Bin Packing with Shapes")
        self.bin_width = tk.DoubleVar(value=300.0)
        self.bin_height = tk.DoubleVar(value=300.0)
        self.shapes = []
        self.listMethod = ["NFDH", "BF", "FFDH", "Brute Force"]  
        self.shape_types = ["Rectangle", "Triangle", "Circle"]
        self.current_shape = tk.StringVar(value="Rectangle")
        self.allow_rotation = tk.BooleanVar(value=False)
        self.current_methode = None
        self.root.geometry("1000x650")
        self.setup_ui()
        self.stop_brute_force = False
        self.progress_var = tk.DoubleVar()
        self.progress_max = 100
        self.packing_results = {}  

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="white", padx=15, pady=15, bd=2, relief="groove")
        left_frame.pack(side="left", fill="y")

        tk.Label(left_frame, text="Bin Dimensions", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, columnspan=2, pady=5)

        tk.Label(left_frame, text="Width:", bg="white").grid(row=1, column=0, sticky="e", padx=5)
        tk.Entry(left_frame, textvariable=self.bin_width, width=8).grid(row=1, column=1, pady=5)

        tk.Label(left_frame, text="Height:", bg="white").grid(row=2, column=0, sticky="e", padx=5)
        tk.Entry(left_frame, textvariable=self.bin_height, width=8).grid(row=2, column=1, pady=5)

        ttk.Separator(left_frame, orient="horizontal").grid(row=3, columnspan=2, pady=10, sticky="ew")

        tk.Label(left_frame, text="Add Shape", font=("Helvetica", 12, "bold"), bg="white").grid(row=4, columnspan=2, pady=5)

        tk.Label(left_frame, text="Type:", bg="white").grid(row=5, column=0, sticky="e", padx=5)
        shape_combo = ttk.Combobox(left_frame, textvariable=self.current_shape, 
                                  values=self.shape_types, width=10)
        shape_combo.grid(row=5, column=1, pady=5)
        shape_combo.bind("<<ComboboxSelected>>",self.set_dim_entry)

        tk.Checkbutton(left_frame, text="Allow Rotation", variable=self.allow_rotation, 
                      bg="white").grid(row=6, columnspan=2, pady=5)

        tk.Label(left_frame, text="Dim 1:", bg="white").grid(row=7, column=0, sticky="e", padx=5)
        self.dim1_entry = tk.Entry(left_frame, width=8)
        self.dim1_entry.grid(row=7, column=1, pady=5)

        tk.Label(left_frame, text="Dim 2:", bg="white").grid(row=8, column=0, sticky="e", padx=5)
        self.dim2_entry = tk.Entry(left_frame, width=8)
        self.dim2_entry.grid(row=8, column=1, pady=5)
        self.dim2_entry.config(state="normal")

        add_btn = tk.Button(left_frame, text="Add Shape", bg="#4CAF50", fg="white",
                           command=self.add_shape)
        add_btn.grid(row=9, columnspan=2, pady=10)

        self.table = ttk.Treeview(left_frame, columns=("Type", "Dim1", "Dim2", "Rotation"), 
                                 show="headings", height=6)
        self.table.heading("Type", text="Type")
        self.table.heading("Dim1", text="Dim1")
        self.table.heading("Dim2", text="Dim2")
        self.table.heading("Rotation", text="Rotation")
        self.table.column("Type", width=80, anchor="center")
        self.table.column("Dim1", width=60, anchor="center")
        self.table.column("Dim2", width=60, anchor="center")
        self.table.column("Rotation", width=70, anchor="center")
        self.table.grid(row=10, columnspan=2, pady=10)

        reset_btn = tk.Button(left_frame, text="Reset All", bg="#f44336", fg="white",
                             command=self.reset_data)
        reset_btn.grid(row=11, columnspan=2, pady=5)

        solve_btn = tk.Button(left_frame, text="Solve", bg="#2196F3", fg="white",
                             command=self.solve)
        solve_btn.grid(row=12, columnspan=2, pady=15)

        right_frame = tk.Frame(main_frame, bg="white", padx=15, pady=15, bd=2, relief="groove")
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text="Packing Method:", bg="white").pack(pady=5)
        self.methodeSelector = ttk.Combobox(right_frame, values=self.listMethod, state="readonly")
        self.methodeSelector.pack(pady=5)
        self.methodeSelector.bind("<<ComboboxSelected>>", self.selection_change)

        canvas_container = tk.Frame(right_frame)
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="white", bd=2, relief="sunken")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.root.minsize(800, 500)

    def set_dim_entry(self,event):
        try:
            shape_type = self.current_shape.get()            
            if shape_type == "Circle":
                self.dim2_entry.config(state="disabled")
            else:
                self.dim2_entry.config(state="normal")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions")
    def add_shape(self):
        try:
            shape_type = self.current_shape.get()
            dim1 = float(self.dim1_entry.get())
            
            if shape_type == "Circle":
                dim2 = dim1  
                rotation = False
                self.dim2_entry.config(state="disabled")
            else:
                dim2 = float(self.dim2_entry.get())
                rotation = self.allow_rotation.get()
                self.dim2_entry.config(state="normal")
            
            shape = {
                "type": shape_type,
                "dim1": dim1,
                "dim2": dim2,
                "rotation": rotation
            }
            
            self.shapes.append(shape)
            
            self.table.insert("", "end", values=(
                shape_type,
                f"{dim1:.2f}",
                f"{dim2:.2f}" if shape_type != "Circle" else "N/A",
                "Yes" if rotation and shape_type != "Circle" else "No"
            ))
            
            self.dim1_entry.delete(0, tk.END)
            self.dim2_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions")

    def reset_data(self):
        self.shapes = []
        self.table.delete(*self.table.get_children())
        self.canvas.delete("all")
        self.packing_results = {}

    def solve(self):
        bin_width = self.bin_width.get()
        bin_height = self.bin_height.get()

        if not self.shapes:
            messagebox.showerror("Error", "No shapes to pack")
            return

        if bin_width <= 0 or bin_height <= 0:
            messagebox.showerror("Error", "Bin dimensions must be positive")
            return

        try:
            self.packing_results["NFDH"] = self.nfdh_2d_packing(self.shapes, bin_width, bin_height)
            self.packing_results["BF"] = self.bfdh_2d_packing(self.shapes, bin_width, bin_height)
            self.packing_results["FFDH"] = self.ffdh_2d_packing(self.shapes, bin_width, bin_height)
            self.packing_results["Brute Force"] = self.brute_force_packing(self.shapes, bin_width, bin_height)
            
            if self.current_methode is None:
                self.current_methode = "NFDH"
                self.methodeSelector.set("NFDH")
            
            self.drawSolution()
            messagebox.showinfo("Success", "Packing completed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def draw_packing(self, bins, bin_width, bin_height):
        self.canvas.delete("all")
        
        if not bins:
            return
            
        canvas_width = self.canvas.winfo_width() - 40
        canvas_height = self.canvas.winfo_height() - 40
        
        max_bin_width = bin_width
        max_bin_height = bin_height * len(bins) 
        
        scale = min(canvas_width / max_bin_width, canvas_height / max_bin_height)
        scale = min(scale, 1.0)  
        
        y_offset = 20
        bin_spacing = 20
        
        colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(20)]
        
        for bin_idx, bin in enumerate(bins):
            x1 = 20
            y1 = y_offset + bin_idx * (bin_height * scale + bin_spacing)
            x2 = x1 + bin_width * scale
            y2 = y1 + bin_height * scale
            
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lightgray", width=2)
            
            for (x, y, w, h, original_shape, rotated) in bin:
                color = colors[hash(original_shape["type"]) % len(colors)]
                
                cx1 = x1 + x * scale
                cy1 = y1 + y * scale
                cx2 = cx1 + w * scale
                cy2 = cy1 + h * scale
                
                if original_shape["type"] == "Rectangle":
                    self.canvas.create_rectangle(cx1, cy1, cx2, cy2, outline="black", fill=color, width=1)
                    if rotated:
                        center_x = (cx1 + cx2) / 2
                        center_y = (cy1 + cy2) / 2
                        self.canvas.create_oval(center_x-2, center_y-2, center_x+2, center_y+2, fill="red")
                    
                    text = f"{original_shape['dim1']}x{original_shape['dim2']}"
                    if rotated:
                        text += " (R)"
                    self.canvas.create_text((cx1 + cx2)/2, (cy1 + cy2)/2, text=text, font=("Arial", 8))
                
                elif original_shape["type"] == "Triangle":
                    points = [
                        cx1, cy2,
                        (cx1 + cx2)/2, cy1,
                        cx2, cy2
                    ]
                    self.canvas.create_polygon(points, outline="black", fill=color, width=1)
                    self.canvas.create_text((cx1 + cx2)/2, (cy1 + cy2)/2, 
                                          text=f"{original_shape['dim1']}", font=("Arial", 8))
                
                elif original_shape["type"] == "Circle":
                    self.canvas.create_oval(cx1, cy1, cx2, cy2, outline="black", fill=color, width=1)
                    self.canvas.create_text((cx1 + cx2)/2, (cy1 + cy2)/2, 
                                          text=f"{original_shape['dim1']}", font=("Arial", 8))
            
            used_area = sum(w*h for (x,y,w,h,_,_) in bin)
            total_area = bin_width * bin_height
            utilization = used_area / total_area
            
            self.canvas.create_text(x1 + bin_width*scale/2, y1 - 10, 
                                  text=f"Bin {bin_idx+1} - Utilization: {utilization:.1%}",
                                  font=("Arial", 10, "bold"), anchor="center")
        
        total_height = y_offset + len(bins) * (bin_height * scale + bin_spacing)
        self.canvas.config(scrollregion=(0, 0, bin_width * scale + 40, total_height))

    def selection_change(self, event):
        method = self.methodeSelector.get()
        if method is not None:
            self.current_methode = method
            self.drawSolution()

    def drawSolution(self):
        if not hasattr(self, 'canvas') or not self.current_methode:
            return
            
        if self.current_methode in self.packing_results:
            bin_width = self.bin_width.get()
            bin_height = self.bin_height.get()
            self.draw_packing(self.packing_results[self.current_methode], bin_width, bin_height)

if __name__ == "__main__":
    root = tk.Tk()
    app = BinPackingApp(root)
    root.mainloop()