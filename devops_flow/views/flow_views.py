from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsFlowListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "flow_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DevopsFlowListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            app_list_result = hu.get(serivceName="p_job", restName="/rest/flowcontrol/list/", datas=reqData) #/rest/flowcontrol/list/
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


class DevopsFlowCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_form.html"

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
            addAppResults = hu.post(serivceName="p_job", restName="/rest/flowcontrol/add/", datas=reqData) #/rest/flowcontrol/add/
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 200:
                result['status'] = 0
                result['msg'] = '保存应用信息成功'
            else:
                result['status'] = 1
                result['msg'] = '保存应用信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DevopsFlowUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            app_list_result = hu.get(serivceName="p_job", restName="/rest/flowcontrol/list/", datas={'id':id}) #/rest/flowcontrol/list/
            app_list = app_list_result.get("results", {})
            app = {}
            if len(app_list) > 0:
                app = app_list[0]
            context['app_info'] = app
            context['is_add'] = 0
        except Exception as e:
            logger.error(e,exc_info=1)
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
                addAppResults = hu.post(serivceName="p_job", restName="/rest/flowcontrol/updateById/", datas=reqData) #/rest/flowcontrol/update/
                addAppResults = addAppResults.json()
                if addAppResults['status'] == 200:
                    result['status'] = 0
                    result['msg'] = '更新流量调度信息成功'
                else:
                    result['status'] = 1
                    result['msg'] = '更新流量调度信息失败'
            else:
                result['status'] = 1
                result['msg'] = '更新流量调度信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result), content_type='application/json')


class DevopsFlowOperationView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_operation.html"

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
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/",
                                      datas={'tool_id': tool_id, 'tool_version': tool_version,
                                             'is_history': -1})  # /rest/job/list_tool_set/
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
                if p.get("paramNameZh",None) == 'version_yumc' or p.get("paramNameZh",None) == 'jira_yumc':
                    v = p['value']
                    if v:
                        if v.startswith('http'):
                            pass
                        else:
                            try:
                                v_f = open(v, 'r')
                                p['value'] = v_f.readline().replace("\r",'').replace("\n",'')
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
            infom = int(reqData['infom'])
            param = reqData.get('param', None)
            remarks = reqData.get('remarks')
            if param:
                if bind_type == 1:  # 1 - 工具   2 - 常用作业
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
                                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                                           datas={"id": target_group_ids})
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
                            operation_result = hu.post(serivceName="p_job", restName="/rest/flowcontrol/operation/",
                                                       datas={'deploy_id': deploy_id, 'bind_type': bind_type,
                                                              'tool_id': tool_id, 'tool_version': tool_version,
                                                              'param': param,'remarks':remarks})
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
            result['status'] = 1
            result['msg'] = '调度异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsFlowReportView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, TemplateView):
    template_name = "flow_report.html"
    def get_context_data(self, **kwargs):
        context = super(DevopsFlowReportView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            ec_grafana_graph_result = hu.get(serivceName="job", restName="/rest/deploy/ec_grafana_graph/", datas={})
            result = ec_grafana_graph_result.get('data',[])
            for item in result:
                total = 0
                for item2 in item['env']:
                    total += int(item2['value'])
                item['env_total'] = total
                total = 0
                for item2 in item['channel']:
                    total += int(item2['value'])
                item['channel_total'] = total
            context['result']=result
        except Exception as e:
            logging.error(e)
        return context

# class DevopsFlowReportView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
#     template_name = "flow_report.html"
#
#     def get_context_data(self, **kwargs):
#         context = {}
#         try:
#             hu = HttpUtils(self.request)
#             dashboard = hu.get_url("http://172.29.164.91:3000/d/qJbknE7mk/dashboard?orgId=1",datas={},auth=("admin","admin"))
#             #datas = json.dumps({"user":"admin","password":"admin"})
#             #html = requests.post("http://172.29.164.91:3000/login", data=datas.encode('UTF-8'),headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8",}, timeout=10000)
#             #result_cookies = requests.utils.dict_from_cookiejar(html.cookies)
#             html = dashboard.text
#             html = html.replace('href="public', 'href="http://172.29.164.91:3000/public')
#             html = html.replace('src="public', 'href="http://172.29.164.91:3000/public')
#             context['html'] = html
#         except Exception as e:
#             logger.error(e)
#         return context
#
#
# def DevopsFlowReportView2(request):
#     try:
#         datas = json.dumps({"user": "admin", "password": "admin"})
#         html = requests.post("http://172.29.164.91:3000/login", data=datas.encode('UTF-8'),
#                              headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8", },
#                              timeout=10000)
#         result_cookies = requests.utils.dict_from_cookiejar(html.cookies)
#         response = render(request, "flow_report.html", {})
#         response['Access-Control-Allow-Origin'] = "*"
#         response.set_cookie("grafana_remember",result_cookies['grafana_remember'])
#         response.set_cookie("grafana_sess", result_cookies['grafana_sess'])
#         response.set_cookie("grafana_user", result_cookies['grafana_user'])
#     except Exception as e:
#         logger.error(e)
#     return response




