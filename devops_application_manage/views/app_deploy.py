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
            app_list_result = hu.get(serivceName="p_job", restName="/rest/appmanage/list/", datas=reqData) #/rest/app/list_app/
            app_list = app_list_result.get("results", {})
            count = app_list_result.get("count", 0)
            paginator = Paginator(app_list, req.limit)
            paginator.count = count
            context['result_list'] = app_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e,exc_info=1)
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
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            addAppResults = hu.post(serivceName="p_job", restName="/rest/appmanage/add/", datas=reqData)  #/rest/app/add_app/
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 200:
                result['status'] = 200
                result['msg'] = '保存应用信息成功'
            else:
                result['status'] = 500
                result['msg'] = '保存应用信息失败'
        except Exception as e:
            result['status'] = 500
            result['msg'] = '保存异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DevopsAppMgeUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            app_manage_list_result = hu.get(serivceName="p_job", restName="/rest/appmanage/list/",datas={'id': id})
            app_manage_list = app_manage_list_result.get("results", [])
            app_manage = {}
            version_list = []
            if len(app_manage_list) > 0:
                app_manage = app_manage_list[0]

                app_manage_version_list_result = hu.get(serivceName="p_job", restName="/rest/appmanage/appversionlist/",datas={'app_manage_id': app_manage['id']})
                app_manage_version_list = app_manage_version_list_result.get("results", [])
                for app_manage_version in app_manage_version_list:
                    version_list.append(app_manage_version['version'])
            context['version_list'] = version_list
            context['app_info'] = app_manage
            context['is_add'] = 0
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            app_id = reqData.get("id",None)
            if app_id:
                del reqData['offset']
                del reqData['limit']
                del reqData['csrfmiddlewaretoken']
                addAppResults = hu.post(serivceName="p_job", restName="/rest/appmanage/updateById/", datas=reqData) #/rest/app/update_app/
                addAppResults = addAppResults.json()
                if addAppResults['status'] == 200:
                    result['status'] = 200
                    result['msg'] = '更新应用信息成功'
                else:
                    result['status'] = 500
                    result['msg'] = '更新应用信息失败'
            else:
                result['status'] = 500
                result['msg'] = '更新应用信息失败'
        except Exception as e:
            result['status'] = 500
            result['msg'] = '更新异常'
            logger.error(e,exc_info=1)
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
            logger.error(e,exc_info=1)
        return self.render_json_response(result)


class DevopsAppMgeDeployView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            id = kwargs.get('pk', 0)
            reqData = hu.getRequestParam()
            name = reqData.get('name', "")
            tool_id = reqData.get('tool_id')
            tool_version = reqData.get('tool_version')
            commandId = reqData.get('commandId', 0)
            bind_type = reqData.get('bind_type', 0)
            version = reqData.get('version', "")
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostGroup_list = []
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/",datas={'tool_id': tool_id, 'tool_version': tool_version,'is_history': -1})  # /rest/job/list_tool_set/
            tool_list = tool_list_result.get("results", [])
            tool = {}
            if len(tool_list) > 0:
                tool = tool_list[0]
                if int(tool['infom']) == 2:
                    hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
                    hostGroup_list = hostgroupResult.get("data", [])
                if tool['is_public']:
                    tool['is_public'] = 1
                else:
                    tool['is_public'] = 0
                if tool['is_history']:
                    tool['is_history'] = 1
                else:
                    tool['is_history'] = 0
                tool['param'] = json.loads(tool['param'])
                # 检查工具中是否有version_yumc 和 jira_yumc 如果存在获取value值
                self.get_version(tool['param'])
                del tool['is_enabled']

            context["version"] = version
            context["result_dict"] = {}
            context['hostGroup_list'] = hostGroup_list
            context['tool_info'] = tool
            context['commandId'] = commandId
            context['name'] = name
            context['deploy_id'] = id
            context['bind_type'] = bind_type
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def get_version(self,p_list):
        if p_list:
            for p in p_list:
                if p.get("paramNameZh",None) == 'version_yumc' or p.get("paramNameZh",None) == 'jira_yumc' or p.get("type",None) == "path":
                    v = p['value']
                    if v:
                        if v.startswith('http'):
                            pass
                        else:
                            try:
                                v_f = open(v, 'r')
                                p['value'] = v_f.readline().replace("\r",'').replace("\n",'')

                                if p.get("type", None) == "path":
                                    p['type'] = 'input'
                            except Exception as e:
                                if p.get("type", None) == "path":
                                    p['type'] = 'input'
                                p['value'] = ''
                                logger.error(e,exc_info=1)
                            finally:
                                if v_f:
                                    v_f.close()

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            bind_type = int(reqData['bind_type'])
            infom = int(reqData['infom'])
            param = reqData.get('param', None)
            remarks = reqData.get('remarks')
            if param:
                if bind_type == 1: #1 - 工具   2 - 常用作业
                    deploy_id = int(reqData.get("deploy_id", 0))
                    tool_id = reqData.get('tool_id')
                    tool_version = reqData.get('tool_version')
                    if tool_id and tool_version:
                        bool = True
                        if infom == 2:
                            param = json.loads(param)
                            target_type = int(reqData['target_type'])
                            if target_type == 1:
                                target_group_ids = reqData['target_group_ids']
                                go_live = reqData['go_live']
                                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": target_group_ids})
                                host_list = resultNhPilotList.get("data", [])
                                if len(host_list) > 0:
                                    param['hosts'] = ','.join(host_list)
                                else:
                                    bool = False
                                    result['status'] = 500
                                    result['msg'] = '未查到机器列表'
                            else:
                                param['hosts'] = reqData['target_host_list']

                        if bool:
                            operation_result = hu.post(serivceName="p_job",restName="/rest/appmanage/operation/",datas={'deploy_id':deploy_id,'bind_type':bind_type,'tool_id':tool_id,'tool_version':tool_version,'param':param,'remarks':remarks})
                            operation_json = operation_result.json()
                            if operation_json['status'] == 200:
                                result['status'] = 200
                                result['msg'] = operation_json['msg']
                            else:
                                result['status'] = 500
                                result['msg'] = operation_json['msg']
                    else:
                        result['status'] = 500
                        result['msg'] = '发版异常'
                else:
                    commandSetId = int(reqData.get("command_set_id", 0))
            else:
                result['status'] = 500
                result['msg'] = '执行参数为空'

        except Exception as e:
            result['status'] = 500
            result['msg'] = '发版异常'
            logger.error(e, exc_info=1)
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
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result), content_type='application/json')