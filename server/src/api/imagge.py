"""
MODULE contains imagge api calls and functions
"""

import requests

API_KEY = "acc_5557b83c7ed338f"
API_SECRET = "89b4e5c98672d567b0d453efa9992243"
URL = "https://api.imagga.com/v2"
AUTH = (API_KEY, API_SECRET)


def get_tags(file):
    """
    Calls imagga for image tagging
    file: File
    return: list[str]
    """
    response = requests.post(URL + "/tags", auth=AUTH, files={"image": file})
    data = response.json()

    tags = data["result"]["tags"]

    # Saves just the tag key
    # Ignores confidence levels lower than 40
    res = [tag["tag"]["en"] for tag in tags if tag["confidence"] >= 40]

    return res
