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


def main(argv):
    fileWithIperfRaw = argv[1]
    fileWithResults = "iperf.log"
    try:
        os.remove(fileWithResults)
    except OSError:
        pass
    outputResults = []
    with open(fileWithIperfRaw, 'r') as f:
        counter = 0
        found = False
        for line in f:
            if "starting mobility" in line:
                found = True
            elif counter < 100 and found is True:
                outputResults.append(line)
                counter += 1

    with open(fileWithResults, "a+") as f:
        for line in outputResults:
            f.write(str(line))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print "Please as first argument file with iperf output"
