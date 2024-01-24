import re
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
        self.status = Status("at hub")
        self.specialNote = specialNote
        self.deliverWith = []
        self.delay = False
        self.earliestDeparture = None

        # If there is a special not parse and set attributes
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
            "id:%s, addr:%s, city:%s, state:%s, zip:%s, deadLine:%s, weight:%s, status:%s, specialNote:%s, earliestDeparture:%s, deliverWith:%s"
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
                self.earliestDeparture,
                self.deliverWith,
            )
        )
