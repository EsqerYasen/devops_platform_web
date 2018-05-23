from suds.client import Client

def sudsClient(permission_list,client_id,client_secret):
    try:
        url = 'http://api.sso.hwwt2.com/openws/api/LPAccess?wsdl'
        client = Client(url)
        result = client.service.setPermission(permission_list, client_id, client_secret)
        print(result)
    except Exception as e:
        print(e)


permission = [
    {"psid":"102459484","access":True},
    {"psid":"100540249","access":True},
    {"psid":"100316323","access":True},
    {"psid":"102417503","access":True},
    {"psid":"101053466","access":True},
    {"psid":"100051806","access":True},
    {"psid":"100051588","access":True},
    {"psid":"100051588","access":True},
]

print('----------------------------PC开始-------------------------------')
sudsClient(permission,'1112','5c27b773b82241ccaf379317112c940d')
print('----------------------------PC结束-------------------------------')
print('----------------------------H5开始-------------------------------')
sudsClient(permission,'1113','32f4dfg455gfdgdfgdfg33223ddfsdfss')
print('----------------------------H5结束-------------------------------')

