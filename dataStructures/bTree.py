class BTreeNode:
    def __init__(self, minimumDegree, isLeaf=True):
        self.minimumDegree = minimumDegree
        self.isLeaf = isLeaf
        self.keys = []
        self.values = []
        self.children = []


class BTree:
    def __init__(self, minimumDegree=2):
        if minimumDegree < 2:
            raise ValueError("minimumDegree must be >= 2")

        self.minimumDegree = minimumDegree
        self.root = BTreeNode(minimumDegree=minimumDegree, isLeaf=True)

    def search(self, key, node=None):
        if node is None:
            node = self.root

        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1

        if index < len(node.keys) and key == node.keys[index]:
            return node.values[index]

        if node.isLeaf:
            return None

        return self.search(key, node.children[index])

    def insert(self, key, value):
        root = self.root
        maxKeys = 2 * self.minimumDegree - 1

        # If root is full, split before inserting
        if len(root.keys) == maxKeys:
            newRoot = BTreeNode(minimumDegree=self.minimumDegree, isLeaf=False)
            newRoot.children.append(root)
            self._splitChild(newRoot, 0)
            self.root = newRoot

        self._insertNonFull(self.root, key, value)

    def toList(self):
        result = []
        self._inOrder(self.root, result)
        return result

    def contains(self, key):
        return self.search(key) is not None

    def clear(self):
        self.root = BTreeNode(minimumDegree=self.minimumDegree, isLeaf=True)

    def _insertNonFull(self, node, key, value):
        index = len(node.keys) - 1

        if node.isLeaf:
            while index >= 0 and key < node.keys[index]:
                index -= 1

            # Update existing key
            if index >= 0 and node.keys[index] == key:
                node.values[index] = value
                return
            if index + 1 < len(node.keys) and node.keys[index + 1] == key:
                node.values[index + 1] = value
                return

            node.keys.insert(index + 1, key)
            node.values.insert(index + 1, value)
            return

        while index >= 0 and key < node.keys[index]:
            index -= 1
        index += 1

        # Update existing key in internal node
        if index < len(node.keys) and node.keys[index] == key:
            node.values[index] = value
            return

        maxKeys = 2 * self.minimumDegree - 1
        if len(node.children[index].keys) == maxKeys:
            self._splitChild(node, index)
            if key > node.keys[index]:
                index += 1
            elif key == node.keys[index]:
                node.values[index] = value
                return

        self._insertNonFull(node.children[index], key, value)

    def _splitChild(self, parent, childIndex):
        degree = self.minimumDegree
        child = parent.children[childIndex]
        newNode = BTreeNode(minimumDegree=degree, isLeaf=child.isLeaf)

        middleKey = child.keys[degree - 1]
        middleValue = child.values[degree - 1]

        # Move right half to the new node
        newNode.keys = child.keys[degree:]
        newNode.values = child.values[degree:]

        # Keep left half in original child
        child.keys = child.keys[: degree - 1]
        child.values = child.values[: degree - 1]

        if not child.isLeaf:
            newNode.children = child.children[degree:]
            child.children = child.children[:degree]

        parent.keys.insert(childIndex, middleKey)
        parent.values.insert(childIndex, middleValue)
        parent.children.insert(childIndex + 1, newNode)

    def _inOrder(self, node, result):
        if node.isLeaf:
            for index, key in enumerate(node.keys):
                result.append((key, node.values[index]))
            return

        for index, key in enumerate(node.keys):
            self._inOrder(node.children[index], result)
            result.append((key, node.values[index]))

        self._inOrder(node.children[-1], result)
