from django.conf.urls import include, url
from devops_cmdb.views import host_1,host_2,host_3,business_brand

urlpatterns = [
    url(r'^host/', include([
        url(r'^list1/$', host_1.ListView.as_view(), name='list1'),
        url(r'^list2/$', host_2.ListView.as_view(), name='list2'),
        url(r'^list3/$', host_3.ListView.as_view(), name='list3'),
    ])),
    url(r'^business/', include([
        url(r'^attributes_view/', business_brand.BusinesAttributessView.as_view(), name='attributes_view'),
    ])),
]