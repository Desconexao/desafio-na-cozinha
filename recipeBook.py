import json
from recipe import Recipe
from recipeTrie import RecipeTrie
from recipeHash import HashTable
from BTree import BTree


class RecipeBook:
    def __init__(self):
        self.recipesById = HashTable(initialSize=5)
        self.recipesByIngredients = HashTable(initialSize=5)
        self.recipesByCategory = HashTable(initialSize=5)
        self.recipeTrie = RecipeTrie(stringAdaptation=True)
        self.recipesByCost = BTree(minimumDegree=5)
        self.recipesByRating = BTree(minimumDegree=5)
        self.recipesByPrepTime = BTree(minimumDegree=5)
        self.recipesByDifficulty = BTree(minimumDegree=5)

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
                    self._insertRecipesByIngredients(recipe.ingredients, recipe)
                    self._insertRecipesByCategory(recipe.category, recipe)
                    self._insertIntoBTreeIndex(self.recipesByCost, recipe.cost, recipe)
                    self._insertIntoBTreeIndex(
                        self.recipesByRating, recipe.rating, recipe
                    )
                    self._insertIntoBTreeIndex(
                        self.recipesByPrepTime, recipe.prepTime, recipe
                    )
                    self._insertIntoBTreeIndex(
                        self.recipesByDifficulty, recipe.difficulty, recipe
                    )

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

    def searchByName(self, name):
        return self.recipeTrie.searchRecipe(
            name, prefixSearch=True, suggestionDepthLimit=50, suggestionCount=5
        )

    def listAllRecipes(self):
        return self.recipesById.getAll()

    def updateAllHashes(self, filePath):
        # Update the baseline integrity hash for all recipes
        recipes = self.listAllRecipes()
        for recipe in recipes:
            recipe.integrityHash = recipe.calculateCurrentHash()
        self.saveRecipes(filePath)
        print("All integrity hashes have been updated.")

    def _insertRecipesByIngredients(self, ingredients, recipe):

        for ingredient in ingredients:

            entry = self.recipesByIngredients.search(ingredient)

            if entry is None:
                entry = []
                self.recipesByIngredients.insert(ingredient, entry)

            entry.append(recipe)

    def _insertRecipesByCategory(self, category, recipe):

        entry = self.recipesByCategory.search(category)

        if entry is None:
            entry = []
            self.recipesByCategory.insert(category, entry)

        entry.append(recipe)

            

    def _insertIntoBTreeIndex(self, tree: BTree, key, recipe: Recipe):
        current = tree.search(key)
        if current is None:
            tree.insert(key, [recipe])
            return

        current.append(recipe)

    def suggestIdealRecipes(self, maxCost, maxPrepTime, difficultyLevel):
        # Build candidate lists from each criterion
        costRecipes = self._getRecipesUpTo(self.recipesByCost, maxCost)
        prepTimeRecipes = self._getRecipesUpTo(self.recipesByPrepTime, maxPrepTime)
        difficultyRecipes = self._getRecipesByDifficultyLevel(difficultyLevel)

        # Convert to sets for fast intersection
        costIds = set([recipe.id for recipe in costRecipes])
        prepTimeIds = set([recipe.id for recipe in prepTimeRecipes])
        difficultyIds = set([recipe.id for recipe in difficultyRecipes])

        # Keep only recipes present in all three filters (intersection)
        commonIds = costIds.intersection(prepTimeIds).intersection(difficultyIds)
        if not commonIds:
            return []

        # Rebuild recipe objects and rank by rating
        result = []
        for recipe in self.listAllRecipes():
            if recipe.id in commonIds:
                result.append(recipe)

        result.sort(key=lambda recipe: recipe.rating, reverse=True)
        return result

    def _getRecipesUpTo(self, tree: BTree, maxValue):
        result = []
        items = tree.toList()

        # B-Tree is already ordered, collect keys up to maxValue
        for key, recipes in items:
            if key <= maxValue:
                result.extend(recipes)

        return result

    def _getRecipesByDifficultyLevel(self, level):
        # Fixed buckets: 0 easy, 1 medium, 2 hard
        difficultyBuckets = [[], [], []]
        for recipe in self.listAllRecipes():
            bucketIndex = self._mapDifficultyToLevel(recipe.difficulty)
            if bucketIndex is None:
                continue
            difficultyBuckets[bucketIndex].append(recipe)

        if level < 0 or level > 2:
            return []

        return difficultyBuckets[level]

    def _mapDifficultyToLevel(self, difficulty):
        text = str(difficulty).lower()
        if text == "fácil":
            return 0
        if text == "média":
            return 1
        if text == "difícil":
            return 2
        if text == "easy":
            return 0
        if text == "medium":
            return 1
        if text == "hard":
            return 2
        return None

    def generateRecipeCombination(self, objective, maxCost, maxPrepTime):
        if objective == "economic":
            candidates = self._getRecipesUpTo(self.recipesByCost, maxCost)
            candidates.sort(key=lambda recipe: (recipe.cost, recipe.prepTime))
        elif objective == "fast":
            candidates = self._getRecipesUpTo(self.recipesByPrepTime, maxPrepTime)
            candidates.sort(key=lambda recipe: (recipe.prepTime, recipe.cost))
        else:
            return []

        selected = []
        usedIds = set()
        totalCost = 0.0
        totalPrepTime = 0

        # Greedy: pick best local candidate while constraints are valid
        for recipe in candidates:
            if recipe.id in usedIds:
                continue
            if totalCost + recipe.cost > maxCost:
                continue
            if totalPrepTime + recipe.prepTime > maxPrepTime:
                continue

            selected.append(recipe)
            usedIds.add(recipe.id)
            totalCost += recipe.cost
            totalPrepTime += recipe.prepTime

        return selected
