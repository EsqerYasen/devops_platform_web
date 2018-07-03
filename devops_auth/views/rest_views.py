from devops_auth.serializers import *
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
from devops_auth.models.Module import Module
from devops_auth.models.Module_group import Module_group
from devops_auth.models.Module_groups import Module_groups
from devops_auth.models.Module_groups_users import Module_groups_users
from devops_auth.models.Module_permission import Module_permission
from devops_auth.models.Module_group_permission import Module_group_permission
from devops_auth.models.User_group_permission import User_group_permission
from django.core import serializers
from django.db import connection

from common.utils.auth_utils import *

import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class AuthVerifyView(LoginRequiredMixin, APIView):
    # 权限效验
    def get(self, request):
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        result = auth_utils.verify(reqData, request.user)
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleView(LoginRequiredMixin, APIView):
    serializer_class = ModuleSerializer

    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        try:
            id = reqData["id"]
            module = Module.objects.get(id=id)
            result['status'] = 0
            result['info'] = ModuleSerializer(module).data
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "模块不存在"

        return HttpResponse(json.dumps(result),content_type='application/json')

    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()

        if len(input_dict) > 0:
            try:
                if 'id' in input_dict.keys():
                    id = input_dict.get("id")
                    m = Module.objects.get(id=id)
                    m.name = input_dict.get('name', m.name)
                    m.alias = input_dict.get('alias', m.alias)
                    m.url = input_dict.get('url', m.url)
                    m.open_db = input_dict.get('open_db', m.open_db)
                    m.open_table = input_dict.get('open_table', m.open_table)
                    m.open_id = input_dict.get('open_id', m.open_id)
                    m.owner_id = input_dict.get('owner_id', m.owner_id)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    name = input_dict.get('name', '')
                    alias = input_dict.get('alias', '')
                    url = input_dict.get('url', '')
                    open_db = input_dict.get('open_db', '')
                    open_table = input_dict.get('open_table', '')
                    open_id = input_dict.get('open_id', '')
                    owner_id = input_dict.get('owner_id', '')

                    error = ''
                    if not name:
                        error = '模块名不能为空'
                    elif not alias:
                        error = '别名不能为空'
                    elif not url:
                        error = 'URL不能为空'
                    elif not owner_id:
                        error = 'OwnerId不能为空'

                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module(name=name,alias=alias,url=url,owner_id=owner_id, created_by=request.user.username,updated_by=request.user.username, open_table=open_table, open_db=open_db, open_id=open_id)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = ModuleSerializer(m).data
            except Exception as e:

                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])

        return HttpResponse(json.dumps(result),content_type='application/json')

class ModulesView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        result['status'] = 0
        data = Module.objects.filter(is_enabled=1)
        result['info'] = serializers.serialize('json',  data)
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModulesPermissionView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        result['info'] = auth_utils.get_user_permission({"user_id": int(request.user.id), "user_group_ids": request.user.groups.values('id')});
        return HttpResponse(json.dumps(result),content_type='application/json')

class UsersView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        result['status'] = 0
        data = User.objects.filter(is_active=1).values('id','username', 'first_name', 'last_name', 'is_superuser', 'groups')
        result['info'] = list(data)
        return HttpResponse(json.dumps(result),content_type='application/json')

