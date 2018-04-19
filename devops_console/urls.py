from django.conf.urls import include, url
from devops_console.views.issues import *

urlpatterns = [
    url(r'^issues/', include([
        url(r'^list/$', IssuesListView.as_view(), name='list'),
        url(r'^listDone/$', IssuesDoneListView.as_view(), name='listDone'),
    ])),
]