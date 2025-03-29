"""
เส้นทางคาเฟ่ จังหวัดปราจีนบุรี
"""
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# 🔹 สร้างกราฟ
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

cafes = ["A", "B", "C", "D", "E", "F", "G","H","I"]
G.add_nodes_from(cafes)

# เพิ่มข้อมูลชื่อคาเฟ่เป็น attribute ของแต่ละโหนด
for cafe, name in dic_cafe.items():
    G.nodes[cafe]["name"] = name

edges = [
    ("A", "B", 12),
    ("A", "C", 10),
    ("B", "C", 13),
    ("B", "D", 7),
    ("D", "G", 12),
    ("E", "F", 9),
    ("G", "H", 2),
    ("G", "I", 5),
    ("I", "E", 11),
    ("I", "F", 3),
    ("H", "I", 9),
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

# Function to split text into lines if it exceeds a certain length
def wrap_text(text, max_length=100):
    lines = []
    current_line = ""
    
    for word in text.split():
        if len(current_line + " " + word) <= max_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

# Function to draw the shortest path with wrapped text
def draw_shortest_path(path, total_distance):
    plt.figure(figsize=(8, 8))
    pos = {
        "A":(2,6), "B":(1,3), "C":(-0.2,8), "D":(1,0),
        "E":(7,1.2), "F":(4,4), "G":(3,-4), "H":(5,-5), "I":(3,2)
    }

    destination_set = set(destinations) 
    node_colors = [
        "pink" if node == path[0] else 
        "skyblue" if node in destination_set or node == destinations[-1] else
        "lightgreen" if node in path else
        "lightgray"
        for node in G.nodes()
    ]
    #node_colors = ["pink" if node == path[0] or node == path[-1] else "lightgreen" if node in path else "lightgray" for node in G.nodes()]
    edge_colors = ["lightgreen" if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]) else "lightgray" for u, v in G.edges()]

    # Draw the graph
    nx.draw(G, pos, with_labels=False, node_size=1800, node_color=node_colors, font_size=15, font_weight="bold", edge_color=edge_colors, width=2)

    # Adjust labels position slightly so they don't overlap with nodes
    labels = nx.get_node_attributes(G, "name")
    label_pos = {node: (x + 0.05, y + 0.05) if node == path[0] else (x, y) for node, (x, y) in pos.items()}  # Slight offset
    nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=10, font_color="black")

    # Draw edge labels (distances)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Title and path description
    plt.suptitle("Shortest Path Finder for Cafés", fontsize=18, fontweight="bold", color="darkblue", y=1.00)

    # Format the start and end text with full cafe names and wrap the text
    start_end_text = f"Start: {dic_cafe.get(path[0], path[0])} to {dic_cafe.get(path[-1], path[-1])}"
    path_text = f"Path: {' → '.join([dic_cafe.get(cafe, cafe) for cafe in path])} (Total: {total_distance} km)"
    
    # Wrap the text if it's too long
    start_end_text_wrapped = wrap_text(start_end_text, max_length=70)
    path_text_wrapped = wrap_text(path_text, max_length=80)

    # Display wrapped text in the plot
    plt.figtext(0.5, 0.1, start_end_text_wrapped, fontsize=12, color="gray", ha="center")
    plt.figtext(0.5, 0.03, path_text_wrapped, fontsize=12, color="gray", ha="center")

    # Show plot with margin adjustments
    plt.subplots_adjust(top=0.25)
    plt.margins(0.3)
    plt.show()


#ฟังก์ชันแสดงคาเฟ่ใกล้เคียง
def draw_nearby_cafes(start, max_results=3):
    if start not in G:
        print(f"ไม่พบ {start} ในกราฟ")
        return

    nearby = sorted(G[start].items(), key=lambda x: x[1]["weight"])[:max_results]
    nearby_edges = [(start, cafe) for cafe, _ in nearby]

    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    pos = {
        "A":(2,6), "B":(1,3), "C":(-0.2,8), "D":(1,0),
        "E":(7,1.2), "F":(4,4), "G":(3,-4), "H":(5,-5), "I":(3,2)
    }

    node_colors = ["pink" if node == start else "lightgreen" if node in [cafe for cafe, _ in nearby] else "lightgray" for node in G.nodes()]
    edge_colors = ["lightgray" if (start, cafe) in nearby_edges or (cafe, start) in nearby_edges else "lightgray" for (u, v) in G.edges()]

    nx.draw(G, pos, with_labels=False, node_size=1500, node_color=node_colors, font_size=12, font_weight="bold", edge_color=edge_colors, width=2)

    labels = nx.get_node_attributes(G, "name")
    label_pos = {node: (x + 0.05, y + 0.05) if node == start else (x, y) for node, (x, y) in pos.items()}  # Slight offset
    nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=10, font_color="black")

    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.suptitle("Nearby Cafés Finder", fontsize=18, fontweight="bold", color="darkblue", y=1.00)
    plt.figtext(0.5, 0.07, f"Start: {dic_cafe.get(start, start)}", fontsize=12, color="gray", ha="center")
    plt.figtext(0.5, 0.03, f"Nearby: {', '.join([dic_cafe.get(cafe, cafe) for cafe, _ in nearby])}", fontsize=12, color="gray", ha="center")
    plt.subplots_adjust(top=0.25)
    plt.margins(0.2)
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
