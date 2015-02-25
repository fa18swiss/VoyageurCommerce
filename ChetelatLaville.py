__author__ = 'Chetelat Laville'

import math
import random
import time

random.seed()

#Variable déterminant le nombre de solution a garder
nbSolution = 10

class Ville:
    def __init__(self, name, pos):
        self.__name = name
        self.__pos = pos
        self.__x = pos[0]
        self.__y = pos[1]

    def name(self):
        return self.__name

    def pos(self):
        return self.__pos

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def __repr__(self):
        return "'%s' (%d, %d)" % (self.__name, self.__x, self.__y)

    def distance(self, other):
        dx = self.__x - other.__x
        dy = self.__y - other.__y
        return math.sqrt(dx * dx + dy * dy)

class Solution:
    idSeq = 1
    def __init__(self, villes):
        self.__villes = villes
        self.__distance = 0
        self.__id = Solution.idSeq
        Solution.idSeq += 1

    def getDistance(self):
        if self.__distance <= 0:
            self.distance()
        return self.__distance

    def getVilles(self):
        return self.__villes

    def distance(self):
        distance = 0
        precedente = self.__villes[-1]
        for ville in self.__villes:
            distance += ville.distance(precedente)
            precedente = ville
        self.__distance = distance
        return self.__distance

    def __repr__(self):
        return "Solution id = %d distance %d" %(self.__id, self.getDistance())

def croisementSimple(solution1,solution2):
   """
   Fonction de croisement simple
   :param solution1, solution2: Solution, Solution
   :return solutionF1, solutionF2: Solution, Solution
   """
   solutionF1 = []
   solutionF2 = []

   #Récupération des villes de chaque solution
   villes1 = solution1.getVilles()
   villes2 = solution2.getVilles()

   #random 0 et size
   nbRand = random.randrange(len(villes1))

   #Rajouter les villes jusqu'au random
   for i in range(nbRand):
      solutionF1.append(villes1[i])

   for i in range(nbRand):
      solutionF2.append(villes2[i])

   #Rajouter les villes manquantes depuis l'autre solution pour compléter la solution
   for ville in villes2:
      if solutionF1.count(ville) <= 0:
         solutionF1.append(ville)

   for ville in villes1:
      if solutionF2.count(ville) <= 0:
         solutionF2.append(ville)

   return Solution(solutionF1),Solution(solutionF2)

def croisementComplexe(solution1,solution2):
   """
   Fonction de croisement complexe
   :param solution1, solution2: Solution, Solution
   :return solution: Solution
   """
   solution = []

   #Récupération des villes de chaque solution
   villes1 = solution1.getVilles()
   villes2 = solution2.getVilles()
   size = len(villes1)

   #Définit l'index de la 1ere ville aléatoirement
   indexFirstVille = random.randrange(size)

   #Tant que la solution n'est pas complète
   while len(solution) < size:

         #Récupérer la 1ère ville
         firstVille = villes1[indexFirstVille]
         nextVille = 0

         #Si la 1ere ville ne fait pas partie de la solution, chercher ses villes suivantes
         if firstVille not in solution:
            nextVille = chercheVilleSuivante(firstVille,solution,size,villes1,villes2)
            solution.append(firstVille)
            solution.append(nextVille)
            indexFirstVille = villes1.index(nextVille)
         #Si la ville est présent dans la solution mais qu'elle est la dernière, chercher ses villes suivantes
         elif solution[-1] == firstVille:
            nextVille = chercheVilleSuivante(firstVille,solution,size,villes1,villes2)
            solution.append(nextVille)
            indexFirstVille = villes1.index(nextVille)
         #Sinon recommencer avec une autre ville
         else:
            indexFirstVille = random.randrange(size)

   return Solution(solution)


