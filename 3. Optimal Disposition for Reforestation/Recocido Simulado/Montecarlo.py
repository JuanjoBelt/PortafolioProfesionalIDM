import numpy as np
import random
import matplotlib.pyplot as plt
import RecocidoSimulado as rc

random.seed(73)

# -------------------------------------- Definición del Problema --------------------------------------
dimensiones = (26, 26)
n_especies = 10
labels = ['Agave lechuguilla', 'Agave salmiana', 'Agave scabra', 'Agave striata',
          'Opuntia cantabrigiensis', 'Opuntia engelmannii', 'Opuntia robusta',
          'Opuntia streptacantha', 'Prosopis laevigata', 'Yucca filifera']

requisitos = [44, 197, 44, 44, 51, 40, 75, 66,  87, 28]
competencias = [[0, 6, 7, 5, 4, 5, 6, 4, 8, 7],
                [6, 0, 8, 7, 5, 6, 7, 5, 9, 8],
                [7, 8, 0, 7, 5, 6, 6, 5, 8, 7],
                [5, 7, 7, 0, 4, 5, 6, 4, 8, 6],
                [4, 5, 5, 4, 0, 7, 7, 7, 6, 5],
                [5, 6, 6, 5, 7, 0, 8, 8, 6, 6],
                [6, 7, 6, 6, 7, 8, 0, 8, 7, 6],
                [4, 5, 5, 4, 7, 8, 8, 0, 6, 5],
                [8, 9, 8, 8, 6, 6, 7, 6, 0, 8],
                [7, 8, 7, 6, 5, 6, 6, 5, 8, 0]]

fixedpos = (np.ones(dimensiones).astype(int) * (-1)).tolist()
fixedpos[1][1] = 2
fixedpos[0][0] = 2

rc.inicializar(dimensiones, n_especies, labels, requisitos, competencias, fixedpos)

# -------------------------------------- Montecarlo --------------------------------------
muestras_raw = [[ 8,  58,  66,  10,  65,  67,  41,  32,  58, 47, 48, 36, 50, 35, 40, 70, 56, 45, 56, 69, 54, 75, 44, 10, 44, 72, 74, 67, 60, 34],
                [46, 263, 236,  52, 280, 306, 209, 252, 269, 209, 233, 182, 189, 186, 311, 290, 233, 204, 223, 285, 287,	292, 288, 59, 155, 291, 342, 309, 280, 195],
                [16,  47,  51,	15,	 66,  63,  43,	46,	 58,  47,	41,	43,	49,	38,	52,	55,	39,	34,	51,	57,	70,	60,	69,	15,	28,	73,	52,	67,	61,	56],
                [16,  49,  50,	 9,	 61,  61,  49,	40,	 53,  41,	37,	44,	28,	43,	62,	54,	46,	33,	48,	75,	62,	68,	51,	11,	31,	50,	55,	66,	53,	58],
                [11,  60,  71,	15,	 92,  81,  48,	73,	 57,  66,	48,	51,	43,	39,	68,	84,	71,	56,	50,	77,	89,	104,	69,	17,	39,	66,	70,	86,	76,	55],
                [14,  44,  56,	10,	 54,  62,  52,	39,	 58,  43,	40,	41,	33,	44,	63,	50,	45,	46,	48,	74,	58,	62,	60,	18,	39,	62,	76,	54,	68,	46],
                [18, 111, 100,	18,	124, 118,  87,	86,	 94,  96,	94,	68,	73,	73,	132,	105,	83,	82,	93,	107,	126,	109,	122,	17,	65,	125,	100,	120,	109,	91],
                [12,  95,  78,	20,	114,  91,  60,	79,	 91,  71,	65,	72,	76,	61,	89,	77,	81,	48,	90,	103,	109,	95,	100,	10,	50,	101,	100,	103,	85,	63],
                [15,  98, 123,	23,	106, 133,  97,  91,	117, 108,	94,	67,	97,	74,	149,	121,	97,	95,	120,	104,	139,	125,	106,	39,	67,	122,	129,	141,	135,	86],
                [ 9,  39,  28,	11,  41,  45,  27,  26,  37,  29, 27, 19, 25, 23, 53, 40, 32, 17, 33, 25, 44, 43, 39, 8, 25, 31, 44, 33, 36, 23]]

muestras = muestras_raw
t_muestra = [1.28, 6.64, 6.76, 1.38, 8, 7.82, 5.53, 5.64, 7.11, 6.11, 5.64, 4.92, 05.05, 4.75, 7.97, 7.34, 5.98, 5.4, 6.28, 7.6, 8, 8, 7.67, 1.47, 4.19, 7.52, 8, 8, 7.56, 5.4]
# Normalizar las muestras a 1 hectárea
for j in range(len(t_muestra)):
    for i in range(len(muestras_raw)):
        muestras[i][j] = muestras_raw[i][j] / t_muestra[j]
   
