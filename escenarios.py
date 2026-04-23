from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    demand_rate_per_hour: float
    fleet_type: str  # "motos", "furgonetas", "mixto"
    description: str


def build_scenarios(config):
    return [
        Scenario(
            name="A1",
            demand_rate_per_hour=config.tasa_alta_demanda,
            fleet_type="motos",
            description="Alta demanda con flota de motos"
        ),
        Scenario(
            name="A2",
            demand_rate_per_hour=config.tasa_baja_demanda,
            fleet_type="motos",
            description="Baja demanda con flota de motos"
        ),
        Scenario(
            name="B1",
            demand_rate_per_hour=config.tasa_alta_demanda,
            fleet_type="furgonetas",
            description="Alta demanda con furgonetas"
        ),
        Scenario(
            name="B2",
            demand_rate_per_hour=config.tasa_baja_demanda,
            fleet_type="furgonetas",
            description="Baja demanda con furgonetas"
        ),
        Scenario(
            name="C",
            demand_rate_per_hour=config.tasa_baja_demanda,
            fleet_type="motos",
            description="Escenario adicional; luego puede adaptarse a demanda variable"
        ),
    ]