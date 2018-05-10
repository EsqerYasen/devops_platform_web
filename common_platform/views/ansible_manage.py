from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class AnsibleMgeView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "ansible_manage.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            context['hostGroup_list'] = hostgroupResult.get("data", [])
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            runJson = reqData.get("runJson",None)

            if runJson:
                run_data = json.loads(runJson)
                runResult = hu.post(serivceName="job", restName="/rest/job/run_ansible/", datas=run_data)
                runResult = runResult.json()
                if runResult['status'] == "SUCCESS":
                    result['data'] = runResult.get("data",[])
                else:
                    result['status'] = 1
                    result['msg'] = "执行失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = '执行异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class AnsibleMgeLogsListView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "ansible_manage_logs_list.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            logsListResult = hu.get(serivceName="job", restName="/rest/job/list_ansible_history/", datas={})
            context['result_list'] = logsListResult.get("data", [])
        except Exception as e:
            logger.error(e)
        return context

    def get_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()

        except Exception as e:
            result['status'] = 1
            result['msg'] = '执行异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')