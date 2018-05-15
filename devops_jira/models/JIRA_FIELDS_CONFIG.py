from django.db import models

# jira字段对应信息表
class JIRA_FIELDS_CONFIG(models.Model):
    project_id = models.IntegerField(blank=True, null=True, verbose_name='jira project id')
    issue_type_id = models.IntegerField(blank=True, null=True,verbose_name='jira project issue type id')
    fields_config_json = models.CharField(max_length=2000, verbose_name='字段对应关系json数据', default="", null=True) #[{"key":"customfield_10310","name":"问题描述","row_proportion":0.5}]

def __str__(self):
    return self.name

class Meta:
    verbose_name = "jira字段对应信息表"
    verbose_name_plural = verbose_name