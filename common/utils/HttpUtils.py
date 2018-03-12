from devops_platform_web.settings import REST_API_CONFIG
import requests, json

class HttpUtils():

    def get(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        result = requests.get(URLStr,datas,auth=auth,headers = {"Content-Type": "application/json"})
        return result.json()

    def post(self,serivceName,restName,datas=None,auth=()):
        URLStr = self.getUrl(serivceName, restName)
        if datas is not None:
            if type(datas) == dict or type(datas) == list:
                datas = json.dumps(datas)
        return requests.post(URLStr,data=datas.encode('UTF-8'),auth=auth,headers = {"Content-Type": "application/json","Accept-Language":"zh-CN,zh;q=0.8"})

    def getUrl(self,serviceName,restName):
        url = "http://%s%s" % (REST_API_CONFIG[serviceName]['ip_prot'],restName)
        return url