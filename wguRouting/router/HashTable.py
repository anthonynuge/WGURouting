class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # Print the table to the cli for debugging purposes
    def display(self):
        print("Hash Table:")
        for i, j in enumerate(self.table):
            print(f"Index:{i} ", j)

    # Calculate and return index of table to store
    def calcHash(self, id):
        return id % self.size

    # Add obj to table.
    def insert(self, id, obj):
        hashVal = self.calcHash(id)
        # If index of table is empty add array list to store obj and future objs
        if self.table[hashVal] is None:
            self.table[hashVal] = []
        # Add obj to array list
        self.table[hashVal].append((id, obj))
