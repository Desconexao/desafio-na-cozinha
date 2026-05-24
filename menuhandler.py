from recipeBook import RecipeBook

def searchRecipeByName(book: RecipeBook):

    search = input("I'm looking for...: ")
    found, result = book.recipeTrie.searchRecipe(search, prefixSearch=True, suggestionDepthLimit=10, suggestionCount=5)

    if found:
        print("Found!!")
        print(f"ID: {result.id} - {result.name}")

        return

    print("Couldn't find your search...")
    if not result:
        return

    print("Did you mean?")
    for recipe in result:
        print(f"{recipe.id} - {recipe.name}")
