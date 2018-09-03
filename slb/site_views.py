from braces.views import *
from django.views.generic import *
from django.http import HttpResponse
from common.utils.HttpUtils import HttpUtils
import logging,json

logger = logging.getLogger('devops_platform_log')

class ConfigPreviewView(LoginRequiredMixin,JSONResponseMixin,AjaxResponseMixin,View):
    def post_ajax(self, request, *args, **kwargs):
        """
        站点管理 配置文件预览 Ajax post
        :param request:
        :return:
        """
        result = {}
        try:
            config = request.POST.get("config",None)
            if config:
                hu = HttpUtils(request)
                hu.post(serivceName='p_job',restName='/rest/slb/configpreview',datas=config)
            else:
                result['status'] = "500"
                result['msg'] = "预览参数为空"
        except Exception as e:
            logger.error(e,exc_info=1)
            result['status'] = "500"
            result['msg'] = "预览异常"
        return HttpResponse(json.dumps(result), content_type='application/json')


class NginxClusterHostById(LoginRequiredMixin,JSONResponseMixin,AjaxResponseMixin,View):
    def get_ajax(self, request, *args, **kwargs):
        """
        发布 获取nginx 机器
        :param request:
        :return:
        """
        results = {}
        try:
            group_id = request.GET.get("id",None)
            vs = request.GET.get("vs",None)
            if group_id and vs:
                hu = HttpUtils(request)
                result = hu.get(serivceName='p_job', restName='/rest/slb/nginxclusterhostbyid', datas={"id":id,"vs":vs})
                if result['status'] == 200:
                    results['status'] = 200
                    results['data'] =  result['data']
                else:
                    results['status'] = 500
                    results['msg'] = "查询失败"
            else:
                results['status'] = 500
                results['msg'] = "查询参数为空"
        except Exception as e:
            logger.error(e,exc_info=1)
            results['status'] = 500
            results['msg'] = "查询异常"
        return HttpResponse(json.dumps(results), content_type='application/json')


class ConfigVersionDiff(LoginRequiredMixin,JSONResponseMixin,AjaxResponseMixin,View):
    def get_ajax(self, request, *args, **kwargs):
        """
        站点 配置版本对比
        :param request:
        :return:
        """
        results = {}
        try:
            req_get = request.GET
            id = req_get.get("id", None)
            v1 = req_get.get("v1", None)
            v2 = req_get.get("v2", None)
            if id and v1 and v2:
                hu = HttpUtils(request)
                result = hu.get(serivceName='p_job', restName='/rest/slb/configversiondiff',datas={"id": id, "v1": v1,"v2":v2})
                if result['status'] == 200:
                    results['status'] = 200
                    results['data'] =  result['data']
                else:
                    results['status'] = 500
                    results['msg'] = "查询失败"
        except Exception as e:
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(results), content_type='application/json')

class MngSiteCreateOrUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin,View):
    def post_ajax(self, request, *args, **kwargs):
        """
        站点新增
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = {}
        try:
            input_param = results.POST
            if input_param:
                id = input_param['id']
                hu = HttpUtils(request)
                if int(id) < 0:
                    del input_param['id']
                    post_results = hu.post(serivceName='p_job',restName='/rest/slb/addMngSite/',datas=input_param)
                    post_results = post_results.json()
                    if post_results['status'] == 200:
                        results['status'] = 200
                        results['msg'] = "新增成功"
                        results['id'] = post_results['id']
                    else:
                        results['status'] = 500
                        results['msg'] = "新增失败"
                elif int(id) > 0:
                    post_results = hu.post(serivceName='p_job', restName='/rest/slb/updateMngSite/', datas=input_param['data'])
                    post_results = post_results.json()
                    if post_results['status'] == 200:
                        results['status'] = 200
                        results['msg'] = "新增成功"
                        results['id'] = post_results['id']
                    else:
                        results['status'] = 500
                        results['msg'] = "新增失败"
            else:
                results['status'] = 500
                results['msg'] = "新增参数为空"
        except Exception as e:
            logger.error(e,exc_info=1)
            results['status'] = 500
            results['msg'] = "新增异常"
        return HttpResponse(json.dumps(results), content_type='application/json')
