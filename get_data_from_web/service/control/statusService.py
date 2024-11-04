from dao.control import statusDao

def getStatusByName(url, type):
    response = statusDao.getStatusByName(url, type)
    if response.status_code == 200:
        return response.json()['data']
