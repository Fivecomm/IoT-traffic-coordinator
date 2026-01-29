# # # # # # # # # # # # # # # # # # # # # #
# FIVECOMM ©                              #
# Author: Miguel Cantero                  #
# Mail: miguel.cantero@fivecomm.eu        #
# Version: v1.0                           #
# # # # # # # # # # # # # # # # # # # # # #

from INSIGNIA_objects import UE, GroupUE, Grid
import random

def allocation_algorithm(grid, ues_or_groups):
    """
    Algoritmo para asignar los UEs o GroupUE en el grid de la manera más óptima posible.
    Minimiza las colisiones durante la asignación de los bloques de minutos.
    """

    # Validates that the inputs are correct types
    is_valid, msg_validation = validate_types(grid, ues_or_groups)
    if not is_valid:
        return grid, msg_validation
    
    # Obtenemos la lista de todas las UEs a asignar (expandimos los GroupUE)
    all_ues = []
    
    for ue_or_group in ues_or_groups:
        if isinstance(ue_or_group, GroupUE):
            # Expandir los GroupUE en múltiples UEs individuales
            all_ues.extend([ue_or_group.ue_parameters for _ in range(ue_or_group.number_of_ues)])
        else:
            all_ues.append(ue_or_group)
    
    # Ordenamos por el número de conexiones y rangos de tiempo para priorizar los más restrictivos
    all_ues.sort(key=lambda ue: (len(ue.time_ranges), ue.connections_per_day))
    
    # Iterar por cada UE e intentar asignarlo al Grid
    for ue in all_ues:
        for _ in range(ue.connections_per_day):
            # Buscar espacio para este UE en el Grid respetando los rangos de tiempo
            assigned = False
            for time_range in ue.time_ranges:
                start_time, end_time = time_range[0], time_range[1]
                
                # Revisar si hay espacio disponible en el rango de tiempo permitido
                for start_minute in range(start_time, end_time - ue.minutes_connected + 1):
                    if is_available(grid, start_minute, ue.minutes_connected):
                        # Asignamos el UE en ese espacio
                        assign_to_grid(grid, start_minute, ue.minutes_connected, ue.name)
                        assigned = True
                        break
                
                if assigned:
                    break
            
            if not assigned:
                # No se pudo asignar sin colisiones, buscar un espacio donde haya la menor cantidad de colisiones
                assign_with_min_collisions(grid, ue)

    return grid, "Resources successfully allocated."


# Función que verifica si el bloque está disponible en el Grid
def is_available(grid, start_minute, duration):
    # Asegurarse que los slots estén libres
    for i in range(start_minute, start_minute + duration):
        j=i
        while j >= 1440:
            j = j-1440
        if grid.resources[j] != 0:  # 0 significa que el slot está libre
            return False
    return True


# Función que asigna el UE al Grid
def assign_to_grid(grid, start_minute, duration, ue_name):
    for i in range(start_minute, start_minute + duration):
        j=i
        while j >= 1440:
            j = j-1440
        grid.resources[j].append(ue_name)  # Sumamos uno al slot del grid

# Función que asigna el UE con la menor cantidad de colisiones
def assign_with_min_collisions(grid, ue):
    # Buscar el lugar con la menor cantidad de colisiones dentro de los rangos
    min_collisions = float('inf')
    best_start_minute = None
    
    for time_range in ue.time_ranges:
        start_time, end_time = time_range[0], time_range[1]
        
        for start_minute in range(start_time, end_time - ue.minutes_connected + 1):
            collisions = count_collisions(grid, start_minute, ue.minutes_connected)
            
            if collisions < min_collisions:
                min_collisions = collisions
                best_start_minute = start_minute
    
    # Asignar en el mejor lugar posible
    assign_to_grid(grid, best_start_minute, ue.minutes_connected, ue.name)


# Función que cuenta las colisiones en un bloque dado
def count_collisions(grid, start_minute, duration):
    collisions = 0
    for i in range(start_minute, start_minute + duration):
        j=i
        while j >= 1440:
            j = j-1440
        if grid.resources[j] != 0:  # Si el slot ya está ocupado, cuenta como colisión
            collisions += len(grid.resources[j])
    return collisions


# Funciones auxiliares del algoritmo
def validate_types(grid, devices):
    msg = ""
    is_valid = True

    if type(grid)!=Grid:
        msg = "ERROR: El primer input del algoritmo tiene que ser de tipo Grid"
        is_valid = False
    elif type(devices)==list:
        for element in devices:
            if type(element)!=UE and type(element)!=GroupUE:
                msg = "ERROR: El segundo input del algoritmo es una lista, pero no de objetos UE o GroupUE"
                is_valid = False
    else:
        msg = "ERROR: El segundo input del algortimo tiene que ser una lista de objetos UE o GroupUE. Ej.: [GroupUE] o [UE, UE, UE]"
        is_valid = False
    
    return is_valid, msg



# # # # # # # # # # # # # # # #
# # #  RANDOM  ALGORITHM  # # #
# # # # # # # # # # # # # # # #

def random_algorithm(grid, ues_or_groups):

    # Validates that the inputs are correct types
    is_valid, msg_validation = validate_types(grid, ues_or_groups)
    if not is_valid:
        return grid, msg_validation
    
    # Obtenemos la lista de todas las UEs a asignar (expandimos los GroupUE)
    all_ues = []
    
    for ue_or_group in ues_or_groups:
        if isinstance(ue_or_group, GroupUE):
            # Expandir los GroupUE en múltiples UEs individuales
            all_ues.extend([ue_or_group.ue_parameters for _ in range(ue_or_group.number_of_ues)])
        else:
            all_ues.append(ue_or_group)
    
    # Ordenamos por el número de conexiones y rangos de tiempo para priorizar los más restrictivos
    all_ues.sort(key=lambda ue: (len(ue.time_ranges), ue.connections_per_day))
    
    # Iterar por cada UE e intentar asignarlo al Grid
    for ue in all_ues:
        for _ in range(ue.connections_per_day):
            # Buscar espacio para este UE en el Grid respetando los rangos de tiempo
            assigned = False
            for time_range in ue.time_ranges:
                start_time, end_time = time_range[0], time_range[1]
                
                # Asignar de forma aleatoria
                connection_range = end_time - start_time - ue.minutes_connected + 1
                start_minute = random.randint(start_time, start_time + connection_range)
                assign_to_grid(grid, start_minute, ue.minutes_connected, ue.name)

    return grid, "Resources randomly allocated."