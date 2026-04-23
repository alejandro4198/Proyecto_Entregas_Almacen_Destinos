import matplotlib.pyplot as plt

def build_static_city_graph():
    positions = {
        "Almacen": (0, 0),

        "N1": (3, 0),   "N2": (2.5, 2.2), "N3": (0, 3.7),   "N4": (-2.3, 2.0),
        "N5": (-3, 0),  "N6": (-2.6, -2.3), "N7": (0, -3.1), "N8": (2.6, -2.4),

        "N9": (6.5, -0.5),  "N10": (3.8, 4.5), "N11": (0, 6.7),   "N12": (-4.1, 4.5),
        "N13": (-6.3, -0.7), "N14": (-4.7, -3.8), "N15": (0.6, -6.6), "N16": (5.1, -4.5),

        "N17": (9.6, 0.1),  "N18": (6.6, 6.2), "N19": (-0.8, 9.1), "N20": (-6.9, 5.9),
        "N21": (-8.5, -0.4), "N22": (-6.5, -5.8), "N23": (-0.9, -8.6), "N24": (5.9, -6.7),
    }

    edges = []

    # 1) El almacén SOLO se conecta con algunos nodos cercanos
    edges += [
        ("Almacen", "N1"),
        ("Almacen", "N3"),
        ("Almacen", "N5"),
        ("Almacen", "N7"),
    ]

    # 2) Anillo interno
    edges += [
        ("N1", "N2"), ("N2", "N3"), ("N3", "N4"), ("N4", "N5"),
        ("N5", "N6"), ("N6", "N7"), ("N7", "N8"), ("N8", "N1")
    ]

    # 3) Conexiones del anillo interno al intermedio
    edges += [
        ("N1", "N9"),
        ("N2", "N10"),
        ("N3", "N11"),
        ("N4", "N12"),
        ("N5", "N13"),
        ("N6", "N14"),
        ("N7", "N15"),
        ("N8", "N16"),
    ]

    # 4) Anillo intermedio
    edges += [
        ("N9", "N10"), ("N10", "N11"), ("N11", "N12"), ("N12", "N13"),
        ("N13", "N14"), ("N14", "N15"), ("N15", "N16"), ("N16", "N9")
    ]

    # 5) Conexiones del intermedio al anillo lejano
    edges += [
        ("N9", "N17"),
        ("N10", "N18"),
        ("N11", "N19"),
        ("N12", "N20"),
        ("N13", "N21"),
        ("N14", "N22"),
        ("N15", "N23"),
        ("N16", "N24"),
    ]

    # 6) Anillo externo
    edges += [
        ("N17", "N18"), ("N18", "N19"), ("N19", "N20"), ("N20", "N21"),
        ("N21", "N22"), ("N22", "N23"), ("N23", "N24"), ("N24", "N17")
    ]

    # 7) Algunas conexiones extra, pero pocas, para dar realismo
    edges += [
        ("N10", "N18"),
        ("N12", "N20"),
        ("N14", "N22"),
        ("N16", "N24"),
        ("N9", "N17"),
        ("N11", "N19"),
    ]

    return positions, edges


def plot_static_city_graph(save_path="grafo_ciudad_estatico.png"):
    positions, edges = build_static_city_graph()

    fig, ax = plt.subplots(figsize=(10, 10))

    # Dibujar aristas
    for a, b in edges:
        xa, ya = positions[a]
        xb, yb = positions[b]
        ax.plot([xa, xb], [ya, yb], linewidth=1.0, alpha=0.45)

    # Dibujar nodos de entrega
    x_nodes = [positions[f"N{i}"][0] for i in range(1, 25)]
    y_nodes = [positions[f"N{i}"][1] for i in range(1, 25)]
    ax.scatter(x_nodes, y_nodes, s=80, label="Nodos de entrega")

    # Dibujar almacén
    wx, wy = positions["Almacen"]
    ax.scatter([wx], [wy], s=180, marker="s", label="Almacén")

    # Etiquetas
    ax.text(wx + 0.25, wy + 0.25, "Almacén", fontsize=11, weight="bold")
    for i in range(1, 25):
        x, y = positions[f"N{i}"]
        ax.text(x + 0.12, y + 0.12, f"N{i}", fontsize=8)

    ax.set_title("Grafo de la ciudad")
    ax.set_xlabel("Coordenada X")
    ax.set_ylabel("Coordenada Y")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.show()