from django.shortcuts import redirect
from django.http import HttpResponse


def common_data(list1, list2):
    result = False
    for x in list1:
        for y in list2:
            if x == y:
                result = True
                return result
    return result


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            L=[]
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for g in groups:
                    L.append(g.name)
            if common_data(L, allowed_roles):
                return view_func(request, *args, **kwargs)
            return HttpResponse('Not Authorised')
        return wrapper_func
    return decorator
