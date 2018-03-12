from django.conf.urls import include, url

from common_platform.views.command_set import *

urlpatterns = [
    url(r'^command_set/', include([
        url(r'^list/', CommandSetListView.as_view(), name='list'),
    ])),
]

