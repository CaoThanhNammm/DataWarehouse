from dao.control import logDao


def add(url, logJson):
    response = logDao.add(url, logJson)
    if response.status_code == 200:
        return response.json()["data"]