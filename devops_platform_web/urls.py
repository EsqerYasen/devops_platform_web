"""devops_platform_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler400,handler500,handler403
from django.contrib import admin
from django.conf.urls import url, include
from django.views import static
from django.conf import settings

from common import views
from common.views import LoginView
from common.views import hostTotalCount

handler400 = "common.views.page_not_found"
handler500 = "common.views.page_error"
handler403 = "common.views.page_forbidden"

urlpatterns = [
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', LoginView.as_view(), name='index'),
    url(r'^checkLogin/$', views.checkLogin, name='checkLogin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^mainform/$', views.mainform, name='mainform'),
    url(r'^dashboard/$', views.dashboard, name='mainform'),
    url(r'^cmdb/', include('devops_cmdb.urls', namespace='cmdb')),
    url(r'^platform/', include('common_platform.urls', namespace='platform')),
    url(r'^deploy/', include('devops_deploy.urls', namespace='deploy')),
    url(r'^jira/', include('devops_jira.urls', namespace='jira')),
    url(r'^working/',include('devops_tools.urls',namespace='working')),
    url(r'^presrb/',include('devops_pre_srb.urls',namespace='presrb')),
    url(r'^application/',include('devops_application_manage.urls',namespace='application')),
    url(r'^flow/',include('devops_flow.urls',namespace='flow')),
    url(r'^host_total_count/', hostTotalCount, name='host_total_count'),
    url(r'^auth/',include('devops_auth.urls',namespace='auth')),
    url(r'^forward_to_service/',views.forward_to_service,name='forward_to_service'),
    url(r'^menu/',include('devops_menu.urls',namespace='menu')),
    url(r'^slb/',include('slb.urls',namespace='slb')),
]
