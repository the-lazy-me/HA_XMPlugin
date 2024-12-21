import json
from requests import post

def services(url, token, entity_id):
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }

    data = {
        "entity_id": entity_id
    }

    response = post(url, headers=headers, data=json.dumps(data))
    return response