import pandas as pd

ARCHIVO_ENTRADA = "resultados_detallados.csv"
ARCHIVO_SALIDA = "casos_representativos.csv"


def obtener_casos_por_metrica(df, scenario, metrica, criterio="min"):
    """
    criterio = "min" si un valor más bajo es mejor
    criterio = "max" si un valor más alto es mejor
    """
    df_esc = df[df["scenario"] == scenario].copy()

    # Mejor y peor caso
    if criterio == "min":
        idx_mejor = df_esc[metrica].idxmin()
        idx_peor = df_esc[metrica].idxmax()
    else:
        idx_mejor = df_esc[metrica].idxmax()
        idx_peor = df_esc[metrica].idxmin()

    mejor = df_esc.loc[idx_mejor].copy()
    peor = df_esc.loc[idx_peor].copy()

    # Caso promedio = corrida más cercana a la media
    media = df_esc[metrica].mean()
    df_esc["dist_media"] = (df_esc[metrica] - media).abs()
    idx_promedio = df_esc["dist_media"].idxmin()
    promedio = df_esc.loc[idx_promedio].copy()

    mejor["tipo_caso"] = f"mejor_{metrica}"
    peor["tipo_caso"] = f"peor_{metrica}"
    promedio["tipo_caso"] = f"promedio_{metrica}"

    return [mejor, peor, promedio]


def main():
    df = pd.read_csv(ARCHIVO_ENTRADA)

    escenarios = sorted(df["scenario"].unique())
    resultados = []

    for esc in escenarios:
        # Tiempo de entrega: menor es mejor
        resultados.extend(
            obtener_casos_por_metrica(df, esc, "average_delivery_time", criterio="min")
        )

        # Costo total: menor es mejor
        resultados.extend(
            obtener_casos_por_metrica(df, esc, "total_cost", criterio="min")
        )

        # Utilidad: mayor es mejor
        resultados.extend(
            obtener_casos_por_metrica(df, esc, "gross_profit", criterio="max")
        )

    df_resultados = pd.DataFrame(resultados)

    # Quitar columna auxiliar si existe
    if "dist_media" in df_resultados.columns:
        df_resultados = df_resultados.drop(columns=["dist_media"])

    df_resultados.to_csv(ARCHIVO_SALIDA, index=False)

    print("\n=== CASOS REPRESENTATIVOS ===")
    print(
        df_resultados[
            [
                "scenario",
                "tipo_caso",
                "seed",
                "delivered_packages",
                "pending_packages",
                "average_delivery_time",
                "total_cost",
                "gross_profit",
            ]
        ]
    )
    print(f"\nArchivo generado: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()