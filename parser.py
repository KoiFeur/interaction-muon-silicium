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

    energie : float
        sub product energy

    vecteur : Vecteur
        directionnal vector of the particule

    """
    def __init__(self, name: str, energie: float, vec: Vecteur):
        self.name: str = name
        self.energie: float = energie
        self.vecteur: Vecteur = vec

class Reaction: 
    """"
    Reaction struct

    Parameters:

    reaction_equation: list[str]
        List of each term that compose a reaction ["neutron", "+", "Si28", "-->", .. ]
    
    vecteur: Vecteur
        in Vector

    energie: float
        energie of the neutron

    sous_reactions : ndarray[Sub_product]
        list of the reaction Sub_product

    nb_sous_reactifs : int
        sub product number 
    """
    def __get_reac(self, reaction_equation: list) -> list[str]: 
        return [i for i in reaction_equation[:reaction_equation.index("-->")] if (i != "neutronInelastic" and i!="hadElastic" and i!= "+")]
    
    def __get_subproducts_name(self) -> list[str]:
        return [i.name for i in self.sous_reactions]


    def __get_reaction_type(self, reaction_equation: list) -> str:
        if reaction_equation[0] == "hadElastic":
            return "Elastique"
        else:
            #aloo
            reac = self.__get_reac(reaction_equation)
            sub_product = self.__get_subproducts_name()
            #print(product, self.__get_subproducts_name(), "gamma" in self.__get_subproducts_name())
            if reac[0] in sub_product and reac[1] in sub_product and len(set(sub_product)) == 3:
                print(reac, set(sub_product))
                #print("oui")
                return "Inelastique"
            return "Absorption"


    def __init__(self, energie : float, vec: Vecteur, sous_reactions: list, reaction_equation: list):
        self.reaction_equation: list[str] = reaction_equation
        self.vecteur: Vecteur = vec
        self.energie: float = energie
        self.sous_reactions: np.ndarray = np.array(sous_reactions)
        self.reaction_type: str = self.__get_reaction_type(self.reaction_equation)
        self.nb_sous_reactifs: int = len(self.sous_reactions)

def parser(file: str) -> np.ndarray:
    """parse things"""

    print("\nReading file\n")
    liste=[""] #else there is out of range error due tu the liste[-1]+=line line
    with open(file, "r") as dft:
        for line in tqdm(dft): #read file
            if "[" in line:
                line = line.split("[")[0] + line.split("]")[1]
            if "---" in line:
                liste.append(line) #add each reaction line
            else:
                liste[-1]+=line        
        #print("\nClean up : \n")
        #liste = [[[a for a in v.split(" ") if a != ""] for v in i.split("\n") if v != ""] for i in tqdm(liste)][1:] #clean up a little bit. 
                                                                                                                    #The [1:] delete the element added for the code to not crash
        #it's not necessary

    print("\n\nObject list creation : \n")

    reactions = []
    for i in tqdm(liste[1:]):
        v = [[a for a in j.split(" ") if a != ""] for j in i.split("\n") if j != ""]

        energie = float(v[1][3])
        in_vec = Vecteur(v[1][0], v[1][1], v[1][2])
        
        sous_reactions = []
        for i in v[2:]:
            sous_reactions.append(Sub_product(i[0], float(i[1]), Vecteur(i[2], i[3], i[4])))
        reactions_equation = v[0][2:]
        
        reactions.append(Reaction(energie, in_vec, sous_reactions, reactions_equation))
    print("\n")
    #return reactions
    return np.array(reactions)
