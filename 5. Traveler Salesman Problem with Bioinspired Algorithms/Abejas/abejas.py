import math
import random
import time
random.seed(31)

f1 = lambda x : abs((x * math.sin(x))/(2*x - 5)) # [0, 14]
f2 = lambda x : math.exp(x ** 3 - x) # [-1, 0]
f3 = lambda x, y: -(3*y)/(x**2 + y**2 + 1) # [-5, 5], [-5, 5]
f4 = lambda x, y: 3*(1-x)**2 * math.exp(-x**2 -(y+1)**2) - 10 * math.exp(-x**2 -y**2) * (-x**3 + x/5 - y**5) - (1/3) * math.exp(-(x+1)**2 - y**2) # [-3, 3], [-3, 3]


class Bee(object):
    def __init__(self, _function, _rango):
        self.function = _function
        self.rango = _rango

        # Generar una posición inicial aleatoria dentro del rango
        self.pos = random.random() * (self.rango[1] - self.rango[0]) + self.rango[0]
        # Obtener el máximo hasta ahora
        self.best = (self.pos, self.function(self.pos))

    def move(self, referencia):
        # Generar un número aleatorio entre 0 y 1
        phi = random.random()
        self.pos += phi * (referencia.pos - self.pos)
        # Asegurar que no salga del rango
        self.pos = min(self.pos, max(self.rango))
        self.pos = max(self.pos, min(self.rango))

        # Actualizar el mejor
        if self.function(self.pos) > self.best[1]:
            self.best = (self.pos, self.function(self.pos))

    def fit(self):
        return self.function(self.pos)

    def str(self):
        return "Mejor x: " + str(self.best[0]) + ". Mejor función objetivo: " + str(self.best[1]) + "."


class BeeColony(object):
    def __init__(self, _k, _lim, _function, _rango):
        self.k = _k
        self.lim = _lim
        self.function = _function
        self.rango = _rango

        self.iteracion = 0
        self.executionTime = -1
        self.colony = []
        for i in range(self.k):
            self.colony.append(Bee(self.function, self.rango))

    def run(self):
        print('>> Ejecutando iteraciones...\n•', end='')
        # Hacer cada iteración
        start_time = time.time()
        while not self.criterioParo():
            # Calcular distriución de probabilidad
            fits = []
            for abeja in self.colony:
                fits.append(abeja.fit())

            for abeja in self.colony:
                referencia = random.choices(self.colony, weights = fits, k = 1)[0]
                abeja.move(referencia)

            self.iteracion += 1
            print('•', end = '')
            if self.iteracion % 100 == 0:
                print('')
        
        self.executionTime = time.time() - start_time


    def criterioParo(self):
        return self.iteracion >= self.lim
    

    def show(self):
        print(f'>> Colonia actual (Iteración #{self.iteracion})')
        for abeja in self.colony:
            print(abeja.str())


    def showResults(self):
        colonyBest = max(self.colony, key = lambda x: x.best[1])
        print('>> Ejecución terminada en', self.executionTime, 's.')
        print('>> Mejor solución:', colonyBest.str())


exampleBees = BeeColony(_k = 10,
                        _lim = 100,
                        _function = f2,
                        _rango = [-1, 0])

exampleBees.show()
exampleBees.run()
exampleBees.show()
exampleBees.showResults()