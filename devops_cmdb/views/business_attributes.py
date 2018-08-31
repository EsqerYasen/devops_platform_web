from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from devops_platform_web.settings import PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('devops_platform_log')

def business_list(request):
    return render(request, 'business/business_list.html')

class Attributes_Manage_View(LoginRequiredMixin, TemplateView):
    template_name = "business/attributes_manage.html"

    def get_context_data(self, **kwargs):
        context = super(Attributes_Manage_View, self).get_context_data(**kwargs)
        context['business_id'] = kwargs.get('pk')
        return context

def __rest_business_resp(request, restName, serviceName):
    restName=restName
    serviceName=serviceName
    if request.method=='GET':
        business_id = request.GET.get('business_id', None)
        data = dict(business_id=business_id) if business_id is not None else None
        name = request.GET.get('name', None)
        data = dict(business_id=business_id) if business_id is not None else None
        if name:
            data.update({'name':name})
        hu = HttpUtils(request)
        ret = hu.get(serivceName="cmdb", restName=restName, datas=data)
        #print(ret)
        return JsonResponse(data=ret)
    elif request.method=='POST':
        hu = HttpUtils(request)
        data = json.loads(request.body)
        ret = hu.post(serivceName="cmdb", restName=restName, datas=data)
        #print(ret.json())
        return JsonResponse(data=ret.json())

@csrf_exempt
def rest_business(request):
    restName="/rest/business/attributes_manage/business/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

@csrf_exempt
def rest_business_attr(request):
    restName = "/rest/business/attributes_manage/attr/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

@csrf_exempt
def rest_business_int(request):
    restName = "/rest/business/attributes_manage/interface/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

@csrf_exempt
def rest_business_cmt(request):
    restName = "/rest/business/attributes_manage/cmt/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

@csrf_exempt
def rest_business_attr_history(request):
    restName = "/rest/business/attributes_manage/attrHistory/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

@csrf_exempt
def rest_business_int_history(request):
    restName = "/rest/business/attributes_manage/interfaceHistory/"
    serviceName = "cmdb"
    return __rest_business_resp(request, restName, serviceName)

