from django.conf.urls import include, url
from devops_jira.views.jira_view import *

app_name = 'jira'

urlpatterns = [
    url(r'^issues/', include([
        url(r'^list/$', IssuesListView.as_view(), name='list'),
        url(r'^listDone/$', IssuesListView.as_view(), name='listDone'),
        url(r'^detail/$', IssuesDetailView.as_view(), name='detail'),
    ])),
]
