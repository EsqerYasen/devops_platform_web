from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os,types

logger = logging.getLogger('devops_platform_log')

class DeployToolListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "deploy_tool_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DeployToolListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            deploy_tool_list_result = hu.get(serivceName="p_job", restName="/rest/deploytool/list/", datas=reqData) #/rest/deploytool/list/
            deploy_tool_list = deploy_tool_list_result.get("results", {})
            for deploy_tool in deploy_tool_list:
                version_list_result = hu.get(serivceName="p_job", restName="/rest/deploytool/versionlist/", datas={"deploy_tool_id":deploy_tool['id']}) #/rest/deploytool/versionlist/
                deploy_tool['version_list'] = version_list_result.get("results",[])
            count = deploy_tool_list_result.get("count", 0)
            paginator = Paginator(deploy_tool_list, req.limit)
            paginator.count = count
            context['result_list'] = deploy_tool_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class DeployToolCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_tool_form.html"

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
            addDeployToolResults = hu.post(serivceName="p_job", restName="/rest/deploytool/add/", datas=reqData) #/rest/deploytool/add/
            deployToolResults = addDeployToolResults.json()
            if deployToolResults['status'] == 200:
                result['status'] = 0
                result['msg'] = '保存发布信息成功'
            else:
                result['status'] = 1
                result['msg'] = deployToolResults['msg']
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DeployToolUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_tool_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            deploy_tool_list_result = hu.get(serivceName="p_job", restName="/rest/deploytool/list/", datas={'id':id}) #/rest/deploytool/list/
            deploy_tool_list = deploy_tool_list_result.get("results", [])
            deploy_tool = {}
            if len(deploy_tool_list) > 0:
                deploy_tool = deploy_tool_list[0]
            context['deploy_tool'] = deploy_tool
            context['is_add'] = 0
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            app_id = reqData.get("id", None)
            if app_id:
                del reqData['offset']
                del reqData['limit']
                del reqData['csrfmiddlewaretoken']
                deploy_tool_update_result = hu.post(serivceName="p_job", restName="/rest/deploytool/updateById/", datas=reqData) #/rest/deploytool/update/
                deploy_tool_update = deploy_tool_update_result.json()
                if deploy_tool_update['status'] == 200:
                    result['status'] = 0
                    result['msg'] = deploy_tool_update['msg']
                else:
                    result['status'] = 1
                    result['msg'] = '更新发版信息失败'
            else:
                result['status'] = 1
                result['msg'] = '更新发版信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')



