from django.conf.urls import include, url
from rest_framework import routers
from devops_auth.views.app_views import *
from devops_auth.views import rest_views

app_name = 'auth'

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^manager/', include([
        url(r'^list/$', AuthListView.as_view(), name='list')
    ])),
    url(r'^rest/', include([
        url(r'^verify/$', rest_views.AuthVerifyView.as_view()),
        url(r'^module/$', rest_views.ModuleView.as_view()),
        url(r'^module/list/$', rest_views.ModuleListView.as_view()),
        #url(r'^users/list/$', rest_views.UsersView.as_view()),
        url(r'^user_modules/$', rest_views.userModulesView.as_view()),
        url(r'^module_group/$', rest_views.ModuleGroupView.as_view()),
        url(r'^module_group/list/$', rest_views.ModuleGroupView.as_view()),
        url(r'^module_groups/$', rest_views.ModuleGroupsView.as_view()),
        url(r'^module_group/users/$', rest_views.ModuleGroupsUsersView.as_view()),
        url(r'^permission/module/$', rest_views.ModulePermissionView.as_view()),
        url(r'^permission/user_group/$', rest_views.UserGroupPermissionView.as_view()),
        url(r'^permission/module_group/$', rest_views.ModuleGroupPermissionView.as_view()),
        url(r'^user/list/$', rest_views.UserListView.as_view()),
        url(r'^user_group/list/$', rest_views.UserGroupListView.as_view()),
        url(r'^modules_permission/$', rest_views.ModulesPermissionView.as_view()),
        url(r'^menuItems/$', rest_views.MenuItemsView.as_view()),
    ]))
]
