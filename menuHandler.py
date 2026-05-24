from recipeBook import RecipeBook

book: RecipeBook
jsonPath: str

def showMenu():
    print("\n=== Desafio na Cozinha ===")
    print("1. Investigation Mode")
    print("2. Chef Mode")
    print("3. Quick Search Mode")
    print("0. Exit")
    return input("Choose an option: ")

def showInvestigationModeMenu():
    print("\n=== Modo Investigação ===")
    print("1. Run Integrity Check (Investigation)")
    print("2. Update All Hashes (Authorize Changes)")
    print("3. Show HashTable Stats")
    print("0. Back")
    return input("Choose an option: ")

def showChefModeMenu():
    print("\n=== Modo Chef ===")
    print("0. Back")
    return input("Choose an option: ")

def showQuickSearchModeMenu():
    print("\n=== Modo Busca Rápida ===")
    print("1. Search Recipe by ID")
    print("2. Search Recipe by Name")
    print("0. Back")
    return input("Choose an option: ")


def searchRecipeByID():
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


def runIntegrityCheck():
    print("\n--- Running Investigation ---")
    allRecipes = book.listAllRecipes()
    corrupted = [recipe for recipe in allRecipes if recipe.isCorrupted()]
    if not corrupted:
        print("Integrity Check Passed: All recipes match their hashes.")
    else:
        for recipe in corrupted:
            print(f"[!] CORRUPTED: {recipe.name} (ID: {recipe.id})")


def updateAllHashes():
    confirm = input("This will update all integrity hashes. Proceed? (y/n): ")
    if confirm.lower() == "y":
        book.updateAllHashes(jsonPath)


def showHashTableStats():
    hashTable = book.recipesById
    print("\n--- HashTable Statistics ---")
    print(f"Current Size: {hashTable.size}")
    print(f"Total Elements: {hashTable.count}")
    print(f"Load Factor: {hashTable.getLoadFactor():.2f}")
    print(f"Number of Rehashes: {hashTable.rehashCount}")


def searchRecipeByName():
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


def runMenu(bookParam, jsonPathParam):
    global book
    global jsonPath

    book = bookParam
    jsonPath = jsonPathParam

    print("\033[H\033[J", end="")
    while True:
        choice = showMenu()
        print("\033[H\033[J", end="")

        match choice:
            case "1":
                investigationModeMenu()
            case "2":
                chefModeMenu()
            case "3":
                quickSearchModeMenu()
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid option.")


def investigationModeMenu():
    while True:
        choice = showInvestigationModeMenu()
        print("\033[H\033[J", end="")

        match choice:
            case "1":
                runIntegrityCheck()
            case "2":
                updateAllHashes()
            case "3":
                showHashTableStats()
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")

def chefModeMenu():
    while True:
        choice = showChefModeMenu()
        print("\033[H\033[J", end="")

        match choice:
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")

def quickSearchModeMenu():
    while True:
        choice = showQuickSearchModeMenu()
        print("\033[H\033[J", end="")

        match choice:
            case "1":
                searchRecipeByID()
            case "2":
                searchRecipeByName()
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")