import random

def sample_interarrival_time(rate_per_hour: float) -> float:
    """
    Genera el tiempo entre llegadas con distribución exponencial,
    consistente con un proceso de Poisson.
    Retorna tiempo en horas.
    """
    if rate_per_hour <= 0:
        raise ValueError("La tasa de llegada debe ser positiva.")
    return random.expovariate(rate_per_hour)


def sample_uniform(a: float, b: float) -> float:
    return random.uniform(a, b)


def sample_destination_node(num_nodes: int) -> int:
    return random.randint(1, num_nodes)


def sample_distance_km(min_km: float, max_km: float) -> float:
    return random.uniform(min_km, max_km)


def calculate_round_trip_time_hours(distance_km: float, speed_kmh: float) -> float:
    """
    Modelo simple: ida + regreso.
    """
    return (2 * distance_km) / speed_kmh


def calculate_furgoneta_trip_time_hours(avg_distance_km: float, speed_kmh: float) -> float:
    """
    Modelo simplificado para furgoneta:
    distancia promedio de entrega * factor + regreso.
    """
    route_factor = 1.6
    return (avg_distance_km * route_factor + avg_distance_km) / speed_kmh


def sample_package_category():
    """
    Puedes ajustar probabilidades si quieres.
    Por ahora: 70% pequeñas, 30% medianas.
    """
    return random.choices(
        ["pequena", "mediana"],
        weights=[0.7, 0.3],
        k=1
    )[0]


def sample_package_weight(config, category: str) -> float:
    if category == "pequena":
        return random.uniform(config.peso_min_pequena, config.peso_max_pequena)
    elif category == "mediana":
        return random.uniform(config.peso_min_mediana, config.peso_max_mediana)
    else:
        raise ValueError(f"Categoría desconocida: {category}")


def get_shipping_price(config, category: str) -> float:
    if category == "pequena":
        return config.precio_caja_pequena
    elif category == "mediana":
        return config.precio_caja_mediana
    else:
        raise ValueError(f"Categoría desconocida: {category}")


def get_speed_reduction(config, vehicle_type: str, weight_kg: float) -> float:
    """
    Retorna una reducción porcentual entre 0 y 1.
    """

    if vehicle_type == "moto":
        if weight_kg < 3:
            return random.uniform(
                config.reduccion_moto_liviana_min,
                config.reduccion_moto_liviana_max
            )
        elif weight_kg < 7:
            return random.uniform(
                config.reduccion_moto_media_min,
                config.reduccion_moto_media_max
            )
        else:
            return random.uniform(
                config.reduccion_moto_pesada_min,
                config.reduccion_moto_pesada_max
            )

    elif vehicle_type == "furgoneta":
        if weight_kg < 10:
            return random.uniform(
                config.reduccion_furgoneta_liviana_min,
                config.reduccion_furgoneta_liviana_max
            )
        elif weight_kg < 20:
            return random.uniform(
                config.reduccion_furgoneta_media_min,
                config.reduccion_furgoneta_media_max
            )
        else:
            return random.uniform(
                config.reduccion_furgoneta_pesada_min,
                config.reduccion_furgoneta_pesada_max
            )

    else:
        raise ValueError(f"Tipo de vehículo desconocido: {vehicle_type}")


def apply_speed_reduction(base_speed: float, reduction: float) -> float:
    effective_speed = base_speed * (1 - reduction)
    return max(effective_speed, 1.0)  # Evita valores negativos