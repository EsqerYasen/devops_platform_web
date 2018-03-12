from django.conf.urls import include, url
from devops_cmdb.views import host_1,host_2,host_3,business_attributes

urlpatterns = [
    url(r'^host/', include([
        url(r'^list1/$', host_1.ListView.as_view(), name='list1'),
        url(r'^list2/$', host_2.ListView.as_view(), name='list2'),
        url(r'^list3/$', host_3.ListView.as_view(), name='list3'),
    ])),
    url(r'^business/', include([
        url(r'^attributes_view/', business_attributes.BusinesAttributessView.as_view(), name='attributes_view'),
        url(r'^attributes_create_view/', business_attributes.BusinesAttributessCreateAjaxView.as_view(), name='attributes_create_view'),
        url(r'^attributes_update_view/', business_attributes.BusinesAttributessUpdateAjaxView.as_view(), name='attributes_update_view'),
        url(r'^attributes_del_view/', business_attributes.BusinesAttributessDelAjaxView.as_view(),name='attributes_del_view'),
        url(r'^get_groups_by_brandId/', business_attributes.GetGroupsByBrandId.as_view(), name='get_groups_by_brandId'),
    ])),
]