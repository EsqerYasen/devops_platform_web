from django.conf.urls import include, url

from common_platform.views.command_set import *
from common_platform.views.command_set2 import *
from common_platform.views.file_manage import *
from common_platform.views.soft_load import *
from common_platform.views.ansible_manage import *


urlpatterns = [
    url(r'^command_set/', include([
        url(r'^list/', CommandSetListView.as_view(), name='list'),
        url(r'^add/', CommandSetCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', CommandSetUpdateView.as_view(), name='edit'),
        url(r'^delete/', CommandSetDeleteView.as_view(), name='delete'),
        # url(r'^listByIds/', HostListByIdslView.as_view(), name='listByIds'),
        url(r'^listByQueryCriteria/', HostListByQueryCriteria.as_view(), name='listByQueryCriteria'),
        url(r'^(?P<pk>\d+)/exec/', CommandSetExecuteView.as_view(), name='exec'),
        url(r'execLog/', CommandExecuteLogView.as_view(), name='execLog'),
        url(r'getExecLog/', GetCommandExecuteLogView.as_view(), name='getExecLog'),
        url(r'stop/', CommandExecuteStop.as_view(), name='stop'),
    ])),
    url(r'^command_set2/', include([
        url(r'^list/', CommandSetList2View.as_view(), name='list'),
        url(r'^add/', CommandSetCreate2View.as_view(), name='add'),
    ])),
    url(r'^file_manage/', include([
        url(r'^view/', FileManageView.as_view(), name='view'),
        url(r'^get_fileTree_ajax/', FileTreeView.as_view(), name='get_fileTree_ajax'),
        url(r'^create_folder/', FileTreeCreateFolder.as_view(), name='create_folder'),
        url(r'^uploadFile/', FileTreeUploadFile.as_view(), name='uploadFile'),
        url(r'^delete/', DeleteFile.as_view(), name='delete'),
    ])),
    # url(r'^soft_load/', include([
    #     url(r'^page/', SoftLoadView.as_view(), name='page'),
    # ])),
    url(r'^toolset/', include([
        url(r'^list/', ToolSetListView.as_view(), name='list'),
    ])),
    url(r'^ansible/', include([
        url(r'^mge/', AnsibleMgeView.as_view(), name='mge'),
    ])),
]

