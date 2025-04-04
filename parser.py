from tqdm import tqdm
import numpy as np

class Vecteur:
    """
    Just a Vector

    Parameters:

    x: float
        x compenent

    y: float
        y compenent

    z: float
        z compenent
    """
    def __init__(self, x, y, z):
        self.x: float = x
        self.y: float = y
        self.z: float = z

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
            #aloo
            reac = self.__get_reac(eq_reac)
            sub_product = self.__get_subproducts_name()
            #print(product, self.__get_subproducts_name(), "gamma" in self.__get_subproducts_name())
            #print(reac, set(sub_product))
            if reac[0] in sub_product and reac[1] in sub_product and len(set(sub_product)) == 3:
                                #print("oui")
                return "Inelastique"
            """
            if reac[0] in sub_product and reac[1] in sub_product and len(set(sub_product)) == 2:
                print(reac, sub_product)
                print(self.energy, self.reac_number, self.num_line)
                for i in self.sub_products:
                    print(i.name, i.energy)
"""
            #print(reac, sub_product)
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
        



def parser(file: str) -> np.ndarray:
    """parse things"""

    print("\nReading file\n")
    liste=[""] #else there is out of range error due tu the liste[-1]+=line line
    try:
        data = open(file, "r").read().split("\n")
    except:
        print("can't open the file")
        return 1

    for id in tqdm(range(len(data))): #read file
        line = data[id] + "\n" #weird but the progress bar
        if "[" in line:
            line = line.split("[")[0] + line.split("]")[1]
        if "---" in line:
            liste.append(line[:-2] + f" {id + 1}\n") #add each reaction line
        else:
            liste[-1]+=line        
        #print("\nClean up : \n")
        #liste = [[[a for a in v.split(" ") if a != ""] for v in i.split("\n") if v != ""] for i in tqdm(liste)][1:] #clean up a little bit. 
                                                                                                                    #The [1:] delete the element added for the code to not crash
        #it's not necessary

    print("\nObject list creation :")
    
    reactions = []
    for id in tqdm(range(1, len(liste))):
        i = liste[id] # I know this is weird and useless but it's like that to keep the beautiful progress bar
        v = [[a for a in j.split(" ") if a != ""] for j in i.split("\n") if j != ""] #split

        energy = float(v[1][3])
        in_vec = Vecteur(v[1][0], v[1][1], v[1][2])
        
        sub_products = []
        eq_reac = v[0][2:]
        num_line = int(eq_reac[-1])
        eq_reac = eq_reac[:-1]
        try:
            for i in v[2:]:
                sub_products.append(Sub_product(i[0], float(i[1]), Vecteur(i[2], i[3], i[4])))
        except:
            print(num_line)
        
        
        reactions.append(Reaction(energy, in_vec, sub_products, eq_reac, id, num_line))
    print("\n")
    #return reactions
    return np.array(reactions)
