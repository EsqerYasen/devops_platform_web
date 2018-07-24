from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from common.utils.redis_utils import *
from common.utils.common_utils import *
from devops_platform_web.settings import BASE_DIR
from django.http import StreamingHttpResponse
import logging,xlrd,threading

logger = logging.getLogger('devops_platform_log')

class HostGroupView(LoginRequiredMixin, OrderableListMixin, TemplateView):
    template_name = "host_group.html"

    def get_context_data(self, **kwargs):
        context = super(HostGroupView, self).get_context_data(**kwargs)
        try:
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hu = HttpUtils(self.request)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            context['hostGroup_list'] =  hostgroupResult.get("data", [])
        except Exception as e:
            logger.error(e)
        return context


class HostGroupListView(LoginRequiredMixin, OrderableListMixin, TemplateView):
    template_name = "host_tree_copy.html"

    def get_context_data(self, **kwargs):
        context = super(HostGroupListView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
            context['hostGroup_list'] =  json.dumps(hostgroupResult.get("results", []))
        except Exception as e:
            logger.error(e)
        return context



class HostGroupImport(LoginRequiredMixin, TemplateView,AjaxResponseMixin, JSONResponseMixin, View):
    template_name = "host_tree_manage.html"

    def get_context_data(self, **kwargs):
        context = super(HostGroupImport, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
            context['hostGroup_list'] =  json.dumps(hostgroupResult.get("results", []))
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            username = request.user.username
            host_group_import_key = "%s_host_group_import" % username
            isImportRun = RedisBase.hget(host_group_import_key, "is_run", 1)
            if isImportRun is None or isImportRun == 0:
                RedisBase.delete(host_group_import_key, 1)
                host_import_key2 = "%s_msg" % host_group_import_key
                RedisBase.delete(host_import_key2, 1)
                assert_file = request.FILES.get('files', None)
                wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
                ta = threading.Thread(target=import_host_group_fn, args=(request, wb,))
                ta.start()
                time.sleep(1)
                result_json = {"status": 200, "msg": "后台正在导入，请点击“查看后台任务”按钮查看结果"}
            else:
                result_json = {"status": 500, "msg":"您有后台任务正在执行导入操作，请稍后操作导入"}
        except Exception as e:
            result_json = {"status": 500,"msg":"导入执行异常"}
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)

def import_host_group_fn(req, wb):
    total = 0
    success_count = 0
    fail_count = 0
    try:
        username = req.user.username
        start_t = time.time()
        total = wb.sheets()[0].nrows
        log_path = "/opt/devops/host_operation_log/host_group_import_logs/%s/" % (username)
        mkdir(log_path)
        host_group_import_key = "%s_host_gorup_import" % username
        host_group_import_key2 = "%s_msg" % host_group_import_key
        RedisBase.hset(host_group_import_key, "is_run", 1, 1)
        RedisBase.hset(host_group_import_key, "total", total - 1, 1)
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_t))
        file_log = open("%s%s.log" % (log_path, str(start_t).replace('.', '')), 'a+')
        file_log.write("用户:%s   批量导入机器组信息 时间:%s\n" % (username, curtime))
        wb_sheets = wb.sheets()[0]
        hu = HttpUtils(req)

        for i in range(1, total):
            row = wb_sheets.row_values(i)
            biz_brand = row[0].strip().lower().replace('.', '-').replace('_', '-')
            biz_group = row[1].strip().lower().replace('.', '-').replace('_', '-')
            physical_idc = row[2].strip().lower().replace('.', '-').replace('_', '-')
            deployment_environment = row[3].strip().lower().replace('.', '-').replace('_', '-')
            logical_idc = row[4].strip().lower().replace('.', '-').replace('_', '-')
            biz_module = row[5].strip().lower().replace('.', '-').replace('_', '-')

            info_str = "品牌:%s 业务线:%s 机房:%s 环境:%s 区域:%s 应用:%s " %(biz_brand,biz_group,physical_idc,deployment_environment,logical_idc,biz_module)
            if biz_brand and biz_group and physical_idc and deployment_environment and logical_idc and biz_module:
                appendResult = hu.post(serivceName="cmdb", restName="/rest/hostgroup/addnode/",datas={"node_name1": biz_brand,
                                                                                                      "node_name2": biz_group,
                                                                                                      "node_name3": physical_idc,
                                                                                                      "node_name4": deployment_environment,
                                                                                                      "node_name5": logical_idc,
                                                                                                      "node_name6": biz_module
                                                                                                      })
                append = appendResult.json()
                if append['status'] == 200:
                    success_count += 1
                    file_log.write(info_str + "新增成功\n")
                elif append['status'] == 400:
                    fail_count += 1
                    RedisBase.lpush(host_group_import_key2,info_str+"重复节点放弃新增", 1)
                    file_log.write(info_str+"重复节点放弃新增\n")
                else:
                    fail_count += 1
                    RedisBase.lpush(host_group_import_key2, info_str + "新增失败", 1)
                    file_log.write(info_str + "新增失败\n")
            else:
                fail_count += 1
                none_info = info_str + "存在空节点 放弃导入"
                RedisBase.lpush(host_group_import_key2,none_info)
                file_log.write(none_info)

            RedisBase.hset(host_group_import_key, "index", i, 1)
            RedisBase.hset(host_group_import_key, "success_count", success_count, 1)
            RedisBase.hset(host_group_import_key, "fail_count", fail_count, 1)
    except Exception as e:
        RedisBase.lpush(host_group_import_key2, info_str + "导入异常 停止导入", 1)
        file_log.write(info_str + "导入异常 停止导入\n")
        logger.error(e, exc_info=1)
    finally:
        if file_log:
            file_log.close()
        RedisBase.expire(host_group_import_key, 100, 1)
        RedisBase.expire(host_group_import_key2, 90, 1)
        RedisBase.hset(host_group_import_key, "is_run", 0, 1)


