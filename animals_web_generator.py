import json


def load_json(file_path):
    """Load a JSON file and return the data."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def generate_animal_info(animals_data):
    """Generate formatted information for each animal."""
    animals_info_str = ""
    for animal in animals_data:
        # Use .get() to safely access keys
        name = animal.get("name")
        characteristics = animal.get("characteristics", {})
        diet = characteristics.get("diet")
        animal_type = characteristics.get("type")
        locations = animal.get("locations", [])
        animals_info_str += "<li class='cards__item'>"
        if name:
            animals_info_str += f"Name: {name}<br/>\n"
        if diet:
            animals_info_str += f"Diet: {diet}<br/>\n"
        if locations:
            animals_info_str += f"Location: {locations[0]}<br/>\n"
        if animal_type:
            animals_info_str += f"Type: {animal_type}<br/>\n"

        animals_info_str += "</li>"

    return animals_info_str


def read_file(file_path):
    """Read an HTML file and return its contents."""
    with open(file_path, "r") as html_file:
        return html_file.read()


def write_file(file_path, content):
    """Write the modified HTML content to a new file."""
    with open(file_path, "w") as html_output:
        html_output.write(content)


def main():
    """Main function to generate animal HTML from the template."""
    animal_data = load_json("animals_data.json")
    animal_info = generate_animal_info(animal_data)
    template = read_file("animals_template.html")
    updated_template = template.replace("__REPLACE_ANIMALS_INFO__", animal_info)
    write_file("animals.html", updated_template)


if __name__ == "__main__":
    main()

