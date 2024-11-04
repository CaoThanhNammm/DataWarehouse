from dao.staging import bikeDao

def add(url, bikeJson):
    response = bikeDao.add(url, bikeJson)
    if response.status_code == 200:
        return response.json()["data"]

