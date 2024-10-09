import sys
from webbrowser import open as open_browser
from data_fetcher import fetch_data


def write_file(file_path, content):
    """
        Write the given content to a file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Website was successfully generated at {file_path}.")


def load_file(file_path):
    """
        Loads and returns the content of a file.

        This function opens a file (in text mode), reads its content, and returns it as a string.
        It raises an error if the file is not found or is empty.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                raise ValueError(f"Error: The file {file_path} is empty.")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")


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


def generate_list_of_features(data):
    """
        Generate a list of unique skin types from animal data, including an 'All skin types' option.

        Args:
            data (list): A list of animal dictionaries.

        Returns:
            list: A list of skin types.
    """
    features = ["All skin types"]
    features.extend({animal.get("characteristics", {}).get("skin_type") for animal in data if
                     animal.get("characteristics", {}).get("skin_type")})
    return features


def display_menu(features):
    """
        Display a menu for selecting skin type.

        Args:
            features (list): A list of skin types.
    """
    print("\nPlease choose the skin type of animals you want to see:")
    for index, feature in enumerate(features):
        print(f"{index}. {feature}")
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


def get_animal_name():
    """
        Prompts the user to input the name of the animal they're looking for and validates the input.

        Continuously prompts the user until a valid string with at least 2 characters is entered.

        Returns:
            str: The validated animal name entered by the user.
    """
    while True:
        search_key = input("Enter the name of the animal you want to get information about"
                           " (at least 3 characters):")
        if isinstance(search_key, str) and len(search_key) > 2:
            return search_key
        else:
            print('Input must be a string with at least 2 characters. Please try again.')


def main():
    """
        Generate animal information based on user input, filter by skin type, update the HTML template,
        and open it in a browser.

        This function interacts with the user to retrieve animal data, update an HTML template
        with the information,and display the output in a web browser. It handles cases where
        the animal does not exist or when the necessary template file is missing. The user is prompted
        to filter animals by skin type, and the chosen data is serialized into the HTML template.

        Raises:
            FileNotFoundError: If the HTML template file is missing.
            ValueError: If the API key is missing or invalid, or no data is fetched from the API.
    """

    search_key = get_animal_name()

    try:
        data = fetch_data(search_key)
        template = load_file("animals_template.html")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not data:
        animals_info = f"<h2>The animal \"{search_key}\" doesn't exist.</h2>"
    else:
        features = generate_list_of_features(data)
        display_menu(features)
        choice = get_user_choice(features)
        animals_info = serialize_animals(data) if choice == 0 else serialize_animals(data, features[choice])

    updated_template = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    write_file("animals.html", updated_template)
    open_browser("animals.html")


if __name__ == "__main__":
    main()
