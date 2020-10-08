import csv

name_rows = {}
for i in range(3):
    with open(f"attendance{i}.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0].lower().strip()
            if name in name_rows:
                new_row = [string != "" for string in row[1:]]
                name_rows[name][1] = [a or b for a, b in zip(name_rows[name][1], new_row)]
                pass
            else:
                name_rows[name] = [row[0].strip(), [string != '' for string in row[1:]]]

name_rows.pop("name")
key_list = sorted(name_rows.keys())

with open("output.csv","w") as outfile:
    outfile.write("Name, PVMA?, ANS Club?, VetPAC,\n")
    for key in key_list:
        row = name_rows[key]
        
        boollist = row[1]

        five40 = boollist[2]
        six15 = boollist[3]
        name = row[0]
        if not (five40 and six15):
            name = name + "*"
        
        boollist = row[1]
        PVMA = "x" if boollist[0] else ""
        ANS_club = "x" if boollist[1] else ""
        VetPac = "x" if boollist[4] else ""

        outfile.write(f"{name},{PVMA},{ANS_club},{VetPac},\n")

with open("pvma_or_ans.csv", "w") as outfile2:
    outfile2.write("PVMA List\n")
    for key in key_list:
        if name_rows[key][1][0]:
            outfile2.write(name_rows[key][0] + '\n')\

    outfile2.write("\nANS Club List\n")
    for key in key_list:
        if name_rows[key][1][1]:
            outfile2.write(name_rows[key][0] + '\n')

print(name_rows)