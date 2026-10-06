# configuring environment
# filepaths will be different for your local machine
import sys
import os
sys.path.append("/home/ultra/ExedeusMKWII/pynoko/build") # path to pynoko .so
os.environ["KINOKO_FILESYSTEM_ROOT"] = "/home/ultra/ExedeusMKWII/Kinoko/out" # path for locating race data

import cv2 # for displaying images
import pynoko

from sortedcontainers import SortedList

# class storing a node on the game tree
class Node:

    def __init__(self, string, completion, isWin):
        self.string = string
        self.completion = completion
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

def getX(string, frame):
    strIndex = frame*2
    return int(string[strIndex:strIndex+2])

# does a frame and then returns whether or not the race is finished
def doTick(mkw, buttons, x):
    mkw.setInput(buttons, x, 7, pynoko.Trick.NoTrick)
    mkw.calc()
    return (mkw.raceCompletion() > 4.0)

def test1():
    mkw = pynoko.KHostSystem()
    # baby luigi in baby booster automatic hell yeah
    mkw.configureTimeTrial(pynoko.Course.Luigi_Circuit, pynoko.Character.Baby_Luigi, pynoko.Vehicle.Baby_Booster, True)
    mkw.init()
    # always accelerate
    buttons = pynoko.buttonInput([pynoko.KPAD_BUTTON_A])
    
    nodeList = SortedList()
    baseNode = Node("", mkw.raceCompletion(), False)
    nodeList.add(baseNode)
    
    bestNode = baseNode

    solutionFlag = False
    while nodeList and not solutionFlag:
        currentNode = nodeList.pop()
        if currentNode > bestNode:
            bestNode = currentNode
            print(currentNode.completion)

        childNodes = currentNode.getChildren(mkw, buttons, 16)
        for child in childNodes:
            if child.isWin:
                solutionFlag = True
                print(child.string)
                break
            nodeList.add(child)

    mkw.reset()

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
    string = ""
    with open("test1.txt", 'r') as file:
        string = file.read()

    test1()
    #playback(string)

if __name__ == "__main__":
    main()