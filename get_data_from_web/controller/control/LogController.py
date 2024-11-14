from service.control import LogService

def add(url, logJson):
    response = LogService.add(url, logJson)
    print('thêm log thành công')
    return response