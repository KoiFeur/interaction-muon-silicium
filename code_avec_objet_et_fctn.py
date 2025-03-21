import numpy as np
import matplotlib.pyplot as plt

class Reaction:
    def __init__(self, type_r, energie, nbr_sous_prod, vertex):
        self.nbr_sous_prod = nbr_sous_prod
        self.vertex = vertex
        self.type_r = type_r
        self.energie = energie
                          
        
        
        

def parser(file: str) -> list:
    "Rentrer un fichier pour transformation en données utilisables"
    liste = [' ']
    nbr_re = 0
    with open(file,'r') as file:
        for line in file:
            if '---' in line:
                liste.append(line)
                nbr_re += 1
            else:
                liste[-1] += line
                
    for i in range(len(liste)):
        liste[i]=liste[i].split('\n')
        #liste.remove(liste[i][-1])
        
        for n in range(len(liste[i])):
            liste[i][n]=liste[i][n].split(' ')
        
        reaction = Reaction(liste[i][0][2], liste[i][1][6], liste[i][1][7], liste[i][1][0])
    
    #liste.remove(liste[0])
    #liste.remove(liste[-1])

    
    
    print(liste)
    #print(reaction)
    print('Il y a',nbr_re,'réactions.')
    print(liste[0][1][6])

parser('data_for_test')




























