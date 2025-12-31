from json import load as load_json
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Ingredient:
    amount: int
    name: str
    
    def __post_init__(self) -> None:
        if (self.amount <= 0): raise ValueError("Cannot have negative ingredients")
    
    def __str__(self) -> str:
        return f"x{self.amount} {self.name}"
    
    def __repr__(self) -> str:
        return f"x{self.amount} {self.name}"
        
    def __add__(self, other: "Ingredient") -> "Ingredient":
        if (not isinstance(other, Ingredient)): raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        
        return Ingredient(self.amount + other.amount, self.name)
    
    def __iadd__(self, other: "Ingredient") -> "Ingredient":
        if (not isinstance(other, Ingredient)): raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        
        self.amount += other.amount
        return self
    
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
            if (ingredient.amount < 1): raise ValueError(f"Ingredient amount must be positive, but was given {ingredient.amount}")
            
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

@dataclass
class Inventory:
    items: list[Ingredient] = field(default_factory = list)
    
    
    def __str__(self) -> str: return self.items.__str__()
    
    def __add__(self, other: "Inventory | Ingredient") -> "Inventory":
        new_inventory = Inventory([i for i in self.items])
        
        # Add two inventories of Ingredients
        if (isinstance(other, Inventory)):
            for ing in other.items:
                new_inventory.add_ingredient(ing)
            return new_inventory
        
        # Add one ingredient to inventory
        elif (isinstance(other, Ingredient)):
            new_inventory.add_ingredient(other)
            return new_inventory
        
        raise ValueError(f"Cannot add {type(other).__name__} to Inventory")
    
    def __iadd__(self, other: "Inventory | Ingredient") -> "Inventory":
        # Add two inventories of Ingredients
        if (isinstance(other, Inventory)):
            for ing in other.items:
                self.add_ingredient(ing)
            return self
        
        # Add one ingredient to inventory
        elif (isinstance(other, Ingredient)):
            self.add_ingredient(other)
            return self
        
        raise ValueError(f"Cannot add {type(other).__name__} to Inventory")
    
    def add_ingredient(self, new_item: Ingredient) -> None:
        for item in self.items:
            try:
                item += new_item
                return
            except ValueError: continue
        
        self.items.append(new_item)

    def __contains__(self, item: Ingredient) -> bool:
        if (not isinstance(item, Ingredient)): raise TypeError(f"Cannot check an inventory for class {type(item).__name__}")
        
        
        # Add logic later
        return False

    def __mul__(self, other: int) -> "Inventory":
        new_inventory = Inventory()
        for item in self.items:
            new_inventory.items.append(Ingredient(item.amount * other, item.name, item.tags))
        
        return new_inventory
    
def load_recipes(filename: str) -> tuple[list[Recipe], list[str]]:
    converted_recipes: list[Recipe] = []
    all_ingredients: list[Ingredient] = []
    
    with open(filename, "r") as file:
        recipe_list = load_json(file)
    
    # Turn recipes into Recipe class
    for recipe in recipe_list:
        new_ingredients = [Ingredient(item["amount"], item["name"]) for item in recipe["inputs"]]
        for ingredient in new_ingredients: all_ingredients.append(ingredient)
        new_results = [Result(item["name"], item["amount"]) for item in recipe["outputs"]]
        new_recipe = Recipe(recipe["name"], recipe["stations"], new_ingredients, new_results)
        converted_recipes.append(new_recipe)
        
    # Base ingredients are ingredients that do not have a recipe
    base_ingredients: list[str] = []
    recipe_strs = [i.name for i in converted_recipes]
    for ing in all_ingredients:
        if (ing.name not in recipe_strs): 
            base_ingredients.append(ing.name)
        
    return (converted_recipes, base_ingredients)

def get_base_ingredients_for_item(item_to_craft: Recipe, cookbook: list[Recipe], base_ingredients: list[str], layer: int = 0) -> tuple[Inventory, Inventory]:
    final_inventory = Inventory()
    extra_inventory = Inventory()
    if (layer == 0): print(f"{'\t' * (layer)}* Crafting {item_to_craft.name} ({layer = })")
    
    for ingredient in item_to_craft.inputs:
        print(f"{'\t' * (layer + 1)}* Need {ingredient}", end = "")
        # First, check the extra inventory for the item. If we have it, we can add it to the final inventory and continue
        
        if (ingredient.name in base_ingredients): 
            print(f"")
        else: 
            print(f"")
            
    
    return final_inventory, extra_inventory

if __name__ == "__main__":
    recipes, base_ingredients = load_recipes("recipes.json")
    print(f"Base ingredients: {base_ingredients}")
    
    ings, extras = get_base_ingredients_for_item(recipes[0], recipes, base_ingredients)
    print(f"\nCrafting completed")
    print(f"Items needed: {ings}")
    print(f"Leftover ingredients: {extras}")