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
import re


def main(argv):
    filenameToSaveBase = "ifstatOutputResults"
    for file in argv[1:]:
        appendix = str(file).split("_")[-2:]
        appendix = "".join(map(lambda x: x.split(".", 1)[0].title(), appendix))
        filenameToSave = filenameToSaveBase + appendix + ".txt"
        try:
            os.remove(filenameToSave)
        except OSError:
            pass
        eventsTable = ["ethernet down", "ethernet up",
                       "wifi down", "wifi up", "end"]
        ethInput = []
        ethOutput = []
        mobileInput = []
        mobileOutput = []
        wifiInput = []
        wifiOutput = []
        sumInput = []
        sumOutput = []
        allTables = [ethInput, ethOutput, mobileInput,
                     mobileOutput, wifiInput, wifiOutput, sumInput, sumOutput]
        header = []
        interfaceCol = len(allTables) - 2
        with open(file, 'r') as f:
            counter = 0
            for line in f:
                if "sta1-wlan0" in line:
                    counter += 1
                    if counter == 1:
                        order = []
                        line = " ".join(line.split())
                        line = line.replace("-", " ").split(" ")
                        if len(line) == interfaceCol:
                            line = line[1::2]
                            itemsToFind = ["eth1", "eth2", "wlan0"]
                            for x in itemsToFind:
                                indexFound = line.index(x)
                                line.insert(indexFound + 1, x + "Output")
                            line = line + ["sumInput", "sumOutput"]
                            header = " ".join(line)
                            for x in itemsToFind:
                                foundIndexes = finder(line, x)
                                order = order + foundIndexes
                            order = order + [len(order), len(order) + 1]
                            # reorder allTables
                            allTables = [allTables[i] for i in order]
                        else:
                            print "Something went wrong!"
                elif "Kbps" in line:
                    pass
                elif "n/a" in line:
                    pass
                elif any(event in line for event in eventsTable):
                    toAppend = " ".join(line.replace("*", "").split())
                    camleCase = "".join(
                        x for x in toAppend.title() if not x.isspace())
                    for element in allTables:
                        element.append(camleCase)
                else:
                    toAppend = " ".join(line.split())
                    toAppend = toAppend.split(" ")
                    # convert from [Kbit/s] to [Mbit/s]
                    toMbit = map(lambda x: float(x) / 1024, toAppend)
                    toMbit.append(sum(toMbit[::2]))
                    toMbit.append(sum(toMbit[1::2]))
                    if len(toMbit) == len(toAppend) + 2:
                        for i in range(len(toMbit)):
                            allTables[i].append(toMbit[i])

        # just to make sure if it is ok now
        # print ethOutput
        # print wifiOutput
        # print mobileInput
        modifiedHeader = changeHeader(header)
        condt = len(ethInput)

        if all(len(lenCheck) == condt for lenCheck in allTables):
            with open(filenameToSave, "a+") as fw:
                fw.write(str(modifiedHeader) + "\n")
                for i in range(condt):
                    for result in allTables:
                        fw.write(str(result[i]) + " ")
                    fw.write("\n")
        else:
            print "Something went wrong!"


def finder(inList, substr):
    indexes = []
    for i, s in enumerate(inList):
        if substr in s:
            indexes.append(i)
    if len(indexes) > 0:
        return indexes
    else:
        return None


def changeHeader(header):
    newHeader = header
    newHeader = newHeader.replace("eth1", "ethernet")
    newHeader = newHeader.replace("wlan0", "wifi")
    newHeader = newHeader.replace("eth2", "mobile")
    newHeader = re.sub(r"ethernet ", "ethernetInput ", newHeader)
    newHeader = re.sub(r"wifi ", "wifiInput ", newHeader)
    newHeader = re.sub(r"mobile ", "mobileInput ", newHeader)
    return newHeader


if __name__ == "__main__":
    main(sys.argv)
