from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from djqscsv import render_to_csv_response
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *
from common.utils.common_utils import *
from common.utils.redis_utils import *
from xlwt import *
from io import StringIO
from django.http import HttpResponse

import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class List1View(LoginRequiredMixin, OrderableListMixin, ListView):
    #paginate_by = PER_PAGE
    template_name = "host_list_1.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(List1View, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            host = reqData.get('host',None)
            if host:
                host = json.loads(host)
                host['go_live'] = 1
                reqData['host'] = host
            else:
                reqData['host'] = {'go_live':1}
            tree = reqData.get('tree',None)
            if tree:
                reqData['tree'] = json.loads(tree)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/host/list/", datas=reqData)
            resultJson = resultJson.json()
            list = resultJson.get("results", [])
            #hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
            hostGroup_list = RedisBase.get("host_group_1",2)
            count = resultJson.get("count", 0)
            paginator = Paginator(list, req.limit)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
            context['hostGroup_list'] = hostGroup_list
        except Exception as e:
            logger.error(e, exc_info=1)
        return context


def TemplateDownload(request):
    def readFile(filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = '导入模板.xlsx'
    filename = os.path.join(BASE_DIR+'/static/','导入模板.xlsx')
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name.encode('utf-8').decode('ISO-8859-1'))
    return response


class Host1Import(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            username = request.user.username
            host_import_key = "%s_host_import" % username
            isImportRun = RedisBase.hget(host_import_key,"is_run",1)
            if isImportRun is None or isImportRun == 0:
                RedisBase.delete(host_import_key,1)
                host_import_key2 = "%s_msg" % host_import_key
                RedisBase.delete(host_import_key2, 1)
                assert_file = request.FILES.get('files', None)
                wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
                ta = threading.Thread(target=import_host_fn, args=(request,wb,))
                ta.start()
                time.sleep(1)
                result_json = {"status": 200, "msg": "后台正在导入，请点击“查看后台任务”按钮查看结果"}
            else:
                result_json = {"status": 500, "msg":"您有后台任务正在执行导入操作，请稍后操作导入"}
        except Exception as e:
            result_json = {"status": 500,"msg":"导入执行异常"}
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)

