from dataclasses import dataclass, field


@dataclass
class Package:
    package_id: int
    arrival_time: float
    destination_node: int
    distance_km: float
    category: str         # "pequena" o "mediana"
    weight_kg: float
    shipping_price: float

@dataclass
class Vehicle:
    vehicle_id: int
    vehicle_type: str  # "moto" o "furgoneta"
    available: bool = True
    trips_completed: int = 0
    busy_time: float = 0.0


@dataclass
class SimulationMetrics:
    delivered_packages: int = 0
    pending_packages: int = 0

    total_delivery_time: float = 0.0
    total_waiting_time: float = 0.0

    total_cost: float = 0.0
    total_income: float = 0.0

    total_distance_moto: float = 0.0
    total_distance_furgoneta: float = 0.0

    moto_trips: int = 0
    furgoneta_trips: int = 0

    @property
    def average_delivery_time(self) -> float:
        if self.delivered_packages == 0:
            return 0.0
        return self.total_delivery_time / self.delivered_packages

    @property
    def average_waiting_time(self) -> float:
        if self.delivered_packages == 0:
            return 0.0
        return self.total_waiting_time / self.delivered_packages

    @property
    def utilidad_bruta(self) -> float:
        return self.total_income - self.total_cost