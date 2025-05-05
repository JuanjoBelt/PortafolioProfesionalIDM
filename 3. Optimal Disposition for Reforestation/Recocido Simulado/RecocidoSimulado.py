# Importar librerías
import random
import numpy as np
import math
from copy import copy

random.seed(31)

""" # Declarar Variables por defecto
dimensiones = (3, 3)
n_especies = 4
labels = ['Agave lechuguilla', 'Agave salmiana', 'Agave scabra', 'Prro']
requisitos = [1, 2, 3, 3]
competencias = [[2,  6, 7, 10],
                [6,  2, 8, 7],
                [7,  8, 2, 7],
                [10, 7, 7, 2]]

fixedpos = (np.ones(dimensiones).astype(int) * (-1)).tolist()
fixedpos[1][2] = 2
fixedpos[0][0] = 2 """



# -------------------------------------- Model Setup --------------------------------------
# Setear variables
def inicializar(d, n, l, r, c, f):
    global dimensiones
    dimensiones = d
    global n_especies
    n_especies = n
    global labels
    labels = l
    global requisitos
    requisitos = r
    global competencias
    competencias = c
    global fixedpos
    fixedpos = f

    # Algunas comprobaciones
    assert n_especies == len(labels), "Debe haber tantos labels como especies de plantas."
    assert n_especies == len(requisitos), "Debe haber tantos labels como requisitos de plantas."
    assert n_especies == len(competencias) and n_especies == len(competencias[0]),"La matriz de competencias debe ser cuadrada y de lado n_especies."
    assert dimensiones[0] * dimensiones[1] == sum(requisitos),"La suma de los requisitos debe corresponder con las dimensiones del espacio."


# -------------------------------------- Algunas Funciones Útiles --------------------------------------

# Imprimir un estado
def print_state(state):
    # Calcular cuántos digitos hay que considerar
    max_dig = int(math.ceil(math.log10(n_especies)))

    for i in range(len(state)):
        for j in range(len(state[i])):
            # Imprimir siempre a una cantidad de dígitos
            print(f"{state[i][j]:0>{max_dig}}", ' ', end = '')
        print('')

# Generar un estado aleatorio
def random_state(reqs, dims):
    aux = []
    for i in range(len(reqs)):
        aux += [i] * reqs[i]
    random.shuffle(aux)
    aux = np.array(aux).reshape(dims)
    
    return aux.tolist()

# Generar un estado aleatorio con plantas fijas
# reqs: Una lista de cuántas plantas por especie (índice)
# dims: Una tupla con las dimensiones de la plantación
# fixd: Una matriz de dimensiones dims con -1s en las posiciones no-fijas y
# un número del 0 al n_sp correspondiente a la especie fija en cierta posición
def random_fixed_state(reqs, dims, fixd):
    aux = []
    for i in range(len(reqs)):
        #aux += [i] * reqs[i]
        aux += (np.ones(reqs[i]).astype(int) * i).tolist()

    # Quitar de la lista de plantas a elegir aquellas que ya están fijas
    fixedpositions = []
    for i in range(len(fixd)):
        for j in range(len(fixd[0])):
            if fixd[i][j] != -1:
                aux.remove(fixd[i][j])
                fixedpositions.append((i, j))


    # Rellenar los -1's
    for i in range(len(fixd)):
        for j in range(len(fixd[0])):
            if fixd[i][j] == -1:
                fixd[i][j] = random.choice(aux)
                aux.remove(fixd[i][j])
   
    return fixd, fixedpositions


#print_state("Un estado aleatorio:\n", random_state(requisitos, plantacion))

