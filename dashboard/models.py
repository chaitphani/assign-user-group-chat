from django.db import models
from django.contrib.auth.models import User


priority_choices = (('1', 'High'),('2', 'Medium'),('3', 'Low'), ('4', 'Critical'), )
task_status_choices = (('1', 'Not Started'),('2', 'In Progress'),('3', 'In Review'),('4', 'Completed'),('5', 'Blocked'),)
issue_type = (('1','Bug'), ('2', 'Feature'), ('3', 'Improvement'))


class StaffUser(models.Model):

    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active_status = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class WorkSpace(models.Model):

    name = models.CharField(max_length=120)
    slug = models.CharField(max_length=120)

    staff = models.ManyToManyField(StaffUser)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class Task(models.Model):

    task_id = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_assigned_to')
    priority = models.CharField(max_length=10, choices=priority_choices, default='2')
    task_status = models.CharField(max_length=15, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_assigned_by')

    file = models.FileField(upload_to ='media/task', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)


class Issue(models.Model):

    issue_id = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_assigned_to')
    issue_type = models.CharField(max_length=20, choices=issue_type, default='1')
    priority = models.CharField(max_length=10, choices=priority_choices, default='2')
    issue_status = models.CharField(max_length=15, choices=task_status_choices, default='2')
    description = models.TextField(null=True, blank=True)

    planned_start_date = models.DateTimeField(null=True, blank=True)
    planned_end_date = models.DateTimeField(null=True, blank=True)

    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_assigned_by')

    file = models.FileField(upload_to ='media/issue', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)


class TaskComment(models.Model):

    user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.task)


class IssueComment(models.Model):

    user = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.issue)
        
