from service.staging import BikeService

def add(url, bikeJson):
    response = BikeService.add(url, bikeJson)
    print('thêm bike thành công')
    return response

def deleteAll(url):
    response = BikeService.deleteAll(url)
    print('Xoá tất cả dữ liệu bike thành công')
    return response