from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'workspace', 'assigned_to', 'priority', 'task_status', 'description', 'planned_start_date', 'planned_end_date', 'file']


class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['name', 'staff', 'slug']
        extra_kwargs = {
            'slug':{
                'read_only':True,
            },
        }


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'workspace', 'assigned_to', 'priority', 'issue_status', 'description', 'planned_start_date', 'planned_end_date', 'file']
