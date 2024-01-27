from wguRouting.classes.Truck import Truck
from datetime import datetime, timedelta


class DeliveryRouter:
    def __init__(self, hashTable, distanceMatrix, addressList):
        self.hashTable = hashTable
        self.distanceMatrix = distanceMatrix
        self.addressList = addressList

    # Locations arrays such as (currentLocation, unvisited) are stored in a 2d array [packageId][addresssIndex] for easy referencing between id and locations
    # Greedy algorithm using nearest neighbor from list of loaded packages.
    # Worst Case performance O(N^2)
    # Input: Truck
    # Output: Truck.route in order from closest, and truck.distance.
    def generateRoute(self, truck):
        currentTime = truck.earliestDeparture
        unvisited = []
        truckRouteStr = truck.currentLocation + " --> "

        # Zero is placeholder for no package because at start
        currentLocation = [0, self.getAddressIndex(truck.currentLocation)]
        route = []

        # Copy over packages and there address index to unvisited[[packageId][addressIndex]]
        # O(n). Trucks are already loaded with at most 16 packages because of max capacity. So could be considered O(1) because constant size.
        for packageId in truck.route:
            # package search by id O(1)
            p = self.hashTable.lookup(packageId)
            address = p.address
            # get address index O(n)
            addrIndex = self.getAddressIndex(address)
            unvisited.append([p, addrIndex])
        truck.route.clear()  # empties route for loading in order by greedy algorithm

        # Loops until univisited is all loaded back into routes
        # Overall O(N^2) while loop slowest part.
        while unvisited:
            # Returns package with the shortest distance form current location node.
            # O(N)
            nextLocation = min(
                unvisited,
                key=lambda x: self.getDistanceBetween(currentLocation[1], x[1]),
            )

            # Reloads package back into truck and adds distance
            distance = self.getDistanceBetween(currentLocation[1], nextLocation[1])
            truck.loadPackage(nextLocation[0].id)
            truck.distance += distance
            route.append(nextLocation[0].id)

            # Output route order to terminal
            truckRouteStr += self.addressList[nextLocation[1]][2] + " --> "

            # Calculate arrival time to destination and updates package expected delivery time. Current time is then set for next iteration.
            deliveryTime = self.calcDeliveryTime(currentTime, distance, truck.speed)
            nextLocation[0].timeDelivered = deliveryTime
            currentTime = deliveryTime

            # Mark location as as visited and set the new current location for next iteration.
            unvisited.remove(nextLocation)
            currentLocation = nextLocation

            if len(unvisited) < 1:
                distanceHome = self.getDistanceBetween(currentLocation[1], 0)
                timeHome = self.calcDeliveryTime(currentTime, distanceHome, truck.speed)
                truck.distanceHome = distanceHome
                truck.timeReturn = timeHome

        print(f"{truckRouteStr}\n")
        # print(f"package delivery order {route}")
        # print(truck.distance)

    # Find the distance between two points using the distance csv. Input: 2 points, Output: float of miles.
    # Since row and column are interchangeable flip if empty to save time iterating over complete list
    # BigO = O(1)
    def getDistanceBetween(self, current, destination):
        distance = self.distanceMatrix[current][destination]
        if distance == "":
            distance = self.distanceMatrix[destination][current]
        return float(distance)

    # Helper function to return the id of each address. Checks for match of string address search. Returns index for use with distanceTable.
    # Iterates through list of addresss looking for match.
    # BigO = O(n)
    def getAddressIndex(self, search):
        for address in self.addressList:
            if search in address[2]:
                return int(address[0])

    # Calculates time it takes from point A to B using distance traveled and speed. Adds travel time to b to time left point A.
    # Output: Arrival time at point B as str.
    def calcDeliveryTime(self, departureTime, distance, speed):
        departureTime = datetime.strptime(departureTime, "%I:%M %p")
        travelTime = timedelta(hours=distance / speed)
        deliveryTime = (departureTime + travelTime).strftime("%I:%M %p")

        return deliveryTime
