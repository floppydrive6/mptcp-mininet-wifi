#!/usr/bin/python

"""
MPTCP performance test
created by:
Grzegorz Przybylo
University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
"""

import os
import sys


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
        with open(file, 'r') as f:
            for line in f:
                if "sta1-eth1" in line:
                    pass
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
                    if len(toMbit) == 8:
                        for i in range(8):
                            allTables[i].append(toMbit[i])

        condt = len(ethInput)

        if all(len(lenCheck) == condt for lenCheck in allTables):
            with open(filenameToSave, "a+") as fw:
                fw.write(
                    "ethInput ethOutput mobileInput mobileOutput wifiInput wifiOutput sumInput sumOutput \n")
                for i in range(condt):
                    for result in allTables:
                        fw.write(str(result[i]) + " ")
                    fw.write("\n")
        else:
            print "Something went wrong"


if __name__ == "__main__":
    main(sys.argv)
