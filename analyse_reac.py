import numpy as np


def reactiontype(reactions: list) -> list: 
    "Used to determined what's the reaction's type."
    nb_el = 0
    nb_inel = 0
    nb_abs = 0
    dic_el = {}
    dic_inel = {}
    dic_abs = {}
    for reaction in reactions:
        if reaction.reaction_type == "Elastique":
            nb_el += 1
            for i in reaction.sub_products:
                if i.name not in dic_el:
                    dic_el[i.name] = 1
                else:
                    dic_el[i.name] += 1
        elif reaction.reaction_type == "Inelastique":
            nb_inel += 1
            for i in reaction.sub_products:
                if i.name not in dic_inel:
                    dic_inel[i.name] = 1
                else:
                    dic_inel[i.name] += 1
        elif reaction.reaction_type == "Absorption":
            nb_abs += 1
            for i in reaction.sub_products:
                if i.name not in dic_abs:
                    dic_abs[i.name] = 1
                else:
                    dic_abs[i.name] += 1
    dic_type_reac = {"Elastic":nb_el, "Inelastic":nb_inel, "Absorptions":nb_abs}
    return dic_type_reac, dic_el, dic_inel, dic_abs
    
    
    
    
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
        for i in reaction.sub_products:
            if i.name not in dic:
                dic[i.name] = 1
            else:
                dic[i.name] += 1
    dic_sorted = dict(sorted(dic.items(), key=lambda item:item[1]))
    return dic_sorted



def lvl_energy(reactions: dict) -> dict:
    "indicate the amount of energy for each sub product"
    energy={}
    
    for reaction in reactions:
        for i in reaction.sub_products:
            if i.name not in energy:
                energy[i.name]=[i.energy]
            else:
                energy[i.name].append(i.energy)
    return energy            
    
    










































            
       
