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
    nb_type_reac, dic_el, dic_inel, dic_abs = analyse_reac.reactiontype(reactions)
    nb_el = nb_type_reac[0]
    nb_inel = nb_type_reac[1]
    nb_abs = nb_type_reac[2]
    nb_total_reac = [nb_el, nb_inel, nb_abs]
    print("Il y a en tout", nb_abs+nb_el+nb_inel, "réactions.")
    print("Il y a", nb_el, "réactions/chocs élastiques.")
    print("Il y a", nb_inel, "réactions/chocs inélastiques.")
    print("Il y a", nb_abs, "absorptions.")
    print(dic_el)
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

    
   
   
    energy_rangesNe = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_srNe=[i for i in range(len(energy_rangesNe))]
    barresNe = [0] * len(energy_rangesNe)
    for i in range(len(energie["neutron"])):
       for idx, (low, high) in enumerate(energy_rangesNe):
           if low <= energie["neutron"][i] <= high:
               barresNe[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesNe]    
    plt.bar(range(len(energy_rangesNe)),barresNe,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits neutron")
    plt.show()
    print(f"Le maximum d'énergie des sous produits neutron est : {max(energie['neutron'])}")
    print(f"Le minimum d'énergie des sous produits neutron est : {min(energie['neutron'])}")  


    energy_rangesGam = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 16), (16, 18)]
    nb_srGam=[i for i in range(len(energy_rangesGam))]
    barresGam = [0] * len(energy_rangesGam)
    for i in range(len(energie["gamma"])):
        for idx, (low, high) in enumerate(energy_rangesGam):
            if low <= energie["gamma"][i] <= high:
                barresGam[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesGam]    
    plt.bar(range(len(energy_rangesGam)),barresGam,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits gamma")
    plt.show()
    print(f"Le maximum d'énergie des sous produits gamma est : {max(energie['gamma'])}")
    print(f"Le minimum d'énergie des sous produits gamma est : {min(energie['gamma'])}")    
    
    
    energy_rangesPr = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_srPr=[i for i in range(len(energy_rangesPr))]
    barresPr = [0] * len(energy_rangesPr)
    for i in range(len(energie["proton"])):
       for idx, (low, high) in enumerate(energy_rangesPr):
           if low <= energie["proton"][i] <= high:
               barresPr[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesPr]    
    plt.bar(range(len(energy_rangesPr)),barresPr,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits proton")
    plt.show()
    print(f"Le maximum d'énergie des sous produits proton est : {max(energie['proton'])}")
    print(f"Le minimum d'énergie des sous produits proton est : {min(energie['proton'])}")  
    
    
    energy_rangesSi = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 9), (9, 10)]
    nb_srSi=[i for i in range(len(energy_rangesSi))]
    barresSi = [0] * len(energy_rangesSi)
    for i in range(len(energie["Si28"])):
        for idx, (low, high) in enumerate(energy_rangesSi):
            if low <= energie["Si28"][i] <= high:
                barresSi[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesSi]    
    plt.bar(range(len(energy_rangesSi)),barresSi,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits Si28")
    plt.show()
    print(f"Le maximum d'énergie des sous produits Si28 est : {max(energie['Si28'])}")
    print(f"Le minimum d'énergie des sous produits Si28 est : {min(energie['Si28'])}")  
        

    energy_rangesAl = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70)]
    nb_srAl=[i for i in range(len(energy_rangesAl))]
    barresAl = [0] * len(energy_rangesAl)
    for i in range(len(energie["alpha"])):
        for idx, (low, high) in enumerate(energy_rangesAl):
            if low <= energie["alpha"][i] <= high:
                barresAl[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesAl]    
    plt.bar(range(len(energy_rangesAl)),barresAl,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits alpha")
    plt.show()
    print(f"Le maximum d'énergie des sous produits alpha est : {max(energie['alpha'])}")
    print(f"Le minimum d'énergie des sous produits alpha est : {min(energie['alpha'])}")  
       

    energy_rangesDe = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
    nb_srDe=[i for i in range(len(energy_rangesDe))]
    barresDe = [0] * len(energy_rangesDe)
    for i in range(len(energie["deuteron"])):
        for idx, (low, high) in enumerate(energy_rangesDe):
            if low <= energie["deuteron"][i] <= high:
                barresDe[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesDe]    
    plt.bar(range(len(energy_rangesDe)),barresDe,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits deuteron")
    plt.show()
    print(f"Le maximum d'énergie des sous produits deuteron est : {max(energie['deuteron'])}")
    print(f"Le minimum d'énergie des sous produits deuteron est : {min(energie['deuteron'])}")  
    
    
    energy_rangesAl27 = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14)]
    nb_srAl27=[i for i in range(len(energy_rangesAl27))]
    barresAl27 = [0] * len(energy_rangesAl27)
    for i in range(len(energie["Al27"])):
        for idx, (low, high) in enumerate(energy_rangesAl27):
            if low <= energie["Al27"][i] <= high:
                barresAl27[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesAl27]    
    plt.bar(range(len(energy_rangesAl27)),barresAl27,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("Energies des sous produits Al27")
    plt.show()
    print(f"Le maximum d'énergie des sous produits Al27 est : {max(energie['Al27'])}")
    print(f"Le minimum d'énergie des sous produits Al27 est : {min(energie['Al27'])}") 