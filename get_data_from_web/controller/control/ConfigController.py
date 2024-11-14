from service.control import ConfigService

def findAll(url):
    response = ConfigService.findAll(url)
    print('lấy tất cả thông tin website thành công')
    return response


def getIdByKeyword(url, keyword):
    response = ConfigService.getIdByKeyword(url, keyword)
    print('lấy thông tin website thành công')
    return response

def inscreaseScrapeTimes(url, id):
    response = ConfigService.inscreaseScrapeTimes(url, id)
    print('tăng số lần scrape website lên 1 thành công')
    return response
