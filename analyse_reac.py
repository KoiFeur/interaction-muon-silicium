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


def nb_sub_product(reactions: list) -> int:
    """
    dic = {
        "nb_gammas":0, 
        "nb_neutrons":0,
        "nb_deuterons":0,
        "nb"
        }
    """
    nb_gammas = 0
    nb_neutrons = 0
    nb_deuterons = 0
    nb_tritons = 0
    nb_protons = 0
    for reaction in reactions:
        for i in reaction.sous_reactions:
            if i.name == "gamma":
                nb_gammas += 1
            if i.name == "neutron":
                nb_neutrons += 1
            if i.name == "deuteron":
                nb_deuterons += 1
            if i.name == "triton":
                nb_tritons += 1
            if i.name == "proton":
                nb_protons += 1
    return nb_gammas, nb_neutrons, nb_deuterons, nb_tritons, nb_protons
            













































            
       
