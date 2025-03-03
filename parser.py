from tqdm import tqdm

class Vecteur:
    """
    Just a Vector

    Parameters:

    x: float
        x copenent

    y: float
        y copenent

    z: float
        z copenent
    """
    def __init__(self, x, y, z):
        self.x: float = x
        self.y: float = y
        self.z: float = z

class Sub_product:
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
    """
    
    def __get_reaction_type(self, reaction_equation: list) -> str:
        if reaction_equation[0] == "hadElastic":
            return "Elastique"
        clean_eq = [v.split("Si")[0] for v in reaction_equation]
        right = clean_eq[clean_eq.index("-->"):]
        if "" in right:
            return "inelastique"
        else:
            return "absorption"

    def __init__(self, energie : float, vec: Vecteur, sous_reactions: list, reaction_equation: list):
        self.reaction_equation: list[str] = reaction_equation
        self.vecteur: Vecteur = vec
        self.energie: float = energie
        self.sous_reactions: list[Sub_product] = sous_reactions
        self.reaction_type: str = self.__get_reaction_type(self.reaction_equation)
        self.nb_sous_reactifs: int = len(self.sous_reactions)

def parser(file: str) -> list:
    """parse things"""

    print("\nReading file\n")
    liste=[""] #else there is out of range error due tu the liste[-1]+=line line
    with open(file, "r") as dft:
        for line in tqdm(dft): #read file
            if "---" in line:
                liste.append(line) #add each reaction line
            else:
                liste[-1]+=line
        print("\nClean up : \n")
        liste = [[[a for a in v.split(" ") if a != ""] for v in i.split("\n") if v != ""] for i in tqdm(liste)][1:] #clean up a little bit. 
                                                                                                                    #The [1:] delete the element added for the code to not crash

    print("\n\nObject list creation : \n")

    reactions = []
    for v in tqdm(liste):
        energie = float(v[1][3])
        in_vec = Vecteur(v[1][0], v[1][1], v[1][2])
        
        sous_reactions = []
        for i in v[2:]:
            sous_reactions.append(Sub_product(i[0], float(i[1]), Vecteur(i[2], i[3], i[4])))

        reactions_equation = v[0][2:]
        
        reactions.append(Reaction(energie, in_vec, sous_reactions, reactions_equation))
    print("\n")
    return reactions

