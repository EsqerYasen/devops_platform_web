from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from common.utils.HttpUtils import *
from common.utils.redis_utils import RedisBase
from django.views.decorators.csrf import csrf_exempt
from dwebsocket.decorators import accept_websocket
from dwebsocket import require_websocket
import threading
import logging
import time

logger = logging.getLogger('devops_platform_log')
# Create your views here.
def index(request):
    return render(request, 'slb/index.html')

def site_list(request):
    return render(request, 'slb/site_list.html')

def site(request):
    return render(request, 'slb/site.html')

def upstream(request):
    return render(request, 'slb/upstream.html')

def upstream_list(request):
    return render(request, 'slb/upstream_list.html')

def deploy_task(request):
    return render(request, 'slb/deploy_task.html')

def deploy_manage(request):
    return render(request, 'slb/deploy_manage.html')

def trans_cluster_list(cluster_list):
    load_balancin_strategy_dict = {
        1: 'ip-hash',
        2: 'round-robin',
        3: 'consistent_hash_rid',
        4: 'consistent_hash_arg_requestId',
        'ip-hash': 1,
        'round-robin': 2,
        'consistent_hash_rid': 3,
        'consistent_hash_arg_requestId': 4
    }
    check_up_type_dict = {
        1: 'TCP',
        2: 'HTTP',
        'TCP': 1,
        'HTTP': 2,
    }
    ret = []
    for cluster in cluster_list:
        tmp = str(cluster['id'])
        cluster.update({'id': tmp})
        if cluster['check_up_type']:
            tmp = check_up_type_dict[cluster['check_up_type']]
            cluster.update({'check_up_type': tmp})
        if cluster['load_balancin_strategy']:
            tmp = load_balancin_strategy_dict[cluster['load_balancin_strategy']]
            cluster.update({'load_balancin_strategy': tmp})
        ret.append(cluster)
    return ret

def serviceClusterList(request):
    hu = HttpUtils(request)
    #reqData = hu.getRequestParam()
    #physical = reqData.get("physical","")
    #deployment_environment = reqData.get("deployment_environment","")
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/serviceclusterlist/")
    #print(setListResult)
    #/rest/slb/serviceclusterbyid/
    ret = setListResult.get("results", [])
    #print('ret is %s'% ret)
    #ret = {
        #"count": 1,
        #"next": 'null',
        #"previous": 'null',
        #"results": [
            #{
                #"id": "1",
                #"create_time": "2018-08-28 17:35:36",
                #"update_time": "2018-08-28 17:35:38",
                #"cluster_name": "kfc_preorder_nh_pilot_idc_nginx",
                #"check_up_timeout": 3000,
                #"load_balancin_strategy": 1,
                #"check_up_space": 3000,
                #"check_up_type": 1,
                #"keep_alive": 20,
                #"pool_down_ratio": 'null',
                #"pool_force_down": 'null',
                #"is_enabled": True,
                #"created_by": "admin",
                #"updated_by": "admin"
            #}
        #]
    #}
    data = trans_cluster_list(ret)
    #print(data)
    return JsonResponse(data=dict(ret=data))

