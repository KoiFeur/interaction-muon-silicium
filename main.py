import parser
import sys
from colors import bcolors
import pandas as pd
import matplotlib.pyplot as plt
import analyse_reac


if __name__ == "__main__":
    try:
        reactions = parser.parser("testing_limit.txt")
    except IndexError:
        print(bcolors.FAIL + "\nPlease put the name of the file here" + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)
    except FileNotFoundError:
        print(bcolors.FAIL + "Couldn't find the file, you may had misspelled it." + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)


    zdhrvb = analyse_reac.reactiontype(reactions)
    print(zdhrvb)

