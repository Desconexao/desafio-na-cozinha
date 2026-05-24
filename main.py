from recipeBook import RecipeBook
from menuhandler import *


def showMenu():
    print("\n=== Desafio na Cozinha ===")
    print("1. Search Recipe by ID")
    print("2. Run Integrity Check (Investigation)")
    print("3. Update All Hashes (Authorize Changes)")
    print("4. Show HashTable Stats")
    print("5. Search recipe name")
    print("0. Exit")
    return input("Choose an option: ")


def main():
    print("\033[H\033[J", end="")
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
        print("\033[H\033[J", end="")

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


if __name__ == "__main__":
    main()
