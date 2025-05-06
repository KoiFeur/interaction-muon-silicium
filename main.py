import parser
from colors import bcolors
import matplotlib.pyplot as plt
import analyse_reac
import numpy as np



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
    reactions, code_return = parser.parser(file)
    if code_return == -1:
        print(f"{bcolors.FAIL}Error : reactions returned 1 exit status{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Please read the error above or Debug the file{bcolors.ENDC}")
    """
    Objectif n°1 : Compter le nombre de réactions et le type des réactions 
    (élastiques, inélastiques, absorption).
    """                                                                    #Dans cette section, on récupère et print le nbr de réactions el, inel et abs.
    dic_type_reac, dic_el, dic_inel, dic_abs = analyse_reac.reactiontype(reactions)
    nb_total_reac = [dic_type_reac["Elastic"] + dic_type_reac["Inelastic"] + dic_type_reac["Absorptions"]]
    print("There are", nb_total_reac, "reactions.")
    print("There are", dic_type_reac["Elastic"], "elastic reactions/chocs,", dic_type_reac["Inelastic"], "inelastic reactions/chocs, and", dic_type_reac["Absorptions"], "absorptions.")
    
    
    plt.figure()
    plt.bar(range(len(dic_type_reac.values())), dic_type_reac.values(), 1)
   
    q = range(3)
    for key, value in dic_type_reac.items():
        plt.text(q, value, value)
    plt.text(range(1,len(dic_type_reac.values())+1), dic_type_reac.values(), dic_type_reac.values())
        return code_return
    if code_return == -2:
        print(f"{bcolors.FAIL}Error : reactions return 2 exit status")
        print(f"Wrong file type. Please input a correct file type.{bcolors.ENDC}")
        return code_return
    #Dans cette section, on récupère et print le nbr de réactions el, inel et abs.
    nb_type_reac, dic_el, dic_inel, dic_abs = analyse_reac.reactiontype(reactions)
    nb_el = nb_type_reac["Elastic"]
    nb_inel = nb_type_reac["Inelastic"]
    nb_abs = nb_type_reac["Absorptions"]
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

    print("\n")
    
    tot_nb_sub_prod = analyse_reac.nb_sous_prod_tot(reactions)
    dic_sorted = analyse_reac.nb_sub_product(reactions)
    print("There is a total of", tot_nb_sub_prod, "sub-products created.")
    print("There are", len(dic_sorted), "different kinds of sub-products.")
    print("Here are every types of sub-product and how often they appear :", dic_sorted)
    print("\n")
    new_dic = {}
    for key, value in dic_sorted.items():
        if value > 1000:
            new_dic[key] = value
        else:
            continue
    
    k = 0
    for key, value in new_dic.items():
        plt.bar(k+0.5, value, 1, label=key)
        plt.text(k, value, value)
        k += 1
    plt.yscale('log')
    plt.grid()
    plt.title("Type et quantité de chaque sous-produit")
    plt.xticks([])
    plt.show()
    
    print("Here are the kind and number of each sub-product in elastic reactions :", dic_el)
    print("Here are the kind and number of each sub-product in inelastic reactions :", dic_inel)
    print("Here are the kind and number of each sub-product in absorptions :", dic_abs)
    energie=analyse_reac.lvl_energy(reactions)
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
    return 0




if __name__ == "__main__":
    liste = np.array(["secondaries_1GeV.txt", "secondaries_1MeV.txt", "secondaries_500MeV.txt"])
    #liste = ["testing_limit.txt"]
    for i in liste:
        print(f"Executing file {i}")
        code_return = main(i)
        if code_return != 0:
            print(f"\n\n{bcolors.FAIL} Can't process file correctly, continuing{bcolors.ENDC}")
            continue
        print("file processed correctly")
