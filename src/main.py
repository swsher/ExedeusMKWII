# configuring environment
# filepaths will be different for your local machine
import sys
import os
sys.path.append("/home/ultra/ExedeusMKWII/pynoko/build") # path to pynoko .so
os.environ["KINOKO_FILESYSTEM_ROOT"] = "/home/ultra/ExedeusMKWII/Kinoko/out" # path for locating race data

import cv2 # for displaying images
import pynoko

from sortedcontainers import SortedList

# sorting characters and vehicles by weight class
# miis not added currently

lightCharacters = [pynoko.Character.Baby_Mario, pynoko.Character.Baby_Luigi, pynoko.Character.Baby_Peach, pynoko.Character.Baby_Daisy,
                   pynoko.Character.Toad, pynoko.Character.Dry_Bones, pynoko.Character.Toadette, pynoko.Character.Koopa_Troopa]
mediumCharacters = [pynoko.Character.Mario, pynoko.Character.Luigi, pynoko.Character.Yoshi, pynoko.Character.Daisy, pynoko.Character.Peach,
                    pynoko.Character.Birdo, pynoko.Character.Diddy_Kong, pynoko.Character.Bowser_Jr]
heavyCharacters = [pynoko.Character.Waluigi, pynoko.Character.Bowser, pynoko.Character.Donkey_Kong, pynoko.Character.Wario, pynoko.Character.King_Boo,
                   pynoko.Character.Dry_Bowser, pynoko.Character.Funky_Kong, pynoko.Character.Rosalina]

lightVehicles = [pynoko.Vehicle.Standard_Kart_S, pynoko.Vehicle.Baby_Booster, pynoko.Vehicle.Mini_Beast, pynoko.Vehicle.Cheep_Charger, pynoko.Vehicle.Tiny_Titan,
                 pynoko.Vehicle.Blue_Falcon, pynoko.Vehicle.Standard_Bike_S, pynoko.Vehicle.Bullet_Bike, pynoko.Vehicle.Bit_Bike, pynoko.Vehicle.Quacker,
                 pynoko.Vehicle.Magikruiser, pynoko.Vehicle.Jet_Bubble]
mediumVehicles = [pynoko.Vehicle.Standard_Kart_M, pynoko.Vehicle.Classic_Dragster, pynoko.Vehicle.Wild_Wing, pynoko.Vehicle.Super_Blooper, pynoko.Vehicle.Daytripper,
                  pynoko.Vehicle.Sprinter, pynoko.Vehicle.Standard_Bike_M, pynoko.Vehicle.Mach_Bike, pynoko.Vehicle.Sugarscoot, pynoko.Vehicle.Zip_Zip,
                  pynoko.Vehicle.Sneakster, pynoko.Vehicle.Dolphin_Dasher]
heavyVehicles = [pynoko.Vehicle.Standard_Kart_L, pynoko.Vehicle.Offroader, pynoko.Vehicle.Flame_Flyer, pynoko.Vehicle.Piranha_Prowler, pynoko.Vehicle.Jetsetter,
                 pynoko.Vehicle.Honeycoupe, pynoko.Vehicle.Standard_Bike_L, pynoko.Vehicle.Flame_Runner, pynoko.Vehicle.Wario_Bike, pynoko.Vehicle.Shooting_Star,
                 pynoko.Vehicle.Spear, pynoko.Vehicle.Phantom]

