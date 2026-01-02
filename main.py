from __future__ import annotations
from json import load as load_json
from dataclasses import dataclass, field

DEBUG = True

@dataclass
class Ingredient:
    amount: int
    name: str
    
    def __post_init__(self) -> None:
        if (self.amount < 0): raise ValueError("Cannot have negative ingredients")
    
    def __str__(self) -> str:
        return f"x{self.amount} {self.name}"
    
    def __repr__(self) -> str:
        return f"x{self.amount} {self.name}"
        
    def __add__(self, other: Ingredient) -> Ingredient:
        if (not isinstance(other, Ingredient)): raise NotImplemented(f"Expected {Ingredient.__name__}, but got {type(other).__name__} instead")
        elif (self.name != other.name): raise ValueError(f"Cannot add different Ingredients, but got {self} and {other}")
        
        return Ingredient(self.amount + other.amount, self.name)
    
    def __iadd__(self, other: Ingredient) -> Ingredient:
        if (not isinstance(other, Ingredient)): raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        elif (self.name != other.name): raise ValueError(f"Cannot add different Ingredients, but got {self} and {other}")
        
        self.amount += other.amount
        return self
    
    def __sub__(self, other: Ingredient) -> Ingredient:
        if (not isinstance(other, Ingredient)): raise NotImplemented(f"Expected {Ingredient.__name__}, but got {type(other).__name__} instead")
        elif (self.name != other.name): raise TypeError(f"Ingredient subtraction using two different Ingredients, {self.name} and {other.name}")
        elif (self.amount < other.amount): raise ValueError(f"Ingredient subtraction resulted in a negative amount ({self} - {other})")
        
        return Ingredient(self.amount - other.amount, self.name)
    
    
    def __isub__(self, other: Ingredient) -> Ingredient:
        if (not isinstance(other, Ingredient)): raise NotImplemented(f"Expected {Ingredient.__name__}, but got {type(other).__name__} instead")
        elif (self.name != other.name): raise TypeError(f"Ingredient subtraction using two different Ingredients, {self.name} and {other.name}")
        elif (self.amount < other.amount): raise ValueError(f"Ingredient subtraction resulted in a negative amount ({self} - {other})")
        
        self.amount = self.amount - other.amount
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
    
    def __add__(self, other: Inventory | Ingredient) -> Inventory:
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
    
    def __iadd__(self, other: Inventory | Ingredient) -> Inventory:
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
        # Returns True if the Inventory has the item and greater than or equal to the amount in Item
        if (not isinstance(item, Ingredient)): raise NotImplementedError(f"Cannot check an inventory for class {type(item).__name__}")
        
        for curr_item in self.items:
            if (curr_item.name == item.name and curr_item.amount >= item.amount): return True
        return False

    def __mul__(self, other: int) -> Inventory:
        new_inventory = Inventory()
        for item in self.items:
            new_inventory.items.append(Ingredient(item.amount * other, item.name))
        
        return new_inventory
    
    def __sub__(self, other: Ingredient) -> Inventory:
        if (not isinstance(other, Ingredient)): raise NotImplemented(f"Expected {Ingredient.__name__}, but got {type(other).__name__} instead")
        new_inventory = Inventory()
        for new_item in self.items:
            if (new_item.name != other.name): 
                new_inventory.items.append(new_item)
            else:
                if (other.amount <= new_item.amount): 
                    resulting_ingredient = new_item - other
                    if (resulting_ingredient.amount != 0): 
                        new_inventory.items.append(resulting_ingredient)
        
        return new_inventory
    
    def __isub__(self, other: Ingredient) -> Inventory:
        if (not isinstance(other, Ingredient)): raise NotImplementedError(f"Expected {Ingredient.__name__}, but got {type(other).__name__} instead")
        for item in self.items[:]:
            if (item.name == other.name):
                if (other.amount > item.amount): raise ValueError(f"Not enough {item.name} to subtract")
                item.amount -= other.amount
                if (item.amount == 0): self.items.remove(item)
                break
        else: raise ValueError(f"{other.name} not found in inventory")

        return self

    def check_for_item_by_name(self, item_name: str) -> int:
        for item in self.items:
            if (item.name == item_name): return item.amount
        return 0 # We did not have any of that item

    def can_craft(self, recipe: Recipe, count: int = 1) -> bool:
        new_inputs: list[Ingredient] = []
        for inp in recipe.inputs:
            new_inputs.append(Ingredient(inp.amount * count, inp.name))
        temp_recipe = Recipe(recipe.name, [], new_inputs, [])
        
        for needed_item in temp_recipe.inputs:
            if (needed_item not in self): return False
        return True
    
    def do_recipe(self, recipe: Recipe, count: int = 1) -> bool:
        if (not self.can_craft(recipe, count)): return False
        for i in range(count):
            for ingredient in recipe.inputs:
                print(f"Removing {ingredient}")
                self -= ingredient
        return True
    