def trans_cluster_detail(cluster_detail, reverser=False):
    load_balancin_strategy_dict = {
        1: 'ip-hash',
        2: 'round-robin',
        3: 'consistent_hash_rid',
        4: 'consistent_hash_arg_requestId',
        'ip-hash': 1,
        'round-robin': 2,
        'consistent_hash_rid': 3,
        'consistent_hash_arg_requestId': 4
    }
    check_up_type_dict = {
        1: 'TCP',
        2: 'HTTP',
        3:'ssl_hello',
        4:'mysql',
        5:'ajp',
        'TCP': 1,
        'HTTP': 2,
        'ssl_hello': 3,
        'mysql': 4,
        'ajp': 5
    }
    node_state_dict = {
        1: 'enable',
        4: 'down',
        5: 'backup',
        'enable': 1,
        'down': 4,
        'backup': 5
    }
    pop_list = ['created_by', 'updated_by']
    #print(type(cluster_detail['load_balancin_strategy']))

    if cluster_detail['load_balancin_strategy']: 
        tmp = load_balancin_strategy_dict[cluster_detail['load_balancin_strategy']]
        cluster_detail.update({'load_balancin_strategy':tmp})
    if cluster_detail['check_up_type']:
        tmp = check_up_type_dict[cluster_detail['check_up_type']]
        cluster_detail.update({'check_up_type':tmp})
    tmp = int(cluster_detail['id'])
    cluster_detail.update({'id':tmp})
    nodes = cluster_detail['cluster_nodes']
    tmp_nodes = []
    for n in nodes:
        tmp = node_state_dict[n['state']]
        n.update({'state': tmp})
        tmp_nodes.append(n)
    cluster_detail.update({'cluster_nodes':tmp_nodes})
    if reverser:
        for key in pop_list:
            if key in cluster_detail:
                cluster_detail.pop(key)
    return cluster_detail 

@csrf_exempt
def serviceClusterByID(request):
    #data={
            #"id":1,
            #"cluster_name":"kfc_preorder_nh_pilot_idc_nginx",
            #"check_up_timeout":3000,
            #"load_balancin_strategy":1,
            #"check_up_space":3000,
            #"check_up_type":1,
            #"keep_alive":20,
            #"pool_down_ratio": 'null',
            #"pool_force_down": 'null',
            #"is_enabled": True,
            #"created_by":"admin",
            #"updated_by":"admin",
            #"cluster_nodes":[
                #{"id":1,
                #"host_id":1,
                #"service_cluster_id":1,
                #"port":80,
                #"weight":30,
                #"max_fails":20,
                #"fail_timeout":40,
                #"state":1,
                #"host_ip":"1.1.1.1"
                #}]
        #}
    hu = HttpUtils(request)
    if request.method == 'GET':
        upstream_id = int(request.GET.get('id'))
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/serviceclusterbyid/", datas={'id': upstream_id})
        #print(setListResult)
        data = trans_cluster_detail(setListResult)
        return JsonResponse(data=dict(ret=data))
    elif request.method == 'POST':
        #print('str(request.body, 'utf-8'): %s' % str(request.body, 'utf-8'))
        data = json.loads(str(request.body, 'utf-8'))
        #try:
            #assert operation in ['create', 'update']
        #except AssertionError:
            #return JsonResponse(data=dict(status=500, msg="unsupported operation orz"))
        cluster_data = trans_cluster_detail(data, reverser=True)
        if data['id'] < 0:
            restName = "/rest/slb/serviceclustercreate/"
        else:
            restName = "/rest/slb/serviceclusterupdate/"
        #print('cluster_data: %s'%cluster_data)
        setListResult = hu.post(serivceName="p_job", restName=restName, datas=cluster_data)
        #print(json.loads(setListResult.content))
        #{'service_cluster_id': 12, 'status': 200, 'msg': '新增成功'}
        ret = setListResult.json()
        return JsonResponse(data=ret)

def del_servicecluster(request):
    upstream_id = int(request.GET.get('id'))
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/serviceclusterbyid/", datas={'id': upstream_id})
    #print(setListResult)
    data = trans_cluster_detail(setListResult)
    return JsonResponse(data=dict(ret=data))

def trans_siteList(siteList):
    ret = []
    for site in siteList:
        tmp_id = str(site['id'])
        site.update({'id': tmp_id})
        ret.append(site)
    return ret

def trans_siteInfo(site_info):
    state_control_dict = { 1:'enable', 0:'disable', 2:'force_offline','enable':1,'disable':0 ,'force_offline':2}
    #is_https_dict = { 0: False, 1: True,'true':1,'false':0 }
    tmp_id = str(site_info['id'])
    tmp_is_https = int(site_info['is_https']) if type(site_info['is_https']) is bool else bool(site_info['is_https'])
    tmp_state_control = state_control_dict[site_info['state_control']]
    tmp = {'id': tmp_id, 'is_https': tmp_is_https, 'state_control': tmp_state_control}
    site_info.update(tmp)
    return site_info

