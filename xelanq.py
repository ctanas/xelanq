"""XElanQ v0.1a."""

#  Python script for creating a CSV file from an output generated by
#  the software of Perkin Elmer Elan DRC II Inductively Coupled
#  Plasma Mass Spectrometer (ICP-MS).

#  Currently only works for (certain types of) TotalQuant report files.

import os
import sys

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
# Weekdays are used as anchor, for guiding our search withint the file;

elements = ["", "", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg",
                "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V",
                "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
                "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Ru",
                "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
                "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb",
                "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re",
                "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Th", "U"]

# All the chemical elements present in the output file;
# There's two placeholders: in the first position,
# for matching the elements list on the fist column;
# and in the second position for analysis date

isotopes = ["Li,7", "Be,9", "B,11", "C,12", "N,14", "O,16", "F,19", "Ne,20",
            "Na,23", "Mg,24", "Al,27", "Si,28", "P,31", "S,32", "Cl,35",
            "K,39", "Ar,40", "Ca,40", "Sc,45", "Ti,48", "V,51", "Cr,52",
            "Mn,55", "Fe,56", "Fe,57", "Co,59", "Ni,59", "Ni,60", "Cu,64",
            "Cu,63", "Zn,65", "Zn,66", "Ga,70", "Ge,73", "As,75", "Se,79",
            "Br,80", "Kr,84", "Rb,85", "Sr,88", "Y,89", "Zr,91", "Nb,93",
            "Mo,96", "Ru,101", "Rh,103", "Pd,106", "Ag,108", "Ag,107",
            "Cd,112", "Cd,111" "In,115", "Sn,119", "Sb,122", "Te,128",
            "I,127", "Xe,131", "Cs,133", "Ba,137", "La,139", "Ce,140",
            "Pr,141", "Nd,144", "Pm,145", "Sm,150", "Eu,152", "Gd,157",
            "Tb,159", "Dy,163", "Ho,165", "Er,167", "Tm,169", "Yb,173",
            "Lu,175", "Hf,178", "Ta,181", "W,184", "Re,186", "Os,190",
            "Ir,192", "Pt,195", "Au,197", "Hg,201", "Tl,204", "Pb,207",
            "Pb,208", "Bi,209", "Th,232", "U,238", "AsO,91"]

# Isotopes list must have more elements (TO-DO).
# Used for matching search items in Quantitative mode.

# Finding the .rep file in current directory;
asps = []
asps.append("EXIT")
for root, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith('.rep'):
            asps.append(file)
for i in range(0, len(asps)):
    print i, ":", asps[i]
print len(asps), "file detected"
xx = input('Which file? ')
if (xx == 0) or (xx not in range(0, len(asps))):
    sys.exit()

repfilename = str(asps[int(xx)])
# .rep file that will be processed;

csvfilename = repfilename.split('.')[0].rstrip()+".csv"
# Output file (no need for this to be editable);
# Just changed the extension from .rep to .csv;

filetype = "NotDefined"

print "Loading and processing file, please wait..."

