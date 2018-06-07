import subprocess
from common.utils.HttpUtils import *

# def testPopen(cmd):
#     p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     while p.poll() is None:
#         line = p.stdout.readline().strip()
#         if line:
#             print(line)
#
#
# testPopen("ping 172.29.164.92")


list_url = "http://127.0.0.1:8005/rest/tool/list/"
list_data = {
"name":"test1"
}





add_url = "http://127.0.0.1:8005/rest/tool/add/"
add_data = {
"name":"test1",
"tool_type":"1",
"is_public":"1",
"infom":"1",
"command":"/11/11/11",
"param":"12231",
"script_lang":"shell",
}

update_url = "http://127.0.0.1:8005/rest/tool/updateById/"
update_data = {
    "id":1,
"name":"test",
"command":"/11/11/11",
"param":"{1111}",
"script_lang":"shell11",
}


delete_url = "http://127.0.0.1:8005/rest/tool/deleteByToolId/"
delete_data = {
    "tool_id":"1"
}


deploy_tool_url = "http://127.0.0.1:8005/rest/deploytool/updateById/"
deploy_tool_data = {
    "tool_id":"1"
}

# datas = json.dumps(deploy_tool_data)
# result = requests.post(deploy_tool_url, data=datas.encode('UTF-8'), auth=None,
#                          headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8",
#                                   "devopsgroup": 'ec', 'devopsuser': 'admin',
#                                   'clienttype': 'pc'}, timeout=10000)
# print(result.json())


# datas2 = json.dumps(list_data)
# result2 = requests.get(list_url,list_data,headers = {"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8",
#                                   "devopsgroup": 'ec', 'devopsuser': 'admin',
#                                   'clienttype': 'pc'},timeout=10000)
# print(result2.json())




a = "http:/asdf/asdf/aa"
print(a.startswith('http'))