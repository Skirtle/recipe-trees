from json import load as load_json
from dataclasses import dataclass

filename = "alloying_recipes.json"

def get_alloys(filename):
    with open(filename, "r") as file:
        return load_json(file)
    
@dataclass
class Ingredient:
    name: str
    min: int
    max: int
    
    def __str__(self) -> str: return f"{self.name} ({self.min} - {self.max}%)"
    
@dataclass
class Alloy:
    name: str
    ingredients: list[Ingredient]
    
    def generate_ratios(self):
        ranges: dict[tuple[int, int], list[str]] = {}
        
        for ingredient in self.ingredients:
            ing_range = (ingredient.min, ingredient.max)
            if (ing_range not in ranges): ranges[ing_range] = []
            
            ranges[ing_range].append(ingredient.name)

        return ranges

        
    def __str__(self) -> str:
        s = f"{self.name}: ["
        
        for index,ingredient in enumerate(self.ingredients):
            s += ingredient.__str__()
            
            if (index != len(self.ingredients) - 1):
                s += ", "
        
        return s + "]"

def generate_ratios(self):
    print(self)
    ranges: dict[tuple[int, int], list[str]] = {}
    new_ranges: dict[tuple[int, int], list[str]] = {}
    
    for ingredient in self.ingredients:
        ing_range = (ingredient.min, ingredient.max)
        if (ing_range not in ranges): ranges[ing_range] = []
        
        ranges[ing_range].append(ingredient.name)
        
    for r in ranges:
        new_len = len(ranges[r])
        new_r = (r[0] * new_len, r[1] * new_len)
        new_ranges[new_r] = ranges[r]
    
    total = 100
    # Get the highest minimum
    highest_min_range = (0, 0)
    highest_min_names = []
    for r in new_ranges:
        if (r[0] > highest_min_range[0]):
            highest_min_range = r
            highest_min_names = new_ranges[r]
            
    print(f"\t{highest_min_names} = {highest_min_range[0]}")
    semi_final_counts = {highest_min_range[0]: highest_min_names}
    total -= highest_min_range[0]

    return None


alloy_json = get_alloys(filename)
alloys: list[Alloy] = []

for alloy in alloy_json:
    for alloy_name in alloy:
        ing_list: list[Ingredient] = []
        
        for ingredient in alloy[alloy_name]:
            ingredient_name = list(ingredient.keys())[0]
            ing_range = (ingredient[ingredient_name][0], ingredient[ingredient_name][1])
            new_ing = Ingredient(ingredient_name, ing_range[0], ing_range[1])
            ing_list.append(new_ing)
        
        new_alloy = Alloy(alloy_name, ing_list)
        alloys.append(new_alloy)
        
for alloy in alloys:
    generate_ratios(alloy)