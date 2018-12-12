from django.conf.urls import include, url
from devops_cmdb.views.host_1 import *
from devops_cmdb.views.host_2 import *
from devops_cmdb.views.host_3 import *
from devops_cmdb.views.business_attributes import *
from devops_cmdb.views.host_group import *
from devops_cmdb.views.vip import *
from devops_cmdb.views.host_dashboard import *
from devops_cmdb.views import cell_con # add by robin

app_name = 'cmdb'

urlpatterns = [
    url(r'^host/', include([
        url(r'^list1/$', List1View.as_view(), name='list1'),
        url(r'^list2/$', List2View.as_view(), name='list2'),
        url(r'^list3/$', List3View.as_view(), name='list3'),
        url(r'^templateDownload/$', TemplateDownload, name='templateDownload'),
        url(r'^import/$', Host1Import.as_view(), name='import'),
        url(r'^export1/$', Host1ExportView, name='export1'),
        url(r'^(?P<pk>\d+)/detail1/', Host1DetailView.as_view(), name='detail1'),
        url(r'^(?P<pk>\d+)/detail2/', Host2DetailView.as_view(), name='detail2'),
        url(r'^(?P<pk>\d+)/detail3/', Host3DetailView.as_view(), name='detail3'),
        url(r'host1ToNotOnline/', Host1ToNotOnlineView.as_view(), name='host1ToNotOnline'),
        url(r'host1BindingGroup/', Host1BindingGroup.as_view(), name='host1BindingGroup'),
        url(r'host1UnbundlingGroup/', Host1UnbundlingGroup.as_view(), name='host1UnbundlingGroup'),
        url(r'host2BindingGroup/', Host2BindingGroup.as_view(), name='host2BindingGroup'),
        url(r'host2UnbundlingGroup/', Host2UnbundlingGroup.as_view(), name='host2UnbundlingGroup'),
        url(r'host2UpdateStatus/', Host2UpdateGoLiveView.as_view(), name='host2UpdateStatus'),
        url(r'host3UpdateStatus/', Host3UpdateGoLiveView.as_view(), name='host3UpdateStatus'),
        url(r'^deleteHost1/$', Host1DeleteView.as_view(), name='deleteHost1'),
        url(r'^scanHost1/$', Host1ScanView.as_view(), name='scanHost1'),
        url(r'^getImportInfo/$', GetImportStatus.as_view(), name='getImportInfo'),
        url(r'^dashboard/$', HostDashboardView.as_view(), name='dashboard'),
        url(r'^multiconditionquerypage/$', MultiConditionQueryPageView.as_view(), name='multiconditionquerypage'),
        url(r'multiconditionquery/', MultiConditionQueryView.as_view(), name='multiconditionquery'),
        url(r'^host_export/$', HostExportView, name='host_export'),
        url(r'^operationlog_list/$', HostOpertionLogListView.as_view(), name='operationlog_list'),
    ])),
    url(r'^business/', include([
        url(r'^business_list/', business_list, name='business_list'),#add by robin
        url(r'^rest/business/', rest_business, name='rest_business'),#add by robin
        url(r'^(?P<pk>\d+)/attributes_manage/', Attributes_Manage_View.as_view(), name='attributes_manage'),#add by robin
        url(r'^rest/attr/', rest_business_attr, name='rest_attr'),#add by robin
        url(r'^rest/attrHistory/', rest_business_attr_history, name='rest_attr'),#add by robin
        url(r'^rest/interface/', rest_business_int, name='rest_int'),#add by robin
        url(r'^rest/interfaceHistory/', rest_business_int_history, name='rest_int'),#add by robin
        url(r'^rest/cmt/', rest_business_cmt, name='rest_cmt'),#add by robin
        url(r'^attributes_view/', BusinesAttributessView.as_view(), name='attributes_view'),
        url(r'^attributes_create_view/', BusinesAttributessCreateAjaxView.as_view(), name='attributes_create_view'),
        url(r'^attributes_update_view/', BusinesAttributessUpdateAjaxView.as_view(), name='attributes_update_view'),
        url(r'^attributes_del_view/', BusinesAttributessDelAjaxView.as_view(),name='attributes_del_view'),
        url(r'^get_groups_by_brandId/', GetGroupsByBrandId.as_view(), name='get_groups_by_brandId'),
        url(r'^get_module_by_bIdgId/', GetModulesByBIdGId.as_view(), name='get_module_by_bIdgId'),
        url(r'^get_service_by_bIdgIdMid/', GetServiceByBIdGIdMid.as_view(), name='get_service_by_bIdgIdMid'),
    ])),
    url(r'^host_group/', include([
        url(r'^tree_list/', HostGroupView.as_view(), name='tree_list'),
        url(r'^host_tree_list/', HostGroupListView.as_view(), name='host_tree_list'),
        url(r'^host_group_manage/',HostGroupImport.as_view(), name='host_group_manage'),
        url(r'^hostgrouptemplatedownload/',HostGroupTemplateDownload, name='hostgrouptemplatedownload'),
        url(r'^getHostGroupImportInfo/$', GetHostGroupImportStatus.as_view(), name='getHostGroupImportInfo'),
        url(r'^hostgrouprenamenode/$', HostGroupRenameNode.as_view(), name='hostgrouprenamenode'),
        url(r'^hostgroupdeletenode/$', HostGroupDeleteNode.as_view(), name='hostgroupdeletenode'),
    ])),
    url(r'^vip/', include([
        url(r'^list/', VIPListView.as_view(), name='list'),
        url(r'^add/', VIPCreateView.as_view(), name='add'),
        url(r'^edit/', VIPUpdateView.as_view(), name='edit'),
        url(r'^bindIp/', VIPBindIPView.as_view(), name='bindIp'),
        url(r'^delete/', VIPDeleteView.as_view(), name='delete'),
    ])),
    #add by robin
    url(r'^cell/template/index/$', cell_con.template_index, name='template_index'),
    url(r'^cell/template/$', cell_con.cell_template, name='template'),
    url(r'^cell/template/log/$', cell_con.template_log, name='template_log'),
    url(r'^cell/index/$', cell_con.cell_index, name='cell_import'),
    url(r'^cell/post/', cell_con.cell_post, name='cell_post'),
    url(r'^cell/runCell/', cell_con.run_cell, name='run_cell'),
]
