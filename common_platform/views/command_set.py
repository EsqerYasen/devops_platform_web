from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import PER_PAGE,UPLOAD_SCRIPT_PATH
from django.core.paginator import Paginator
from common.utils.HttpUtils import *
from django.urls import reverse_lazy
from django.http import HttpResponse
import logging,os,time

logger = logging.getLogger('devops_platform_log')

class CommandSetListView(LoginRequiredMixin, OrderableListMixin, ListView):
    paginate_by = PER_PAGE
    template_name = "command_set_list.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(CommandSetListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            resultJson = hu.get(serivceName="job", restName="/rest/job/list/", datas=reqData)
            list = resultJson.get("results", [])

            paginator = Paginator(resultJson.get("results", []), req.limit)
            count = resultJson.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class CommandSetCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):

    template_name = "command_set_form.html"
    success_url = reverse_lazy("platform:command_set/list/")

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)

            treeResult = hu.get(serivceName="cmdb", restName="/rest/app/treeview/", datas={})
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)
            pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)
            lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)
            envResult = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)
            mwResult = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)
            dnsResult = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            fileResult = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})

            context["view_num"] = 0
            context["result_dict"] = {}
            context['tree_list'] = treeResult.get("data", [])
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['file_tree'] = json.dumps(fileResult.get("data", []))
            context['brand_list'] = brandResult.get("results", [])
            context['pidc_list'] = pidcResult.get("results", [])
            context['lidc_list'] = lidcResult.get("results", [])
            context['env_list'] = envResult.get("results", [])
            context['mw_list'] = mwResult.get("results", [])
            context['dns_list'] = dnsResult.get("results", [])
            context['localParam_list'] = []
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            user = request.user
            files = request.FILES
            command_set = request.POST.get("command_set",None)

            hu = HttpUtils(request)
            #检查是否有高级查询信息 如果有高级查询信息 需要创建临时组
            commandSet = json.loads(command_set)
            commandStep = commandSet['steps']
            for step in commandStep:
                tabName = step['tab_name']
                target_type = step['target_type']
                if 'advanced_query_tab' in tabName and target_type == '2':
                    hostgroupResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/add/", datas={'name':time.time(),'type':2,'tree_type':2,'parent_id':0})
                    id = hostgroupResult.json().get('id',None)
                    if id:
                        param = {'group_id':id}
                        conditions = []
                        host_filter = step['host_filter']
                        for h in host_filter:
                            conditions.append({'key':h,'value':host_filter[h]})
                        param['conditions'] = conditions
                        smartGroupResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/smart_group_update/",datas=param)
                        step['target_group_ids'] = id

            resultJson = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_set)
            resultJson  = eval(resultJson.text)
            if(resultJson["status"] == "FAILURE"):
                result['status'] = 1
            else:
                localParamList = commandSet['localParamList']

                bool = True
                data = resultJson["data"]
                for k in data:
                    if bool:
                        if len(localParamList) > 0:
                            for l in localParamList:
                                l['set_id'] = int(k)
                            resultJson = hu.post(serivceName="job", restName="/rest/para/add/", datas=localParamList)
                        bool = False
                    step_ids = data[k]
                    for file in files:
                        t = file.split(',')
                        step = step_ids[int(t[0])]
                        f = files[file]
                        path = UPLOAD_SCRIPT_PATH + k + "/"
                        for k2 in step:
                            line = step[k2]
                            path += str(k2) + "/"+str(line[int(t[1])])+"/"
                            os.makedirs(path)
                            destination = open(os.path.join(path, f.name), 'wb+')
                            for chunk in f.chunks():
                                destination.write(chunk)
                            destination.close()
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class CommandSetUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "command_set_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)

            resultJson = hu.get(serivceName="job", restName="/rest/job/list_detail/", datas={'id': kwargs.get('pk', 0)})
            results = resultJson.get("data", [])
            treeResult = hu.get(serivceName="cmdb", restName="/rest/app/treeview/", datas={})
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)
            pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)
            lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)
            envResult = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)
            mwResult = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)
            dnsResult = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            fileResult = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})
            getData['id'] = results['id']
            localParamResult = hu.get(serivceName="job", restName="/rest/para/list/", datas=getData)

            context["view_num"] = 1
            context['result_dict'] = results
            context['tree_list'] = treeResult.get("data", [])
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['file_tree'] = json.dumps(fileResult.get("data", []))
            context['brand_list'] = brandResult.get("results", [])
            context['pidc_list'] = pidcResult.get("results", [])
            context['lidc_list'] = lidcResult.get("results", [])
            context['env_list'] = envResult.get("results", [])
            context['mw_list'] = mwResult.get("results", [])
            context['dns_list'] = dnsResult.get("results", [])
            context['localParam_list'] = localParamResult.get("results", [])
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        pass


