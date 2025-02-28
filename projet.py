from tqdm import tqdm

class Vecteur:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Sous_reaction:
    def __init__(self, name: str, energie: float, vec: Vecteur):
        self.name = name
        self.energie = energie
        self.vecteur = vec


class Reaction: 
    
    def __get_reaction_type(self, reaction_equation: list):
        if reaction_equation[0] == "hadElastic":
            return "Elastique"
        clean_eq = [v.split("Si")[0] for v in reaction_equation]
        right = clean_eq[clean_eq.index("-->"):]

        if "" in right:
            return "inelastique"
        else:
            return "absorption"

    def __init__(self, energie : float, vec: Vecteur, sous_reactions: list, reaction_equation: list):
        self.reaction_equation = reaction_equation
        self.vecteur = vec
        self.energie = energie
        self.sous_reactions = sous_reactions
        self.reaction_type = self.__get_reaction_type(self.reaction_equation)
        self.nb_sous_reactifs = len(self.sous_reactions)



def parser(file: str):
    """parse things"""
    liste=[""]
    with open(file, "r") as dft:
        for line in dft: #read file
            if "---" in line:
                liste.append(line) #add each reaction line
            else:
                liste[-1]+=line

        liste = [[[a for a in v.split(" ") if a != ""] for v in i.split("\n") if v != ""] for i in tqdm(liste)][1:] #clean up a little bit

    reactions = []
    for v in liste:
        energie = float(v[1][3])
        in_vec = Vecteur(v[1][0], v[1][1], v[1][2])
        
        sous_reactions = []
        for i in v[2:]:
            sous_reactions.append(Sous_reaction(i[0], float(i[1]), Vecteur(i[2], i[3], i[4])))

        reactions_equation = v[0][2:]
        
        reactions.append(Reaction(energie, in_vec, sous_reactions, reactions_equation))
    return reactions

reactions = parser("data_for_test")

for v in reactions:
    print("reaction :", v.reaction_equation)
    print("reaction type :", v.reaction_type)
    print("vecteur = ", v.vecteur.x, v.vecteur.y, v.vecteur.z)
    print("energie : ", v.energie)
    print("nb_sous_reactifs :", v.nb_sous_reactifs)
    print("\n")
