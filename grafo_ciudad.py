import matplotlib.pyplot as plt


def build_static_city_graph():
    positions = {
        "Almacen": (0.0, 0.0),

        # Rama izquierda superior
        "N1": (-9.0, 8.2),
        "N22": (-8.2, 3.8),
        "N23": (-6.4, 6.0),
        "N20": (-4.0, 4.4),
        "N7": (-2.0, 4.0),

        # Rama izquierda inferior
        "N3": (-8.8, -7.2),
        "N5": (-6.4, -8.8),
        "N12": (-3.8, -2.2),
        "N14": (-2.0, -5.0),

        # Centro
        "N9": (-0.2, 4.8),
        "N18": (1.8, 5.0),
        "N11": (-0.8, -1.4),
        "N16": (1.0, 1.8),
        "N6": (4.2, 4.2),
        "N15": (3.0, 1.2),
        "N10": (2.5, -2.1),
        "N21": (1.5, -4.1),
        "N17": (4.2, -2.8),
        "N25": (6.2, -6.6),
        "N19": (5.2, 1.1),
        "N8": (4.8, -0.8),
        "N13": (5.8, 2.8),

        # Rama derecha
        "N2": (8.2, 7.8),
        "N24": (9.0, 4.0),
        "N4": (9.2, -4.5),
    }

    edges = [
    # Conexiones del almacén al núcleo
    ("Almacen", "N11"),
    ("Almacen", "N16"),
    ("Almacen", "N15"),

    # Rama izquierda superior
    ("N1", "N23"),
    ("N22", "N23"),
    ("N23", "N20"),
    ("N20", "N7"),
    ("N7", "N9"),

    # Rama izquierda inferior
    ("N3", "N5"),
    ("N5", "N14"),
    ("N14", "N12"),
    ("N12", "N11"),
    ("N3", "N12"),

    # Zona central
    ("N9", "N18"),
    ("N7", "N11"),
    ("N18", "N16"),
    ("N18", "N6"),
    ("N11", "N16"),
    ("N16", "N15"),
    ("N16", "N6"),
    ("N15", "N19"),
    ("N15", "N13"),
    ("N15", "N8"),
    ("N15", "N10"),
    ("N10", "N21"),
    ("N10", "N17"),
    ("N17", "N25"),
    ("N8", "N17"),
    ("N13", "N19"),
    ("N13", "N6"),
    ("N19", "N24"),
    ("N19", "N4"),
    ("N5", "N25"),

    # Rama derecha
    ("N6", "N2"),
    ("N2", "N24"),
    ("N17", "N4"),
    ("N14", "N21"),
    ]   

    return positions, edges


def plot_static_city_graph(save_path="grafo_ciudad.png"):
    positions, edges = build_static_city_graph()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F9FA")

    # Definir zonas para colorear nodos
    zona_izquierda = {"N1", "N22", "N23", "N20", "N7", "N3", "N5", "N12", "N14"}
    zona_centro = {"N9", "N18", "N11", "N16", "N6", "N15", "N10", "N21", "N17", "N25", "N19", "N8", "N13"}
    zona_derecha = {"N2", "N24", "N4"}

    # Dibujar aristas
    for a, b in edges:
        xa, ya = positions[a]
        xb, yb = positions[b]
        ax.plot(
            [xa, xb], [ya, yb],
            color="#8D99AE",
            linewidth=1.8,
            alpha=0.75,
            zorder=1
        )

    # Dibujar nodos por zona
    def draw_nodes(node_set, color, label):
        x = [positions[n][0] for n in node_set]
        y = [positions[n][1] for n in node_set]
        ax.scatter(
            x, y,
            s=110,
            color=color,
            edgecolors="white",
            linewidths=1.5,
            label=label,
            zorder=3
        )

    draw_nodes(zona_izquierda, "#4C78A8", "Zona izquierda")
    draw_nodes(zona_centro, "#54A24B", "Zona central")
    draw_nodes(zona_derecha, "#F58518", "Zona derecha")

    # Dibujar almacen
    wx, wy = positions["Almacen"]
    ax.scatter(
        [wx], [wy],
        s=220,
        marker="s",
        color="#E63946",
        edgecolors="white",
        linewidths=2,
        label="Almacén",
        zorder=4
    )

    # Etiquetas de nodos
    for nodo, (x, y) in positions.items():
        if nodo == "Almacen":
            continue
        ax.text(
            x + 0.08, y + 0.18, nodo,
            fontsize=8,
            color="#222222",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.7),
            zorder=5
        )

    # Titulo y formato
    ax.set_title("Grafo de la ciudad", fontsize=16, weight="bold", pad=15)
    ax.set_xlabel("Coordenada X", fontsize=11)
    ax.set_ylabel("Coordenada Y", fontsize=11)

    ax.grid(True, linestyle="--", alpha=0.25)
    ax.set_aspect("equal")

    # Limites para que mejore el grafo
    ax.set_xlim(-10.5, 11)
    ax.set_ylim(-10.2, 10.2)

    plt.tight_layout()
    plt.savefig(save_path, dpi=250, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    plot_static_city_graph()