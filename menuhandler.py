from recipeBook import RecipeBook
# Menu option 1
def searchRecipeByID(book: RecipeBook):
    try:
        searchId = int(input("Enter Recipe ID: "))
        recipe = book.getRecipeById(searchId)
        if recipe:
            print(f"\n--- Recipe Details ---")
            print(f"Name: {recipe.name}")
            print(f"Category: {recipe.category}")
            print(
                f"Status: {'OK' if not recipe.isCorrupted() else 'CORRUPTED'}"
            )
        else:
            print("Recipe not found.")
    except ValueError:
        print("Invalid ID.")


# Menu option 2
def runIntegrityCheck(book: RecipeBook):
    print("\n--- Running Investigation ---")
    allRecipes = book.listAllRecipes()
    corrupted = [recipe for recipe in allRecipes if recipe.isCorrupted()]
    if not corrupted:
        print("Integrity Check Passed: All recipes match their hashes.")
    else:
        for recipe in corrupted:
            print(f"[!] CORRUPTED: {recipe.name} (ID: {recipe.id})")


# Menu option 3
def updateAllHashes(book: RecipeBook, jsonPath: str):
    confirm = input("This will update all integrity hashes. Proceed? (y/n): ")
    if confirm.lower() == "y":
        book.updateAllHashes(jsonPath)


# Menu option 4
def showHashTableStats(book: RecipeBook):
    hashTable = book.recipesById
    print(f"\n--- HashTable Statistics ---")
    print(f"Current Size: {hashTable.size}")
    print(f"Total Elements: {hashTable.count}")
    print(f"Load Factor: {hashTable.getLoadFactor():.2f}")
    print(f"Number of Rehashes: {hashTable.rehashCount}")


# Menu option 5
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

