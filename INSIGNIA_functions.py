# # # # # # # # # # # # # # # # # # # # # #
# FIVECOMM ©                              #
# Author: Miguel Cantero                  #
# Mail: miguel.cantero@fivecomm.eu        #
# Version: v1.0                           #
# # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import json
import datetime
import os
import matplotlib.pyplot as plt

# REFERENCIA: https://www.aimc.es/otros-estudios-trabajos/navegantes-la-red/infografia-resumen-20o-navegantes-la-red/
horas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
valores = [19.5, 9.0, 4.5, 3.0, 2.0, 1.5, 7.5, 15.0, 23.0, 40.0, 41.5, 40.5, 45.5, 38.3, 32.0, 38.0, 41.5, 41.0, 45.0, 45.0, 44.0, 47.5, 47.0, 35.5]

def save_graph_in_json(x, random, algorithm, is_range = False, filename="graph_data"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))+".json"):

    # 1. Crear un diccionario con todos los datos que quieras guardar
    data = {
        "x": list(x) if is_range else list(range(x)), 
        "Random": random,
        "Algorithm": algorithm
    }

    # 2. Guardar en un archivo JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_ues_base_values(horas=horas, valores=valores):
    # Lista para almacenar los 1440 minutos
    minutos = np.linspace(0, 23, num=1440)  # 1440 minutos desde las 00:00 hasta las 23:59

    # Ajustamos las horas para interpolar correctamente sobre el ciclo completo
    horas_ajustadas = horas + [24]  # Añadir la hora 24 al final para cerrar el ciclo
    valores_ajustados = valores + [valores[0]]  # Añadir el valor correspondiente de la hora 0

    # Interpolación de los valores
    valores_interpolados = np.interp(minutos, horas_ajustadas, valores_ajustados)

    # Convertir a lista
    lista_final = valores_interpolados.tolist()

    return lista_final

def add_batch_to_file(name):
    try:
        f = open("batch.txt", "a")
        f.write(name)
        f.close()
    except:
        print("ERROR: Couldn't write filename on batch file")


def read_batch_from_file(filename="batch.txt"):
    f = open(filename, "r")
    content = f.read().split("\n")
    print(content[:-1])
    return content[:-1]


def save_json(j, name=""):
    dir_name = "simulation_results"

    if not os.path.exists("./"+dir_name):
      os.mkdir("./"+dir_name)

    time = str(datetime.datetime.now()).replace(":",".")
    filename = dir_name + "/" + name + time + '.json'
    with open(filename, 'w') as f:
        json.dump(j, f)

    batch_filename = name + time + '.json\n'
    add_batch_to_file(batch_filename)
    

def load_json(j):
    try:
        with open("simulation_results/"+j, 'r') as file:
            data = json.load(file)
        return data
    
    except:
        print("ERROR al leer el json "+j)
        quit()


def plot2(grid_random, grid_algorithm):
    rresources_per_slot = [0 for e in range(24*60)]
    aresources_per_slot = [0 for e in range(24*60)]

    for i, resource in enumerate(grid_random.resources):
        rresources_per_slot[i] = len(resource)

    for i, resource in enumerate(grid_algorithm.resources):
        aresources_per_slot[i] = len(resource)

    rtotal_resources = sum(rresources_per_slot)  # Recursos totales utilizados en un día
    rmax_resources = max(rresources_per_slot)  # Recursos en el slot con más carga del día
    rslots_saturados = [0 for e in range(rmax_resources)]  # Slots que saturan para cada valor de carga hasta el máximo
    rporcentaje_slots_servidos = [0 for e in range(rmax_resources)]
    rues_servidos = [0 for e in range(rmax_resources)]
    rporcentaje_ues_servidos = [0 for e in range(rmax_resources)]

    atotal_resources = sum(aresources_per_slot)  # Recursos totales utilizados en un día
    amax_resources = max(aresources_per_slot)  # Recursos en el slot con más carga del día
    aslots_saturados = [0 for e in range(rmax_resources)]  # Slots que saturan para cada valor de carga hasta el máximo
    aporcentaje_slots_servidos = [0 for e in range(rmax_resources)]
    aues_servidos = [0 for e in range(rmax_resources)]
    aporcentaje_ues_servidos = [0 for e in range(rmax_resources)]

    # RANDOM: Por cada X recursos tope
    for nivel_saturacion in range(rmax_resources):
        # Cada slot para los X recursos tope
        for resource_slot in rresources_per_slot:
            if resource_slot > nivel_saturacion:
                rslots_saturados[nivel_saturacion] += 1
                rues_servidos[nivel_saturacion] += nivel_saturacion
            else:
                # si satura, los máximos es el nivel de saturación, sino, todos son servidos
                rues_servidos[nivel_saturacion] += resource_slot
        rporcentaje_slots_servidos[nivel_saturacion] = (1440 - rslots_saturados[nivel_saturacion])/1440
        rporcentaje_ues_servidos[nivel_saturacion] = rues_servidos[nivel_saturacion]/rtotal_resources

    # ALGORITMO: Por cada X recursos tope
    for nivel_saturacion in range(rmax_resources):
        # Cada slot para los X recursos tope
        for resource_slot in aresources_per_slot:
            if resource_slot > nivel_saturacion:
                aslots_saturados[nivel_saturacion] += 1
                aues_servidos[nivel_saturacion] += nivel_saturacion
            else:
                # si satura, los máximos es el nivel de saturación, sino, todos son servidos
                aues_servidos[nivel_saturacion] += resource_slot
        aporcentaje_slots_servidos[nivel_saturacion] = (1440 - aslots_saturados[nivel_saturacion])/1440
        aporcentaje_ues_servidos[nivel_saturacion] = aues_servidos[nivel_saturacion]/atotal_resources
                

    # GRÁFICO 1 #######################################################
    # Crear una figura con dos subgráficos
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig, ax = plt.subplots()

    # Guarda los datos en un JSON para poder graficarlos en otro software
    save_graph_in_json(rmax_resources, rslots_saturados, aslots_saturados, filename="graph1.json")

    # Primer gráfico
    ax.plot(range(rmax_resources), rslots_saturados, label = "Random")

    # Segundo gráfico
    ax.plot(range(rmax_resources), aslots_saturados, label = "Algorithm")

    ax.set_xlabel("Resources")
    ax.set_ylabel("Slots saturated")
    ax.set_title("Slots saturados")
    ax.legend()

    # Mostrar los gráficos
    plt.tight_layout()
    plt.show()


    # GRÁFICO 2 #######################################################
    # Crear una figura con dos subgráficos
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig, ax = plt.subplots()

    # Guarda los datos en un JSON para poder graficarlos en otro software
    save_graph_in_json(rmax_resources, rporcentaje_ues_servidos, aporcentaje_ues_servidos, filename="graph2.json")

    # Primer gráfico
    ax.plot(range(rmax_resources), rporcentaje_ues_servidos, label = "Random")

    # Segundo gráfico
    ax.plot(range(rmax_resources), aporcentaje_ues_servidos, label = "Algorithm")

    ax.set_xlabel("Resources")
    ax.set_ylabel("UEs servidos")
    ax.set_title("UEs servidos")
    ax.legend()

    # Mostrar los gráficos
    plt.tight_layout()
    plt.show()


