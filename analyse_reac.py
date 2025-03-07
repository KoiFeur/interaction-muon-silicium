import numpy as np
import matplotlib.pyplot as plt


def reactiontype(reactions: list) -> list: 
    "(used to determined what's the reaction's type)"
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


            



