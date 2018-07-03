import json
from common.utils.redis_utils import *
from devops_auth.models.Module import Module
from devops_auth.models.Module_group import Module_group
from devops_auth.models.Module_groups import Module_groups
from devops_auth.models.Module_groups_users import Module_groups_users
from devops_auth.models.Module_permission import Module_permission
from devops_auth.models.Module_group_permission import Module_group_permission
from devops_auth.models.User_group_permission import User_group_permission
from django.db import connection
from rest_framework import serializers

import logging,os,xlrd,threading,re
logger = logging.getLogger('devops_platform_log')

class auth_utils():
    def verify(reqData, user):
        result = {}
        result['status'] = 1
        result['msg'] = "没有操作权限"

        id = reqData["id"]
        action = reqData["action"]

        try:
            user_id = user.id
            groups = user.groups.values('id')
            user_group_ids = []
            for gid in groups:
                user_group_ids.append(gid['id'])

            action_value = auth_utils.get_action_value(action)
            if action_value > 0:
                permissions = {}
                key = "user_permissions_%s" % (user_id)
                cache_value = RedisBase.get(key)
                if cache_value:
                    permissions = json.loads(cache_value)
                    logger.info('get from redis: %s' % permissions)

                if not permissions:
                    permissions = auth_utils.get_user_permission({'user_id':user_id, 'user_group_ids': user_group_ids})
                    if permissions:
                        RedisBase.set(key, json.dumps(permissions), 60*60*8)
                        logger.info('set to redis: size=%s' % len(permissions))

                if id in permissions.keys():
                    if action_value <= permissions.get(str(id)):
                        result['status'] = 0
                        result['msg'] = "权限效验成功"
        except Exception as e:
            logger.error(e)
            result['status'] = 1
            result['msg'] = "权限效验失败"

        result['id'] = id
        result['uid'] = user_id

        return result

    # 查询操作权限值
    def get_action_value(action):
        """
        操作权限, 最大值4：
        执行操作 x - 1
        读操作 r - 2
        写操作 w - 4

        :param action:
        :return:
        """
        value = 0
        permission_list = {'x':1, 'r':2, 'w':4}

        if action is not None:
            for a in permission_list.keys():
                if a in action:
                    if permission_list.get(a) > value:
                        value = permission_list.get(a)

        return value

    # 查询用户权限列表
    def get_user_permission(input_dict):
        """
        查询用户拥有模块和模块组权限
        查询用户管理的模块权限
        查询用户组权限
        查询用户管理的模块组权限

        合并权限，权限值取最大

        :param input_dict:
        :return:
        """

        permissions = {}
        output = {}
        results = set()
        modules = Module.objects.filter(is_enabled=1)
        moduleListMapping = {}
        moduleList = {}
        for m in modules:
            moduleList[m.id] = m

        # Owner 权限
        owner_list = Module.objects.filter(owner_id=input_dict['user_id'],is_enabled=1)
        for m in owner_list:
            permissions[str(m.id)] = 4 # 模块Owner 有全部权限

        # 模块组Owner权限
        m_groups = Module_group.objects.filter(owner_id=input_dict['user_id'],is_enabled=1).values('id')
        if m_groups:
            ids = []
            for m_g in m_groups:
                ids.append(m_g['id'])
            m_g_permissions = Module_group_permission.objects.filter(group_id__in=ids,is_enabled=1).values('group_id', 'value')
            for m in m_g_permissions:
                value = m['value']
                gid = m['group_id']
                m_modules = Module_groups.objects.filter(group_id=gid).values('module_id').values('module_id')
                for m_m in m_modules:
                    id = str(m_m['module_id'])
                    if id in permissions.keys():
                        if value > permissions[id]:
                            permissions[id] = value
                    else:
                        permissions[id] = value

        # 用户级别权限
        m_permissions = Module_permission.objects.filter(user_id=input_dict['user_id'],is_enabled=1).values('module_id', 'value')
        for m_p in m_permissions:
            id = str(m_p['module_id'])
            value = m_p['value']
            if id in permissions.keys():
                if value > permissions[id]:
                    permissions[id] = value
            else:
                permissions[id] = value

        # 用户组权限
        ug_permissions = User_group_permission.objects.filter(group_id__in=input_dict['user_group_ids'],is_enabled=1).values('module_id', 'value')
        for ug_p in ug_permissions:
            id = str(ug_p['module_id'])
            value = ug_p['value']
            if id in permissions.keys():
                if value > permissions[id]:
                    permissions[id] = value
            else:
                permissions[id] = value

        # 模块组用户权限
        mg_users = Module_groups_users.objects.filter(user_id=input_dict['user_id']).values('group_id')
        if mg_users:
            ids = []
            for m_g in mg_users:
                ids.append(m_g['group_id'])
            mg_permissions = Module_group_permission.objects.filter(group_id__in=ids,is_enabled=1).values('group_id', 'value')
            for mg_p in mg_permissions:
                value = mg_p['value']
                gid = mg_p['group_id']
                m_groups = Module_groups.objects.filter(group_id=gid).values('module_id')
                for m_g in m_groups:
                    id = str(m_g['module_id'])
                    if id in permissions.keys():
                        if value > permissions[id]:
                            permissions[id] = value
                    else:
                        permissions[id] = value
        for id in moduleList:
            if permissions.get(str(id)) is not None:
                m = moduleList[id]
                if m.open_db is not None and m.open_table is not None and m.open_id is not None:
                    output[id] = {
                        "dataset": m.open_db,
                        "collection": m.open_table,
                        "idx": m.open_id,
                        "value": permissions.get(str(id))
                    }
        return output
