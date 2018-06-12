from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from djqscsv import render_to_csv_response
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *

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
            type = req.GET.get("type",0)
            reqData = hu.getRequestParam()
            list = []
            if type == '2':
                group_id = reqData.get("group_id",0)
                resultJson = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host_sp/", datas={"id":group_id,"go_live":1,"offset":reqData.get("offset",0),"limit":reqData.get("limit")})
                list = resultJson.get("results", [])
            else:
                reqData['go_live'] = 1
                resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=reqData)
                list = resultJson.get("results",[])

            for host in list:
                apps = host.get("apps", [])
                groupIds = []
                for app in apps:
                    groupIds.append(str(app.get("group_id", 0)))
                resultListLeader = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_leader/",
                                          datas={"id": '+'.join(groupIds)})
                listLeader = resultListLeader.get("data", {})
                ops = listLeader.get("ops", [])
                opsStr = ""
                for o in ops:
                    if o:
                        opsStr += o + ","
                developStr = ""
                develop = listLeader.get("develop", [])
                for d in develop:
                    if d:
                        developStr += d + ","
                host['ops'] = opsStr
                host['develop'] = developStr

            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)

            paginator = Paginator(resultJson.get("results",[]), req.limit)
            count = resultJson.get("count",0)
            paginator.count = count
            context['result_list'] = list
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e,exc_info=1)
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

HOST1_IMPORT_STATIC={}
class Host1Import(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            username = request.user.username
            s = HOST1_IMPORT_STATIC.get(username,None)
            isImportRun = 0
            if s:
                isImportRun = int(s.get('isImportRun', 0))

            if s is None or isImportRun == 0:
                HOST1_IMPORT_STATIC[username] = {}
                assert_file = request.FILES.get('files', None)
                wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
                ta = threading.Thread(target=import_host_fn, args=(request,wb,))
                ta.start()
                result_json = {"status": 1, "msg": "后台正在导入，请点击“查看后台任务”按钮查看结果"}
            else:
                result_json = {"status": 1, "msg":"您有后台任务正在执行导入操作，请稍后操作导入"}
        except Exception as e:
            result_json = {"status": 1,"msg":"导入执行异常"}
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)

def import_host_fn(req,wb):
    total = 0
    add_total = 0
    binding_total = 0
    failList = []
    try:
        username = req.user.username
        HOST1_IMPORT_STATIC[username] = {'isImportRun': 1}
        hu = HttpUtils(req)
        groupId = 0
        for i in range(1, wb.sheets()[0].nrows):
            row = wb.sheets()[0].row_values(i)
            host_ip = row[0].strip()
            if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$",
                        host_ip):

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

                add_host = {'host_ip': host_ip, 'biz_brand': biz_brand, 'biz_group': biz_group,
                            'physical_idc': physical_idc,
                            'deployment_environment': deployment_environment, "logical_idc": logical_idc,
                            "biz_module": biz_module}
                logger.info("add2 datas:%s" % (add_host))
                add2ResultObj = hu.post(serivceName="cmdb", restName="/rest/host/add2/", datas=add_host)
                addResult = add2ResultObj.json()
                logger.info("add2 result:%s" % (addResult))
                if addResult['status'] == 200:
                    add_total += 1
                    if groupId > 0:
                        logger.info("static_group_append 200 datas: groupId:%s host_ids%s:" % (groupId,host_ip))
                        appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append/",datas={'group_id': groupId, 'host_ids': [host_ip]})
                        append = appendResult.json()
                        logger.info("static_group_append 200 result:%s" % (append))
                        if append['status'] == "SUCCESS":
                            success_count = append['success_count']
                            fail_count = append['fail_count']
                            skip_count = append['skip_count']
                            if int(success_count) > 0:
                                binding_total += 1
                            elif int(fail_count) > 0:
                                failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 绑定失败 请检查此机器相关数据" % (path)})
                            elif int(skip_count) > 0:
                                failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 发现重复绑定此应用 取消绑定" % (path)})
                            else:
                                failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 未知错误 请检查此机器相关数据" % (path)})
                    else:
                        failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s未查询到此节点，绑定失败" % (path)})
                elif addResult['status'] == 400:
                    result_host = json.loads(addResult['host'])
                    if int(result_host['go_live']) < 3:
                        if groupId > 0:
                            logger.info("static_group_append 400 datas: groupId:%s host_ids%s:" % (groupId, host_ip))
                            appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append/",
                                                   datas={'group_id': groupId, 'host_ids': [host_ip]})
                            append = appendResult.json()
                            logger.info("static_group_append 400 result:%s" % (append))
                            if append['status'] == "SUCCESS":
                                success_count = append['success_count']
                                fail_count = append['fail_count']
                                skip_count = append['skip_count']
                                if int(success_count) > 0:
                                    binding_total += 1
                                elif int(fail_count) > 0:
                                    failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 绑定失败 请检查此机器相关数据" % (path)})
                                elif int(skip_count) > 0:
                                    failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 发现重复绑定此应用 取消绑定" % (path)})
                                else:
                                    failList.append({'host_ip': host_ip, "msg": "新增IP成功 %s 未知错误 请检查此机器相关数据" % (path)})
                        else:
                            failList.append({'host_ip': host_ip, "msg": "IP已存在 %s未查询到此节点，绑定失败" % (path)})
                    else:
                        failList.append({'host_ip': host_ip, "msg": "已上线，不能进行任何操作,放弃绑定"})
            else:
                failList.append({'host_ip': host_ip, "msg": "IP格式错误"})

    except Exception as e:
        logger.error(e, exc_info=1)
    finally:
        s = HOST1_IMPORT_STATIC[username]
        s['isImportRun'] = 0
        s['add_total'] = add_total
        s['binding_total'] = binding_total
        s['fail'] = len(failList)
        s['total'] = total
        s['failList'] = failList



