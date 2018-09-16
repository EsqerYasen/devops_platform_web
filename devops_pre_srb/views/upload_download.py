#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : upload_download.py
# @Author: Xuan.Chen
# @Date  : 2018/9/10
# @Desc  :

from rest_framework.views import APIView


from braces.views import *
from django.views.generic import *
from django.http import StreamingHttpResponse
from common.utils.redis_utils import *
import os,ctypes,platform
from django.conf import settings
import logging

logger = logging.getLogger('devops_platform_log')

class DownloadFile(APIView):
    def get(self, request):
        try:
            req = self.request.GET
            filename = req['filename']
            filepath = os.path.join(settings.FILES_DIR, filename)
            response = StreamingHttpResponse(readFile(filepath))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
                filename.encode('utf-8').decode('ISO-8859-1'))

        except Exception as e:
            logger.error(e,exc_info=1)

        return response


def get_free_space_gb(folder):
    """ Return folder/drive free space (in Gbytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024


class UploadFile(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):

        try:

            free_space = get_free_space_gb(settings.FILES_DIR)
            if free_space < 0.2:
                result_json = {"status": 500, "msg": "磁盘空间不足"}
                return self.render_json_response(result_json)
            username = request.user.username
            file_handle = request.FILES.get('files', None)
            handle_uploaded_file(file_handle)
            result_json = {"status": 200, "msg": "上传成功"}

        except Exception as e:
            result_json = {"status": 500,"msg":"上传失败"}
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)


def handle_uploaded_file(f):
    try:
        if not os.path.exists(settings.FILES_DIR):
            os.makedirs(settings.FILES_DIR)
        dst_path = os.path.join(settings.FILES_DIR, f.name)
        with open(dst_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except Exception as e:
        logger.error(e, exc_info=1)



def readFile(filename, chunk_size=512):
    try:
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    except Exception as e:
        logger.error(e, exc_info=1)
