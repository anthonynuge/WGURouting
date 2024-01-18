class Truck:
    def __init__(self, id):
        self.id = id
        self.distance = 0
        self.driver = None
        self.route = []
        self.speed = 18
        self.capacity = 16

    # def getCurrentLocation(time):
    #     pass
    #
    # def deliverPackage():
    #     pass
    #
    # def returnToHub():
    #     pass
    #
    # def add(package):
    #     pass
    #

    def hasRoom(self) -> bool:
        return len(self.route) <= self.capacity

    def loadPackage(self, packageId):
        self.route.append(packageId)
