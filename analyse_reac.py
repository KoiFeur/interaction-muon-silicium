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
    "Used to determine the nimber of sub-products in the entire file"
    nb_sous_prod_tot = 0
    for reaction in reactions:
        nb_sous_prod_tot += reaction.nb_sous_reactifs
    return nb_sous_prod_tot


def nbr_gamma(reactions: list) -> int:
    "Used to determine how many gamma ray are in the file"
    nb_gamma = 0
    for sub_product in reactions:
        if sub_product.name == "gamma":
            nb_gamma =+ 1
    return nb_gamma
            
       
