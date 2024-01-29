# Author: Anthony Nguyen
from datetime import datetime
from wguRouting.router.DeliveryRouter import DeliveryRouter
from wguRouting.router.reader import processCsv
from wguRouting.router.HashTable import HashTable
from wguRouting.classes.Package import Package
from wguRouting.classes.Truck import Truck
from wguRouting.ui.CommandLineInterface import CommandLineInterface
from wguRouting.classes.Status import Status

ui = CommandLineInterface()

# Convert CSV into a array list
addressList = processCsv("wguRouting/data/address_cleaned.csv")
distanceList = processCsv("wguRouting/data/distance_table_cleaned.csv")
packagesList = processCsv("wguRouting/data/packages_cleaned.csv")

# Create Hash table and load package objects with id keys.
packageTable = HashTable(int(len(packagesList) / 2))

router = DeliveryRouter(packageTable, distanceList, addressList)
start = "4001 South 700 East"

# Create truck instances all begininning at hub
# Trucks are manually loaded based on package requirements. Packaged that are going to same location are grouped onto the same truck for efficiency.
# Truck 1 = Mainly used for priority packages with deadlines
# Truck 2 and 3 for packages arriving late
# EOD packages are loaded into trucks by most efficiency
truck1 = Truck(1, start, "8:00 am")
truck2 = Truck(2, start, "10:20 am")
truck3 = Truck(3, start, "9:05 am")

truck1.route = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck2.route = [3, 6, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
truck3.route = [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33]

endOfDay = datetime.strptime("11:59 pm", "%I:%M %p")


# Create package instances from list and stores into the hash table
def loadPackageData(list, table):
    for obj in list:
        p = Package(int(obj[0]), obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7])
        table.insert(p.id, p)


loadPackageData(packagesList, packageTable)


# Prints out the Main page and options. Includes logic for user input.
# Continuously loops until exit code or different page is requested by user
# Initial page trucks are only manually loaded and routes have not bean generated.
# Welcome page allows for search and viewing of packages and trucks before routes are processed and delivery  day begins
def welcomePage():
    while True:
        ui.welcomePage()
        userInput = input()
        if userInput == "1":
            loadPackagePage()
        elif userInput == "2":
            loadTrucksPage()

        # Starts the route generation process and trucks are reloaded with routes using nearest neighbor algorithm.
        # Pulls up the delivery page where can check package status and truck distances.
        elif userInput == "3":
            print("Truck 1 Route:")
            router.generateRoute(truck1)

            print("\nTruck 2 Route:")
            router.generateRoute(truck2)

            # Check to see which truck out of the first 2 with drivers would return first and switch drivers.
            t1 = datetime.strptime(truck1.timeReturn, "%I:%M %p")
            t2 = datetime.strptime(truck2.timeReturn, "%I:%M %p")
            if t1 < t2:
                switchDriver(truck1, truck3)
            else:
                switchDriver(truck2, truck3)

            print("\nTruck 3 Route:")
            router.generateRoute(truck3)

            ui.printSuccess("Packages have been loaded. Ready to begin deliveries.")
            input("Press enter to continue")
            loadSimulationPage()

        # Exit the program
        elif userInput == "4":
            print("Exiting Program. Goodbye!")
            break
        else:
            ui.printError("Please choose valid choice 1-4")


# Prints out the package page and options. Includes logic for user input.
# Continuously loops until exit code or different page is requested by user
def loadPackagePage():
    while True:
        ui.packagePage()
        userInput = input()
        if (
            userInput == "1"
        ):  # Print out package details for specific package. Loops until user is done searching.
            print("\nSearch for a package or q to stop")
            while True:
                search = input("\nEnter Id >>> ")
                if search == "q":
                    break
                try:
                    search = int(search)
                    output = packageTable.lookup(search)
                    if output is not None:
                        ui.printSuccess(output)
                    else:
                        ui.printError(f"Package {search} was not found")
                except ValueError:
                    ui.printError("Enter a valid integer or 'q' to quite")

        elif userInput == "2":  # Print list of all packages
            printAllPackages(packagesList)
            input("\nPress enter to clear")
        elif (
            userInput == "3"
        ):  # End page loop and navigate back to welcome page while loop
            break
        else:
            ui.printError("Please choose valid choice 1-4")
    return


