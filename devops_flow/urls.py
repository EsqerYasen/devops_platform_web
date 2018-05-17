from django.conf.urls import include, url
from devops_flow.views.flow_views import *

urlpatterns = [
    url(r'^control/', include([
        url(r'^list/', DevopsFlowListView.as_view(), name='list'),
        url(r'^add/', DevopsFlowCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsFlowUpdateView.as_view(), name='edit'),
        url(r'^(?P<pk>\d+)/operation/', DevopsFlowOperationView.as_view(), name='operation'),
        # url(r'^report/', DevopsFlowReportView.as_view(), name='report'),
        # url(r'^report2/', DevopsFlowReportView2, name='report2'),
    ]))
]