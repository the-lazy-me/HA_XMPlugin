import json
from requests import get

def states(url, token):
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }

    response = get(url, headers=headers)
    return response.json()