DIFFICULTY_BONUS = {
    "Fácil": 10,
    "Media": 7,
    "Média": 7,
    "Difícil": 4,
    "Dificil": 4,
}


def recipeScore(recipe):
    ratingScore = recipe.rating * 20
    costScore = max(0, 100 - recipe.cost) / 10
    timeScore = max(0, 120 - recipe.prepTime) / 10
    difficultyScore = DIFFICULTY_BONUS.get(recipe.difficulty, 5)
    return round(ratingScore + costScore + timeScore + difficultyScore, 2)


def selectCandidates(recipes, limit=6):
    ranked = sorted(recipes, key=lambda recipe: recipeScore(recipe), reverse=True)
    return ranked[:limit]


def minimax(recipeIds, scores, maximizing):
    if not recipeIds:
        return 0, []

    if maximizing:
        bestValue = None
        bestPath = []

        for recipeId in recipeIds:
            remaining = tuple(item for item in recipeIds if item != recipeId)
            value, path = minimax(remaining, scores, False)
            value += scores[recipeId]

            if bestValue is None or value > bestValue:
                bestValue = value
                bestPath = [recipeId] + path

        return bestValue, bestPath

    bestValue = None
    bestPath = []

    for recipeId in recipeIds:
        remaining = tuple(item for item in recipeIds if item != recipeId)
        value, path = minimax(remaining, scores, True)
        value -= scores[recipeId]

        if bestValue is None or value < bestValue:
            bestValue = value
            bestPath = [recipeId] + path

    return bestValue, bestPath


def simulateChefCompetition(recipes, candidateLimit=6):
    candidates = selectCandidates(recipes, candidateLimit)
    scores = {recipe.id: recipeScore(recipe) for recipe in candidates}
    recipeIds = tuple(recipe.id for recipe in candidates)
    finalAdvantage, path = minimax(recipeIds, scores, True)

    chefScore = 0
    rivalScore = 0
    turns = []

    for index, recipeId in enumerate(path):
        recipe = next(recipe for recipe in candidates if recipe.id == recipeId)
        points = scores[recipeId]

        if index % 2 == 0:
            player = "Chef"
            chefScore += points
        else:
            player = "Rival"
            rivalScore += points

        turns.append(
            {
                "player": player,
                "recipe": recipe,
                "score": points,
            }
        )

    return {
        "candidates": candidates,
        "scores": scores,
        "turns": turns,
        "chef_score": round(chefScore, 2),
        "rival_score": round(rivalScore, 2),
        "final_advantage": round(finalAdvantage, 2),
    }
