from django.conf.urls import include, url
from devops_tools.views.devops_tools import *

app_name = 'working'

urlpatterns = [
    url(r'^tools/', include([
        url(r'^list/', DevopsToolsListView.as_view(), name='list'),
        url(r'^add/', DevopsToolsCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsToolsUpdateView.as_view(), name='edit'),
        url(r'^delete/', DevopsToolsDeleteView.as_view(), name='delete'),
        url(r'^yamlCheck/', DevopsToolsYamlCheckView.as_view(), name='yamlCheck'),
        url(r'^getversionbyname/', DevopsToolVersionByName.as_view(), name='getversionbyname'),
        url(r'^(?P<pk>\d+)/gethistoryversionbytoolId/', DevopsToolHistoryVersionByToolId.as_view(), name='gethistoryversionbytoolId'),
        url(r'^infobytoolidandversion/', DevopsToolInfoByToolIdAndVersion.as_view(), name='infobytoolidandversion'),

    ]))
]
