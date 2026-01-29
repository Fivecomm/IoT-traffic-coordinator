# # # # # # # # # # # # # # # # # # # # # #
# FIVECOMM ©                              #
# Author: Miguel Cantero                  #
# Mail: miguel.cantero@fivecomm.eu        #
# Version: v1.0                           #
# # # # # # # # # # # # # # # # # # # # # #

import random
import matplotlib.pyplot as plt
import datetime


##############################################################
# UE
# Description: Describes a UE with all its characteristics
##############################################################
class UE:
    def __init__(self, name = "UE", connections_per_day = 1, minutes_connected = 10, time_ranges = [(0, 23.59)]):
        self.name = name                                    # Nombre del grupo de UEs
        self.connections_per_day = connections_per_day      # Número de conexiones por día
        self.minutes_connected = minutes_connected                # Tiempo total conectado (en minutos)
        self.time_ranges = self.time_ranges_parsing(time_ranges)   # Rango de tiempos de conexión (lista de pares de horas)
        self.selected_time = -1                 # Hora seleccionada por el algoritmo para que envíe el UE
        self.is_selected_time_random = False

        self.allowed_allocations = self.get_allowed_allocations()
        self.random_allocation()

    def random_allocation(self):
        if self.selected_time < 0:
            self.selected_time = random.choice(self.allowed_allocations)
            self.is_selected_time_random = True
        else:
            print("El UE ya tiene asignada una hora:", self.min_to_time(self.selected_time))

    def get_allowed_allocations(self):
        allowed_allocations = []
        for _range in self.time_ranges:
            for i in range(int(_range[0]), int(_range[1])):
                allowed_allocations.append(i)
        return allowed_allocations
    
    def select_time_ue(self, time):
        in_minutes = self.time_to_min(time)
        self.allowed_allocations = self.get_allowed_allocations() # Update the available time ranges
        if in_minutes in self.allowed_allocations:
            self.selected_time = in_minutes
            self.is_selected_time_random = False
            print(f"UE successfully configurated at {self.min_to_time_str(in_minutes)}")
        else:
            print(f"**ERROR: {self.min_to_time_str(in_minutes)} not possible in the avaiable time ranges: {self.time_ranges_reverse_parsing(self.time_ranges)}**")

    def time_ranges_parsing(self, time_ranges):
        for i, range in enumerate(time_ranges):
            time_ranges[i] = (self.time_to_min(range[0]), self.time_to_min(range[1]))
        return time_ranges

    def time_to_min(self, time):
        in_minutes = int(time)*60 + (time-int(time))*100
        return int(in_minutes)
    
    def time_ranges_reverse_parsing(self, time_ranges):
        for i, range in enumerate(time_ranges):
            time_ranges[i] = (self.min_to_time(range[0]), self.min_to_time(range[1]))
        return time_ranges
    
    def min_to_time(self, in_minutes):
        hours = in_minutes // 60
        minutes = in_minutes % 60
        return hours + minutes/100

    def min_to_time_str(self, in_minutes):
        hours = in_minutes // 60
        minutes = in_minutes % 60
        if minutes < 10 : minutes = "0"+str(minutes)
        return f"{hours}:{minutes}"

    def display_info(self):
        print(f"Nombre: {self.name}")
        print(f"Conexiones por día: {self.connections_per_day}")
        print(f"Minutos conectado: {self.minutes_connected}")
        print(f"Rangos de conexión: {self.time_ranges_reverse_parsing(self.time_ranges)}")
        print(f"Hora asignada por la red: {self.min_to_time_str(self.selected_time)} (random={self.is_selected_time_random})")


##############################################################
# GroupUE
# Description: Describes a group of UEs with the same UE profile
##############################################################
class GroupUE:
    def __init__(self, name="group", number_of_ues=1, ue_parameters=UE()):
        self.name = name
        self.number_of_ues = number_of_ues
        self.ue_parameters = ue_parameters
        self.ue_allocation_list = []

    def display_info(self):
        print()
        print(f"Nombre: {self.name}")
        print(f"Número de UEs: {self.number_of_ues}")
        print(f"Parámetros de los UEs:\n- UE: {self.ue_parameters.name}\n- Conexiones por día: {self.ue_parameters.connections_per_day}\n- Minutos conectado: {self.ue_parameters.minutes_connected}\n- Rango de conexión: {self.ue_parameters.time_ranges}")
        print()