def load_recipes(filename: str) -> tuple[list[Recipe], list[str]]:
    converted_recipes: list[Recipe] = []
    all_ingredients: list[Ingredient] = []
    
    with open(filename, "r") as file:
        recipe_list = load_json(file)
    
    # Turn recipes into Recipe class
    for recipe in recipe_list:
        new_ingredients = [Ingredient(item["amount"], item["name"]) for item in recipe["inputs"]]
        for ingredient in new_ingredients: 
            all_ingredients.append(ingredient)
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

def get_base_ingredients_for_item(recipe_to_craft: Recipe, count: int, cookbook: list[Recipe], base_ingredients_list: list[str]):
    print()
    print()
    print(f"Starting {recipe_to_craft.name}")
    base_ingredient_inventory = Inventory()
    while (not base_ingredient_inventory.can_craft(recipe_to_craft, count)):
        print(f"\tCannot craft {count} {recipe_to_craft.name} from {base_ingredient_inventory}")
        for recipe_ingredient in recipe_to_craft.inputs:
            
            if (recipe_ingredient in base_ingredient_inventory): continue
            
            
            for base_ing_name in base_ingredients_list:
                if (base_ing_name == recipe_ingredient.name):
                    base_ingredient_inventory += recipe_ingredient
                    print(f"\t\tAdding {recipe_ingredient} (it is a base ingredient) ({base_ingredient_inventory})")
                    break # The current ingrendient we are looking at is a base ingredient, so we can go to the next one
            else:
                for found_recipe in cookbook:
                    if (recipe_ingredient.name == found_recipe.name):
                        found_recipe.outputs
                        base_ingredient_inventory += get_base_ingredients_for_item(found_recipe, recipe_ingredient.amount, cookbook, base_ingredients_list)
                        print(f"\t\tAdding {found_recipe.name}'s ingredients (we grabbed the needed base ingredients) ({base_ingredient_inventory})")
        
    
    
    return base_ingredient_inventory


if __name__ == "__main__":    
    recipes, base_ingredients = load_recipes("recipes.json")
    test = Inventory([Ingredient(6, "Redstone Torch"), Ingredient(2, "Nether Quartz"), Ingredient(6, "Stone")])
    
    rec = recipes[3]
    count = 5

    base_inv = get_base_ingredients_for_item(rec, count, recipes, base_ingredients)
    print(base_inv)
    
    
    
    """
    To make 1 set of Redstone Comparator, you need: [3x Redstone Torch, 1x Nether Quartz, 3x Stone]
        Do we have any Redstone Torch in extra_inventory? No
        Is Redstone Torch a base ingredient? No
        Try to craft one set of Redstone Torch
            To make 1 set of Redstone Torch, you need: [1x Redstone Dust, 1x Stick]
                Do we have any Redstone Dust in extra_inventory? No
                Is Redstone Dust a base ingredient? Yes, add it to the base_inventory
                Do we have any Stick in extra_inventory? No
                Is Stick a base ingredient? No
                Try to craft one set of Stick
                    To make 1 set of Stick, you need: [2x Oak Plank]
                    Do we have any Oak Plank in extra_inventory? No
                    Is Oak Plank a base ingredient? No
                    Try to craft one set of Oak Plank
                        To make 1 set of Oak Plank, you need: [1x Oak Log]
                        Do we have any Oak Log in extra_inventory? No
                        Is Oak Log a base ingredient? Yes, add is to the base_inventory
                    
    
    """