import random
import math

def f1(x):
    return abs((x * math.sin(x)) / (2*x - 5))

def ABC(func, lb, ub, dim, NP, FoodNumber, Limit, maxCycle):
    """
    Implementación del algoritmo de colonia de abejas artificial (ABC)

    Args:
        func: Función objetivo
        lb: Límite inferior de la búsqueda
        ub: Límite superior de la búsqueda
        dim: Dimensión del problema
        NP: Número de abejas
        FoodNumber: Número de fuentes de alimento
        Limit: Límite de abandono
        maxCycle: Número máximo de ciclos
    """

    # Inicialización de la población
    Population = [[random.uniform(lb, ub) for _ in range(dim)] for _ in range(NP)]
    Fitness = [func(ind) for ind in Population]

    # Bucle principal
    for cycle in range(maxCycle):
        # Empleadas
        for i in range(FoodNumber):
            # Generar una nueva solución
            v = Population[i].copy()
            k = random.randint(0, dim-1)
            phi = random.uniform(-1, 1)
            v[k] = Population[i][k] + phi * (Population[i][k] - Population[random.randint(0, FoodNumber-1)][k])
            v = max(lb, min(ub, x)) for x in v  # Asegurar que esté dentro de los límites
            fv = func(v)
            if fv > Fitness[i]:
                Population[i] = v.copy()
                Fitness[i] = fv

        # Observadoras
        for i in range(FoodNumber, NP):
            # Seleccionar una fuente de alimento
            i = random.randint(0, FoodNumber-1)
            # Generar una nueva solución
            v = Population[i].copy()
            k = random.randint(0, dim-1)
            phi = random.uniform(-1, 1)
            v[k] = Population[i][k] + phi * (Population[i][k] - Population[random.randint(0, FoodNumber-1)][k])
            v = [max(lb, min(ub, x)) for x in v]  # Asegurar que esté dentro de los límites
            fv = func(v)
            if fv > Fitness[i]:
                Population[i] = v.copy()
                Fitness[i] = fv

        # Exploradoras
        count = 0
        for i in range(FoodNumber):
            if Fitness[i] < Limit:
                count += 1
                Population[i] = [random.uniform(lb, ub) for _ in range(dim)]
                Fitness[i] = func(Population[i])
        if count > 0.9 * FoodNumber:
            for j in range(FoodNumber, NP):
                Population[j] = [random.uniform(lb, ub) for _ in range(dim)]
                Fitness[j] = func(Population[j])

    # Obtener la mejor solución
    best_index = Fitness.index(max(Fitness))
    best = Population[best_index]
    return best, func(best)

# Parámetros del problema
dim = 1  # Dimensión del problema
lb = 0  # Límite inferior
ub = 14  # Límite superior
NP = 50  # Número de abejas
FoodNumber = NP//2  # Número de fuentes de alimento
Limit = 0.5  # Límite de abandono
maxCycle = 1000  # Número máximo de ciclos

# Ejecutar el algoritmo
best, fbest = ABC(f1, lb, ub, dim, NP, FoodNumber, Limit, maxCycle)

print("El máximo valor de la función es:", fbest)
print("En el punto:", best)