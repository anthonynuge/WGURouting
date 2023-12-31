from .Status import Status


class Package:
    def __init__(self, id, address, city, state, zip, deadLine, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadLine = deadLine
        self.weight = weight
        self.status = Status(status)

    def __str__(self) -> str:
        return (
            "id:%s, addr:%s, city:%s, state:%s, zip:%s, deadLine:%s, weight:%s, status:%s"
            % (
                self.id,
                self.address,
                self.city,
                self.state,
                self.zip,
                self.deadLine,
                self.weight,
                self.status.value,
            )
        )
