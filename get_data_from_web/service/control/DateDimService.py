from dao.control import DateDimDao

def getIdToday(url, dateDimJson):
    response = DateDimDao.getIdToday(url, dateDimJson)
    if response.status_code == 200:
        return response.json()["data"]
