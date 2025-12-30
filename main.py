import json
from dataclasses import dataclass
from typing import Optional, Any

default_tags = {
    
}

@dataclass
class Ingredient:
    amount: int
    name: Optional[str] = None
    tags: Optional[list[str]] = None
    screen_name: str = ""
    
    def __post_init__(self) -> None:
        if (self.name != None): 
            self.item_or_tag = "item"
            self.screen_name = self.name
        elif (self.tags != None): 
            self.item_or_tag = "tag"
            self.screen_name = f"any {self.tags}"
        
    
    def __str__(self) -> str:
        s = f"x{self.amount}"
        if (self.item_or_tag == "item"): s += f" {self.name}"
        else: s += f" '{self.tags}' item"
        return s
    
    def __repr__(self) -> str:
        s = f"x{self.amount}"
        if (self.item_or_tag == "item"): s += f" {self.name}"
        else: s += f" {self.tags}"
        return s
    
@dataclass
class Result:
    name: str
    amount: int
    
    def __str__(self) -> str:
        s = f"x{self.amount} {self.name}"
        return s

@dataclass
class Recipe:
    name: str
    stations: list[str]
    inputs: list[Ingredient]
    outputs: list[Result]
    
    def __post_init__(self) -> None:
        for ingredient in self.inputs:
            if (ingredient.name == None and ingredient.tags == None): raise ValueError(f"Ingredient {ingredient} needs either a name or tags, but was given neither")
            elif (ingredient.name != None and ingredient.tags != None): raise ValueError(f"Ingredient {ingredient} needs either a name or tags, but was given both")
            elif (ingredient.amount < 1): raise ValueError(f"Ingredient amount must be positive, but was given {ingredient.amount}")
            
    def __str__(self) -> str:
        s = f"Recipe: {self.name}\n\tCrafted in: "
        for index,station in enumerate(self.stations):
            s += station
            if (index != (len(self.stations) - 1)): s += ", "
       
        s += "\n\tRequires: "
        for index,ingredient in enumerate(self.inputs):
            s += ingredient.__str__()
            if (index != (len(self.inputs) - 1)): s += ", "
            
        s += "\n\tCreates: "
        for index,result in enumerate(self.outputs):
            s += result.__str__()
            if (index != (len(self.outputs) - 1)): s += ", "
        
        return s

def load_recipes(filename: str) -> tuple[list[Recipe], list[str]]:
    converted_recipes: list[Recipe] = []
    all_ingredients: list[Ingredient] = []
    
    with open(filename, "r") as file:
        recipe_list = json.load(file)
    
    # Turn recipes into Recipe class
    for recipe in recipe_list:
        new_ingredients = [Ingredient(item["amount"], item["name"], item["tags"]) for item in recipe["inputs"]]
        for ingredient in new_ingredients: all_ingredients.append(ingredient)
        new_results = [Result(item["name"], item["amount"]) for item in recipe["outputs"]]
        new_recipe = Recipe(recipe["name"], recipe["stations"], new_ingredients, new_results)
        converted_recipes.append(new_recipe)
        
    # Base ingredients are ingredients that do not have a recipe
    base_ingredients: list[str] = []
    recipe_strs = [i.name for i in converted_recipes]
    for ing in all_ingredients:
        if ing.name not in recipe_strs and ing.item_or_tag != "tag": base_ingredients.append(ing.screen_name)
        
    return (converted_recipes, base_ingredients)

def load_tags(filename: str) -> dict[str, list[str]]:
    with open(filename, "r") as file:
        return json.load(file)
    
if __name__ == "__main__":
    recipe_filename = "recipes.json"
    tags_filename = "tags.json"
    
    recipes,base_ingredients = load_recipes(recipe_filename)
    tags = load_tags(tags_filename)
    
    for recipe in recipes:
        print(recipe)
        
    print(f"Base ingredients: {base_ingredients}")