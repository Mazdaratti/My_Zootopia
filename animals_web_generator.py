import json


def load_json(file_path):
    """Load and return the data from a JSON file."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def serialize_animal(animal_obj):
    """Generate formatted information for a single animal."""
    name = animal_obj.get("name")
    characteristics = animal_obj.get("characteristics", {})
    diet = characteristics.get("diet")
    animal_type = characteristics.get("type")
    locations = animal_obj.get("locations", [])

    # Using a list to accumulate strings for better performance
    animal_info_parts = ["<li class='cards__item'>"]

    if name:
        animal_info_parts.append(f"Name: {name}<br/>\n")
    if diet:
        animal_info_parts.append(f"Diet: {diet}<br/>\n")
    if locations:
        animal_info_parts.append(f"Location: {locations[0]}<br/>\n")
    if animal_type:
        animal_info_parts.append(f"Type: {animal_type}<br/>\n")

    animal_info_parts.append("</li>")

    return ''.join(animal_info_parts)


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


