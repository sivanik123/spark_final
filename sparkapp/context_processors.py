# attendance/context_processors.py

from django.contrib.auth.models import Group

def is_teacher(request):
    return {'is_teacher': request.user.groups.filter(name='Teacher').exists()}

def is_admin(request):
    return {'is_admin': request.user.groups.filter(name='Admin').exists()}

def is_principal(request):
    return {'is_principal': request.user.groups.filter(name='Principal').exists()}