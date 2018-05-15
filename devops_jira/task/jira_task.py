from celery import Celery
from django.conf import settings
from devops_jira.models.External_system_user_mapping import External_system_user_mapping
from devops_jira.models.JIRA_ISSUES import JIRA_ISSUES
from common.utils.jira_api import jira_api
import logging
import os

logger = logging.getLogger('devops_platform_log')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devops_platform_web.settings')
app = Celery('tasks', backend='amqp', broker='django://')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


is_run = False

@app.task
def issues_list_sync():
    global is_run
    if not is_run:
        try:
            fields = "project,issuetype,summary,components,assignee,priority,reporter,creator,status,created,updated"
            jql = "assignee = currentUser() ORDER BY updated DESC"
            user_mapping_list = External_system_user_mapping.objects.filter(external_system='jira')
            for user_mapping in user_mapping_list:
                jira_obj = jira_api(settings.JIRA_SERVER, user_mapping.external_system_username, user_mapping.external_system_password)
                jira_obj.login()
                issues_list = jira_obj.get_issue_list(jql_str=jql, page=0, limit=1000, fields=fields)
                for issues in issues_list:
                    files_t = issues.fields
                    defaults = {"issues_id":issues.id,
                                "issue_summary":files_t.summary,
                                "issue_type_id":files_t.issuetype.id,
                                "issue_type_name":files_t.issuetype.name,
                                "issue_priority":files_t.priority.name,
                                "issue_reporter":files_t.reporter.displayName,
                                "issue_status":files_t.status.name,
                                "issue_create_date":files_t.created.replace("T"," ").replace("+0800",""),
                                "issue_assignee":files_t.assignee.key,
                                "project_Id":files_t.project.id,
                                "project_key":files_t.project.key,
                                "inner_user_name":user_mapping.inner_user_name,
                                "inner_user_group": user_mapping.inner_user_group
                    }
                    JIRA_ISSUES.objects.update_or_create(issues_id=issues.id,defaults=defaults)

            print("issues_list_sync is runing ")
        except Exception as e:
            logger.error(e)
