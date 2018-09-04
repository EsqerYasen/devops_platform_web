from django.conf.urls import *
from . import views,site_views

app_name = 'slb'

urlpatterns = [
    ##page
    # /slb/
    url(r'^index/', views.index, name='index'),
    url(r'^site/', views.site, name='site'),
    url(r'^site_list/', views.site_list, name='site_list'),
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
    url(r'^rest/delsite/', views.del_site, name='rest_del_site'),
    url(r'^rest/deployversionbysiteid/', views.site_versions, name='rest_site_verisons'),
    url(r'^rest/deployversioncreateview/', views.create_site_version, name='rest_create_site_verison'),
    url(r'^rest/getmappingruleslist/', views.mappingRuleList, name='rest_mappingrule'),
    url(r'^rest/getcmdlist/', views.cmdList, name='rest_mappingrule_info'),

    url(r'^rest/configpreview/', site_views.ConfigPreviewView.as_view(), name='configpreviewview'),
    url(r'^rest/nginxclusterhostbyid/', site_views.NginxClusterHostById.as_view(), name='nginxclusterhostbyid'),
    url(r'^rest/configversiondiff/', site_views.ConfigVersionDiff.as_view(), name='configpreviewview'),

    url(r'^rest/mappingrulescreateorupdate/', views.MappingRulesCreateOrUpdate, name='mappingrulescreateorupdate'),
    url(r'^rest/mngsitecreateorupdate/', views.MngSiteCreateOrUpdate, name='mngsitecreate'),
    url(r'^rest/nginxclustertree/', views.NginxClusterTree, name='nginxclustertree'),
    url(r'^rest/gethostlistbygrupid/', views.GetHostListByGrupId, name='gethostlistbygrupid'),
]
