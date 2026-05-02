import pandas as pd

ARCHIVO_ENTRADA = "tabla_casos_resumen.csv"
ARCHIVO_SALIDA = "tabla_casos_presentacion.csv"


def formatear_cop(valor):
    return f"{valor:,.0f}".replace(",", ".")


def main():
    df = pd.read_csv(ARCHIVO_ENTRADA)

    # Redondear tiempos
    columnas_tiempo = [
        "mejor_tiempo", "peor_tiempo", "promedio_tiempo"
    ]
    for col in columnas_tiempo:
        df[col] = df[col].round(3)

    # Formatear costos y utilidades
    columnas_costo_utilidad = [
        "mejor_costo", "peor_costo", "promedio_costo",
        "mejor_utilidad", "peor_utilidad", "promedio_utilidad"
    ]
    for col in columnas_costo_utilidad:
        df[col] = df[col].apply(formatear_cop)

    # Renombrar columnas para que se vean mejor
    df = df.rename(columns={
        "scenario": "Escenario",
        "mejor_tiempo": "Mejor tiempo (h)",
        "peor_tiempo": "Peor tiempo (h)",
        "promedio_tiempo": "Caso promedio tiempo (h)",
        "mejor_costo": "Mejor costo (COP)",
        "peor_costo": "Peor costo (COP)",
        "promedio_costo": "Caso promedio costo (COP)",
        "mejor_utilidad": "Mejor utilidad (COP)",
        "peor_utilidad": "Peor utilidad (COP)",
        "promedio_utilidad": "Caso promedio utilidad (COP)"
    })

    df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")

    print("\n=== TABLA PARA PRESENTACIÓN ===")
    print(df)
    print(f"\nArchivo generado: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()