from dao.control import EmailDao


def send(url, receiver, subject, message):
    response = EmailDao.send(url, receiver, subject, message)
    if response.status_code == 200:
        return response.json()["data"]
