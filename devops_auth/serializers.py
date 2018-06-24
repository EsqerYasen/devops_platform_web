from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.apps import apps
#from devops_auth.models import Module, Module_group, Module_group_permission, Module_groups, Module_permission, User_group_permission
from devops_auth.models.Module import Module
from devops_auth.models.Module_group import Module_group
from devops_auth.models.Module_groups import Module_groups
from devops_auth.models.Module_permission import Module_permission
from devops_auth.models.Module_group_permission import Module_group_permission
from devops_auth.models.User_group_permission import User_group_permission

class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'alias', 'url', 'owner_id')

class ModuleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module_group
        fields = ('id', 'name', 'owner_id')

class ModuleGroupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module_groups
        fields = ('group_id', 'module_id')

class ModuleGroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module_group_permission
        fields = ('group_id', 'value')

class ModulePermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module_permission
        fields = ('user_id', 'module_id', 'value')

class UserGroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_group_permission
        fields = ('group_id', 'module_id', 'value')