__author__ = 'Chetelat Laville'

import math
import random
import time

random.seed()

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

def construirePopulation(villes):
    solutions = []
    solutions.append(Solution(list(villes)))
    for i in range(nbSolution-1):
        villesSolution = list(villes)
        #print("villes before =", end="")
        #print(villesSolution)
        random.shuffle(villesSolution)


        #print("villes after =", end="")
        #print(villesSolution)
        solutions.append(Solution(villesSolution))
    return solutions

def mutate(solutions):
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
            #print(onlySwap2)
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

            #print("v1(%d), v2(%d)" % (v1, v2))
        newSols.append(Solution(villesSolution))
    return newSols + solutions

def elitisme(solutions):
    #print("befire :")
    #print(solutions)
    solutionsSorted = list(solutions)
    solutionsSorted.sort(key=lambda sol: sol.getDistance())
    #print("after")
    #print(solutionsSorted)
    return solutionsSorted[0:int(len(solutionsSorted)/2)]

def ga_solve(file=None, gui=True, maxTime=None):

    #gui = False
    #file = "data/pb010.txt"
    #maxTime = 5


    limitTime = None
    if maxTime:
        limitTime = maxTime + time.time()
    if not file and not gui:
        raise Exception("No file and no gui !")

    import pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
    import sys

    screen_x = 500
    screen_y = 500


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
        screen.fill(0)
        for ville in villes:
            screen.blit(font_city.render(str(ville), True, font_color, ), ville.pos())
            pygame.draw.circle(screen,city_color,ville.pos(),city_radius)
        text = font.render("Nombre: %i" % len(villes), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()
    def drawSol(solution, i):
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

    cities = []
    if file:
        fileReader = open(file, "r")
        for line in fileReader:
            line = line.replace("\n", "")
            #print("Line : " + line)
            parts = line.split(" ")
            pos = (int(parts[1]), int(parts[2]))
            cities.append(Ville(parts[0], pos))
        #print(cities)
        fileReader.close()
    else:
        citiesIndex = 0
        collecting = True
        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    citiesIndex += 1
                    cities.append(Ville("v%d" % citiesIndex, pygame.mouse.get_pos()))
                    draw(cities)


    if len(cities) == 0:
        print("Pas de villes !")
        #todo MggBox
        sys.exit(0)

    solutions = None

    continueLoop = True
    i = 1
    lastBestSolDist = float("inf")
    nbSolEquals = 0
    while continueLoop:
        if solutions:
            solutions = mutate(solutions)
        else:
            solutions = construirePopulation(cities)

        solutions = elitisme(solutions)
        bestSolution = solutions[0]
        #print(bestSolution)
        if gui:
            drawSol(bestSolution, i)
        if limitTime:
            if time.time() > limitTime:
                continueLoop = False
        else:
            if lastBestSolDist == bestSolution.getDistance():
                nbSolEquals += 1
                if nbSolEquals > 1000:
                    continueLoop = False
            else:
                nbSolEquals = 0
            lastBestSolDist = bestSolution.getDistance()

        i += 1
    while gui:
        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT: break
    if gui:
        print("end with %s" % bestSolution)
    print("%d;" % i, end="")
    return bestSolution.getDistance(), [v.name() for v in bestSolution.getVilles()]

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-gui",  help="no graphical user interface", action="store_true")
    parser.add_argument("--maxTime", help="max execution time", type=int)
    parser.add_argument("filename",  help="file of cities", nargs='?')
    args = parser.parse_args()

    dist, cities = ga_solve(args.filename, not args.no_gui, args.maxTime)
    print("Solve distance = %d" % dist)

if __name__ == "__main__":
    main()
