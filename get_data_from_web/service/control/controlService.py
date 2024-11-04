from dao.control import controlDao

def getIdByKeyword(url, keyword):
    response = controlDao.getIdByKeyword(url, keyword)
    if response.status_code == 200:
        return response.json()["data"]

def inscreaseScrapeTimes(url, id):
    response = controlDao.inscreaseScrapeTimes(url, id)
    if response.status_code == 200:
        return response.json()["data"]