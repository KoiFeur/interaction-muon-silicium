import matplotlib.pyplot as plt
import numpy as np
import parser
import analyse_reac


#reactions = parser.parser('data_for_test.txt')
reactions, return_code = parser.parser('secondaries_14MeV.txt')



def reactiontype(reactions: list) -> dict: 
    "Used to count how many of each reaction's type there are."
    type_reac = {'Elastique' : 0, 'Inelastique' : 0, 'Absorption' : 0}
    for reaction in reactions:
        for kind, nb in type_reac.items():
            if reaction.reaction_type == kind:
                type_reac[kind] += 1
            else:
                continue
    return type_reac



def secondaries_by_kind(reactions: list) -> list:
    "Used to determine how many of each kind of secondary there are in each kind of reaction"
    dic_sub_in_el = {}
    dic_sub_in_inel = {}
    dic_sub_in_abs = {}
    for reaction in reactions:
        for i in reaction.sub_products:
            if reaction.reaction_type == 'Elastique':
                if i.name not in dic_sub_in_el:
                    dic_sub_in_el[i.name] = 1
                else :
                    dic_sub_in_el[i.name] += 1
            elif reaction.reaction_type == 'Inelastique':
                if i.name not in dic_sub_in_inel:
                    dic_sub_in_inel[i.name] = 1
                else :
                    dic_sub_in_inel[i.name] += 1
            elif reaction.reaction_type == 'Absorption':
                if i.name not in dic_sub_in_abs:
                    dic_sub_in_abs[i.name] = 1
                else :
                    dic_sub_in_abs[i.name] += 1
    return dic_sub_in_el, dic_sub_in_inel, dic_sub_in_abs



def nb_tot_sec(reactions: list) -> int:
    "Used to determine how many reactions there are in the file"
    type_reac = reactiontype(reactions)
    nb_tot_secondaries = type_reac['Elastique'] + type_reac['Inelastique'] + type_reac['Absorption']
    return nb_tot_secondaries



def limit(reactions: list) -> int:
    "Used to determine which limit of occurences do we take for secondaries"
    nb_tot_secondaries = nb_tot_sec(reactions)
    limit = nb_tot_secondaries*0.15
    return limit



def histo_nb_reac(reactions):
    "Used to creat an histogram which represent the number of each kind of reaction"
    colors = ["navy", "orange", "pink", "brown", "gray", "cyan", "magenta", "lime", "teal", "olive", "maroon", "silver", "gold"]
    type_reac = reactiontype(reactions)
    k = 0
    text = 0
    for key, value in type_reac.items():
        text = value
        plt.text(k, value/2, text)
        k += 1
    plt.bar(type_reac.keys(), type_reac.values(), color = colors[:len(colors)])
    plt.xlabel("Type of reaction")
    plt.ylabel("Number of ocurences")
    plt.title("Number of each occurences by type of reaction")
    plt.show()
    
    
    
def nb_sec_by_type_of_sec(reactions: list) -> dict:    #by Oscar
    "Used to determine the number of each kind of sub-product"
    nb_sec = {}
    for reaction in reactions:
        for i in reaction.sub_products:
            if i.name not in nb_sec:
                nb_sec[i.name] = 1
            else:
                nb_sec[i.name] += 1
    nb_sec_sorted = dict(sorted(nb_sec.items(), key=lambda item:item[1]))
    return nb_sec_sorted





def nb_sec_by_type_of_sec_limited(reactions: list) -> dict:
    "Used to apply the limit on the dict nb_sec_sorted"
    limite = limit(reactions)
    nb_sec_sorted_limited = {}
    nb_sec_sorted = nb_sec_by_type_of_sec(reactions)
    for key, value in nb_sec_sorted.items():
        if value >= limite:
            nb_sec_sorted_limited[key] = value
    return nb_sec_sorted_limited