def dictFetchAll(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class userModulesView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            id = int(reqData["id"])
            if id is -1:
                id = request.user.id
            cursor = connection.cursor()
            result['status'] = 0
            sql = "SELECT damp.id, damp.user_id, dam.name, dam.owner_id, damp.value as privilege FROM devops_auth_module dam join devops_auth_module_permission damp on dam.id = damp.module_id and dam.is_enabled =1 and  damp.is_enabled=1 where damp.user_id=%s"
            cursor.execute(sql, id)
            data = dictFetchAll(cursor)
            cursor.close()
            connection.close()
            result['info'] = (data)
        except Exception as e:
            result['status'] = 1
            result['info'] = []
            result['msg'] = ""

        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleGroupView(LoginRequiredMixin, APIView):
    serializer_class = ModuleGroupSerializer

    # TODO
    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        try:
            id = request.GET.get('id', None)# reqData["order_by"] reqData["id"]
            if id is None:
                m = Module_group.objects.filter(is_enabled=1).values('name', 'owner_id', 'created_by', 'id')
                result['info'] = list(m)
            else:
                cursor = connection.cursor()
                type = request.GET.get('type', 'module')
                extraParam = ""
                if type == "module":
                    sql = "SELECT damg.id AS group_id, dam.id AS id, dam.name AS name FROM devops_auth_module_group damg JOIN devops_auth_module_groups admgs on admgs.group_id=damg.id join devops_auth_module dam ON admgs.module_id = dam.id AND damg.is_enabled = 1 AND dam.is_enabled = 1  where {0}" .format("damg.id=%s")
                else :
                    sql = "SELECT damgu.id as id, concat(au.username, \"(\",au.first_name, \" \", au.last_name,\")\") as name, damg.id as group_id FROM devops_auth_module_group damg JOIN devops_auth_module_groups_users damgu ON damgu.group_id = damg.id JOIN auth_user au ON damgu.user_id = au.id AND damgu.is_enabled = 1 AND damg.is_enabled = 1  where {0}".format("damg.id=%s")
                cursor.execute(sql, id)
                data = dictFetchAll(cursor)
                result['info'] = data
                cursor.close()
                connection.close()
            result['status'] = 0

        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

    # TODO
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = input_dict.get("id")
                    m = Module_group.objects.get(id=id)
                    m.name = input_dict.get('name', m.name)
                    m.owner_id = input_dict.get('owner_id', m.owner_id)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    name = input_dict.get('name', '')
                    owner_id = input_dict.get('owner_id', '')

                    error = ''
                    if not name:
                        error = '名称不能为空'
                    elif not owner_id:
                        error = 'OwnerId不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module_group(name=name,owner_id=owner_id,created_by=request.user.username,updated_by=request.user.username)
                    m.save()
                    if "value" in input_dict.keys():
                        value = input_dict.get('name')
                        Module_group_permission(group_id=m.id,value=value,created_by=request.user.username,updated_by=request.user.username)
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = ModuleGroupSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleGroupsView(LoginRequiredMixin, APIView):
    # TODO
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = request.data["id"]
                    m = Module_groups.objects.get(id=id)
                    if 'is_enabled' in input_dict.keys:
                        m.delete()
                    else:
                        m.module_id = input_dict.get('module_id', m.module_id)
                        m.group_id = input_dict.get('group_id', m.group_id)
                        m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    module_id = input_dict.get('module_id', '')
                    group_id = input_dict.get('group_id', '')

                    error = ''
                    if not module_id:
                        error = 'ModuleId不能为空'
                    elif not group_id:
                        error = 'GroupId不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module_groups(module_id=module_id,group_id=group_id)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = ModuleGroupsSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleGroupsUsersView(LoginRequiredMixin, APIView):
    # TODO
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()


        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = request.data["id"]
                    m = Module_groups_users.objects.get(id=id)
                    if "is_enabled" in input_dict.keys():
                        m.delete()
                    else:
                        m.user_id = input_dict.get('user_id', m.user_id)
                        m.group_id = input_dict.get('group_id', m.group_id)
                        m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    user_id = input_dict.get('user_id', '')
                    group_id = input_dict.get('group_id', '')

                    error = ''
                    if not user_id:
                        error = 'UserId不能为空'
                    elif not group_id:
                        error = 'GroupId不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module_groups_users(user_id=user_id,group_id=group_id)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = ModuleGroupUserSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModulePermissionView(LoginRequiredMixin, APIView):
    serializer_class = ModulePermissionSerializer
    def get(self, request):
        result = {}

        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            id = int(reqData["id"])
            type = (request.GET.get('type', "user"))# reqData["order_by"]
            result['status'] = 0
            if id is -1:
                result['info'] = []
                return HttpResponse(json.dumps(result),content_type='application/json')
            cursor = connection.cursor()
            param = ""
            extraParam = ""
            if type == "module_id":
                sql = "SELECT damp.id, damp.user_id, concat(au.username, \"(\",au.first_name, \" \", au.last_name,\")\") as name, dam.id as module_id, dam.owner_id, damp.value as privilege FROM devops_auth_module dam join devops_auth_module_permission damp on dam.id = damp.module_id join auth_user au on au.id =damp.user_id and dam.is_enabled =1 and  damp.is_enabled=1 where {0}"
                param = "damp.module_id=%s"
            else:
                param = "damp.user_id=%s"
                sql = "SELECT damp.id, damp.user_id, dam.name, dam.id as module_id, dam.owner_id, damp.value as privilege FROM devops_auth_module dam join devops_auth_module_permission damp on dam.id = damp.module_id and dam.is_enabled =1 and  damp.is_enabled=1 where {0}"
            sql = sql.format(param)
            cursor.execute(sql, id)
            data = dictFetchAll(cursor)
            cursor.close()
            connection.close()
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

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = request.data["id"]
                    m = Module_permission.objects.get(id=id)
                    m.user_id = input_dict.get('user_id', m.user_id)
                    m.module_id = input_dict.get('module_id', m.module_id)
                    m.value = input_dict.get('value', m.value)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    user_id = input_dict.get('user_id', '')
                    module_id = input_dict.get('module_id', '')
                    value = input_dict.get('value', '')

                    error = ''
                    if not user_id:
                        error = 'UserID不能为空'
                    elif not module_id:
                        error = 'ModuleId不能为空'
                    elif not value:
                        error = 'Value不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module_permission(user_id=user_id,module_id=module_id,value=value,created_by=request.user.username,updated_by=request.user.username)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = False
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class UserGroupView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            id = int(reqData["id"])
            type = (request.GET.get('type', "user"))
            cursor = connection.cursor()
            result['status'] = 0
            if id is -1:
                cursor.close()
                result['info'] = []
                # sql = "SELECT ag.name, ag.id, daugp.value, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1"
                return HttpResponse(json.dumps(result),content_type='application/json')
            else:
                if type == "module_id":
                    param = "daugp.module_id=%s"
                    sql = "SELECT ag.name, ag.id, daugp.value  as privilege, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1 where {0}".format(param)
                else:
                    param = "daugp.group_id=%s"
                    sql = "SELECT dam.name, dam.id, daugp.value  as privilege, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id join  devops_auth_module dam on dam.id= daugp.module_id and daugp.is_enabled = 1 and dam.is_enabled=1 where {0}".format(param)
                    print(sql)
            cursor.execute(sql, id)
            data = dictFetchAll(cursor)
            cursor.close()
            connection.close()
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

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = request.data["id"]
                    g = Group.objects.get(id=id)
                    g.group_id = input_dict.get('group_id', g.group_id)
                    g.user_id = input_dict.get('user_id', g.user_id)
                    g.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    group_id = input_dict.get('group_id', '')
                    user_id = input_dict.get('user_id', '')

                    error = ''
                    if not group_id:
                        error = 'GroupId不能为空'
                    elif not user_id:
                        error = 'UserId不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    g = Group(group_id=group_id,user_id=user_id)
                    g.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = g.id
                    # result['info'] = ModuleSerializer(g).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class UserGroupPermissionView(LoginRequiredMixin, APIView):
    # TODO
    def get(self, request):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            id = int(reqData["id"])
            type = (request.GET.get('type', "user"))
            cursor = connection.cursor()
            result['status'] = 0
            if id is -1:
                cursor.close()
                result['info'] = []
                # sql = "SELECT ag.name, ag.id, daugp.value, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1"
                return HttpResponse(json.dumps(result),content_type='application/json')
            else:
                if type == "module_id":
                    param = "daugp.module_id=%s"
                    sql = "SELECT ag.name, daugp.id, ag.id as group_id, daugp.value  as privilege, daugp.created_by, daugp.module_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1 where {0}".format(param)
                else:
                    param = "daugp.group_id=%s"
                    sql = "SELECT dam.name, daugp.id, dam.id as module_id, daugp.value  as privilege, daugp.id as user_group_permission_id,daugp.created_by, daugp.module_id, group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id join  devops_auth_module dam on dam.id= daugp.module_id and daugp.is_enabled = 1 and dam.is_enabled=1 where {0}".format(param)
            print(2222, sql)
            cursor.execute(sql, id)
            data = dictFetchAll(cursor)
            cursor.close()
            connection.close()
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

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = input_dict.get("id")
                    m = User_group_permission.objects.get(id=id)
                    m.group_id = input_dict.get('group_id', m.group_id)
                    m.module_id = input_dict.get('module_id', m.module_id)
                    m.value = input_dict.get('value', m.value)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    group_id = input_dict.get('group_id', '')
                    module_id = input_dict.get('module_id', '')
                    value = input_dict.get('value', '')
                    is_enabled = input_dict.get('is_enabled', 1)

                    error = ''
                    if not group_id:
                        error = 'GroupId不能为空'
                    elif not module_id:
                        error = 'ModuleId不能为空'
                    elif not value:
                        error = 'Value不能为空'

                    if error:
                        return HttpResponseBadRequest(error)

                    m = User_group_permission(group_id=group_id,module_id=module_id,value=value,is_enabled=is_enabled,created_by=request.user.username,updated_by=request.user.username)
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = UserGroupPermissionSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleGroupPermissionView(LoginRequiredMixin, APIView):
    serializer_class = ModuleGroupPermissionSerializer
    # TODO
    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        type = (request.GET.get('type', "user"))
        result['status'] = 0
        try:
            id = reqData["id"]
            if id is -1:
                result['status'] = 0
                result['info'] = []
                # sql = "SELECT ag.name, ag.id, daugp.value, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1"
                return HttpResponse(json.dumps(result),content_type='application/json')
            else:
                pass
                # if type == "module_id":
                #     param = "dam.id=%s"
                #     sql = "SELECT damg.id, damg.name,dam.id as module_id, damgp.value,damg.owner_id   FROM devops_workshop_dev_web.devops_auth_module_group_permission damgp join devops_auth_module_group damg on damg.id= damgp.group_id join devops_auth_module_groups damgs on damgs.group_id=damgp.group_id join devops_auth_module dam on dam.id = damgs.module_id and damgp.is_enabled=1 and damgs.is_enabled = 1 and dam.is_enabled = 1 and damg.is_enabled = 1 where {0}".format(param)
                # else:
                #     param = "daugp.group_id=%s"
                #     sql = "SELECT ag.name, ag.id, daugp.value, daugp.created_by, daugp.module_id,group_id FROM  devops_auth_user_group_permission daugp join  auth_group ag on ag.id= daugp.group_id and daugp.is_enabled = 1 where {0}".format(param)
            param = "dam.id=%s"
            sql = "SELECT damgp.id, damg.id as module_group_id,  damg.name,dam.id as module_id, damgp.value  as privilege,damg.owner_id   FROM devops_workshop_dev_web.devops_auth_module_group_permission damgp join devops_auth_module_group damg on damg.id= damgp.group_id join devops_auth_module_groups damgs on damgs.group_id=damgp.group_id join devops_auth_module dam on dam.id = damgs.module_id and damgp.is_enabled=1 and damgs.is_enabled = 1 and dam.is_enabled = 1 and damg.is_enabled = 1 where {0}".format(param)
            print(sql)
            cursor = connection.cursor()
            cursor.execute(sql, id)
            data = dictFetchAll(cursor)
            cursor.close()
            connection.close()
            result['info'] = (data)
            # m = Module_group_permission.objects.get(id=id)
            # serializer = ModuleGroupPermissionSerializer(m)

            # result['info'] = serializer.data
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

    # TODO
    def post(self, request):
        result = {}
        hu = HttpUtils(self.request)
        input_dict = hu.getRequestParam()

        if input_dict is not None:
            try:
                if "id" in input_dict.keys():
                    id = request.data["id"]
                    m = Module_group_permission.objects.get(id=id)
                    m.group_id = input_dict.get('group_id', m.group_id)
                    m.value = input_dict.get('value', m.value)
                    if 'is_enabled' in input_dict.keys():
                        m.is_enabled = input_dict.get('is_enabled')
                    m.updated_by = request.user.username
                    m.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                else:
                    group_id = input_dict.get('group_id', '')
                    value = input_dict.get('value', '')

                    error = ''
                    if not group_id:
                        error = 'GroupId不能为空'
                    elif not value:
                        error = 'Value不能为空'
                    if error:
                        return HttpResponseBadRequest(error)

                    m = Module_group_permission(group_id=group_id,value=value,created_by=request.user.username,updated_by=request.user.username)
                    m.save()
                    if "module_id" in input_dict.keys():
                        module_id = input_dict.get('module_id')
                        try:
                            mm = Module_groups.objects.get(group_id=group_id,module_id=module_id)
                        except Module_groups.DoesNotExist:
                            mm = Module_groups(module_id=module_id,group_id=group_id)
                            mm.save()
                    result['status'] = 0
                    result['msg'] = "保存成功"
                    result['id'] = m.id
                    result['info'] = ModuleGroupPermissionSerializer(m).data
            except Exception as e:
                logger.error(e)
                result['status'] = 1
                result['msg'] = "保存失败"
                return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')

class ModuleListView(LoginRequiredMixin, APIView):
    serializer_class = ModuleSerializer

    #TODO, 所有有效模块（非disabled的，支持按请求字段排序,(正序，倒序))
    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        try:
            orderby = 'id'
            if 'order_by' in reqData:
                orderby = reqData["order_by"]
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

            module = Module.objects.filter(is_enabled=1).values('id', 'name', 'alias', 'url', 'open_db', 'open_table', 'open_id', 'owner_id').order_by(orderby)[offset:limit]
            # serializer = ModuleSerializer(module)
            print(module)
            result['status'] = 0
            result['info'] = list(module)
            # result['info'] = serializers.serialize('json', module)
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])

        return HttpResponse(json.dumps(result),content_type='application/json')

    #TODO, 根据用户查找所属模块（非disabled的）
    def get_by_user(self, uid):
        print('get_by_user')
        pass

    #TODO, 根据用户组查找所属模块（非disabled的）
    def get_by_user_group(self, gid):
        pass

    #TODO, 根据模块组查找所属模块（非disabled的）
    def get_by_module_group(self, gid):
        pass

