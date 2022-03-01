from django.shortcuts import render, redirect
from django.contrib import messages

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        try:
            user_obj = StaffUser.objects.get(id=request.session['id'])
        except:
            user_obj = False
        if 'id' in request.session.keys() and user_obj:
            return f(request, *args, **kwargs)

        request.session.clear()
        return redirect("login")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap


@is_authenticated
def home(request):

    try:
        staff_obj = ''
        workspace_obj = ''

        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)

        if request.session.get('is_admin') == False:
            workspace_view = WorkSpace.objects.filter(status=True, staff=user_obj)
        else:
            workspace_view = WorkSpace.objects.filter(status=True)

        if request.method == 'POST':
            invite_email = request.POST.get('email')
            workspace_id = request.POST.get('workspace')
            workspace_obj = WorkSpace.objects.get(id=workspace_id)

            try:
                staff_obj = StaffUser.objects.get(email=invite_email)
            except Exception as e:
                print('-----exception as e----', e)
                pass

            if not staff_obj in workspace_obj.staff.all():
                workspace_obj.staff.add(staff_obj)
                workspace_obj.save()
            else:
                messages.error(request, 'Member already exist in provided workspace.')


    except Exception as e:
        print('-----e----', e)
        user_obj = ''
        employees = ''
        workspace_view = ''

    page = request.GET.get('page', 1)
    paginator = Paginator(workspace_view, 6)
    try:
        workspace_view = paginator.page(page)
    except PageNotAnInteger:
        workspace_view = paginator.page(1)
    except EmptyPage:
        workspace_view = paginator.page(paginator.num_pages)         
    data = {
        'obj': user_obj, 'employees':employees, 
        'workspace_view': workspace_view, 
        'len_work':len(workspace_view), 
    }
    return render(request,'dashboard/home.html', data)


@is_authenticated
def workspace_edit(request, id):
    
    workspace_obj = WorkSpace.objects.get(id=id)
    if request.method == 'POST':
        form = WorkspaceUpdateForm(request.POST, instance=workspace_obj)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = WorkspaceUpdateForm(instance=workspace_obj)
    return render(request, 'dashboard/workspace_update.html', {'object':workspace_obj})