def generaMapaPoisson(m):
    # Inicializar mapa de -1's
    mapa = (np.ones(dimensiones).astype(int) * (-1)).tolist()
    # Calcular las medias de cada especie
    medias = [sum(i)/len(i) for i in m]
    # Número de plantas por especie
    # num_p = [min(np.random.poisson(lam = media), requisitos[]) for media in medias]
    num_p = []
    for i in range(len(medias)):
        aux = min(np.random.poisson(lam = medias[i]), requisitos[i])
        num_p.append(aux)
    # Lista con todas las posibles posiciones de plantas
    espacios = [(p, q) for p in range(dimensiones[0]) for q in range(dimensiones[1])]

    # Lista de plantas que ya estaban plantadas
    plantas = []
    for i in range(len(num_p)):
        # Ir añandiendo tantos i como plantas de esa especie
        plantas += (np.ones(num_p[i]).astype(int) * i).tolist()

    # Elegir posiciones fijas al azar
    elegidas = random.choices(population = espacios, k = len(plantas))

    for i in range(len(plantas)):
        mapa[elegidas[i][0]][elegidas[i][1]] = plantas[i]

    return mapa, num_p

# -------------------------------------- Implementar simulated Anealing --------------------------------------
alpha = 0.999
t0 = 100
tmin = 0.005
guardar_img = True # Guardar imagenes sobre cada iteración
printMode = 1 # Imprimir información sobre cada iteración
# 0: No imprime nada
# 1: Imprime un punto cada que completa una iteracion
# 2: Imprime el costo cada que completa una iteración

# Iteraciones para Montecarlo
iteraciones = 34

# Lista de objetos Plantacion que contiene las soluciones
h_soluciones = []
# Lista de listas, cada una con la distribución nativa por especie (índice)
h_distribuciones = []

# Ejecutar Montecarlo
print('---------- Ejecutando Simulación ----------')
for i in range(iteraciones):
    #print('Posiciones fijas:')
    fixedpos, dist_nativa = generaMapaPoisson(muestras)
    if guardar_img: plt.imshow(fixedpos)
    if guardar_img: plt.set_cmap('gist_earth')
    if guardar_img: plt.savefig(f'soluciones/in{i}.png')
    #rc.print_state(fixedpos)
    #print('Plantacion inicial')
    initial_plantacion = rc.Plantacion(dimensiones, n_especies, labels, requisitos, competencias, fixedpos)
    #rc.print_state(initial_plantacion.state)
    solution = rc.simulated_anealing(initial_plantacion, t0, tmin, alpha, False)
    # Imprimir la solución
    #print('Solución', i, ':')
    #rc.print_state(solution.state)

    if guardar_img: plt.imshow(solution.state)
    if guardar_img: plt.set_cmap('gist_earth')
    if guardar_img: plt.savefig(f'soluciones/out{i}.png')

    h_soluciones.append(solution)
    h_distribuciones.append(dist_nativa)
    if printMode == 1:
        if i % 20 == 19: print('•\n', end = '')
        else: print('•', end = '')
    if printMode == 2: print('Iteración ', i, ' completada con éxito. Compentencia: ', solution.cost(), sep = '')


# -------------------------------------- Mostrar Resultados --------------------------------------
print('\n--------------- Resultados ----------------')
# Total de plantas nativas por hectárea
aux = 0
for i in range(len(h_distribuciones)):
    aux += sum(h_distribuciones[i])
aux = aux / len(h_distribuciones)
print('Total de plantas nativas por hectárea:', aux)

# Valor esperado de plantas por especie en una hectárea
aux = []
for i in range(len(h_distribuciones[0])):
    count = 0
    for dist in h_distribuciones:
        count += dist[i]
    aux.append(count / len(h_distribuciones))
print('Total de plantas nativas por especie en una hectárea:')
for i in range(len(aux)):
    print('>> ', labels[i], ': ', aux[i], sep = '')

# Valor esperado de plantas por especie a suministrar por hectárea
print('Total de plantas a suministrar por especie en una hectárea:')
for i in range(len(aux)):
    print('>> ', labels[i], ': ', requisitos[i]-aux[i], sep = '')

# Valor esperado de competencia existente en una hectárea
aux = 0
for solu in h_soluciones:
    aux += solu.competencia
aux = aux / len(h_soluciones)
print('Valor esperado de la competencia existente en una hectárea: ', aux, sep = '')