class BusinesAttributessView(LoginRequiredMixin, TemplateView):
    template_name = "business_attributes.html"

    def get_context_data(self, **kwargs):
        context = super(BusinesAttributessView, self).get_context_data(**kwargs)
        reqGet = self.request.GET
        tab = reqGet.get("tab", 0)
        # self.template_name = self.template_name_dict[tab]
        offset = int(reqGet.get('offset', 1))

        resultJson = {}
        if tab == "0":
            resultJson = self.brandList(reqGet)
        elif tab == "1":
            resultJson = self.groupList(reqGet)
            context['brand_list'] = self.brandList({'offset': 1, 'limit': 1000, 'is_enabled': 1}).get("results", [])
        elif tab == "2":
            resultJson = self.moduleList(reqGet)
            context['brand_list'] = self.brandList({'offset': 1, 'limit': 1000, 'is_enabled': 1}).get("results", [])
        elif tab == "3":
            resultJson = self.serviceList(reqGet)
            context['brand_list'] = self.brandList({'offset': 1, 'limit': 1000, 'is_enabled': 1}).get("results", [])
        elif tab == "4":
            resultJson = self.middlewareList(reqGet)
        elif tab == "5":
            resultJson = self.logical_idcList(reqGet)
        elif tab == "6":
            resultJson = self.physical_idcList(reqGet)
        elif tab == "7":
            resultJson = self.deployment_environmentList(reqGet)
        elif tab == "8":
            resultJson = self.dns(reqGet)

        list = resultJson.get("results", [])
        paginator = Paginator(list, PER_PAGE)
        count = resultJson.get("count", 0)
        paginator.count = count
        context['result_list'] = list
        context['is_paginated'] = count > 0
        context['page_obj'] = paginator.page(offset)
        context['paginator'] = paginator
        context['tab'] = tab
        return context

    def brandList(self, args):
        offset = int(args.get('offset', 1))
        limit = int(args.get('limit', 0))
        offset2 = (offset - 1) * PER_PAGE
        if limit == 0:
            limit = PER_PAGE

        getData = {'offset': offset2, 'limit': limit, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)
        return resultJson

    def groupList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        biz_brand_id = args.get('biz_brand_id', None)
        if biz_brand_id:
            getData['biz_brand'] = biz_brand_id
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/groups/", datas=getData)
        return resultJson

    def moduleList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        biz_brand_id = args.get('biz_brand_id', None)
        if biz_brand_id:
            getData['biz_brand'] = biz_brand_id
        biz_group_id = args.get('biz_group_id', None)
        if biz_group_id:
            getData['biz_group'] = biz_group_id
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/modules/", datas=getData)
        return resultJson

    def serviceList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        biz_brand_id = args.get('biz_brand_id', None)
        if biz_brand_id:
            getData['biz_brand'] = biz_brand_id
        biz_group_id = args.get('biz_group_id', None)
        if biz_group_id:
            getData['biz_group'] = biz_group_id
        biz_module_id = args.get('biz_module_id', None)
        if biz_module_id:
            getData['biz_module'] = biz_module_id
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/services/", datas=getData)
        return resultJson

    def middlewareList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)
        return resultJson

    def logical_idcList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)
        return resultJson

    def physical_idcList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)
        return resultJson

    def deployment_environmentList(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)
        return resultJson

    def dns(self, args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils(self.request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)
        return resultJson

class BusinesAttributessCreateAjaxView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        try:
            tab = request.POST.get("tab", None)
            resultJson = {}
            if tab == "0":
                resultJson = self.createBrand(request)
            elif tab == "1":
                resultJson = self.createGroup(request)
            elif tab == "2":
                resultJson = self.createModule(request)
            elif tab == "3":
                resultJson = self.createService(request)
            elif tab == "4":
                resultJson = self.createMiddleware(request)
            elif tab == "5":
                resultJson = self.createLogical_idc(request)
            elif tab == "6":
                resultJson = self.createPhysical_idc(request)
            elif tab == "7":
                resultJson = self.createDeployment_environment(request)
            elif tab == "8":
                resultJson = self.createDns(request)

        except Exception as e:
            logger.error(e)
        return self.render_json_response(resultJson)

    def createBrand(self,req):
        result = {}
        saveJson = req.POST.get("saveJson",None)
        if saveJson:
            user = req.user
            saveJson = eval(saveJson)
            saveJson['created_by'] = user.username
            saveJson['updated_by'] = user.username
            saveJson['is_enabled'] = True
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/brand_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
        else:
            result['status'] = 'FAILURE';
        return result

    def createGroup(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            user = req.user
            saveJson = eval(saveJson)
            if int(saveJson.get("biz_brand_id",0)) > 0:
                saveJson['created_by'] = user.username
                saveJson['updated_by'] = user.username
                saveJson['is_enabled'] = True
                hu = HttpUtils(req)
                resultJson = hu.post(serivceName="cmdb", restName="/rest/group_add/", datas=saveJson)
                resultJson = resultJson.json()
                if resultJson['status'] == 'SUCCESS':
                    result['status'] = 'SUCCESS';
                else:
                    result['status'] = 'FAILURE';
                    result['msg'] = resultJson['msg'];
            else:
                result['status'] = 'FAILURE';
                result['msg'] = '品牌为空';
        else:
            result['status'] = 'FAILURE';
        return result

    def createModule(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            user = req.user
            saveJson = eval(saveJson)
            brand_id = int(saveJson.get("biz_brand_id", 0))
            group_id = int(saveJson.get("biz_group_id", 0))
            if brand_id > 0 and group_id > 0:
                hu = HttpUtils(req)
                resultJson = hu.post(serivceName="cmdb", restName="/rest/module_add/", datas=saveJson)
                resultJson = resultJson.json()
                if resultJson['status'] == 'SUCCESS':
                    result['status'] = 'SUCCESS';
                else:
                    result['status'] = 'FAILURE';
                    result['msg'] = resultJson['msg'];
            else:
                result['status'] = 'FAILURE';
                result['msg'] = '品牌或业务线为空';
        else:
            result['status'] = 'FAILURE';
        return result

    def createService(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            user = req.user
            saveJson = eval(saveJson)
            brand_id = int(saveJson.get("biz_brand_id", 0))
            group_id = int(saveJson.get("biz_group_id", 0))
            module_id = int(saveJson.get("biz_module_id", 0))
            if brand_id > 0 and group_id > 0 and module_id > 0:
                hu = HttpUtils(req)
                resultJson = hu.post(serivceName="cmdb", restName="/rest/service_add/", datas=saveJson)
                resultJson = resultJson.json()
                if resultJson['status'] == 'SUCCESS':
                    result['status'] = 'SUCCESS';
                else:
                    result['status'] = 'FAILURE';
                    result['msg'] = resultJson['msg'];
            else:
                result['status'] = 'FAILURE';
                result['msg'] = '品牌、业务线或模块为空';
        else:
            result['status'] = 'FAILURE';
        return result

    def createMiddleware(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/middleWare_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def createLogical_idc(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/logicalIDC_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def createPhysical_idc(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/physicalIDC_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def createDeployment_environment(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/deploymentEnv_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def createDns(self, req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/dns_add/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result


class BusinesAttributessUpdateAjaxView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        try:
            tab = request.POST.get("tab", None)
            resultJson = {}
            if tab == "0":
                resultJson = self.updateBrand(request)
            elif tab == "1":
                resultJson = self.updateGroup(request)
            elif tab == "2":
                resultJson = self.updateModule(request)
            elif tab == "3":
                resultJson = self.updateService(request)
            elif tab == "4":
                resultJson = self.updateMiddleware(request)
            elif tab == "5":
                resultJson = self.updateLogical_idc(request)
            elif tab == "6":
                resultJson = self.updatePhysical_idc(request)
            elif tab == "7":
                resultJson = self.updateDeployment_environment(request)
            elif tab == "8":
                resultJson = self.updateDns(request)

        except Exception as e:
            logger.error(e)
        return self.render_json_response(resultJson)

    def updateBrand(self,req):
        result = {}
        saveJson = req.POST.get("saveJson",None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/brand_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateGroup(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/group_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateModule(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/module_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateService(self, req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/service_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateMiddleware(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/middleWare_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateLogical_idc(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/logicalIDC_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updatePhysical_idc(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/physicalIDC_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateDeployment_environment(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/deploymentEnv_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result

    def updateDns(self,req):
        result = {}
        saveJson = req.POST.get("saveJson", None)
        if saveJson:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/dns_edit/", datas=saveJson)
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result


class BusinesAttributessDelAjaxView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        try:
            tab = request.POST.get("tab", None)
            resultJson = {}
            url = ""
            if tab == "0":
                url = "/rest/brand_edit/"
            elif tab == "1":
                url = "/rest/group_edit/"
            elif tab == "2":
                url = "/rest/module_edit/"
            elif tab == "3":
                url = "/rest/service_edit/"
            elif tab == "4":
                url = "/rest/middleWare_edit/"
            elif tab == "5":
                url = "/rest/logicalIDC_edit/"
            elif tab == "6":
                url = "/rest/physicalIDC_edit/"
            elif tab == "7":
                url = "/rest/deploymentEnv_edit/"
            elif tab == "8":
                url = "/rest/dns_edit/"
            resultJson = self.delPub(url,request)
        except Exception as e:
            logger.error(e)
        return self.render_json_response(resultJson)

    def delPub(self,url,req):
        result = {}
        id = req.POST.get("id",None)
        if id:
            hu = HttpUtils(req)
            resultJson = hu.post(serivceName="cmdb", restName=url, datas={"id":id,"is_enabled":False})
            resultJson = resultJson.json()
            if resultJson['status'] == 'SUCCESS':
                result['status'] = 'SUCCESS';
            else:
                result['status'] = 'FAILURE';
                result['msg'] = resultJson['msg'];
        else:
            result['status'] = 'FAILURE';
        return result



class GetGroupsByBrandId(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        brand_id = request.GET.get("brand_id", 0)
        if brand_id == "":
            brand_id = 0
        hu = HttpUtils(request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/groups",
                            datas={"biz_brand": brand_id, 'limit': 100, "offset": 0, 'is_enabled': 1})

        return self.render_json_response(resultJson["results"])

class GetModulesByBIdGId(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        brand_id = request.GET.get("brand_id", 0)
        if brand_id == "":
            brand_id = 0
        group_id = request.GET.get("group_id", 0)
        if group_id == "":
            group_id = 0
        hu = HttpUtils(request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/modules",
                            datas={"biz_brand": brand_id,'biz_group':group_id, 'limit': 100, "offset": 0, 'is_enabled': 1})

        return self.render_json_response(resultJson["results"])

class GetServiceByBIdGIdMid(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        brand_id = request.GET.get("brand_id", 0)
        if brand_id == "":
            brand_id = 0
        group_id = request.GET.get("group_id", 0)
        if group_id == "":
            group_id = 0
        biz_module = request.GET.get("biz_module", 0)
        if biz_module == "":
            biz_module = 0
        hu = HttpUtils(request)
        resultJson = hu.get(serivceName="cmdb", restName="/rest/services",
                            datas={"biz_brand": brand_id,'biz_group':group_id,'biz_module':biz_module, 'limit': 100, "offset": 0, 'is_enabled': 1})

        return self.render_json_response(resultJson["results"])
