from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dashboard.models import *
from dashboard.serializers import *
from dashboard.views.dashboard_views import is_authenticated

import re


class TaskView(APIView):

    serializer_class = TaskSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        logged_in_mem = StaffUser.objects.get(id=request.session.get('id'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serialize = serializer.save()
                serialize.task_id = 'Task-' + str(serialize.id)
                serialize.assigned_by = logged_in_mem
                serialize.save()
                workspace_obj = WorkSpace.objects.get(id=serializer.data.get('workspace'))

                messages.success(request, 'Task add success...!')
                return redirect('/' + workspace_obj.slug) 
            else:
                messages.error(request, 'No workspace to assign task...!')
                return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkSpaceView(APIView):

    serializer_class = WorkSpaceSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serialize = serializer.save()
            slug_name = serialize.name.lower()
            serialize.slug = re.sub("[$₹%\‘@’+;()/:&!?.'|*^–,`~#]", "", slug_name).replace(" ", "-")
            serialize.save()

            workspace_mem_list_email = []
            for mem in serializer.data.get('staff'):
                staff_mem = StaffUser.objects.get(id=mem)
                workspace_mem_list_email.append(staff_mem.email)

            messages.success(request, 'Work space add success...')
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueView(APIView):

    serializer_class = IssueSerializer

    @method_decorator(is_authenticated)
    def post(self, request):
        logged_in = StaffUser.objects.get(id=request.session.get('id'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if len(WorkSpace.objects.filter(status=True)) > 0:
                serialize = serializer.save()
                serialize.issue_id = 'Issue-1' + str(serialize.id)
                serialize.assigned_by = logged_in
                serialize.save()

                workspace_obj = WorkSpace.objects.get(id=serializer.data.get('workspace'))
                messages.success(request, 'Issue add success...')
                return redirect('/' + workspace_obj.slug)
            else:
                messages.error(request, 'No workspace to assign issue...!')
                return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentView(APIView):

    def post(self, request, task_id):
        try:
            task_obj = Task.objects.get(id=task_id)
            user_obj = StaffUser.objects.get(id=request.session.get('id'))
            comment_obj = TaskComment.objects.create(user=user_obj, task=task_obj, comment=request.data.get('comment'), status=True)
            comment_obj.save()
            return redirect('/'+ str(task_obj.workspace.slug) +'/'+ str(task_obj.id) +'/task')
        except Exception as e:
            return Response({'error':'Task obj not found with the id..'}, status=status.HTTP_404_NOT_FOUND)


class IssueCommentView(APIView):

    def post(self, request, issue_id):
        try:
            issue_obj = Issue.objects.get(id=issue_id)
            user_obj = StaffUser.objects.get(id=request.session.get('id'))
            
            comment_obj = IssueComment.objects.create(user=user_obj, issue=issue_obj, comment=str(request.data.get('comment')), status=True)
            comment_obj.save()

            return redirect('/' + str(issue_obj.workspace.slug) + '/' + str(issue_obj.id) + '/issue')
        except Exception as e:
            print('----exception as e-----', e)
            return Response({'error':'Issue obj not found with the id..'}, status=status.HTTP_404_NOT_FOUND)
