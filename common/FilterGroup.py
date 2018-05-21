from django.utils.deprecation import MiddlewareMixin
from devops_platform_web.settings import PER_PAGE
from django.views import debug
from django.http import Http404
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

class Filter(MiddlewareMixin):
    def process_request(self, request):
        response = None
        method = request.method
        devopsgroup = None
        offset = 0
        limit = 0
        if method == "GET":
            devopsgroup = request.GET.get("devopsgroup",None)
            offset = int(request.GET.get('offset', 1))
            limit = int(request.GET.get('limit', PER_PAGE))
        if  method == "POST":
            devopsgroup = request.POST.get("devopsgroup", None)
            offset = int(request.POST.get('offset', 1))
            limit = int(request.POST.get('limit', PER_PAGE))

        request.offset = offset
        request.limit = limit
        user = request.user
        if user.is_active:  #user.is_authenticated
            request.clienttype = 'PC'
            if devopsgroup:
                request.devopsgroup = devopsgroup
                request.devopsuser = user.username
            else:
                isSuperUser = user.is_superuser
                if isSuperUser:
                    devopsgroup = 'all'
                else:
                    user_group = Group.objects.get(user=user)
                    devopsgroup = user_group.name
                if devopsgroup:
                    request.devopsgroup = devopsgroup
                    request.devopsuser = user.username
                else:
                    response = debug.technical_404_response(request, Http404())

        return response

