import hashlib
import json


class Recipe:
    def __init__(
        self,
        id,
        name,
        category,
        ingredients,
        instructions,
        prepTime=0,
        cost=0.0,
        difficulty="Medium",
        integrityHash=None,
        rating=0.0,
    ):
        self.id = id
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions
        self.prepTime = prepTime
        self.cost = cost
        self.difficulty = difficulty
        self.rating = rating

        if integrityHash:
            self.integrityHash = integrityHash
        else:
            self.integrityHash = self.calculateCurrentHash()

    def calculateCurrentHash(self):
        # Generate SHA-256 hash  prevent any sabotage
        content = {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "ingredients": sorted(self.ingredients),
            "instructions": self.instructions,
            "prepTime": self.prepTime,
            "cost": self.cost,
            "difficulty": self.difficulty,
            "rating": self.rating,
        }
        contentStr = json.dumps(content, sort_keys=True).encode("utf-8")
        return hashlib.sha256(contentStr).hexdigest()

    def isCorrupted(self):
        return self.calculateCurrentHash() != self.integrityHash

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "prepTime": self.prepTime,
            "cost": self.cost,
            "difficulty": self.difficulty,
            "rating": self.rating,
            "integrityHash": self.integrityHash,
        }

    def __repr__(self):
        status = " [!] ERROR" if self.isCorrupted() else ""
        return (
            f"Recipe(ID: {self.id}, Name: '{self.name}', Cat: {self.category}){status}"
        )
