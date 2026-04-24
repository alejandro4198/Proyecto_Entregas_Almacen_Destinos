import pandas as pd

from simulacion import run_single_simulation

def run_replicas(config, scenario):
    results = []
    for rep in range(config.replicas_por_escenario):
        #seed = 1000 + rep #usar una semilla para tener resultados similares, para investigacion
        #result = run_single_simulation(config, scenario, seed=seed)
        result = run_single_simulation(config, scenario)
        results.append(result)
    return pd.DataFrame(results)

def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("scenario").agg(
        delivered_mean=("delivered_packages", "mean"),
        delivered_std=("delivered_packages", "std"),
        pending_mean=("pending_packages", "mean"),
        delivery_time_mean=("average_delivery_time", "mean"),
        delivery_time_std=("average_delivery_time", "std"),
        cost_mean=("total_cost", "mean"),
        cost_std=("total_cost", "std"),
        profit_mean=("gross_profit", "mean"),
        profit_std=("gross_profit", "std"),
    ).reset_index()
    return summary