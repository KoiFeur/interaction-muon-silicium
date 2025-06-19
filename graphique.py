from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import pygame

def vectors(reactions):
    return np.array([np.array([i.vecteur.x, i.vecteur.y, i.vecteur.z]) for i in tqdm(reactions[:1000])]).T





def run(reactions):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim3d([-1,1])
    ax.set_ylim3d([-1,1])
    ax.set_zlim3d([-1,1])
    i = np.array(i.galette)
    ax.scatter(i[0], i[1], i[2])
    plt.savefig(f"figures/figure{reactions[0].eq_reac}.png")
