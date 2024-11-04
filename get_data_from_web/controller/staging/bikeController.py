from service.staging import bikeService

def add(url, bikeJson):
    response = bikeService.add(url, bikeJson)
    print('thêm bike thành công')
    return response