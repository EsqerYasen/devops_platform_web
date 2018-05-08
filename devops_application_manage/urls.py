from django.conf.urls import include, url
from devops_application_manage.views.app_deploy import *

urlpatterns = [
    url(r'^manage/', include([
        url(r'^list/', DevopsAppMgeListView.as_view(), name='list'),
        url(r'^add/', DevopsAppMgeCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsAppMgeUpdateView.as_view(), name='edit'),
        url(r'^(?P<pk>\d+)/deploy/', DevopsAppMgeDeployView.as_view(), name='deploy'),
        url(r'^get_command_set_info', GetCommandSetInfoView.as_view(), name='get_command_set_info'),
    ]))
]