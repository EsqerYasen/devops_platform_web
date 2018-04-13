from django.conf.urls import include, url
from devops_deploy.views.deploy import *
from devops_deploy.views.operation_log import *

urlpatterns = [
    url(r'^list/',DeployListView.as_view(), name='list'),
    url(r'^add/',DeployCreateView.as_view(), name='add'),
    url(r'^getAppListByPid/',GetAppListByPidView.as_view(), name='getAppListByPid'),
    url(r'^deployExec/',DeployExecView.as_view(), name='deployExec'),
    url(r'^deployRollback/',DeployRollbackView.as_view(), name='deployRollback'),
    url(r'^executeLog/',ExecuteLogView.as_view(), name='executeLog'),
    url(r'^operationLog/',OperationLogView.as_view(), name='operationLog')
]