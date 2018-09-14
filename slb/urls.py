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
    url(r'^upstream_list/', views.upstream_list, name='upstream_list'),
    url(r'^deploy/deploy_task/', views.deploy_task, name='deploy_task'),
    url(r'^deploy/manage/', views.deploy_manage, name='deploy_management'),


    ##rest
    #site
    url(r'^rest/getmngsitelist/', views.siteList, name='rest_sites'),
    url(r'^rest/getmngsiteinfo/', views.siteInfo, name='rest_siteinfo'),
    url(r'^rest/deployversionbysiteid/', views.site_versions, name='rest_site_verisons'),
    url(r'^rest/delsite/', views.del_site, name='rest_del_site'),
    url(r'^rest/deployversioncreateview/', views.create_site_version, name='rest_create_site_verison'),
    url(r'^rest/mngsitecreateorupdate/', views.MngSiteCreateOrUpdate, name='mngsitecreate'),
    #preview
    url(r'^rest/configpreview/', views.config_preview, name='configpreviewview'),
    url(r'^rest/configversiondiff/', views.config_version_diff, name='configpreviewview'),
    #mappingrule
    url(r'^rest/getmappingruleslist/', views.mappingRuleList, name='rest_mappingrule'),
    url(r'^rest/getcmdlist/', views.cmdList, name='rest_mappingrule_info'),
    url(r'^rest/mappingrulescreateorupdate/', views.MappingRulesCreateOrUpdate, name='mappingrulescreateorupdate'),
    url(r'^rest/deletemappingrule/', views.del_mappingrule, name='mappingrulescreateorupdate'),

    #upstream
    url(r'^rest/serviceclusterlist/', views.serviceClusterList, name='rest_clusters'),
    url(r'^rest/serviceclusterbyid/', views.serviceClusterByID, name='rest_clusterbyid'),
    url(r'^rest/serviceclusterdel/', views.del_servicecluster, name='rest_del_cluster'),

    url(r'^rest/nginxclusterhostbyid/', views.NginxClusterHostById, name='nginxclusterhostbyid'),
    url(r'^rest/configversiondiff/', site_views.ConfigVersionDiff.as_view(), name='configpreviewview'),

    url(r'^rest/nginxclustertree/', views.NginxClusterTree, name='nginxclustertree'),
    url(r'^rest/gethostlistbygrupid/', views.GetHostListByGrupId, name='gethostlistbygrupid'),


    #deploy
    url(r'^rest/deployagent', views.deploy_agent, name='deploy_agent'),
    url(r'^rest/nginxdeploylogsbyip/', views.get_nginx_log, name='gethostlistbygrupid'),
    url(r'^rest/deploytaskslist/', views.get_deploytaskslist, name='gethostlistbygrupid'),
    #ws
    url(r'^ws/rtlog', views.rtlog, name='realtime_log'),
]
