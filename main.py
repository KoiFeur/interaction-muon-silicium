import parser
import sys
from colors import bcolors
import pandas as pd
import matplotlib.pyplot as plt
import analyse_reac
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter



"""
Rappel des différents objectifs :
    - Compter le nombre de réactions et le type des réactions (élastiques, inélastiques, absorption).
    Etat : fait, peut-être "améliorer" le code ?
    
    - Compter le nombre et le type de produits secondaires (gamma, protons, Mg25, Si28,….) produits par
    types de réactions et au total – Représenter graphiquement les résultats.
    Etat : nbr de sous produits total fait, pas le reste.
    
    - Tracer les histogrammes en énergie des produits secondaires par type de produits.
    
    
"""



if __name__ == "__main__":
    try:
        reactions = parser.parser("secondaries_500MeV.txt")
    except IndexError:
        print(bcolors.FAIL + "\nPlease put the name of the file here" + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)
    except FileNotFoundError:
        print(bcolors.FAIL + "Couldn't find the file, you may had misspelled it." + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)
        
    
    
                                                                        #Dans cette section, on récupère et print le nbr de réactions el, inel et abs.
    nb_type_reac = analyse_reac.reactiontype(reactions)
    nb_el = nb_type_reac[0]
    nb_inel = nb_type_reac[1]
    nb_abs = nb_type_reac[2]
    nb_total_reac = [nb_el, nb_inel, nb_abs]
    print("Il y a en tout", nb_abs+nb_el+nb_inel, "réactions.")
    print("Il y a", nb_el, "réactions/chocs élastiques.")
    print("Il y a", nb_inel, "réactions/chocs inélastiques.")
    print("Il y a", nb_abs, "absorptions.")
                                                                        #On cherche ensuite à classer sur un histograme les 3 diff types de réactions

    x = np.arange(len(nb_total_reac))
    plt.figure(figsize=(8, 5))
    plt.bar(0, nb_el, 1, label="Nombre de réactions élastiques", color = "lightskyblue")
    plt.bar(1, nb_inel, 1, label="Nombre de réactions inélastiques", color = "cornflowerblue")
    plt.bar(2, nb_abs, 1, label="Nombre d'absorptions", color = "royalblue")
    plt.xlabel("Classes de Réactions")
    plt.ylabel("Nombre d'occurrences")
    plt.title("Histogramme des Réactions")
    plt.legend()
    plt.xticks([])
    plt.show()

    
    
                                                                            #Dans cette section, on cherche à déterminer le nombre de sous-produit pour tout le fichier
    nb_sous_prod_tot = analyse_reac.nb_sous_prod_tot(reactions)
    print("Il y a au total ", nb_sous_prod_tot, "sous-produits de créés.")
                                                                               #On veut ensuite déterminer le nombre de chaque type de produits secondaires : 
                                                                                    #proton, neutron, deutron, triton, gamma, Si27, Mg25, Si28 ...
    
    print("\n")
    dic_sorted = analyse_reac.nb_sub_product(reactions)
    print(dic_sorted)

    k = 0
    for key, value in dic_sorted.items():
        plt.bar(k, value, 1, label=key)
        k += 1
    plt.yscale('log')
    plt.grid()
    plt.title("Type et quantité de chaque sous-produit")
    plt.xticks([])
    plt.show()
    
    print('\n')
    print(len(dic_sorted))
    
    new_dic = {}
    for key, value in dic_sorted.items():
        if value > 500:
            new_dic[key] = value
        else:
            continue
            
    print(new_dic)
    
    plt.barh(range(len(new_dic)), new_dic.values(), 0.5, tick_label=list(new_dic.keys()))
    plt.yscale('log')
    plt.title("Type et quantité de chaque sous-produit")
    plt.xticks(rotation=90)
    plt.show()
    """
    for key, value in new_dic.items():
        if 
    """






    energie=analyse_reac.lvl_energie(reactions)

    #print(energie["proton"])
   
    print(max(energie["proton"]))
    print(min(energie["proton"]))
    #print((energie["proton"]))
    
    energy_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_sr=[i for i in range(len(energy_ranges))]
    barres = [0] * len(energy_ranges)
    for i in range(len(energie["proton"])):
       for idx, (low, high) in enumerate(energy_ranges):
           if low <= energie["proton"][i] <= high:
               barres[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_ranges]    
    plt.bar(range(len(energy_ranges)),barres,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits proton")
    plt.show()
    
   
    print(max(energie["neutron"]))
    print(min(energie["neutron"]))
   
   
    energy_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_sr=[i for i in range(len(energy_ranges))]
    barres = [0] * len(energy_ranges)
    for i in range(len(energie["neutron"])):
       for idx, (low, high) in enumerate(energy_ranges):
           if low <= energie["neutron"][i] <= high:
               barres[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_ranges]    
    plt.bar(range(len(energy_ranges)),barres,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits neutron")
    plt.show()


    print(max(energie["gamma"]))
    print(min(energie["gamma"]))    

    energy_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_sr=[i for i in range(len(energy_ranges))]
    barres = [0] * len(energy_ranges)
    for i in range(len(energie["gamma"])):
        for idx, (low, high) in enumerate(energy_ranges):
            if low <= energie["gamma"][i] <= high:
                barres[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_ranges]    
    plt.bar(range(len(energy_ranges)),barres,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits gamma")
    plt.show()   

    
   

    
    
