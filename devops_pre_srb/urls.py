from django.conf.urls import include, url
from devops_pre_srb.views.pre_srb import *

urlpatterns = [
    url(r'^project/', include([
        url(r'^list/',PreSrbListView.as_view(), name='list'),
        url(r'^add/',PreSrbCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/',PreSrbUpdateView.as_view(), name='edit'),
        url(r'^projectItem_add/$', ProjectItemCreateView.as_view(), name='projectItem_add'),
        url(r'^pro_report_views/$', ProjectReportView.as_view(), name='pro_report_views'),
    ]))
]