# -------------------------------------- Planteamiento del Problema --------------------------------------
class Plantacion(object):

    # Inicializar la instancia
    def __init__(self, dims, n_sp, labs, reqs, cmps, fixd):
        # dims: Dimensiones de la plantación como tupla
        # n_sp: Un entero representando la cantidad de especies
        # labs: Una lista con los labels asociados a cada planta
        # reqs: Una lista de requisitos por cada planta
        # cmps: Competencia entre especies
        # state: Una matriz con la plantación
        # fixd: Matriz de plantas con posición fija
        self.dims = dims
        self.n_sp = n_sp
        self.labs = labs
        self.reqs = reqs
        self.cmps = cmps
        self.fixd = fixd
        self.competencia = None
        self.state, self.blocked = random_fixed_state(reqs, dims, fixd)

    # Devolver la matriz con las plantas
    def getState(self):
        return self.state
    
    def show(self):
        print_state(self.state)
    
    # Intercambiar de lugar los especímenes en las posiciones (i, j) y (p, q)
    def swapPlants(self, p1, p2):
        (i, j) = p1
        (p, q) = p2
        # Intercambiar las plantas
        (a, b) = (self.state[i][j], self.state[p][q])
        (self.state[i][j], self.state[p][q]) = (b, a)

    # Devolver el costo del estado actual
    def cost(self):
        costo = 0
        mapa = self.state
        # Va recorriendo el mapa de izquierda a derecha, arriba a abajo y solo suma 
        # los costos por competencia a la derecha y abajo, para no contar doble
        for i in range(self.dims[0]):
            for j in range(self.dims[0]):
                # Si existe la posición i + 1...
                if i + 1 < self.dims[0]:
                    costo += self.cmps[mapa[i][j]][mapa[i+1][j]]
                # Si existe la posición j + 1...
                if j + 1 < self.dims[0]:
                    costo += self.cmps[mapa[i][j]][mapa[i][j+1]]
        self.competencia = costo
        return costo
    

    # Devuelve un instancia Plantacion correspondiente al mejor vecino encontrado.
    # Un vecino es válido si cumple con los requisitos de especímenes por especie
    # y si solo se intercambian entre sí un par de plantas tales que...
        # No sean de la misma especie
    # De no existir ningún vecino válido, se retornará un None.
    def best_neighbor(self):

        best_plantacion = None
        best_costo = None

        # Recorre todos los pares de plantas intercambiables (i, j), (p, q) y verifica su costo.
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                if (i, j) in self.blocked:
                    continue # Salta esta iteración, porque esa planta es fija
                # Para cada planta, recorre a su derecha y abajo
                for p in range(i+1, self.dims[0]):
                    for q in range(j+1, self.dims[1]):
                        # Verificar las restricciones de vecino:
                        if self.state[i][j] == self.state[p][q]:
                            continue # Brinca esta iteración
                        if (p, q) in self.blocked:
                            continue # Brinca esta iteración porque esa planta es fija
                        # Crear el nuevo estado:
                        new_plantacion = copy(self)
                        # Intercambiar las plantas
                        new_plantacion.swapPlants((i, j), (p, q))
                        # Calcular el costo
                        new_costo = new_plantacion.cost()
                        # Comparar si quedarse con él o no:
                        if best_costo == None or new_costo > best_costo:
                            best_plantacion = new_plantacion
                            best_costo = new_costo

        return best_plantacion

    # Retorna una instancia de Plantacion correspondiente a un vecino valido aleatorio.
    def rand_neighbor(self):
        # Lista de plantas por posición:
        plants = [(p, q) for p in range(self.dims[0]) for q in range(self.dims[0])]
        # Eliminar las que no se pueden mover
        for pos in self.blocked:
            plants.remove(pos)

        # Elegir la primera planta a intercambiar
        p1 = random.choice(plants)
        plants.remove(p1)

        # Elegir la segunda planta a intercambiar
        valido = False
        while(not valido):
            p2 = random.choice(plants)
            if(self.state[p1[0]][p1[1]] != self.state[p2[0]][p2[1]]):
                valido = True
            else:
                plants.remove(p2)

        # Intercambiarlas
        new_plantacion = copy(self)
        new_plantacion.swapPlants(p1, p2)
        return new_plantacion
    

# -------------------------------------- Implementar Greedy --------------------------------------
def greedy(current):
    print("-------- Estado Inicial -----------")
    current.show()
    cost = current.cost() # Costo inicial
    print("Costo Inicial: ", cost)

    step = 0 # Conteo de iteraciones
    while True:
        step += 1

        # Obtener el mejor vecino
        neighbor = current.best_neighbor()
        if neighbor == None:
            # Si el vecino es nulo, significa que no existen posiciones vecinas que estén al alcance del robot
            break
        new_cost = neighbor.cost()

        # Comprobar si el mejor vecino es mejor
        if new_cost < cost:
            # Devuelve el caracter asociado para imprimir la dirección del movimiento
            #mov = deduce_direccion(current.getPos(), neighbor.getPos())
            # Sustituye el vecino actual
            current = neighbor
            cost = new_cost
        else:
            break



        #print("Iteracion: ", step, "    Costo: ", cost, "    Pos: ", current.getPos())

    print("\n-------- Solucion -----------")
    current.show()
    print("Costo Final: ", cost)
    return current

# Intento de Greedy
#initial_plantacion = Plantacion(dimensiones, n_especies, labels, requisitos, competencias)
#solution = greedy(initial_plantacion)





# -------------------------------------- Implementar simulated Anealing --------------------------------------
def simulated_anealing(current, t0, tmin, alpha, verbose):
    if verbose: print("-------- Estado Inicial -----------")
    if verbose: current.show()
    cost = current.cost() # Costo Inicial
    if verbose: print("Costo Inicial: ", cost)

    step = 0 # Contar iteraciones
    t = t0 # Temperatura actual
    while t > tmin and cost > 0:

        # Calcular temperatura
        t = t0 * math.pow(alpha, step)
        step += 1

        # Obtener un vecino aleatorio
        neighbor = current.rand_neighbor()
        new_cost = neighbor.cost()

        # Comprobar si el vecino es mejor
        if new_cost < cost:
            current = neighbor
            cost = new_cost
        else:
            # Calcular la probabilidad de aceptar al vecino
            p = math.exp(-(new_cost - cost)/t)
            if p >= random.random():
                current = neighbor
                cost = new_cost

        #print("Iteracion: ", step, "    Costo: ", cost, "    Temperatura: ", t, "    Map:")
        #current.show()

    if verbose: print("\n-------- Solucion -----------")
    if verbose: current.show()
    if verbose: print("Costo Final: ", cost)
    return current

# Prueba de Recocido Simulado
# initial_plantacion = Plantacion(dimensiones, n_especies, labels, requisitos, competencias, fixedpos)
# alpha = 0.999
# t0 = 100000
# tmin = 0.001
# solution = simulated_anealing(initial_plantacion, t0, tmin, alpha)