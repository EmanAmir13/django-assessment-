from django.contrib import admin

from api.models.project import Project
from api.models.task import Task
from api.models.user import User

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)
