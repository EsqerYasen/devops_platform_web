from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
import logging

logger = logging.getLogger('devops_platform_log')

class HostDashboardView(LoginRequiredMixin, OrderableListMixin,JSONResponseMixin,AjaxResponseMixin, ListView):
    template_name = "host_dashboard.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(HostDashboardView, self).get_context_data(**kwargs)
        return context

    def post_ajax(self, request, *args, **kwargs):
        resultList = []
        try:
            reqPost = self.request.POST
            flag = reqPost.get("flag", 0)
            if flag == '0':
                resultList = self.GetPhysicalIdcInfo();
            elif flag == '1':
                resultList = self.GetLogicalIdcInfo();
            elif flag == '2':
                resultList = self.GetNhBizGroupInfo();
            elif flag == '3':
                resultList = self.GetZrBizGroupInfo();
            elif flag == '4':
                resultList = self.GetKfcPreorderInfo();
            elif flag == '5':
                resultList = self.GetKfcDeliveryInfo();
            elif flag == '6':
                resultList = self.GetPhDeliveryInfo();

        except Exception as e:
            logger.error(e)
        return self.render_json_response(resultList)

    def GetPhysicalIdcInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultNh = hu.get(serivceName="cmdb", restName="/rest/host/", datas={'offset': 0, 'limit': 1,"physical_idc":'nh'})
        result.append({"name":"nh","value":resultNh.get("count",0)})
        resultZr = hu.get(serivceName="cmdb", restName="/rest/host/",datas={'offset': 0, 'limit': 1, "physical_idc": 'zr'})
        result.append({"name": "zr", "value": resultZr.get("count", 0)})
        return result

    def GetLogicalIdcInfo(self):
        result = {}
        hu = HttpUtils(self.request)
        idc = {}
        resultIdcNh = hu.get(serivceName="cmdb", restName="/rest/host/", datas={'offset': 0, 'limit': 1, "physical_idc": 'nh','logical_idc':'idc'})
        idc['nh'] = resultIdcNh.get("count", 0)
        resultIdcZr = hu.get(serivceName="cmdb", restName="/rest/host/",datas={'offset': 0, 'limit': 1, "physical_idc": 'zr', 'logical_idc': 'idc'})
        idc['zr'] = resultIdcZr.get("count", 0)
        result['IDC'] = idc

        dmz = {}
        resultDmzNh = hu.get(serivceName="cmdb", restName="/rest/host/", datas={'offset': 0, 'limit': 1, "physical_idc": 'nh', 'logical_idc': 'dmz'})
        dmz['nh'] = resultDmzNh.get("count", 0)
        resultDmzZr = hu.get(serivceName="cmdb", restName="/rest/host/",datas={'offset': 0, 'limit': 1, "physical_idc": 'zr', 'logical_idc': 'dmz'})
        dmz['zr'] = resultDmzZr.get("count", 0)
        result['DMZ'] = dmz
        return result

    def GetNhBizGroupInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_id_by_name/",datas={'name':'nh'})
        nhGroupIds = resultNh.get("data",[])
        for groupId in nhGroupIds:
            temp = {}
            resultNhPath = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_full_path/", datas={'id': groupId})
            nhName = resultNhPath.get("data","_").split('_')
            temp['name'] = nhName[0]+"-"+nhName[1]
            resultDmzNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            temp['value'] = len(resultDmzNh.get("data",[]))
            result.append(temp)
        return result

    def GetZrBizGroupInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultZr = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_id_by_name/", datas={'name': 'zr'})
        zrGroupIds = resultZr.get("data", [])
        for groupId in zrGroupIds:
            temp = {}
            resultNhPath = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_full_path/", datas={'id': groupId})
            nhName = resultNhPath.get("data", "_").split('_')
            temp['name'] = nhName[0] + "-" + nhName[1]
            resultDmzNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            temp['value'] = len(resultDmzNh.get("data", []))
            result.append(temp)
        return result

    def GetKfcPreorderInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_preorder_nh_online"})

        onlineCount = 0
        if resultNhOnline['status'] == 'SUCCESS':
            groupId = resultNhOnline.get("data", 0)
            resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            onlineCount = len(resultNhOnlineList.get("data", []))

        resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_preorder_zr_online"})
        if resultZrOnline['status'] == 'SUCCESS':
            groupId = resultZrOnline.get("data", 0)
            resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            onlineCount += len(resultZrOnlineList.get("data", []))

        resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_preorder_nh_pilot"})
        pilotCount = 0
        if resultNhPilot['status'] == 'SUCCESS':
            groupId = resultNhPilot.get("data",0)
            resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            pilotCount = len(resultNhPilotList.get("data", []))

        resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_preorder_zr_pilot"})
        if resultZrPilot['status'] == 'SUCCESS':
            groupId = resultZrPilot.get("data", 0)
            resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            pilotCount += len(resultZrPilotList.get("data", []))

        result.append({'name':'online','value':onlineCount})
        result.append({'name': 'pilot', 'value': pilotCount})
        return result

    def GetKfcDeliveryInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_delivery_nh_online"})

        onlineCount = 0
        if resultNhOnline['status'] == 'SUCCESS':
            groupId = resultNhOnline.get("data", 0)
            resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            onlineCount = len(resultNhOnlineList.get("data", []))

        resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_delivery_zr_online"})
        if resultZrOnline['status'] == 'SUCCESS':
            groupId = resultZrOnline.get("data", 0)
            resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            onlineCount += len(resultZrOnlineList.get("data", []))

        resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_delivery_nh_pilot"})
        pilotCount = 0
        if resultNhPilot['status'] == 'SUCCESS':
            groupId = resultNhPilot.get("data", 0)
            resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            pilotCount = len(resultNhPilotList.get("data", []))

        resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_delivery_zr_pilot"})
        if resultZrPilot['status'] == 'SUCCESS':
            groupId = resultZrPilot.get("data", 0)
            resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            pilotCount += len(resultZrPilotList.get("data", []))

        result.append({'name': 'online', 'value': onlineCount})
        result.append({'name': 'pilot', 'value': pilotCount})
        return result

    def GetPhDeliveryInfo(self):
        result = []
        hu = HttpUtils(self.request)
        resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "ph_delivery_nh_online"})

        onlineCount = 0
        if resultNhOnline['status'] == 'SUCCESS':
            groupId = resultNhOnline.get("data", 0)
            resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
            onlineCount = len(resultNhOnlineList.get("data", []))

        resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "ph_delivery_zr_online"})
        if resultZrOnline['status'] == 'SUCCESS':
            groupId = resultZrOnline.get("data", 0)
            resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                        datas={"id": groupId})
            onlineCount += len(resultZrOnlineList.get("data", []))

        resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                               datas={'path': "kfc_delivery_nh_pilot"})
        pilotCount = 0
        if resultNhPilot['status'] == 'SUCCESS':
            groupId = resultNhPilot.get("data", 0)
            resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            pilotCount = len(resultNhPilotList.get("data", []))

        resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "ph_delivery_zr_pilot"})
        if resultZrPilot['status'] == 'SUCCESS':
            groupId = resultZrPilot.get("data", 0)
            resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
            pilotCount += len(resultZrPilotList.get("data", []))

        result.append({'name': 'online', 'value': onlineCount})
        result.append({'name': 'pilot', 'value': pilotCount})
        return result
