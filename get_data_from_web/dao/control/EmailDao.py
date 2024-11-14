import requests

def send(url, receiver, subject, message):
    response = requests.get(url, params={
        "receiver": receiver,
        "subject": subject,
        "message": message
    })
    return response


