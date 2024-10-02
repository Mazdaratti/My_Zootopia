import json
import sys
from webbrowser import open as open_browser


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
        Convert a single animal's data into an HTML list item.

        Args:
            animal (dict): A dictionary representing an animal's data.

        Returns:
            str: An HTML string representation of the animal.
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


def serialize_animals(data, skin_type=None):
    """
    Convert a list of animals into HTML, with optional filtering by skin type.

    Args:
        data (list): A list of animal dictionaries.
        skin_type (str, optional): The skin type to filter by. If None, all animals are serialized.

    Returns:
        str: An HTML string representing the filtered or unfiltered list of animals.
    """
    return ''.join(
        serialize_animal(animal)
        for animal in data
        if skin_type is None or animal.get('characteristics', {}).get('skin_type') == skin_type
    )


def generate_list_of_values(data):
    """
    Generate a list of unique skin types from animal data, including an 'All skin types' option.

    Args:
        data (list): A list of animal dictionaries.

    Returns:
        list: A list of skin types.
    """
    values = ["All skin types"]
    values.extend({animal.get("characteristics", {}).get("skin_type") for animal in data if animal.get("characteristics", {}).get("skin_type")})
    return values


def display_menu(values):
    """
    Display a menu for selecting skin type.

    Args:
        values (list): A list of skin types.
    """
    print("\nPlease choose the skin type of animals you want to see:")
    for index, value in enumerate(values):
        print(f"{index}. {value}")
    print()


def get_user_choice(menu_entries):
    """
    Prompt the user to select an option from the menu and ensure valid input.

    Args:
        menu_entries (list): A list of menu entries.

    Returns:
        int: The index of the chosen entry.
    """
    while True:
        user_input = input(f"Enter choice (0-{len(menu_entries) - 1}): ").strip()
        if user_input.isdigit():
            choice = int(user_input)
            if 0 <= choice < len(menu_entries):
                return choice
        print(f"Invalid choice: [{user_input}]")


def write_file(file_path, content):
    """Write the given content to a file."""
    with open(file_path, "w") as file:
        file.write(content)
        print(f"Website was successfully generated at {file_path}.")


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

    values = generate_list_of_values(data)
    display_menu(values)

    choice = get_user_choice(values)
    animals_info = serialize_animals(data) if choice == 0 else serialize_animals(data, values[choice])

    updated_template = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    write_file("animals.html", updated_template)
    open_browser("animals.html")

if __name__ == "__main__":
    main()