class DeployToolOperationView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_tool_operation.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            id = kwargs.get('pk',0)
            reqData = hu.getRequestParam()
            name = reqData.get('name',"")
            tool_id = reqData.get('tool_id')
            tool_version = reqData.get('tool_version')
            commandId = reqData.get('commandId',0)
            bind_type = reqData.get('bind_type',0)
            version = reqData.get('version',"")
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/",datas={'tool_id':tool_id,'tool_version':tool_version,'is_history':-1}) #/rest/job/list_tool_set/
            tool_list = tool_list_result.get("results", [])
            tool = {}
            if len(tool_list) > 0:
                for tool in tool_list:
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
                tool = tool_list[0]
            context["version"] = version
            context["result_dict"] = {}
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['tool_info'] = tool
            context['commandId'] = commandId
            context['name'] = name
            context['deploy_id'] = id
            context['bind_type'] = bind_type
        except Exception as e:
            logger.error(e, exc_info=1)
        return context

    def get_version(self,p_list):
        if p_list:
            for p in p_list:
                if p.get("paramNameZh",None) == 'version_yumc' or p.get("paramNameZh",None) == 'jira_yumc':
                    v = p['value']
                    if v:
                        if v.startswith('http'):
                            pass
                        else:
                            try:
                                v_f = open(v, 'r')
                                p['value'] = v_f.readline()
                            except Exception as e:
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
            param = reqData.get('param', None)
            if param:
                if bind_type == 1: #1 - 工具   2 - 常用作业
                    deploy_id = int(reqData.get("deploy_id", 0))
                    tool_id = reqData.get('tool_id')
                    tool_version = reqData.get('tool_version')
                    if tool_id and tool_version:
                        operation_result = hu.post(serivceName="p_job",restName="/rest/deploytool/operation/",datas={'deploy_id':deploy_id,'bind_type':bind_type,'tool_id':tool_id,'tool_version':tool_version,'param':param})
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
        return HttpResponse(json.dumps(result), content_type='application/json')

    # def post_ajax(self, request, *args, **kwargs):
    #     result = {'status': 0}
    #     try:
    #         hu = HttpUtils(self.request)
    #         reqData = hu.getRequestParam()
    #         commandSetId = int(reqData.get("command_set_id", 0))
    #         command_info = reqData.get("command_info", None)
    #         deploy_info = reqData.get("deploy_info", None)
    #         deploy_id = reqData.get("deploy_id", None)
    #         version = reqData.get("version", None)
    #         commandLineId = reqData.get("commandLineId", None)
    #         if commandSetId == 0 and command_info:
    #             jobAddResults = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_info)
    #             jobAddResults = jobAddResults.json()
    #             if (jobAddResults["status"] == "FAILURE"):
    #                 logger.error("创建安装job失败")
    #             else:
    #                 data = jobAddResults["data"]
    #                 deploy_info = {}
    #                 step = json.loads(command_info)['steps'][0]
    #                 line = step['lines'][0]
    #                 for k in data:
    #                     commandSetId = k
    #                     deploy_info['command_set_id'] = k
    #                     deploy_info['new_flow'] = 1
    #                     deploy_info['paras'] = {
    #                         '1': {
    #                             "target_type": step['target_type'],
    #                             "target_group_ids": step['target_group_ids'],
    #                             "target_host_list": step['target_host_list'],
    #                             "go_live": step['go_live']
    #                         }
    #                     }
    #                     step_ids = data[k]
    #                     step = step_ids[0]
    #                     for k2 in step:
    #                         line_id = step[k2][0]
    #                         commandLineId = line_id
    #                         deploy_info['paras']['1'][line_id] = {
    #                             "parameter": line['default_script_parameter'],
    #                             "is_skip": 0
    #                         }
    #                         id = kwargs.get('pk', 0)
    #                         addAppResults = hu.post(serivceName="job", restName="/rest/deploytool/update/",
    #                                                 datas={'id': id, "command_set_id": commandSetId,
    #                                                        'command_line_id': line_id})
    #                         addAppResults = addAppResults.json()
    #                         if addAppResults['status'] == 'FAILURE':
    #                             logger.error(addAppResults)
    #                             deploy_info = None
    #         if deploy_info:
    #             if isinstance(deploy_info,str):
    #                 deploy_info = json.loads(deploy_info)
    #             version_url = "/opt/deploy/%s/versions/%s" %(commandSetId,version)
    #             if not os.path.exists(version_url):
    #                 os.makedirs(version_url)
    #             new_parameter = deploy_info['paras']['1'][commandLineId]['parameter']+";version_url="+version_url
    #             deploy_info['paras']['1'][commandLineId]['parameter'] = new_parameter
    #             runResults = hu.post(serivceName="job", restName="/rest/job/run/", datas=deploy_info)
    #             runJson = runResults.json()
    #             if int(runJson.get("job_id", 0)) > 0:
    #                 result["status"] = "0"
    #                 versionaddResult = hu.post(serivceName="job", restName="/rest/deploytool/versionadd/", datas={'deploy_id':deploy_id,'version':version})
    #                 updateResult = hu.post(serivceName="job", restName="/rest/deploytool/update/",datas={'id': deploy_id, "current_version": version})
    #                 appAddHistoryResult = hu.post(serivceName="job", restName="/rest/deploy/app_add_history/",datas={'app_id': deploy_id, "job_id":runJson['job_id'],"version": version,"type":3})
    #             else:
    #                 result["status"] = "1"
    #                 result['msg'] = '发版失败'
    #             result['job_id'] = runJson.get("job_id", 0)
    #             result['set_id'] = commandSetId
    #         else:
    #             result['status'] = 1
    #             result['msg'] = '没有发版信息，发版失败'
    #     except Exception as e:
    #         result['status'] = 1
    #         result['msg'] = '发版异常'
    #         logger.error(e,exc_info=1)
    #     return HttpResponse(json.dumps(result),content_type='application/json')