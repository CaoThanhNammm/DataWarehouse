from dao.control import ConfigDao

def findAll(url):
    response = ConfigDao.findAll(url)
    if response.status_code == 200:
        return response.json()["data"]

def getIdByKeyword(url, keyword):
    response = ConfigDao.getIdByKeyword(url, keyword)
    if response.status_code == 200:
        return response.json()["data"]

def inscreaseScrapeTimes(url, id):
    response = ConfigDao.inscreaseScrapeTimes(url, id)
    if response.status_code == 200:
        return response.json()["data"]

