from service.control import EmailService

def send(url, receiver, subject, message):
    response = EmailService.send(url, receiver, subject, message)
    if not response == 'None':
        print('gửi email thông báo không thành công')
    else:
        print('gửi email thông báo thành công')

    return response

