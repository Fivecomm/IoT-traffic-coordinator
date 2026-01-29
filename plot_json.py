import json
import matplotlib.pyplot as plt


lines_dpi = 250
wiots_dpi = 250


filename = input("Nombre del archivo JSON: ")
graph_type = input("Tipo de gráfica:\n1: Data WIOTs\n2: Data Random y Coordinated a)\n3: Data Random y Coordinated b)\n4: Data Transversal\nSelección: ")

# 1️ Cargar el JSON
with open(""+filename+".json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Data WIOTs
if graph_type == "1":
    ylimit = input("Límite Y (dejar vacío para automático): ")
    
    x = data["x"]
    y = data["y"]
    # base = y["base"]
    # wiothub = y["WIOTHUB"]
    # wiotpress = y["WIOTPRESS"]
    # wiotrad = y["WIOTRAD"]

    colors = {"base": "grey", "WIOTHUB": "orange", "WIOTPRESS": "green", "WIOTRAD": "red", "UE type 1": "orange", "UE type 2": "green", "UE type 3": "red"}
    
    plt.figure(figsize=(1100/wiots_dpi, 900/wiots_dpi), dpi=wiots_dpi)

    # plot en stack bar
    last_plot = [0 for e in range(24*60)]
    for device_type in y.keys():
        plt.bar(range(24*60), y[device_type], bottom=last_plot, color=colors[device_type], width=1.0)
        for i in range(24*60):
            last_plot[i] += y[device_type][i]

    # Mostrar horas en el eje X, no minutos
    plt.xticks(
        ticks=[i for i in range(0, 1441, 120)],
        labels=[f"{i//60:02d}" for i in range(0, 1441, 120)]
    )

    plt.xlabel("Horas del día")
    plt.ylabel("Recursos de la red")
    plt.legend(y.keys())
    if ylimit != "":
        plt.ylim(0, int(ylimit))


    # GUARDAR
    figure_name = filename # input("Nombre del archivo para guardar la gráfica (dejar vacío para no guardar): ")
    if figure_name != "":
        plt.savefig(f'INSIGNIA results/figuras/{figure_name}.png')


    plt.show(block=True)

# Data Random y Coordinated
# 2: Slots saturados (%)
# 3: UEs servidos (%)
# 4: Recursos para X% de UEs servidos
elif graph_type == "2" or graph_type == "3" or graph_type == "4":
    x = data["x"]
    random = data["Random"]
    coordinated = data["Algorithm"]

    # Para pasar de escala 0-1 a 0-100
    random = [e*100 for e in random]
    coordinated = [e*100 for e in coordinated]

    fig, ax = plt.subplots(figsize=(1100/lines_dpi, 900/lines_dpi), dpi=lines_dpi)

    # Primer gráfico
    ax.plot(x, random, label = "Aleatorio")

    # Segundo gráfico
    ax.plot(x, coordinated, label = "Coordinado")

    if graph_type == "2":
        # Seleccionamos que muestra en el eje Y
        plt.yticks(
            ticks=[i for i in range(0, 144001, 28800)],
            labels=[f"{i/1440:.0f}" for i in range(0, 144001, 28800)]
        )
        ax.set_xlabel("Recursos de red")
        ax.set_ylabel("Slots saturados (%)")
        ax.set_title("Slots saturados")
    
    elif graph_type == "3":
        # Seleccionamos que muestra en el eje Y
        plt.yticks(
            ticks=[i for i in range(0, 101, 20)],
            labels=[f"{i:.0f}" for i in range(0, 101, 20)]
        )
        ax.set_xlabel("Recursos de red")
        ax.set_ylabel("UEs servidos (%)")
        ax.set_title("UEs servidos")
    
    elif graph_type == "4":
        ymax = input("Límite MAX Y (dejar vacío para automático): ")
        if ymax != "":
            ymin = input("Límite MIN Y (dejar vacío para automático): ")
            if ymin == "":
                plt.ylim(0, int(ymax))
            else:
                plt.ylim(int(ymin), int(ymax))
        porcentaje = input("Porcentaje de UEs: ")
        ax.set_xlabel("UEs totales simulación")
        ax.set_ylabel("Recursos")
        ax.set_title(f"Recursos para {porcentaje}% de UEs servidos")
    ax.legend()

    plt.tight_layout()

    # GUARDAR
    figure_name = filename # input("Nombre del archivo para guardar la gráfica (dejar vacío para no guardar): ")
    if figure_name != "":
        plt.savefig(f'INSIGNIA results/figuras/{figure_name}.png')

    # plt.figure(figsize=(1000/dpi, 1000/dpi), dpi=dpi)
    plt.show()

# Error input
else:
    print("Tipo de gráfica no válido")







