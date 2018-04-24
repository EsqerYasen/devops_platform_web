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
            elif flag == '7':
                resultList = self.GetPublicCouponInfo();
            elif flag == '8':
                resultList = self.GetPublicEGiftcardInfo();

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
        # resultNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_id_by_name/",datas={'name':'nh'})
        # nhGroupIds = resultNh.get("data",[])
        # for groupId in nhGroupIds:
        #     temp = {}
        #     resultNhPath = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_full_path/", datas={'id': groupId})
        #     if resultNhPath['status'] == "SUCCESS":
        #         nhName = resultNhPath.get("data","_").split('_')
        #         temp['name'] = nhName[0]+"-"+nhName[1]
        #         resultDmzNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
        #         temp['value'] = len(resultDmzNh.get("data",[]))
        #         result.append(temp)
        group = self.request.devopsgroup
        if group == 'ec':
            groupId1 = 0
            resultKfcPreOrder = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "kfc_preorder_nh"})
            if resultKfcPreOrder['status'] == 'SUCCESS':
                groupId1 = resultKfcPreOrder.get("data", 0)

            groupId2 = 0
            resultPublic = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "public"})
            if resultPublic['status'] == 'SUCCESS':
                resultPublic.get("data", 0)

            result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": str(groupId1)+"+"+str(groupId2)})
            count1 = len(result1List.get("data", []))
            result.append({'name':'kfc_preorder','value':count1})

            resultKfcDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/", datas={'path': "kfc_delivery_nh"})
            if resultKfcDelivery['status'] == 'SUCCESS':
                groupId =  resultKfcDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_delivery', 'value': count1})

            resultPhDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",datas={'path': "ph_delivery_nh"})
            if resultPhDelivery['status'] == 'SUCCESS':
                groupId = resultPhDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'ph_delivery', 'value': count1})

            resultDevops = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/", datas={'path': "devops"})
            if resultDevops['status'] == 'SUCCESS':
                groupId = resultDevops.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'devops', 'value': count1})

            resultGoLive = hu.get(serivceName="cmdb", restName="/rest/host/", datas={'offset': 0, 'limit': 1,'go_live':1, "physical_idc": 'nh'})
            count1 = resultGoLive.get("count", 0)
            result.append({'name': '弹性节点', 'value': count1})
        elif group == 'brand':
            groupId1 = 0
            resultKfcPreOrder = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_superapp_nh"})
            if resultKfcPreOrder['status'] == 'SUCCESS':
                groupId1 = resultKfcPreOrder.get("data", 0)

            groupId2 = 0
            resultPublic = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                  datas={'path': "public"})
            if resultPublic['status'] == 'SUCCESS':
                resultPublic.get("data", 0)

            result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                 datas={"id": str(groupId1) + "+" + str(groupId2)})
            count1 = len(result1List.get("data", []))
            result.append({'name': 'kfc_superapp', 'value': count1})

            resultKfcDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_campaign_nh"})
            if resultKfcDelivery['status'] == 'SUCCESS':
                groupId = resultKfcDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_campaign', 'value': count1})

            resultPhDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                      datas={'path': "kfc_ges_nh"})
            if resultPhDelivery['status'] == 'SUCCESS':
                groupId = resultPhDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_ges', 'value': count1})

            resultDevops = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                  datas={'path': "kfc_crm_nh"})
            if resultDevops['status'] == 'SUCCESS':
                groupId = resultDevops.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_crm', 'value': count1})

            resultGoLive = hu.get(serivceName="cmdb", restName="/rest/host/",
                                  datas={'offset': 0, 'limit': 1, 'go_live': 1, "physical_idc": 'nh'})
            count1 = resultGoLive.get("count", 0)
            result.append({'name': '弹性节点', 'value': count1})
        return result

    def GetZrBizGroupInfo(self):
        result = []
        hu = HttpUtils(self.request)
        # resultZr = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_id_by_name/", datas={'name': 'zr'})
        # zrGroupIds = resultZr.get("data", [])
        # for groupId in zrGroupIds:
        #     temp = {}
        #     resultNhPath = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_full_path/", datas={'id': groupId})
        #     if resultNhPath['status'] == "SUCCESS":
        #         nhName = resultNhPath.get("data", "_").split('_')
        #         temp['name'] = nhName[0] + "-" + nhName[1]
        #         resultDmzNh = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
        #         temp['value'] = len(resultDmzNh.get("data", []))
        #         result.append(temp)
        group = self.request.devopsgroup
        if group == 'ec':
            groupId1 = 0
            resultKfcPreOrder = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_preorder_zr"})
            if resultKfcPreOrder['status'] == 'SUCCESS':
                groupId1 = resultKfcPreOrder.get("data", 0)

            groupId2 = 0
            resultPublic = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/", datas={'path': "public"})
            if resultPublic['status'] == 'SUCCESS':
                resultPublic.get("data", 0)

            result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                 datas={"id": str(groupId1) + "+" + str(groupId2)})
            count1 = len(result1List.get("data", []))
            result.append({'name': 'kfc_preorder', 'value': count1})

            resultKfcDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_delivery_zr"})
            if resultKfcDelivery['status'] == 'SUCCESS':
                groupId = resultKfcDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_delivery', 'value': count1})

            resultPhDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                      datas={'path': "ph_delivery_zr"})
            if resultPhDelivery['status'] == 'SUCCESS':
                groupId = resultPhDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'ph_delivery', 'value': count1})

            resultDevops = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/", datas={'path': "devops"})
            if resultDevops['status'] == 'SUCCESS':
                groupId = resultDevops.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'devops', 'value': count1})

            resultGoLive = hu.get(serivceName="cmdb", restName="/rest/host/",
                                  datas={'offset': 0, 'limit': 1, 'go_live': 1, "physical_idc": 'zr'})
            count1 = resultGoLive.get("count", 0)
            result.append({'name': '弹性节点', 'value': count1})
        elif group == 'brand':
            groupId1 = 0
            resultKfcPreOrder = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_superapp_nh"})
            if resultKfcPreOrder['status'] == 'SUCCESS':
                groupId1 = resultKfcPreOrder.get("data", 0)

            groupId2 = 0
            resultPublic = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                  datas={'path': "public"})
            if resultPublic['status'] == 'SUCCESS':
                resultPublic.get("data", 0)

            result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                 datas={"id": str(groupId1) + "+" + str(groupId2)})
            count1 = len(result1List.get("data", []))
            result.append({'name': 'kfc_superapp', 'value': count1})

            resultKfcDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                       datas={'path': "kfc_campaign_zr"})
            if resultKfcDelivery['status'] == 'SUCCESS':
                groupId = resultKfcDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_campaign', 'value': count1})

            resultPhDelivery = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                      datas={'path': "kfc_ges_zr"})
            if resultPhDelivery['status'] == 'SUCCESS':
                groupId = resultPhDelivery.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_ges', 'value': count1})

            resultDevops = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                  datas={'path': "kfc_crm_zr"})
            if resultDevops['status'] == 'SUCCESS':
                groupId = resultDevops.get("data", 0)
                result1List = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/", datas={"id": groupId})
                count1 = len(result1List.get("data", []))
                result.append({'name': 'kfc_crm', 'value': count1})

            resultGoLive = hu.get(serivceName="cmdb", restName="/rest/host/",
                                  datas={'offset': 0, 'limit': 1, 'go_live': 1, "physical_idc": 'zr'})
            count1 = resultGoLive.get("count", 0)
            result.append({'name': '弹性节点', 'value': count1})
        return result

    def GetKfcPreorderInfo(self):
        result = {}
        group = self.request.devopsgroup
        hu = HttpUtils(self.request)
        if group == 'ec':
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

            data = []

            data.append({'name':'online','value':onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'KFC-PreOrder'
        elif group == 'brand':
            resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_superapp_nh_online"})

            onlineCount = 0
            if resultNhOnline['status'] == 'SUCCESS':
                groupId = resultNhOnline.get("data", 0)
                resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount = len(resultNhOnlineList.get("data", []))

            resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_superapp_zr_online"})
            if resultZrOnline['status'] == 'SUCCESS':
                groupId = resultZrOnline.get("data", 0)
                resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount += len(resultZrOnlineList.get("data", []))

            resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_superapp_nh_pilot"})
            pilotCount = 0
            if resultNhPilot['status'] == 'SUCCESS':
                groupId = resultNhPilot.get("data", 0)
                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount = len(resultNhPilotList.get("data", []))

            resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_superapp_zr_pilot"})
            if resultZrPilot['status'] == 'SUCCESS':
                groupId = resultZrPilot.get("data", 0)
                resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount += len(resultZrPilotList.get("data", []))

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'KFC-SuperApp'
        return result

    def GetKfcDeliveryInfo(self):
        result = {}
        hu = HttpUtils(self.request)
        group = self.request.devopsgroup
        if group == 'ec':
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

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'KFC-Delivery'
        elif group == 'brand':
            resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_campaign_nh_online"})

            onlineCount = 0
            if resultNhOnline['status'] == 'SUCCESS':
                groupId = resultNhOnline.get("data", 0)
                resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount = len(resultNhOnlineList.get("data", []))

            resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_campaign_zr_online"})
            if resultZrOnline['status'] == 'SUCCESS':
                groupId = resultZrOnline.get("data", 0)
                resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount += len(resultZrOnlineList.get("data", []))

            resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_campaign_nh_pilot"})
            pilotCount = 0
            if resultNhPilot['status'] == 'SUCCESS':
                groupId = resultNhPilot.get("data", 0)
                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount = len(resultNhPilotList.get("data", []))

            resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_campaign_zr_pilot"})
            if resultZrPilot['status'] == 'SUCCESS':
                groupId = resultZrPilot.get("data", 0)
                resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount += len(resultZrPilotList.get("data", []))

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'KFC-Campaign'
        return result

    def GetPhDeliveryInfo(self):
        result = {}
        hu = HttpUtils(self.request)
        group = self.request.devopsgroup
        if group == 'ec':
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

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'PH-Delivery'
        elif group == 'brand':
            resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_ges_nh_online"})

            onlineCount = 0
            if resultNhOnline['status'] == 'SUCCESS':
                groupId = resultNhOnline.get("data", 0)
                resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount = len(resultNhOnlineList.get("data", []))

            resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "kfc_ges_zr_online"})
            if resultZrOnline['status'] == 'SUCCESS':
                groupId = resultZrOnline.get("data", 0)
                resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount += len(resultZrOnlineList.get("data", []))

            resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_ges_nh_pilot"})
            pilotCount = 0
            if resultNhPilot['status'] == 'SUCCESS':
                groupId = resultNhPilot.get("data", 0)
                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount = len(resultNhPilotList.get("data", []))

            resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "kfc_ges_zr_pilot"})
            if resultZrPilot['status'] == 'SUCCESS':
                groupId = resultZrPilot.get("data", 0)
                resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount += len(resultZrPilotList.get("data", []))

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'KFC-Ges'
        return result


    def GetPublicCouponInfo(self):

        result = {}
        hu = HttpUtils(self.request)
        group = self.request.devopsgroup
        if group == 'ec':
            pass
        elif group == 'brand':
            resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "public_coupon_nh_online"})

            onlineCount = 0
            if resultNhOnline['status'] == 'SUCCESS':
                groupId = resultNhOnline.get("data", 0)
                resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount = len(resultNhOnlineList.get("data", []))

            resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "public_coupon_zr_online"})
            if resultZrOnline['status'] == 'SUCCESS':
                groupId = resultZrOnline.get("data", 0)
                resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount += len(resultZrOnlineList.get("data", []))

            resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "public_coupon_nh_pilot"})
            pilotCount = 0
            if resultNhPilot['status'] == 'SUCCESS':
                groupId = resultNhPilot.get("data", 0)
                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount = len(resultNhPilotList.get("data", []))

            resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "public_coupon_zr_pilot"})
            if resultZrPilot['status'] == 'SUCCESS':
                groupId = resultZrPilot.get("data", 0)
                resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount += len(resultZrPilotList.get("data", []))

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'Public-Coupon'
        return result

    def GetPublicEGiftcardInfo(self):

        result = {}
        hu = HttpUtils(self.request)
        group = self.request.devopsgroup
        if group == 'ec':
            pass
        elif group == 'brand':
            resultNhOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "public_e-giftcard_nh_online"})

            onlineCount = 0
            if resultNhOnline['status'] == 'SUCCESS':
                groupId = resultNhOnline.get("data", 0)
                resultNhOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount = len(resultNhOnlineList.get("data", []))

            resultZrOnline = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                    datas={'path': "public_e-giftcard_zr_online"})
            if resultZrOnline['status'] == 'SUCCESS':
                groupId = resultZrOnline.get("data", 0)
                resultZrOnlineList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                            datas={"id": groupId})
                onlineCount += len(resultZrOnlineList.get("data", []))

            resultNhPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "public_e-giftcard_nh_pilot"})
            pilotCount = 0
            if resultNhPilot['status'] == 'SUCCESS':
                groupId = resultNhPilot.get("data", 0)
                resultNhPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount = len(resultNhPilotList.get("data", []))

            resultZrPilot = hu.get(serivceName="cmdb", restName="/rest/hostgroup/get_id_by_path/",
                                   datas={'path': "public_e-giftcard_zr_pilot"})
            if resultZrPilot['status'] == 'SUCCESS':
                groupId = resultZrPilot.get("data", 0)
                resultZrPilotList = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host/",
                                           datas={"id": groupId})
                pilotCount += len(resultZrPilotList.get("data", []))

            data = []
            data.append({'name': 'online', 'value': onlineCount})
            data.append({'name': 'pilot', 'value': pilotCount})
            result['data'] = data
            result['title'] = 'public-E-Giftcard'
        return result