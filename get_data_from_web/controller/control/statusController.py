

from service.control import statusService

def getStatusByName(url, type):
    response =  statusService.getStatusByName(url, type)
    print('lấy trạng thái thành công')
    return response