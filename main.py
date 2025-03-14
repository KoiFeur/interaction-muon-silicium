import parser
import sys
from colors import bcolors
import pandas as pd
import matplotlib.pyplot as plt
import analyse_reac
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter


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
    plt.bar(0, nb_el, 1, label="Nombre de réactions élastiques")
    plt.bar(1, nb_inel, 1, label="Nombre de réactions inélastiques")
    plt.bar(2, nb_abs, 1, label="Nombre d'absorptions")
    plt.xlabel("Classes de Réactions")
    plt.ylabel("Nombre d'occurrences")
    plt.title("Histogramme des Réactions")
    plt.legend()
    plt.xticks([])
    plt.show()
    
    
    
    
    
    
    #Dans cette section, on cherche à afficher l'énergie de chaque réac sur un histogramme
    #analyse_reac.energies(reactions)
    
    
    
    
    
    #Dans cette section, on cherche à déterminer le nombre de sous-produit pour tout le fichier
    nb_sous_prod_tot = analyse_reac.nb_sous_prod_tot(reactions)
    print("Il y a au total ", nb_sous_prod_tot, "sous-produits dans ce fichiers.")
   
    """
    #objectif : réaliser un histograme pour "classer" les énergies
    n_bins = 20
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    axs[0].hist(nb_sous_prod_tot, bins=n_bins)
    plt.show()
    """
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   

    
    