with open(repfilename, 'r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]

for i in range(0, len(content)):
    for j in range(0, len(isotopes)):
        if ((content[i].split(',')[0].rstrip() == "U") and
           (content[i-1].split(',')[0].rstrip() == "Th")):
                filetype = "TQ"
        elif (isotopes[j] in content[i]):
                filetype = "CC"

print "File type seems to be:", filetype

if (filetype == "NotDefined"):
    print "File not recognized, sorry"
    sys.exit(0)


def TotalQuantGO():
    """Deal with TotalQuant report files."""
    el_exception = ["C", "N", "O", "F", "Ne", "P",
                    "S", "Cl", "Ar", "Kr", "Xe"]
    # elements we don't want in the output file
    # since they have no meaning for ICP-MS;

    c_sample = 0  # sample counter, it's initialized to zero;

    # Opening the file and reading its content to an array;

    with open(repfilename, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    for i in range(0, len(content)):
        if (weekdays[0] in content[i]) or (weekdays[1] in content[i]) or \
           (weekdays[2] in content[i]) or (weekdays[3] in content[i]) or \
           (weekdays[4] in content[i]) or (weekdays[5] in content[i]) or \
           (weekdays[6] in content[i]):
            c_sample = c_sample+1

    w, h = len(elements), c_sample
    sample = [[0 for x in range(w)] for y in range(h)]
    # Initialization of the array containing the data based on
    # number of samples present in the file and the
    # number of elements detected;

    for i in range(0, len(content)):
        if (weekdays[0] in content[i]) or (weekdays[1] in content[i]) or \
           (weekdays[2] in content[i]) or (weekdays[3] in content[i]) or \
           (weekdays[4] in content[i]) or (weekdays[5] in content[i]) or \
           (weekdays[6] in content[i]):
            for j in range(1, 30):
                if ((content[i+j].split(',')[0].rstrip() == "Li") and
                   (content[i+j+1].split(',')[0].rstrip() == "Be")):
                    break
    gap1 = j
    # The gap between the date and the first value for Li;
    # This is needed to know where to start reading the concentration values;

    c_sample = 0  # reseting the counter, it's needed again;

    for i in range(0, len(content)):
        if (weekdays[0] in content[i]) or (weekdays[1] in content[i]) or \
           (weekdays[2] in content[i]) or (weekdays[3] in content[i]) or \
           (weekdays[4] in content[i]) or (weekdays[5] in content[i]) or \
           (weekdays[6] in content[i]):
            sample[c_sample][0] = content[i-1]
            sample[c_sample][1] = content[i].split(',', 1)[1]
            # the index 0 will hold the sample code,
            # the concentration follows from index 1 onwards;

            for j in range(2, len(elements)):
                temp_sample = content[i+gap1+j-2].split(',')[1].rstrip()
                try:
                    temp_value = float(temp_sample)
                    if (temp_value < 100):
                        sample[c_sample][j] = str(round(temp_value, 1))
                    if (temp_value >= 100):
                        sample[c_sample][j] = str(int(temp_value))
                except ValueError:  # if there's an error,
                                    # then we don't apply rounding;
                    sample[c_sample][j] = temp_sample
                    # Getting the concentration value from the file,
                    # cps detector values and other info are discarded;
                    # Then it rounds the values >100 ppb to no decimal,
                    # and it rounds to one decimal for values <100ppb;
            c_sample = c_sample+1

    print "Processed", c_sample, "samples in", len(content), "lines."

    # Writing the output file;
    file = open(csvfilename, "w")
    for j in range(0, len(elements)):
        if (elements[j] in el_exception):
            continue
        # Skipping the elements that make no sense;
        for k in range(0, c_sample):
            if k == 0:
                file.write(elements[j])
                file.write(";")
            file.write(sample[k][j])
            file.write(";")
        file.write("\n")
    file.close()


def QuantitativeGO():
    """Deal with Quantitative report files."""
    print "Not yet implemented!"
    print "Debug purposes only!"

    c_sample = 0  # Yet another reset;

    with open(repfilename, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    for i in range(0, len(content)):
        if (weekdays[0] in content[i]) or (weekdays[1] in content[i]) or \
           (weekdays[2] in content[i]) or (weekdays[3] in content[i]) or \
           (weekdays[4] in content[i]) or (weekdays[5] in content[i]) or \
           (weekdays[6] in content[i]):
            c_sample = c_sample+1

    # w, h = len(isotopes), c_sample
    w, h = 10000, 10000
    s_index = 0
    sample = [[0 for x in range(w)] for y in range(h)]
    for i in range(0, len(content)):
        if (weekdays[0] in content[i]) or (weekdays[1] in content[i]) or \
           (weekdays[2] in content[i]) or (weekdays[3] in content[i]) or \
           (weekdays[4] in content[i]) or (weekdays[5] in content[i]) or \
           (weekdays[6] in content[i]):
            sample[s_index][0] = content[i-1]
            sample[s_index][1] = content[i]
            b = 3
            s_index = s_index + 1
        for j in range(0, len(isotopes)):
            if ((isotopes[j] in content[i]) and (content[i].endswith("ppb"))):
                    sample[s_index-1][b] = content[i].split(',')[1].rstrip(), \
                        content[i].split(',')[-4].rstrip()
                    sample[s_index-1][2] = b - 2
                    b = b + 1

    print "Processed", c_sample, "samples in", len(content), "lines."

    # Multiple groups (batch), based on number of elements determined
    # user will select which group to process.


if filetype == "TQ":
    TotalQuantGO()
if filetype == "CC":
    QuantitativeGO()

print "All done!"

# Changelog:
# - switched to Python 2, for compatibility with Windows XP;
# - Cleaned the code, PEP8 compliant;
# - Added date of analysis in sample concentration list
