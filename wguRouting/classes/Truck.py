class Truck:
    def __init__(self, id, start, earliestDeparture):
        self.id = id
        self.distance = 0
        self.driver = None
        self.route = []
        self.speed = 18
        self.capacity = 16
        self.currentLocation = start
        self.earliestDeparture = earliestDeparture
        self.distanceHome = 0
        self.timeReturn = None

    def hasRoom(self) -> bool:
        return len(self.route) <= self.capacity

    def loadPackage(self, packageId):
        self.route.append(packageId)

    def __str__(self) -> str:
        return (
            # "id:%s\n, addr:%s\n, city:%s\n, state:%s\n, zip:%s\n, deadLine:%s\n, weight:%s\n, status:%s\n, specialNote:%s\n, earliestDeparture:%s\n, deliverWith:%s\n"
            "Truck %s: \n Total Travel Distance: %s\n Route: %s\n"
            % (
                self.id,
                self.distance,
                self.route,
            )
        )
