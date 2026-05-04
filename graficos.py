import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTADOS_DETALLADOS = "resultados_detallados.csv"
RESUMEN_ESCENARIOS = "resumen_escenarios.csv"
CARPETA_SALIDA = "graficos"

def asegurar_carpeta_salida():
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

def cargar_datos():
    df_detallado = pd.read_csv(RESULTADOS_DETALLADOS)
    df_resumen = pd.read_csv(RESUMEN_ESCENARIOS)
    return df_detallado, df_resumen

# Cajas y bigotes
def boxplot_variable(df, variable, titulo, ylabel, nombre_archivo):
    escenarios = sorted(df["scenario"].unique())
    datos = [df[df["scenario"] == esc][variable].dropna() for esc in escenarios]

    plt.figure(figsize=(10, 6))
    plt.boxplot(datos, tick_labels=escenarios)
    plt.title(titulo)
    plt.xlabel("Escenario")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_SALIDA, nombre_archivo), dpi=200)
    plt.show()

# Barras
def barplot_promedios(df_resumen):
    escenarios = df_resumen["scenario"]

    # Ajuste de nombre
    delivered = df_resumen["delivered_mean"]
    delivery_time = df_resumen["delivery_time_mean"]
    cost = df_resumen["cost_mean"]
    profit = df_resumen["profit_mean"]

    # 1. Paquetes entregados promedio
    plt.figure(figsize=(10, 6))
    plt.bar(escenarios, delivered)
    plt.title("Paquetes entregados promedio por escenario")
    plt.xlabel("Escenario")
    plt.ylabel("Paquetes entregados promedio")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_SALIDA, "barras_paquetes_entregados.png"), dpi=200)
    plt.show()

    # 2. Tiempo promedio de entrega
    plt.figure(figsize=(10, 6))
    plt.bar(escenarios, delivery_time)
    plt.title("Tiempo promedio de entrega por escenario")
    plt.xlabel("Escenario")
    plt.ylabel("Tiempo promedio de entrega (horas)")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_SALIDA, "barras_tiempo_entrega.png"), dpi=200)
    plt.show()

    # 3. Costo promedio
    plt.figure(figsize=(10, 6))
    plt.bar(escenarios, cost)
    plt.title("Costo operativo promedio por escenario")
    plt.xlabel("Escenario")
    plt.ylabel("Costo promedio (COP)")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_SALIDA, "barras_costo_promedio.png"), dpi=200)
    plt.show()

    # 4. Utilidad promedio
    plt.figure(figsize=(10, 6))
    plt.bar(escenarios, profit)
    plt.title("Utilidad bruta promedio por escenario")
    plt.xlabel("Escenario")
    plt.ylabel("Utilidad promedio (COP)")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_SALIDA, "barras_utilidad_promedio.png"), dpi=200)
    plt.show()

# Histogramas
def histogramas_tiempo_entrega(df):
    escenarios = sorted(df["scenario"].unique())

    for esc in escenarios:
        datos = df[df["scenario"] == esc]["average_delivery_time"].dropna()

        plt.figure(figsize=(10, 6))
        plt.hist(datos, bins=10)
        plt.title(f"Histograma del tiempo promedio de entrega - Escenario {esc}")
        plt.xlabel("Tiempo promedio de entrega (horas)")
        plt.ylabel("Frecuencia")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(
            os.path.join(CARPETA_SALIDA, f"hist_tiempo_entrega_{esc}.png"),
            dpi=200
        )
        plt.show()


def main():
    asegurar_carpeta_salida()
    df_detallado, df_resumen = cargar_datos()

    # Cajas y bigotes
    boxplot_variable(
        df_detallado,
        variable="average_delivery_time",
        titulo="Boxplot del tiempo promedio de entrega por escenario",
        ylabel="Tiempo promedio de entrega (horas)",
        nombre_archivo="boxplot_tiempo_entrega.png"
    )

    boxplot_variable(
        df_detallado,
        variable="total_cost",
        titulo="Boxplot del costo operativo total por escenario",
        ylabel="Costo total (COP)",
        nombre_archivo="boxplot_costo_total.png"
    )

    boxplot_variable(
        df_detallado,
        variable="gross_profit",
        titulo="Boxplot de utilidad bruta por escenario",
        ylabel="Utilidad bruta (COP)",
        nombre_archivo="boxplot_utilidad_bruta.png"
    )

    # Barras
    barplot_promedios(df_resumen)

    # Histogramas
    histogramas_tiempo_entrega(df_detallado)

    print("\nGraficos generados correctamente en la carpeta 'graficos'.") 
    #Verificacion de creacion de diagramas y carpeta, por si acaso :)


if __name__ == "__main__":
    main()