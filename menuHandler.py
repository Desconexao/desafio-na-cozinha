from recipeBook import RecipeBook


def showMenu():
    print("\n=== Desafio na Cozinha ===")
    print("1. Search Recipe by ID")
    print("2. Run Integrity Check (Investigation)")
    print("3. Update All Hashes (Authorize Changes)")
    print("4. Show HashTable Stats")
    print("5. Search Recipe by Name")
    print("0. Exit")
    return input("Choose an option: ")


def searchRecipeByID(book):
    try:
        searchId = int(input("Enter Recipe ID: "))
        recipe = book.getRecipeById(searchId)
        if recipe:
            print("\n--- Recipe Details ---")
            print(f"Name: {recipe.name}")
            print(f"Category: {recipe.category}")
            print(f"Status: {'OK' if not recipe.isCorrupted() else 'CORRUPTED'}")
        else:
            print("Recipe not found.")
    except ValueError:
        print("Invalid ID.")


def runIntegrityCheck(book):
    print("\n--- Running Investigation ---")
    allRecipes = book.listAllRecipes()
    corrupted = [recipe for recipe in allRecipes if recipe.isCorrupted()]
    if not corrupted:
        print("Integrity Check Passed: All recipes match their hashes.")
    else:
        for recipe in corrupted:
            print(f"[!] CORRUPTED: {recipe.name} (ID: {recipe.id})")


def updateAllHashes(book, jsonPath):
    confirm = input("This will update all integrity hashes. Proceed? (y/n): ")
    if confirm.lower() == "y":
        book.updateAllHashes(jsonPath)


def showHashTableStats(book):
    hashTable = book.recipesById
    print("\n--- HashTable Statistics ---")
    print(f"Current Size: {hashTable.size}")
    print(f"Total Elements: {hashTable.count}")
    print(f"Load Factor: {hashTable.getLoadFactor():.2f}")
    print(f"Number of Rehashes: {hashTable.rehashCount}")


def searchRecipeByName(book):
    search = input("I'm looking for...: ")
    found, result = book.searchByName(search)

    if found:
        print("Found!!")
        print(f"ID: {result.id} - {result.name}")
        return

    print("Couldn't find an exact match...")
    if not result:
        return

    print("Did you mean?")
    for recipe in result:
        print(f"{recipe.id} - {recipe.name}")


def runMenu(book, jsonPath):
    while True:
        choice = showMenu()

        match choice:
            case "1":
                searchRecipeByID(book)
            case "2":
                runIntegrityCheck(book)
            case "3":
                updateAllHashes(book, jsonPath)
            case "4":
                showHashTableStats(book)
            case "5":
                searchRecipeByName(book)
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid option.")
