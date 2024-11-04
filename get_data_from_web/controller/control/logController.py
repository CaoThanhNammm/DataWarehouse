from service.control import logService

def add(url, logJson):
    response = logService.add(url, logJson)
    print('thêm log thành công')
    return response