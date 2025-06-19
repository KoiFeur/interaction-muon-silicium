from colors import bcolors
from tqdm import tqdm
import numpy as np
import re
import sys
np.set_printoptions(threshold=sys.maxsize)

class Fichier:
    def __str__(self):
        return self.name
    
    def __reactions_types(self, content: list):
        temp = [i.reaction_type for i in content]
        temp = sorted(temp)
        temp_set = sorted(list(set(temp)))
        try:
            for i in range(1, len(temp_set)):
                self.reactions_types[temp[temp.index(temp_set[i-1])]] = temp.index(temp_set[i]) - temp.index(temp_set[i-1])
        except IndexError:
            self.reactions_types[temp[0]] = len(temp)
        except KeyboardInterrupt:
            quit()
        finally:
            self.reactions_types[temp[-1]] = len(temp) - temp.index(temp_set[-1])
            del(temp, temp_set)
    
    def limit(self, content: list):
        "Used to determine which limit of occurences do we take for secondaries"
        nb_tot_secondaries = self.nb_tot_secondaries
        limit = nb_tot_secondaries*0.15
        return limit
    
    
    def __nb_tot_sec(self, content: list):
        "Used to determine how many secondaries there are in the file"
        nb_sec_sorted = self.nb_sec_sorted
        nb_tot_secondaries = 0
        for key, value in nb_sec_sorted.items():
            nb_tot_secondaries += value
        self.nb_tot_secondaries = nb_tot_secondaries
        
    
    def __secondaries_by_kind(self, content: list):
        "Used to determine how many of each kind of secondary there are in each kind of reaction"
        self.products_kind_type = {i : {} for i in self.reactions_types.keys()}
        for reaction in content:
            for keys in self.reactions_types.keys():
                for i in reaction.sub_products:
                    if reaction.reaction_type == keys:
                        if i.name not in self.products_kind_type[keys].keys():
                            self.products_kind_type[keys][i.name] = 1
                        else:
                            self.products_kind_type[keys][i.name] += 1
    
    def __nb_sec_by_type_of_sec(self, content: list) -> dict:
        "Used to determine the number of each kind of sub-product"
        nb_sec = {}
        for reaction in content:
            for i in reaction.sub_products:
                if i.name not in nb_sec:
                    nb_sec[i.name] = 1
                else:
                    nb_sec[i.name] += 1
        self.nb_sec_sorted = dict(sorted(nb_sec.items(), key=lambda item:item[1]))
    

    def __galette(self, content):
        return np.array([[i.vecteur.x, i.vecteur.y, i.vecteur.z] for i in content])


    def __nb_sec_by_type_of_sec_limited(self, content: list) -> dict:
        "Used to apply the limit on the dict nb_sec_sorted"
        limite = self.limit
        self.nb_sec_sorted_limited = {}
        nb_sec_sorted = self.nb_sec_sorted
        for key, value in nb_sec_sorted.items():
            if value >= limite:
                self.nb_sec_sorted_limited[key] = value
        
    def __lvl_energy(self, content: list) -> list:
        "indicate the amount of energy for each sub product"
        limite = self.limit(content)
        energy = {}
        energy_limited = {}
        for reaction in content:
            for i in reaction.sub_products:
                if i.name not in energy:
                    energy[i.name]=[i.energy]
                else:
                    energy[i.name].append(i.energy)
        for key, value in energy.items():
            if len(value) >= limite:
                energy_limited[key] = value
        self.energy_limited = energy_limited
        del(limite, energy, energy_limited)

    
    def __extremum_of_energy(self, content: list) -> list:
        "Used to create a list with all of the energies of the secondaries in the file"
        energy_limited = self.energy_limited
        all_the_energy = []
        for energies in energy_limited.values():
            for value in energies:
                all_the_energy.append(value)
        self.en_minimum = min(i for i in all_the_energy)
        self.en_maximum = max(i for i in all_the_energy)
    
    def __init__(self, name, content: np.ndarray, energy):
        #attribut : 
        self.energy: int = energy
        self.name: str = name
        self.content: np.ndarray = content[:30]
        self.nb_tot_secondaries: int = 0
        self.reactions_types: dict = {}
        self.nb_sec_sorted: dict = {}
        self.nb_sec_sorted_limited: dict = {}
        self.energy_limited: dict = {}
        self.products_kind_type: dict = {}
        self.galette: np.ndarray = self.__galette(content)
        #self.energy_limited_merged:dict = {}
        self.en_minimum: int = 0
        self.en_maximum: int = 0
        
        #appel des méthodes : 
        self.__reactions_types(content)
        self.__lvl_energy(content)
        #self.__merging_secondaries(content)
        self.__extremum_of_energy(content)
        self.__secondaries_by_kind(content)
        self.__nb_sec_by_type_of_sec(content)
        self.__nb_tot_sec(content)

