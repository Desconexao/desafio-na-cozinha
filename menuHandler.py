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
    print("1. Get My Ideal Dish")
    print("2. Generate Recipe Combination")
    print("0. Back")
    return input("Choose an option: ")

def showQuickSearchModeMenu():
    print("\n=== Modo Busca Rápida ===")
    print("1. Search Recipe by ID")
    print("2. Search Recipe by Name")
    print("3. Search Recipe by Category")
    print("4. Search Recipe by Ingredient")
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

def searchRecipeByCategory():
    categories = book.recipesByCategory.getKeys()
    if not categories:
        print("No categories found.")
        return

    print("Choose one of the following categories: ")
    for i, category in enumerate(categories):
        print(f"{i} - {category}")

    try:
        choice = int(input("Enter category number: "))
    except ValueError:
        print("Invalid option.")
        return

    if choice < 0 or choice >= len(categories):
        print("Invalid option.")
        return

    selectedCategory = categories[choice]
    recipes = book.recipesByCategory.search(selectedCategory)
    if not recipes:
        print("Category not found.")
        return

    print("\nFound recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - {recipe.name}")


def searchRecipeByIngredient():
    ingredients = book.recipesByIngredients.getKeys()
    if not ingredients:
        print("No ingredients found.")
        return

    print("Choose one of the following ingredients: ")
    for i, ingredient in enumerate(ingredients):
        print(f"{i} - {ingredient}")

    try:
        choice = int(input("Enter ingredient number: "))
    except ValueError:
        print("Invalid option.")
        return

    if choice < 0 or choice >= len(ingredients):
        print("Invalid option.")
        return

    selectedIngredient = ingredients[choice]
    recipes = book.recipesByIngredients.search(selectedIngredient)
    if not recipes:
        print("Ingredient not found.")
        return

    print("\nFound recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - {recipe.name}")


def getMyIdealDish():
    try:
        maxCost = float(input("Enter max price: "))
        maxPrepTime = int(input("Enter max prep time: "))
        difficultyLevel = int(input("Enter difficulty (0 easy, 1 medium, 2 hard): "))
    except ValueError:
        print("Invalid value.")
        return

    suggestions = book.suggestIdealRecipes(maxCost, maxPrepTime, difficultyLevel)
    if not suggestions:
        print("No matching recipes found.")
        return

    print("\n--- Best Suggestions ---")
    for i, recipe in enumerate(suggestions, start=1):
        print(
            f"{i}. ID: {recipe.id} - {recipe.name} | "
            f"Rating: {recipe.rating} | Cost: {recipe.cost} | PrepTime: {recipe.prepTime}"
        )


def generateRecipeCombination():
    print("\nChoose objective:")
    print("1. Economic Menu")
    print("2. Fast Menu")
    objectiveChoice = input("Choose an option: ")

    if objectiveChoice == "1":
        objective = "economic"
    elif objectiveChoice == "2":
        objective = "fast"
    else:
        print("Invalid option.")
        return

    try:
        maxCost = float(input("Enter max total cost: "))
        maxPrepTime = int(input("Enter max total prep time: "))
    except ValueError:
        print("Invalid value.")
        return

    recipes = book.generateRecipeCombination(objective, maxCost, maxPrepTime)
    if not recipes:
        print("No combination found for this objective.")
        return

    print("\n--- Suggested Combination ---")
    totalCost = 0.0
    totalPrepTime = 0
    for i, recipe in enumerate(recipes, start=1):
        totalCost += recipe.cost
        totalPrepTime += recipe.prepTime
        print(
            f"{i}. ID: {recipe.id} - {recipe.name} | "
            f"Cost: {recipe.cost} | PrepTime: {recipe.prepTime} | Rating: {recipe.rating}"
        )

    print(f"Total Cost: {totalCost}")
    print(f"Total PrepTime: {totalPrepTime}")


def runMenu(bookParam, jsonPathParam):
    global book
    global jsonPath

    book = bookParam
    jsonPath = jsonPathParam

    #print("\033[H\033[J", end="")
    while True:
        choice = showMenu()
        #print("\033[H\033[J", end="")

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
        #print("\033[H\033[J", end="")

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
        #print("\033[H\033[J", end="")

        match choice:
            case "1":
                getMyIdealDish()
            case "2":
                generateRecipeCombination()
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")

def quickSearchModeMenu():
    while True:
        choice = showQuickSearchModeMenu()
        #print("\033[H\033[J", end="")

        match choice:
            case "1":
                searchRecipeByID()
            case "2":
                searchRecipeByName()
            case "3":
                searchRecipeByCategory()
            case "4":
                searchRecipeByIngredient()
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")
