from braces.views import *
from django.views.generic import *
from django.conf import settings
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from devops_jira.models.JIRA_FIELDS_CONFIG import *
from devops_jira.models.JIRA_ISSUES import JIRA_ISSUES
from devops_platform_web.settings import PER_PAGE
import logging,xlrd,json,datetime

from devops_jira.task.jira_task import *

logger = logging.getLogger('devops_platform_log')

class IssuesListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "issues_list.html"
    model = JIRA_ISSUES
    paginate_by = PER_PAGE
    context_object_name = 'result_list'

    def get_queryset(self):
        req = self.request
        status = req.GET.get("status",None)
        result_list = JIRA_ISSUES.objects.filter(inner_user_group=req.devopsgroup)

        return result_list

    def get_context_data(self, **kwargs):
        req = self.request
        JiraIssueListSync().issues_list_sync(req.devopsuser)
        context = super(IssuesListView, self).get_context_data(**kwargs)
        return context


class IssuesDetailView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "issues_detail.html"

    def get_context_data(self, **kwargs):
        context = super(IssuesDetailView, self).get_context_data(**kwargs)
        result = {}
        try:
            req = self.request
            pid = req.GET.get("pid",None)
            itid = req.GET.get("itid",None)
            iid = req.GET.get("iid",None)
            if pid and itid and iid:
                fields_config = JIRA_FIELDS_CONFIG.objects.filter(project_id=pid,issue_type_id=itid)
                #user_mapping_list = External_system_user_mapping.objects.filter(external_system='jira',inner_user_name=req.devopsuser)
                #if user_mapping_list and fields_config:
                if fields_config:
                    #user_mapping = user_mapping_list[0]
                    fields_config_obj = json.loads(fields_config[0].fields_config_json)

                    jira_obj = jira_api(settings.JIRA_SERVER, settings.JIRA_USER,settings.JIRA_PWD)
                    jira_obj.login()
                    issue_info = jira_obj.get_issue_info(iid)
                    transitions = jira_obj.get_transitions_from_issue(issue_info)
                    result['issues_id'] = iid
                    i_transitions = []
                    for tran in transitions:
                        i_transitions.append({'id':tran['id'],'name':tran['name']})
                    result['transitions'] = i_transitions
                    raw = issue_info.raw
                    fields = raw['fields']
                    fields['comment']['comments'].reverse()
                    i_comments = fields['comment']['comments']
                    comments = []
                    for com in i_comments:
                        if com.get("body",None):
                            comments.append({'body':com.get("body",''),
                                             'created':com.get("created",'').replace("T"," ")[:-9],
                                             'updated':com.get("updated",'').replace("T"," ")[:-9],
                                             'author':com.get("author",'').get("name",''),
                                             'updateAuthor':com.get("author",'').get("name",'')})
                    result['comments'] = comments
                    fields_list = []
                    for config in fields_config_obj:
                        value = fields.get(config['key'],"")
                        if value is None:
                            value = ""
                        config['value'] = value
                        fields_list.append(config)

                    result['fields'] = fields_list
                    result['description'] = fields.get("description","")
                    result['type'] = fields['issuetype']['name']
                    result['status'] = fields['status']['name']
                    result['priority'] = fields['priority']['name']
                    result['labels'] = ','.join(fields['labels'])
                    result['assignee'] = fields['assignee']['name']
                    result['reporter'] = fields['reporter']['name']
            context["result"] = result
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            issues_id = request.POST.get('issues_id', '')
            transition_id = request.POST.get('tran_id', '')
            assignee = request.POST.get('assignee', '')
            #transition_name = request.POST.get('tran_name', '')
            comment = request.POST.get('comment', '')
            user_mapping_list = External_system_user_mapping.objects.filter(external_system='jira',inner_user_name=req.devopsuser)
            if user_mapping_list:
                user_mapping = user_mapping_list[0]
                jira_obj = jira_api(settings.JIRA_SERVER, user_mapping.external_system_username,user_mapping.external_system_password)
                jira_obj.login()
                jira_obj.transition_issues(issues_id, transition_id, assignee, comment)
                JIRA_ISSUES.objects.filter(issues_id=issues_id).update(issue_assignee=assignee,issue_status=None)
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class JiraIssueListSync():

    def issues_list_sync(self,username):
        try:
            fields = "project,issuetype,summary,components,assignee,priority,reporter,creator,status,created,updated"
            #jql = "assignee = %s and issuetype = 版本发布 and project IN (KPO,KD,KRD) and status != Closed ORDER BY updated DESC"
            jql = "assignee = %s and issuetype = 版本发布 and project IN (KPO,KD) and status != Closed ORDER BY updated DESC"
            user_mapping_list = External_system_user_mapping.objects.filter(external_system='jira',inner_user_name=username)
            for user_mapping in user_mapping_list:
                jira_obj = jira_api(settings.JIRA_SERVER, settings.JIRA_USER,settings.JIRA_PWD)
                jira_obj.login()
                jql = jql % (user_mapping.external_system_username)
                issues_list = jira_obj.get_issue_list(jql_str=jql, page=0, limit=1000, fields=fields)
                for issues in issues_list:
                    files_t = issues.fields
                    defaults = {"issues_id": issues.id,
                                "issue_summary": files_t.summary,
                                "issue_type_id": files_t.issuetype.id,
                                "issue_type_name": files_t.issuetype.name,
                                "issue_priority": files_t.priority.name,
                                "issue_reporter": files_t.reporter.displayName,
                                "issue_status": files_t.status.name,
                                "issue_create_date": datetime.datetime.strptime(files_t.created.replace("T"," ")[:-9], "%Y-%m-%d %H:%M:%S"),
                                "issue_assignee": files_t.assignee.key,
                                "project_Id": files_t.project.id,
                                "project_key": files_t.project.key,
                                "inner_user_name": user_mapping.inner_user_name,
                                "inner_user_group": user_mapping.inner_user_group
                                }
                    JIRA_ISSUES.objects.update_or_create(issues_id=issues.id, defaults=defaults)
        except Exception as e:
            logger.error(e)