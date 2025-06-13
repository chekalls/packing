import itertools
import matplotlib.pyplot as plt

def plot_bins(items, bin_capacity, algo_func, algo_name):
    bins, impossible_items = algo_func(items, bin_capacity)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    objects_text = f"Objets: {items}\nCapacité max: {bin_capacity}"
    plt.suptitle(objects_text, fontsize=12, y=1.05)
    
    for i, bin in enumerate(bins):
        ax.barh(i, bin_capacity, left=0, height=0.6, color='lightgray', edgecolor='black', alpha=0.3)
        left = 0
        for item in bin:
            ax.barh(i, item, left=left, height=0.4, color='skyblue', edgecolor='black')
            ax.text(left + item/2, i, str(item), ha='center', va='center', fontweight='bold')
            left += item
    
        if impossible_items:
            # impossible_title_pos = len(bins)
            # ax.text(0, impossible_title_pos - 0.3, "OBJETS IMPOSSIBLES :", 
            #         ha='left', va='center', color='red', fontweight='bold', fontsize=12)

            # for i, item in enumerate(impossible_items):
            #     impossible_pos = len(bins) + i
            #     ax.barh(impossible_pos, bin_capacity, left=0, height=0.6, 
            #             color='lightgray', edgecolor='black', alpha=0.3)
            #     ax.barh(impossible_pos, item, left=0, height=0.4, 
            #             color='red', edgecolor='black')
            #     ax.text(item/2, impossible_pos, str(item), 
            #             ha='center', va='center', color='white', fontweight='bold')
            #     ax.text(0, impossible_pos, f"Objet {i+1}", 
            #             ha='left', va='center', color='black', fontsize=10)
            pass

    total_bins = len(bins)
    ax.set_title(f"{algo_name} | Conteneurs: {len(bins)} | Impossible: {len(impossible_items)}", pad=20)
    ax.set_yticks(range(total_bins))
    ax.set_yticklabels([f"Conteneur {i+1}" for i in range(len(bins))] )
    ax.set_xlabel("Taille des objets")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(f"1D_{algo_name}.png", dpi=100, bbox_inches='tight')
    plt.close()

def first_fit(items, bin_capacity):
    bins = []
    impossible_items = []
    
    for item in items:
        if item > bin_capacity:
            impossible_items.append(item)
            continue
            
        placed = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                placed = True
                break
                
        if not placed:
            bins.append([item])
    
    return bins, impossible_items

def best_fit(items, bin_capacity):
    bins = []
    impossible_items = [item for item in items if item > bin_capacity]
    valid_items = [item for item in items if item <= bin_capacity]
    
    for item in valid_items:
        best_bin = None
        min_space = bin_capacity + 1 
        
        for bin in bins:
            remaining = bin_capacity - sum(bin)
            if remaining >= item and remaining < min_space:
                best_bin = bin
                min_space = remaining
                
        if best_bin is not None:
            best_bin.append(item)
        else:
            bins.append([item])
    
    return bins, impossible_items

def worst_fit(items, bin_capacity):
    bins = []
    impossible_items = [item for item in items if item > bin_capacity]
    valid_items = [item for item in items if item <= bin_capacity]
    
    for item in valid_items:
        worst_bin = None
        max_space = -1  
        
        for bin in bins:
            remaining = bin_capacity - sum(bin)
            if remaining >= item and remaining > max_space:
                worst_bin = bin
                max_space = remaining
                
        if worst_bin is not None:
            worst_bin.append(item)
        else:
            bins.append([item])
    
    return bins, impossible_items

def brute_force_bin_packing(items, bin_capacity):
    n = len(items)
    min_bins = float('inf')
    best_solution = None
    
    for permutation in itertools.permutations(items):
        bins = []
        current_bin = []
        
        for item in permutation:
            placed = False
            for bin in bins:
                if sum(bin) + item <= bin_capacity:
                    bin.append(item)
                    placed = True
                    break
            if not placed:
                bins.append([item])
        
        if len(bins) < min_bins:
            min_bins = len(bins)
            best_solution = [bin.copy() for bin in bins]
    
    return best_solution, min_bins

items = [1,2,3,4,5,6,7,8,9,10]
taille_bac = 10

bins, impossible = first_fit(items, taille_bac)
plot_bins(items, taille_bac, first_fit, "FF")

bins ,impossible = best_fit(items,taille_bac)
plot_bins(items,taille_bac,best_fit,"BF")


bins,impossible = worst_fit(items,taille_bac)
plot_bins(items,taille_bac,worst_fit,"WF")

items = [1,2,3,4,5,6,7,8,9,10]


solution, num_bins = brute_force_bin_packing(items, taille_bac)
print(f"Solution optimale: {solution}")
print(f"Nombre minimal de bacs: {num_bins}")