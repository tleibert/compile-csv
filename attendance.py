#! /usr/bin/env python3
"""
This program intakes a list of files formatted as so:
Student Name, PVMA member? ANS member?, 5:40 attendance?, 6:15 attendance?, VetPAC member

? denotes a boolean, where false columns are empty and true columns are not

It then determines if students were present in both attendances, and if they weren't
prints a * next to their name in the output. It 'or's all columns with their counterparts
in the other sheets.
"""
import glob
import sys
import csv


def load_and_process_files(files):
    """
    Loads the input csv files by filename
    organizing by student name, and converting
    empty columns to False and full columns to True.
    """
    name_rows = {}
    for file in files:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name = row[0].lower().strip()
                if name in name_rows:
                    bool_row = [string != "" for string in row[1:]]
                    name_rows[name][1] = [
                        a or b for a, b in zip(name_rows[name][1], bool_row)
                    ]
                else:
                    name_rows[name] = [
                        row[0].strip(),
                        [string != "" for string in row[1:]],
                    ]

    # remove header row
    name_rows.pop("name")
    return name_rows


def write_compiled_csv(data, filename, write_order):
    """
    Writes the data in the following format
    Student Name (optional *), PVMA member?, ANS club member? vetpac member?
    Prints a * next to student name if not present at both attendance blocs
    """
    with open(filename, "w") as outfile:
        outfile.write("Name, PVMA?, ANS Club?, VetPAC,\n")
        for key in write_order:
            row = data[key]

            boollist = row[1]

            five40 = boollist[2]
            six15 = boollist[3]
            name = row[0]
            if not (five40 and six15):
                name = name + "*"

            pvma = "x" if boollist[0] else ""
            ans_club = "x" if boollist[1] else ""
            vet_pac = "x" if boollist[4] else ""

            outfile.write(f"{name},{pvma},{ans_club},{vet_pac},\n")


def write_pvma_and_ans_lists(data, filename, write_order):
    """
    Writes two lists to a csv file:
        list of all members of PVMA
        list of all members of VetPac
    """
    with open(filename, "w") as outfile:
        outfile.write("PVMA List\n")
        for name in write_order:
            if data[name][1][0]:
                outfile.write(data[name][0] + "\n")
        outfile.write("\nANS Club List\n")
        for name in write_order:
            if data[name][1][1]:
                outfile.write(data[name][0] + "\n")


def main():
    """
    Retrieves the two output file names, or sets them to default
    vals if they aren't found.
    """
    compiled_file = "output.csv"
    list_file = "pvma_or_ans.csv"

    if len(sys.argv) == 3:
        compiled_file = sys.argv[1]
        list_file = sys.argv[2]
    elif len(sys.argv) != 1:
        sys.exit("Please give two arguments if you wish to specify output file names")

    infiles = glob.glob("*.csv")
    if compiled_file in infiles:
        infiles.remove(compiled_file)
    if list_file in infiles:
        infiles.remove(list_file)

    data = load_and_process_files(infiles)
    write_order = sorted(data.keys())
    write_compiled_csv(data, compiled_file, write_order)
    write_pvma_and_ans_lists(data, list_file, write_order)


if __name__ == "__main__":
    main()
