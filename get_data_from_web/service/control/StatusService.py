from dao.control import StatusDao

def getStatusByName(url, type):
    response = StatusDao.getStatusByName(url, type)
    if response.status_code == 200:
        return response.json()['data']
