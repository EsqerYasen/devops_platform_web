from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import PER_PAGE,UPLOAD_SCRIPT_PATH
from django.core.paginator import Paginator
from common.utils.HttpUtils import *
from django.urls import reverse_lazy
from django.http import HttpResponse
import logging,os

logger = logging.getLogger('devops_platform_log')

class CommandSetList2View(LoginRequiredMixin, OrderableListMixin, ListView):
    paginate_by = PER_PAGE
    template_name = "command_set_list2.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(CommandSetList2View, self).get_context_data(**kwargs)
        try:
            req = self.request
            offset = int(req.GET.get('offset', 1))

            hu = HttpUtils()
            offset2 = (offset - 1)*10
            resultJson = hu.get(serivceName="job", restName="/rest/job/list/", datas={'offset': offset2, 'limit': PER_PAGE})
            list = resultJson.get("results", [])

            paginator = Paginator(resultJson.get("results", []), PER_PAGE)
            count = resultJson.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class CommandSetCreate2View(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):

    template_name = "command_set_form2.html"
    success_url = reverse_lazy("platform:command_set2/list/")

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils()
            pidc_list = hu.get(serivceName="appcenter", restName="/rest/pidc/", datas={})
            env_list = hu.get(serivceName="appcenter", restName="/rest/env/", datas={})

            context["view_num"] = 0
            context["result_dict"] = {}
            context['pidc_list'] = pidc_list["results"]
            context['env_list'] = env_list["results"]
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            user = request.user
            files = request.FILES
            command_set = request.POST.get("command_set",None)

            hu = HttpUtils()
            resultJson = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_set)
            resultJson  = eval(resultJson.text)
            if(resultJson["status"] == "FAILURE"):
                result['status'] = 1
            else:
                data = resultJson["data"]
                for k in data:
                    step_ids = data[k]
                    for file in files:
                        t = file.split(',')
                        step = step_ids[int(t[0])]
                        f = files[file]
                        path = UPLOAD_SCRIPT_PATH + k + "/"
                        for k2 in step:
                            line = step[k2]
                            path += str(k2) + "/"+str(line[int(t[1])])+"/"
                            os.makedirs(path)
                            destination = open(os.path.join(path, f.name), 'wb+')
                            for chunk in f.chunks():
                                destination.write(chunk)
                            destination.close()
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')