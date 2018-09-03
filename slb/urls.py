from django.conf.urls import *
from . import views,site_views

app_name = 'slb'

urlpatterns = [
    ##page
    # /slb/
    url(r'^index/', views.index, name='index'),
    url(r'^site/', views.site, name='site'),
    url(r'^upstream/', views.upstream, name='upstream'),
    url(r'^deploy/deploy_task', views.deploy_task, name='deploy_task'),
    url(r'^deploy/manage', views.deploy_manage, name='deploy_management'),


    ##rest
    #upstream
    url(r'^rest/serviceclusterlist/', views.serviceClusterList, name='rest_clusters'),
    url(r'^rest/serviceclusterbyid/', views.serviceClusterByID, name='rest_clusterbyid'),

    #site
    url(r'^rest/getmngsitelist/', views.siteList, name='rest_sites'),
    url(r'^rest/getmngsiteinfo/', views.siteInfo, name='rest_siteinfo'),
    url(r'^rest/deployversionbysiteid/', views.site_versions, name='rest_site_verisons'),
    url(r'^rest/deployversioncreateview/', views.create_site_version, name='rest_create_site_verison'),
    url(r'^rest/getmappingruleslist/', views.mappingRuleList, name='rest_mappingrule'),
    url(r'^rest/getcmdlist/', views.cmdList, name='rest_mappingrule_info'),

    url(r'^site/configpreview/', site_views.ConfigPreviewView.as_view(), name='configpreviewview'),
    url(r'^site/nginxclusterhostbyid/', site_views.NginxClusterHostById.as_view(), name='nginxclusterhostbyid'),
    url(r'^site/configversiondiff/', site_views.ConfigVersionDiff.as_view(), name='configpreviewview'),
    url(r'^test/configversiondiffview/', site_views.ConfigVersionDiffView.as_view(), name='configversiondiffview'),
]
