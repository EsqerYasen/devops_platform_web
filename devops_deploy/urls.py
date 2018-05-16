from django.conf.urls import include, url
from devops_deploy.views.deploy import *
from devops_deploy.views.operation_log import *
from devops_deploy.views.deploy_tool_views import *

urlpatterns = [
    url(r'^list/',DeployListView.as_view(), name='list'),
    url(r'^add/',DeployCreateView.as_view(), name='add'),
    url(r'^import/',DeployCreateImport.as_view(), name='import'),
    url(r'^update/',DeployUpdateView.as_view(),name='update'),
    url(r'^getAppListByPid/',GetAppListByPidView.as_view(), name='getAppListByPid'),
    url(r'^deployExec/',DeployExecView.as_view(), name='deployExec'),
    # url(r'^deployRollback/',DeployRollbackView.as_view(), name='deployRollback'),
    url(r'^executeLog/',ExecuteLogView.as_view(), name='executeLog'),
    url(r'^operationLog/',OperationLogView.as_view(), name='operationLog'),
    url(r'^deleteApp/',DeleteAppView.as_view(), name='deleteApp'),
    url(r'^deployVersion/',DeployVersionView.as_view(), name='deployVersion'),
    url(r'^deployPre/',DeployPreExecView.as_view(), name='deployPre'),
    url(r'^tool/', include([
        url(r'^list/', DeployToolListView.as_view(), name='list'),
        url(r'^add/', DeployToolCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DeployToolUpdateView.as_view(), name='edit'),
        url(r'^(?P<pk>\d+)/operation/', DeployToolOperationView.as_view(), name='operation'),
    ]))
]