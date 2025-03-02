import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# สร้างกราฟ
G = nx.Graph()
cafes = ["Cafe A", "Cafe B", "Cafe C", "Cafe D", "Cafe E"]
G.add_nodes_from(cafes)

edges = [
    ("Cafe A", "Cafe B", 3),
    ("Cafe A", "Cafe D", 2),
    ("Cafe B", "Cafe D", 4),
    ("Cafe B", "Cafe E", 7),
    ("Cafe C", "Cafe D", 6),
    ("Cafe C", "Cafe E", 5),
    ("Cafe D", "Cafe E", 8)
]
G.add_weighted_edges_from(edges)

# ฟังก์ชันหาเส้นทางที่ดีที่สุด
def find_best_shortest_path(start, destinations):

    if len(destinations) == 1:
        # ถ้ามีแค่จุดหมายเดียว ใช้ Dijkstra ปกติ
        end = destinations[0]
        path = nx.shortest_path(G, source=start, target=end, weight="weight")
        distance = nx.shortest_path_length(G, source=start, target=end, weight="weight")
        return path, distance
    
    best_path = None
    best_distance = float("inf")
    best_detailed_info = None

    # ลองทุกลำดับของจุดหมายปลายทาง
    for perm in permutations(destinations):
        path = [start]
        total_distance = 0
        detailed_path_info = []
        current_location = start

        for next_stop in perm:
            sub_path = nx.shortest_path(G, source=current_location, target=next_stop, weight="weight")
            sub_distance = nx.shortest_path_length(G, source=current_location, target=next_stop, weight="weight")

            # เพิ่มข้อมูลเส้นทาง
            for i in range(len(sub_path) - 1):
                u, v = sub_path[i], sub_path[i + 1]
                dist = G[u][v]['weight']
                detailed_path_info.append(f"{u} → {v} : ({dist} km)")

            # รวมเส้นทาง
            path.extend(sub_path[1:])
            total_distance += sub_distance
            current_location = next_stop

        # เลือกเส้นทางที่ดีที่สุด (ระยะทางรวมสั้นที่สุด)
        if total_distance < best_distance:
            best_distance = total_distance
            best_path = path
            best_detailed_info = detailed_path_info

    return best_path, best_distance, best_detailed_info

# 🔹 ทดสอบหาเส้นทางจาก Cafe A ไป Cafe C และ Cafe E
start = "Cafe A"
destinations = ["Cafe C", "Cafe E"]
shortest_path, total_distance, path_details = find_best_shortest_path(start, destinations)

# 🔹 วาดกราฟ
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(8, 8))

nx.draw(G, pos, with_labels=True, node_size=3000, node_color="#90CAF9", font_size=12, font_weight="bold", edge_color="gray", width=2)
# 🔹 ไฮไลท์เส้นทางที่ดีที่สุด
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2.5)  # ลดความหนาลงเล็กน้อย

# 🔹 ปรับตำแหน่งตัวเลขน้ำหนัก
edge_labels = {(u, v): w for u, v, w in edges}
label_pos = {}

for (u, v) in edge_labels:
    x_mid = (pos[u][0] + pos[v][0]) / 2  # จุดกึ่งกลางเส้น
    y_mid = (pos[u][1] + pos[v][1]) / 2  

    # ขยับตัวเลขขึ้น-ลงตามแนวเส้น
    if (u, v) in path_edges or (v, u) in path_edges:
        y_mid += 0.08  # ขยับขึ้นเพิ่มจากเส้นสีแดง
        x_mid += 0.02  # ขยับออกจากจุดกึ่งกลางเล็กน้อย

    label_pos[(u, v)] = (x_mid, y_mid)

# 🔹 วาดตัวเลขน้ำหนักแบบชัดเจน
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10,
                             bbox=dict(facecolor="white", edgecolor="none", alpha=1), 
                             verticalalignment='center', horizontalalignment='center', rotate=False)



# 🔹 แสดงผลลัพธ์
plt.suptitle("Best Shortest Path Finder for Cafés", fontsize=18, fontweight="bold", color="darkblue", y=1.00)
plt.figtext(0.5, 0.92, f"Best Path: {shortest_path} (Total: {total_distance} km)", fontsize=12, color="gray", ha="center")
plt.figtext(0.5, 0.85, "Route Details:\n" + "| → |".join(path_details), fontsize=11, color="green", ha="center", bbox=dict(facecolor="white", alpha=0.7))
plt.subplots_adjust(top=0.75)

plt.show()


