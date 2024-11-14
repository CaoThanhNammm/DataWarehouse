from service.control import StatusService

def getStatusByName(url, type):
    response =  StatusService.getStatusByName(url, type)
    print('lấy trạng thái thành công')
    return response