from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from common.utils.HttpUtils import *
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('devops_platform_log')
# Create your views here.
def index(request):
    return render(request, 'slb/index.html')

def site(request):
    return render(request, 'slb/site.html')

def upstream(request):
    return render(request, 'slb/upstream.html')

def deploy_task(request):
    return render(request, 'slb/deploy_task.html')

def deploy_manage(request):
    return render(request, 'slb/deploy_manage.html')

def trans_cluster_list(cluster_list):
    ret = []
    for cluster in cluster_list:
        tmp = str(cluster['id'])
        cluster.update({'id': tmp})
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
        'TCP': 1,
        'HTTP': 2,
    }
    node_state_dict = {
        1: 'enable',
        4: 'down',
        5: 'backup',
        'enable': 1,
        'down': 4,
        'backup': 5
    }
    pop_list = ['id', 'created_by', 'updated_by']
    #print(type(cluster_detail['load_balancin_strategy']))

    tmp = load_balancin_strategy_dict[cluster_detail['load_balancin_strategy']]
    cluster_detail.update({'load_balancin_strategy':tmp})
    tmp = check_up_type_dict[cluster_detail['check_up_type']]
    cluster_detail.update({'check_up_type':tmp})
    nodes = cluster_detail['cluster_nodes'] 
    tmp_nodes = []
    for n in nodes:
        tmp = node_state_dict[n['state']]
        n.update({'state': tmp})
        tmp_nodes.append(n)
    cluster_detail.update({'cluster_nodes':tmp_nodes})
    if reverser:
        for key in pop_list:
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
        #print('request.body: %s' % request.body)
        data = json.loads(request.body)
        operation = data['operation']
        cluster_data = data['data']
        if operation == 'create':
            restName = "/rest/slb/serviceclustercreate/"
            cluster_data = trans_cluster_detail(cluster_data, reverser=True)
        elif operation == 'update':
            restName = "/rest/slb/serviceclusterupdate/"
        #print('cluster_data: %s'%cluster_data)
        try:
            assert operation in ['create', 'update']
        except AssertionError:
            return JsonResponse(data=dict(status=500, msg="unsupported operation orz"))
        setListResult = hu.post(serivceName="p_job", restName=restName, datas=cluster_data)
        #print(json.loads(setListResult.content))
        #{'service_cluster_id': 12, 'status': 200, 'msg': '新增成功'}
        ret = json.loads(setListResult.content)
        return JsonResponse(data=ret)

def trans_siteList(siteList):
    ret = []
    for site in siteList:
        tmp_id = str(site['id'])
        site.update({'id': tmp_id})
        ret.append(site)
    return ret

def trans_siteInfo(site_info):
    state_control_dict = { 1:'enable', 0:'disable', 2:'forced_offline' }
    is_https_dict = { 0: False, 1: True }
    tmp_id = str(site_info['id'])
    tmp_is_https = is_https_dict[site_info['is_https']]
    tmp_state_control = state_control_dict[site_info['is_https']]
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

def trans_mappingRuleList(mprulelist):
    case_sensitive_dict = {1: True, 0: False}
    https_type_dict = { 1: 'all', 2: 'http', 3: 'https' }
    matching_type_dict = { 1: 'prefix', 2: 'regex', 3:'common', 4:'exact' }
    ret = []
    for mpr in mprulelist:
        tmp_id = str(mpr['id'])
        tmp_nginx_site_id = str(mpr['nginx_site_id'])

        tmp_case_sensitive = case_sensitive_dict[mpr['case_sensitive']]
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
        ret.append(mpr)
    return ret

@csrf_exempt
def mappingRuleList(request):
    if request.method == 'GET':
        nginx_site_id = int(request.GET.get('nginx_site_id'))
        hu = HttpUtils(request)
        setListResult = hu.get(serivceName="p_job", restName="/rest/slb/getMappingRulesList/", datas={'nginx_site_id':nginx_site_id})
        ret = setListResult.get("results", [])
        data = trans_mappingRuleList(ret)
        return JsonResponse(data=dict(ret=data))
    
def trans_cmdList(cmd_list):
    command_type_dict = {
        1: 'access_log', 
        2: 'custom',
        3: 'ifelse', 
        4: 'more_clear_headers', 
        5: 'more_set_headers', 
        6: 'proxy_pass',
        7: 'return',
        8: 'rewrite',
        9: 'static-resource'
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
        0:"新版本未发布",
        1:"成功",
        2:"失败",
        3:"部分失败"
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
    setListResult = trans_versions(setListResult)
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
        input_param = json.loads(request.body)
        if input_param:
            id = input_param['id']
            hu = HttpUtils(request)
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
                    results['msg'] = "新增成功"
                    results['id'] = post_results['id']
                else:
                    results['status'] = 500
                    results['msg'] = "新增失败"
        else:
            results['status'] = 500
            results['msg'] = "新增参数为空"
    except Exception as e:
        logger.error(e, exc_info=1)
        results['status'] = 500
        results['msg'] = "新增异常"
    return JsonResponse(data=results)