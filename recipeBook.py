import json
from recipe import Recipe
from recipeTrie import RecipeTrie
from recipeHash import HashTable


class RecipeBook:
    def __init__(self):
        self.recipesById = HashTable(initialSize=5)
        self.recipesByIngredients = HashTable(initialSize=5)
        self.recipesByCategory = HashTable(initialSize=5)
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
                    self.recipesByCategory.insert(recipe.category, recipe)

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

    def _insertRecipesByIngredients(self, ingredients: list, recipe: Recipe):
        for ingredient in ingredients:
            self.recipesByIngredients.insert(ingredient, recipe)