def chercheVilleSuivante(firstVille, solution,size,villes1,villes2):
   """
   Fonction de recherche de la ville suivante pour croisement complexe
   :param ville,solution,size,villes1,villes2: Ville,Solution,int,List<Ville>,List<Ville>
   :return solutions: List<Solution>
   """
   nextVille = 0

   #Si l'index de la ville suivante, pour la même solution, n'est pas hors limite
   index1 = villes1.index(firstVille)+1
   if index1 >= size:
      index1 = 0
   villeSuivante1 = villes1[index1]

   #Récupérer l'index de la ville suivante pour la solution 2
   #Vérifier si l'index est hors limite
   index2 = villes2.index(firstVille)+1
   if index2 >= size:
      index2 = 0
   villeSuivante2 = villes2[index2]

   #Tant qu'il n'y a pas au moins 1 ville qui n'est pas encore présent dans la solution
   while villeSuivante1 in solution and villeSuivante2 in solution:
      if villeSuivante1 in solution:
         villeSuivante1 = villes1[random.randrange(size)]
      if villeSuivante2 in solution:
         villeSuivante2 = villes2[random.randrange(size)]

   distance1 = -1
   distance2 = -1

   if villeSuivante1 not in solution:
      distance1 = firstVille.distance(villeSuivante1)
   if villeSuivante2 not in solution:
      distance2 = firstVille.distance(villeSuivante2)

   if distance1 != -1:
      if distance2 != -1:
         if distance1 > distance2:
            nextVille = villeSuivante2
         else:
            nextVille = villeSuivante1
      else:
         nextVille = villeSuivante1
   else:
      nextVille = villeSuivante2

   return nextVille

def construirePopulation(villes):
    """
    Fonction de construction de la population
    :param villes: List<Ville>
    :return solutions: List<Solution>
    """

    solutions = []
    #Rajouter la population de base
    solutions.append(Solution(list(villes)))
    #Rajouter des autres populations dans la solution
    for i in range(nbSolution-1):
        villesSolution = list(villes)
        random.shuffle(villesSolution)
        solutions.append(Solution(villesSolution))
    return solutions

def mutate(solutions):
    """
    Fonction de mutation
    :param solution: Solution
    :return solution: Solution
    """
    newSols = []
    for solution in solutions:
        villesSolution = list(solution.getVilles())
        size = len(villesSolution)
        nbChange = random.randrange(int(size / 10.0 + 1)) + 1
        for i in range(nbChange):
            v1 = v2 = random.randrange(size)
            while v1 == v2:
                v2 = random.randrange(size)
            onlySwap2 = random.randrange(2) == 0

            if onlySwap2:
                villesSolution[v1], villesSolution[v2] = villesSolution[v2], villesSolution[v1]
            else:
                #check v1 < v2
                if v1 > v2:
                    v1, v2 = v2, v1
                while v1 < v2:
                    villesSolution[v1], villesSolution[v2] = villesSolution[v2], villesSolution[v1]
                    v1 += 1
                    v2 -= 1

        newSols.append(Solution(villesSolution))
    return newSols + solutions

def elitisme(solutions):
   """
   Fonction de selection de type élitisme
   :param solution: Solution
   :return solution: Solution
   """
   solutionsSorted = list(solutions)
   solutionsSorted.sort(key=lambda sol: sol.getDistance())
   return solutionsSorted[:nbSolution]