def import_host_fn(req,wb):
    total = 0
    success_count = 0
    fail_count = 0
    try:
        username = req.user.username
        start_t = time.time()
        total = wb.sheets()[0].nrows

        host_import_key = "%s_host_import" % username
        host_import_key2 = "%s_msg" % host_import_key
        RedisBase.hset(host_import_key,"is_run",1,1)
        RedisBase.hset(host_import_key, "total", total - 1, 1)

        log_path = "/opt/devops/host_operation_log/host_import_logs/%s/" % (username)
        hu = HttpUtils(req)
        groupId = 0
        mkdir(log_path)

        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_t))
        file_log = open("%s%s.log" % (log_path,str(start_t).replace('.', '')),'a+')
        file_log.write("用户:%s   批量导入机器信息 时间:%s\n" % (username, curtime))
        wb_sheets = wb.sheets()[0]
        for i in range(1, total):
            row = wb_sheets.row_values(i)
            host_ip = row[0].strip()
            if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$",host_ip):

                biz_brand = row[1].strip()
                biz_group = row[2].strip()
                physical_idc = row[3].strip()
                deployment_environment = row[4].strip()
                logical_idc = row[5].strip()
                biz_module = row[6].strip()
                count = 0
                path = ""
                if biz_brand:
                    path += biz_brand
                    count += 1
                if biz_group:
                    path += "_" + biz_group
                    count += 1
                if physical_idc:
                    path += "_" + physical_idc
                    count += 1
                if deployment_environment:
                    path += "_" + deployment_environment
                    count += 1
                if logical_idc:
                    path += "_" + logical_idc
                    count += 1
                if biz_module:
                    path += "_" + biz_module
                    count += 1
                if count == 6:
                    getPathResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                           datas={"path": path})
                    print(getPathResult)
                    if getPathResult['status'] == "SUCCESS":
                        groupId = getPathResult['data']
                    else:
                        groupId = 0
                else:
                    groupId = 0
                host_ips = host_ip.split('.')
                add_host = {'host_ip': host_ip, 'biz_brand': biz_brand, 'biz_group': biz_group,
                            'physical_idc': physical_idc,
                            'deployment_environment': deployment_environment, "logical_idc": logical_idc,
                            "biz_module": biz_module,"ip_1":host_ips[0],"ip_2":host_ips[1],"ip_3":host_ips[2],"ip_4":host_ips[3]}
                logger.info("add2 datas:%s" % (add_host))
                add2ResultObj = hu.post(serivceName="cmdb", restName="/rest/host/add2/", datas=add_host)
                addResult = add2ResultObj.json()
                logger.info("add2 result:%s" % (addResult))
                if addResult['status'] == 200:
                    success_count += 1
                    if groupId > 0:
                        host_id = addResult['id']
                        logger.info("static_group_append2 200 datas: groupId:%s host_ip:%s host_id:%s" % (groupId,host_ip,host_id))
                        appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append2/",datas={'group_id': groupId, 'host_id': host_id})
                        append = appendResult.json()
                        logger.info("static_group_append2 200 result:%s" % (append))
                        if append['status'] == 200:
                            file_log.write("新增 %s 成功 绑定此应用(%s) 成功\n" % (host_ip,path))
                        elif append['status'] == 400:
                            RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "新增IP成功 %s 发现重复绑定此应用 取消绑定" % (path)}), 1)
                            file_log.write("新增 %s 成功 发现重复绑定此应用(%s) 取消绑定\n" % (host_ip, path))
                        else:
                            RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "新增IP成功 %s 绑定失败 请检查此机器相关数据" % (path)}), 1)
                            file_log.write("新增 %s 成功 绑定失败(%s) 请检查此机器相关数据\n" % (host_ip, path))
                    else:
                        RedisBase.lpush(host_import_key2,json.dumps({'host_ip': host_ip, "msg": "新增IP成功 %s未查询到此节点，绑定失败" % (path)}),1)
                        file_log.write("新增 %s 成功 未查询到此节点(%s) 绑定失败\n" % (host_ip, path))
                elif addResult['status'] == 400:
                    result_host = addResult['host']
                    if int(result_host['go_live']) < 3:
                        if groupId > 0:
                            host_id = result_host['id']
                            logger.info("static_group_append2 400 datas: groupId:%s host_ip:%s host_id:%s" % (groupId, host_ip,host_id))
                            appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append2/",datas={'group_id': groupId, 'host_id': host_id})
                            append = appendResult.json()
                            logger.info("static_group_append2 400 result:%s" % (append))
                            if append['status'] == 200:
                                success_count += 1
                                file_log.write("%s 已存在 节点(%s) 绑定成功\n" % (host_ip, path))
                            elif append['status'] == 400:
                                fail_count += 1
                                RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "IP已存在 %s 发现重复绑定此应用 取消绑定" % (path)}), 1)
                                file_log.write("%s 已存在 发现重复绑定此应用(%s) 取消绑定\n" % (host_ip, path))
                            else:
                                fail_count += 1
                                RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "IP已存在 %s 绑定失败 请检查此机器相关数据" % (path)}), 1)
                                file_log.write("%s 已存在 绑定失败(%s) 请检查此机器相关数据\n" % (host_ip, path))
                        else:
                            fail_count += 1
                            RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "IP已存在 %s未查询到此节点，绑定失败" % (path)}), 1)
                            file_log.write("%s 已存在 未查询到此节点(%s) 绑定失败\n" % (host_ip, path))
                    else:
                        fail_count += 1
                        RedisBase.lpush(host_import_key2,json.dumps({'host_ip': host_ip, "msg": "已上线，不能进行任何操作,放弃绑定"}), 1)
                        file_log.write("%s 已上线 不能进行任何操作,放弃绑定(%s)\n" % (host_ip, path))
            else:
                fail_count += 1
                RedisBase.lpush(host_import_key2, json.dumps({'host_ip': host_ip, "msg": "IP格式错误"}), 1)
                file_log.write("%s 格式错误\n" % (host_ip))

            RedisBase.hset(host_import_key, "index", i, 1)
            RedisBase.hset(host_import_key, "success_count", success_count, 1)
            RedisBase.hset(host_import_key, "fail_count", fail_count, 1)
    except Exception as e:
        RedisBase.lpush(host_import_key2, json.dumps({'host_ip': "", "msg": "导入异常 停止导入"}), 1)
        file_log.write("导入异常 停止导入\n")
        logger.error(e, exc_info=1)
    finally:
        if file_log:
            file_log.close()
        RedisBase.expire(host_import_key,10,1)
        RedisBase.expire(host_import_key2, 9, 1)
        RedisBase.hset(host_import_key, "is_run", 0, 1)


