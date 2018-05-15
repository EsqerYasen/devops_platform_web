from django.conf.urls import include, url
from devops_flow.views.flow_views import *

urlpatterns = [
    url(r'^manage/', include([
        url(r'^list/', DevopsFlowListView.as_view(), name='list'),
    ]))
]