import requests


def add(url, logJson):
    response = requests.post(url, json=logJson)
    return response
