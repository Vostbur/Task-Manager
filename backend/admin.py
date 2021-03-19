from django.contrib import admin

from .models import Project, Task


class TaskInLine(admin.TabularInline):
    model = Task


class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInLine, ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)
