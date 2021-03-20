from django.contrib import admin

from .models import Project, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_done')


class TaskInLine(admin.TabularInline):
    model = Task


class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInLine, ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
