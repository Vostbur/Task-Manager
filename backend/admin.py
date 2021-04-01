from django.contrib import admin

from .models import Project, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'project', 'is_done')


class TaskInLine(admin.TabularInline):
    model = Task


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'user')
    ordering = ['id']
    inlines = [TaskInLine, ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
