import parser
import sys
from colors import bcolors


if __name__ == "__main__":
    try:
        reactions = parser.parser("secondaries_500MeV.txt")
    except IndexError:
        print(bcolors.FAIL + "\nPlease put the name of the file here" + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)
    except FileNotFoundError:
        print(bcolors.FAIL + "Couldn't find the file, you may had misspelled it." + bcolors.ENDC)
        print(bcolors.FAIL + "python3 main.py [file to analyse]\n" + bcolors.ENDC)

    print(len(reactions))

    for i in range(len(reactions[:20])):
        print('Réaction numéro', i+1)
        print('Vecteur de la réaction :')
        print('   Coordonnées x du vecteur:', reactions[i].vecteur.x)
        print('   Coordonnées y du vecteur:', reactions[i].vecteur.y)
        print('   Coordonnées z du vecteur:', reactions[i].vecteur.z)
        print('Nombre de sous-produits de la réaction :', reactions[i].nb_sous_reactifs)
        print('\n')
