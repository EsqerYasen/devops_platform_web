from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import UPLOAD_SCRIPT_PATH
from common.utils.HttpUtils import *
import os,logging,subprocess

logger = logging.getLogger('devops_platform_log')

class FileManageView(LoginRequiredMixin, TemplateView):
    template_name = "file_manage.html"

    def get_context_data(self, **kwargs):
        context = super(FileManageView, self).get_context_data(**kwargs)

        return context

class FileTreeView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        hu = HttpUtils()
        resultJson = hu.get(serivceName="job", restName="/rest/file/list_tree/", datas={})
        return self.render_json_response(resultJson)

class FileTreeCreateFolder(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        saveJson = request.POST.get('saveJson',{})
        path = request.POST.get('path',None)
        resultJson = {}
        if path:
            hu = HttpUtils()
            result = hu.post(serivceName="job", restName="/rest/file/add/", datas=saveJson)
            resultJson = result.json()
            if resultJson['status'] == "SUCCESS":
                try:
                    os.makedirs(UPLOAD_SCRIPT_PATH + path)
                except Exception as e:
                    logger.log(e)
        else:
            resultJson['status'] = 'fail'
            resultJson['msg'] = '文件夹路径为空'
        return self.render_json_response(resultJson)

class FileTreeUploadFile(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        files = request.FILES
        path = request.POST.get("path", None)
        resultJson = {}
        if path:
            saveJson = request.POST.get("saveJson",None)
            hu = HttpUtils()
            result = hu.post(serivceName="job", restName="/rest/file/add/", datas=saveJson)
            resultJson = result.json()
            if resultJson['status'] == "SUCCESS":
                try:
                    file = files['files']
                    destination = open(os.path.join(UPLOAD_SCRIPT_PATH + path, file.name), 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()

                    (status, output) = subprocess.getstatusoutput("sed -i 's/\r$//' "+UPLOAD_SCRIPT_PATH+path+file.name)
                    if status != 0:
                        logger.error(output);
                except Exception as e:
                    logger.error(e)
        else:
            resultJson['status'] = 'fail'
            resultJson['msg'] = '文件夹路径为空'
        return self.render_json_response(resultJson)

