from django.db import models

# jira issues信息表
class JIRA_ISSUES(models.Model):
    project_Id = models.CharField(max_length=20, verbose_name="项目Id", null=True)
    project_key = models.CharField(max_length=100, verbose_name="项目", null=True)
    issues_id = models.CharField(max_length=100, verbose_name="问题类型", null=True)
    issue_type_id = models.CharField(max_length=20, verbose_name="问题类型ID", null=True)
    issue_type_name = models.CharField(max_length=100, verbose_name="问题类型", null=True)
    issue_summary = models.CharField(max_length=200, verbose_name="主题", null=True)
    issue_priority = models.CharField(max_length=20, verbose_name="优先级", null=True)
    issue_reporter = models.CharField(max_length=30, verbose_name="报告人", null=True)
    issue_assignee = models.CharField(max_length=30, verbose_name="经办人", null=True)
    issue_status = models.CharField(max_length=20, verbose_name="状态", null=True)
    issue_create_date = models.DateTimeField(verbose_name="JIRA ISSUE 创建时间", blank=True, null=True)
    inner_user_group = models.CharField(max_length=10, verbose_name="内部系统账户组", null=True)
    inner_user_name = models.CharField(max_length=30, verbose_name="内部系统用户名称", null=True)

def __str__(self):
    return self.name

class Meta:
    verbose_name = "jira字段对应信息表"
    verbose_name_plural = verbose_name

