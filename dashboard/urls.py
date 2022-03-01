from django.urls import path
from dashboard.views import dashboard_views as dash_views
from dashboard.views import api_views
from dashboard import helpers as helper_views
from dashboard.views import auth_views
from dashboard.views import workspace_views


urlpatterns = (

    path('', dash_views.home, name='home'),
    path('workspace/<int:id>/update', dash_views.workspace_edit, name='workspace-edit'),

    path('login', auth_views.login, name='login'),
    path('signup', auth_views.signup, name='signup'),
    path('logout', auth_views.logout, name='logout'),

    path('task-status', helper_views.tasK_status_change, name='task-status'),
    path('issue-status', helper_views.issue_status_change, name='issue-status'),

    path('api/task', api_views.TaskView.as_view(), name='task-add'),
    path('api/issue', api_views.IssueView.as_view(), name='issue-add'),
    path('api/work-space', api_views.WorkSpaceView.as_view(), name='work-space-add'),
    path('api/comment/task/<int:task_id>', api_views.TaskCommentView.as_view(), name='task-comment-add'),
    path('api/comment/issue/<int:issue_id>', api_views.IssueCommentView.as_view(), name='issue-comment-add'),

    path('<slug:name>', workspace_views.workspace_view, name='workspace'),
    path('<slug:workspace_slug>/<int:id>/task', workspace_views.task_detail_update_view, name='task-edit'),
    path('<slug:workspace_slug>/<int:id>/issue', workspace_views.issue_detail_update_view, name='issue-edit'),

    path('<int:id>/task/delete', workspace_views.task_delete, name='task-delete'),
    path('<int:id>/issue/delete', workspace_views.issue_delete, name='issue-delete'),

)