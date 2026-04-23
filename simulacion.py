import random
import simpy

from entidades import Package, Vehicle, SimulationMetrics

from utiles import (
    sample_interarrival_time,
    sample_uniform,
    sample_destination_node,
    sample_distance_km,
    calculate_round_trip_time_hours,
    calculate_furgoneta_trip_time_hours,
    sample_package_category,
    sample_package_weight,
    get_shipping_price,
    get_speed_reduction,
    apply_speed_reduction,
)

class DeliverySystem:
    def __init__(self, env, config, scenario):
        self.env = env
        self.config = config
        self.scenario = scenario
        self.metrics = SimulationMetrics()

        self.package_queue = []
        self.package_counter = 0

        self.motos = []
        self.furgonetas = []

        if scenario.fleet_type == "motos":
            self.motos = [Vehicle(i, "moto") for i in range(config.num_motos)]
        elif scenario.fleet_type == "furgonetas":
            self.furgonetas = [Vehicle(i, "furgoneta") for i in range(config.num_furgonetas)]
        elif scenario.fleet_type == "mixto":
            self.motos = [Vehicle(i, "moto") for i in range(config.num_motos // 2)]
            self.furgonetas = [Vehicle(i, "furgoneta") for i in range(config.num_furgonetas // 2)]

    def can_accept_package(self) -> bool:
        return len(self.package_queue) < self.config.capacidad_warehouse

    def get_available_vehicle(self, vehicle_type: str):
        fleet = self.motos if vehicle_type == "moto" else self.furgonetas
        available = [v for v in fleet if v.available]
        if not available:
            return None
        return random.choice(available)

    def create_package(self):
        self.package_counter += 1
        node = sample_destination_node(self.config.num_nodos_entrega)
        distance = sample_distance_km(
            self.config.distancia_min_km,
            self.config.distancia_max_km
        )

        category = sample_package_category()
        weight = sample_package_weight(self.config, category)
        shipping_price = get_shipping_price(self.config, category)

        return Package(
            package_id=self.package_counter,
            arrival_time=self.env.now,
            destination_node=node,
            distance_km=distance,
            category=category,
            weight_kg=weight,
            shipping_price=shipping_price
        )

    def add_daily_fixed_costs(self):
        if self.scenario.fleet_type == "motos":
            self.metrics.total_cost += (
                self.config.num_motos * self.config.salario_diario +
                self.config.num_motos * self.config.costo_diario_moto
            )
        elif self.scenario.fleet_type == "furgonetas":
            self.metrics.total_cost += (
                self.config.num_furgonetas * self.config.salario_diario +
                self.config.num_furgonetas * self.config.costo_diario_furgoneta
            )

def package_generator(env, system):
    while env.now < system.config.jornada_horas:
        interarrival = sample_interarrival_time(system.scenario.demand_rate_per_hour)
        yield env.timeout(interarrival)

        if env.now > system.config.jornada_horas:
            break

        if system.can_accept_package():
            package = system.create_package()
            system.package_queue.append(package)

def moto_dispatcher(env, system):
    while env.now < system.config.jornada_horas:
        if len(system.package_queue) >= system.config.capacidad_moto:
            moto = system.get_available_vehicle("moto")
            if moto is not None:
                package = system.package_queue.pop(0)
                moto.available = False
                env.process(run_moto_trip(env, system, moto, package))
        yield env.timeout(0.05) # Pequeña espera para no saturar el bucle si no hay paquetes

def run_moto_trip(env, system, moto, package):
    base_speed = sample_uniform(system.config.vel_moto_min, system.config.vel_moto_max)
    reduction = get_speed_reduction(system.config, "moto", package.weight_kg)
    speed = apply_speed_reduction(base_speed, reduction)

    trip_time = calculate_round_trip_time_hours(package.distance_km, speed)

    start_time = env.now
    yield env.timeout(trip_time)

    if env.now <= system.config.jornada_horas:
        waiting_time = start_time - package.arrival_time
        delivery_time = env.now - package.arrival_time

        system.metrics.delivered_packages += 1
        system.metrics.total_waiting_time += waiting_time
        system.metrics.total_delivery_time += delivery_time
        system.metrics.total_income += package.shipping_price

        total_distance = 2 * package.distance_km
        system.metrics.total_distance_moto += total_distance
        system.metrics.moto_trips += 1

        fuel_cost = total_distance * system.config.consumo_moto_litro_km * system.config.precio_gasolina_litro
        system.metrics.total_cost += fuel_cost

    moto.available = True
    moto.trips_completed += 1
    moto.busy_time += env.now - start_time

def furgoneta_dispatcher(env, system):
    while env.now < system.config.jornada_horas:
        if len(system.package_queue) >= system.config.capacidad_furgoneta:
            van = system.get_available_vehicle("furgoneta")
            if van is not None:
                packages = [
                    system.package_queue.pop(0)
                    for _ in range(system.config.capacidad_furgoneta)
                ]
                van.available = False
                env.process(run_furgoneta_trip(env, system, van, packages))
        yield env.timeout(0.05)

def run_furgoneta_trip(env, system, van, packages):
    base_speed = sample_uniform(system.config.vel_furgoneta_min, system.config.vel_furgoneta_max)
    total_weight = sum(p.weight_kg for p in packages)
    reduction = get_speed_reduction(system.config, "furgoneta", total_weight)
    speed = apply_speed_reduction(base_speed, reduction)

    avg_distance = sum(p.distance_km for p in packages) / len(packages)
    trip_time = calculate_furgoneta_trip_time_hours(avg_distance, speed)

    start_time = env.now
    yield env.timeout(trip_time)

    if env.now <= system.config.jornada_horas:
        total_distance = avg_distance * 2.6

        for package in packages:
            waiting_time = start_time - package.arrival_time
            delivery_time = env.now - package.arrival_time

            system.metrics.delivered_packages += 1
            system.metrics.total_waiting_time += waiting_time
            system.metrics.total_delivery_time += delivery_time
            system.metrics.total_income += package.shipping_price

        system.metrics.total_distance_furgoneta += total_distance
        system.metrics.furgoneta_trips += 1
        system.metrics.total_cost += total_distance * system.config.costo_energia_furgoneta_km

    van.available = True
    van.trips_completed += 1
    van.busy_time += env.now - start_time

def run_single_simulation(config, scenario, seed=None):
    if seed is not None:
        random.seed(seed)

    env = simpy.Environment()
    system = DeliverySystem(env, config, scenario)
    system.add_daily_fixed_costs()

    env.process(package_generator(env, system))

    if scenario.fleet_type == "motos":
        env.process(moto_dispatcher(env, system))
    elif scenario.fleet_type == "furgonetas":
        env.process(furgoneta_dispatcher(env, system))
    elif scenario.fleet_type == "mixto":
        env.process(moto_dispatcher(env, system))
        env.process(furgoneta_dispatcher(env, system))

    env.run(until=config.jornada_horas)

    system.metrics.pending_packages = len(system.package_queue)

    return {
        "scenario": scenario.name,
        "description": scenario.description,
        "seed": seed,
        "delivered_packages": system.metrics.delivered_packages,
        "pending_packages": system.metrics.pending_packages,
        "average_delivery_time": system.metrics.average_delivery_time,
        "average_waiting_time": system.metrics.average_waiting_time,
        "total_cost": system.metrics.total_cost,
        "total_income": system.metrics.total_income,
        "gross_profit": system.metrics.utilidad_bruta,
        "moto_distance": system.metrics.total_distance_moto,
        "furgoneta_distance": system.metrics.total_distance_furgoneta,
        "moto_trips": system.metrics.moto_trips,
        "furgoneta_trips": system.metrics.furgoneta_trips,
    }
