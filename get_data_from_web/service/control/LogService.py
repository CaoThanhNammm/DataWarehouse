from dao.control import LogDao


def add(url, logJson):
    response = LogDao.add(url, logJson)
    if response.status_code == 200:
        return response.json()["data"]

def isShouldRunning(url, logJson):
    response = LogDao.isShouldRunning(url, logJson)
    if response.status_code == 200:
        return response.json()["data"]