#!/usr/bin/python

"""
calculating stats
created by:
Grzegorz Przybylo
AGH, University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
"""

import os
import re
import sys
import statistics


def main(argv):
    filenameToSave="statsResults.txt"
    try:
        os.remove(filenameToSave)
    except OSError:
        pass
    for file in argv[1:]:
        results = []
        with open(file, 'r') as f:
            for line in f:
                line = line.split(" ")
		if re.match(r'\d+[.]{0,1}\d+', line[1]):
                	results.append(float(line[1]))
        meanVal = statistics.mean(results)
        stdDevVal = statistics.stdev(results)
        pm = file.split("_")[1]
        sched = file.split("_")[2].split(".")[0]
        meanString = "Mean value for is: " + str(meanVal)
        stdDevString = "Standard Deviation value for is: " + str(stdDevVal)
        with open(filenameToSave, "a+") as fw:
            fw.write("Path Manager: " + pm + " and Scheduler: " + sched + "\n")
            fw.write(meanString + "\n")
            fw.write(stdDevString + "\n")
            fw.write("-" * 50 + "\n")


if __name__ == "__main__":
    main(sys.argv)
