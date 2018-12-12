from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.conf import settings
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from common.utils.HttpUtils import *
from .cell_utils import *
from .Template import Template
# from django.forms.models import model_to_dict
# from django.utils import timezone
# from rest_framework.views import APIView

import json
import os
import hashlib
import time
import xlrd

def template_index(request):
    resp = render(request, 'cell/cell_template_index.html')
    return resp

def template_log(request):
    try:
        template_id = request.GET['template_id']
        t_logs = Template.get_log(template_id)
        return JsonResponse(dict(status=200, data=t_logs))
    except Exception as e:
        print(e)
        return JsonResponse(dict(status=500, msg='fail'))

@csrf_exempt
def cell_template(request):
    if request.method == 'GET':
        template_id = request.GET.get('template_id','')
        try:
            if template_id:
                template = Template.get(template_id)
                assert template is not None
                services =[]
                func = lambda x: x.split('_')[-1]
                x = sorted(template.keys(), key=func)
                for key in x:
                    # if not key in ['creator', 'name', 'version', 'id']:
                    if not isinstance(template[key], (str, int)): 
                        services.append(template[key])
                template.update(dict(services=services))
                return JsonResponse(dict(status=200, data=template))
            else:
                templates = Template.list_templates()
                return JsonResponse(dict(status=200, data=templates))
            # return a
        except Exception as e:
            print(e)
            return JsonResponse(dict(status=500, msg='fail'))

    if request.method == 'POST':
        action = request.POST.get('action', '')
        template_id = request.POST.get('template_id', '')
        
        try:
            assert action in ['create', 'update', 'delete']
            if action == 'create':
                template_data = json.loads(request.POST.get('template', ''))
                template_data.update(dict(creator=request.devopsuser))
                t = Template(template_data)
                template_id = t.save()
                #log
                file_name = Template.get_file_name(template_id)

            elif action == 'update':
                template_data = json.loads(request.POST.get('template', ''))
                template_data.update(dict(user=request.devopsuser))
                t = Template(template_data)
                t.update(template_id)
                file_name = Template.get_file_name(template_id)

            elif action == 'delete':
                template_id = request.POST['template_id']
                Template.delete(template_id)
                file_name = ''
            history_log = dict(
                user = request.devopsuser,
                template_id = template_id,
                action = action,
                file_name = file_name)
            Template.add_log(history_log)
        except Exception as e:
            print(e)
            return JsonResponse(dict(status=500, msg='%s fail'%action))
        return JsonResponse(dict(status=200, template_id=template_id, action=action, msg=''))

def gen_filename(tmp_name):
    t = time.time()
    byte_t = bytes(str(t), encoding='utf8')
    h = hashlib.sha1()
    h.update(byte_t)
    return h.hexdigest()+tmp_name

@csrf_exempt
def cell_post(request, debug=False):
    assert request.method == 'POST'
    is_API_deploy = request.POST.get('is_API_deploy', None)
    template_id = request.POST.get('template_id', '')
    template = Template.get(template_id)
    location = request.POST.get('location', [])
    location = location.split(',')
    try:
        cc = Cell(template, location)
    except:
        return JsonResponse(dict(status=500, data=None))
    if is_API_deploy==True or is_API_deploy=='true':
        cc.from_api()
    else:
        tmp = request.FILES['file']
        tmp_name = request.FILES['file'].name
        tmp_name = gen_filename(tmp_name)
        with open(os.path.join(settings.STATIC_ROOT, tmp_name), 'wb') as f:
            f.write(tmp.read())
    
        workbook = xlrd.open_workbook(os.path.join(settings.STATIC_ROOT, tmp_name))
        sheet = workbook.sheet_by_index(0) # read first sheet
        try:
            cc.from_sheet(sheet)
        except Exception as e:
            print(e)
            return JsonResponse(dict(status=500, data=None))
    print(cc.cell['cell_config'])
    # delete file
    delete_file(os.path.join(settings.STATIC_ROOT, tmp_name))
    
    try:
        push_key(
            request, 
            cc.cell['cell_id'], 
            cc.cell['cell_config'], 
            cc.connections, 
            'root', 
            'VuBX8g+IPg==', 
            debug = debug
        )
        #insert cell to cmdb
        insert_cell(request, cc, debug=debug)
    except Exception as e:
        print(e)
        return JsonResponse(dict(status=500, data=None))
    return JsonResponse(dict(status=200, data=cc.cell))

def cell_index(request):
    resp = render(request, 'cell/cell.html')
    return resp

def insert_cell(request, cell, debug=False):
    if debug==True:
        return
    cmdb_cell_table = CmdbCellTable(request)
    cmdb_cell_table.insert(cell.cell['cell_config'])

def run_cell(request, debug=False):
    request.method = 'GET'
    cell_id = request.GET.get('cell_id', '')
    try:
        assert bool(cell_id) == True
    except AssertionError:
        return JsonResponse(dict(status=500, msg='input args error'))
    # return JsonResponse(dict(status=200)) if is_rpc_started(cell_id) else JsonResponse(dict(status=500))
    # tmp_bool = is_rpc_started("test")
    if debug==False:
        cmdb_cell_table = CmdbCellTable(request)
        cell_config = cmdb_cell_table.get_cell_config(cell_id)
        # connections = cmdb_cell_table.get_cell_connections(cell_id)
    else:
        cell_config = [{'ip': '172.29.164.91',
                'cpu': 2.0,
                'mem': 4.0,
                'disk': 50.0,
                'node_type': 'jar',
                'node_name': 'kfc_preorder_nh_online_sgemfb8r_jar2'}]
    hu = HttpUtils(request)
    hu.post(
        serivceName = 'p_job',
        restName = '/rest/cell/deploy/', 
        datas=dict(host_list=cell_config, cell_name=cell_id)
    )
    tmp_bool = True
    if tmp_bool:
        return JsonResponse(dict(status=200))
    else:
        return JsonResponse(dict(status=500))

def push_key(request, cell_id, cell_config, connections, ssh_user, ssh_passwd, debug=False):
    """
    push key file to servers derived from excel
    """
    print("cell_id is %s"%(cell_id))
    if debug:
        cell_config = [
            {'ip': '172.29.164.91',
            'cpu': 2.0,
            'mem': 4.0,
            'disk': 50.0,
            'node_type': 'jar',
            'node_name': 'kfc_preorder_nh_online_sgemfb8r_jar2'}
        ]

        connections = {'a':'b'}
    hu = HttpUtils(request)
    ret = hu.post(
        serivceName = 'p_job',
        restName = '/rest/cell/authorizedkey/', 
        datas=dict(
            host_list=cell_config,
            relation_dict=connections,
            cell_name = cell_id,
            ssh_user = ssh_user,
            ssh_passwd = ssh_passwd
        )
    )
    print(ret)

def debug_push_key(cell_id, cell_config):
    redis_mq = RedisMQ(cell_id)
    steps = [
        {
            "step_tag": "push_key",
            "status": 0,
            "success": [],
            "fail": []
        }
    ]
    msg = json.dumps(dict(steps=steps, data=cell_config))
    redis_mq.publish(msg)