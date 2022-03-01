from django.contrib import admin
from .models import *


class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_admin', 'is_employee', 'created_on')
    list_filter = ('active_status',)
    date_hierarchy = 'created_on'


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'issue_status', 'workspace')
    list_filter = ('issue_status', 'issue_type')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'task_status', 'workspace')
    list_filter = ('task_status',)


class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'get_staff')
    date_hierarchy = 'created_on'
    
    def get_staff(self, obj):
        return obj.staff.values('name')


admin.site.register(StaffUser, StaffUserAdmin)
admin.site.register(WorkSpace, WorkspaceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(TaskComment)