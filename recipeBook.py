import json
from recipe import Recipe
from RecipeTrie import RecipeTrie


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


    def getLoadFactor(self):
        return self.count / self.size


class RecipeBook:
    def __init__(self):
        self.recipesById = HashTable(initialSize=5)
        self.recipeTrie = RecipeTrie(stringAdaptation=True)

    def loadRecipes(self, filePath):
        # Load recipes from JSON file
        try:
            with open(filePath, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)
                for recipeData in data:
                    recipe = Recipe(
                        id=recipeData.get("id"),
                        name=recipeData.get("name", "Unknown"),
                        category=recipeData.get("category", "General"),
                        ingredients=recipeData.get("ingredients", []),
                        instructions=recipeData.get("instructions", ""),
                        prepTime=recipeData.get("prepTime", 0),
                        cost=recipeData.get("cost", 0.0),
                        difficulty=recipeData.get("difficulty", "Medium"),
                        rating=recipeData.get("rating", 0.0),
                        integrityHash=recipeData.get("integrityHash"),
                    )
                    self.recipesById.insert(recipe.id, recipe)
                    self.recipeTrie.addRecipe(recipe)
            print(f"Success: {len(self.recipesById.getAll())} recipes loaded.")
        except Exception as e:
            print(f"Load error: {e}")

    def saveRecipes(self, filePath):
        # Save recipes to JSON
        data = [recipe.toDict() for recipe in self.recipesById.getAll()]
        try:
            with open(filePath, "w", encoding="utf-8") as jsonFile:
                json.dump(data, jsonFile, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Save error: {e}")

    def getRecipeById(self, recipeId):
        return self.recipesById.search(recipeId)

    def listAllRecipes(self):
        return self.recipesById.getAll()

    def updateAllHashes(self, filePath):
        # Update the baseline integrity hash for all recipes
        recipes = self.listAllRecipes()
        for recipe in recipes:
            recipe.integrityHash = recipe.calculateCurrentHash()
        self.saveRecipes(filePath)
        print("All integrity hashes have been updated.")
