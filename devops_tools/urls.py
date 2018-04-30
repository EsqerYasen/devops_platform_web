from django.conf.urls import include, url
from devops_tools.views.devops_tools import *

urlpatterns = [
    url(r'^tools/', include([
        url(r'^list/', DevopsToolsListView.as_view(), name='list'),
        url(r'^add/', DevopsToolsCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsToolsUpdateView.as_view(), name='edit'),
    ]))
]