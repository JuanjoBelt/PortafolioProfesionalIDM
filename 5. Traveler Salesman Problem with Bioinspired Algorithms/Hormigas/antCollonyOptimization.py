import numpy as np
import random
import time

random.seed(17)

""" -----------------------------------------------------------
                DEFINIR PARÁMETROS DEL PROBLEMA
----------------------------------------------------------- """
costos = [[-1, 40, 54, 98, -1],
          [-1, -1, 43, 62, 87],
          [-1, -1, -1, 48, 71],
          [-1, -1, -1, -1, 49],
          [-1, -1, -1, -1, -1]]

n = len(costos)

origen = 0
destino = 4


""" -----------------------------------------------------------
                        CLASE HORMIGA
----------------------------------------------------------- """
class Ant(object):
    def __init__(self, _alpha, _beta):
        self.alpha = _alpha
        self.beta = _beta
        self.best = [999999, [-1]] # [Costo, Ruta]
        self.last = [999999, [-1]] # [Costo, Ruta]
        self.nombre = random.choice(['Pancho', 'Luupee', 'Peepee', 'Chaava', 'Loolaa',
                                     'Juuaan', 'Keevin', 'Mirnda', 'Feedra', 'Maarco',
                                     'Riigoo', 'Pnfilo', 'Chucho', 'Toonyy', 'Uucaan'])

    def str(self):
        aux = "Hormiga " + self.nombre + ".  Mejor ruta: " + str([i + 1 for i in self.best[1]]) + ". Mejor costo: " + str(self.best[0])
        aux += ". Última ruta: " + str([i + 1 for i in self.last[1]]) + ". Último costo: " + str(self.last[0]) + "."
        return aux
    
    def explore(self, tau, eta):
        nodoAct = origen
        # Agrear el primer nodo a la ruta
        route = [nodoAct]
        cost = 0
        deltaFeromonas = np.zeros((n, n), int).tolist()

        while nodoAct != destino:
            # Calcular las probabilidades
            probs = np.zeros(n, int).tolist()
            accum = 0
            for i in range(n):
                if costos[nodoAct][i] != -1:
                    probs[i] = (tau[nodoAct][i] ** self.alpha) + (eta[nodoAct][i] ** self.beta)
                    accum += probs[i]
            # Normalizar las probabilidades
            for i in range(n):
                probs[i] /= accum
            # Elegir un camino al azar siguiendo la distribución
            newNode = random.choices(list(range(n)), weights=probs, k=1)[0]
            # Agregar el nuevo nodo
            cost += costos[nodoAct][newNode]
            deltaFeromonas[nodoAct][newNode] = 1
            route.append(newNode)
            nodoAct = newNode

        self.last = [cost, route]

        # Revisar si es el mejor que ha visto la hormiga
        if cost < self.best[0]:
            self.best = [cost, route]

        for i in range(n):
            for j in range(n):
                deltaFeromonas[i][j] /= cost

        return deltaFeromonas
            




""" -----------------------------------------------------------
                 CLASE COLONIA DE HORMIGAS
----------------------------------------------------------- """
class AntColony(object):
    def __init__(self, _k, _m, _alpha, _beta, _rho):
        # Hiperparámetros
        self.k = _k
        self.m = _m
        self.alpha = _alpha
        self.beta = _beta
        self.rho = _rho

        # Variables
        self.tau = self.initTau()
        self.eta = self.initEta()
        self.iteracion = 0
        self.executionTime = 0

        self.colonia = []
        # Población de hormigas
        for i in range(self.k):
            self.colonia.append(Ant(self.alpha, self.beta))



    def showColony(self):
        print(f'>> Colonia actual (Iteración #{self.iteracion})')
        for i in self.colonia:
            print(i.str())



    def initEta(self):
        eta = np.zeros((n, n), int).tolist()
        accum = 0
        # Calcular la sumatoria de los costos
        for i in range(n):
            for j in range(n):
                if costos[i][j] != -1:
                    accum += costos[i][j]
                    eta[i][j] = costos[i][j]
        # Dividir entre la sumatoria de los costos
        for i in range(n):
            for j in range(n):
                eta[i][j] /= accum
        return eta          



    def initTau(self):
        tau = np.zeros((n,n), int).tolist()
        counter = 0
        # Calcular la sumatoria de los costos
        for i in range(n):
            for j in range(n):
                if costos[i][j] != -1:
                    counter += 1
        # Asignar un rasto equivalente de feromonas a cada camino
        for i in range(n):
            for j in range(n):
                if costos[i][j] != -1:
                    tau[i][j] = 1/counter
        return tau


    """
    - nuevasFeromonas: numpy array con la suma acumulada de las feromonas depositadas por cada hormiga en cada arco.
    (Es el segundo sumando de la fórmula)
    """
    def updateTau(self, nuevasFeromonas):
        self.tau = np.array(self.tau) * (1 - self.rho)
        self.tau += nuevasFeromonas


    def run(self):
        print('>> Ejecutando iteraciones...\n•', end='')
        # Hacer cada iteración
        start_time = time.time()
        for i in range(self.m):
            nuevasFeromonas = np.zeros((n,n), float)
            for hormiga in self.colonia:
                # Mandar las hormigas a explorar
                deltaFeromonas = hormiga.explore(self.tau, self.eta)
                # Acumular las feromonas que deja cada hormiga
                nuevasFeromonas += np.array(deltaFeromonas, float)

            # Actualizar Tau
            self.updateTau(nuevasFeromonas)
        
            # Monitorear en la consola
            self.iteracion += 1
            print('•', end = '')
            if self.iteracion % 100 == 0:
                print('')
        
        # Calcular el tiempo de ejecución
        self.executionTime = time.time() - start_time

    def showResults(self):
        colonyBest = max(self.colonia, key = lambda x: x.best[0])
        print('>> Ejecución terminada en', self.executionTime, 's.')
        print('>> Feromonas en los arcos:')
        print(self.tau)
        print('>> Mejor solución:', colonyBest.str())





""" -----------------------------------------------------------
              EJECUTAR ANT COLONY OPTIMIZATION
----------------------------------------------------------- """
exampleAntColony = AntColony(_k = 7,         # Cantidad de hormigas
                             _m = 100,       # Cantidad de iteraciones
                             _alpha = 1,     # Influencia de feromonas
                             _beta = 1,      # Influencia del costo
                             _rho = 0.2)     # Constante de evaporación

exampleAntColony.showColony()
exampleAntColony.run()
exampleAntColony.showColony()
exampleAntColony.showResults()

