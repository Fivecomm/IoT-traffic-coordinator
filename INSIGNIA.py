# # # # # # # # # # # # # # # # # # # # # #
# FIVECOMM ©                              #
# Author: Miguel Cantero                  #
# Mail: miguel.cantero@fivecomm.eu        #
# Version: v1.0                           #
# # # # # # # # # # # # # # # # # # # # # #

from INSIGNIA_objects import UE, GroupUE, Grid
from INSIGNIA_algorithm import allocation_algorithm, random_algorithm
from INSIGNIA_functions import generate_ues_base_values, save_json, load_json, plot2, plot3_getvalues, plot3, read_batch_from_file
from Configurations_UEs import config, custom_config, custom_dict
import numpy as np
import argparse

# CONFIGURATION PARAMETERS #############################
base_ues = False
plot_1 = True
plot_2 = True
print_values = True
save_json_in_file = True
ues = [20000, 25000, 30000]
load_from_file = ""
########################################################


def parse_arguments():
    """Parse command line arguments with default values"""
    parser = argparse.ArgumentParser(
        description='INSIGNIA Simulation - Resource Allocation Algorithm',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Parámetros booleanos
    parser.add_argument('--base-ues', action='store_true', default=base_ues,
                        help='Use base UEs values from statistics')
    parser.add_argument('--plot1', action='store_true', default=plot_1,
                        help='Enable plot 1 (grid algorithm visualization)')
    parser.add_argument('--plot2', action='store_true', default=plot_2,
                        help='Enable plot 2 (comparison visualization)')
    parser.add_argument('--print-values', action='store_true', default=print_values,
                        help='Enable printing values')
    parser.add_argument('--save-json', action='store_true', default=save_json_in_file,
                        help='Save JSON files')
    
    # Lista de UEs a simular
    parser.add_argument('--ues', type=int, nargs='+', default=[20000, 25000, 30000],
                        help='List of UE numbers to simulate')
    
    # Archivo a cargar
    parser.add_argument('--load', type=str, default='',
                        help='JSON file to load (leave empty to simulate new data)')
    
    # Opción para modo no interactivo
    parser.add_argument('--non-interactive', action='store_true',
                        help='Run in non-interactive mode (skip input prompt for load file)')
    
    return parser.parse_args()


# Update the configuration values based on command line arguments
args = parse_arguments()
base_ues = args.base_ues
plot_1 = args.plot1  # Por defecto True
plot_2 = args.plot2  # Por defecto True
print_values = args.print_values  # Por defecto True
save_json_in_file = args.save_json  # Por defecto True
ues = args.ues
load_from_file = args.load

# Mostrar configuración
base_msg = '- With UEs base\n' if base_ues else '- Without UEs base\n'
plot1_msg = '- Plot 1 enabled\n' if plot_1 else '- Plot 1 disabled\n'
plot2_msg = '- Plot 2 enabled\n' if plot_2 else '- Plot 2 disabled\n'
print_msg = '- Print values enabled\n' if print_values else '- Print values disabled\n'
save_msg = '- Save JSON\n' if save_json_in_file else '- Do not save JSON\n'
ues_msg = f'- UEs to simulate: {ues}\n'
dict_msg = f'- Custom dictionary UE type (for {ues[0]} UEs): {custom_dict(ues[0])}\n'

options = f"{base_msg}{plot1_msg}{plot2_msg}{print_msg}{save_msg}{ues_msg}{dict_msg}"
print("Configuration options:\n" + options)

# Si no se especificó un archivo para cargar y no está en modo no interactivo, preguntar
if load_from_file == "" and not args.non_interactive:
    load_from_file = input("Filename to load / Enter to simulate / 'q' for exiting: ")
    if load_from_file == "q":
        print("Exiting...")
        quit()
    
if load_from_file != "":
    load_from_file = load_from_file.replace(".json", "") + ".json"

########################################################

##### R U N #####
def run(
        base_ues, 
        plot_1, 
        plot_2, 
        print_values, 
        save_json_in_file, 
        load_from_file, 
        custom_config_dict, 
        json_name=""
    ):

    # Configuraciones preestablecidas
    # groups_list = config(1)
    groups_list = custom_config(custom_config_dict)


    # grid = Grid()

    # Se crean los objetos Grid para cada algoritmo
    grid_random = Grid()
    grid_algorithm = Grid()


    # Si no se carga desde archivo, se simula
    if load_from_file == "": 
        print("Simulating new data...")
        # SET THE BASE VALUES FROM STATISTICS
        if base_ues:
            grid_random.set_base_ues(generate_ues_base_values())
            grid_algorithm.set_base_ues(generate_ues_base_values())

        # CREATE ALGORITM THAT SELECTS EACH UE ALLOCATION IN THE GRID
        for group in groups_list:
            grid_random, msg = random_algorithm(grid_random, [group]) #, pilotos_wiotpress_vlc])
            grid_algorithm, msg = allocation_algorithm(grid_algorithm, [group]) #, pilotos_wiotpress_vlc])

        print(msg)

    # Si se carga desde archivo, se leen los datos
    else:
        data = load_json(load_from_file)
        print("Succesfully readed from datafile")

        grid_random.resources = data["random"]
        grid_algorithm.resources = data["algorithm"]



    # Print values
    if print_values:
        _print_values(grid_random, grid_algorithm)

    # Save JSON files
    if save_json_in_file and load_from_file=="":
        _save_json(grid_random, grid_algorithm, json_name)

    # Plots
    if plot_1:
        plot1(grid_random, grid_algorithm)
    if plot_2:
        plot2(grid_random, grid_algorithm)

    

def _print_values(grid_random, grid_algorithm):
    # RANDOM ####################################################################
    resources = list(grid_random.get_statistics().values())
    v_random = [max(resources), np.percentile(resources, 98), np.percentile(resources, 95), np.percentile(resources, 90),
                    np.percentile(resources, 70), np.percentile(resources, 50)]
    print("\nRANDOM")
    print(f"Max: {v_random[0]}")
    print(f"98%: {int(v_random[1])}")
    print(f"95%: {int(v_random[2])}")
    print(f"90%: {int(v_random[3])}")
    print(f"70%: {int(v_random[4])}")
    print(f"50%: {int(v_random[5])}")


    # ALGORITHM ##################################################################
    resources = list(grid_algorithm.get_statistics().values())
    v_algorithm = [max(resources), np.percentile(resources, 98), np.percentile(resources, 95), np.percentile(resources, 90),
                    np.percentile(resources, 70), np.percentile(resources, 50)]
    print("\nALGORITHM")
    print(f"Max: {v_algorithm[0]}")
    print(f"98%: {int(v_algorithm[1])}")
    print(f"95%: {int(v_algorithm[2])}")
    print(f"90%: {int(v_algorithm[3])}")
    print(f"70%: {int(v_algorithm[4])}")
    print(f"50%: {int(v_algorithm[5])}")


    # LOAD REDUCTION ##############################################################
    print("\nLOAD REDUCTION (RANDOM -> ALGORITHM)")
    print(f"Max: {round(100*(v_random[0]-v_algorithm[0])/v_random[0], 2)}%")
    print(f"98%: {round(100*(v_random[1]-v_algorithm[1])/v_random[1], 2)}%")
    print(f"95%: {round(100*(v_random[2]-v_algorithm[2])/v_random[2], 2)}%")
    print(f"90%: {round(100*(v_random[3]-v_algorithm[3])/v_random[3], 2)}%")
    print(f"70%: {round(100*(v_random[4]-v_algorithm[4])/v_random[4], 2)}%")
    print(f"50%: {round(100*(v_random[5]-v_algorithm[5])/v_random[5], 2)}%")


def _save_json(grid_random, grid_algorithm, json_name):
    save_json({"random": grid_random.resources, "algorithm": grid_algorithm.resources}, json_name)


def plot1(grid_random, grid_algorithm):
    grid_random.plot()
    grid_algorithm.plot()


##### PROCESS BATCHES #####
def process_batch(batches_list, ues):

    grid_random = Grid()
    grid_algorithm = Grid()

    limite_ues = 0.90
    resources_random = []
    resources_algorithm = []

    for batch in batches_list:
        data = load_json(batch)
        print("Succesfully readed from datafile")

        # Carga los valores en objetos Grid
        grid_random.resources = data["random"]
        grid_algorithm.resources = data["algorithm"]

        value_random = plot3_getvalues(grid_random, limite_ues)
        print("RANDOM:", value_random)
        value_algorithm = plot3_getvalues(grid_algorithm, limite_ues)
        print("ALGORITHM:", value_algorithm)
    
        resources_random.append(value_random)
        resources_algorithm.append(value_algorithm)

    print("RANDOM")
    print(resources_random)
    print("ALGORITHM")
    print(resources_algorithm)

    print("LEN UEs:", len(ues))
    print("LEN Resources:", len(resources_algorithm))
    plot3(resources_random, resources_algorithm, ues, limite_ues)


##### MAIN #####

# INSIGNIA: Process multiple batches defined in batches.txt

# batch_filename = "batch copy.txt"
# batches = read_batch_from_file(filename=batch_filename)
# process_batch(batches, ues)


# ues = range(2000, 10000, 500)
for ue in ues:
    json_name = f"{ue}UEs_"
    custom_config_dict = custom_dict(ue) # Genera el dictionary que incluye las configuraciones de los UEs (Configurations_UEs.py)
    
    run(base_ues, 
        plot_1, 
        plot_2, 
        print_values, 
        save_json_in_file, 
        load_from_file, 
        custom_config_dict, 
        json_name
        )