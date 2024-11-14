from dao.staging import BikeDao

def add(url, bikeJson):
    response = BikeDao.add(url, bikeJson)
    if response.status_code == 200:
        return response.json()["data"]

def deleteAll(url):
    response = BikeDao.deleteAll(url)
    if response.status_code == 200:
        return response.json()["data"]
