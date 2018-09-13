#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: Xuan.Chen
# @Date  : 2018/9/12
# @Desc  :

from rest_framework.views import APIView
from django.http.response import HttpResponse
from django.conf import settings
import os,logging,json

logger = logging.getLogger('devops_platform_log')

class GetFileList(APIView):
    def get(self, request):
        try:
            data = request.GET
            file_list = []
            for parent, dirnames, filenames in os.walk(settings.FILES_DIR):
                for filename in filenames:
                    file_list.append(filename)
        except Exception as e:
            logger.error(e,exc_info=1)

        return HttpResponse(json.dumps(file_list), content_type='application/json')
