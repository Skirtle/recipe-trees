from json import load as load_json
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Ingredient:
    amount: int
    name: Optional[str] = None
    tags: Optional[list[str]] = None
    screen_name: str = ""
    
    def __post_init__(self) -> None:
        if (self.amount <= 0): raise ValueError("Cannot have negative ingredients")
        
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
    
    def __add__(self, other: "Ingredient") -> "Ingredient":
        if (not isinstance(other, Ingredient)): raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        
        self_tags = self.tags or []
        other_tags = other.tags or []
        if (self.name != other.name or self_tags !=other_tags): raise ValueError(f"Cannot add generic tags and specific items")
        
        return Ingredient(self.amount + other.amount, self.name, self.tags)
    
    def __iadd__(self, other: "Ingredient") -> "Ingredient":
        if (not isinstance(other, Ingredient)): raise TypeError(f"Cannot add {type(self)} and {type(other)}")
        
        self_tags = self.tags or []
        other_tags = other.tags or []
        if (self.name != other.name or self_tags !=other_tags): raise ValueError(f"Cannot add generic tags and specific items")
        
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

def load_recipes(filename: str) -> tuple[list[Recipe], list[str]]:
    converted_recipes: list[Recipe] = []
    all_ingredients: list[Ingredient] = []
    
    with open(filename, "r") as file:
        recipe_list = load_json(file)
    
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
        if (ing.name not in recipe_strs and ing.item_or_tag != "tag"): 
            base_ingredients.append(ing.screen_name)
        
    return (converted_recipes, base_ingredients)

def load_tags(filename: str) -> dict[str, list[str]]:
    with open(filename, "r") as file:
        return load_json(file)

if __name__ == "__main__":
    recipes,base_ingredients = load_recipes("recipes.json")
    tags = load_tags("tags.json")
    
    for rec in recipes: print(rec)
    print(f"{base_ingredients = }")
    
    print("tags: {")
    for tag in tags: print(f"\t{tag}: {tags[tag]}")
    print("}")