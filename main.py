from __future__ import annotations
import json

_DEBUG = False

class Ingredient():
    name: str
    amount: int
    
    def __init__(self, name: str, amount: int = 0):
        if (not isinstance(amount, int)): raise TypeError(f"Expected int, got {type(amount).__name__}")
        if (amount < 0): raise ValueError(f"Expected non-negative integer, got {amount}")
        
        self.name = name
        self.amount = amount
        
    def __str__(self): return f"{self.amount}x {self.name}"
    def __repr__(self): return self.__str__()
    def __add__(self, other):
        if (not isinstance(other, Ingredient)): return NotImplemented
        elif (self.name != other.name): raise ValueError(f"Cannot add Ingredients of diffent types, {self.name} and {other.name}")
        return Ingredient(self.name, self.amount + other.amount)
    def __mult__(self, other):
        if (not isinstance(other, int)): return NotImplemented
        elif (other < 0): raise ValueError(f"Expected non-negative integer, got {other}")
        return Ingredient(self.name, self.amount * other)
    
    def __sub__(self, other):
        if (not isinstance(other, Ingredient)): return NotImplemented
        elif (self.name != other.name): raise ValueError(f"Cannot subtract Ingredients of diffent types, {self.name} and {other.name}")
        elif (self.amount < other.amount): raise ValueError(f"Cannot have negative amounts of ingredients")
        return Ingredient(self.name, self.amount - other.amount)

class Recipe():
    inputs: list
    outputs: list
    station: str
    name: str
    
    def __init__(self, inputs: list, outputs: list, station: str = "Crafting Table", name: str = "None"):
        self.inputs = inputs
        self.outputs = outputs
        self.station = station
        self.name = name
        
    def __str__(self):
        s = f"[{self.name} at a {self.station}]\nInputs:"
        for item in self.inputs:
            s += f"\n  - {item}"
        s += "\nOutputs:"
        for item in self.outputs:
            s += f"\n  - {item}"
        return s
    
    def __repr__(self):
        return f"{self.name} recipe"

class Inventory():
    items: dict
    
    def __init__(self, starting: dict = None) -> None: 
        self.items = {}
        
        if (starting is not None):
            for item_name in starting:
                if (not isinstance(starting[item_name], Ingredient)): 
                    raise TypeError(f"Expected Ingredient, got {type(starting[item_name]).__name__}")
            self.items = starting
     
    
    def add(self, other) -> None:
        # Add an item
        if (isinstance(other, Ingredient)):
            if (other.name in self.items): self.items[other.name] += other
            else: self.items[other.name] = other
        # Add an inventory
        elif (isinstance(other, Inventory)):
            for item in other.items:
                self.add(other.items[item])
        # Failed to add
        else:
            raise TypeError(f"Expected Ingredient or Inventory, got {type(other).__name__}")
        
    def has_item(self, other) -> bool:
        if (isinstance(other, Ingredient)): name = other.name
        elif (isinstance(other, str)): name = other
        else: raise TypeError(f"Expected Ingredient or str, got {type(other).__name__}")
        return name in self.items
    
    def has_amount(self, other, amount = None) -> bool:
        if (not self.has_item(other)): return False
        
        if (isinstance(other, Ingredient)): 
            name = other.name
            check_amount = other.amount
        elif (isinstance(other, str) and isinstance(amount, int)):
            name = other
            check_amount = amount
        else: raise TypeError(f"Expected int for amount, got {type(amount).__name__}")
        
        return self.items[name].amount >= check_amount
        
    def can_craft(self, recipe: Recipe) -> bool:
        for item in recipe.inputs:
            if (not self.has_amount(item)): return False
        return True
    
    def __str__(self):
        s = "Inventory:"
        for i in self.items:
            s += f"\n  - {i}: {self.items[i].amount}"
        s += "\n  - Empty" if len(self.items) == 0 else ""
        return s
    
    def get_missing_ingredients(self, recipe: Recipe) -> Inventory:
        missing = []
        # Go through each input in the recipe and check if we have the amount
        for item in recipe.inputs:
            if (self.has_amount(item)): continue # We have the amount we need
            # Check to see if the item even exists
            elif (self.has_item(item)):
                # Item exists, we just need more
                new_amount =  item.amount - self.items[item.name].amount
                missing.append(Ingredient(item.name, new_amount))
            else: 
                # Item does not exist, we need all of it
                missing.append(Ingredient(item.name, item.amount))
        return missing
        
def load_recipes(filename) -> list:
    recipes = []
    
    with open(filename, "r") as file:
        data = json.load(file)
    
    for recipe in data:
        name = recipe["name"]
        station = recipe["station"]
        inputs = []
        outputs = []
        
        for input in recipe["inputs"]: inputs.append(Ingredient(input["name"], input["amount"]))
        for output in recipe["outputs"]: outputs.append(Ingredient(output["name"], output["amount"]))
        recipes.append(Recipe(inputs, outputs, station, name))
        if (_DEBUG): print(f"Loaded {name} recipe")
        
    return recipes
    
    

recipes = load_recipes("recipes.json")
inv = Inventory()
inv.add(Ingredient("Aluminum Plate", 2))
inv.add(Ingredient("1x Copper Cable", 1))
inv.add(Ingredient("Aluminum Rod", 1))
inv.add(Ingredient("Small Aluminum Gear", 0))
inv.add(Ingredient("MV Electric Motor", 0))

rec = recipes[0]
missing = inv.get_missing_ingredients(rec)
for item in missing:
    print(item)