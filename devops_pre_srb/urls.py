from django.conf.urls import include, url
from devops_pre_srb.views.pre_srb import *

urlpatterns = [
    url(r'^project/', include([
        url(r'^list/',PreSrbListView.as_view(), name='list'),
        url(r'^add/',PreSrbCreateView.as_view(), name='add'),
    ]))
]