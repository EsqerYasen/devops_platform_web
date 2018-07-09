from devops_menu.serializers import *
from django.apps import apps
from braces.views import *
from django.views.generic import *
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import auth
from django.core.paginator import Paginator
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from devops_menu.models.Devops_Menu import MenuItem as Menu
# from devops_menu.models.Module_group import Module_group
# from devops_menu.models.Module_groups import Module_groups
# from devops_menu.models.Module_groups_users import Module_groups_users
# from devops_menu.models.Module_permission import Module_permission
# from devops_menu.models.Module_group_permission import Module_group_permission
# from devops_menu.models.User_group_permission import User_group_permission
from django.core import serializers
from django.db import connection
from common.utils import DBUtils

import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class MenuItemsView(LoginRequiredMixin, APIView):
    serializer_class = MenuSerializer
    # TODO
    def get(self, request):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            # type = (request.GET.get('type', "user"))
            request.user
            cursor = connection.cursor()
            result['status'] = 0
            condition = "1"
            if "isParent" in reqData:
                condition = "has_sub_menu =1 "
            else:
                condition = 1
            sql = "SELECT id, name, menu, parent_id, has_sub_menu FROM  devops_menu_menuitem where {0} and is_enabled = 1".format(condition)
            data = DBUtils.query(sql)
            result['info'] = (data)
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['info'] = []
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

    # TODO
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()
        print(input_dict)
        # {'offset': 0, 'limit': 10, 'name': '423', 'menu': '2314234', 'parentId': '-1', 'has_sub': '1', 'csrfmiddlewaretoken': 'EJvAtR9zUt8EFQq862e7ImUDe3aEm0IX05PQJ4ia1QPz9tT2CQvGyyo16jomfPzu'}

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = input_dict.get("id")
                    m = Menu.objects.get(id=id)
                    m.name = input_dict.get('name', m.name)
                    m.menu = input_dict.get('menu', m.menu)
                    m.parent_id = input_dict.get('parentId', m.parent_id)
                    m.has_sub_menu = input_dict.get('has_sub', m.has_sub_menu)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    menu = input_dict.get('menu', '')
                    parentId = input_dict.get('parentId', -1)
                    has_sub = input_dict.get('has_sub', 0)
                    name = input_dict.get('name')

                    error = ''
                    if not name:
                        error = 'name不能为空'

                    if error:
                        return HttpResponseBadRequest(error)

                    m = Menu(name=name,menu=menu,parent_id=parentId,has_sub_menu=has_sub,created_by=request.user.username,updated_by=request.user.username)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = MenuSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')


