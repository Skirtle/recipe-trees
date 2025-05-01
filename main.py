class Inventory():
    items: list
    
    def __init__(self, starting: list = None) -> None: 
        self.items = []
        
        if (starting is not None):
            for item in starting:
                if (isinstance(item, Ingredient)): self.items.append(item)
                elif (isinstance(item, Inventory)): self.items.extend(item.items)
                else: raise TypeError(f"Expected Ingredient or Inventory, got {type(item).__name__}")
     
    
    def add(self, other) -> None:
        if (isinstance(other, Inventory)):  self.items += other.items
        elif (isinstance(other, Ingredient)):  self.items.append(other)
        else: raise TypeError(f"Expected Ingredient or Inventory, got {type(other).__name__}")
        self.combine_items()
        
    def has_item(self, other) -> bool:
        if (isinstance(other, Ingredient)): name = other.name
        elif (isinstance(other, str)): name = other
        else: raise TypeError(f"Expected Ingredient or Inventory, got {type(other).__name__}")
        return any(item.name == name and item.amount >= 1 for item in self.items)
    
    def combine_items(self):
        ...
        
        
        
            

class Recipe():
    inputs: list
    outputs: list
    station: str
    
    def __init__(self, inputs: list, outputs: list, station: str = None):
        self.inputs = inputs
        self.outputs = outputs
        self.station = station
        
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
    
    def __sub__(self, other):
        if (not isinstance(other, Ingredient)): return NotImplemented
        elif (self.name != other.name): raise ValueError(f"Cannot subtract Ingredients of diffent types, {self.name} and {other.name}")
        elif (self.amount < other.amount): raise ValueError(f"Cannot have negative amounts of ingredients")
        return Ingredient(self.name, self.amount - other.amount)

inventory = Inventory()


wood_log = Ingredient("Wood Log")
wood_plank = Ingredient("Wood Plank")
cobblestone = Ingredient("Cobblestone")
redstone_dust = Ingredient("Redstone Dust")
iron_ore = Ingredient("iron_ore")
iron_ingot = Ingredient("Iron Ingot")

a = [1,2,3]
b = [4,5]

print(a + b)