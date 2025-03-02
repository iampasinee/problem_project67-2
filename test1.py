import networkx as nx
import matplotlib.pyplot as plt

# สร้างกราฟ
G = nx.Graph()

# เพิ่มโหนด (คาเฟ่)
cafes = ["Cafe A", "Cafe B", "Cafe C", "Cafe D", "Cafe E"]
G.add_nodes_from(cafes)

# เพิ่มเส้นเชื่อมพร้อมน้ำหนัก
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

# ฟังก์ชันหาเส้นทางที่สั้นที่สุด
def find_shortest_path(start, end):
    path = nx.shortest_path(G, source=start, target=end, weight="weight")
    distance = nx.shortest_path_length(G, source=start, target=end, weight="weight")
    return path, distance

# ทดสอบหาเส้นทางจาก Cafe A ไป Cafe E
start, end = "Cafe A", "Cafe E"
shortest_path, total_distance = find_shortest_path(start, end)

# ตำแหน่งโหนด
pos = nx.spring_layout(G, seed=42)

# 🔹 ปรับขนาดกราฟให้มีพื้นที่มากขึ้น
fig, ax = plt.subplots(figsize=(8, 8))

# วาดโหนดและเส้นเชื่อม
nx.draw(G, pos, with_labels=True, 
        node_size=3000, node_color="#90CAF9",  
        font_size=12, font_weight="bold", edge_color="gray", width=2)

# ใส่น้ำหนักบนเส้นเชื่อม
edge_labels = {(u, v): w for u, v, w in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, bbox=dict(facecolor="white", alpha=0.7))

# ไฮไลต์เส้นทางที่สั้นที่สุด
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)

# 🔹 เพิ่ม Title และ Subtitle ให้สูงขึ้น + ลดขนาด Subtitle
plt.suptitle("Shortest Path Finder for Cafés", fontsize=18, fontweight="bold", color="darkblue", y=1.00)
plt.figtext(0.5, 0.92, f"Start: {start} to {end}", fontsize=12, color="gray", ha="center")
plt.figtext(0.5, 0.87, f"Path: {shortest_path} (Total: {total_distance} km)", 
            fontsize=12, color="gray", ha="center")

# ปรับพื้นที่ด้านบนให้ Title ไม่ทับกราฟ
plt.subplots_adjust(top=0.75)

# แสดงกราฟ
plt.show()
