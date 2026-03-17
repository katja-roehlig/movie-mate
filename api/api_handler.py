import requests
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
API_KEY = os.getenv("API_KEY")


def get_movie_info_per_title(title):
    """
    fetches information about a movie title from the API

    :param title: movie title
    :return title, year, rating, image
    """
    request_url = "https://www.omdbapi.com/?"
    params = {"apikey": API_KEY, "t": title}
    try:
        response = requests.get(request_url, params=params)
        data = response.json()
        if data.get("Response") == "False":
            return False
        else:
            return (
                data["Title"],
                data["Year"],
                data["Director"],
                data.get("Poster", "N/A"),
            )
    except (requests.exceptions.ConnectionError, requests.exceptions.TimeoutError):
        return None
