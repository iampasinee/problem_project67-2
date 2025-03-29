import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from itertools import permutations

# สร้างกราฟ
G = nx.Graph()
dic_cafe = {
    "A": "Myrrh Cafe Prachinburi",
    "B": "Toast bar Cafe",
    "C": "Noen Hom Cafe",
    "D": "Rong See Coffee Prachinburi",
    "E": "Homurumu Cafe",
    "F": "Eto slowbar",
    "G": "Nare Cafe",
    "H": "VV Cafe & bistro",
    "I": "Baan Fuangfah cafe"
}
G.add_nodes_from(dic_cafe.keys())

edges = [
    ("A", "B", 12), ("A", "C", 10), ("B", "C", 13), ("B", "D", 7),
    ("D", "G", 12), ("E", "F", 9), ("G", "H", 2), ("G", "I", 5),
    ("I", "E", 11), ("I", "F", 3), ("H", "I", 9)
]
G.add_weighted_edges_from(edges)

# ฟังก์ชันคำนวณเส้นทาง

def find_best_shortest_path(start, destinations):
    best_path, best_distance = None, float("inf")
    for perm in permutations(destinations):
        path = [start]
        total_distance = 0
        current = start
        for stop in perm:
            sub_path = nx.shortest_path(G, source=current, target=stop, weight="weight")
            total_distance += nx.shortest_path_length(G, source=current, target=stop, weight="weight")
            path.extend(sub_path[1:])
            current = stop
        if total_distance < best_distance:
            best_distance, best_path = total_distance, path
    return best_path, best_distance

# ฟังก์ชันวาดเส้นทาง

def draw_shortest_path(path, total_distance):
    pos = nx.spring_layout(G, seed=42)
    node_colors = ["pink" if node == path[0] or node == path[-1] else "lightgreen" if node in path else "lightgray" for node in G.nodes()]
    edge_colors = ["lightgreen" if (u, v) in zip(path, path[1:]) else "lightgray" for u, v in G.edges()]
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color=node_colors, edge_color=edge_colors, width=2)
    plt.title(f"Best Path (Total: {total_distance} km)")
    plt.show()

# GUI

def find_route():
    start = start_var.get()
    destinations = [dest_var.get()]
    if not start or not destinations[0]:
        result_label.config(text="กรุณาเลือกจุดเริ่มต้นและจุดหมาย")
        return
    path, distance = find_best_shortest_path(start, destinations)
    result_label.config(text=f"เส้นทาง: {' → '.join(path)} (รวม {distance} km)")
    draw_shortest_path(path, distance)

root = tk.Tk()
root.title("Café Route Finder")
root.geometry("400x300")

start_var = tk.StringVar()
dest_var = tk.StringVar()

# เลือกจุดเริ่มต้น
start_label = tk.Label(root, text="เลือกจุดเริ่มต้น:")
start_label.pack()
start_menu = ttk.Combobox(root, textvariable=start_var, values=list(dic_cafe.keys()))
start_menu.pack()

# เลือกจุดหมาย
dest_label = tk.Label(root, text="เลือกจุดหมาย:")
dest_label.pack()
dest_menu = ttk.Combobox(root, textvariable=dest_var, values=list(dic_cafe.keys()))
dest_menu.pack()

# ปุ่มค้นหา
find_button = tk.Button(root, text="ค้นหาเส้นทาง", command=find_route)
find_button.pack()

# แสดงผลลัพธ์
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()