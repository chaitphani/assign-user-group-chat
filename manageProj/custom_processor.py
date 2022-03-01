from operator import truediv
from dashboard.models import StaffUser, WorkSpace


def get_members(request):

    try:
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        members = StaffUser.objects.filter(active_status=True).order_by('name')
        all_staff = StaffUser.objects.filter(active_status=True, is_employee=True).order_by('name')
        workspaces = WorkSpace.objects.all().order_by('name')
    except:
        user_obj= ''
        members = ''
        all_staff = ''
        workspaces = ''

    return {'obj': user_obj, 'members':members, 'all_staff':all_staff, 'workspaces':workspaces}