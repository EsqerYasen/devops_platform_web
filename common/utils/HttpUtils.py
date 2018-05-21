from devops_platform_web.settings import REST_API_CONFIG
import requests, json,time

class HttpUtils(object):

    def __init__(self, request):
        self.webRequest = request

    def get(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        result = requests.get(URLStr,datas,auth=auth,headers = {"Content-Type": "application/json","devopsgroup":self.webRequest.devopsgroup,'devopsuser':self.webRequest.devopsuser,'clienttype':self.webRequest.clienttype},timeout=10000)
        return result.json()

    def get_url(self,URLStr,datas=None,auth=()):
        return requests.get(URLStr,datas,auth=auth,headers = {"Content-Type": "text/html"},timeout=10000)

    def post(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        if datas is not None:
            if type(datas) == dict or type(datas) == list:
                datas = json.dumps(datas)
        return requests.post(URLStr,data=datas.encode('UTF-8'),auth=auth,headers = {"Content-Type": "application/json","Accept-Language":"zh-CN,zh;q=0.8","devopsgroup":self.webRequest.devopsgroup,'devopsuser':self.webRequest.devopsuser,'clienttype':self.webRequest.clienttype},timeout=10000)

    def getUrl(self,serviceName,restName):
        url = "http://%s%s" % (REST_API_CONFIG[serviceName]['ip_prot'],restName)
        return url

    def getRequestParam(self,hasEmpty=False):
        datas = {}
        webRequest = self.webRequest
        method = webRequest.method
        param = None
        if method == "GET":
            param = webRequest.GET
        if method == "POST":
            param = webRequest.POST

        offset2 = (webRequest.offset - 1) * 10
        limit = webRequest.limit
        datas["offset"] = offset2
        datas["limit"] = limit

        for d in param:
            if d in 'offset' or d in 'limit':
                continue
            value = param[d]
            if not hasEmpty and value:
                if ',' in value and not self.check_json_format(value):
                    datas[d] = '+'.join(value.split(','))
                else:
                    datas[d] = value
            if hasEmpty:
                datas[d] = value

        return datas

    def check_json_format(self,raw_msg):
        """
        用于判断一个字符串是否符合Json格式
        :param self:
        :return:
        """
        if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False




datas1 = {
    "code":"9ccd525d-eea7-4edd-9d15-ba777083ed6a",
    "client_id":"1112",
    "client_secret":"5c27b773b82241ccaf379317112c940d",
    "redirect_uri":"http://172.29.164.92:8002/checkLogin/",
    "grant_type":"authorization_code",
    "oauth_timestamp":time.time()
}

hu = HttpUtils(None)
result = hu.get_url("http://ssotest.hwwt2.com/openapi/oauth/token",datas1)
print(result.json())
if result.status_code == 200:
    access_token = result.json()['access_token']

    datas2 = {"access_token":access_token}
    result2 = hu.get_url("http://ssotest.hwwt2.com/openapi/oauth/userinfo",datas2)
    print(result2.json())
