from argparse import ArgumentParser
from itertools import islice
import os.path
import csv


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


def setupValues(values):
    # State variables
    # states A(011), B(101), C(110)
    values["nrOfStateA"] = 0
    values["nrOfStateB"] = 0
    values["nrOfStateC"] = 0

    # State changed variables
    values["stateAToA"] = 0
    values["stateBToB"] = 0
    values["stateCToC"] = 0
    values["stateAToB"] = 0
    values["stateAToC"] = 0
    values["stateBToA"] = 0
    values["stateBToC"] = 0
    values["stateCToA"] = 0
    values["stateCToB"] = 0

    # Polymorph types
    values["nrOfPolyType1"] = 0
    values["nrOfPolyType2"] = 0
    values["nrOfPolyType3"] = 0
    values["nrOfPolyType1And2"] = 0
    values["nrOfPolyType1And3"] = 0
    values["nrOfPolyType2And3"] = 0

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

    values = {}
    setupValues(values)

    # Create dictionary reader
    # Perform calculations
    with open(args.filename) as patterns:
        reader = csv.DictReader(patterns, delimiter="\t")
        for row in islice(reader, start, finish):

            currentBaboon1 = int(row[baboon1])
            currentBaboon2 = int(row[baboon2])
            currentBaboon3 = int(row[baboon3])

            print(currentBaboon1, currentBaboon2, currentBaboon3)

            accumulateState(currentBaboon1, currentBaboon2,
                            currentBaboon3, values)

            accumulatePoly(currentBaboon1, currentBaboon2,
                           currentBaboon3, values)

    output = ("#StateA: {}, #StateB: {}, #StateC: {}"
              "\n#PolyType1: {}, #PolyType2: {}, #PolyType3: {}"
              "\n#PolyType1And2: {}, #PolyType1And3: {}, #PolyType2And3: {}").format(
                  values["nrOfStateA"], values["nrOfStateB"], values["nrOfStateC"],
                  values["nrOfPolyType1"], values["nrOfPolyType2"],
                  values["nrOfPolyType3"], values["nrOfPolyType1And2"],
                  values["nrOfPolyType1And3"], values["nrOfPolyType2And3"])
    print(output)

if __name__ == "__main__":
    main()
