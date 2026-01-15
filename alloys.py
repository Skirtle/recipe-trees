from json import load as load_json


filename = "alloying_recipes.json"

def get_alloys(filename):
    with open(filename, "r") as file:
        return load_json(file)
    
    
print(get_alloys(filename))