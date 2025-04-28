# Exemple de dictionnaire contenant des noms de sous-produits et leur nombre d'apparitions

# Trier le dictionnaire par valeurs (nombre d'apparitions) en ordre décroissant
import parser
import sys
from colors import bcolors
import pandas as pd
import matplotlib.pyplot as plt
import analyse_reac
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
def main(file):
    reactions = parser.parser(file)
    if type(reactions) == type(1):
        print(f"{bcolors.FAIL}Error : reactions returned 1 exit status{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Please read the error above or Debug the file{bcolors.ENDC}")

                                                                        #Dans cette section, on récupère et print le nbr de réactions el, inel et abs.
    nb_type_reac, dic_el, dic_inel, dic_abs = analyse_reac.reactiontype(reactions)
    print(nb_type_reac.items())
    nb_el = nb_type_reac['Elastic']
    nb_inel = nb_type_reac['Inelastic']
    nb_abs = nb_type_reac['Absorptions']
    nb_total_reac = [nb_el, nb_inel, nb_abs]
    print("There are", nb_abs+nb_el+nb_inel, "reactions.")
    print("There are", nb_el, "elastic reactions/chocs,", nb_inel, "inelastic reactions/chocs, et", nb_abs, "absorptions.")
    
    plt.bar(0, nb_el, 1, label="Number of elastic reactions", color = "lightskyblue")
    plt.bar(1, nb_inel, 1, label="Number of inelastic reactions", color = "cornflowerblue")
    plt.bar(2, nb_abs, 1, label="Number of absorptions", color = "royalblue")    
    q = 0
    for nbtypereac in nb_total_reac:
        plt.text(q, nbtypereac, nbtypereac)
        q += 1
    plt.xlabel("Reaction's type")
    plt.ylabel("Number of occurrences")
    plt.title("Reaction's histogram")
    plt.legend()
    plt.xticks([])
    plt.show()
sous_produits_tries = sorted(dic_el.items(), key=lambda item: item[1], reverse=True)


top_7_sous_produits = sous_produits_tries[:7]


print("Les 7 sous-produits les plus fréquents sont :")
for produit, apparitions in top_7_sous_produits:
    print(f"{produit}: {apparitions} apparitions")