def ga_solve(file=None, gui=True, maxTime=None):
    # controle des paramètres
    if not file and not gui:
        raise Exception("No file and no gui !")

    #temps limite
    limitTime = None
    # si maxTime est défini
    if maxTime:
        #calcule du temps limite
        limitTime = maxTime + time.time()

    # importation pygame
    import pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN
    import sys
    # paramètres d'écran
    screen_x = 500
    screen_y = 500

    #tableau des villes chargées
    cities = []
    #si gui, création fenetre
    if gui:
        city_color = [10,10,200] # blue
        city_radius = 3

        font_color = [255,255,255] # white
        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption('Exemple')
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None,30)
        font_city = pygame.font.Font(None,20)

    def draw(villes):
        """
        Fonction pour dessiner le tableau de ville
        :param villes: Tableau de villes
        :return: None
        """
        screen.fill(0)
        for ville in villes:
            screen.blit(font_city.render(str(ville), True, font_color, ), ville.pos())
            pygame.draw.circle(screen,city_color,ville.pos(),city_radius)
        text = font.render("Nombre: %i" % len(villes), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()
    def drawSol(solution, i):
        """
        Fonction pour dessiner une solution
        :param solution: Solution
        :param i: no de l'itération
        :return: None
        """
        cities = solution.getVilles()
        screen.fill(0)
        for ville in cities:
            screen.blit(font_city.render(str(ville), True, font_color, ), ville.pos())
            pygame.draw.circle(screen,city_color,ville.pos(),city_radius)
        pygame.draw.lines(screen,city_color,True,[city.pos() for city in cities])
        text = font.render("%d %s" % (i, repr(bestSolution)), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    if gui:
        #si gui, affihage du tableau (même vide
        draw(cities)

    if file: #si la source est le fichier, ouverture et lecture
        fileReader = open(file, "r")
        # pour chaque ligne
        for line in fileReader:
            #suppression caractères inutils
            line = line.replace("\n", "")
            #séparation par l'espace
            parts = line.split(" ")
            # création tableau position
            pos = (int(parts[1]), int(parts[2]))
            # ajout en tant que ville
            cities.append(Ville(parts[0], pos))
        fileReader.close()
    else: # sinon la source est l'utilisateur
        citiesIndex = 0
        #flag collection
        collecting = True
        #tant qu'il faut collecter
        while collecting:
            # pour chaque évènement
            for event in pygame.event.get():
                # si quit, fin du programme
                if event.type == QUIT:
                    sys.exit(0)
                #si touche enter, fin de la collection si le nombre est suffisant
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    if len(cities) > 2:
                        collecting = False
                # si click souris
                elif event.type == MOUSEBUTTONDOWN:
                    citiesIndex += 1
                    #récupération et création d'une ville
                    cities.append(Ville("v%d" % citiesIndex, pygame.mouse.get_pos()))
                    # affichage
                    draw(cities)

    # si le nombre de ville n'est pas suffisant, erreur et arret
    if len(cities) == 0:
        print("Pas de villes !")
        sys.exit(0)

    # tableau de solutions initialisé a des chemins aux hazard
    solutions = construirePopulation(cities)
    # flag pour la boucle
    continueLoop = True
    # Nombre d'itération
    i = 1
    #valeur de la meilleur solution
    lastBestSolDist = float("inf")
    #nombre d'itération avec la même valeur pour la meilleir solution
    nbSolEquals = 0
    # tant que boucle
    while continueLoop:

        """
        Suite à plusieurs tests de performances,
        nous avons remarqué que notre algorithme génétique donnait de meilleurs résultats
        avec seulement des mutations.
        C'est pour cela que nous avons implémentés les croisements, 1 simple et l'autre plus complexe,
        mais que l'on ne les appelle pas
        """
        #Croisement Complexe
        """
        tmpSol = []
        for i in range(nbSolution-1):
           sol1 = croisementComplexe(solutions[i],solutions[i+1])
           tmpSol.append(sol1)
        solutions = solutions + tmpSol
        """
        #Croisement Simple
        """
        tmpSol = []
        for i in range(nbSolution-1):
           sol1,sol2 = croisementSimple(solutions[i],solutions[i+1])
           tmpSol.append(sol1)
           tmpSol.append(sol2)
        solutions = list(tmpSol)
        """
        # mutation des solutions
        solutions = mutate(solutions)
        # elitisme
        solutions = elitisme(solutions)
        # récupération de la meilleur solition, grace à l'élitisme, c'est la 1ere
        bestSolution = solutions[0]
        # affichage de la solution si nécessaire
        if gui:
            drawSol(bestSolution, i)
        #contrôle du temps
        if limitTime: #si le temps est limité
            #controle que pas dépassé
            if time.time() > limitTime:
                continueLoop = False
        else:#sinon on parcour attant d'avoir n itération avec la même solution
            # si la distance est la même que la dernière fois
            if lastBestSolDist == bestSolution.getDistance():
                # nombre incrémenté
                nbSolEquals += 1
                # si > n fin de boucle
                if nbSolEquals > 1000:
                    continueLoop = False
            else:# si différent, reset
                nbSolEquals = 0
            #mag dernière solution
            lastBestSolDist = bestSolution.getDistance()
        #incrémentation
        i += 1
    # si gui, on affiche la meilleure solutions tant que on n'appiye pas sur une touche
    while gui:
        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT: break

    if gui:
        print("end with %s (i=%d)" % (bestSolution, i))
    #retour de la meilleur solution ainsi que la liste des nom des villes
    return bestSolution.getDistance(), [v.name() for v in bestSolution.getVilles()]

def main():
    #Utilise argParse
    import argparse
    parser = argparse.ArgumentParser()
    #définition des arguments
    parser.add_argument("--no-gui",  help="no graphical user interface", action="store_true")
    parser.add_argument("--maxTime", help="max execution time (seconds)", type=int)
    parser.add_argument("filename",  help="file of cities", nargs='?')
    # récupération des arguments
    args = parser.parse_args()
    # appel dee la fonction avec les arguments
    dist, cities = ga_solve(args.filename, not args.no_gui, args.maxTime)
    #affichage
    print("Solve distance = %d" % dist)

if __name__ == "__main__":
    main()
