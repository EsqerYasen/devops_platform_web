from django.conf.urls import include, url

from common_platform.views.command_set import *
from common_platform.views.file_manage import *

urlpatterns = [
    url(r'^command_set/', include([
        url(r'^list/', CommandSetListView.as_view(), name='list'),
    ])),
    url(r'^file_manage/', include([
        url(r'^view/', FileManageView.as_view(), name='view'),
        url(r'^get_fileTree_ajax/', FileTreeView.as_view(), name='get_fileTree_ajax'),
        url(r'^create_folder/', FileTreeCreateFolder.as_view(), name='create_folder'),
        url(r'^uploadFile/', FileTreeUploadFile.as_view(), name='uploadFile'),
    ])),
]

