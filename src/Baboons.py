def is_valid_file(parser, file):
    if not os.path.isfile(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return file

if __name__ == "__main__":
    from argparse import ArgumentParser
    import os.path
    import csv

    # Set arguments for the program
    parser = ArgumentParser(description="Argument parser for baboons.")
    parser.add_argument("-file", dest="filename", required=True,
                        help="Input file with baboon data", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    # Parse the arguments
    args = parser.parse_args()

    # Create dictionary reader
    with open(args.filename) as patterns:
        reader = csv.DictReader(patterns, delimiter="\t")
        for row in reader:
            print(row["Chromosome"])
