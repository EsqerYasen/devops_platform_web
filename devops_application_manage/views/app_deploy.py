from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsAppMgeListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "app_deploy_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DevopsAppMgeListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            app_list_result = hu.get(serivceName="job", restName="/rest/app/list_app/", datas=reqData)
            app_list = app_list_result.get("results", {})
            count = app_list_result.get("count", 0)
            paginator = Paginator(app_list, req.limit)
            paginator.count = count
            context['result_list'] = app_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context

class DevopsAppMgeCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            context['version_list'] = []
            context['app_info'] = {}
            context['is_add'] = 1
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            version_list_str = reqData.get("version_list",None)
            addAppResults = hu.post(serivceName="job", restName="/rest/app/add_app/", datas=reqData)
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 'SUCCESS':
                app_id = addAppResults['data']
                version_list = json.loads(version_list_str)
                appVersionResults = hu.post(serivceName="job", restName="/rest/app/update_app_version/", datas={'app_id':app_id,'version':version_list})
                appVersion = appVersionResults.json()
                if appVersion['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '保存应用信息成功'
                else:
                    result['status'] = 1
                    result['msg'] = '保存应用版本信息失败'
            else:
                result['status'] = 1
                result['msg'] = '保存应用信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsAppMgeUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            app_list_result = hu.get(serivceName="job", restName="/rest/app/list_app/", datas={'id':id})
            app_list = app_list_result.get("results", {})
            app = {}
            version_list = []
            if len(app_list) > 0:
                app = app_list[0]
                versionListResult = hu.get(serivceName="job", restName="/rest/app/list_app_version/", datas={'id': app['id']})
                versionList = versionListResult.get("data", [])
                for version in versionList:
                    version_list.append(version['version'])
            context['version_list'] = version_list
            context['app_info'] = app
            context['is_add'] = 0
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            version_list_str = reqData.get("version_list", None)
            app_id = reqData.get("id",None)
            if app_id:
                del reqData['offset']
                del reqData['limit']
                del reqData['csrfmiddlewaretoken']
                del reqData['version_list']
                addAppResults = hu.post(serivceName="job", restName="/rest/app/update_app/", datas=reqData)
                addAppResults = addAppResults.json()
                if addAppResults['status'] == 'SUCCESS':
                    version_list = json.loads(version_list_str)
                    appVersionResults = hu.post(serivceName="job", restName="/rest/app/update_app_version/",datas={'app_id': app_id, 'version': version_list})
                    appVersion = appVersionResults.json()
                    if appVersion['status'] == 'SUCCESS':
                        result['status'] = 0
                        result['msg'] = '更新应用信息成功'
                    else:
                        result['status'] = 1
                        result['msg'] = '更新应用版本信息失败'
                else:
                    result['status'] = 1
                    result['msg'] = '更新应用信息失败'
            else:
                result['status'] = 1
                result['msg'] = '更新应用信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')


class DevopsAppMgeDeleteView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            req = self.request
            id = req.GET.get("id",0)
            hu = HttpUtils(req)
            resultJson = hu.get(serivceName="job", restName="/rest/app/delete_app/",datas={"id": id})
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 0
                result['msg'] = '删除成功'
            else:
                result['status'] = 1
                result['msg'] = '删除失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '删除异常'
            logger.error(e)
        return self.render_json_response(result)


class DevopsAppMgeDeployView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            id = kwargs.get('pk',0)
            reqData = hu.getRequestParam()
            name = reqData.get('name',"")
            toolId = reqData.get('toolId')
            commandId = reqData.get('commandId',0)
            if not commandId or commandId == "None":
                commandId = 0
            commandLineId = reqData.get('commandLineId',0)
            if not commandLineId or commandLineId == "None":
                commandLineId = 0
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            versionListResult = hu.get(serivceName="job", restName="/rest/app/list_app_version/", datas={'id':id})
            tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/",datas={'id':toolId})
            tool_list = tool_list_result.get("results", [])
            tool = {}
            if len(tool_list) > 0:
                for tool in tool_list:
                    tool['param'] = json.loads(tool['param'])
                    del tool['is_enabled']
                tool = tool_list[0]

            version_list = versionListResult.get("data", [])
            new_version_list = []
            for version in version_list:
                new_version_list.append({'id':version['version'],'version':version['version']});
            context["result_dict"] = {}
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['version_list'] = new_version_list
            context['tool_info'] = tool
            context['commandId'] = commandId
            context['commandLineId'] = commandLineId
            context['is_add'] = 1
            context['name'] = name
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            commandSetId = int(reqData.get("command_set_id",0))
            command_info = reqData.get("command_info",None)
            deploy_info = reqData.get("deploy_info",None)
            if commandSetId == 0 and command_info:
                jobAddResults = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_info)
                jobAddResults = jobAddResults.json()
                if (jobAddResults["status"] == "FAILURE"):
                    logger.error("创建安装job失败")
                else:
                    data = jobAddResults["data"]
                    deploy_info = {}
                    step = json.loads(command_info)['steps'][0]
                    line = step['lines'][0]
                    for k in data:
                        commandSetId = k
                        deploy_info['command_set_id'] = k
                        deploy_info['paras'] = {
                            1:{
                                "target_type": step['target_type'],
                                "target_group_ids": step['target_group_ids'],
                                "target_host_list": step['target_host_list'],
                                "go_live": step['go_live']
                            }
                        }
                        step_ids = data[k]
                        step = step_ids[0]
                        for k2 in step:
                            line_id = step[k2][0]
                            deploy_info['paras'][1][line_id] = {
                                "parameter": line['default_script_parameter'],
                                "is_skip": 0
                            }
                            id = kwargs.get('pk', 0)
                            addAppResults = hu.post(serivceName="job", restName="/rest/app/update_app/", datas={'id':id,"command_set_id":commandSetId,'command_line_id':line_id})
                            addAppResults = addAppResults.json()
                            if addAppResults['status'] == 'FAILURE':
                                deploy_info = None

            if deploy_info:
                runResults = hu.post(serivceName="job", restName="/rest/job/run/", datas=deploy_info)
                runJson = runResults.json()
                if int(runJson.get("job_id", 0)) > 0:
                    result["status"] = "0"
                else:
                    result["status"] = "1"
                    result['msg'] = '安装失败'
                result['job_id'] = runJson.get("job_id", 0)
                result['set_id'] = commandSetId
            else:
                result['status'] = 1
                result['msg'] = '没有安装信息，安装失败'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '安装异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class GetCommandSetInfoView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            name = req.GET.get('name',None)
            if name:
                resultJson = hu.get(serivceName="job", restName="/rest/job/list_tool_set/", datas={'name': name})
                resultList = resultJson.get("results", [])
                if len(resultList) > 0:
                    result = resultList[0]
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')