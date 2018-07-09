from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.apps import apps
#from devops_menu.models import Module, Module_group, Module_group_permission, Module_groups, Module_permission, User_group_permission
from devops_menu.models.Devops_Menu import MenuItem

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        # fields = '__all__'
        fields=("id", "name", "menu", "parent_id", "has_sub_menu")
