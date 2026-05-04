# Proyecto de Modelado y Simulación — Pronti

## Descripción
Este proyecto desarrolla una simulación del sistema de entregas rápidas de la empresa **Pronti**, con el objetivo de comparar diferentes configuraciones de flota y determinar su desempeño en términos de:

- tiempo promedio de entrega
- costo operativo total
- utilidad bruta

El problema parte de un centro de distribución único y evalúa si conviene operar con **motos**, **furgonetas** o una **flota mixta**, bajo distintos niveles de demanda.

---

## Objetivo
Evaluar mediante simulación estocástica el comportamiento de diferentes configuraciones de flota para identificar cuál resulta más conveniente según criterios operativos y económicos.

---

## Escenarios evaluados

### Escenarios base
- **A1:** Alta demanda con 10 motos
- **A2:** Baja demanda con 10 motos
- **B1:** Alta demanda con 4 furgonetas
- **B2:** Baja demanda con 4 furgonetas

### Escenario adicional
- **C:** Alta demanda con flota mixta
  - 5 motos
  - 2 furgonetas

---

## Características del modelo
El modelo incorpora:

- llegada de pedidos con distribución de **Poisson**
- capacidad de carga:
  - moto = 1 pedido
  - furgoneta = 10 pedidos
- velocidad promedio de entrega
- regla de salida con vehículos llenos
- costo diario de empleados
- amortización de vehículos a 10 años
- representación espacial mediante un **grafo de ciudad**
- paquetes con:
  - categoría
  - peso
  - precio variable
- reducción de velocidad según el peso del paquete
- análisis estadístico con múltiples corridas por escenario

---

## Estructura del proyecto

```text
Modelado y Simulación/
│
├── configuracion.py
├── entidades.py
├── utiles.py
├── escenarios.py
├── simulacion.py
├── analisis.py
├── main.py
├── graficos.py
├── casos_representativos.py
├── tabla_casos_resumen.py
├── tabla_casos_presentacion.py
├── grafo_ciudad.py
├── resultados_detallados.csv
├── resumen_escenarios.csv
├── casos_representativos.csv
├── tabla_casos_resumen.csv
├── tabla_casos_presentacion.csv
├── grafo_ciudad.png
└── graficos/