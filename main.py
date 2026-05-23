from recipeBook import RecipeBook


def showMenu():
    print("\n=== Desafio na Cozinha ===")
    print("1. Search Recipe by ID")
    print("2. Run Integrity Check (Investigation)")
    print("3. Update All Hashes (Authorize Changes)")
    print("4. Show HashTable Stats")
    print("0. Exit")
    return input("Choose an option: ")


def main():
    book = RecipeBook()
    jsonPath = "recipes2.json"
    book.loadRecipes(jsonPath)
    allRecipes = book.listAllRecipes()

    # Auto-protect: if file has no hashes, calculate and save them
    try:
        import json

        with open(jsonPath, "r", encoding="utf-8") as jsonFile:
            firstItem = json.load(jsonFile)[0]
            if firstItem.get("integrityHash") is None:
                print(
                    "Unprotected file detected. Generating initial integrity hashes..."
                )
                book.updateAllHashes(jsonPath)
    except:
        pass

    while True:
        choice = showMenu()

        if choice == "1":
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

        elif choice == "2":
            print("\n--- Running Investigation ---")
            allRecipes = book.listAllRecipes()
            corrupted = [recipe for recipe in allRecipes if recipe.isCorrupted()]
            if not corrupted:
                print("Integrity Check Passed: All recipes match their hashes.")
            else:
                for recipe in corrupted:
                    print(f"[!] CORRUPTED: {recipe.name} (ID: {recipe.id})")

        elif choice == "3":
            confirm = input("This will update all integrity hashes. Proceed? (y/n): ")
            if confirm.lower() == "y":
                book.updateAllHashes(jsonPath)

        elif choice == "4":
            hashTable = book.recipesById
            print(f"\n--- HashTable Statistics ---")
            print(f"Current Size: {hashTable.size}")
            print(f"Total Elements: {hashTable.count}")
            print(f"Load Factor: {hashTable.getLoadFactor():.2f}")
            print(f"Number of Rehashes: {hashTable.rehashCount}")

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
