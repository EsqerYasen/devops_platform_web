from django.db import models

# 系统模块表
class Module(models.Model):
    name = models.CharField(max_length=255, verbose_name="模块名称", null=False)
    alias = models.CharField(max_length=255, verbose_name="模块别名", null=False)
    url = models.CharField(max_length=255, verbose_name="URL", null=False)
    owner_id = models.IntegerField(verbose_name="Owner ID", null=False)
    is_enabled = models.NullBooleanField(verbose_name='是否启用', default=True, null=False, blank=False)
    created_by = models.CharField(max_length=255, verbose_name='创建人')
    updated_by = models.CharField(max_length=255, verbose_name='最后更新人')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "系统模块表"
        verbose_name_plural = verbose_name