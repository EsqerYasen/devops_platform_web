from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from common.utils.redis_utils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class AnsibleMgeView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "ansible_manage.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            #hu = HttpUtils(self.request)
            #getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            #hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            #context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['hostGroup_list'] = RedisBase.get("host_group_3", 2)
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            runJson = reqData.get("runJson",None)

            if runJson:
                run_data = json.loads(runJson)
                runResult = hu.post(serivceName="p_job", restName="/rest/commandset/ansibleruncmd/", datas=run_data) #/rest/job/run_ansible/
                runResult = runResult.json()
                if runResult['status'] == 200:
                    result['data'] = runResult.get("data",[])
                else:
                    result['status'] = 1
                    result['msg'] = "执行失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = '执行异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')


class AnsibleMgeLogsListView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "ansible_manage_logs_list.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            logsListResult = hu.get(serivceName="p_job", restName="/rest/commandset/ansiblehistorylist/", datas=reqData) #/rest/job/list_ansible_history/
            list = logsListResult.get("results", [])
            paginator = Paginator(list, req.limit)
            count = logsListResult.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def get_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            logsListResult = hu.get(serivceName="p_job", restName="/rest/commandset/ansibleoutput/", datas={"id":reqData.get("id",0)}) #/rest/job/get_ansible_log_by_id/
            result['status'] = 0
            result['logs'] = logsListResult.get("data", [])
        except Exception as e:
            result['status'] = 1
            result['msg'] = '执行异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')