def loadTrucksPage():
    while True:
        ui.trucksPage()
        userInput = input()
        if userInput == "1":
            print(truck1)
            print(truck2)
            print(truck3)
            input("\nPress enter to clear")
        elif userInput == "2":
            pass
        elif userInput == "3":
            break
        else:
            ui.printError("Please choose valid choice 1-4")
    return


def loadSimulationPage():
    totalMileage = truck1.distance + truck2.distance + truck3.distance
    ui.simulationPage(totalMileage)
    while True:
        userInput = input()

        # Run trucks and deliveries throughout the whole day
        if userInput == "1":
            checkPackagesAtTime(endOfDay)
            input("Enter to clear")
            loadSimulationPage()

        # Check package status at specific times
        elif userInput == "2":
            while True:
                checkedTime = input(
                    "Enter a time you would like to view in format HH:MM am: "
                )
                try:
                    checkedTimeObj = datetime.strptime(checkedTime, "%I:%M %p")
                    while True:
                        userInput = input(
                            "\nEnter id to search for specific package or hit enter for a list of all packages or q to exit time mode "
                        )
                        print(totalMileage)
                        print(f"Current Time is {checkedTime}")
                        if userInput == "q":
                            break
                        elif userInput != "":
                            checkPackagesAtTime(checkedTimeObj, userInput)
                        else:
                            checkPackagesAtTime(checkedTimeObj)

                    # break out of time loop clear terminal and go back to delivery simulation screen
                    loadSimulationPage()
                    break
                except ValueError as e:
                    print(f"ValueError: {e}")

        # Get truck locations at certain times
        elif userInput == "3":
            pass

        # End program
        elif userInput == "4":
            print("Exiting Program. Goodbye!")
            exit()
        else:
            ui.printError("Please choose valid choice 1-4")


# Print all the packages and change output color of packages based on the status
# O(n)
def printAllPackages(packageList):
    print("All Packages List: ")
    for i in range(len(packageList)):
        p = packageTable.lookup(i + 1)
        statusColorPrint(p)


# Print the packages for specific trucks and change color based on package status
# O(n)
def printTruckPackages(truck):
    print(f"\nTruck {truck.id}, Miles Traveled: {truck.distance}")
    for package in truck.route:
        p = packageTable.lookup(package)
        statusColorPrint(p)


# Test colors for status (AT_HUB = red, DELIVERED = green, ENROUTE = yellow)
def statusColorPrint(p):
    if p.status == Status.AT_HUB:
        ui.printError(p)
    elif p.status == Status.DELIVERED:
        result = str(p) + ", Time Delivered: " + p.timeDelivered
        ui.printSuccess(result)
    elif p.status == Status.ENROUTE:
        ui.printNeutral(p)


# Calculates the status based on the delivery time prints color based on status.
# If no search id is given will update all packages and print all.
# If search id is given will update only that one and print it out.
# O(n) for checking packages of all
# O(1) for single search package
def checkPackagesAtTime(time, searchId=None):
    startRoutes(time, truck1)
    startRoutes(time, truck2)
    startRoutes(time, truck3)

    if searchId is None:
        for i in range(len(packagesList)):
            p = packageTable.lookup(i + 1)
            p.updateStatus(time)
            # statusColorPrint(p)
        printTruckPackages(truck1)
        printTruckPackages(truck2)
        printTruckPackages(truck3)
    else:
        try:
            search = int(searchId)
            p = packageTable.lookup(search)
            if p is not None:
                p.updateStatus(time)
                statusColorPrint(p)
            else:
                ui.printError(f"Package {search} was not found")
        except ValueError:
            ui.printError("Enter a valid integer or 'q' to quite")


# Function switches the driver appends distance home to total distance of truck route of returning truck.
# Other truck departs only when truck first returns
def switchDriver(truckDone, truckOn):
    truckDone.distance += truckDone.distanceHome
    truckOn.earliestDeparture = truckDone.timeReturn


def startRoutes(time, truck):
    # First reset all packages to AT_HUB in case already been ran before
    for packageId in truck.route:
        p = packageTable.lookup(packageId)
        p.status = Status.AT_HUB
    startTime = datetime.strptime(truck.earliestDeparture, "%I:%M %p")
    # time = datetime.strptime(time, "%I:%M %p")
    if startTime < time:
        for packageId in truck.route:
            p = packageTable.lookup(packageId)
            p.status = Status.ENROUTE


def main():
    loadPackageData(packagesList, packageTable)
    welcomePage()


if __name__ == "__main__":
    main()
