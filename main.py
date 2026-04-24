import pandas as pd
from configuracion import SimulationConfig
from escenarios import build_scenarios
from analisis import run_replicas, summarize_results
from grafo_ciudad import plot_static_city_graph

def main():
    config = SimulationConfig()
    scenarios = build_scenarios(config)

    all_results = []
    for scenario in scenarios[:]:  # primero los obligatorios -> Sin restricciones de escenarios
        df = run_replicas(config, scenario)
        all_results.append(df)

    if not all_results:
        print("No se generaron resultados. Revisa la configuración de escenarios.")
        return

    final_df = pd.concat(all_results, ignore_index=True)

    summary = summarize_results(final_df)

    print("\n=== RESULTADOS DETALLADOS ===")
    print(final_df.head())

    print("\n=== RESUMEN ===")
    print(summary)

    final_df.to_csv("resultados_detallados.csv", index=False)
    summary.to_csv("resumen_escenarios.csv", index=False)

if __name__ == "__main__":
    main()
    plot_static_city_graph()