import requests


def getIdToday(url, dateDimJson):
    response = requests.get(url, json=dateDimJson)
    return response
