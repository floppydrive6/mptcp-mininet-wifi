import os
import sys
import statistics


def main(argv):
    try:
        os.remove("statsResults.txt")
    except OSError:
        pass
    for file in argv[1:]:
        results = []
        with open(file, 'r') as f:
            for line in f:
                line = line.split(" ")
                results.append(float(line[1]))
        meanVal = statistics.mean(results)
        stdDevVal = statistics.stdev(results)
        meanString = "Mean value for " + file + " is: " + str(meanVal)
        stdDevString = "Standard Deviation value for " + \
            file + " is: " + str(stdDevVal)
        print meanString
        print stdDevString
        with open("statsResults.txt", "a+") as fw:
            fw.write(meanString + "\n")
            fw.write(stdDevString + "\n")


if __name__ == "__main__":
    main(sys.argv)
