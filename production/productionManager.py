from recipeBook import RecipeBook
from dataStructures.stack import Stack
from typing import List, Dict, Any, Optional


class ProductionManager:
    """Manages recipe dependencies and production sequences using DFS."""

    def __init__(self, recipeBook: RecipeBook):
        self.recipeBook = recipeBook

    def checkAndSort(self) -> Dict[str, Any]:
        """
        Detects dependency cycles and returns a valid production sequence.
        Uses DFS with an explicit Stack and a 'visiting' set to identify
        circular dependencies.
        """
        recipes = self.recipeBook.listAllRecipes()
        visited = set()  # finalized recipes
        visiting = set()  # recipes currently being processed in the DFS stack
        order = []  # topological order

        def extractCycle(depId: int, path: List[int]) -> List[int]:
            if depId not in path:
                return [depId]

            start = path.index(depId)
            return path[start:] + [depId]

        def removeFromPath(recipeId: int, path: List[int]):
            if path and path[-1] == recipeId:
                path.pop()
                return

            if recipeId in path:
                path.remove(recipeId)

        def dfs(startId: int) -> Optional[List[int]]:
            stack = Stack()
            path = []
            stack.push((startId, False))

            while not stack.isEmpty():
                recipeId, expanded = stack.pop()

                if expanded:
                    visiting.remove(recipeId)
                    visited.add(recipeId)
                    order.append(recipeId)
                    removeFromPath(recipeId, path)
                    continue

                if recipeId in visited:
                    continue

                if recipeId in visiting:
                    return extractCycle(recipeId, path)

                visiting.add(recipeId)
                path.append(recipeId)
                stack.push((recipeId, True))

                recipe = self.recipeBook.getRecipeById(recipeId)
                if recipe:
                    for depId in reversed(recipe.dependencies):
                        if depId in visiting:
                            return extractCycle(depId, path)
                        if depId not in visited:
                            stack.push((depId, False))

            return None

        for r in recipes:
            if r.id not in visited:
                cycle = dfs(r.id)
                if cycle:
                    return {
                        "viable": False,
                        "cycle": cycle,
                        "order": [],
                    }

        return {"viable": True, "cycle": [], "order": order}

    def getPrerequisites(self, targetId: int) -> List[int]:
        """
        Returns all recursive prerequisites for a given recipe
        """
        visited = set()
        prereqs = []

        def dfs(recipeId: int):
            recipe = self.recipeBook.getRecipeById(recipeId)
            if recipe:
                for depId in recipe.dependencies:
                    if depId not in visited:
                        visited.add(depId)
                        prereqs.append(depId)
                        dfs(depId)

        dfs(targetId)
        return prereqs