# class storing a node on the game tree
class Node:

    def __init__(self, string, completion, isWin):
        self.string = string
        self.completion = completion-1.0
        self.completion = self.getWeightedCompletion()
        self.isWin = isWin
    
    # comparators to allow easy sorting by sortedcontainers
    def __eq__(self, other):
        return self.completion == other.completion
    
    def __ne__(self, other):
        return self.completion != other.completion

    def __le__(self, other):
        return self.completion <= other.completion
    
    def __lt__(self, other):
        return self.completion < other.completion
    
    def __ge__(self, other):
        return self.completion >= other.completion
    
    def __gt__(self, other):
        return self.completion > other.completion

    # returns children of the node by simulating new time trials
    def getChildren(self, mkw, buttons, frames):
        childList = []
        for i in range(0, 15):
            iString = ""
            if i < 10:
                iString = "0" + str(i)
            else:
                iString = str(i)

            mkw.reset()
            childString = self.string + (iString*frames)
            isWin = False
            for frame in range(0, len(self.string)//2 + frames):
                # full faith in chat for this fix, well beyond my scope of experience with kinoko
                # fucking ridiculous that it caught this bug and resolved it
                # ai getting too good holy
                if frame != 171:
                    isWin = doTick(mkw, buttons, getX(childString, frame))
                else:
                    isWin = doTick(mkw, 0, 7)
                if isWin:
                    childString = childString[:frame*2]
                    break
            
            childList.append(Node(childString, mkw.raceCompletion(), isWin))
        
        return childList
    
    def getWeightedCompletion(self):
        return -1.0 if self.completion < 0 else (self.completion*self.completion)/max(self.getTime(), 2)
    
    def getTime(self):
        return (len(self.string) // 2) - 172

def getX(string, frame):
    strIndex = frame*2
    return int(string[strIndex:strIndex+2])

# does a frame and then returns whether or not the race is finished
def doTick(mkw, buttons, x):
    mkw.setInput(buttons, x, 7, pynoko.Trick.NoTrick)
    mkw.calc()
    return (mkw.raceCompletion() > 4.0)

def allCombinations():
    # not all right now
    courses = [pynoko.Course.Bowsers_Castle]#list(pynoko.Course)
    characters = [heavyCharacters[0]]
    vehicles = heavyVehicles
    autos = [True]
    bestTime = 999999999999999
    for course in courses:
        for character in characters:
            for vehicle in vehicles:
                for isAuto in autos:
                    if character in lightCharacters and vehicle in lightVehicles:
                        bestTime = test1(course, character, vehicle, isAuto, bestTime)
                    elif character in mediumCharacters and vehicle in mediumVehicles:
                        bestTime = test1(course, character, vehicle, isAuto, bestTime)
                    elif character in heavyCharacters and vehicle in heavyVehicles:
                        bestTime = test1(course, character, vehicle, isAuto, bestTime)
    
def test1(course, character, vehicle, isAuto, bestTime):
    print(course, character, vehicle, isAuto)
    mkw = pynoko.KHostSystem()
    mkw.configureTimeTrial(course, character, vehicle, isAuto)
    mkw.init()
    # always accelerate
    buttons = pynoko.buttonInput([pynoko.KPAD_BUTTON_A])
    
    nodeList = SortedList()
    baseNode = Node("07"*172, mkw.raceCompletion(), False)
    nodeList.add(baseNode)
    
    bestNode = baseNode

    solutionFlag = False
    while nodeList and not solutionFlag:
        currentNode = nodeList.pop()
        if currentNode > bestNode:
            bestNode = currentNode

        childNodes = currentNode.getChildren(mkw, buttons, 128)
        for child in childNodes:
            if child.isWin:
                solutionFlag = True
                if child.getTime() < bestTime:
                    bestTime = child.getTime()
                    print(child.string[172*2:])
                break
            nodeList.add(child)

    mkw.reset()
    return bestTime

def playback(string):
    mkw = pynoko.KHostSystem()
    mkw.configureTimeTrial(pynoko.Course.Luigi_Circuit, pynoko.Character.Baby_Luigi, pynoko.Vehicle.Baby_Booster, True)
    mkw.init()
    buttons = pynoko.buttonInput([pynoko.KPAD_BUTTON_A])

    for frame in range(0, len(string)//2):
        if frame != 171:
            mkw.setInput(buttons, getX(string, frame), 7, pynoko.Trick.NoTrick)
        else:
            mkw.setInput(0, 7, 7, pynoko.Trick.NoTrick)

        mkw.calc()
        mkw.draw()

        cv2.imshow("mkw", mkw.getFrame()[:, :, 2::-1])
        cv2.waitKey(1)
    
    mkw.reset()


def main():
    # string = ""
    # with open("files/test1.txt", 'r') as file:
    #     string = file.read()

    # #test1()
    #playback(string)
    allCombinations()

if __name__ == "__main__":
    main()