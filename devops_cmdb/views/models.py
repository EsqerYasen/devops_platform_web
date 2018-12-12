from django.db import models

class TemplateTable(models.Model):
    name = models.CharField(max_length=50)
    # business = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    update_time = models.DateTimeField()
    file_name = models.CharField(max_length=50)
    class Meta:
        unique_together = ('name', 'business',)

class TemplateHistory(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField()
    template_id = models.CharField(max_length=50)
    action = models.CharField(max_length=10)
    file_name = models.CharField(max_length=50)