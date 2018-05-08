from django.conf.urls import include, url
from devops_application_manage.views.app_deploy import *

urlpatterns = [
    url(r'^manage/', include([
        url(r'^list/', DevopsAppMgeListView.as_view(), name='list'),
        url(r'^add/', DevopsAppMgeCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/edit/', DevopsAppMgeUpdateView.as_view(), name='edit'),
    ]))
]