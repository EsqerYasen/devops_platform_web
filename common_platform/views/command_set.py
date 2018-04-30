from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import PER_PAGE,UPLOAD_SCRIPT_PATH
from django.core.paginator import Paginator
from common.utils.HttpUtils import *
from django.urls import reverse_lazy
from django.http import HttpResponse
import logging,os,time,stat

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
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            fileResult = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})

            context["view_num"] = 0
            context["result_dict"] = {}
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['file_tree'] = json.dumps(fileResult.get("data", []))
            context['localParam_list'] = []
        except Exception as e:
            logger.error(e)
        return context

    # def post_ajax(self, request, *args, **kwargs):
    #     result = {'status': 0}
    #     try:
    #         user = request.user
    #         files = request.FILES
    #         command_set = request.POST.get("command_set",None)
    #
    #         hu = HttpUtils(request)
    #         #检查是否有高级查询信息 如果有高级查询信息 需要创建临时组
    #         commandSet = json.loads(command_set)
    #         commandStep = commandSet['steps']
    #         resultJson = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_set)
    #         resultJson  = eval(resultJson.text)
    #         if(resultJson["status"] == "FAILURE"):
    #             result['status'] = 1
    #         else:
    #             localParamList = commandSet['localParamList']
    #
    #             bool = True
    #             data = resultJson["data"]
    #             for k in data:
    #                 if bool:
    #                     if len(localParamList) > 0:
    #                         for l in localParamList:
    #                             l['set_id'] = int(k)
    #                         resultJson = hu.post(serivceName="job", restName="/rest/para/add/", datas=localParamList)
    #                     bool = False
    #                 step_ids = data[k]
    #                 for file in files:
    #                     t = file.split(',')
    #                     step = step_ids[int(t[0])]
    #                     f = files[file]
    #                     path = UPLOAD_SCRIPT_PATH + k + "/"
    #                     for k2 in step:
    #                         line = step[k2]
    #                         path += str(k2) + "/"+str(line[int(t[1])])+"/"
    #                         os.makedirs(path)
    #                         destination = open(os.path.join(path, f.name), 'wb+')
    #                         for chunk in f.chunks():
    #                             destination.write(chunk)
    #                         destination.close()
    #     except Exception as e:
    #         logger.error(e)
    #     return HttpResponse(json.dumps(result),content_type='application/json')

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            user = request.user
            files = request.FILES
            command_set = request.POST.get("command_set",None)

            t = time.time()
            filePath = "/opt/devops/shell_script/%s/"%(int(round(t * 1000)))

            hu = HttpUtils(request)
            #检查是否有高级查询信息 如果有高级查询信息 需要创建临时组
            commandSet = json.loads(command_set)
            commandStep = commandSet['steps']
            for setp in commandStep:
                seq_no = setp['seq_no']
                lines = setp['lines']
                for i in range(len(lines)):
                    source_file_name = lines[i]['source_file_name']
                    if source_file_name:
                        f = None
                        try:
                            if not os.path.exists(filePath):
                                os.makedirs(filePath)
                            fileName = "%s%s_%s.sh" % (filePath,seq_no,i)
                            f = open(fileName, 'w')
                            f.write(source_file_name)
                            f.close()
                            os.chmod(fileName, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
                            lines[i]['source_file_name'] = fileName
                        except Exception as e:
                            logger.error(e)
                            f.close()

            resultJson = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_set)
            resultJson  = eval(resultJson.text)
            if(resultJson["status"] == "FAILURE"):
                result['status'] = 1
            else:
                result['status'] = 0
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class CommandSetUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "command_step_edit.html"

    # def get_context_data(self, **kwargs):
    #     context = {}
    #     try:
    #         hu = HttpUtils(self.request)
    #
    #         resultJson = hu.get(serivceName="job", restName="/rest/job/list_detail/", datas={'id': kwargs.get('pk', 0)})
    #         results = resultJson.get("data", [])
    #         getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
    #         hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
    #         fileResult = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})
    #         getData['id'] = results['id']
    #         localParamResult = hu.get(serivceName="job", restName="/rest/para/list/", datas=getData)
    #
    #         context["view_num"] = 1
    #         context['result_dict'] = results
    #         context['hostGroup_list'] = hostgroupResult.get("data", [])
    #         context['file_tree'] = json.dumps(fileResult.get("data", []))
    #         context['localParam_list'] = localParamResult.get("results", [])
    #     except Exception as e:
    #         logger.error(e)
    #     return context

    def get_context_data(self,**kwargs):
        context = super(CommandSetUpdateView, self).get_context_data(**kwargs)
        context["view_num"] = '2'
        context['readOnly'] = 'readonly'

        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="job", restName="/rest/job/list_detail/", datas={'id': kwargs.get('pk', 0)})
        results = resultJson.get("data", [])
        result_dcit = {}
        result_dcit['id'] = results['id']
        result_dcit['name'] = results['name']
        steps = []
        for step in results['steps']:
            stepDict = {}
            stepDict['id'] = step['id']
            stepDict['name'] = step['name']
            stepDict['activeIndex'] = step['host_filter']
            stepDict['seq_no'] = step['seq_no']
            lines = []
            for line in step['lines']:
                lineDict = json.loads(line['file_display_name'])
                lineDict['id'] = line['id']
                lineDict['filePath'] = line['source_file_name']
                del lineDict['is_enabled']
                lines.append(lineDict)
            stepDict['lines'] = lines
            steps.append(stepDict)

        result_dcit['steps'] = steps

        context['result_dict'] = result_dcit
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            command_set = request.POST.get("command_set", None)
            commandSet = json.loads(command_set)
            commandStep = commandSet['steps']
            for setp in commandStep:
                seq_no = setp['seq_no']
                lines = setp['lines']
                for i in range(len(lines)):
                    source_file_name = lines[i]['source_file_name']
                    fileName = lines[i]['filePath']
                    filePath = fileName[0:fileName.rindex("/")+1]
                    if os.path.exists(fileName):
                        os.remove(fileName)
                    if source_file_name:
                        f = None
                        try:

                            if not os.path.exists(filePath):
                                os.makedirs(filePath)
                            fileName = "%s%s_%s.sh" % (filePath, seq_no, i)
                            f = open(fileName, 'w')
                            f.write(source_file_name)
                            f.close()
                            os.chmod(fileName, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
                            lines[i]['source_file_name'] = fileName
                        except Exception as e:
                            logger.error(e)
                            f.close()
            hu = HttpUtils(request)
            resultJson = hu.post(serivceName="job", restName="/rest/job/update/", datas=command_set)
            resultJson = eval(resultJson.text)
            if (resultJson["status"] == "FAILURE"):
                result['status'] = 1
            else:
                result['status'] = 0

        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')


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
            result = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id":reqData.get("group_id",0),"go_live":reqData.get("go_live",0)})
            result_json['host_list'] = result
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)

