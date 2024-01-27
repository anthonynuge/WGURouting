import os

# Print outputs for different screens and pages in the terminal.
# File also has methods for printing color text to terminial using ansi escape sequences.


class CommandLineInterface:
    def __init__(self):
        pass

    def welcomePage(self):
        page = (
            "╔════════════════════════════╗\n"
            "║     Delivery Routing       ║\n"
            "║         Program            ║\n"
            "╚════════════════════════════╝\n"
            "Welcome to WGU postal services\n"
            "\n"
            "Select a option:\n"
            "[1] View Packages\n"
            "[2] View Trucks\n"
            "[3] Load Packages\n"
            "[4] Exit\n"
        )
        clearTerm()
        print(page)

    def packagePage(self):
        page = (
            "╔════════════════════════════╗\n"
            "║          Packages          ║\n"
            "╚════════════════════════════╝\n"
            "Select a option:\n"
            "[1] Package Lookup\n"
            "[2] View All\n"
            "[3] Back\n"
        )
        clearTerm()
        print(page)

    def trucksPage(self):
        page = (
            "╔════════════════════════════╗\n"
            "║           Trucks           ║\n"
            "╚════════════════════════════╝\n"
            "Select a option:\n"
            "[1] Package Truck 1\n"
            "[2] View Truck 2\n"
            "[3] Back\n"
        )
        clearTerm()
        print(page)

    def simulationPage(self, totalMileage):
        page = (
            "╔════════════════════════════╗\n"
            "║       Ready to Deliver     ║\n"
            "╚════════════════════════════╝\n\n"
            # f"The current time is {currentTime}\n\n"
            f"Total Mileage = {totalMileage}\n\n"
            "Select a option:\n"
            "[1] Deliver All Packages\n"
            "[2] Check package status at specific time\n"
            "[3] Get truck locations at specific time\n"
            "[4] Exit program\n"
        )
        clearTerm()
        print(page)

    def printSuccess(self, message):
        print(f"\033[0;32m {message} \033[0m")

    def printError(self, message):
        print(f"\033[0;31m {message} \033[0m")

    def printNeutral(self, message):
        print(f"\033[0;33m {message} \033[0m")


def clearTerm():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
