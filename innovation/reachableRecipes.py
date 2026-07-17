from dataStructures.stack import Stack


def buildReverseDependencyGraph(recipes):
    graph = {}

    for recipe in recipes:
        graph[recipe.id] = []

    for recipe in recipes:
        for dependencyId in recipe.dependencies:
            if dependencyId not in graph:
                graph[dependencyId] = []
            graph[dependencyId].append(recipe.id)

    return graph


def findReachableRecipes(recipes, startId):
    graph = buildReverseDependencyGraph(recipes)
    visited = set()
    reachable = []
    stack = Stack()

    stack.push(startId)
    visited.add(startId)

    while not stack.isEmpty():
        currentId = stack.pop()

        for nextId in graph.get(currentId, []):
            if nextId not in visited:
                visited.add(nextId)
                reachable.append(nextId)
                stack.push(nextId)

    return reachable
