#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: Xuan.Chen
# @Date  : 2018/9/12
# @Desc  :

from rest_framework.views import APIView
from django.http.response import HttpResponse
from django.conf import settings
import os

import logging,json

logger = logging.getLogger("devops_pre_srb")

class GetFileList(APIView):
    def get(self, request):
        data = request.GET
        file_list = []
        for parent, dirnames, filenames in os.walk(settings.FILES_DIR):
            for filename in filenames:
                file_list.append(filename)

        return HttpResponse(json.dumps(file_list), content_type='application/json')
