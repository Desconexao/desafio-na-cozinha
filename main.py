from recipeBook import RecipeBook
from menuHandler import runMenu


def main():
    book = RecipeBook()
    jsonPath = "recipes2.json"

    # Load data
    book.loadRecipes(jsonPath)

    # Auto-protect database
    try:
        import json

        with open(jsonPath, "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            if data and data[0].get("integrityHash") is None:
                print("Unprotected file detected. Generating hashes...")
                book.updateAllHashes(jsonPath)
    except Exception as e:
        print(f"Startup check: {e}")

    # Start menu
    runMenu(book, jsonPath)


if __name__ == "__main__":
    main()