##############################################################
# Grid
# Description: Describes a grid object, where all the resources 
#              will be distributed
##############################################################
class Grid:
    def __init__(self):
        self.resources = [[] for i in range(24 * 60)]     # Bloques de recursos de 1 minuto
        self.other_devices = [0 for i in range(24 * 60)]  # UEs externos de los que se parte como base. Por defecto sería cero (ningún UE externo)

    def add(self, init, end, resources=1):
        for slot in range(self.time_to_min(init), self.time_to_min(end)):
            self.resources[slot] += resources

    def set_base_ues(self, other_devices=[0 for i in range(24 * 60)]):
        if type(other_devices)==list and len(other_devices)==24*60:
            # self.other_devices = other_devices
            for i, devices in enumerate(other_devices):
                for device in range(int(devices)):
                    self.resources[i].append("base")
        else:
            print("ERROR: Los valores de los UEs de fondo no tienen un formato correcto. Deben ser una lista de 1440 int e.g.: [0, 1 ... 1438, 1439]")

    def time_to_min(self, time):
        in_minutes = int(time)*60 + (time-int(time))*100
        return int(in_minutes)

    def display_info(self):
        print(f"Resources: {self.resources}")

    def select_color(self, device_type):
        color = "purple"
        if device_type == "base":
            color = "grey"
        elif device_type == "WIOTHUB" or device_type == "UE type 1":
            color = "orange"
        elif device_type == "WIOTPRESS" or device_type == "UE type 2":
            color = "green"
        elif device_type == "WIOTRAD" or device_type == "UE type 3":
            color = "red"
        return color
    
    def get_statistics(self):
        resource_dict = {}

        for i, resource in enumerate(self.resources):
            resource_dict[i] = 0
            for ue in resource:
                resource_dict[i] += 1
        
        return resource_dict

    def plot(self):
        
        different_names = []
        resource_dict = {}

        for i, resource in enumerate(self.resources):
            for name in resource:
                if name not in different_names:
                    different_names.append(name)
                    resource_dict[name] = [0 for e in range(24*60)]
                resource_dict[name][i] += 1

        # GUARDAR LA GRÁFICA EN JSON ########
        import json
        data = {
            "x": list(range(24*60)), 
            "y": resource_dict
        }
        with open("plot1.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        #####################################

        # print(resource_dict)

        # plot en stack bar
        last_plot = [0 for e in range(24*60)]
        for device_type in resource_dict.keys():
            plt.bar(range(24*60), resource_dict[device_type], bottom=last_plot, color=self.select_color(device_type))
            for i in range(24*60):
                last_plot[i] += resource_dict[device_type][i]
        plt.xlabel("One day")
        plt.ylabel("Network resources")
        plt.legend(resource_dict.keys())

        # FOR AROMA3D RESULTS
        plt.ylim(0,70)
        # plt.legend(["UE type 1", "UE type 2", "UE type 3"])

        # Mostrar el gráfico
        # plt.show()
        # Guardar el gráfico
        date = f'{datetime.datetime.now()}'.replace(":",".")
        plt.savefig(f'{date}.png')

    def plot2(self):
        resources_per_slot = [0 for e in range(24*60)]

        for i, resource in enumerate(self.resources):
            resources_per_slot[i] = len(resource)

        total_slots = sum(resources_per_slot)  # Recursos totales utilizados en un día
        max_resources = max(resources_per_slot)  # Recursos en el slot con más carga del día
        slots_saturados = [0 for e in range(max_resources)]  # Slots que saturan para cada valor de carga hasta el máximo
        porcentaje_slots_servidos = [0 for e in range(max_resources)]
        porcentaje_ues_servidos = [0 for e in range(max_resources)]

        # Por cada X recursos tope
        for nivel_saturacion in range(max_resources):
            
            # Cada slot para los X recursos tope
            for resource_slot in resources_per_slot:
                
                if resource_slot > nivel_saturacion:
                    slots_saturados[nivel_saturacion] += 1
            
            porcentaje_slots_servidos[nivel_saturacion] = (1440 - slots_saturados[nivel_saturacion])/1440
                    
        
        # plt.bar(range(max_resources), slots_saturados)
        # plt.xlabel("One day")
        # plt.ylabel("Network resources")
        # plt.show()

        # Crear una figura con dos subgráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Primer gráfico de barras
        ax1.bar(range(max_resources), slots_saturados)
        ax1.set_xlabel("Resources")
        ax1.set_ylabel("Slots saturated")
        ax1.set_title("Slots saturados")

        # Segundo gráfico de barras
        ax2.bar(range(max_resources), porcentaje_slots_servidos)
        ax2.set_xlabel("Resources")
        ax2.set_ylabel("Slots served")
        ax2.set_title("% slots servidos")

        # Mostrar los gráficos
        plt.tight_layout()
        plt.show()


##############################################################
# USAGE EXAMPLES
##############################################################

# # Ejemplo de uso
# wiothub = UE(
#     name="WIOTHUB",
#     connections_per_day=5, 
#     minutes_connected=120, 
#     time_ranges=[(0.00, 6.00), (12.00, 15.00)]
#     )

# wiothub.display_info()
# print()
# # wiothub.select_time_ue(18.00)
# # print()
# # wiothub.display_info()

# group = GroupUE(
#     name="WIOTHUBs-vlc",
#     number_of_ues=3,
#     ue_parameters=wiothub
# )

# group.display_info()
