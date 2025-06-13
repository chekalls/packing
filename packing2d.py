import matplotlib.pyplot as plt
import matplotlib.patches as patches

def ffdh_2d_packing(rectangles, bin_width, bin_height):
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

def nfdh_2d_packing(rectangles, bin_width, bin_height):
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

def bfdh_2d_packing(rectangles, bin_width, bin_height):
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

def visualize_packing(bins, bin_width, bin_height):
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
    plt.savefig('2D_FFDH.png', dpi=120, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    rectangles = [(6, 7), (5, 6), (4, 5), (3, 4), (2, 3), (1, 2),(8,2.5),(2,2)]
    bin_width = 8
    bin_height = 20
    
    bins = nfdh_2d_packing(rectangles, bin_width, bin_height)

    visualize_packing(bins, bin_width, bin_height)