# def importFunction(req,wb):
#     updateReq = []
#     failList = []
#     success = 0
#     binding = 0
#     total = 0
#     try:
#         username = req.user.username
#         HOST1_IMPORT_STATIC[username] = {'isImportRun':1}
#         addReq = []
#         param = []
#         hu = HttpUtils(req)
#         failDict = {1: '不合法的IP', 2: 'IP已存在于数据库', 3: '数据库操作失败', 4: 'IP不存在于数据库', 5: '不可修改已上线的主机'}
#         for i in range(1, wb.sheets()[0].nrows):
#             row = wb.sheets()[0].row_values(i)
#             host_ip = row[0].strip()
#             biz_brand = row[1].strip()
#             biz_group = row[2].strip()
#             physical_idc = row[3].strip()
#             deployment_environment = row[4].strip()
#             logical_idc = row[5].strip()
#             biz_module = row[6].strip()
#             groupId = None
#
#             count = 0
#             path = ""
#             if biz_brand:
#                 path+=biz_brand
#                 count+=1
#             if biz_group:
#                 path += "_"+biz_group
#                 count += 1
#             if physical_idc:
#                 path += "_"+physical_idc
#                 count += 1
#             if deployment_environment:
#                 path += "_" + deployment_environment
#                 count += 1
#             if logical_idc:
#                 path += "_" + logical_idc
#                 count += 1
#             if biz_module:
#                 path += "_" + biz_module
#                 count += 1
#             if count == 6:
#                 getPathResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={"path": path})
#                 print(getPathResult)
#                 if getPathResult['status'] == "SUCCESS":
#                     groupId = getPathResult['data']
#                 else:
#                     failList.append({'host_ip':})
#
#             addReq.append({'host_ip':host_ip})
#             param.append({'host_ip': host_ip, 'biz_brand': biz_brand, 'biz_group': biz_group,'physical_idc': physical_idc,
#                              'deployment_environment': deployment_environment,"logical_idc":logical_idc,"biz_module":biz_module,"group_id":groupId})
#
#         total = len(addReq)
#         addResult = hu.post(serivceName="cmdb", restName="/rest/host/add/", datas=addReq)
#         addResult = addResult.json()
#         if len(addResult) > 0:
#             #for d in addResult:
#             for j in range(len(addResult)):
#                 d = addResult[j]
#                 status = d['status']
#                 host_ip = d['host_ip']
#                 if status == 0:
#                     #updateReq.append(param[host_ip])
#                     updateReq.append(param[j])
#                 elif status == 2: #IP已存在于数据库 追加绑定应用
#                     #group_id = param[host_ip]['group_id']
#                     group_id = param[j]['group_id']
#                     if (group_id):
#                         resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas={"host_ip":host_ip})
#                         list = resultJson.get("results", [])
#                         if len(list) > 0:
#                             host = list[0];
#                             go_live = host['go_live']
#                             if int(go_live) < 3:
#                                 hostId = host['id']
#                                 appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append/",
#                                                        datas={'group_id': group_id, 'host_ids': [hostId]})
#                                 append = appendResult.json()
#                                 if append['status'] == "SUCCESS":
#                                     success_count = append['success_count']
#                                     fail_count = append['fail_count']
#                                     skip_count = append['skip_count']
#                                     if int(success_count) > 0:
#                                         binding += 1
#                                         d['error'] = "IP已存在于数据库 追加绑定应用:%s_%s_%s_%s_%s_%s" % (
#                                          param[j]['biz_brand'], param[j]['biz_group'], param[j]['physical_idc'],
#                                          param[j]['deployment_environment'], param[j]['logical_idc'], param[j]['biz_module'])
#                                         #param[host_ip]['biz_brand'], param[host_ip]['biz_group'], param[host_ip]['physical_idc'],
#                                         #param[host_ip]['deployment_environment'], param[host_ip]['logical_idc'], param[host_ip]['biz_module'])
#                                     elif int(fail_count) > 0:
#                                         d['error'] = "绑定失败 请检查此机器相关数据"
#                                     elif int(skip_count) > 0:
#                                         d['error'] = "发现重复绑定此应用 取消绑定"
#                                     else:
#                                         d['error'] = "未知错误 请检查此机器相关数据"
#                                 else:
#                                     d['error'] = "绑定失败 请检查此机器相关数据"
#                             else:
#                                 d['error'] = "此机器已上线 无法绑定应用"
#                     failList.append(d)
#                 else:
#                     d['error'] = failDict.get(d['status'], "其他错误")
#                     failList.append(d)
#
#         updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=updateReq)
#         updateResult = updateResult.json()
#
#         if len(updateResult) > 0:
#             for d in updateResult:
#                 status = d['status']
#                 if status == 0:
#                     host_ip = d['host_ip']
#                     success += 1
#                     group_id = param[host_ip]['group_id']
#                     if(group_id):
#                         appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append/", datas={'group_id':group_id,'host_ids':[d['host_id']]})
#                         append = appendResult.json()
#                         if append['status'] == "SUCCESS":
#                             binding+=1
#                         else:
#                             d['error'] = "绑定失败"
#                             failList.append(d)
#                 else:
#                     d['error'] = failDict.get(d['status'], "其他错误")
#                     failList.append(d)
#
#     except Exception as e:
#         logger.error(e,exc_info=1)
#     finally:
#         s = HOST1_IMPORT_STATIC[username]
#         s['isImportRun'] = 0
#         s['success'] = success
#         s['binding'] = binding
#         s['fail'] = len(failList)
#         s['total'] = total
#         s['failList'] = failList

