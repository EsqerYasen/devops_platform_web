from suds.client import Client

def sudsClient(permission_list,client_id,client_secret):
    try:
        url = 'http://api.sso.hwwt2.com/openws/api/LPAccess?wsdl'
        client = Client(url)
        result = client.service.setPermission(permission_list, client_id, client_secret)
        print(result)
    except Exception as e:
        print(e)


ec_permission = [
    {"psid":"102452252","access":True},    #
    {"psid":"100540249","access":True},    #朱骏GCZ6626
    {"psid":"100316323","access":True},    #张利LXZ1064
    {"psid":"102459484","access":True},    #何立LCH7395
    {"psid":"102417503","access":True},    #龚英YCG4672
    {"psid":"101053466","access":True},    #常晓飞XXC3995
    {"psid":"100051806","access":True},    #施健JXS3744
    {"psid":"100051588","access":True},    #孙磊LXS5596
]

print('----------------------------ec PC开始-------------------------------')
sudsClient(ec_permission,'1112','5c27b773b82241ccaf379317112c940d')
print('----------------------------ec PC结束-------------------------------')
print('----------------------------ec H5开始-------------------------------')
sudsClient(ec_permission,'1113','32f4dfg455gfdgdfgdfg33223ddfsdfss')
print('----------------------------ec H5结束-------------------------------')


store_permission = [
    {"psid":"102452252","access":True},    #
    {"psid":"100042878","access":True},    #姚兴中XCY7144
    {"psid":"100025652","access":True},    #吴子麟ZXW5127
    {"psid":"102459484","access":True},    #何立LCH7395
    {"psid":"100051933","access":True},    #沈大年DXS7735
    {"psid":"100051482","access":True},    #严勇YXY0268
    {"psid":"100051806","access":True},    #施健JXS3744
]

print('----------------------------store PC开始-------------------------------')
sudsClient(store_permission,'1116','w83oahcnv7354565njcvbvjdhfjkfcns')
print('----------------------------store PC结束-------------------------------')
print('----------------------------store H5开始-------------------------------')
sudsClient(store_permission,'1117','63jdbg82365hjdhvjdfg2qtreegsnvlo')
print('----------------------------store H5结束-------------------------------')


brand_permission = [
    {"psid":"102452252","access":True},    #
    {"psid":"100426045","access":True},    #王韦WXW5675
    {"psid":"102452669","access":True},    #唐麒俊GCT2371
    {"psid":"102459484","access":True},    #何立LCH7395
    {"psid":"100226881","access":True},    #陈华HXC1920
    {"psid":"100054478","access":True},    #刘毅LXL2562
    {"psid":"100051806","access":True},    #施健JXS3744
    {"psid":"100426040","access":True},    #黄华刚 EXH9916
]

print('----------------------------brand PC开始-------------------------------')
sudsClient(brand_permission,'1114','8js923jg7dfjbvld7rkg8jkg7djna422')
print('----------------------------brand PC结束-------------------------------')
print('----------------------------brand H5开始-------------------------------')
sudsClient(brand_permission,'1115','nc823lfhd05ufhglsgq4385jgmnlrsna')
print('----------------------------brand H5结束-------------------------------')