def graph_secondaries(reactions):            #by Oscar
    "Represent the main sub products and their numbers"
    colors = ["navy", "orange", "pink", "brown", "gray", "cyan", "magenta", "lime", "teal", "olive", "maroon", "silver", "gold"]
    nb_sec_sorted_limited = nb_sec_by_type_of_sec_limited(reactions)
    k = 0
    text_value = 0
    for key, value in nb_sec_sorted_limited.items():
        text_value = value
        plt.text(k, value, text_value)
        k += 1
    plt.bar(nb_sec_sorted_limited.keys(), nb_sec_sorted_limited.values(), color = colors[:len(colors)])
    plt.yscale('log')
    plt.grid(True,which="both", linestyle='-', linewidth=0.3)
    plt.title("Types and frequency of each secondaries")
    plt.xlabel("Type of the secondary")
    plt.ylabel("Number of occurences")
    plt.show()
    

            
def graph_secondaries_by_type_of_reac_by_Mistral(reactions):  #!!j'ai utilisé Mistral AI
    "Represents the main secondaries in each kind of reaction"
    colors = ["navy", "orange", "pink", "brown", "gray", "cyan", "magenta", "lime", "teal",
        "dodgerblue", "maroon", "silver", "gold", "indigo", "turquoise", "lavender",
        "beige", "coral", "crimson", "chocolate", "darkorchid", "deeppink", "olive"]
    dic_sub_in_el, dic_sub_in_inel, dic_sub_in_abs = secondaries_by_kind(reactions)
    sec_in_type_reac = [(dic_sub_in_el, 'elastic'), (dic_sub_in_inel, 'inelastic'), 
                        (dic_sub_in_abs, 'absorption')]
    for sec_in, kindreac in sec_in_type_reac:
        plt.bar(sec_in.keys(), sec_in.values(), color = colors[:len(colors)])
        plt.yscale('log')
        k = 0
        text = 0
        for key, value in sec_in.items():
            plt.text(k-0.4, value, value, rotation=45)
            k += 1
        plt.ylabel('Number of occurences')
        plt.xticks(rotation=60)
        plt.title("Type and frequency of each secondaries in " + kindreac + " reactions")
        plt.show()




                

def lvl_energy(reactions: list) -> list:
    "indicate the amount of energy for each sub product"
    limite = limit(reactions)
    energy={}
    energy_limited = {}
    for reaction in reactions:
        for i in reaction.sub_products:
            if i.name not in energy:
                energy[i.name]=[i.energy]
            else:
                energy[i.name].append(i.energy)
    for key, value in energy.items():
        if len(value) >= limite:
            energy_limited[key] = value 
    return energy_limited



def merging_secondaries(reactions: list) -> dict:
    liste_secondaries_to_merge = ['Si', 'Mg', 'Al']
    energy_limited = lvl_energy(reactions)
    for i in liste_secondaries_to_merge:
        energy_limited[i] = []
        for key, value in energy_limited.items():
            if i in key:
                energy_limited[i] = energy_limited[i] + value
    return energy_limited




def histo_energy(reactions):                        #not finished
    "Used to create an histogram with the energy of each kind of secondary by the number of occurences"
    energy_limited = merging_secondaries(reactions)
    bins = np.logspace(-6, 2)
    plt.figure(figsize=[10,5])
    for secondary in energy_limited.keys():
        F, B, _ = plt.hist(energy_limited[secondary], bins, color="white")
        CB = (B[:-1]+B[1:])/2
        plt.grid(True, which='both', linestyle='-', linewidth=0.3)
        plt.xscale('log')
        plt.yscale('log')
        plt.step(CB, F, label=secondary)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Energy (in eV)")
        plt.ylabel("Occurences")
        plt.title('Occurences of each energy by kind of secondary')
        plt.legend()
        plt.grid(True, which='both', linestyle='-', linewidth=0.3)
    plt.show()
    





if return_code == 0:
    """
    histo_nb_reac(reactions)
    graph_secondaries(reactions)
    graph_secondaries_by_type_of_reac_by_Mistral(reactions)

    """
    


    histo_energy(reactions)




















