from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,xlrd

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
            minProcessCount = int(treeDict.get('min_process_count',0))
            maxProcessCount = int(treeDict.get('max_process_count',0))
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

class DeployCreateImport(JSONResponseMixin,AjaxResponseMixin, TemplateView):

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        success = 0
        fail = 0
        try:
            req = self.request
            hu = HttpUtils(req)
            assert_file = request.FILES.get('files', None)
            wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
            for i in range(1, wb.sheets()[0].nrows):
                row = wb.sheets()[0].row_values(i)
                treeDict = self.generate_dict(row)
                pathList = self.generate_file_list(row)
                parentName = treeDict['parentName']
                minProcessCount = int(treeDict.get('min_process_count', 0))
                maxProcessCount = int(treeDict.get('max_process_count', 0))
                treeDict['min_process_count'] = minProcessCount
                treeDict['max_process_count'] = maxProcessCount
                setAddResult = hu.get(serivceName="job", restName="/rest/deploy/set_getoradd/",
                                      datas={"name": parentName})
                if setAddResult['status'] == "SUCCESS":
                    setId = setAddResult['data']
                    treeDict['parent_id'] = setId
                    treeDict['files'] = pathList

                    appAddResult = hu.post(serivceName="job", restName="/rest/deploy/app_add/", datas=[treeDict])
                    appAddResult = appAddResult.json()
                    if appAddResult['status'] == "SUCCESS":
                        success += 1
                        appCreateCmd = hu.get(serivceName="job", restName="/rest/deploy/app_createcmd/",
                                              datas={"id": appAddResult["data"][0]})
                    else:
                        fail += 1
                else:
                    fail += 1
            result['success'] = success
            result['fail'] = fail
        except Exception as e:
            fail += 1
            request['msg'] = "导入异常"
            logger.error(e)
            return self.render_json_response(request)

    def generate_dict(self,para_list):
        (group_id, port, path, min_count, max_count, start_script, stop_script, pre_script, post_script,
         check_script) = para_list[:10]
        # print(group_id,port,path,min_count,max_count,start_script,stop_script,pre_script,post_script,check_script)
        output_dict = {
            "parentName": "_".join(group_id.split('_')[:2]),
            # "group_id": group_id,
            "name": group_id.split('_')[-1],
            "idc": group_id.split('_')[2],
            "env": group_id.split('_')[3],
            "port": str(int(port)),
            "path": path,
            "min_process_count": str(int(min_count)),
            "max_process_count": str(int(max_count)),
            "start_script": start_script,
            "stop_script": stop_script,
            "pre_script": pre_script,
            "post_script": post_script,
            "check_script": check_script
        }
        headers = {"Content-Type": "application/json", "devopsuser": "zhuge", "devopsgroup": "ec"}
        url = 'http://172.17.144.150:8000/rest/hostgroup/get_id_by_path/'
        r = requests.get(url, {"path": group_id}, headers=headers)
        result_json = r.json()
        if result_json["status"] == "SUCCESS":
            output_dict["group_id"] = result_json["data"]
        else:
            print(result_json["msg"])
        return output_dict

    def generate_file_list(self,para_list):
        path = para_list[2]
        (war, source_ip, source_war_path, source_config_path, source_static_path, dest_config_path,
         dest_static_path) = para_list[10:]
        # print(dest_static_path)
        output_list = []
        wars = war.split('/')
        for item in wars:
            source_dict = {
                "path": source_ip + ":" + source_war_path + item,
                "type": 1,
                "source_type": 1
            }
            dest_dict = {
                "path": path + item,
                "type": 1,
                "source_type": 2
            }
            output_list.append(source_dict)
            output_list.append(dest_dict)
        if source_config_path:
            config_source_dict = {
                "path": source_ip + ":" + source_config_path,
                "type": 2,
                "source_type": 1
            }
            config_dest_dict = {
                "path": dest_config_path,
                "type": 2,
                "source_type": 2
            }
            output_list.append(config_source_dict)
            output_list.append(config_dest_dict)
        if source_static_path:
            folders = source_static_path.split(',')
            for item in folders:
                static_source_dict = {
                    "path": source_ip + ":" + item,
                    "type": 3,
                    "source_type": 1
                }
                static_dest_dict = {
                    "path": dest_static_path + item.split('/')[-1],
                    "type": 3,
                    "source_type": 2
                }
                output_list.append(static_source_dict)
                output_list.append(static_dest_dict)
        return output_list

class DeployUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_edit.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            app_id = req.GET.get("appId",None)
            if app_id:
                applistResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/", datas={"id": app_id})
                applist = applistResult.get("results",[])
                context['app_info'] = applist[0]
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            treeDictStr = reqData.get("treeDict", [])
            treeDict = json.loads(treeDictStr)
            appId = treeDict.get("id",None)
            if appId:
                pathListStr = reqData.get("pathList", [])
                pathList = json.loads(pathListStr)
                minProcessCount = int(treeDict.get('min_process_count', 0))
                maxProcessCount = int(treeDict.get('max_process_count', 0))
                treeDict['min_process_count'] = minProcessCount
                treeDict['max_process_count'] = maxProcessCount

                treeDict['files'] = pathList
                appUpdateResult = hu.post(serivceName="job", restName="/rest/deploy/app_update/", datas=[treeDict])
                appUpdateResult = appUpdateResult.json()
                if appUpdateResult['status'] == "SUCCESS":
                    appCreateCmd = hu.get(serivceName="job", restName="/rest/deploy/app_createcmd/",datas={"id": appId})
                    appCreaterollbackcmd = hu.get(serivceName="job", restName="/rest/deploy/app_createrollbackcmd/",datas={"id": appId})
                    result['status'] = 0
                    result['msg'] = "更新成功"
                else:
                    result['status'] = 1
                    result['msg'] = "更新失败"
            else:
                result['status'] = 1
                result['msg'] = "更新失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = "更新异常"
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
            idc = reqData.get("idc",None)
            env = reqData.get("env",None)
            #is_all = reqData.get("is_all",0)
            if id and appids:
                appids = json.loads(appids)
                setRunResult = hu.post(serivceName="job", restName="/rest/deploy/set_run/", datas={"id":id,"app_ids":appids,"idc":idc,"env":env})
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
            idc = reqData.get("idc", None)
            env = reqData.get("env", None)
            if type and type == '1':  #小版本
                app_id = reqData.get("app_id")
                version = reqData.get("version")
                if app_id and version:
                    setRunResult2 = hu.get(serivceName="job", restName="/rest/deploy/app_createrollbackcmd/",
                                           datas={"id": app_id, "version": version})
                    setRunResult = hu.post(serivceName="job", restName="/rest/deploy/app_run_rollback/",datas={"app_id":app_id,"version":version,"idc":idc,"env":env})
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
                app_ids = reqData.get("app_ids")
                appids = json.loads(app_ids)
                setRunResult2 = hu.get(serivceName="job", restName="/rest/deploy/app_createversionrollbackcmd/",datas={"id": pid, "version": version,"app_ids":appids})
                setRunResult = hu.post(serivceName="job", restName="/rest/deploy/set_run_rollback/",datas={"id": pid,"app_ids":appids, "rollback_version": version,"idc":idc,"env":env})
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
                        applistResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/",datas={"id": id})
                        applist = applistResult.get("results", [])
                        app_info = applist[0]
                        job_id = appListVersion[0].get("job_id",None)
                        log_info = hu.get(serivceName="job", restName="/rest/job/list_history/",datas={'job_id': job_id})
                        log_info['deploy_name'] = app_info.get("name","")
                        logInfoList.append(log_info)
            else:
                job_id = job_id.split(" ")
                for id in job_id:
                    if id:
                        log_info = hu.get(serivceName="job", restName="/rest/job/list_history/", datas={'job_id': id})
                        commandSetName = log_info.get("command_set_name")
                        if commandSetName:
                            commandSetNameList = commandSetName.split('_')
                            applistResult = hu.get(serivceName="job", restName="/rest/deploy/app_list/", datas={"id": commandSetNameList[1]})
                            applist = applistResult.get("results", [])
                            app_info = applist[0]
                            log_info['deploy_name'] = app_info.get("name", "")
                        else:
                            log_info['deploy_name'] = ""
                        logInfoList.append(log_info)
            result['logInfoList'] = logInfoList
        except Exception as e:
            result['status'] = 1
            result['msg'] = "查询日志异常"
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')


class DeleteAppView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin,View):
    def get_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            appId = req.GET.get("app_id",None)
            if appId:
                appDelResult = hu.post(serivceName="job", restName="/rest/deploy/app_delete/",datas=[{"id": appId}])
                appDelResult = appDelResult.json()
                if appDelResult["status"] == "SUCCESS":
                    result['status'] = 0
                    result['msg'] = "删除成功"
                else:
                    result['status'] = 1
                    result['msg'] = "删除失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = "删除异常"
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')