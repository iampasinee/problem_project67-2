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
def draw_nearby_cafes(start, max_results=3):
    """ วาดกราฟและไฮไลต์คาเฟ่ที่อยู่ใกล้กับจุดที่เลือก """
    if start not in G:
        print(f"❌ ไม่พบ {start} ในกราฟ")
        return
    
    # หาคาเฟ่ใกล้เคียง
    nearby = sorted(G[start].items(), key=lambda x: x[1]["weight"])[:max_results]
    nearby_edges = [(start, cafe) for cafe, _ in nearby]

    # วาดกราฟ
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # วาดโหนดและเส้นขอบเขตทั้งหมด
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="#90CAF9", font_size=12, font_weight="bold", edge_color="gray", width=2)
    
    # ไฮไลต์คาเฟ่ที่อยู่ใกล้ด้วยเส้นสีเขียว
    nx.draw_networkx_edges(G, pos, edgelist=nearby_edges, edge_color="green", width=2.5)
    
    # แสดงตัวเลขระยะทางบนเส้น
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # เพิ่มหัวข้อ
    plt.title(f"Nearby Cafés from {start}", fontsize=16, fontweight="bold", color="darkgreen")
    
    plt.show()

# 🔹 ทดสอบวาดกราฟคาเฟ่ใกล้ Cafe A
selected_cafe = "Cafe A"
draw_nearby_cafes(selected_cafe)
