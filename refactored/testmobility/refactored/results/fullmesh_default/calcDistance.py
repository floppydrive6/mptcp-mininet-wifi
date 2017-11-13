#!/usr/bin/python

"""
MPTCP performance test
created by:
Grzegorz Przybylo
AGH University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
"""

import os
import sys
import math


def main(argv):
    fileWithIperf = argv[1]
    fileWithPosition = argv[2]
    whichAp = argv[3]
    fileWithResults = "distanceAndBwAp" + whichAp + ".txt"
    try:
        os.remove(fileWithResults)
    except OSError:
        pass
    testDuration = 100
    #  ap2 - 55.0 , 20.0 ap3 - 50.0 , 11.0
    if int(whichAp) == 3:
        pos_x = 50.0
        pos_y = 11.0
    else:
        pos_x = 55.0
        pos_y = 20.0
    print pos_x
    print pos_y
    bandwidthTab = []
    positionTab = []
    distanceTab = []
    with open(fileWithIperf, 'r') as fi:
        for line in fi:
            line = line.split(" ")
            bandwidthValue = float(line[-2])
            bandwidthTab.append(bandwidthValue)
    with open(fileWithPosition, 'r') as fi:
        for line in fi:
            line = line.strip("()").split(",")[:-1]
            positionTab.append(line)
    for pos in positionTab:
        xSta = float(pos[0].strip('\''))
        ySta = float(pos[1].strip(" ").strip('\''))
        distance = calcPos(pos_x, pos_y, xSta, ySta)
        distanceTab.append(distance)
    for i in range(testDuration):
        with open(fileWithResults, "a+") as fw:
            fw.write(str(distanceTab[i]) + " " + str(bandwidthTab[i]) + "\n")


def calcPos(posXA, posYA, posXB, posYB):
    return math.sqrt(pow(posXB - posXA, 2) + pow(posYB - posYA, 2))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv)
    else:
        print "Please specify 3 arguments"
