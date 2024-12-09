import requests


def add(url, logJson):
    response = requests.post(url, json=logJson)
    return response

def isShouldRunning(url, logJson):
    response = requests.get(url, json=logJson)
    return response