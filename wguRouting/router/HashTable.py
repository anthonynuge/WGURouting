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

    # Checks if a package is in the hashtable based on id. Overall time complexity of O(n)
    def lookup(self, searchId):
        hashVal = self.calcHash(searchId)
        # Only iterates through inner array if there is a hash match. Helps with efficiency. O(1)
        if self.table[hashVal] is not None:
            # Checks each element in inner array time consuming part depending on number of obj collisions: O(n)
            for id, obj in self.table[hashVal]:
                if id == searchId:
                    return obj
        return None
