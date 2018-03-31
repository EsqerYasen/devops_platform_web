from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from djqscsv import render_to_csv_response
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *

import logging,os,xlrd,threading

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
            reqData['go_live'] = 1
            resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=reqData)
            list = resultJson.get("results",[])

            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}

            brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)

            pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)

            lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)

            mwResult = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)

            dnsResult = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)

            envResult = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)

            paginator = Paginator(resultJson.get("results",[]), req.limit)
            count = resultJson.get("count",0)
            paginator.count = count
            context['result_list'] = list
            context['brand_list'] = brandResult.get("results",[])
            context['pidc_list'] = pidcResult.get("results", [])
            context['lidc_list'] = lidcResult.get("results", [])
            context['mw_list'] = mwResult.get("results", [])
            context['dns_list'] = dnsResult.get("results", [])
            context['env_list'] = envResult.get("results", [])
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
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
                ta = threading.Thread(target=importFunction, args=(request,wb,))
                ta.start()
                result_json = {"status": 1, "msg": "后台正在导入，请点击“查看后台任务”按钮查看结果"}
            else:
                result_json = {"status": 1, "msg":"您有后台任务正在执行导入操作，请稍后操作导入"}

            # assert_file = request.FILES.get('files',None)
            # wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
            # req_list = []
            # hu = HttpUtils(request)
            # for i in range(1, wb.sheets()[0].nrows):
            #     row = wb.sheets()[0].row_values(i)
            #     brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas={'key_code': row[1]}).get("results", [])
            #     if len(brandResult) > 0:
            #         groupResult = hu.get(serivceName="cmdb", restName="/rest/groups/", datas={'key_code':row[2]}).get("results", [])
            #         if len(groupResult):
            #             pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas={'key_code':row[3]}).get("results", [])
            #             if len(pidcResult):
            #                 lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas={'key_code':row[4]}).get("results", [])
            #                 if len(lidcResult):
            #                     dict = {'host_ip': row[0], 'biz_brand': brandResult[0]['id'], 'biz_group': groupResult[0]['id'], 'physical_idc': pidcResult[0]['id'],'logical_idc': lidcResult[0]['id']}
            #                     req_list.append(dict)
            #
            #
            # addResult = hu.post(serivceName="cmdb", restName="/rest/host/add/", datas=req_list)
            # addResult = addResult.json()
            # if len(addResult) > 0:
            #     updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=req_list)
            #     updateResult = updateResult.json()
            #     if len(updateResult) > 0:
            #         result_json = {"status": 0}
        except Exception as e:
            result_json = {"status": 1,"msg":"导入执行异常"}
            logger.error(e)
        return self.render_json_response(result_json)


def importFunction(req,wb):
    updateReq = []
    failList = []
    success = 0
    total = 0
    try:
        username = req.user.username
        HOST1_IMPORT_STATIC[username] = {'isImportRun':1}
        addReq = []
        param = {}
        hu = HttpUtils(req)

        for i in range(1, wb.sheets()[0].nrows):
            row = wb.sheets()[0].row_values(i)
            addReq.append({'host_ip':row[0]})
            param[row[0]] = {'host_ip': row[0], 'biz_brand': row[1], 'biz_group': row[2],'physical_idc': row[3], 'logical_idc': row[4]}

        total = len(addReq)
        addResult = hu.post(serivceName="cmdb", restName="/rest/host/add/", datas=addReq)
        addResult = addResult.json()

        failDict = {1:'不合法的IP',2:'IP已存在于数据库',3:'数据库操作失败',4:'IP不存在于数据库',5:'不可修改已上线的主机'}
        if len(addResult) > 0:
            for d in addResult:
                status = d['status']
                host_ip = d['host_ip']
                if status == 0:
                    host_ip_param = param[host_ip]
                    brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/",datas={'key_code': host_ip_param['biz_brand']}).get("results", [])
                    if len(brandResult) > 0:
                        groupResult = hu.get(serivceName="cmdb", restName="/rest/groups/",datas={'key_code': host_ip_param['biz_group']}).get("results", [])
                        if len(groupResult):
                            pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/",datas={'key_code': host_ip_param['physical_idc']}).get("results", [])
                            if len(pidcResult):
                                lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/",datas={'key_code': host_ip_param['logical_idc']}).get("results", [])
                                if len(lidcResult):
                                    dict = {'host_ip':host_ip, 'biz_brand': brandResult[0]['id'],
                                            'biz_group': groupResult[0]['id'], 'physical_idc': pidcResult[0]['id'],
                                            'logical_idc': lidcResult[0]['id']}
                                    updateReq.append(dict)
                                else:
                                    d['error'] = "未匹配到此区域：" + host_ip_param['logical_idc']
                                    failList.append(d)
                            else:
                                d['error'] = "未匹配到此机房：" + host_ip_param['biz_group']
                                failList.append(d)
                        else:
                            d['error'] = "未匹配到此业务线：" + host_ip_param['biz_group']
                            failList.append(d)
                    else:
                        d['error'] = "未匹配到此品牌："+host_ip_param['biz_brand']
                        failList.append(d)
                else:
                    d['error'] = failDict.get(d['status'], "其他错误")
                    failList.append(d)

        updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=updateReq)
        updateResult = updateResult.json()
        if len(updateResult) > 0:
            for d in updateResult:
                status = d['status']
                if status == 0:
                    success += 1
                else:
                    d['error'] = failDict.get(d['status'], "其他错误")
                    failList.append(d)
    except Exception as e:
        logger.error(e)
    finally:
        s = HOST1_IMPORT_STATIC[username]
        s['isImportRun'] = 0
        s['success'] = success
        s['fail'] = len(failList)
        s['total'] = total
        s['failList'] = failList

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



class Host1EditView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            flag = request.POST.get("flag",None);
            if flag:
                hu = HttpUtils(request)
                editInfo = json.loads(request.POST.get("edit"))
                reqParam = []
                if flag == '1':
                    ip_list = json.loads(request.POST.get("ip_list"))
                    for ip in ip_list:
                        reqDict = editInfo.copy()
                        reqDict['host_ip'] = ip
                        reqParam.append(reqDict)
                else:
                    seach = json.loads(request.POST.get("seach", None))
                    seach['go_live'] = 1
                    resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=seach)
                    list = resultJson.get("results", [])
                    for l in list:
                        reqDict = editInfo.copy()
                        reqDict['host_ip'] = l.get("host_ip")
                        reqParam.append(reqDict)

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
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
            logger.error(e)
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
            logger.error(e)
        return self.render_json_response(result_json)

class Host1ToNotOnlineView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            flag = request.POST.get("flag",None);
            if flag:
                hu = HttpUtils(request)
                toNotOnline = json.loads(request.POST.get("toNotOnline"))
                toNotOnline['go_live'] = 2
                reqParam = []
                if flag == '1':
                    ip_list = json.loads(request.POST.get("ip_list"))
                    for ip in ip_list:
                        reqDict = toNotOnline.copy()
                        reqDict['host_ip'] = ip
                        reqParam.append(reqDict)
                else:
                    seach = json.loads(request.POST.get("seach", None))
                    seach['go_live'] = 1
                    resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=seach)
                    list = resultJson.get("results", [])
                    for l in list:
                        reqDict = toNotOnline.copy()
                        reqDict['host_ip'] = l.get("host_ip")
                        reqParam.append(reqDict)

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)