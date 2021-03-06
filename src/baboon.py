from argparse import ArgumentParser
import os.path
import csv
import collections
import random


def is_valid_file(parser, file):
    if not os.path.isfile(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return file


def accumulate_poly(baboon1, baboon2, baboon3, checkValue, values):
    if baboon1 == checkValue:
        values["nrOfPolyType1"] += 1
    if baboon2 == checkValue:
        values["nrOfPolyType2"] += 1
    if baboon3 == checkValue:
        values["nrOfPolyType3"] += 1
    if baboon1 == checkValue and baboon2 == checkValue:
        values["nrOfPolyType1And2"] += 1
    if baboon1 == checkValue and baboon3 == checkValue:
        values["nrOfPolyType1And3"] += 1
    if baboon2 == checkValue and baboon3 == checkValue:
        values["nrOfPolyType2And3"] += 1


def accumulate_state(baboon1, baboon2, baboon3, currentState, values):
    if baboon1 == 0 and baboon2 == 1 and baboon3 == 1:
        values["nrOfStateA"] += 1
        return 1, True
    elif baboon1 == 1 and baboon2 == 0 and baboon3 == 1:
        values["nrOfStateB"] += 1
        return 2, True
    elif baboon1 == 1 and baboon2 == 1 and baboon3 == 0:
        values["nrOfStateC"] += 1
        return 3, True
    else:
        return 0, False


def accumulate_type_not_zero(baboon1, baboon2, baboon3, values):
    if baboon1 > 0 or baboon2 > 0 or baboon3 > 0:
        values["typeNotZero"] += 1


def accumulate_state_changed(lastState, currentState, values):
    if lastState == 0:
        return currentState
    if lastState == 1 and currentState == 1:
        values["stateAToA"] += 1
        return 1
    if lastState == 1 and currentState == 2:
        values["stateAToB"] += 1
        return 2
    if lastState == 1 and currentState == 3:
        values["stateAToC"] += 1
        return 3
    if lastState == 2 and currentState == 2:
        values["stateBToB"] += 1
        return 2
    if lastState == 2 and currentState == 1:
        values["stateBToA"] += 1
        return 1
    if lastState == 2 and currentState == 3:
        values["stateBToC"] += 1
        return 3
    if lastState == 3 and currentState == 3:
        values["stateCToC"] += 1
        return 3
    if lastState == 3 and currentState == 1:
        values["stateCToA"] += 1
        return 1
    if lastState == 3 and currentState == 2:
        values["stateCToB"] += 1
        return 2


def reencode(baboon):
    if baboon == 0:
        return 0
    if baboon == 1:
        return random.randint(0, 1)
    if baboon == 2:
        return 1


def setup_keys(orDict):
    orDict.clear()
    # Number of lines read for a
    # specific Chromosome
    orDict["startPosition"] = 0
    orDict["endPosition"] = 0
    orDict["typeNotZero"] = 0

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


def output_to_file(currentChromosome, orDict, outFile):
    # Output current chromosome and data
    outFile.write("\n")
    outFile.write(str(currentChromosome))
    outFile.write("\t")

    for value in orDict.values():
        outFile.write(str(value))
        outFile.write("\t")


def main():
    # Seed the random generator
    random.seed(None)
    # Set arguments for the program
    parser = ArgumentParser(description="Argument parser for baboons.")
    parser.add_argument("-input", dest="input", required=True,
                        help="Input file with baboon data", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-out", dest="output", required=True,
                        help="Where to place output file", metavar="FILE")
    parser.add_argument("-s", dest="slice", required=True,
                        help="The slice for for each Chromosome",
                        metavar="SLICE", type=int)
    parser.add_argument("-b", dest="baboons", required=True, nargs=3,
                        help="Input selected baboon species",
                        metavar="BABOON", type=str)
    parser.add_argument("-reencode", action="store_true",
                        help="Input if file should be reencoded before use")
    # Parse the arguments
    args = parser.parse_args()

    # Slice
    windowSlice = args.slice

    # Reencode
    # Set standard polymorphic check value
    shouldReencode = args.reencode
    poly_checkvalue = 1 if shouldReencode else 2

    # Save the three input species
    baboon1 = args.baboons[0]
    baboon2 = args.baboons[1]
    baboon3 = args.baboons[2]

    # Create dictionary reader
    # Perform calculations
    with open(args.input) as patterns, open(args.output, 'a') as out:
        reader = csv.DictReader(patterns, delimiter="\t")

        # Setup ordered map for holding results
        # for each chromosome before writing
        # them to out file
        orDict = collections.OrderedDict()
        setup_keys(orDict)

        # Current Chromosome, assumming starting with 1
        currentChromosome = "1"

        # No state = 0
        # A state (011) = 1
        # B state (101) = 2
        # C state (110) = 3
        lastState = 0
        currentState = 0

        # Output fieldnames and tab seperate them
        out.write("Chromosome\t")
        for key in orDict.keys():
            out.write(key)
            out.write("\t")

        shouldSetStartPosition = True
        startPosition = -1

        for row in reader:
            if shouldSetStartPosition:
                startPosition = int(row["Position"])
                orDict["startPosition"] = startPosition
                shouldSetStartPosition = False
            if row["Chromosome"] != currentChromosome or (int(row["Position"]) - startPosition) >= windowSlice:
                orDict["endPosition"] = row["Position"]
                output_to_file(currentChromosome, orDict, out)
                setup_keys(orDict)
                currentChromosome = row["Chromosome"]
                lastState = 0
                currentState = 0
                orDict["startPosition"] = row["Position"]

            currentBaboon1 = int(row[baboon1])
            currentBaboon2 = int(row[baboon2])
            currentBaboon3 = int(row[baboon3])

            accumulate_poly(currentBaboon1, currentBaboon2,
                            currentBaboon3, poly_checkvalue, orDict)

            if(shouldReencode):
                currentBaboon1 = reencode(currentBaboon1)
                currentBaboon2 = reencode(currentBaboon2)
                currentBaboon3 = reencode(currentBaboon3)

            accumulate_type_not_zero(currentBaboon1, currentBaboon2,
                                     currentBaboon2, orDict)

            currentState, stateChanged = accumulate_state(currentBaboon1,
                                                          currentBaboon2,
                                                          currentBaboon3,
                                                          currentState,
                                                          orDict)

            if stateChanged:
                lastState = accumulate_state_changed(lastState,
                                                     currentState, orDict)

        # If shouldSetStartPosition is true, we are done with the file
        if not shouldSetStartPosition:
            orDict["endPosition"] = row["Position"]
            output_to_file(currentChromosome, orDict, out)


if __name__ == "__main__":
    main()
