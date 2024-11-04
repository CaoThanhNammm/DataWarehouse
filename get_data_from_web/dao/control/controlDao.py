import requests

def getIdByKeyword(url, keyword):
    response = requests.get(url + f'/{keyword}')
    return response

def inscreaseScrapeTimes(url, id):
    response = requests.put(url + f'/{id}')
    return response