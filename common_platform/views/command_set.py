from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import PER_PAGE,UPLOAD_SCRIPT_PATH
from django.core.paginator import Paginator
from common.utils.HttpUtils import *
from django.urls import reverse_lazy
from django.http import HttpResponse
from common.utils.redis_utils import *
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
            resultJson = hu.get(serivceName="p_job", restName="/rest/commandset/list/", datas=reqData)
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
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
            context["view_num"] = 0
            context['hostGroup_list'] = hostgroupResult.get("results", [])
        except Exception as e:
            logger.error(e)
        return context


    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            command_set_str = request.POST.get("command_set",None)
            hu = HttpUtils(request)
            resultJson = hu.post(serivceName="p_job", restName="/rest/commandset/add/", datas=command_set_str) #/rest/job/add/
            resultJson  = eval(resultJson.text)
            if resultJson["status"] == 200:
                result['status'] = 1
            else:
                result['status'] = 0
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class CommandSetUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "command_step_edit.html"

    def get_context_data(self,**kwargs):
        try:
            context = super(CommandSetUpdateView, self).get_context_data(**kwargs)
            context["view_num"] = '2'
            context['readOnly'] = 'readonly'

            hu = HttpUtils(self.request)
            resultJson = hu.get(serivceName="p_job", restName="/rest/commandset/infoById/", datas={'id': kwargs.get('pk', 0)})
            results = resultJson.get("results", [])

            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={}) #/rest/hostgroup/list_tree/
            context['hostGroup_list'] = hostgroupResult.get("data", [])

            context['result_dict'] = json.dumps(results)
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            command_set_str = request.POST.get("command_set", None)
            hu = HttpUtils(request)
            resultJson = hu.post(serivceName="p_job", restName="/rest/commandset/updateById/",datas=command_set_str)
            resultJson = eval(resultJson.text)
            if resultJson["status"] == 200:
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
        resultJson = hu.post(serivceName="p_job", restName="/rest/job/deleteById/",datas=[{"id": id}])
        return self.render_json_response(resultJson.json())


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
        resultJson = hu.get(serivceName="p_job", restName="/rest/commandset/infoById/",datas={'id': kwargs.get('pk', 0)})
        results = resultJson.get("results", [])
        hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
        context['hostGroup_list'] = hostgroupResult.get("data", [])
        context['result_dict'] = json.dumps(results)
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
            deploy_id = req.GET.get("deploy_id","")
            bind_type = req.GET.get("bind_type","")
            name = req.GET.get("name",'')
            context['name'] = name
            context['deploy_id'] = deploy_id
            context['bind_type'] = bind_type
            context['exec_type'] = req.GET.get("exec_type","")
        except Exception as e:
            logger.error(e)
        return context

    def post(self, request, *args, **kwargs):
        resultJson = {}
        try:
            pass
        except Exception as e:
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')

class GetCommandExecuteLogView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 200}
        try:
            req = self.request
            id = req.GET.get("id", None)
            deploy_id = req.GET.get("exec_id", None)
            bind_type = req.GET.get("bind_type", None)
            exec_type = req.GET.get("exec_type", None)
            log_index = int(req.GET.get("log_index", 0))
            log_str = ""
            if deploy_id and bind_type:
                if id:
                    hu = HttpUtils(request)
                    execRecordResult = hu.get(serivceName="p_job", restName="/rest/tool/execRecordList/", datas={'id': id,'type':exec_type})
                    list = execRecordResult.get("results", [])
                    if len(list):
                        execRecord = list[0]
                        path = execRecord['path']
                        tool_list = execRecord['parameter']
                        #result_json['tool_list'] = json.loads(tool_list)
                        log_f = open(path+"exec.log","r")
                        for line in log_f.readlines():
                            log_str += line
                        result_json['log_str'] = log_str
                        result_json['status'] = 500
                    else:
                        result_json['log_str'] = "未查询到相关记录"
                        result_json['status'] = 500
                else:
                    log_k = "%s_%s_%s_log" % (deploy_id, bind_type,exec_type)
                    r_v1 = RedisBase.get("%s_%s_%s" % (deploy_id, bind_type,exec_type),1)
                    if r_v1:
                        r_v1 = str(r_v1,encoding="utf-8")
                    r_v2 = RedisBase.exists(log_k,1)
                    logger.info("-----------r_v1:%s" % (r_v1))
                    if r_v1 is not None or r_v2:
                        r_v1_json= json.loads(r_v1.replace("'",'"').replace("False",'0').replace("True",'1'))
                        log_list = RedisBase.lrange(redisKey=log_k,start=log_index,db=1)
                        if log_list:
                            logger.info("log_list:%s" % (log_list))
                            for log in log_list:
                                log_index += 1
                                log_str += str(log,encoding="utf-8")+"\n"
                        result_json['log_str'] = log_str
                        #result_json['tool_list']=r_v1_json['tool_list']
                        result_json['log_index'] = log_index
                        result_json['status'] = 200
                    else:
                        result_json['status'] = 500
            else:
                result_json['status'] = 500
        except Exception as e:
            result_json['status'] = 500
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)

class GetCommandExecuteRecord(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 200}
        try:
            req = self.request
            hu = HttpUtils(req)
            exec_id = req.GET.get("exec_id", None)
            type = req.GET.get("type", None)
            execRecordResult = hu.get(serivceName="p_job", restName="/rest/tool/execRecordList/",datas={'exec_id': exec_id, 'type': type})
            list = execRecordResult.get("results", [])
            result_json['data'] = list
        except Exception as e:
            result_json['status'] = 500
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class GetCommandExecuteJobIdView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            req = self.request
            hu = HttpUtils(req)
            setId = req.GET.get("setId", None)
            log_info = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'set_id':setId,'status':1})
            result_json['log_info'] = log_info
        except Exception as e:
            logger.error(e,exc_info=1)
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
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


class ToolSetListView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/listToCommandSet/", datas={}) #/rest/job/list_tool_set/
            tool_list = tool_list_result.get("results",[])
            result_json['data'] = tool_list
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)