class CommandSetExecuteView(LoginRequiredMixin, TemplateView):
    template_name = "command_step_execute.html"

    def get_context_data(self, **kwargs):
        context = super(CommandSetExecuteView, self).get_context_data(**kwargs)
        context["view_num"] = '2'
        context['readOnly'] = 'readonly'

        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="job", restName="/rest/job/list_detail/", datas={'id': kwargs.get('pk',0)})
        results = resultJson.get("data", [])
        result_dcit = {}
        result_dcit['id'] = results['id']
        result_dcit['name'] = results['name']
        steps = []
        for step in results['steps']:
            stepDict = {}
            stepDict['id'] = step['id']
            stepDict['name'] = step['name']
            stepDict['activeIndex'] = step['host_filter']
            stepDict['seq_no'] = step['seq_no']
            lines = []
            for line in step['lines']:
                lineDict = json.loads(line['file_display_name'])
                lineDict['id'] = line['id']
                if lineDict.get("is_enabled",None):
                    del lineDict['is_enabled']
                lines.append(lineDict)
            stepDict['lines'] = lines
            steps.append(stepDict)

        result_dcit['steps'] = steps

        context['result_dict'] = result_dcit
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


class ToolSetListView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/", datas={})
            result_json['data'] = tool_list_result.get("data",{})
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)