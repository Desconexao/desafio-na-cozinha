class HashTable:
    # Hash Table with chaining and dynamic resizing
    def __init__(self, initialSize=5):
        self.size = initialSize
        self.count = 0
        self.rehashCount = 0
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        # Generate table index
        return hash(key) % self.size

    def _resize(self):
        # Double the table size (Rehash)
        oldTable = self.table
        self.size *= 2
        self.rehashCount += 1
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in oldTable:
            for storedId, storedRecipe in bucket:
                self.insert(storedId, storedRecipe)

    def insert(self, key, value):
        # Resize if load factor >= 1
        if (self.count / self.size) >= 1.0:
            self._resize()

        index = self._hash(key)
        # Check if key already exists to update without increasing count
        for i, (storedId, storedRecipe) in enumerate(self.table[index]):
            if storedId == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))
        self.count += 1

    def search(self, key):
        index = self._hash(key)
        for storedId, storedRecipe in self.table[index]:
            if storedId == key:
                return storedRecipe
        return None

    def getAll(self):
        allValues = []
        for bucket in self.table:
            for storedId, storedRecipe in bucket:
                allValues.append(storedRecipe)
        return allValues
    
    def getKeys(self) -> list:
        keys = []

        for bucket in self.table:
            for key, value in bucket:
                keys.append(key)

        return keys

    def getLoadFactor(self):
        return self.count / self.size
