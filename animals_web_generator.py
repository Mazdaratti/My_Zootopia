import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


animals_data = load_data('animals_data.json')
#print(animals_data)

for animal in animals_data:
    if "name" in animal.keys():
        print(f"Name: {animal["name"]}")
    if "diet" in animal["characteristics"].keys():
        print(f"Diet: {animal["characteristics"]["diet"]}")
    if "locations" in animal.keys():
        print(f"Location: {animal["locations"][0]}")
    if "type" in animal["characteristics"].keys():
        print(f"Type: {animal["characteristics"]["type"]}")
    print()