@csrf_exempt
def siteList(request):
    hu = HttpUtils(request)
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/getMngSiteList/")
    ret = setListResult.get("results", [])
    data = trans_siteList(ret)
    return JsonResponse(data=dict(ret=data))

@csrf_exempt
def siteInfo(request):
    if request.method == 'GET':
        site_id = int(request.GET.get('id'))
        hu = HttpUtils(request)
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/getMngSiteInfo/", datas={'id':site_id})
        ret = setListResult.get("results", {})
        data = trans_siteInfo(ret)
        return JsonResponse(data=dict(ret=data))

@csrf_exempt
def del_site(request):
    site_id = int(request.GET.get('id'))
    #print(site_id)
    hu = HttpUtils(request)
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/deleteMngSite/", datas={'id':site_id})
    return JsonResponse(data=dict(ret=setListResult))

def trans_mappingRule(mpr):
    #case_sensitive_dict = {1: True, 0: False, True: 1, False: 0}
    https_type_dict = { 1: 'all', 2: 'http', 3: 'https', 'all': 1, 'http': 2, 'https': 3}
    matching_type_dict = { 1: 'prefix', 2: 'regex', 3:'common', 4:'exact', 'prefix':1, 'regex': 2, 'common': 3, 'exact':4 }

    #tmp_case_sensitive = case_sensitive_dict[mpr['case_sensitive']]
    tmp_case_sensitive = int(mpr['case_sensitive']) if type(mpr['case_sensitive']) is bool else bool(mpr['case_sensitive'])
    tmp_https_type = https_type_dict[mpr['https_type']]
    tmp_matching_type = matching_type_dict[mpr['matching_type']]
    mpr.update(
        {
            'case_sensitive': tmp_case_sensitive,
            'matching_type': tmp_matching_type,
            'https_type': tmp_https_type
        }
    )
    cmd_list = trans_cmdList(mpr['cmd_list'])
    mpr.update({'cmd_list': cmd_list})
    return mpr

def trans_mappingRuleList(mprulelist, cmd_list_flag=False):
    #case_sensitive_dict = {1: True, 0: False, True: 1, False: 0}
    https_type_dict = { 1: 'all', 2: 'http', 3: 'https', 'all': 1, 'http': 2, 'https': 3 }
    matching_type_dict = {
        1: 'prefix',
        2: 'regex',
        3:'common',
        4:'exact',
        'prefix': 1,
        'regex': 2,
        'common': 3,
        'exact': 4
    }
    ret = []
    for mpr in mprulelist:
        tmp_id = str(mpr['id'])
        tmp_nginx_site_id = str(mpr['nginx_site_id'])

        #tmp_case_sensitive = case_sensitive_dict[mpr['case_sensitive']]
        tmp_case_sensitive = int(mpr['case_sensitive']) if type(mpr['case_sensitive']) is bool else bool(mpr['case_sensitive'])
        tmp_https_type = https_type_dict[mpr['https_type']]
        tmp_matching_type = matching_type_dict[mpr['matching_type']]
        mpr.update(
            {
                'id': tmp_id, 
                'nginx_site_id': tmp_nginx_site_id, 
                'case_sensitive': tmp_case_sensitive,
                'matching_type': tmp_matching_type,
                'https_type': tmp_https_type
            }
        )
        if cmd_list_flag:
            cmd_list = trans_cmdList(mpr['cmd_list'])
            mpr.update({'cmd_list': cmd_list})
        ret.append(mpr)
    return ret

