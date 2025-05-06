import time
from colors import bcolors
from tqdm import tqdm
import numpy as np
import re
import traceback

class Vecteur:
    """
    Just a Vector

    Parameters:

    x: float
        x component 

    y: float
        y component

    z: float
        z component
    """
    def get_norm(self):
        return np.sqrt((self.x + self.y + self.z) ** 2)

    def __init__(self, x, y, z):
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

class Sub_product:
    """
    Sub_product struct

    Parameters: 

    name : str
        sub product name

    energy : float
        sub product energy

    vecteur : Vecteur
        directionnal vector of the particule

    """
    def __init__(self, name: str, energy: float, vec: Vecteur):
        self.name: str = name
        self.energy: float = energy
        self.vecteur: Vecteur = vec

class Reaction: 
    """"
    Reaction struct

    Parameters:

    eq_reac: list[str]
        List of each term that compose a reaction ["neutron", "+", "Si28", "-->", .. ]
    
    vecteur: Vecteur
        in Vector

    energy: float
        energy of the neutron

    sub_products : ndarray[Sub_product]
        list of the reaction Sub_product

    nb_sous_reactifs : int
        sub product number 
    """
    def __get_reac(self, eq_reac: list) -> list: 
        return [i for i in eq_reac[1:eq_reac.index('-->')] if i != "+"]
    
    def __get_subproducts_name(self) -> list:
        return [i.name for i in self.sub_products]

    def __get_reaction_type(self, eq_reac: list) -> str:
        if eq_reac[0] == "hadElastic":
            return "Elastique"
        else:
            reac = self.__get_reac(eq_reac)
            sub_product = self.__get_subproducts_name()
            if reac[0] in sub_product and reac[1] in sub_product and len(set(sub_product)) == 3:
                return "Inelastique"
            return "Absorption"

    def __init__(self, energy : float, vec: Vecteur, sub_products: list, eq_reac: list, reac_number: int, num_line: int):
        self.reac_number: int = reac_number
        self.num_line: int = num_line
        self.eq_reac: list[str] = eq_reac
        self.vecteur: Vecteur = vec
        self.energy: float = energy
        self.sub_products: np.ndarray = np.array(sub_products)
        self.reaction_type: str = self.__get_reaction_type(self.eq_reac)
        self.nb_sous_reactifs: int = len(self.sub_products)

def parser(file: str) -> tuple[np.ndarray, int]:
    """parse things"""
    print("\n Openning file : \n")
    liste=[""] #else there is out of range error due tu the liste[-1]+=line line
    start = time.time_ns()
    try:
        f = open(file, "r")
        data = f.read()
        f.close()
        if re.search(r"[^ -~\n]", data) != None:
            print(f"\n{bcolors.FAIL}Non ASCII character detected {bcolors.ENDC}")
            return (np.array(liste), -2)
        data = data.split('\n')
    except FileNotFoundError:
        print(f"{bcolors.FAIL}{file} : No such a directory file{bcolors.ENDC}")
        return (np.array(liste), -1)
    except:
        print(f"{bcolors.FAIL}Can't open file{bcolors.ENDC}")
        return (np.array(liste), -1)
    stop = time.time_ns()

    print(f"File read in {stop - start} ns ({round((stop - start) * 1e-9, 2)} s)")
    
    print("\n Reading file : \n")

    for i in tqdm(range(len(data))): #read file
        line = data[i] + "\n" #weird but the progress bar
        if "[" in line:
            line = line.split("[")[0] + line.split("]")[1]
        if "---" in line:
            liste.append(line[:-2] + f" {i + 1}\n") #add each reaction line
        else:
            liste[-1]+=line     
        
    if len(liste) == 1 :
        print("File contain one or less reaction")
        return (np.array(liste), -2)

    print("\nObject list creation :")
    
    reactions = []
    for id in tqdm(range(1, len(liste))):
        i = liste[id] # I know this is weird and useless but it's to keep the beautiful progress bar
        v = [[a for a in j.split(" ") if a != ""] for j in i.split("\n") if j != ""] #split
        
        try:
            energy = float(v[1][3])
            in_vec = Vecteur(v[1][0], v[1][1], v[1][2])
        
            sub_products = []
            eq_reac = v[0][2:]
            num_line = int(eq_reac[-1])
            eq_reac = eq_reac[:-1]
            for i in v[2:]:
                sub_products.append(Sub_product(i[0], float(i[1]), Vecteur(i[2], i[3], i[4])))
        except IndexError:
            print(f"{bcolors.FAIL}Can't parse the {id}th reaction. Something is missing.{bcolors.ENDC}")
            return (np.array(reactions), -2)
        except ValueError:
            print(f"{bcolors.FAIL}Can't parse the {id}th reaction. Can't convert things into float.{bcolors.ENDC}")
            return (np.array(reactions), -2)
        
        reactions.append(Reaction(energy, in_vec, sub_products, eq_reac, id, num_line))
    print("\n")
    return np.array(reactions), 0
