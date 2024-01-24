class DeliveryRouter:
    def __init__(self, hashTable, distanceMatrix, addressList):
        self.hashTable = hashTable
        self.distanceMatrix = distanceMatrix
        self.addressList = addressList

    def generateRoute(self, packageList, start):
        unvisited = []
        currentLocation = [0, self.getAddressIndex(start)]
        route = []

        # [ 1, 2, 3] packageId
        for packageId in packageList:
            address = self.hashTable.lookup(packageId).address
            addrIndex = self.getAddressIndex(address)
            # unvisited.append(addrIndex)
            unvisited.append([packageId, addrIndex])

        print("Univisited [[packageId][addresdId]]")
        print(unvisited)

        while unvisited:
            nextLocation = min(
                unvisited,
                key=lambda x: self.getDistanceBetween(currentLocation[1], x[1]),
            )
            route.append(nextLocation[0])
            # route.append(self.addressList[nextLocation])
            # route.append(self.addressList[nextLocation][2])

            unvisited.remove(nextLocation)
            currentLocation = nextLocation

        print(f"package delivery order {route}")
        print()
        return route

    # Find the distance between two points using the distance csv. Input: 2 points, Output: float of miles.
    # Since row and column are interchangeable flip if empty to save time iterating over complete list
    def getDistanceBetween(self, current, destination):
        distance = self.distanceMatrix[current][destination]
        if distance == "":
            distance = self.distanceMatrix[destination][current]
        return float(distance)

    # Helper function to return the id of each address. Checks for match of string address and search. Returns index for use with distanceTable
    def getAddressIndex(self, search):
        for address in self.addressList:
            if search in address[2]:
                return int(address[0])