@csrf_exempt
def mappingRuleList(request):
    if request.method == 'GET':
        nginx_site_id = int(request.GET.get('nginx_site_id'))
        hu = HttpUtils(request)
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/getMappingRulesList/", datas={'nginx_site_id':nginx_site_id})
        ret = setListResult.get("results", [])
        #print(ret)
        data = trans_mappingRuleList(ret)
        return JsonResponse(data=dict(ret=data))

@csrf_exempt
def del_mappingrule(request):
    if request.method == 'GET':
        #nginx_site_id = int(request.GET.get('nginx_site_id'))
        mid = int(request.GET.get('id'))
        #print('id :%s' % mid)
        hu = HttpUtils(request)
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/deleteMappingRules/", datas={'id': mid})
        print(setListResult)
        return JsonResponse(data=dict(ret=setListResult))
    
def trans_cmdList(cmd_list):
    command_type_dict = {
        1: 'access_log', 
        2: 'custom',
        3: 'ifelse', 
        4: 'more_clear_headers', 
        5: 'proxy_pass', 
        6: 'return',
        7: 'rewrite',
        8: 'static-resource',
        9: 'include',
        10: 'more_set_headers',
        'access_log': 1, 
        'custom': 2,
        'ifelse': 3, 
        'more_clear_headers': 4, 
        'proxy_pass': 5, 
        'return': 6,
        'rewrite': 7,
        'static-resource': 8,
        'include': 9,
        'more_set_headers': 10
    }
    ret = []
    for cmd in cmd_list:
        tmp_command_type = command_type_dict[cmd['command_type']]
        cmd.update({'command_type': tmp_command_type})
        ret.append(cmd)
    return ret