class GetImportStatus(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            index = int(request.GET.get("index",0))
            username = request.user.username
            host_import_key = "%s_host_import" % username
            host_import_key2 = "%s_msg" % host_import_key
            isImportRun = int(RedisBase.hget(host_import_key, "is_run", 1))
            result_json['is_run'] = isImportRun
            if isImportRun is not None or isImportRun == 1:
                result_json['total'] = int(RedisBase.hget(host_import_key, "total", 1))
                result_json['run_index'] = int(RedisBase.hget(host_import_key, "index", 1))
                result_json['success_count'] = int(RedisBase.hget(host_import_key, "success_count", 1))
                result_json['fail_count'] = int(RedisBase.hget(host_import_key, "fail_count", 1))
                msg_list = RedisBase.lrange(redisKey=host_import_key2, start=index, db=1)
                if msg_list:
                    data_list = []
                    for msg in msg_list:
                        index += 1
                        data_list.append(json.loads(str(msg,encoding='utf-8')))
                    result_json['status'] = 200
                    result_json['data'] = data_list
                    result_json['index'] = index
                else:
                    result_json['status'] = 200
                    result_json['data'] = []
                    result_json['index'] = index
            else:
                result_json['status'] = 500
                result_json['msg'] = "没有正在执行的任务"
        except Exception as e:
            logger.error(e,exc_info=1)
            result_json['status'] = 500
            result_json['msg'] = "查询异常"
        return self.render_json_response(result_json)




def Host1ExportView(request):
    result_list = []

    return render_to_csv_response(result_list)


class Host1DetailView(LoginRequiredMixin, TemplateView):
    template_name = "host_detail1.html"

    def get_context_data(self, **kwargs):
        context = super(Host1DetailView, self).get_context_data(**kwargs)
        hu = HttpUtils(self.request)
        result = hu.post(serivceName="cmdb", restName="/rest/host/id_list/", datas={'host_id':[kwargs.get('pk')]})
        list = result.json().get("result", [])
        if list:
            context['host_info'] = list[0]
        else:
            context['host_info'] = {}
        return context



class Host1BindingGroup(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            groupId = request.POST.get("group_id",None)
            host_ids = request.POST.get("host_ids",None)
            if groupId and host_ids:
                hu = HttpUtils(request)
                reqParam = {"group_id":groupId,"host_ids":host_ids.split(',')}
                updateResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/batch_host_bind_group/", datas=reqParam) #"/rest/hostgroup/static_group_append/"
                result = updateResult.json()
                if result['status'] == 200:
                    result_json = {"status": 0,'failCount':len(result['500']),'successCount':len(result['200'])}
                else:
                    result_json = {"status": 1, 'failCount': len(result['500']), 'successCount': len(result['200'])}
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class Host1UnbundlingGroup(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            groupId = request.POST.get("group_id",None)
            host_ids = request.POST.get("host_ids",None)
            if groupId and host_ids:
                hu = HttpUtils(request)
                reqParam = {"group_id":groupId,"host_ids":host_ids.split(',')}
                updateResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/batch_host_unbind_group/", datas=reqParam) #/rest/hostgroup/static_group_delete/
                result = updateResult.json()
                if result['status'] == 200:
                    result_json = {"status": 0, 'failCount': len(result['500']), 'successCount': len(result['200'])}
                else:
                    result_json = {"status": 1, 'failCount': len(result['500']), 'successCount': len(result['200'])}
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class Host1DeleteView(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            hu = HttpUtils(request)
            host_ids = request.POST.get("host_ids", None)
            updateResult = hu.post(serivceName="cmdb", restName="/rest/host/batch_delete/",datas={"host_ids":host_ids.split(',')})
            result = updateResult.json()
            if result['status'] == 200:
                result_json = {"status": 0, 'failCount': len(result['500']), 'successCount': len(result['200'])}
            else:
                result_json = {"status": 1, 'failCount': len(result['500']), 'successCount': len(result['200'])}
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)



class Host1ScanView(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            hostIp = request.POST.get("hostIp", None);
            reqParam = []
            hu = HttpUtils(request)
            for ip in hostIp.split(','):
                reqParam.append({'host_ip':ip})
            scanResult = hu.post(serivceName="cmdb", restName="/rest/host/scan/", datas=reqParam)
            result = scanResult.json()
            if len(result) > 0:
                result_json = {"status": 0}
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)

class Host1ToNotOnlineView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        success = 0
        fail = 0
        try:
            hu = HttpUtils(request)
            hostIds = request.POST.get("host_ids",None)
            if len(hostIds)>0:
                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/pre_online/", datas={"host_ids":hostIds.split(',')})
                result = updateResult.json()
                for i in result:
                    if i['status'] == 0:
                        success+=1
                    else:
                        fail+=1
                result_json['status'] = 0
                result_json['success'] = success
                result_json['fail'] = fail
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class MultiConditionQueryPageView(LoginRequiredMixin, TemplateView,AjaxResponseMixin):
    template_name = "multi_condition_query.html"

    def get_context_data(self, **kwargs):
        context = super(MultiConditionQueryPageView, self).get_context_data(**kwargs)
        return context

class MultiConditionQueryView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            para = request.POST.get("p", None)
            hu = HttpUtils(request)
            results = hu.post(serivceName="cmdb", restName="/rest/hostgroup/multi_condition_query/", datas=para)
            result = results.json()
            result_json['status'] = 200
            result_json['data'] = result['data']
        except Exception as e:
            result_json['status'] = 500
            result_json['msg'] = "查询异常"
            logger.error(e, exc_info=1)
        return self.render_json_response(result_json)

def HostExportView(request):
    response = None
    try:
        go_live_dict={"1":"未分配","2":"待上线","3":"已上线"}
        para = request.GET.get("p",None)
        hu = HttpUtils(request)
        results = hu.post(serivceName="cmdb", restName="/rest/hostgroup/multi_condition_query/",datas=para)
        result = results.json()
        result_list = result['data']
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet("host_list")
        w.write(0, 0, "树节点")
        w.write(0, 1, "IP")
        w.write(0, 2, "主机名")
        w.write(0, 3, "操作系统")
        w.write(0, 4, "操作系统版本")
        w.write(0, 5, "CPU")
        w.write(0, 6, "内存")
        w.write(0, 7, "资源环境")
        excel_row = 1
        for host in result_list:
            w.write(excel_row, 0, host['node_name'])
            w.write(excel_row, 1, host['host_ip'])
            w.write(excel_row, 2, host['host_name'])
            w.write(excel_row, 3, host['os'])
            w.write(excel_row, 4, host['kernel_release'])
            w.write(excel_row, 5, host['num_cpus'])
            w.write(excel_row, 6, host['mem_total'])
            w.write(excel_row, 7, go_live_dict[str(host['go_live'])])
            excel_row += 1

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=HostExport%s.xls' % time.strftime('%Y%m%d%H%M%S')
        ws.save(response)
    except Exception as e:
        logger.error(e,exc_info=1)
        response = HttpResponse("无数据")
    return response



class HostOpertionLogListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "host_operationlog_list.html"
    context_object_name = 'result_list'

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(HostOpertionLogListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            resultJson = hu.get(serivceName="cmdb", restName="/rest/host/operationlog_list/", datas=reqData)
            list = resultJson.get("results", [])
            count = resultJson.get("count", 0)
            paginator = Paginator(list, req.limit)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e, exc_info=1)
        return context