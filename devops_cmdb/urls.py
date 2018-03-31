from django.conf.urls import include, url
from devops_cmdb.views.host_1 import *
from devops_cmdb.views.host_2 import *
from devops_cmdb.views.host_3 import *
from devops_cmdb.views.business_attributes import *
from devops_cmdb.views.host_group import *

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
    ])),
    url(r'^business/', include([
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
    ]))
]