class ModuleGroupListView(LoginRequiredMixin, APIView):
    #TODO, 所有有效模块组（非disabled的，支持按请求字段排序,(正序，倒序))
    def get(self, request):
        pass

class UserListView(LoginRequiredMixin, APIView):
    #TODO, 所有有效用户列表（非disabled的，支持按请求字段排序,(正序，倒序))
    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        try:
            limit = reqData["limit"]
            offset = reqData["offset"]
            if offset < 0:
                offset = 0
            # order_by = reqData["order_by"]
            order_by = request.GET.get('order_by', 'id')# reqData["order_by"]

            user_list = User.objects.all().order_by(order_by)[offset:offset+limit]
            info = []
            if len(user_list) > 0:
                for u in user_list:
                    info.append({'id':u.id, 'username':u.username, 'first_name':u.first_name, 'last_name':u.last_name, 'email':u.email, 'is_superuser':u.is_superuser})
            result['status'] = 0
            result['info'] = info
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])

        return HttpResponse(json.dumps(result),content_type='application/json')

    def get_by_module(self, mid):
        pass

class UserGroupListView(LoginRequiredMixin, APIView):
    #TODO, 所有有效用户组（支非disabled的，持按请求字段排序,(正序，倒序))
    def get(self, request):
        result = {}
        hu = HttpUtils(self.request)
        reqData = hu.getRequestParam()
        try:
            limit = reqData["limit"]
            offset = reqData["offset"]
            if offset < 0:
                offset = 0
            # order_by = reqData["order_by"]
            order_by = request.GET.get('order_by', 'id')# reqData["order_by"]
            group_list = Group.objects.all().order_by(order_by)[offset:offset+limit]
            info = []
            if len(group_list) > 0:
                for u in group_list:
                    info.append({'id':u.id, 'name':u.name})
            result['status'] = 0
            result['info'] = info
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "不存在"
            return HttpResponseBadRequest(result['msg'])
        return HttpResponse(json.dumps(result),content_type='application/json')
        # pass

    def get_by_module(self, mid):
        pass
