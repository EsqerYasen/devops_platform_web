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
from django.conf import settings

import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class MenuView(LoginRequiredMixin, APIView):
    serializer_class = MenuSerializer
    # TODO
    def get(self, request):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            adminMenu = False
            adminAuth = False
            if self.request.user.is_superuser:
                adminMenu = {
                    "id": -20,
                    "name": "admin",
                    "menu": """
                            <a class="J_menuItem" href="/menu/list/">
                                <i class="fa fa-columns"></i>
                                <span class="nav-label">菜单</span>
                            </a>
                        """,
                    "parent_id": -1,
                    "has_sub_menu": 0,
                    "mgp_v": 0,
                    "mp_v": 1,
                    "ug_v":0
                }
                adminAuth = {
                    "id": -10,
                    "name": "admin",
                    "menu": """
                            <a href="#">
                                <i class="glyphicon glyphicon-user"></i>
                                <span class="nav-label">权限管理</span>
                                <span class="fa arrow"></span>
                            </a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a class="J_menuItem" href="/auth/manager/list/#users">用户</a>
                                </li>
                                <li>
                                    <a class="J_menuItem" href="/auth/manager/list/#usergroups">用户组</a>
                                </li>
                                <li>
                                    <a class="J_menuItem" href="/auth/manager/list/#modules">模块</a>
                                </li>
                                <li>
                                    <a class="J_menuItem" href="/auth/manager/list/#modulegroups">模块组</a>
                                </li>

                            </ul>
                        """,
                    "parent_id": -1,
                    "has_sub_menu": 0,
                    "mgp_v": 0,
                    "mp_v": 1,
                    "ug_v":0
                }


            sql = """
                SELECT
                    dmm.id, dmm.name, dmm.menu, dmm.parent_id, dmm.has_sub_menu, MAX(mgp.value) AS mgp_v, MAX(mp.value) AS mp_v, MAX(ugp.value) AS ug_v
                FROM
                    (select * from {1}.{3} where is_enabled<>0) dmm
                    JOIN (select * from {1}.devops_auth_module) m ON dmm.id = m.open_id AND m.open_db = '{1}' AND open_table = '{3}'
                    LEFT OUTER JOIN {1}.devops_auth_module_groups mgs ON m.id = mgs.module_id
                    LEFT OUTER JOIN (select * from {1}.devops_auth_user_group_permission where is_enabled<>0) ugp ON ugp.module_id = m.id
                    LEFT OUTER JOIN (select * from {1}.devops_auth_module_permission where user_id = {0} and is_enabled<>0) mp ON m.id = mp.module_id
                    LEFT OUTER JOIN (select * from {1}.auth_user where id = {0}) u ON mp.user_id = u.id
                    LEFT OUTER JOIN (select * from {1}.devops_auth_module_group where owner_id = {0}) mg ON mgs.group_id = mg.id
                    LEFT OUTER JOIN (select * from {1}.devops_auth_module_group_permission where is_enabled<>0) mgp ON mgp.group_id = mgs.group_id
                    LEFT OUTER JOIN (select * from {1}.devops_auth_module_groups_users where user_id = {0} and is_enabled<>0 ) mgu ON mgu.group_id = mgs.group_id
                    LEFT OUTER JOIN (select group_id,user_id from {1}.auth_user_groups where user_id = {0}) ug ON (ug.group_id = ugp.group_id )
                    where (mgu.user_id={0} or mgu.user_id={0} or mp.user_id={0} or ug.user_id={0})
                    group by m.open_db, m.open_table, m.open_id order by dmm.order_index desc
            """.format(self.request.user.id, settings.DB_NAME['WEB_DB'], settings.DB_NAME['WEB_DB'], 'devops_menu_menuitem')
            data = DBUtils.query(sql)
            if self.request.user.is_superuser:
                data.append(adminMenu)
                data.append(adminAuth)
            result['info'] = (data)
            result['status'] = 0
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['info'] = []
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

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
            sql = "SELECT id, name, menu, parent_id, has_sub_menu, order_index  FROM  devops_menu_menuitem where {0} and is_enabled = 1 order by order_index desc".format(condition)
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

                    m = Menu(name=name,menu=menu,parent_id=parentId,has_sub_menu=has_sub,created_by=request.user.username,updated_by=request.user.username, order_index=1)
                    m.save()
                    m = Menu.objects.get(id=m.id)
                    m.order_index=m.id
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

class MenuItemsOrder(LoginRequiredMixin, APIView):
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()
        print(input_dict)
        print (request.POST.get('from', '{}'))
        _f = request.POST.get('from', '{}')
        print (request.POST.get('to', '{}'))
        _t = request.POST.get('to', '{}')
        _from = json.loads(_f)
        _to = json.loads(_t)
        m1 = None
        m2 = None
        print(_from, _to)
        if _from and _from['id']:
            m1 = Menu.objects.get(id=_from['id'])
        if _to and _to['id']:
            m2 = Menu.objects.get(id=_to['id'])
        print (m1.order_index, m1)
        print (m2.order_index, m2)
        tempOrderIdx = None
        if m1 and m2:
            tempOrderIdx = m1.order_index
            m1.order_index = m2.order_index;
            m1.save()
            m2.order_index = tempOrderIdx;
            m2.save()
        return HttpResponse(json.dumps(result),content_type='application/json')
