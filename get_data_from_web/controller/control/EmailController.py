from service.control import EmailService

def send(url, receiver, subject, message):
    response = EmailService.send(url, receiver, subject, message)
    if response == 'None':
        print('gửi email thông báo không thành công')
    else:
        print('gửi email thông báo thành công')

    return response

