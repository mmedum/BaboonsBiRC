from argparse import ArgumentParser
from itertools import islice
import os.path
import csv


def is_valid_file(parser, file):
    if not os.path.isfile(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return file


def accumulate_poly(baboon1, baboon2, baboon3, poly1, poly2, poly3,
                    poly1And2, poly1And3, poly2And3):
    if baboon1 == 2:
        poly1 += 1
    if baboon2 == 2:
        poly2 += 1
    if baboon3 == 2:
        poly3 += 1
    if baboon1 == 2 and baboon2 == 2:
        poly1And2 += 1
    if baboon1 == 2 and baboon2 == 2:
        poly1And3 += 1
    if baboon2 == 2 and baboon3 == 2:
        poly2And3 += 1
    return poly1, poly2, poly3, poly1And2, poly1And3, poly2And3


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

    # State variables
    # states A(011), B(101), C(110)
    nrOfStateA = 0
    nrOfstateB = 0
    nrOfstateC = 0

    # Polymorph types
    nrOfPolyType1 = 0
    nrOfPolyType2 = 0
    nrOfPolyType3 = 0
    nrOfPolyType1And2 = 0
    nrOfPolyType1And3 = 0
    nrOfPolyType2And3 = 0

    # Create dictionary reader
    # Perform calculations
    with open(args.filename) as patterns:
        reader = csv.DictReader(patterns, delimiter="\t")
        for row in islice(reader, start, finish):
            # ref = row["ref"]
            # alt = row["alt"]

            currentBaboon1 = int(row[baboon1])
            currentBaboon2 = int(row[baboon2])
            currentBaboon3 = int(row[baboon3])

            print(currentBaboon1, currentBaboon2, currentBaboon3)

            nrOfStateA, nrOfstateB, nrOfstateC = accumulate_state(
                currentBaboon1, currentBaboon2, currentBaboon3,
                nrOfStateA, nrOfstateB, nrOfstateC)

            nrOfPolyType1, nrOfPolyType2, nrOfPolyType3, nrOfPolyType1And2, nrOfPolyType1And3, nrOfPolyType2And3 = accumulate_poly(
                currentBaboon1, currentBaboon2, currentBaboon3,
                nrOfPolyType1, nrOfPolyType2, nrOfPolyType3,
                nrOfPolyType1And2, nrOfPolyType1And3, nrOfPolyType2And3)

    output = ("#StateA: {}, #StateB: {}, #StateC: {}"
              "\n#PolyType1: {}, #PolyType2: {}, #PolyType3: {}"
              "\n#PolyType1And2: {}, #PolyType1And3: {}, #PolyType2And3: {}").format(
        nrOfStateA, nrOfstateB, nrOfstateC,
        nrOfPolyType1, nrOfPolyType2, nrOfPolyType3,
        nrOfPolyType1And2, nrOfPolyType1And3, nrOfPolyType2And3)
    print(output)

if __name__ == "__main__":
    main()
