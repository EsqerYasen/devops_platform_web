from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
import logging

logger = logging.getLogger('devops_platform_log')

class ListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "deploy_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            physical = reqData.get("physical","")
            deployment_environment = reqData.get("deployment_environment","")
            setListResult = hu.get(serivceName="job", restName="/rest/deploy/set_list/", datas=reqData)
            setList = setListResult.get("results",[])
            for set in setList:
                setId = set['id']
                reqDcit = {"parent_id":setId,"offset":0,"limit":1000}
                if physical != "":
                    reqDcit['idc'] = physical
                if deployment_environment != "":
                    reqDcit['env'] = deployment_environment
                appListResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/", datas=reqDcit)
                appList = appListResult.get("results", [])
                set['appList'] = appList

            context['setList'] = setList
        except Exception as e:
            logger.error(e)
        return context

class CreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_add.html"

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
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            treeListStr = reqData.get("treeList",[])
            treeList = json.loads(treeListStr)
            pathListStr = reqData.get("pathList",[])
            pathList = json.loads(pathListStr)
            scriptDictStr = reqData.get("scriptDict",{})
            scriptDict = json.loads(scriptDictStr)
            parentName = treeList[0]['parentName']
            setAddResult = hu.get(serivceName="job", restName="/rest/deploy/set_getoradd/", datas={"name": parentName})
            if setAddResult['status'] == "SUCCESS":
                setId = setAddResult['data']
                for t in treeList:
                    t['parent_id'] = setId
                    t['pathList'] = pathList
                    t['pre_script'] = scriptDict.get("deploy_before","")
                    t['post_script'] = scriptDict.get("deploy_after", "")
                    t['check_script'] = scriptDict.get("deploy_check", "")
                    t['files'] = pathList

                appAddResult = hu.post(serivceName="job", restName="/rest/deploy/app_add/", datas=treeList)
                appAddResult = appAddResult.json()
                if appAddResult['status'] == "SUCCESS":
                    result['status'] = 0
                else:
                    result['status'] = 1
            else:
                result['status'] = 1

        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')