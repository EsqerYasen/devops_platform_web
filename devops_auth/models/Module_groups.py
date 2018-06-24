from django.db import models

# 系统模块组关联表
class Module_groups(models.Model):
    module_id = models.IntegerField(verbose_name="模块ID", null=False)
    group_id = models.IntegerField(verbose_name="模块组ID", null=False)

def __str__(self):
    return self.name

class Meta:
    verbose_name = "系统模块组关联表"
    verbose_name_plural = verbose_name