class GetImportStatus(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1, "msg": "导入执行异常"}
        username = request.user.username
        s = HOST1_IMPORT_STATIC.get(username,None)
        if s:
            isImportRun = int(s.get('isImportRun', 0))
            result_json = {"status": 0, "msg": "您没有正在导入的后台操作",'result':s}
            if isImportRun == 0:
                 del HOST1_IMPORT_STATIC[username]
        else:
            result_json = {"status": 0, "msg": "您没有正在导入的后台操作","result":[],"isRun":0}
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
                updateResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_append/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == "SUCCESS":
                    result_json = {"status": 0,'failCount':result['fail_count'],'successCount':result['success_count']}
                else:
                    result_json['failCount'] = result['fail_count']
                    result_json['successCount'] = result['success_count']
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
                updateResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/static_group_delete/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == "SUCCESS":
                    result_json = {"status": 0, 'failCount': result['fail_count'],'successCount': result['success_count']}
                else:
                    result_json['failCount'] = result['fail_count']
                    result_json['successCount'] = result['success_count']
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class Host1DeleteView(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            hostIp = request.POST.get("hostIp", None);
            reqParam = []
            hu = HttpUtils(request)
            for ip in hostIp.split(','):
                reqParam.append({'host_ip':ip,'is_enabled':0})
            updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
            result = updateResult.json()
            if len(result) > 0:
                result_json = {"status": 0}
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