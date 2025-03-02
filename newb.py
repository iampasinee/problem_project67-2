import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# 🔹 สร้างกราฟ
G = nx.Graph()

dic_cafe = {
    "A": "Morning Brew",
    "B": "Cozy Corner",
    "C": "Bean & Leaf",
    "D": "Sunrise Café",
    "E": "Moonlight Coffee"
}

cafes = ["A", "B", "C", "D", "E"]
G.add_nodes_from(cafes)

edges = [
    ("A", "B", 3),
    ("A", "D", 2),
    ("B", "D", 4),
    ("B", "E", 7),
    ("C", "D", 6),
    ("C", "E", 5),
    ("D", "E", 8)
]
G.add_weighted_edges_from(edges)

# 🔹 ฟังก์ชันหาเส้นทางที่ดีที่สุด

def find_best_shortest_path(start, destinations):
    if len(destinations) == 1:
        end = destinations[0]
        path = nx.shortest_path(G, source=start, target=end, weight="weight")
        distance = nx.shortest_path_length(G, source=start, target=end, weight="weight")
        return path, distance
    
    best_path, best_distance = None, float("inf")

    for perm in permutations(destinations):
        path = [start]
        total_distance = 0
        current_location = start

        for next_stop in perm:
            sub_path = nx.shortest_path(G, source=current_location, target=next_stop, weight="weight")
            sub_distance = nx.shortest_path_length(G, source=current_location, target=next_stop, weight="weight")
            path.extend(sub_path[1:])
            total_distance += sub_distance
            current_location = next_stop

        if total_distance < best_distance:
            best_distance, best_path = total_distance, path

    return best_path, best_distance

# 🔹 ฟังก์ชันวาดเส้นทางที่ดีที่สุด

def draw_shortest_path(path, total_distance):
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    
    node_colors = ["red" if node == path[0] else "green" if node in path else "gray" for node in G.nodes()]
    edge_colors = ["green" if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]) else "gray" for u, v in G.edges()]
    
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=12, font_weight="bold", edge_color=edge_colors, width=2)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.suptitle("Shortest Path Finder for Cafés", fontsize=18, fontweight="bold", color="darkblue", y=1.00)
    plt.figtext(0.5, 0.92, f"Start: {path[0]} to {path[-1]}", fontsize=12, color="gray", ha="center")
    plt.figtext(0.5, 0.87, f"Path: {' → '.join(path)} (Total: {total_distance} km)", fontsize=12, color="gray", ha="center")
    
    plt.subplots_adjust(top=0.75)
    plt.show()

# 🔹 ฟังก์ชันแสดงคาเฟ่ใกล้เคียง

def draw_nearby_cafes(start, max_results=3):
    if start not in G:
        print(f"ไม่พบ {start} ในกราฟ")
        return
    
    nearby = sorted(G[start].items(), key=lambda x: x[1]["weight"])[:max_results]
    nearby_edges = [(start, cafe) for cafe, _ in nearby]
    
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    
    node_colors = ["red" if node == start else "green" if node in [cafe for cafe, _ in nearby] else "gray" for node in G.nodes()]
    edge_colors = ["green" if (start, cafe) in nearby_edges or (cafe, start) in nearby_edges else "gray" for (u, v) in G.edges()]
    
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=12, font_weight="bold", edge_color=edge_colors, width=2)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.suptitle("Nearby Cafés Finder", fontsize=18, fontweight="bold", color="darkblue", y=1.00)
    plt.figtext(0.5, 0.92, f"Start: {start}", fontsize=12, color="gray", ha="center")
    plt.figtext(0.5, 0.87, f"Nearby: {', '.join([cafe for cafe, _ in nearby])}", fontsize=12, color="gray", ha="center")
    
    plt.subplots_adjust(top=0.75)
    plt.show()

# 🔹 เมนูหลัก
while True:
    try:
        print("\n--- Café Route Finder ---")
        print("1. Set Start & Destination")
        print("2. Nearby Destinations")
        print("0. Exit")
        menu = int(input("Select menu: "))

        if menu == 1:
            print(f"{'-'*30}\n{'Cafe':10} | {'Name ':15} \n{'-'*30}")
            for cafe, name in dic_cafe.items():
                print(f"{cafe:10} | {name:20}\n{'-'*30}")

            start = input("Enter Start Café: ").strip().upper()
            destinations = [d.strip().upper() for d in input("Enter Destinations (comma separated ex: A,B): ").split(",")]

            if start not in G or any(dest not in G for dest in destinations):
                print("Invalid Café name(s). Try again.")
                continue

            path, distance = find_best_shortest_path(start, destinations)
            print(f"Best Path: {' → '.join(path)} (Total: {distance} km)")
            draw_shortest_path(path, distance)

        elif menu == 2:
            print(f"{'-'*30}\n{'Cafe':10} | {'Name ':15} \n{'-'*30}")
            for cafe, name in dic_cafe.items():
                print(f"{cafe:10} | {name:20}\n{'-'*30}")
            start = input("Enter Café to find nearby locations: ").strip().upper()
            if start not in G:
                print("Invalid Café name.")
                continue
            draw_nearby_cafes(start)

        elif menu == 0:
            print("Exit Program.")
            input("Press Enter to Exit... ")
            break

        else:
            print("Invalid selection. Please try again.")

    except Exception as e:
        print(f"Error: {e}. Try again.")
