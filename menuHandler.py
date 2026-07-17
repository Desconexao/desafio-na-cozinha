from recipeBook import RecipeBook
from typing import cast
from recipe import Recipe
from vip_menu import generate_vip_menu
from dataStructures.graph import load_graph_from_json
from logistics.logistics_algorithms import mst_kruskal, dijkstra, reconstruct_path
from logistics.logistics_planner import load_kitchens, load_orders, load_regions, allocate_orders_greedy


def showMenu():
    print("\n=== Desafio na Cozinha ===")
    print("1. Modo Investigação")
    print("2. Modo Chef")
    print("3. Modo Busca Rápida")
    print("4. O Pesadelo Logístico (Operação de Delivery)")
    print("0. Sair")
    return input("Escolha uma opção: ")


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
    print("3. Menu Degustação VIP (Otimização)")
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


def showLogisticsModeMenu():
    print("\n=== O Pesadelo Logístico - Operação de Delivery ===")
    print("1. Planejar Rede de Hubs de Retirada (Árvore Geradora Mínima - Kruskal)")
    print("2. Calcular Rota do Entregador (Caminho Mais Curto - Dijkstra)")
    print("3. Distribuir Pedidos entre Cozinhas (Alocação de Capacidade)")
    print("0. Voltar")
    return input("Escolha uma opção: ")


def searchRecipeByID(book: RecipeBook):
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


def runIntegrityCheck(book: RecipeBook):
    print("\n--- Running Investigation ---")
    allRecipes = book.listAllRecipes()
    corrupted = [recipe for recipe in allRecipes if recipe.isCorrupted()]
    if not corrupted:
        print("Integrity Check Passed: All recipes match their hashes.")
    else:
        for recipe in corrupted:
            print(f"[!] CORRUPTED: {recipe.name} (ID: {recipe.id})")


def updateAllHashes(book: RecipeBook, jsonPath: str):
    confirm = input("This will update all integrity hashes. Proceed? (y/n): ")
    if confirm.lower() == "y":
        book.updateAllHashes(jsonPath)


def showHashTableStats(book: RecipeBook):
    print("\n=== HashTable Statistics ===")

    # 1.IDHashTable
    tableId = book.recipesById
    print("\n[ID Table]")
    print(f"Size: {tableId.size} | Elements: {tableId.count}")
    print(
        f"Load Factor: {tableId.getLoadFactor():.2f} | Rehashes: {tableId.rehashCount}"
    )

    # 2.CategoryHashTable
    tableCat = book.recipesByCategory
    print("\n[Category Table]")
    print(f"Size: {tableCat.size} | Elements: {tableCat.count}")
    print(
        f"Load Factor: {tableCat.getLoadFactor():.2f} | Rehashes: {tableCat.rehashCount}"
    )

    # 3.IngredientHashTable
    tableIng = book.recipesByIngredients
    print("\n[Ingredient Table]")
    print(f"Size: {tableIng.size} | Elements: {tableIng.count}")
    print(
        f"Load Factor: {tableIng.getLoadFactor():.2f} | Rehashes: {tableIng.rehashCount}"
    )


def searchRecipeByName(book: RecipeBook):
    search = input("I'm looking for...: ")
    found, result = book.searchByName(search)

    if found:
        print("Found!!")
        exactMatch = cast(Recipe, result)
        print(f"ID: {exactMatch.id} - {exactMatch.name}")
        return

    print("Couldn't find an exact match...")
    if not result:
        return

    print("Did you mean?")
    suggestions = cast(tuple[Recipe, ...], result)
    for recipe in suggestions:
        print(f"{recipe.id} - {recipe.name}")


def searchRecipeByCategory(book: RecipeBook):
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


def searchRecipeByIngredient(book: RecipeBook):
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


def getMyIdealDish(book: RecipeBook):
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


def generateRecipeCombination(book: RecipeBook):
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


def runMenu(book: RecipeBook, jsonPath: str):
    while True:
        choice = showMenu()

        match choice:
            case "1":
                investigationModeMenu(book, jsonPath)
            case "2":
                chefModeMenu(book)
            case "3":
                quickSearchModeMenu(book)
            case "4":
                logisticsModeMenu(book)
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")


def investigationModeMenu(book: RecipeBook, jsonPath: str):
    while True:
        choice = showInvestigationModeMenu()

        match choice:
            case "1":
                runIntegrityCheck(book)
            case "2":
                updateAllHashes(book, jsonPath)
            case "3":
                showHashTableStats(book)
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")


def chefModeMenu(book: RecipeBook):
    while True:
        choice = showChefModeMenu()

        match choice:
            case "1":
                getMyIdealDish(book)
            case "2":
                generateRecipeCombination(book)
            case "3":
                generateVipMenu(book)
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")


