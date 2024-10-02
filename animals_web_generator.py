import json


def load_json(file_path):
    """Load and return the data from a JSON file."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def serialize_animal(animal):
    """
        Serialize a single animal's data into an HTML list item.

        Parameters:
            animal (dict): A dictionary with animal data.

        Returns:
            str: An HTML string representing the animal.
    """
    output = '    <li class="cards__item">\n'
    animal_name = animal.get("name", "Unknown Animal")
    output += f'        <div class="card__title">{animal_name}</div>\n'
    output += '        <ul>\n'
    animal_details = {
        "Scientific name": animal.get("taxonomy", {}).get("scientific_name"),
        "Diet": animal.get("characteristics", {}).get("diet"),
        "Location": animal.get("locations", [None])[0],
        "Type": animal.get("characteristics", {}).get("type"),
        "Most distinctive feature": animal.get("characteristics", {}).get("most_distinctive_feature"),
        "Color": animal.get("characteristics", {}).get("color"),
        "Skin type": animal.get("characteristics", {}).get("skin_type"),
    }
    for key, value in animal_details.items():
        if value:
            output += f'            <li><span class="field__name">{key}:</span> {value}</li>\n'
    output += '        </ul>\n'
    output += '    </li>\n'
    return output


def serialize_animals(data):
    """Serialize a list of animals data into an HTML string."""
    return ''.join(serialize_animal(animal) for animal in data)


def read_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, content):
    """Write the given content to a file."""
    with open(file_path, "w") as file:
        file.write(content)


def main():
    """Generate animal information and update the HTML template."""
    data = load_json("animals_data.json")
    animals_info = serialize_animals(data)
    template = read_file("animals_template.html")
    updated_template = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    write_file("animals.html", updated_template)


if __name__ == "__main__":
    main()


