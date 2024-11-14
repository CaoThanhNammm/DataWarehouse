from service.control import DateDimService

def getIdToday(url, dateDimJson):
    response = DateDimService.getIdToday(url, dateDimJson)
    if response:
        print('lấy id của ngày hôm nay trong datedim thành công')
        return response
    print('lấy id của ngày hôm nay trong datedim thất bại')


# url = "http://192.168.101.7:8080/api/dateDim/id"
# dateDimJson = {
#     "fullDate": "2024-11-12"
# }
# print(getIdToday(url, dateDimJson))