def generateVipMenu(book: RecipeBook):
    print("\nEscolha a restrição para otimização:")
    print("1. Orçamento máximo (cost)")
    print("2. Tempo total máximo (prepTime)")
    choice = input("Escolha 1 ou 2: ")

    if choice == "1":
        try:
            max_cost = float(input("Digite o orçamento máximo (ex: 500): "))
        except ValueError:
            print("Valor inválido.")
            return
        weight_attr = "cost"
        capacity = max_cost
    elif choice == "2":
        try:
            max_time = int(input("Digite o tempo total máximo em minutos (ex: 180): "))
        except ValueError:
            print("Valor inválido.")
            return
        weight_attr = "prepTime"
        capacity = max_time
    else:
        print("Opção inválida.")
        return

    # candidates: use all recipes (no prefiltering); the chosen weight_attr enforces the single constraint
    candidates = book.listAllRecipes()

    selected, meta = generate_vip_menu(candidates, capacity, weight_attr=weight_attr)

    if not selected:
        print("Nenhuma combinação encontrada para a restrição informada.")
        return

    print("\n--- Menu Degustação VIP (Sugestão) ---")
    for i, recipe in enumerate(selected, start=1):
        print(
            f"{i}. ID: {recipe.id} - {recipe.name} | Cost: {recipe.cost} | PrepTime: {recipe.prepTime} | Rating: {recipe.rating}"
        )

    print(f"Total Cost: {meta.get('total_cost')}")
    print(f"Total PrepTime: {meta.get('total_prep_time')}")
    print(f"Total Rating: {meta.get('total_rating')}")


def quickSearchModeMenu(book: RecipeBook):
    while True:
        choice = showQuickSearchModeMenu()

        match choice:
            case "1":
                searchRecipeByID(book)
            case "2":
                searchRecipeByName(book)
            case "3":
                searchRecipeByCategory(book)
            case "4":
                searchRecipeByIngredient(book)
            case "0":
                print("Exiting mode...")
                break
            case _:
                print("Invalid option.")


def buildMST():
    print("\n--- Planejar Rede de Hubs de Retirada ---")
    try:
        graph = load_graph_from_json('logistics/regions.json', 'logistics/roads.json')
        mst_edges, mst_weight = mst_kruskal(graph)
        
        print(f"\nArvore Geradora Minima Construida!")
        print(f"  Regioes: {len(graph.nodes())}")
        print(f"  Conexoes: {len(mst_edges)} (esperado: {len(graph.nodes()) - 1})")
        print(f"  Custo Total: {mst_weight}")
        print(f"\nPrimeiras 10 conexoes:")
        for i, (u, v, w) in enumerate(mst_edges[:10], 1):
            print(f"  {i}. {u:2} -- {v:2} (tempo: {w:5.1f} min)")
    except Exception as e:
        print(f"Erro ao construir MST: {e}")


def calculateShortestPath():
    print("\n--- Calcular Rota do Entregador ---")
    try:
        graph = load_graph_from_json('logistics/regions.json', 'logistics/roads.json')
        
        source = int(input("Regiao de saida (1-30): "))
        target = int(input("Regiao de destino (1-30): "))
        
        if source not in graph.nodes() or target not in graph.nodes():
            print("Regioes invalidas.")
            return
        
        distances, parents = dijkstra(graph, source)
        path = reconstruct_path(parents, source, target)
        
        if path:
            print(f"\nRota encontrada: {' -> '.join(map(str, path))}")
            print(f"Tempo total: {distances[target]:.1f} minutos")
        else:
            print(f"Sem rota entre regiao {source} e {target}.")
    except ValueError:
        print("Entrada invalida.")
    except Exception as e:
        print(f"Erro: {e}")


def simulateOrderAllocation():
    print("\n--- Distribuir Pedidos entre Cozinhas ---")
    try:
        graph = load_graph_from_json('logistics/regions.json', 'logistics/roads.json')
        kitchens = load_kitchens('logistics/kitchens.json')
        orders = load_orders('logistics/orders.json')
        regions = load_regions('logistics/regions.json')
        recipe_book = RecipeBook()
        
        print(f"\nDados carregados:")
        print(f"  Regioes: {len(regions)}")
        print(f"  Cozinhas: {len(kitchens)}")
        print(f"  Pedidos: {len(orders)}")
        
        allocation_report = allocate_orders_greedy(orders, kitchens, graph, regions, recipe_book)
        allocation = allocation_report['allocation']
        kitchen_loads = allocation_report['kitchen_loads']
        delayed = allocation_report['delayed_orders']
        gargalos = allocation_report['gargalos']
        
        print(f"\nAlocacao Concluida:")
        print(f"  Pedidos atendidos: {len(allocation)}/{len(orders)}")
        print(f"  Pedidos pendentes: {len(delayed)}")
        
        print(f"\nCarga por Cozinha:")
        for kitchen in kitchens:
            kid = kitchen['id']
            load = len(kitchen_loads.get(kid, []))
            capacity = kitchen['capacity_per_hour'] * 24
            util_pct = (load / capacity * 100) if capacity > 0 else 0
            print(f"  {kid}: {load:2}/{capacity:3} pedidos ({util_pct:5.1f}%)")
        
        print(f"\nGargalos:")
        if gargalos:
            for gb in gargalos:
                print(f"  {gb['kitchen_id']}: {gb['assigned']} pedidos > {gb['capacity']} (excesso: {gb['excess']})")
        else:
            print("  Nenhum gargalo identificado!")
    except Exception as e:
        print(f"Erro na simulacao: {e}")


def logisticsModeMenu(book: RecipeBook):
    while True:
        choice = showLogisticsModeMenu()
        
        match choice:
            case "1":
                buildMST()
            case "2":
                calculateShortestPath()
            case "3":
                simulateOrderAllocation()
            case "0":
                print("Voltando...")
                break
            case _:
                print("Opção inválida.")
