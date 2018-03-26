from devops_platform_web.settings import REST_API_CONFIG
import requests, json

class HttpUtils(object):

    def __init__(self, request):
        self.webRequest = request

    def get(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        result = requests.get(URLStr,datas,auth=auth,headers = {"Content-Type": "application/json","devopsgroup":self.webRequest.devopsgroup,'devopsuser':self.webRequest.devopsuser})
        return result.json()

    def post(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        if datas is not None:
            if type(datas) == dict or type(datas) == list:
                datas = json.dumps(datas)
        return requests.post(URLStr,data=datas.encode('UTF-8'),auth=auth,headers = {"Content-Type": "application/json","Accept-Language":"zh-CN,zh;q=0.8","devopsgroup":self.webRequest.devopsgroup,'devopsuser':self.webRequest.devopsuser})

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
                if ',' in value:
                    datas[d] = '+'.join(value.split(','))
                else:
                    datas[d] = value
            if hasEmpty:
                datas[d] = value

        return datas