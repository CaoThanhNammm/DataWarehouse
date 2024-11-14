import requests

def add(url, bikeJson):
    response = requests.post(url, json=bikeJson)
    return response

def deleteAll(url):
    response = requests.delete(url)
    return response