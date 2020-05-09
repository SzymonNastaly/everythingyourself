from .models import VideoTemplate

template_queryset = VideoTemplate.objects.all()
pre_templates = list(set([template.name for template in template_queryset]))
templates = [(name, name) for name in pre_templates]
# default for first deployment/pre-migrations:
# templates = [("template1", "template1"), ("template2", "template2")]