import os
from dotenv import load_dotenv
import requests


API_URL = 'https://api.api-ninjas.com/v1/animals?name={}'


def load_api_key():
    """
        Loads the API key from environment variables.

        This function loads environment variables using `load_dotenv` and retrieves the API key
        from the 'API_KEY' environment variable. If the API key is missing or invalid
        (not 40 characters long),it raises a ValueError.

        Returns:
            str: The API key as a string.

        Raises:
            ValueError: If the API key is missing or invalid.
    """
    load_dotenv()
    api_key = os.getenv('API_KEY')

    if not api_key or len(api_key) != 40:
        raise ValueError(f"Invalid or missing API key [{api_key}]. Please check your .env file.")

    return api_key


def fetch_data(animal_name):
    """
    Fetches data about animals from an API based on the provided search key.

    This function sends a GET request to the animals API using the provided search key
    and returns a list of animal data if the request is successful. If the request
    fails, an error message is printed along with the status code and error details.

    Args:
        animal_name (str): The search term used to query the API for animal data.

    Returns:
        list: A list of dictionaries containing the animal data, or None if the request fails.

    Raises:
        requests.exceptions.HTTPError: If the request fails with a status code other than 200.
    """

    res = requests.get(API_URL.format(animal_name), headers={'X-Api-Key': load_api_key()})

    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        raise requests.exceptions.HTTPError(f"Error: {res.status_code}, {res.text}")
