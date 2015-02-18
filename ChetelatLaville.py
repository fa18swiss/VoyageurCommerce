__author__ = 'Chetelat Laville'

import math
from random import shuffle

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
        distance1 = math.sqrt(self.__x * self.__x + self.__y*self.__y)
        distance2 = math.sqrt(other.__x * other.__x + other.__y*other.__y)
        return math.fabs(distance1 - distance2)

def mutate(self):
    #todo
    return None

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
        shuffle(villesSolution)
        #print("villes after =", end="")
        #print(villesSolution)
        solutions.append(Solution(villesSolution))
    return solutions

def mutate(solutions):
    newSols = []
    for solution in solutions:
        villesSolution = list(solution.getVilles())
        shuffle(villesSolution)
        newSols.append(Solution(villesSolution))
    return newSols + solutions

def elitisme(solutions):
    def comp(sol1):
        return sol1.getDistance()
    print("befire :")
    print(solutions)
    solutionsSorted = list(solutions)
    solutionsSorted.sort(key=lambda sol: sol.getDistance())
    print("after")
    print(solutionsSorted)
    return solutionsSorted[0:int(len(solutionsSorted)/2)]

def ga_solve(file=None, gui=True, maxtime=0):
    if file == None and gui == False:
        raise Exception("No file and no gui !")


    import pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
    import sys

    screen_x = 500
    screen_y = 500

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

    cities = []
    draw(cities)

    if file:
        #todo loades cities from file
        fileReader = open(file, "r")
        for line in fileReader:
            line = line.replace("\n", "")
            print("Line : " + line)
            parts = line.split(" ")
            pos = (int(parts[1]), int(parts[2]))
            cities.append(Ville(parts[0], pos))
            pass
        print(cities)
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

    for i in range(10):
        if solutions:
            solutions = mutate(solutions)
        else:
            solutions = construirePopulation(cities)

        solutions = elitisme(solutions)
        bestSolution = solutions[0]
        cities = bestSolution.getVilles();
        screen.fill(0)
        for ville in cities:
            screen.blit(font_city.render(str(ville), True, font_color, ), ville.pos())
            pygame.draw.circle(screen,city_color,ville.pos(),city_radius)
        pygame.draw.lines(screen,city_color,True,[city.pos() for city in cities])
        text = font.render(repr(bestSolution), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT: break

def main():
    import sys
    gui = None
    maxtime = None
    filename = None
    nextismaxtime = False
    for arg in sys.argv[1:]:
        print("arg = '%s'" % arg)
        if arg == "--no-gui":
            nextismaxtime = False
            gui = False
        elif arg == "--maxTime":
            nextismaxtime = True
        elif nextismaxtime:
            maxtime = int(arg)
            nextismaxtime = False
        else:
            if filename:
                print("Two filename define !")
                sys.exit(0)
            filename = arg
    ga_solve(filename, gui, maxtime)



if __name__ == "__main__":
    main()
