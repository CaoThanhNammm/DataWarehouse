from service.control import LogService

def add(url, logJson):
    response = LogService.add(url, logJson)
    print('thêm log thành công')
    return response

def isShouldRunning(url, logJson):
    response = LogService.isShouldRunning(url, logJson)
    print('Có nên lấy dữ liệu hay không')
    return response
