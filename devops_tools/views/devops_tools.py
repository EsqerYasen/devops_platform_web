from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsToolsListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "devops_tools_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            reqData['flag'] = 1
            tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/",datas=reqData)
            tool_list = tool_list_result.get("results", {})
            count = tool_list_result.get("count", 0)
            for tool in tool_list:
                tool['param'] = json.loads(tool['param'])
            paginator = Paginator(tool_list, req.limit)
            paginator.count = count
            context['result_list'] = tool_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class DevopsToolsCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "devops_tools_add.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            context["result_dict"] = {}
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            script_lang_dict = {'shell':'sh','python':'py','yaml':'yaml'}
            if reqData:
                tool_set_prime_type = reqData.get("tool_set_prime_type",None)
                tool_set_type = reqData.get("tool_set_type",None)
                if tool_set_prime_type and tool_set_type:
                    if tool_set_prime_type == '1' and tool_set_type == '5':
                        t = time.time()
                        toolScriptPath = '/opt/devops/tool_script/'
                        command = reqData.get("command",None)
                        script_lang = reqData.get("script_lang","shell")
                        try:
                            if not os.path.exists(toolScriptPath):
                                os.makedirs(toolScriptPath)
                            fileName = "%s%s.%s" % (toolScriptPath, int(round(t * 1000)),script_lang_dict[script_lang])
                            f = open(fileName, 'w')
                            f.write(command)
                            reqData['command'] = fileName
                        except Exception as e:
                            logger.error(e)
                        finally:
                            f.close()

                    addResult = hu.post(serivceName="job", restName="/rest/job/add_tool_set/", datas=reqData)
                    addResultJson = addResult.json()
                    if addResultJson['status'] == 'SUCCESS':
                        result['status'] = 0
                        result['msg'] = '保存成功'
                    else:
                        result['status'] = 1
                        result['msg'] = '保存失败'
                else:
                    result['status'] = 1
                    result['msg'] = '未检测到类别和类型信息，保存失败'
            else:
                result['status'] = 1
                result['msg'] = '保存值为空'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DevopsToolsUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "devops_tools_edit.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/", datas={"id":kwargs.get('pk',0),"offset":0,"limit":"1"})
            tool_list = tool_list_result.get("results", [])
            for tool in tool_list:
                tool['param'] = json.loads(tool['param'])
                tool_set_prime_type = tool["tool_set_prime_type"]
                tool_set_type = tool["tool_set_type"]
                if tool_set_prime_type == 1 and tool_set_type == 5:
                    command = tool["command"]
                    file_object = open(command, 'rU')
                    tool['filename'] = command
                    try:
                        content = ""
                        for line in file_object:
                            content += line
                        tool["command"] = content
                    finally:
                        file_object.close()
                else:
                    tool['filename'] = ""
                tool["command"] = tool["command"].replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')
            context["result_dict"] = tool_list[0]
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            if reqData:
                tool_set_prime_type = reqData.get("tool_set_prime_type", None)
                tool_set_type = reqData.get("tool_set_type", None)
                if tool_set_prime_type and tool_set_type:
                    if tool_set_prime_type == '1' and tool_set_type == '5':
                        command = reqData.get("command",None)
                        try:
                            fileName = reqData.get("filename",None)
                            f = open(fileName, 'w')
                            f.write(command)
                            reqData['command'] = fileName
                        except Exception as e:
                            logger.error(e)
                        finally:
                            f.close()
                    addResult = hu.post(serivceName="job", restName="/rest/job/update_tool_set/", datas=reqData)
                    addResultJson = addResult.json()
                    if addResultJson['status'] == 'SUCCESS':
                        result['status'] = 0
                        result['msg'] = '更新成功'
                    else:
                        result['status'] = 1
                        result['msg'] = '更新失败'
                else:
                    result['status'] = 1
                    result['msg'] = '未检测到类别和类型信息，保存失败'
            else:
                result['status'] = 1
                result['msg'] = '更新值为空'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsToolsDeleteView(LoginRequiredMixin,JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            req = self.request
            id = req.GET.get("id",0)
            hu = HttpUtils(req)
            resultJson = hu.get(serivceName="job", restName="/rest/job/delete_tool_set/",datas={"id": id})
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


class DevopsToolsYamlCheckView(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result = {'status': 1}
        try:
            req = self.request
            t = time.time()
            fileName = None
            toolScriptPath = '/tmp/yumcheck/'
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            command = reqData.get("command", None)
            try:
                if not os.path.exists(toolScriptPath):
                    os.makedirs(toolScriptPath)
                fileName = "%s%s.yaml" % (toolScriptPath, int(round(t * 1000)))
                f = open(fileName, 'w')
                f.write(command)
                reqData['command'] = fileName
            except Exception as e:
                logger.error(e)
            finally:
                f.close()
            if fileName:
                resultJson = hu.get(serivceName="job", restName="/rest/job/test_yaml/", datas={"file": fileName})
                if resultJson['status'] == 'SUCCESS':
                    result['status'] = 0
                else:
                    result['status'] = 1
                    result['msg'] = resultJson['msg']
        except Exception as e:
            result['status'] = 1
            result['msg'] = '检查脚本异常'
            logger.error(e)
        return self.render_json_response(result)