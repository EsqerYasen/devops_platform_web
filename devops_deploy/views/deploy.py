from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('devops_platform_log')

class DeployListView(LoginRequiredMixin, OrderableListMixin, ListView):
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
                setListVersionResult = hu.get(serivceName="job", restName="/rest/deploy/set_list_version/", datas={"id":setId})
                setListVersion = setListVersionResult.get("data", [])
                set['version'] = setListVersion
                reqDcit = {"parent_id":setId,"offset":0,"limit":1000}
                if physical != "":
                    reqDcit['idc'] = physical
                if deployment_environment != "":
                    reqDcit['env'] = deployment_environment
                appListResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/", datas=reqDcit)
                appList = appListResult.get("results", [])
                for app in appList:
                    applistversionResult = hu.get(serivceName="job", restName="/rest/deploy/app_list_version/", datas={"id":app.get("id","")})
                    applistversion = applistversionResult.get("data", [])
                    app['version'] = applistversion
                set['appList'] = appList


            paginator = Paginator(setList, self.request.limit)
            count = setListResult.get("count", 0)
            paginator.count = count
            context['setList'] = setList
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(self.request.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context

class DeployCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
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
            treeDictStr = reqData.get("treeDict",[])
            treeDict = json.loads(treeDictStr)
            pathListStr = reqData.get("pathList",[])
            pathList = json.loads(pathListStr)
            parentName = treeDict['parentName']
            minProcessCount = int(treeDict['min_process_count'])
            maxProcessCount = int(treeDict['max_process_count'])
            treeDict['min_process_count'] = minProcessCount
            treeDict['max_process_count'] = maxProcessCount

            setAddResult = hu.get(serivceName="job", restName="/rest/deploy/set_getoradd/", datas={"name": parentName})
            if setAddResult['status'] == "SUCCESS":
                setId = setAddResult['data']
                treeDict['parent_id'] = setId
                treeDict['files'] = pathList

                appAddResult = hu.post(serivceName="job", restName="/rest/deploy/app_add/", datas=[treeDict])
                appAddResult = appAddResult.json()
                if appAddResult['status'] == "SUCCESS":
                    result['status'] = 0
                    appCreateCmd = hu.get(serivceName="job", restName="/rest/deploy/app_createcmd/",datas={"id": appAddResult["data"][0]})
                else:
                    result['status'] = 1
            else:
                result['status'] = 1

        except Exception as e:
            result['status'] = 1
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class GetAppListByPidView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    def get_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            appListResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/", datas=reqData)
            appList = appListResult.get("results", [])
            result['appList'] = appList
        except Exception as e:
            result = {'status': 1}
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DeployExecView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            id = reqData.get("id",None)
            appids = reqData.get("app_ids",None)
            if id and appids:
                appids = json.loads(appids)
                setRunResult = hu.post(serivceName="job", restName="/rest/deploy/set_run/", datas={"id":id,"app_ids":appids})
                setRunResult = setRunResult.json()
                if setRunResult['status'] == "SUCCESS":
                    result['status'] = 0
                    result['msg'] = "发布成功，后端正在执行中"
                else:
                    result['status'] = 1
                    result['msg'] = setRunResult['msg']
            else:
                result['status'] = 1
                result['msg'] = "发布失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = "发布异常"
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DeployRollbackView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            type = reqData.get("type",None)
            if type and type == '1':  #小版本
                app_id = reqData.get("app_id")
                version = reqData.get("version")
                if app_id and version:
                    setRunResult2 = hu.get(serivceName="job", restName="/rest/deploy/app_createrollbackcmd/",
                                           datas={"id": app_id, "version": version})
                    setRunResult = hu.post(serivceName="job", restName="/rest/deploy/app_run_rollback/",datas={"app_id":app_id,"version":version})
                    setRunResult = setRunResult.json()
                    if setRunResult['status'] == "SUCCESS":
                        result['status'] = 0
                        result['msg'] = "回滚成功"
                    else:
                        result['status'] = 1
                        result['msg'] = "回滚失败"
                else:
                    result['status'] = 1
                    result['msg'] = "回滚失败"
            elif type and type == '2': #大版本
                pid = reqData.get("pid")
                version = reqData.get("version")
                setRunResult2 = hu.get(serivceName="job", restName="/rest/deploy/app_createversionrollbackcmd/",datas={"id": pid, "version": version})
                setRunResult = hu.post(serivceName="job", restName="/rest/deploy/set_run_rollback/",datas={"app_id": pid, "version": version})
                setRunResult = setRunResult.json()
                if setRunResult['status'] == "SUCCESS":
                    result['status'] = 0
                    result['msg'] = "回滚成功"
                else:
                    result['status'] = 1
                    result['msg'] = "回滚失败"
            else:
                result['status'] = 1
                result['msg'] = "回滚异常"

        except Exception as e:
            result['status'] = 1
            result['msg'] = "回滚异常"
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class ExecuteLogView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):

    template_name = "deploy_log.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            appids = req.GET.get("app_ids","")
            job_id = req.GET.get("job_id", "")
            context['appids'] = appids
            context['job_id'] = job_id
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            appids = reqData.get("app_ids", None)
            job_id = reqData.get("job_id", None)
            logInfoList = []
            if appids:
                appids = appids.split(" ")

                for id in appids:
                    appListVersionResult = hu.get(serivceName="job", restName="/rest/deploy/app_list_history/",datas={"id": id})
                    appListVersion = appListVersionResult.get("data",[])
                    if appListVersion:
                        job_id = appListVersion[0].get("job_id",None)
                        log_info = hu.get(serivceName="job", restName="/rest/job/list_history/",datas={'job_id': job_id})
                        logInfoList.append(log_info)
            else:
                job_id = job_id.split("+")
                for id in job_id:
                    log_info = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'job_id': id})
                    logInfoList.append(log_info)
            result['logInfoList'] = logInfoList
        except Exception as e:
            result['status'] = 1
            result['msg'] = "查询日志异常"
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')
