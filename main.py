# Author: Anthony Nguyen
from wguRouting.router.reader import processCsv
from wguRouting.router.HashTable import HashTable
from wguRouting.classes.Package import Package
from wguRouting.classes.Truck import Truck

# from wguRouting.router.testAlgo import helloFrom


# Create package objs from list and stores into the hash table
def loadPackageData(list, table):
    for obj in list:
        p = Package(int(obj[0]), obj[1], obj[2], obj[3], obj[4], obj[5], obj[6])
        table.insert(p.id, p)
    table.display()


def main():
    # Convert CSV into a array list
    addressList = processCsv("wguRouting/data/address_cleaned.csv")
    distanceList = processCsv("wguRouting/data/distance_table_cleaned.csv")
    packagesList = processCsv("wguRouting/data/packages_cleaned.csv")

    packageTable = HashTable(int(len(packagesList) / 2))
    loadPackageData(packagesList, packageTable)

    print(packageTable.lookup(10))


if __name__ == "__main__":
    main()
