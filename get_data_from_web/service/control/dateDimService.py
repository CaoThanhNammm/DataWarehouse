from dao.control import dateDimDao

def getIdToday(url, dateDimJson):
    response = dateDimDao.getIdToday(url, dateDimJson)
    if response.status_code == 200:
        return response.json()["data"]
