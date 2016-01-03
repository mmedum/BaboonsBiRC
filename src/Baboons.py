from argparse import ArgumentParser
from itertools import islice
import os.path
import csv


def is_valid_file(parser, file):
    if not os.path.isfile(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return file


def accumulate_poly(baboon1, baboon2, baboon3, poly1, poly2, poly3):
    print("Hellow", baboon1)
    if baboon1 == 2:
        poly1 += 1
    if baboon2 == 2:
        poly2 += 1
    if baboon3 == 2:
        poly3 += 1
    return poly1, poly2, poly3


def accumulate_state(baboon1, baboon2, baboon3, stateA, stateB, stateC):
    if baboon1 == 0 and baboon2 == 1 and baboon3 == 1:
        stateA += 1
    elif baboon1 == 1 and baboon2 == 0 and baboon3 == 1:
        stateB += 1
    elif baboon1 == 1 and baboon2 == 1 and baboon3 == 0:
        stateC += 1
    return stateA, stateB, stateC


def main():
    # Set arguments for the program
    parser = ArgumentParser(description="Argument parser for baboons.")
    parser.add_argument("-file", dest="filename", required=True,
                        help="Input file with baboon data", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-slice", dest="slice", required=True,
                        help="Number of lines to look at",
                        metavar="SLICE", type=int)
    parser.add_argument("-b", dest="baboons", required=True, nargs=3,
                        help="Input selected baboon species",
                        metavar="BABOON", type=str)
    # Parse the arguments
    args = parser.parse_args()

    # Save the three input species
    baboon1 = args.baboons[0]
    baboon2 = args.baboons[1]
    baboon3 = args.baboons[2]

    # State variables
    nrOfStateA = 0
    nrOfstateB = 0
    nrOfstateC = 0

    nrOfPolyArg1 = 0
    nrOfPolyArg2 = 0
    nrOfPolyArg3 = 0

    # Create dictionary reader
    # Setup variables
    # states A(011), B(101), C(110)
    with open(args.filename) as patterns:
        reader = csv.DictReader(patterns, delimiter="\t")
        for row in islice(reader, 0, args.slice):
            # ref = row["ref"]
            # alt = row["alt"]

            currentBaboon1 = row[baboon1]
            currentBaboon2 = row[baboon2]
            currentBaboon3 = row[baboon3]

            print(currentBaboon1, currentBaboon2, currentBaboon3)

            nrOfStateA, nrOfstateB, nrOfstateC = accumulate_state(
                currentBaboon1, currentBaboon2, currentBaboon3,
                nrOfStateA, nrOfstateB, nrOfstateC)

            nrOfPolyArg1, nrOfPolyArg2, nrOfPolyArg3 = accumulate_poly(
                currentBaboon1, currentBaboon2, currentBaboon3,
                nrOfPolyArg1, nrOfPolyArg2, nrOfPolyArg3)

    output = "#StateA: {}, #StateB: {}, #StateC: {} \n #PolyArg1: {}, #PolyArg2: {}, #PolyArg3: {}".format(nrOfStateA, nrOfstateB, nrOfstateC, nrOfPolyArg1, nrOfPolyArg2, nrOfPolyArg3)
    print(output)

if __name__ == "__main__":
    main()
