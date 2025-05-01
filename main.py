import json

class Ingredient():
    name: str
    amount: int
    
    def __init__(self, name, amount = 0):
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
    
    def __init__(self, inputs: list, outputs: list, station: str = "Crafting Table"):
        self.inputs = inputs
        self.outputs = outputs
        self.station = station
        
    def __str__(self):
        s = f"[{self.station}]\nInputs:"
        for item in self.inputs:
            s += f"\n  - {item}"
        s += "\nOutputs:"
        for item in self.outputs:
            s += f"\n  - {item}"
        return s

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
        
def read_recipes(filename) -> list:
    with open(filename, "r") as file:
        ...

piston_recipe = Recipe([Ingredient("Wood Plank", 3), Ingredient("Cobblestone", 4), Ingredient("Redstone Dust", 1), Ingredient("Iron Ingot", 1)], [Ingredient("Piston", 1)])

inv = Inventory()
inv.add(Ingredient("Wood Plank", 3))
inv.add(Ingredient("Cobblestone", 4))
inv.add(Ingredient("Redstone Dust", 0))
inv.add(Ingredient("Iron Ingot", 1))

print(inv.can_craft(piston_recipe))