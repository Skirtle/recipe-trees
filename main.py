import json
from pprint import pprint
from dataclasses import dataclass
from typing import Any

@dataclass
class Item:
    is_base: bool = False


def load_recipes(filename: str) -> list[Any]:
    with open(filename, "r") as file:
        return json.load(file)
    
if __name__ == "__main__":
    recipe_filename = "recipes.json"
    x = load_recipes(recipe_filename)