@csrf_exempt
def cmdList(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        hu = HttpUtils(request)
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/getMappingRulesInfo/", datas={'id':id})
        #print(setListResult)
        ret = setListResult.get("results", {})
        #print(ret['cmd_list'])
        cmd_list = trans_cmdList(ret['cmd_list'])
        return JsonResponse(data=dict(ret={'id':id, 'cmd_list': cmd_list}))

def trans_versions(versions):
    status_dict = {
        '0':"新版本未发布",
        '1':"成功",
        '2':"失败",
        '3':"部分失败"
    }
    ret = []
    for v in versions:
        tmp_status = status_dict[v['status']]
        v.update({'status': tmp_status})
        ret.append(v)
    return ret

@csrf_exempt
def site_versions(request):
    id = int(request.GET.get('id'))
    hu = HttpUtils(request)
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/deployversionbysiteid/", datas={'site_id':id})
    #print(setListResult)
    #setListResult = trans_versions(setListResult)
    return JsonResponse(data={'ret':setListResult})
    
@csrf_exempt
def create_site_version(request):
    id = int(request.GET.get('id'))
    hu = HttpUtils(request)
    setListResult = hu.get(serivceName="p_job", restName="/rest/slb/deployversioncreateview/", datas={'site_id':id})
    #{'task_id': 5, 'msg': '创建版本成功', 'status': 200, 'version': 4, 'site_id': '1'}
    return JsonResponse(data={'ret':setListResult})

@csrf_exempt
def MngSiteCreateOrUpdate(request):
    results = {}
    try:
        input_param = json.loads(str(request.body, 'utf-8'))
        if input_param:
            id = input_param['id']
            hu = HttpUtils(request)
            input_param = trans_siteInfo(input_param)
            if int(id) < 0:
                del input_param['id']
                post_results = hu.post(serivceName='p_job', restName='/rest/slb/addMngSite/', datas=input_param)
                post_results = post_results.json()
                if post_results['status'] == 200:
                    results['status'] = 200
                    results['msg'] = "新增成功"
                    results['id'] = post_results['id']
                else:
                    results['status'] = 500
                    results['msg'] = "新增失败"
            elif int(id) > 0:
                post_results = hu.post(serivceName='p_job', restName='/rest/slb/updateMngSite/',datas=input_param)
                post_results = post_results.json()
                if post_results['status'] == 200:
                    results['status'] = 200
                    results['msg'] = "修改成功"
                else:
                    results['status'] = 500
                    results['msg'] = "修改失败"
        else:
            results['status'] = 500
            results['msg'] = "参数为空"
    except Exception as e:
        logger.error(e, exc_info=1)
        results['status'] = 500
        results['msg'] = "新增或更新异常"
    return JsonResponse(data=results)


@csrf_exempt
def MappingRulesCreateOrUpdate(request):
    results = {}
    try:
        input_param = json.loads(str(request.body, 'utf-8'))
        if input_param:
            id = input_param['id']
            hu = HttpUtils(request)
            if int(id) < 0:
                input_param = trans_mappingRule(input_param)
                del input_param['id']
                post_results = hu.post(serivceName='p_job', restName='/rest/slb/addMappingRules/', datas=input_param)
                post_results = post_results.json()
                if post_results['status'] == 200:
                    results['status'] = 200
                    results['msg'] = "新增成功"
                    results['id'] = post_results['id']
                else:
                    results['status'] = 500
                    results['msg'] = "新增失败"
            else:
                mapping_rules_list = input_param['mapping_rules_list']
                new_mapping_rules_list = []
                for mapping_rule in mapping_rules_list:
                    tmp = trans_mappingRule(mapping_rule)
                    new_mapping_rules_list.append(tmp)
                input_param.update({'mapping_rules_list': new_mapping_rules_list})
                print(input_param)
                post_results = hu.post(serivceName='p_job', restName='/rest/slb/updateMappingRules/',datas=input_param)
                post_results = post_results.json()
                if post_results['status'] == 200:
                    results['status'] = 200
                    results['msg'] = "修改成功"
                else:
                    results['status'] = 500
                    results['msg'] = "修改失败"
        else:
            results['status'] = 500
            results['msg'] = "参数为空"
    except Exception as e:
        results['status'] = 500
        results['msg'] = "新增或更新异常"
        logger.error(e,exc_info=1)
    return JsonResponse(data=results)

@csrf_exempt
def NginxClusterTree(request):
    results = {}
    try:
        hostGroup_list = RedisBase.get("host_group_1", 2)
        results['status'] = 200
        results['data'] = str(hostGroup_list,encoding='utf-8')
    except Exception as e:
        logger.error(e,exc_info=1)
        results['status'] = 500
        results['msg'] = "查询异常"
    return JsonResponse(data=results)

@csrf_exempt
def GetHostListByGrupId(request):
    results = {}
    try:
        group_id = request.GET['group_id']
        if group_id:
            hu = HttpUtils(request)
            setListResult = hu.get(serivceName="cmdb", restName="/rest/slb/nginxclusterhostbyid/",datas={'group_id': group_id})
            results['status'] =  200
            results['data'] = setListResult
    except Exception as e:
        logger.error(e,exc_info=1)
        results['status'] = 500
        results['msg'] = "查询异常"
    return JsonResponse(data=results)

@csrf_exempt
def NginxClusterHostById(request):
    """
    发布 获取nginx 机器
    :param request:
    :return:
    """
    results = {}
    try:
        group_id = request.GET.get("id", None)
        vs = request.GET.get("vs", None)
        if group_id and vs:
            hu = HttpUtils(request)
            result = hu.get(serivceName='p_job', restName='/rest/slb/nginxclusterhostbyid', datas={"id": group_id, "vs": vs})
            if result['status'] == 200:
                results['status'] = 200
                results['data'] = result['data']
            else:
                results['status'] = 500
                results['msg'] = "查询失败"
        else:
            results['status'] = 500
            results['msg'] = "查询参数为空"
    except Exception as e:
        logger.error(e, exc_info=1)
        results['status'] = 500
        results['msg'] = "查询异常"
    return JsonResponse(data=results)

@csrf_exempt
def deploy_agent(request):
    if request.method == 'POST':
        data = json.loads(str(request.body, 'utf-8'))
        site_id = data['id']
        #site_name = data['site_name']
        host_list = data['hosts']
        version = data['version']
        hu = HttpUtils(request)
        result = hu.post(serivceName='p_job', restName='/rest/slb/deployagent/', datas={"id": site_id, "version": version, 'hosts':host_list})
        return JsonResponse(data=result.json())

def trans4configpreview(config_data):
    new_dy = {}
    dynamicAttrs = config_data['dynamicAttributes']
    for dy in dynamicAttrs:
        new_dy.update({dy['param_key']: dy['param_value']})
    config_data.update({'dynamicAttributes': new_dy})
    return config_data

@csrf_exempt
def config_preview(request):
    if request.method == 'POST':
        data = str(request.body, 'utf-8')
        data = json.loads(data)
        siteDetail = data['siteDetail']
        siteDetail = trans_siteInfo(siteDetail)
        #siteDetail = trans4configpreview(siteDetail)
        mplist = data['mplist']
        mplist = trans_mappingRuleList(mplist, cmd_list_flag=True)
        hu = HttpUtils(request)
        siteDetail.update({'locations': mplist})
        result = hu.post(serivceName='p_job',restName='/rest/slb/configpreview/', datas=siteDetail)
        result = result.json()
        return JsonResponse(data=dict(ret=result))

def config_version_diff(request):
        results = {}
        try:
            req_get = request.GET
            id = req_get.get("id", None)
            v1 = req_get.get("v1", None)
            v2 = req_get.get("v2", None)
            if id and v1 and v2:
                hu = HttpUtils(request)
                result = hu.get(serivceName='p_job', restName='/rest/slb/configversiondiff',datas={"id": id, "v1": v1,"v2":v2})
                if result['status'] == 200:
                    results['status'] = 200
                    results['data'] =  result['data']
                else:
                    results['status'] = 500
                    results['msg'] = "查询失败"
        except Exception as e:
            logger.error(e,exc_info=1)
        return JsonResponse(data=results)

def get_server_status(site_id):
    server_status_dict = RedisBase.hgetAll(site_id, db=5)
    ret_server_status_list = [{'ip': str(k, 'utf-8'), 'status': str(v, 'utf-8')} for k,v in server_status_dict.items() ]
    return ret_server_status_list

@require_websocket
def rtlog(request):
    message = request.websocket.wait()
    message = json.loads(str(message, 'utf-8'))
    tmp_msg = message['ip_list']
    site_id = int(message['site_id'])
    server_list = [m['host_ip'] for m in tmp_msg]
    while(message):
        data = get_server_status(site_id)
        data = json.dumps(data)
        datab = data.encode(encoding='utf-8', errors = 'strict')
        request.websocket.send(datab)
        message = request.websocket.wait()
        time.sleep(3)
    return HttpResponse('close') 

def get_nginx_log(request):
    ip = request.GET.get('ip', None)
    deployId = request.GET.get('deployId', None)
    version = request.GET.get('version', None)
    siteId = request.GET.get('siteId', None)
    result = {'log':''}
    if all([ip, deployId, version, siteId]):
        hu = HttpUtils(request)
        data={'ip':ip, 'siteId':siteId, 'deployId': deployId, 'version': version}
        result = hu.get(serivceName='p_job',restName='/rest/slb/nginxdeploylogsbyip', datas=data)
    return JsonResponse(data=result)

def trans_deploytask(task):
    task_status_dict = {0: 'running', 1: 'success', 2: 'fail'}
    status = task['status']
    new_status = task_status_dict[status]
    task.update({'status': new_status})
    return task

def get_deploytaskslist(request):
    hu = HttpUtils(request)
    result = hu.get(serivceName='p_job',restName='/rest/slb/deploytaskslist/')
    for index, task in enumerate(result['results']):
        task = trans_deploytask(task)
        result['results'][index] = task
    return JsonResponse(data=dict(ret=result))


