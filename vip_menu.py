from typing import List, Tuple
from recipe import Recipe


def detect_scale_factor(recipes: List[Recipe], capacity_float: float | None = None, weight_attr: str = "cost") -> int:
    """Detect minimal integer scale factor for costs when weight is 'cost'.
    If weight_attr is 'prepTime' returns 1 (prepTime is integer minutes).
    """
    if weight_attr == "prepTime":
        return 1

    max_decimals = 0
    for r in recipes:
        s = f"{r.cost}"
        if "." in s:
            decimals = len(s.split(".")[1])
            if decimals > max_decimals:
                max_decimals = decimals
    if capacity_float is not None:
        s = f"{capacity_float}"
        if "." in s:
            decimals = len(s.split(".")[1])
            if decimals > max_decimals:
                max_decimals = decimals
    return 10 ** max(1, max_decimals)


def generate_vip_menu(recipes: List[Recipe], capacity: float, weight_attr: str = "cost") -> Tuple[List[Recipe], dict]:
    """
    0/1 knapsack bottom-up DP.
    - weight_attr: 'cost' (default) or 'prepTime'
    - If weight_attr == 'cost': weight = recipe.cost (scaled to int), capacity is float money
    - If weight_attr == 'prepTime': weight = int(recipe.prepTime), capacity is int minutes

    Returns (selected_recipes, metadata).
    """
    if not recipes:
        return [], {"total_cost": 0.0, "total_prep_time": 0, "total_rating": 0.0}

    factor = detect_scale_factor(recipes, capacity, weight_attr)

    if weight_attr == "cost":
        weights = [int(round(r.cost * factor)) for r in recipes]
        W = int(round(capacity * factor))
    elif weight_attr == "prepTime":
        # prepTime is already integer minutes
        weights = [int(round(r.prepTime)) for r in recipes]
        W = int(round(capacity))
    else:
        raise ValueError("weight_attr must be 'cost' or 'prepTime'")

    values = [float(r.rating) for r in recipes]
    n = len(recipes)

    # DP table (n+1) x (W+1)
    dp: List[List[float]] = [[0.0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        prev = dp[i - 1]
        curr = dp[i]
        for c in range(0, W + 1):
            best = prev[c]
            if w <= c:
                val = prev[c - w] + v
                if val > best:
                    best = val
            curr[c] = best

    # reconstruct solution
    selected: List[Recipe] = []
    c = W
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(recipes[i - 1])
            c -= weights[i - 1]

    selected.reverse()

    total_cost = sum(r.cost for r in selected)
    total_prep_time = sum(int(r.prepTime) for r in selected)
    total_rating = sum(float(r.rating) for r in selected)

    metadata = {
        "total_cost": total_cost,
        "total_prep_time": total_prep_time,
        "total_rating": total_rating,
        "scale_factor": factor,
        "capacity": capacity,
        "weight_attr": weight_attr,
    }

    return selected, metadata