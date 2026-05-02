import pandas as pd

df = pd.read_csv("casos_representativos.csv")

filas = []
for esc in sorted(df["scenario"].unique()):
    sub = df[df["scenario"] == esc]

    fila = {"scenario": esc}

    # Tiempo
    fila["mejor_tiempo"] = sub[sub["tipo_caso"] == "mejor_average_delivery_time"]["average_delivery_time"].values[0]
    fila["peor_tiempo"] = sub[sub["tipo_caso"] == "peor_average_delivery_time"]["average_delivery_time"].values[0]
    fila["promedio_tiempo"] = sub[sub["tipo_caso"] == "promedio_average_delivery_time"]["average_delivery_time"].values[0]

    # Costo
    fila["mejor_costo"] = sub[sub["tipo_caso"] == "mejor_total_cost"]["total_cost"].values[0]
    fila["peor_costo"] = sub[sub["tipo_caso"] == "peor_total_cost"]["total_cost"].values[0]
    fila["promedio_costo"] = sub[sub["tipo_caso"] == "promedio_total_cost"]["total_cost"].values[0]

    # Utilidad
    fila["mejor_utilidad"] = sub[sub["tipo_caso"] == "mejor_gross_profit"]["gross_profit"].values[0]
    fila["peor_utilidad"] = sub[sub["tipo_caso"] == "peor_gross_profit"]["gross_profit"].values[0]
    fila["promedio_utilidad"] = sub[sub["tipo_caso"] == "promedio_gross_profit"]["gross_profit"].values[0]

    filas.append(fila)

df_resumen = pd.DataFrame(filas)
df_resumen.to_csv("tabla_casos_resumen.csv", index=False)

print("\n=== TABLA RESUMEN DE CASOS ===")
print(df_resumen)
print("\nArchivo generado: tabla_casos_resumen.csv")