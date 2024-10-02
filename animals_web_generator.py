import json
import sys

def load_file(file_path, file_type="data"):
    """
    Load and return the content of a file.

    Args:
        file_path (str): The path to the file.
        file_type (str): The type of file, either "data" for JSON or "template" for HTML.

    Returns:
        data: The content of the file, parsed JSON if it's a data file or raw content otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or cannot be parsed (for JSON files).
    """
    try:
        with open(file_path, "r") as file:
            content = file.read() if file_type == "template" else json.load(file)
            if not content:  # Check if the file is empty
                raise ValueError(f"Error: The {file_type} file is empty.")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The {file_type} file '{file_path}' was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: The JSON file '{file_path}' could not be decoded.")


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


def write_file(file_path, content):
    """Write the given content to a file."""
    with open(file_path, "w") as file:
        file.write(content)


def main():
    """
        Generate animal information, filter by skin type, update the HTML template, and open it in a browser.
    """
    try:
        data = load_file("animals_data.json", file_type="data")
        template = load_file("animals_template.html", file_type="template")
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    animals_info = serialize_animals(data)
    updated_template = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    write_file("animals.html", updated_template)


if __name__ == "__main__":
    main()


