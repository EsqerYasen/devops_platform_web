from django.conf.urls import include, url
from rest_framework import routers
from devops_menu.views.app_views import *
from devops_menu.views import rest_views

router = routers.DefaultRouter()

urlpatterns = [
  url(r'^list/$', MenuListView.as_view(), name='list'),
  url(r'^rest/', include([
        url(r'^menuItems/$', rest_views.MenuItemsView.as_view()),
        url(r'^menu/$', rest_views.MenuView.as_view()),
    ]))
]
