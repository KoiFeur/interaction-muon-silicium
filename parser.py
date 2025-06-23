from os import walk
from colors import bcolors
from tqdm import tqdm
import numpy as np
import re
import sys
from manim import *
np.set_printoptions(threshold=sys.maxsize)

AMU = 931.5 # MeV/c**2

ATOMS = {
    "gamma" : {"mass" : 0, "color" : ManimColor.from_hex("#FF00FF"), "radius" : 0.1},
    "e-" : {"mass" : 0.51099895069, "color" : GOLD_E, "radius" : 0.1},
    "omega-" : {"mass" : 1672.45, "color" : GREY_B , "radius" : 0.1},
    "xi-" : {"mass" : 1314.86, "color" : ORANGE, "radius" : 0.1},
    "xi0" : {"mass" : 1321.71, "color" : ORANGE, "radius" : 0.1},
    "pi-" : {"mass" : 139.57018, "color" : YELLOW, "radius" : 0.1},
    "pi+" : {"mass" : 139.57018, "color" : YELLOW, "radius" : 0.1},
    "pi0" : {"mass" : 134.9766, "color" : YELLOW, "radius" : 0.1},
    "kaon0S" : {"mass" : 497.611, "color" : GOLD_A, "radius" : 0.1},
    "kaon0L" : {"mass" : 497.611, "color" : GOLD_A, "radius" : 0.1},
    "kaon+" : {"mass" : 493.677, "color" : GOLD_A, "radius" : 0.1},
    "kaon-" : {"mass" : 493.677, "color" : GOLD_A, "radius" : 0.1},
    "sigma+" : {"mass" : 1189.37, "color" : BLUE_A, "radius" : 0.1},
    "sigma-" : {"mass" : 1197.449, "color" : BLUE_A, "radius" : 0.1},
    "sigma0" : {"mass" : 1192.642, "color" : BLUE_A, "radius" : 0.1},
    "eta" : {"mass" : 547.862, "color" : GREEN_E, "radius" : 0.1},
    "eta_prime" : {"mass" : 957.78, "color" : GREEN_D, "radius" : 0.1},
    "lambda" : {"mass" : 1115.683, "color" : LIGHT_BROWN, "radius" : 0.1},
    "neutron" : {"mass" : 939.565422, "color" : GREEN, "radius" : 0.2},
    "proton" : {"mass" : 938.272089, "color" : WHITE, "radius" : 0.2},
    "deuteron" : {"mass" : 2.01410177812 * AMU, "color" : WHITE, "radius" : 0.2},
    "triton" : {"mass" : 3.0160492779 * AMU, "color" : WHITE, "radius" : 0.2},
    "H4" : {"mass" : 4.02643 * AMU, "color" : GREY_B, "radius" : 0.2},
    "H5" : {"mass" : 5.03531 * AMU, "color" : GREY_B, "radius" : 0.2},
    "H6" : {"mass" : 6.04496 * AMU, "color" : GREY_B, "radius" : 0.2},
    "H7" : {"mass" : 7.052750 * AMU, "color" : GREY_B, "radius" : 0.2},
    "alpha": {"mass" : 3.726379e3, "color" : BLUE_B, "radius" : 0.3},
    "He3" : {"mass" : 3.0160293201 * AMU, "color" : TEAL, "radius" : 0.3},
    "He4" : {"mass" : 4.00260325413 * AMU, "color" : TEAL, "radius" : 0.3},
    "He5" : {"mass" : 5.012057 * AMU, "color" : TEAL, "radius" : 0.3},
    "He6" : {"mass" : 6.0188891 * AMU, "color" : TEAL, "radius" : 0.3},
    "He7" : {"mass" : 7.028021 * AMU, "color" : TEAL, "radius" : 0.3},
    "He8" : {"mass" : 8.033922 * AMU, "color" : TEAL, "radius" : 0.3},
    "He9" : {"mass" : 9.043946 * AMU, "color" : TEAL, "radius" : 0.3},
    "He10" : {"mass" : 10.05281531 * AMU, "color" : TEAL, "radius" : 0.3},
    "Li4" : {"mass" : 4.02719 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li5" : {"mass" : 5.01254 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li6" : {"mass" : 6.0151228874 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li7" : {"mass" : 7.0160034366 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li8" : {"mass" : 8.02248736 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li9" : {"mass" : 9.0267895 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li10" : {"mass" : 10.035483 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Li11" : {"mass" : 11.0437236 * AMU, "color" : YELLOW_E, "radius" : 0.3},
    "Be6" : {"mass" : 6.019726 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be7" : {"mass" : 7.01692983 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be8" : {"mass" : 8.00530510 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be9" : {"mass" : 9.012183065 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be10" : {"mass" : 10.0135338 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be11" : {"mass" : 11.021658 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be12" : {"mass" : 12.026921 * AMU, "color" : PURPLE, "radius" : 0.3},
    "Be13" : {"mass" : 13.036135 * AMU, "color" : PURPLE, "radius" : 0.3},
    "B7" : {"mass" : 8.0246073 * AMU, "color" : MAROON_E, "radius" : 0.3},
    "B8" : {"mass" : 8.0246072 * AMU, "color" : MAROON_E, "radius" : 0.3},
    "B9" : {"mass" : 9.0133288 * AMU, "color" : MAROON_E, "radius" : 0.3},
    "B10" : {"mass" : 10.01293695 * AMU, "color" : MAROON_E, "radius" : 0.4},
    "B11" : {"mass" : 11.00930536 * AMU, "color" : MAROON_E, "radius" : 0.4},
    "B12" : {"mass" : 12.0143521 * AMU, "color" : MAROON_E, "radius" : 0.4},
    "B13" : {"mass" : 13.0177802 * AMU, "color" : MAROON_E, "radius" : 0.4},
    "B14" : {"mass" : 14.025404 * AMU, "color" : MAROON_E, "radius" : 0.4},
    "C8" : {"mass" : 8.037643 * AMU, "color" : BLACK, "radius" : 0.4},
    "C9" : {"mass" : 9.0310372 * AMU, "color" : BLACK, "radius" : 0.4},
    "C10" : {"mass" : 10.0168532 * AMU, "color" : BLACK, "radius" : 0.4},
    "C11" : {"mass" : 11.0114336 * AMU, "color" : BLACK, "radius" : 0.4},
    "C12" : {"mass" : 12 * AMU, "color" : BLACK, "radius" : 0.4},
    "C13" : {"mass" : 13.00335483507 * AMU, "color" : BLACK, "radius" : 0.4},
    "C14" : {"mass" : 14.0032419884 * AMU, "color" : BLACK, "radius" : 0.4},
    "C15" : {"mass" : 15.0105993 * AMU, "color" : BLACK, "radius" : 0.4},
    "C16" : {"mass" : 16.014701 * AMU, "color" : BLACK, "radius" : 0.4},
    "C17" : {"mass" : 17.022579 * AMU, "color" : BLACK, "radius" : 0.4},
    "N11" : {"mass" : 11.02609 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N12" : {"mass" : 12.0186132 * AMU, "color" :   PURE_BLUE, "radius" : 0.4},
    "N13" : {"mass" : 13.00573861 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N14" : {"mass" : 14.00307400443 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N15" : {"mass" : 15.00010889888 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N16" : {"mass" : 16.0061017 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N17" : {"mass" : 17.008450 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N18" : {"mass" : 18.014078 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N19" : {"mass" : 19.017022 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "N20" : {"mass" : 20.023370 * AMU, "color" : PURE_BLUE, "radius" : 0.4},
    "O12" : {"mass" : 12.034368 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O13" : {"mass" : 13.024815 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O14" : {"mass" : 19.003580 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O15" : {"mass" : 15.0030656 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O16" : {"mass" : 15.99491461957 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O17" : {"mass" : 16.99913175650 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O18" : {"mass" : 17.99915961286 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O19" : {"mass" : 19.003580 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O20" : {"mass" : 20.0040767 *  AMU, "color" : PURE_RED, "radius" : 0.4},
    "O21" : {"mass" : 21.008656 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O22" : {"mass" : 22.00997 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "O23" : {"mass" : 23.01570 * AMU, "color" : PURE_RED, "radius" : 0.4},
    "F15" : {"mass" : 15.01801 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F16" : {"mass" : 16.011466 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F17" : {"mass" : 17.00209524 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F18" : {"mass" : 18.0009380 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F19" : {"mass" : 18.99840316273 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F20" : {"mass" : 19.99998132 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F21" : {"mass" : 20.9999490 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F22" : {"mass" : 22.002999 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F23" : {"mass" : 23.003530 * AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "F24" : {"mass" : 24.008100  *AMU, "color" : ManimColor.from_hex("#AAAA30"), "radius" : 0.4},
    "Ne16" : {"mass" : 16.025751 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne17" : {"mass" : 17.0177140 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne18" : {"mass" : 18.0057082 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne19" : {"mass" : 19.0018802 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne20" : {"mass" : 19.9924401762 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne21" : {"mass" : 20.993846685 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne22" : {"mass" : 21.991385114 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne23" : {"mass" : 22.99446690 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne24" : {"mass" : 23.9936108 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne25" : {"mass" : 24.997810 * AMU, "color" : MAROON, "radius" : 0.4},
    "Ne26" : {"mass" : 26.000516 * AMU, "color" : MAROON, "radius" : 0.4},
    "Na20" : {"mass" : 20.007351 * AMU, "color" : LOGO_BLUE, "radius" : 0.4},
    "Na21" : {"mass" : 20.9976552 * AMU, "color" : LOGO_BLUE, "radius" : 0.4},
    "Na22" : {"mass" : 21.9944364 * AMU, "color" : LOGO_BLUE, "radius" : 0.4},
    "Na23" : {"mass" : 22.9897692820 * AMU, "color" : LOGO_BLUE, "radius" : 0.5},
    "Na24" : {"mass" : 23.99096278 * AMU, "color" : LOGO_BLUE, "radius" : 0.5},
    "Na25" : {"mass" : 24.9899540 * AMU, "color" : LOGO_BLUE, "radius" : 0.5},
    "Na26" : {"mass" : 25.992633 * AMU, "color" : LOGO_BLUE, "radius" : 0.5},
    "Na27" : {"mass" : 26.994077 * AMU, "color" : LOGO_BLUE, "radius": 0.5},
    "Na28" : {"mass" : 27.998939 * AMU, "color" : LOGO_BLUE, "radius" : 0.5},
    "Mg20" : {"mass" : 20.0187631 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg21" : {"mass" : 21.011713 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg22" : {"mass" : 21.9995738 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg23" : {"mass" : 22.9941237 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg24" : {"mass" : 23.985041697 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg25" : {"mass" : 24.985836976 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg26" : {"mass" : 25.982592968 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg27" : {"mass" : 26.98434059 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg28" : {"mass" : 27.9838768 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Mg29" : {"mass" : 28.9886072 * AMU, "color" : ManimColor.from_hex("#C036AC"), "radius" : 0.5},
    "Al22" : {"mass" : 22.01942310 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al23" : {"mass" : 23.00724435 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al24" : {"mass" : 23.99994760 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al25" : {"mass" : 24.990428308 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al26" : {"mass" : 25.98689169 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al27" : {"mass" : 26.98153853 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al28" : {"mass" : 27.981910009 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al29" : {"mass" : 28.98045316 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Al30" : {"mass" : 29.9829692 * AMU, "color" : LOGO_GREEN, "radius" : 0.5},
    "Si22" : {"mass" : 22.03611 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si23" : {"mass" : 23.02571 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si24" : {"mass" : 24.011535 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si25" : {"mass" : 25.004109 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si26" : {"mass" : 25.992330 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si27" : {"mass" : 26.98670491 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si28" : {"mass" : 27.97692653465 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si29" : {"mass" : 28.97649466490 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si30" : {"mass" : 29.973770136 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "Si31" : {"mass" : 30.975363196 * AMU, "color" : PURPLE_A, "radius" : 0.5},
    "P25" : {"mass" : 25.01178 * AMU, "color" : TEAL_E, "radius" : 0.5}, #?????? wrong mass
    "P26" : {"mass" : 26.01178 * AMU, "color" : TEAL_E, "radius" : 0.5},
    "P27" : {"mass" : 26.999230 *AMU, "color" : TEAL_E, "radius" : 0.5},
    "P28" : {"mass" : 27.992315 * AMU, "color" : TEAL_E, "radius" : 0.5},
    "P29" : {"mass" : 28.98180037 * AMU, "color" : TEAL_E, "radius" : 0.5},
    "P30" : {"mass" : 29.978313490 * AMU, "color" : TEAL_E, "radius" : 0.5},
}

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
        return np.array([[i.vecteur[0], i.vecteur[1], i.vecteur[2]] for i in content])

    def get_reac(self) -> np.ndarray :
        return parser(self.name)[0]

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
        if "anti_" in self.name:
            self.name = self.name.split("_")[1]
        self.dic: dict = ATOMS[self.name] 
        self.norm: float = np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
        self.vecteur /= self.norm
        self.norm: float = np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

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

    def __init__(self, vec: Vecteur, sub_products: list, eq_reac: list, reaction_str: str):
        # Attributs
        self.reaction_str: str = reaction_str
        self.eq_reac: list[str] = eq_reac
        self.reac = self.__get_reac()
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
        
        in_vec = np.array([float(v[1][0]), float(v[1][1]), float(v[1][2])])

        eq_reac = v[0][2:]
        eq_reac = eq_reac[:-1]
        sub_products = [Sub_product(i[0], float(i[1]), np.array([float(i[2]), float(i[3]), float(i[4])])) for i in v[2:]]
        reactions.append(Reaction(in_vec, sub_products, eq_reac, i))

    del(liste)
 
    return np.array(reactions), int(energy), 0
