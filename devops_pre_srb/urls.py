from django.conf.urls import include, url
from devops_pre_srb.views.pre_srb import *
from devops_pre_srb.views.upload_download import *
from devops_pre_srb.views.utils import *

app_name = 'presrb'

urlpatterns = [
    url(r'^project/', include([
        url(r'^list/',PreSrbListView.as_view(), name='list'),
        url(r'^add/',PreSrbCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/',PreSrbUpdateView.as_view(), name='edit'),
        url(r'^projectupdatestatus/$', ProjectUpdateStatusView.as_view(), name='projectupdatestatus'),
        url(r'^projectItem_add/$', ProjectItemCreateView.as_view(), name='projectItem_add'),
        url(r'^pro_report_views/$', ProjectReportView.as_view(), name='pro_report_views'),
        url(r'^project_item_list/$', ProjectItemListView.as_view(), name='project_item_list'),

        url(r'^upload/$',UploadFile.as_view(),name='upload'),
        url(r'^download/$',DownloadFile.as_view(),name='download'),
        url(r'^delete_file/$',DeleteFile.as_view(),name='delete_file'),
        url(r'^filelist/$',GetFileList.as_view(),name='filelist'),
		url(r'^generate_ppt/$', ProjectPptReportView.as_view(), name='generate_ppt'),

    ]))
]
