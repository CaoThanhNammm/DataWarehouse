from service.control import controlService

def getIdByKeyword(url, keyword):
    response = controlService.getIdByKeyword(url, keyword)
    print('lấy thông tin website thành công')
    return response

def inscreaseScrapeTimes(url, id):
    response = controlService.inscreaseScrapeTimes(url, id)
    print('tăng số lần scrape website lên 1 thành công')
    return response
