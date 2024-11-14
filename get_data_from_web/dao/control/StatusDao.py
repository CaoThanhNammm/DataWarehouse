import requests

def getStatusByName(url, type):
    response = requests.get(url + f"/{type}")
    return response