class Vecteur:
    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def get_norm(self):
        return np.sqrt((self.x + self.y + self.z) ** 2)

    def __init__(self, x, y, z):
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

class Sub_product:
    def __init__(self, name: str, energy: float, vec):
        self.name: str = name
        self.energy: float = energy
        self.vecteur: np.ndarray = vec

class Reaction: 
    def __get_reac(self) -> list: 
        return [i for i in self.eq_reac[1:self.eq_reac.index('-->')] if i != "+"]
    
    def __get_subproducts_name(self) -> list:
        return [i.name for i in self.sub_products]

    def __get_reaction_type(self) -> int:
        if self.eq_reac[0] == "hadElastic":
            self.reaction_type = "Elastic"
            return 0
        else:
            reac = self.__get_reac()
            sub_product = self.__get_subproducts_name()
            if reac[0] in sub_product and reac[1] in sub_product and len(set(sub_product)) == 3:
                self.reaction_type = "Inelastic"
                return 0
            self.reaction_type = "Absorption"
            return 0

    def __init__(self, vec: Vecteur, sub_products: list, eq_reac: list):
        # Attributs
        self.eq_reac: list[str] = eq_reac
        self.vecteur: Vecteur = vec
        self.sub_products: np.ndarray = np.array(sub_products)
        self.nb_sous_reactifs: int = len(self.sub_products)
        self.reaction_type: str = ""

        # Appel des méthodes
        self.__get_reaction_type()

def open_multiple_files(liste: list) -> list:
    files = []
    for i in tqdm(liste):
        reaction, energy, return_code = parser(i)
        if return_code != 0:
            print(f"{bcolors.FAIL} File {i} didn't process correctly {bcolors.ENDC}")
        else:
            files.append(Fichier(i, reaction, energy))
            del(reaction)
    files = [(int(i.energy), i) for i in files]
    files = np.array(sorted(files)).T
    return files[1]

def parser(file: str) -> tuple[np.ndarray, int, int]:
    """parse things"""
    liste=[""] #else there is out of range error due tu the liste[-1]+=line
    try:
        f = open(file, "r")
        data = f.read()
        f.close()
        if re.search(r"[^ -~\n]", data) != None:
            print(f"\n{bcolors.FAIL}Non ASCII character detected {bcolors.ENDC}")
            return (np.array(liste),0, -2)
        data = data.split('\n')
    except FileNotFoundError:
        print(f"{bcolors.FAIL}{file} : No such a directory file{bcolors.ENDC}")
        return (np.array(liste),0, -1)
    except:
        print(f"{bcolors.FAIL}Can't open file{bcolors.ENDC}")
        return (np.array(liste),0, -1)

    for line in data: #read file
        line += "\n" #weird but the progress bar
        if "[" in line:
            line = line.split("[")[0] + line.split("]")[1]
        if "---" in line:
            liste.append(line) #add each reaction line
        else:
            liste[-1]+=line
        
    del(data)
    if len(liste) == 1 :
        print("File contain one or less reaction")
        return (np.array(liste),0, -2)

    reactions = []

    energy = liste[1].split("\n")[1].split(" ")[6]

    for i in liste[1:]:
        v = [[a for a in j.split(" ") if a != ""] for j in i.split("\n") if j != ""]
        
        in_vec = Vecteur(v[1][0], v[1][1], v[1][2])

        eq_reac = v[0][2:]
        eq_reac = eq_reac[:-1]
        sub_products = [Sub_product(i[0], float(i[1]), np.array([i[2], i[3], i[4]])) for i in v[2:]]
        reactions.append(Reaction(in_vec, sub_products, eq_reac))

    del(liste)
 
    return np.array(reactions), int(energy), 0