class CommandSetDeleteView(LoginRequiredMixin,JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        req = self.request
        id = req.GET.get("id",0)
        hu = HttpUtils(req)
        resultJson = hu.post(serivceName="job", restName="/rest/job/delete/",datas=[{"command_set_id": id}])
        return self.render_json_response(resultJson.json())


# class HostListByIdslView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
#
#     def post_ajax(self, request, *args, **kwargs):
#         result_json = {"status": 1}
#         try:
#             hu = HttpUtils(self.request)
#             reqData = hu.getRequestParam()
#             result = hu.post(serivceName="cmdb", restName="/rest/host/id_list/", datas=reqData)
#             list = result.json().get("result", [])
#             if list:
#                 result_json['host_info'] = list
#             else:
#                 result_json['host_info'] = {}
#         except Exception as e:
#             logger.error(e)
#         return self.render_json_response(result_json)


class HostListByQueryCriteria(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            list = []
            if reqData['tabType'] == '1':
                result = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas=reqData)
                list = result.get("data", [])
                result_json['flag'] = 2;
            else:
                result = hu.get(serivceName="cmdb", restName="/rest/host/", datas=reqData)
                list = result.get("results", [])
                result_json['flag'] = 1;
            result_json['host_list'] = list
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)

class CommandSetExecuteView(LoginRequiredMixin, TemplateView):
    template_name = "command_set_form.html"

    def get_context_data(self, **kwargs):
        context = super(CommandSetExecuteView, self).get_context_data(**kwargs)
        context["view_num"] = '2'
        context['readOnly'] = 'readonly'

        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="job", restName="/rest/job/list_detail/", datas={'id': kwargs.get('pk',0)})
        results = resultJson.get("data", [])

        treeResult = hu.get(serivceName="cmdb", restName="/rest/app/treeview/", datas={})
        getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
        brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)
        pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)
        lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)
        envResult = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)
        mwResult = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)
        dnsResult = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)
        hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
        fileResult = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})
        getData['id'] = results['id']
        localParamResult = hu.get(serivceName="job", restName="/rest/para/list/", datas=getData)

        context['result_dict'] = results
        context['tree_list'] = treeResult.get("data", [])
        context['hostGroup_list'] = hostgroupResult.get("data", [])
        context['file_tree'] = json.dumps(fileResult.get("data", []))
        context['brand_list'] = brandResult.get("results", [])
        context['pidc_list'] = pidcResult.get("results", [])
        context['lidc_list'] = lidcResult.get("results", [])
        context['env_list'] = envResult.get("results", [])
        context['mw_list'] = mwResult.get("results", [])
        context['dns_list'] = dnsResult.get("results", [])
        context['localParam_list'] = localParamResult.get("results", [])
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        execJson = request.POST.get("execJson",None)
        setId = kwargs.get('pk',0)
        resultJson = {}

        hu = HttpUtils(self.request)
        runResults = hu.post(serivceName="job", restName="/rest/job/run/", datas=execJson)
        runJson = runResults.json()
        if int(runJson.get("job_id",0)) > 0:
            resultJson["status"] = "0"
        else:
            resultJson["status"] = "1"
        resultJson['job_id'] = runJson.get("job_id",0)
        resultJson['set_id'] = setId
        return HttpResponse(json.dumps(resultJson),content_type='application/json')


class CommandExecuteLogView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "command_execute_log.html"

    def get_context_data(self, **kwargs):
        context = super(CommandExecuteLogView, self).get_context_data(**kwargs)
        try:
            req = self.request
            setId = req.GET.get("setId","")
            jobId = req.GET.get("jobId","")
            name = req.GET.get("name",'')
            hu = HttpUtils(req)
            historyResults = []
            log_info = {}
            if setId:
                historyResults = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'set_id':setId,'count':50})
            # if jobId:
            #     log_info = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'job_id': jobId})
            context['list_history'] = historyResults
            #context['log_info'] = log_info
            context['name'] = name
            context['set_id'] = setId
            context['job_id'] = jobId
        except Exception as e:
            logger.error(e)
        return context

    def post(self, request, *args, **kwargs):
        resultJson = {}
        try:
            pass
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')

class GetCommandExecuteLogView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            req = self.request
            hu = HttpUtils(req)
            jobId = req.GET.get("jobId", None)
            log_info = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'job_id': jobId})
            result_json['log_info'] = log_info
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)


class CommandExecuteStop(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            req = self.request
            hu = HttpUtils(req)
            jobId = req.GET.get("jobId", None)
            log_info = hu.get(serivceName="job", restName="/rest/job/stop/", datas={'job_id': jobId})
            result_json['log_info'] = log_info
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)

