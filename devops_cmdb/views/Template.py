import json
import uuid
from django.conf import settings
import os
from .models import TemplateTable, TemplateHistory
from django.utils import timezone

class Template():
    path = os.path.join(settings.STATIC_ROOT, 'cmdb', 'cell_templates')

    def __init__(self, template):
        self.template = template
        self.template_id = None if not 'id' in template.keys() else template['template_id']
    
    def save(self):
        file_name = str(uuid.uuid1())
        file_path = os.path.join(Template.path, file_name)
        with open(file_path, 'w') as template_file:
            template_file.write(json.dumps(self.template))
        data = dict(
            name = self.template['name'],
            # business = self.template['business'],
            user = self.template['creator'],
            update_time = timezone.now(),
            file_name = file_name
        )
        t = TemplateTable.objects.create(**data)
        t.save()
        return t.id

    def update(self, template_id):
        file_name = str(uuid.uuid1())
        file_path = os.path.join(Template.path, file_name)
        with open(file_path, 'w') as template_file:
            template_file.write(json.dumps(self.template))
        TemplateTable.objects.filter(id=template_id).update(
            file_name=file_name,
            update_time=timezone.now()
        )
    
    @staticmethod
    def delete(template_id):
        tmp = list(TemplateTable.objects.filter(id=template_id))
        file_name = tmp[0].file_name
        file_path = os.path.join(Template.path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        TemplateTable.objects.filter(id=template_id).delete()

    @staticmethod
    def get(template_id):
        """
        query the content of template file by id
        """
        try:
            tmp = list(TemplateTable.objects.filter(id=template_id))
            file_name = tmp[0].file_name
            file_path = os.path.join(Template.path, file_name)
            with open(file_path) as template_file:
                ret = json.load(template_file)
            ret.update(id=tmp[0].id)
        except:
            return None
        return ret

    @staticmethod
    def get_file_name(template_id):
        tmp = list(TemplateTable.objects.filter(id=template_id))
        file_name = tmp[0].file_name
        return file_name

    @staticmethod
    def list_templates():
        return list(TemplateTable.objects.filter().values())

    @staticmethod
    def add_log(history_log):
        history_log.update(dict(time=timezone.now()))
        t_history = TemplateHistory.objects.create(**history_log)
        t_history.save()

    @staticmethod
    def get_log(template_id):
        """
        query log of a template by id
        """
        t_logs = list(TemplateHistory.objects.filter(template_id=template_id).values())
        return t_logs