def HostGroupTemplateDownload(request):
    def readFile(filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = '业务树导入模板.xlsx'
    filename = os.path.join(BASE_DIR+'/static/','业务树导入模板.xlsx')
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name.encode('utf-8').decode('ISO-8859-1'))
    return response



class GetHostGroupImportStatus(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            index = int(request.GET.get("index",0))
            username = request.user.username
            host_import_key = "%s_host_gorup_import" % username
            host_import_key2 = "%s_msg" % host_import_key
            isImportRun = int(RedisBase.hget(host_import_key, "is_run", 1))
            result_json['is_run'] = isImportRun
            if isImportRun is not None or isImportRun == 1:
                result_json['total'] = int(RedisBase.hget(host_import_key, "total", 1))
                result_json['run_index'] = int(RedisBase.hget(host_import_key, "index", 1))
                result_json['success_count'] = int(RedisBase.hget(host_import_key, "success_count", 1))
                result_json['fail_count'] = int(RedisBase.hget(host_import_key, "fail_count", 1))
                msg_list = RedisBase.lrange(redisKey=host_import_key2, start=index, db=1)
                if msg_list:
                    data_list = []
                    for msg in msg_list:
                        index += 1
                        data_list.append(str(msg,encoding='utf-8'))
                    result_json['status'] = 200
                    result_json['data'] = data_list
                    result_json['index'] = index
                else:
                    result_json['status'] = 200
                    result_json['data'] = []
                    result_json['index'] = index
            else:
                result_json['status'] = 500
                result_json['msg'] = "没有正在执行的任务"
        except Exception as e:
            logger.error(e,exc_info=1)
            result_json['status'] = 500
            result_json['msg'] = "查询异常"
        return self.render_json_response(result_json)


class HostGroupRenameNode(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            hu = HttpUtils(request)
            req_post = request.POST
            group_id = req_post.get("group_id",None)
            level = req_post.get("level",None)
            name = req_post.get("name",None)
            if group_id and level is not None and level != "" and name:
                renamenode_results = hu.post(serivceName="cmdb", restName="/rest/hostgroup/renamenode/", datas={"group_id":group_id,"level":level,"name":name})
                renamenode_result_json = renamenode_results.json()
                result_json['status'] = renamenode_result_json['status']
                result_json['msg'] = renamenode_result_json['msg']
            else:
                result_json['status'] = 500
                result_json['msg'] = "参数为空"
        except Exception as e:
            logger.error(e,exc_info=1)
            result_json['status'] = 500
            result_json['msg'] = "更新异常(web)"
        return self.render_json_response(result_json)


class HostGroupDeleteNode(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {}
        try:
            hu = HttpUtils(request)
            req_post = request.POST
            group_id = req_post.get("group_id",None)
            level = req_post.get("level",None)
            if group_id and level is not None and level != "":
                renamenode_results = hu.post(serivceName="cmdb", restName="/rest/hostgroup/deletenode/", datas={"group_id":group_id,"level":level})
                renamenode_result_json = renamenode_results.json()
                result_json['status'] = renamenode_result_json['status']
                result_json['msg'] = renamenode_result_json['msg']
            else:
                result_json['status'] = 500
                result_json['msg'] = "参数为空"
        except Exception as e:
            logger.error(e,exc_info=1)
            result_json['status'] = 500
            result_json['msg'] = "删除异常(web)"
        return self.render_json_response(result_json)