# Plot transversal
def plot3_getvalues(grid, ues_served=0.9):

    total_slots = 1440  # Total de slots en un día (24 horas * 60 minutos)
    resources_per_slot = [0 for e in range(total_slots)]

    for i, resource in enumerate(grid.resources):
        resources_per_slot[i] = len(resource)

    total_resources = sum(resources_per_slot)  # Recursos totales utilizados en un día
    max_resources = max(resources_per_slot)  # Recursos en el slot con más carga del día
    slots_saturados = [0 for e in range(max_resources)]  # Slots que saturan para cada valor de carga hasta el máximo
    porcentaje_slots_servidos = [0 for e in range(max_resources)]
    rues_servidos = [0 for e in range(max_resources)]
    porcentaje_ues_servidos = [0 for e in range(max_resources)]

    # RANDOM: Por cada X recursos tope
    # Para valores de SATURATION = 1, 2, 3, ... max_resources
    for nivel_saturacion in range(max_resources):

        # nivel_saturacion = 5, por ejemplo
        # Cada slot para los X recursos tope
        for resource_slot in resources_per_slot:
            if resource_slot > nivel_saturacion: #=5
                # Si este slot tiene más recursos que el nivel de saturación
                slots_saturados[nivel_saturacion] += 1
                rues_servidos[nivel_saturacion] += nivel_saturacion
            else:
                # si satura, los máximos es el nivel de saturación, sino, todos son servidos
                rues_servidos[nivel_saturacion] += resource_slot
        porcentaje_slots_servidos[nivel_saturacion] = (total_slots - slots_saturados[nivel_saturacion])/total_slots
        porcentaje_ues_servidos[nivel_saturacion] = rues_servidos[nivel_saturacion]/total_resources

    # print(f"Porcentaje de UEs servidos: {porcentaje_ues_servidos}")
    ini=0
    ini_recursos=0
    fin=0
    fin_recursos=0
    for i, e in enumerate(porcentaje_ues_servidos):
        if e >= ues_served:
            if e == ues_served:
                ini = e
                fin = e
                ini_recursos = i
                fin_recursos = i
            else:
                fin = e
                ini = porcentaje_ues_servidos[i-1]
                fin_recursos = i
                ini_recursos = i-1
            break
    
    # print(f"Inicio: {ini} - {ini_recursos}\nFin: {fin} - {fin_recursos}")
    
    if ini==fin:
        p = ini
    else:
        p = (fin_recursos*(ues_served-ini) + ini_recursos*(fin-ues_served)) / (fin-ini)

    # print(f"Resultado final: {p}")
    # p = porcentaje 
    return p

# Plot transversal
def plot3(resources_random, resources_algorithm, ues, limite_ues):

    # Guarda los datos en un JSON para poder graficarlos en otro software
    save_graph_in_json(ues, resources_random, resources_algorithm, filename="graph_"+str(limite_ues)+".json", is_range=True)

    plt.plot(ues, resources_random, label = "Random")

    # Segundo gráfico
    plt.plot(ues, resources_algorithm, label = "Algorithm")

    plt.xlabel("UEs totales simulación")
    plt.ylabel("Recursos")
    plt.title(f"Recursos para {limite_ues*100}% de UEs servidos")
    plt.legend()

    # Mostrar los gráficos
    plt.show()