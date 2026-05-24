from recipeBook import RecipeBook
from menuHandler import runMenu


def main():
    print("=== Desafio na Cozinha - Startup ===")
    print("1. Load recipes.json (50 Recipes - Default)")
    print("2. Load recipes2.json (100 Recipes)")
    fileChoice = input("Choose the database: ")

    if fileChoice == "2":
        jsonPath = "recipes2.json"
    else:
        jsonPath = "recipes.json"

    book = RecipeBook()

    # Load data
    book.loadRecipes(jsonPath)

    # Auto-protect database
    try:
        import json

        with open(jsonPath, "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            if data and data[0].get("integrityHash") is None:
                print(f"Unprotected file ({jsonPath}) detected. Generating hashes...")
                book.updateAllHashes(jsonPath)
    except Exception as e:
        print(f"Startup check: {e}")

    # Start menu
    runMenu(book, jsonPath)


if __name__ == "__main__":
    main()
