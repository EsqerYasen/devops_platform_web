from django.conf.urls import include, url
from devops_deploy.views.deploy import *

urlpatterns = [
    url(r'^list/',ListView.as_view(), name='list'),
    url(r'^add/',CreateView.as_view(), name='add')
]