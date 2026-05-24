import recipe
from time import sleep

class RecipeTrie:
    def __init__(self, stringAdaptation: bool = True):
        self.root = _StringTrieNode("*", False)

        # String adaptation disregards
        # whitespaces: "bolo de cenoura" -> "bolodecenoura"
        # accented letters: "maçã" -> "maça"
        self.adapt = stringAdaptation

    def addRecipe(self, recipe: recipe):
        string = (recipe.name).upper()
        
        if self.adapt:
            string = self._adaptString(string)

        currentNode = self.root
        for char in string:
            if char not in currentNode.children:
                newNode = _StringTrieNode(char, False)
                currentNode.children[char] = newNode

            currentNode = currentNode.children[char]

        currentNode._setFinal(True)
        currentNode._setRecipe(recipe)

    def searchRecipe(self, string: str, prefixSearch: bool = True, suggestionDepthLimit: int = 10, suggestionCount: int = 5) -> tuple[bool, object]:
        """
            returns [bool, object]

            if the returned boolean is:
                True: The whole String was found, the object returned alongside is the recipe itself.
                False: If prefix search is:
                    True: the reurned object is a limited tuple of recipes with the same prefix
                    False: returns None
        """

        if self.adapt:
            string = self._adaptString(string)

        string = string.upper()

        currentNode = self.root
        for char in string:
            sleep(0.5)
            print(f"[DEBUG] Char: {char}")
            if char not in currentNode.children:
                #print("No children for this char")
                #print(f"Children: {currentNode._getChildrenKeys()}")
                break

            currentNode = currentNode.children[char]

        if currentNode._isFinal():
            return True, currentNode._getRecipe()
        
        if not prefixSearch:
            return False, None
        
        suggestions = self._findAutocomplete(currentNode, suggestionDepthLimit, suggestionCount)

        return False, tuple(suggestions)

    def _findAutocomplete(
        self,
        startNode: "_StringTrieNode",
        depth: int,
        size: int
    ) -> tuple:

        suggestions = []

        def dfs(node: "_StringTrieNode", currDepth: int):

            if len(suggestions) >= size:
                return

            if currDepth > depth:
                return

            if node._isFinal():
                suggestions.append(node._getRecipe())

            for child in node.children.values():
                dfs(child, currDepth + 1)

        dfs(startNode, 0)

        return tuple(suggestions[:size])


    def _adaptString(self, string: str) -> str:

        TRANSLATION = str.maketrans({
            "Á": "A",
            "À": "A",
            "Ã": "A",
            "Â": "A",
            "É": "E",
            "Ê": "E",
            "Í": "I",
            "Ó": "O",
            "Ô": "O",
            "Õ": "O",
            "Ú": "U",
        })

        # removes whitespaces
        string = string.replace(" ", "")

        # remove accented chars
        string = string.translate(TRANSLATION)

        return string




class _StringTrieNode:
    def __init__(self, char: str, isFinal: bool):
        self.char = char
        self.children: dict[str, "_StringTrieNode"] = {}
        self.isFinal = isFinal
        self.recipe = None

    def _getChar(self) -> str:
        return self.char
    
    def _isFinal(self) -> bool:
        return self.isFinal
    
    def _setFinal(self, isFinal: bool):
        self.isFinal = isFinal

    def _addChild(self, node: "_StringTrieNode"):
        childChar = node._getChar()

        self.children[self.char] = node

    def _setRecipe(self, recipe: recipe):
        self.recipe = recipe

    def _getRecipe(self) -> recipe:
        return self.recipe
    
    def _getChildrenKeys(self):
        return self.children.keys()
