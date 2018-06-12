from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from common.utils.common_utils import *
import logging,time,os,stat

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
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/",datas=reqData) #/rest/job/list_tool_set/
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
            logger.error(e,exc_info=1)
        return context


class DevopsToolsCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "devops_tools_add.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            context["result_dict"] = {}
        except Exception as e:
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            script_lang_dict = {'shell':'sh','python':'py','yaml':'yaml'}
            if reqData:
                logger.info("DevopsToolsCreateView.post_ajax reqData:%s" % (reqData))
                #tool_set_prime_type = reqData.get("tool_set_prime_type",None)
                tool_type = reqData.get("tool_type",None)
                if tool_type:
                    fileName = ""
                    #if tool_type == '5':
                    t = time.time()
                    toolScriptPath = settings.TOOL_SCRIPT_PATH #'/opt/devops/tool_script/'
                    command = reqData.get("command",None)
                    script_lang = reqData.get("script_lang","shell")
                    try:
                        if not os.path.exists(toolScriptPath):
                            os.makedirs(toolScriptPath)
                        fileName = "%s%s%s.%s" % (toolScriptPath, int(round(t * 1000)),randomCharStr(),script_lang_dict[script_lang])
                        f = open(fileName, 'w')
                        f.write(command)
                        os.chmod(fileName, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
                        reqData['command'] = fileName
                        reqData['script_md5'] = md5(command)
                    except Exception as e:
                        logger.error(e,exc_info=1)
                    finally:
                        f.close()

                    addResult = hu.post(serivceName="p_job", restName="/rest/tool/add/", datas=reqData) #/rest/job/add_tool_set/
                    addResultJson = addResult.json()
                    if addResultJson['status'] == 200:
                        result['status'] = 0
                        result['msg'] = '保存成功'
                    else:
                        remove_file(fileName)
                        result['status'] = 1
                        result['msg'] = addResultJson['msg']
                else:
                    result['status'] = 1
                    result['msg'] = '未检测到类别和类型信息，保存失败'
            else:
                result['status'] = 1
                result['msg'] = '保存值为空'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DevopsToolsUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "devops_tools_edit.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/", datas={"id":kwargs.get('pk',0),"offset":0,"limit":"1"}) #/rest/job/list_tool_set/
            tool_list = tool_list_result.get("results", [])
            for tool in tool_list:
                tool['param'] = json.loads(tool['param'])
                #tool_set_prime_type = tool["tool_set_prime_type"]
                tool_set_type = tool["tool_type"]
                if tool_set_type == 5:
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
            logger.error(e,exc_info=1)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            if reqData:
                logger.info("DevopsToolsUpdateView.post_ajax reqData:%s" % (reqData))
                #tool_set_prime_type = reqData.get("tool_set_prime_type", None)
                tool_type = reqData.get("tool_type", None)
                if tool_type:
                    #if tool_set_prime_type == '1' and tool_set_type == '5':
                    script_md5 = reqData['script_md5']
                    command = reqData.get("command",None)
                    history_filename = ""
                    fileName = reqData.get("filename", None)
                    try:
                        #无论是否修改脚本 先做备份
                        history_path = "%s/history/" % (settings.TOOL_SCRIPT_PATH)
                        script_lang_dict = {'shell': 'sh', 'python': 'py', 'yaml': 'yaml'}
                        script_lang = reqData.get("script_lang", "shell")
                        t = time.time()
                        history_filename = "%s%s%s.%s" % (history_path, int(round(t * 1000)), randomCharStr(), script_lang_dict[script_lang])
                        mkdir(history_path)
                        cp(fileName,history_filename)

                        f = open(fileName, 'w')
                        f.write(command)
                        reqData['command'] = fileName
                    except Exception as e:
                        logger.error(e)
                    finally:
                        f.close()
                    new_script_md5 = file_md5(fileName)
                    if new_script_md5 != script_md5:
                        reqData['script_md5'] = new_script_md5
                        reqData['old_script_md5'] = script_md5
                        # 告诉后端接口脚本文件发生变化
                        reqData['script_is_chanage'] = 1
                    else:
                        reqData['old_script_md5'] = script_md5
                        # 告诉后端接口脚本文件没有发生变化
                        reqData['script_is_chanage'] = 0
                    reqData['history_filename'] = history_filename
                    addResult = hu.post(serivceName="p_job", restName="/rest/tool/updateById/", datas=reqData) #/rest/job/update_tool_set/
                    addResultJson = addResult.json()
                    if addResultJson['status'] == 200:
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
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsToolsDeleteView(LoginRequiredMixin,JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            req = self.request
            tool_id = req.GET.get("tool_id",0)
            hu = HttpUtils(req)
            del_result = hu.post(serivceName="p_job", restName="/rest/tool/deleteByToolId/",datas={"tool_id": tool_id}) #/rest/job/delete_tool_set/
            resultJson = del_result.json()
            if resultJson['status'] == 200:
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
                logger.info("DevopsToolsYamlCheckView.post_ajax reqData:%s" % (reqData))
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
            logger.error(e,exc_info=1)
        return self.render_json_response(result)


class DevopsToolVersionByName(LoginRequiredMixin,JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {'status': 200}
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            logger.info("DevopsToolVersionByName.get reqData:%s" % (reqData))
            tool_list_result = hu.get(serivceName="p_job", restName="/rest/tool/list/",datas={'name':reqData['name']})  # /rest/job/list_tool_set/
            tool_list = tool_list_result.get("results", [])
            datas = []
            if len(tool_list) == 1:
                logger.info("DevopsToolVersionByName.get tool_list:%s" % (tool_list))
                tool = tool_list[0]
                tool_id = tool['tool_id']
                datas.append({'id':tool['id'],'tool_id':tool['tool_id'],'name':tool['name'],'tool_version':tool['tool_version']})
                tool_list_result2 = hu.get(serivceName="p_job", restName="/rest/tool/list/",datas={'tool_id': tool_id,'is_history':1})
                tool_list2 = tool_list_result2.get("results", [])
                for tool2 in tool_list2:
                    datas.append({'id': tool2['id'], 'tool_id': tool2['tool_id'], 'name': tool2['name'],'tool_version': tool2['tool_version']})
            result['data'] = datas
        except Exception as e:
            result['status'] = 500
            result['msg'] = '查询异常'
            logger.error(e,exc_info=1)
        return self.render_json_response(result)
