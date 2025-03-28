import numpy as np


def reactiontype(reactions: list) -> list: 
    "Used to determined what's the reaction's type."
    nb_el = 0
    nb_inel = 0
    nb_abs = 0
    for reaction in reactions:
        if reaction.reaction_type == "Elastique":
            nb_el += 1
        elif reaction.reaction_type == "Inelastique":
            nb_inel += 1
        elif reaction.reaction_type == "Absorption":
            nb_abs += 1
    return [nb_el, nb_inel, nb_abs]
    
    
    
    
def nb_sous_prod_tot(reactions: list) -> int:
    "Used to determine the number of sub-products in the entire file"
    nb_sous_prod_tot = 0
    for reaction in reactions:
        nb_sous_prod_tot += reaction.nb_sous_reactifs
    return nb_sous_prod_tot




def nb_sub_product(reactions: list) -> int:
    "Used to determine the number of each kind of sub-product"
    dic = {}
    for reaction in reactions:
        for i in reaction.sous_reactions:
            if i.name not in dic:
                dic[i.name] = 1
            else:
                dic[i.name] += 1
    dic_sorted = dict(sorted(dic.items(), key=lambda item:item[1]))
    return dic_sorted



def lvl_energie(reactions: list) -> list:
    "indicate the amount of energy for each sub product"
    energie={}
    
    for reaction in reactions:
        for i in reaction.sous_reactions:
            if i.name not in energie:
                energie[i.name]=[i.energie]
            else:
                energie[i.name].append(i.energie)
    return energie            
    
    










































            
       
