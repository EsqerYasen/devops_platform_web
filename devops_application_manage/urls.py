from django.conf.urls import include, url
from devops_application_manage.views.app_deploy import *
from devops_application_manage.views.file_monitored import *

app_name = 'application'

urlpatterns = [
    url(r'^manage/', include([
        url(r'^list/', DevopsAppMgeListView.as_view(), name='list'),
        url(r'^add/', DevopsAppMgeCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsAppMgeUpdateView.as_view(), name='edit'),
        url(r'^delete/', DevopsAppMgeDeleteView.as_view(), name='delete'),
        url(r'^(?P<pk>\d+)/deploy/', DevopsAppMgeDeployView.as_view(), name='deploy'),
        url(r'^get_command_set_info', GetCommandSetInfoView.as_view(), name='get_command_set_info'),
        url(r'^filemonitoredlist', FileMonitoredView.as_view(), name='filemonitoredlist'),
        url(r'^filemonitoredconfiglist', FileMonitoredConfigListView.as_view(), name='filemonitoredconfiglist'),
        url(r'^filemonitoredconfigadd', FileMonitoredConfigCreateView.as_view(), name='filemonitoredconfigadd'),
    ]))
]
