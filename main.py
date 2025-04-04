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



def main(file):
    reactions = parser.parser(file)
    if type(reactions) == type(1):
        print(f"{bcolors.FAIL}Error : reactions returned 1 exit status{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Please read the error above or Debug the file{bcolors.ENDC}")

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
    


    energy=analyse_reac.lvl_energy(reactions)


    #j'ai juré va falloir tout changer ça là ya du rouge partout chez moi ça casse la tête
    #+ ya explicitement marqué dans le truc qu'il y a obligation de ne pas utiliser du hard coding
    """
    energy_rangesNe = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_srNe=[i for i in range(len(energy_rangesNe))]
    barresNe = [0] * len(energy_rangesNe)
    for i in range(len(energy["neutron"])):
       for idx, (low, high) in enumerate(energy_rangesNe):
           if low <= energy["neutron"][i] <= high:
               barresNe[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesNe]    
    plt.bar(range(len(energy_rangesNe)),barresNe,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits neutron")
    plt.show()
    print(f"Le maximum d'énergie des sous produits neutron est : {max(energy['neutron'])}")
    print(f"Le minimum d'énergie des sous produits neutron est : {min(energy['neutron'])}")  


    energy_rangesGam = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 16), (16, 18)]
    nb_srGam=[i for i in range(len(energy_rangesGam))]
    barresGam = [0] * len(energy_rangesGam)
    for i in range(len(energy["gamma"])):
        for idx, (low, high) in enumerate(energy_rangesGam):
            if low <= energy["gamma"][i] <= high:
                barresGam[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesGam]    
    plt.bar(range(len(energy_rangesGam)),barresGam,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits gamma")
    plt.show()
    print(f"Le maximum d'énergie des sous produits gamma est : {max(energy['gamma'])}")
    print(f"Le minimum d'énergie des sous produits gamma est : {min(energy['gamma'])}")    
    
    
    energy_rangesPr = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400), (400, 450), (450, 500)]
    nb_srPr=[i for i in range(len(energy_rangesPr))]
    barresPr = [0] * len(energy_rangesPr)
    for i in range(len(energy["proton"])):
       for idx, (low, high) in enumerate(energy_rangesPr):
           if low <= energy["proton"][i] <= high:
               barresPr[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesPr]    
    plt.bar(range(len(energy_rangesPr)),barresPr,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits proton")
    plt.show()
    print(f"Le maximum d'énergie des sous produits proton est : {max(energy['proton'])}")
    print(f"Le minimum d'énergie des sous produits proton est : {min(energy['proton'])}")  
    
    
    energy_rangesSi = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 9), (9, 10)]
    nb_srSi=[i for i in range(len(energy_rangesSi))]
    barresSi = [0] * len(energy_rangesSi)
    for i in range(len(energy["Si28"])):
        for idx, (low, high) in enumerate(energy_rangesSi):
            if low <= energy["Si28"][i] <= high:
                barresSi[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesSi]    
    plt.bar(range(len(energy_rangesSi)),barresSi,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits Si28")
    plt.show()
    print(f"Le maximum d'énergie des sous produits Si28 est : {max(energy['Si28'])}")
    print(f"Le minimum d'énergie des sous produits Si28 est : {min(energy['Si28'])}")  
        

    energy_rangesAl = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70)]
    nb_srAl=[i for i in range(len(energy_rangesAl))]
    barresAl = [0] * len(energy_rangesAl)
    for i in range(len(energy["alpha"])):
        for idx, (low, high) in enumerate(energy_rangesAl):
            if low <= energy["alpha"][i] <= high:
                barresAl[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesAl]    
    plt.bar(range(len(energy_rangesAl)),barresAl,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits alpha")
    plt.show()
    print(f"Le maximum d'énergie des sous produits alpha est : {max(energy['alpha'])}")
    print(f"Le minimum d'énergie des sous produits alpha est : {min(energy['alpha'])}")  
       

    energy_rangesDe = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
    nb_srDe=[i for i in range(len(energy_rangesDe))]
    barresDe = [0] * len(energy_rangesDe)
    for i in range(len(energy["deuteron"])):
        for idx, (low, high) in enumerate(energy_rangesDe):
            if low <= energy["deuteron"][i] <= high:
                barresDe[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesDe]    
    plt.bar(range(len(energy_rangesDe)),barresDe,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits deuteron")
    plt.show()
    print(f"Le maximum d'énergie des sous produits deuteron est : {max(energy['deuteron'])}")
    print(f"Le minimum d'énergie des sous produits deuteron est : {min(energy['deuteron'])}")  
    
    
    energy_rangesAl27 = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14)]
    nb_srAl27=[i for i in range(len(energy_rangesAl27))]
    barresAl27 = [0] * len(energy_rangesAl27)
    for i in range(len(energy["Al27"])):
        for idx, (low, high) in enumerate(energy_rangesAl27):
            if low <= energy["Al27"][i] <= high:
                barresAl27[idx] += 1
    name=[f"{low}-{high}eV" for  low, high in energy_rangesAl27]    
    plt.bar(range(len(energy_rangesAl27)),barresAl27,tick_label=name)
    plt.xticks(rotation=90)
    plt.title("energys des sous produits Al27")
    plt.show()
    print(f"Le maximum d'énergie des sous produits Al27 est : {max(energy['Al27'])}")
    print(f"Le minimum d'énergie des sous produits Al27 est : {min(energy['Al27'])}") 
    """





if __name__ == "__main__":
    liste = np.array(["secondaries_1GeV.txt", "secondaries_1MeV.txt", "secondaries_500MeV.txt"])
    liste = ["testing_limit.txt"]
    for i in liste:
        print(f"Executing file {i}")
        main(i)
