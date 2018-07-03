import requests,json

headers = {"Content-Type": "application/json", "devopsuser":"ec", "devopsgroup":"ec","clienttype":"PC"}

def get(url,datas):
    result = requests.get(url, datas,headers={"Content-Type": "application/json", "devopsgroup": 'ec','devopsuser': 'test', 'clienttype': 'pc'},timeout=10000)
    return result.json()



def post(url,datas):
    if datas is not None:
        if type(datas) == dict or type(datas) == list:
            datas = json.dumps(datas)
    return requests.post(url, data=datas.encode('UTF-8'),headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8","devopsgroup": 'ec', 'devopsuser': 'test','clienttype': 'pc'}, timeout=10000)



if __name__ == 'main':

    command_set = """
        {"id":7,"name":"command_set","tool_list":[{"id":57,"name":"test_comset1","tool_version":"1.1","time_out":600,"seq_no":1,"is_error_continue":0,"param":[{"key":"a","value":"111"},{"key":"b","value":"222"},{"key":"version_yumc","value":"version-1.1"},{"key":"jira_yumc","value":"jira-1.2"}],"command":"/opt/devops/tool_script/1530251594758sK6TF.sh"},[{"id":59,"name":"test_comset2","tool_version":"1.0","time_out":600,"seq_no":1,"is_error_continue":0,"param":[{"key":"e","value":"111"},{"key":"f","value":"222"},{"key":"version_yumc","value":"version-2.1"},{"key":"jira_yumc","value":"jira-2.2"}],"command":"/opt/devops/tool_script/1530252019138idrC0.sh"},{"id":60,"name":"test_comset3","tool_version":"1.0","time_out":600,"seq_no":1,"is_error_continue":0,"param":[{"key":"aa","value":"123"},{"key":"bb","value":"456"}],"command":"/opt/devops/tool_script/1530252296459AQG26.sh"}]]}
    """

