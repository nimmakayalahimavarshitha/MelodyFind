
class CustomHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)

        # If the key already exists, add another value
        for item in self.table[index]:
            if item[0] == key:
                item[1].append(value)
                return

        # Otherwise, store a new key-value pair
        self.table[index].append([key, [value]])
        self.count += 1

    def search(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item[0] == key:
                return item[1]

        return []

    def display(self):
        for index, bucket in enumerate(self.table):
            if bucket:
                print(index, bucket)


if __name__ == "__main__":
    ht = CustomHashTable()

    ht.insert(123, ("Song A", 0))
    ht.insert(456, ("Song B", 5))
    ht.insert(123, ("Song C", 2))

    print("Search for 123:", ht.search(123))
    print("Search for 999:", ht.search(999))
    ht.display()
