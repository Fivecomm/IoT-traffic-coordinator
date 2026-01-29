from INSIGNIA_objects import UE, GroupUE, Grid


# # # # # # # # # # # # # # #
# # #  C O N F I G   1  # # #
# # # # # # # # # # # # # # #

# Creamos los perfiles de WIOTHUB, WIOTPRESS y WIOTRAD
wiothub = UE(
    name="WIOTHUB",
    connections_per_day=1, 
    minutes_connected=5, 
    time_ranges=[(0.00, 6.30), (22.00, 23.59)]
    )

wiotpress = UE(
    name="WIOTPRESS",
    connections_per_day=1, 
    minutes_connected=2, 
    time_ranges=[(0.00, 23.59)]
    )

wiotrad = UE(
    name="WIOTRAD",
    connections_per_day=1, 
    minutes_connected=5, 
    time_ranges=[(10.00, 18.00)]
    )

# Creamos varios grupos de UEs, correspondientes a varios despliegues
global_wiothubs_vlc1 = GroupUE(
    name="Global VLC",
    number_of_ues=1000,
    ue_parameters=wiothub
)

pilotos_wiotpress_vlc1 = GroupUE(
    name="Pilotos press VLC",
    number_of_ues=1400,
    ue_parameters=wiotpress
)

perte_wiotrad1 = GroupUE(
    name="Perte WIOTRAD",
    number_of_ues=600,
    ue_parameters=wiotrad
)

# # # # # # # # # # # # # # #
# # #  C O N F I G   2  # # #
# # # # # # # # # # # # # # #

# Creamos los perfiles de WIOTHUB, WIOTPRESS y WIOTRAD
wiothub2 = UE(
    name="WIOTHUB",
    connections_per_day=1, 
    minutes_connected=15, 
    time_ranges=[(0.00, 6.30), (22.00, 23.59)]
    )

# Creamos varios grupos de UEs, correspondientes a varios despliegues
global_wiothubs_vlc2 = GroupUE(
    name="Global VLC",
    number_of_ues=1000,
    ue_parameters=wiothub2
)


# # # # # # # # # # # # # # #
# # #  C O N F I G   3  # # #
# # # # # # # # # # # # # # #

wiotrad3 = UE(
    name="WIOTRAD",
    connections_per_day=1, 
    minutes_connected=5, 
    time_ranges=[(8.00, 22.00)]
    )

perte_wiotrad3 = GroupUE(
    name="Perte WIOTRAD",
    number_of_ues=600,
    ue_parameters=wiotrad3
)


# # # # # # # # # # # # # # #
# # #  C O N F I G   4  # # #
# # # # # # # # # # # # # # #

wiothub4 = UE(
    name="WIOTHUB",
    connections_per_day=1, 
    minutes_connected=15, 
    time_ranges=[(0.00, 23.59)]
    )

wiotpress4 = UE(
    name="WIOTPRESS",
    connections_per_day=1, 
    minutes_connected=2, 
    time_ranges=[(0.00, 23.59)]
    )

wiotrad4 = UE(
    name="WIOTRAD",
    connections_per_day=1, 
    minutes_connected=5, 
    time_ranges=[(0.00, 23.59)]
    )

# Creamos los grupos de UEs
global_wiothubs_vlc4 = GroupUE(
    name="Global VLC",
    number_of_ues=1000,
    ue_parameters=wiothub4
)

pilotos_wiotpress_vlc4 = GroupUE(
    name="Pilotos press VLC",
    number_of_ues=1400,
    ue_parameters=wiotpress4
)

perte_wiotrad4 = GroupUE(
    name="Perte WIOTRAD",
    number_of_ues=600,
    ue_parameters=wiotrad4
)



def config(i=0):
    if i==0:
        print("**CONFIGURACIONES**\n- 1: Original\n- 2: HUB pasa de 5 a 15 min\n- 3: RAD horario ampliado\n- 4: Todos a todas horas")
    elif i==1:
        return [pilotos_wiotpress_vlc1, global_wiothubs_vlc1, perte_wiotrad1]
    elif i==2:
        return [pilotos_wiotpress_vlc1, global_wiothubs_vlc2, perte_wiotrad1]
    elif i==3:
        return [pilotos_wiotpress_vlc1, global_wiothubs_vlc2, perte_wiotrad3]
    elif i==4:
        return [pilotos_wiotpress_vlc4, global_wiothubs_vlc4, perte_wiotrad4]
    else:
        return [pilotos_wiotpress_vlc1, global_wiothubs_vlc1, perte_wiotrad1]


def custom_config(config):
    
    # EXAMPLE OF "config" DICTIONARY
    # {
    #     "group1":{
    #         "n_ues": 200,
    #         "ue": {
    #             "connections_per_day": 1, 
    #             "minutes_connected": 5, 
    #             "time_ranges": [(0.00, 23.59)]
    #         }
    #     },
    #     "group2":{},
    #     "group3":{},
    #  }

    ues = []
    groups = []

    for i, group in enumerate(config.keys()):
        ues.append(
            UE(
                name = f"UE type {i+1}",
                connections_per_day = config[group]["ue"]["connections_per_day"], 
                minutes_connected = config[group]["ue"]["minutes_connected"], 
                time_ranges = config[group]["ue"]["time_ranges"]
            )
        )
        groups.append(
            GroupUE(
                name = f"Group type {i+1}",
                number_of_ues = config[group]["n_ues"],
                ue_parameters = ues[i]
            )
        )

    return groups

def custom_dict(ue):

    # TEST 1
    if ue == 1:
        return {
                    "group1": 
                    {
                        "n_ues": 1000,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(0.00, 6.30), (22.00, 23.59)]
                        }
                    },
                    "group2": 
                    {
                        "n_ues": 600,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(10.00, 18.00)]
                        }
                    },
                    "group3": 
                    {
                        "n_ues": 1400,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 2, 
                            "time_ranges": [(0.00, 23.59)]
                        }
                    },
                    
                }
    
    # TEST 2
    elif ue == 2:
        return {
                    "group1": 
                    {
                        "n_ues": 1000,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(0.00, 23.59)]
                        }
                    },
                    "group2": 
                    {
                        "n_ues": 1400,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 2, 
                            "time_ranges": [(0.00, 23.59)]
                        }
                    },
                    "group3": 
                    {
                        "n_ues": 600,
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(0.00, 23.59)]
                        }
                    },
                    
                }
    
    else:
        return {
                    "group1": 
                    {
                        "n_ues": int(ue/3),
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(0.00, 6.30), (22.00, 23.59)]
                        }
                    },
                    "group2": 
                    {
                        "n_ues": int(ue*14/30),
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 2, 
                            "time_ranges": [(0.00, 23.59)]
                        }
                    },
                    "group3": 
                    {
                        "n_ues": int(ue*6/30),
                        "ue": 
                        {
                            "connections_per_day": 1, 
                            "minutes_connected": 5, 
                            "time_ranges": [(10.00, 18.00)]
                        }
                    },
                    
                }