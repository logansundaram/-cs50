import csv
from sys import argv
from sys import exit


def main():

    # TODO: Check for command-line usage

    if len(argv) != 3:
        print("Missing command line argument")
        exit()

    # TODO: Read database file into a variable
    counter = 0
    database = []
    if argv[1] == "databases/large.csv":
        counter = 1
    with open(argv[1]) as file:
        reader = csv.DictReader(file)
        for data in reader:
            database.append(data)

    # TODO: Read DNA sequence file into a variable

    sequence = ""
    with open(argv[2]) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence

    person_dna = {}

    person_dna["AGATC"] = longest_match(sequence, "AGATC")
    person_dna["AATG"] = longest_match(sequence, "AATG")
    person_dna["TATC"] = longest_match(sequence, "TATC")

    if counter == 1:
        person_dna["TTTTTTCT"] = longest_match(sequence, "TTTTTTCT")
        person_dna["TCTAG"] = longest_match(sequence, "TCTAG")
        person_dna["GATA"] = longest_match(sequence, "GATA")
        person_dna["GAAA"] = longest_match(sequence, "GAAA")
        person_dna["TCTG"] = longest_match(sequence, "TCTG")

    # TODO: Check database for matching profiles

    for str in database:
        if int(str["AGATC"]) == person_dna["AGATC"] and int(str["AATG"]) == person_dna["AATG"] and int(str["TATC"]) == person_dna["TATC"]:
            if counter == 1:
                if int(str["TTTTTTCT"]) == person_dna["TTTTTTCT"] and int(str["TCTAG"]) == person_dna["TCTAG"] and int(str["GATA"]) == person_dna["GATA"] and int(str["GAAA"]) == person_dna["GAAA"] and int(str["TCTG"]) == person_dna["TCTG"]:
                    print(str["name"])
                    break
            elif counter == 0:
                print(counter)
                print(str["name"])
                break

    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
