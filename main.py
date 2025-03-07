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

    """
    La variable `reactions` est une liste d'objet.
    Pour accéder aux différents objets, on note reactions[i] avec i de 0 à (len(reactions) - 1)
    len(reactions) retourne le nombre d'éléments de la liste.

    Les objets ici sont des objets de type `Reaction` et possèdes plusieurs arguments listés dans le fichier `parser.py` à la ligne 55 (en gros sous le __init__)

    Pour accéder à un argument de l'objet, on note nom_objet.arguments

    Par exemple, admettons que l'on veuille afficher l'énergie mise en jeu lors la première reaction.

    Nous marquons donc `reactions[0].energie`

    Cette ligne nous retourne l'énergie de la première reaction.

    
    Dans les exercices suivants, l'affichage doit être un minimum propre et aérée.

    Exercice 1 : Nous voulons afficher, pour chacune des reactions, l'énergie mise en jeu et le type de reaction qui a eu lieu.
                (aide, on utilisera une boucle for pour le faire).
                Chat GPT et l'utilisation de toute autre ia est interdite, en plus de ne rien apprendre elle vole le code.
                par contre on pourra utiliser internet pour chercher différents moyen de le faire.
    
    Exercice 2 : On veut affichier les coordonnées du vecteur incident de chacune des réactions.
                (on pourra reprendre en partie le code de l'exercice 1)
    
    Exercice 3 : Attention, plus dur ! On veut afficher le vecteur et le nom de chacun des sous produits de chacune des réactions.

    """
    print(len(reactions))
    #Exercice 1
    """
    for i in range(len(reactions)):
        print('this reaction has an energy of',reactions[i].energie)
        print('The type of this reaction is ',reactions[i].reaction_type, '\n')
    """
    """
    Exercice 1 validé par le professeur
    """
    """
    #Exercice 2
    for i in range(len(reactions)):
        print('Réaction numéro', i+1)
        print('Coordonnées x du vecteur:', reactions[i].vecteur.x)
        print('Coordonnées y du vecteur:', reactions[i].vecteur.y)
        print('Coordonnées z du vecteur:', reactions[i].vecteur.z, '\n')
    """
    """
    Exercice 2 validé par le professeur
    """
    
    # #Exercice 3
    for i in range(len(reactions[:20])):
        print('Réaction numéro', i+1)
        print('Vecteur de la réaction :')
        print('   Coordonnées x du vecteur:', reactions[i].vecteur.x)
        print('   Coordonnées y du vecteur:', reactions[i].vecteur.y)
        print('   Coordonnées z du vecteur:', reactions[i].vecteur.z)
        print('Nombre de sous-produits de la réaction :', reactions[i].nb_sous_reactifs)
        print('\n')
