import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

liste=[""]
with open("data_for_test", "r") as dft:
    nbr_reaction = 0
    for line in dft:
        if "---" in line:
            liste.append(line)
            nbr_reaction+=1
            print(line)
        else:
            liste[-1]+=line
    print(liste)
