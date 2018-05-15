from django.db import models

# jira字段对应信息表
class External_system_user_mapping(models.Model):
    external_system_username = models.CharField(max_length=255, verbose_name="外部系统用户名", null=True)
    external_system_password = models.CharField(max_length=255, verbose_name="外部系统密码", null=True)
    external_system = models.CharField(max_length=255, verbose_name="外部系统名称", null=True)
    inner_user_group = models.CharField(max_length=10, verbose_name="内部系统账户组", null=True)
    inner_user_name = models.CharField(max_length=30, verbose_name="内部系统用户名称", null=True)

def __str__(self):
    return self.name

class Meta:
    verbose_name = "jira字段对应信息表"
    verbose_name_plural = verbose_name