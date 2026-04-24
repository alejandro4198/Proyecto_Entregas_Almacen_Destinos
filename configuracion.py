from dataclasses import dataclass

@dataclass
class SimulationConfig:
    # Tiempo
    jornada_horas: float = 12.0

    # Warehouse
    capacidad_warehouse: int = 10000

    # Ciudad
    num_nodos_entrega: int = 24
    distancia_min_km: float = 2.0
    distancia_max_km: float = 20.0

    # Llegadas
    tasa_baja_demanda: float = 8.0   # paquetes por hora
    tasa_alta_demanda: float = 18.0  # paquetes por hora

    # Flota
    num_motos: int = 10
    num_furgonetas: int = 4
    capacidad_moto: int = 1
    capacidad_furgoneta: int = 10

    # Velocidades
    vel_moto_min: float = 30.0
    vel_moto_max: float = 60.0
    vel_furgoneta_min: float = 20.0
    vel_furgoneta_max: float = 55.0

    # Costos
    costo_moto: float = 5_900_000
    costo_furgoneta: float = 110_000_000
    amortizacion_anos: int = 10

    salario_mensual_empleado: float = 3_000_000
    dias_mes: int = 30

    precio_gasolina_litro: float = 15_891
    consumo_moto_litro_km: float = 0.03
    costo_energia_furgoneta_km: float = 800.0

    ingreso_por_envio: float = 80_000

    # Réplicas
    replicas_por_escenario: int = 1000

    # Cajas
    precio_caja_pequena: float = 30_000
    precio_caja_mediana: float = 80_000

    peso_min_pequena: float = 0.5   # kg
    peso_max_pequena: float = 12.0  # kg

    peso_min_mediana: float = 5.0   # kg
    peso_max_mediana: float = 30.0  # kg

    # Reducción de velocidad en moto según peso
    reduccion_moto_liviana_min: float = 0.00
    reduccion_moto_liviana_max: float = 0.03

    reduccion_moto_media_min: float = 0.04
    reduccion_moto_media_max: float = 0.09

    reduccion_moto_pesada_min: float = 0.10
    reduccion_moto_pesada_max: float = 0.15

    # Reducción de velocidad en furgoneta según peso
    reduccion_furgoneta_liviana_min: float = 0.00
    reduccion_furgoneta_liviana_max: float = 0.02

    reduccion_furgoneta_media_min: float = 0.03
    reduccion_furgoneta_media_max: float = 0.08

    reduccion_furgoneta_pesada_min: float = 0.09
    reduccion_furgoneta_pesada_max: float = 0.15

    # Escenario mixto
    num_motos_mixto: int = 5
    num_furgonetas_mixto: int = 2

    @property
    def salario_diario(self) -> float:
        return self.salario_mensual_empleado / self.dias_mes

    @property
    def costo_diario_moto(self) -> float:
        return self.costo_moto / (self.amortizacion_anos * 365)

    @property
    def costo_diario_furgoneta(self) -> float:
        return self.costo_furgoneta / (self.amortizacion_anos * 365)
