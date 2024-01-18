import csv


# Takes a csv and reads it into a string list
def processCsv(filePath):
    with open(filePath) as file:
        return list(csv.reader(file))
