from django.urls import path
from . import views

app_name = 'slb'

urlpatterns = [
    ##page
    # /slb/
    path('', views.index, name='index'),
    path('site/', views.site, name='site'),
    path('upstream/', views.upstream, name='upstream'),
    path('deploy/deploy_task', views.deploy_task, name='deploy_task'),
    path('deploy/manage', views.deploy_manage, name='deploy_management'),


    ##rest
    #upstream
    path('rest/serviceclusterlist/', views.serviceClusterList, name='rest_clusters'),
    path('rest/serviceclusterbyid/', views.serviceClusterByID, name='rest_clusterbyid'),

    #site
    path('rest/getmngsitelist/', views.siteList, name='rest_sites'),
    path('rest/getmngsiteinfo/', views.siteInfo, name='rest_siteinfo'),
    path('rest/deployversionbysiteid/', views.site_versions, name='rest_site_verisons'),
    path('rest/deployversioncreateview/', views.create_site_version, name='rest_create_site_verison'),
    path('rest/getmappingruleslist/', views.mappingRuleList, name='rest_mappingrule'),
    path('rest/getcmdlist/', views.cmdList, name='rest_mappingrule_info'),


]
