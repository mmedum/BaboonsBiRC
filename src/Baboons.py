from argparse import ArgumentParser
from itertools import islice
import os.path
import csv
import collections


def is_valid_file(parser, file):
    if not os.path.isfile(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return file


def accumulatePoly(baboon1, baboon2, baboon3, values):
    if baboon1 == 2:
        values["nrOfPolyType1"] += 1
    if baboon2 == 2:
        values["nrOfPolyType2"] += 1
    if baboon3 == 2:
        values["nrOfPolyType3"] += 1
    if baboon1 == 2 and baboon2 == 2:
        values["nrOfPolyType1And2"] += 1
    if baboon1 == 2 and baboon2 == 2:
        values["nrOfPolyType1And3"] += 1
    if baboon2 == 2 and baboon3 == 2:
        values["nrOfPolyType2And3"] += 1


def accumulateState(baboon1, baboon2, baboon3, values):
    if baboon1 == 0 and baboon2 == 1 and baboon3 == 1:
        values["nrOfStateA"] += 1
    elif baboon1 == 1 and baboon2 == 0 and baboon3 == 1:
        values["nrOfStateB"] += 1
    elif baboon1 == 1 and baboon2 == 1 and baboon3 == 0:
        values["nrOfStateC"] += 1


def setupKeys(orDict):
    # Number of lines read for a
    # specific Chromosome
    orDict["nrOfLines"] = 0

    # State variables
    # states A(011), B(101), C(110)
    orDict["nrOfStateA"] = 0
    orDict["nrOfStateB"] = 0
    orDict["nrOfStateC"] = 0

    # State changed variables
    orDict["stateAToA"] = 0
    orDict["stateBToB"] = 0
    orDict["stateCToC"] = 0
    orDict["stateAToB"] = 0
    orDict["stateAToC"] = 0
    orDict["stateBToA"] = 0
    orDict["stateBToC"] = 0
    orDict["stateCToA"] = 0
    orDict["stateCToB"] = 0

    # Polymorph types
    orDict["nrOfPolyType1"] = 0
    orDict["nrOfPolyType2"] = 0
    orDict["nrOfPolyType3"] = 0
    orDict["nrOfPolyType1And2"] = 0
    orDict["nrOfPolyType1And3"] = 0
    orDict["nrOfPolyType2And3"] = 0


def outputToFile(currentChromosome, orDict, outFile):
    # Output current chromosome and data
    outFile.write("\n")
    outFile.write(str(currentChromosome))
    outFile.write("\t")

    for value in orDict.values():
        outFile.write(str(value))
        outFile.write("\t")


def main():
    # Set arguments for the program
    parser = ArgumentParser(description="Argument parser for baboons.")
    parser.add_argument("-file", dest="filename", required=True,
                        help="Input file with baboon data", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-s", dest="slice", required=True, nargs=2,
                        help="Number of lines to look at, start - finish",
                        metavar="SLICE", type=int)
    parser.add_argument("-b", dest="baboons", required=True, nargs=3,
                        help="Input selected baboon species",
                        metavar="BABOON", type=str)
    # Parse the arguments
    args = parser.parse_args()

    # Slice
    start = args.slice[0]
    finish = args.slice[1]

    # Save the three input species
    baboon1 = args.baboons[0]
    baboon2 = args.baboons[1]
    baboon3 = args.baboons[2]

    # Current Chromosome, assumming starting with 1
    currentChromosome = "1"

    # Create dictionary reader
    # Perform calculations
    with open(args.filename) as patterns, open('output.txt', 'a') as out:
        reader = csv.DictReader(patterns, delimiter="\t")
        next(reader)  # skip fieldnames

        # Setup ordered map for holding results
        # for each chromosome before writing
        # them to out file
        orDict = collections.OrderedDict()
        setupKeys(orDict)

        # Output fieldnames and tab seperate them
        out.write("Chromosome\t")
        for key in orDict.keys():
            out.write(key)
            out.write("\t")

        for row in islice(reader, start, finish):
            orDict["nrOfLines"] += 1
            if row["Chromosome"] != currentChromosome:
                outputToFile(currentChromosome, orDict, out)
                orDict.clear()
                setupKeys(orDict)
                currentChromosome = row["Chromosome"]
            else:
                currentBaboon1 = int(row[baboon1])
                currentBaboon2 = int(row[baboon2])
                currentBaboon3 = int(row[baboon3])

                accumulateState(currentBaboon1, currentBaboon2,
                                currentBaboon3, orDict)

                accumulatePoly(currentBaboon1, currentBaboon2,
                               currentBaboon3, orDict)

        outputToFile(currentChromosome, orDict, out)

if __name__ == "__main__":
    main()
