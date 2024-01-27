import re
from datetime import datetime, timedelta
from .Status import Status


class Package:
    def __init__(self, id, address, city, state, zip, deadLine, weight, specialNote):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadLine = deadLine
        self.weight = weight
        self.status = Status.AT_HUB
        self.specialNote = specialNote
        self.deliverWith = []
        self.delay = False
        self.earliestDeparture = None
        self.timeDelivered = None

        # Parses special note into attributes for processing.
        if specialNote:
            if "Must be delivered with" in specialNote:
                together = list(map(int, re.findall("\d+", specialNote)))
                for t in together:
                    self.deliverWith.append(t)
            elif "Delayed" in specialNote:
                time_pattern = re.compile(r"\b(\d{1,2}:\d{2}\s*[ap]m)\b", re.IGNORECASE)
                self.delay = True
                timeMatch = time_pattern.search(specialNote)
                if timeMatch:
                    self.earliestDeparture = timeMatch.group(1)

    def __str__(self) -> str:
        return (
            # "id:%s, addr:%s, city:%s, state:%s, zip:%s, deadLine:%s, weight:%s, status:%s, specialNote:%s, earliestDeparture:%s, deliverWith:%s"
            "id:%s, addr:%s, city:%s, state:%s, zip:%s, deadLine:%s, weight:%s, status:%s, specialNote:%s"
            # "id: %s\n addr: %s\n city: %s\n state: %s\n zip: %s\n deadLine: %s\n weight: %s\n status: %s\n specialNote: %s\n earliestDeparture:%s\n deliverWith: %s\n"
            % (
                self.id,
                self.address,
                self.city,
                self.state,
                self.zip,
                self.deadLine,
                self.weight,
                self.status.value,
                self.specialNote,
                # self.earliestDeparture,
                # self.deliverWith,
            )
        )

    # Updates package status based on specific time. Status is updated only after routes are generated and package expectedDeliveryTime is set.
    # O(1)
    def updateStatus(self, checkedTime):
        expectedDeliveryTime = datetime.strptime(self.timeDelivered, "%I:%M %p")
        if checkedTime > expectedDeliveryTime and self.status == Status.ENROUTE:
            self.status = Status.DELIVERED
        # elif checkedTime < expectedDeliveryTime:
        #     self.status = Status.ENROUTE
