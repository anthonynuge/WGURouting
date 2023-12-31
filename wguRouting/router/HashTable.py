class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # Print the table to the cli for debugging purposes
    def display(self):
        print("Hash Table:")
        for i, j in enumerate(self.table):
            print(f"Index:{i} ", j)
